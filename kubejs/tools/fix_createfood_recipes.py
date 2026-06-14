#!/usr/bin/env python3
"""
Arcadia V2 - CreateFood recipe format fixer.

CreateFood ships its Create processing-recipe ITEM outputs in a nested shape
that the stable Create (6.0.10/6.0.11) ProcessingOutput codec cannot parse:

    "results": [ { "item": { "id": "createfood:x" }, "count": 2, "chance": 0.5 } ]

Create expects the item id FLAT:

    "results": [ { "id": "createfood:x", "count": 2, "chance": 0.5 } ]

Affected recipes are silently skipped at load -> the food exists but is not
craftable via Create machines. This script reads the recipe JSONs straight out
of the CreateFood jar, flattens the nested item outputs, and writes the fixed
copies into kubejs/data/<namespace>/recipe/... as datapack overrides (datapack
recipes take precedence over a mod's bundled ones at the same id).

Only recipes whose outputs are actually nested are emitted; everything else is
left to the mod. Fluid outputs ({amount,id}) and all ingredients are copied
verbatim (the codec accepts them as-is; only results are the documented break).

Usage (from the instance root):
    python kubejs/tools/fix_createfood_recipes.py

Re-run after updating CreateFood; it auto-detects the newest createfood*.jar.

Author: vyrriox
"""

import glob
import json
import os
import sys
import zipfile

INSTANCE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MODS_DIR = os.path.join(INSTANCE_ROOT, "mods")
# Datapack override target. KubeJS exposes kubejs/data as a datapack namespace root.
OUT_ROOT = os.path.join(INSTANCE_ROOT, "kubejs", "data")
GENERATED_MARKER = "createfood"  # only ever write/cleanup under this namespace


def find_createfood_jar():
    jars = sorted(glob.glob(os.path.join(MODS_DIR, "createfood*.jar")))
    return jars[-1] if jars else None


def result_is_nested(result):
    """A result entry whose item id is wrapped in an 'item' object."""
    return isinstance(result, dict) and isinstance(result.get("item"), dict)


def flatten_result(result):
    """{'item':{'id':X,'count':C}, count, chance} -> {'id':X, 'count', 'chance'}."""
    out = {}
    inner = result.get("item")
    if isinstance(inner, dict):
        if "id" in inner:
            out["id"] = inner["id"]
        if "count" in inner:
            out["count"] = inner["count"]
    elif "id" in result:
        out["id"] = result["id"]
    # Top-level wrappers win over the inner ones if both are present.
    if "count" in result:
        out["count"] = result["count"]
    if "chance" in result:
        out["chance"] = result["chance"]
    if "amount" in result:  # fluid output, keep as-is
        out["amount"] = result["amount"]
    return out


# CreateFood writes fluid ingredients with custom type ids that the stable
# Create / NeoForge fluid_ingredient registry does not know. Map them to the
# native NeoForge fluid ingredient types Create expects.
def fluid_ingredient_needs_fix(ing):
    return isinstance(ing, dict) and ing.get("type") in (
        "fluid_tag", "fluid_stack", "fluid",
    )


def fix_fluid_ingredient(ing):
    t = ing.get("type")
    amount = ing.get("amount")
    if t == "fluid_tag":
        # {type:fluid_tag, amount, fluid_tag:X} -> {type:neoforge:tag, amount, tag:X}
        out = {"type": "neoforge:tag"}
        if amount is not None:
            out["amount"] = amount
        out["tag"] = ing.get("fluid_tag")
        return out
    # fluid_stack / fluid -> {type:neoforge:single, amount, fluid:X}
    out = {"type": "neoforge:single"}
    if amount is not None:
        out["amount"] = amount
    out["fluid"] = ing.get("fluid")
    if "nbt" in ing:
        out["nbt"] = ing["nbt"]
    return out


def recipe_needs_fix(data):
    results = data.get("results")
    if isinstance(results, list) and any(result_is_nested(r) for r in results):
        return True
    ingredients = data.get("ingredients")
    if isinstance(ingredients, list) and any(
        fluid_ingredient_needs_fix(i) for i in ingredients
    ):
        return True
    return False


def fix_recipe(data):
    fixed = dict(data)  # shallow copy preserves type, flags, conditions
    results = data.get("results")
    if isinstance(results, list):
        fixed["results"] = [
            flatten_result(r) if result_is_nested(r) else r for r in results
        ]
    ingredients = data.get("ingredients")
    if isinstance(ingredients, list):
        fixed["ingredients"] = [
            fix_fluid_ingredient(i) if fluid_ingredient_needs_fix(i) else i
            for i in ingredients
        ]
    return fixed


def main():
    jar_path = find_createfood_jar()
    if not jar_path:
        print("ERROR: no createfood*.jar found in", MODS_DIR)
        return 1
    print("Reading:", os.path.basename(jar_path))

    written = 0
    scanned = 0
    written_paths = []

    with zipfile.ZipFile(jar_path) as jar:
        for entry in jar.namelist():
            # CreateFood lays recipes under data/<ns>/recipe/... ; only the
            # create/* processing recipes carry the nested-output break.
            if not entry.endswith(".json"):
                continue
            if "/recipe/create/" not in entry:
                continue
            scanned += 1
            try:
                data = json.loads(jar.read(entry).decode("utf-8"))
            except Exception:
                continue
            if not data.get("type") or not recipe_needs_fix(data):
                continue
            fixed = fix_recipe(data)

            # Mirror the jar's internal path verbatim into kubejs/data so the id
            # matches the original recipe and the override replaces it.
            rel = entry[entry.index("data/") + len("data/"):]
            out_path = os.path.join(OUT_ROOT, *rel.split("/"))
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(fixed, f, separators=(",", ":"))
            written += 1
            written_paths.append(out_path)

    print(f"Scanned {scanned} create/* recipes, wrote {written} flattened overrides.")
    if written_paths:
        print("Output root:", os.path.join(OUT_ROOT, GENERATED_MARKER, "recipe", "create"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
