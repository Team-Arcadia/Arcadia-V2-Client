"""
Build a global dictionary of mod items:
  item_id -> { en_name, fr_name, mod }
Used to validate quest descriptions reference the right items.
"""
import json
import os
import re
import zipfile

MODS_DIR = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/mods"
WS = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/ftbq_audit"


def extract_lang(jar_path, lang_code):
    """Extract en_us or fr_fr lang from a jar — return dict of item_id -> name."""
    try:
        with zipfile.ZipFile(jar_path) as z:
            for name in z.namelist():
                # Match assets/<modid>/lang/<lang>.json
                m = re.match(rf"assets/([^/]+)/lang/{lang_code}\.json$", name)
                if not m:
                    continue
                modid = m.group(1)
                try:
                    data = json.loads(z.read(name).decode("utf-8", errors="replace"))
                except Exception:
                    continue
                yield modid, data
    except Exception:
        return


def main():
    all_items = {}  # full_id -> { name_en, name_fr, mod }
    all_entities = {}  # full_id -> { name_en, name_fr, mod }
    jar_count = 0
    for jar_name in sorted(os.listdir(MODS_DIR)):
        if not jar_name.endswith(".jar"):
            continue
        jar_path = os.path.join(MODS_DIR, jar_name)
        jar_count += 1

        # EN first
        en_entries = {}
        for modid, data in extract_lang(jar_path, "en_us"):
            for k, v in data.items():
                if k.startswith("item.") or k.startswith("block."):
                    parts = k.split(".", 2)
                    if len(parts) < 3:
                        continue
                    if parts[1] != modid:
                        continue
                    item_id = f"{parts[1]}:{parts[2]}"
                    all_items.setdefault(item_id, {})["name_en"] = v
                    all_items[item_id]["mod"] = modid
                elif k.startswith("entity."):
                    parts = k.split(".", 2)
                    if len(parts) < 3:
                        continue
                    if parts[1] != modid:
                        continue
                    ent_id = f"{parts[1]}:{parts[2]}"
                    all_entities.setdefault(ent_id, {})["name_en"] = v
                    all_entities[ent_id]["mod"] = modid

        # FR
        for modid, data in extract_lang(jar_path, "fr_fr"):
            for k, v in data.items():
                if k.startswith("item.") or k.startswith("block."):
                    parts = k.split(".", 2)
                    if len(parts) < 3:
                        continue
                    item_id = f"{parts[1]}:{parts[2]}"
                    if item_id in all_items:
                        all_items[item_id]["name_fr"] = v
                elif k.startswith("entity."):
                    parts = k.split(".", 2)
                    if len(parts) < 3:
                        continue
                    ent_id = f"{parts[1]}:{parts[2]}"
                    if ent_id in all_entities:
                        all_entities[ent_id]["name_fr"] = v

    # Also pull from kubejs assets (where I added FR translations earlier)
    kjs_dir = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/kubejs/assets"
    if os.path.isdir(kjs_dir):
        for modid in os.listdir(kjs_dir):
            lang_path = os.path.join(kjs_dir, modid, "lang", "fr_fr.json")
            if not os.path.exists(lang_path):
                continue
            try:
                data = json.load(open(lang_path, encoding="utf-8"))
            except Exception:
                continue
            for k, v in data.items():
                if k.startswith("item.") or k.startswith("block."):
                    parts = k.split(".", 2)
                    if len(parts) < 3 or parts[1] != modid:
                        continue
                    item_id = f"{parts[1]}:{parts[2]}"
                    if item_id in all_items:
                        all_items[item_id].setdefault("name_fr", v)
                    else:
                        all_items[item_id] = {"name_fr": v, "mod": modid}
                elif k.startswith("entity."):
                    parts = k.split(".", 2)
                    if len(parts) < 3 or parts[1] != modid:
                        continue
                    ent_id = f"{parts[1]}:{parts[2]}"
                    if ent_id in all_entities:
                        all_entities[ent_id].setdefault("name_fr", v)
                    else:
                        all_entities[ent_id] = {"name_fr": v, "mod": modid}

    print(f"Jars scanned: {jar_count}")
    print(f"Items extracted: {len(all_items)}")
    print(f"Entities extracted: {len(all_entities)}")

    with open(os.path.join(WS, "mod_items.json"), "w", encoding="utf-8") as f:
        json.dump(all_items, f, ensure_ascii=False, indent=1, sort_keys=True)
    with open(os.path.join(WS, "mod_entities.json"), "w", encoding="utf-8") as f:
        json.dump(all_entities, f, ensure_ascii=False, indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
