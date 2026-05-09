"""
Find keys where FR value == EN value (truly untranslated despite being present in fr_fr.json).
Per-mod, write the missing-to-translate file with these untranslated entries.
"""
import json
import os
import re

WS = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace"
KJS = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/kubejs/assets"
EN_DIR = os.path.join(WS, "audit2", "all_en")
JAR_FR_DIR = os.path.join(WS, "audit2", "all_jar_fr")
OUT = os.path.join(WS, "audit2", "untranslated_per_mod")
os.makedirs(OUT, exist_ok=True)


def parse_lang(path):
    if not os.path.exists(path):
        return None
    try:
        if path.endswith(".json"):
            with open(path, encoding="utf-8-sig") as f:
                d = json.load(f)
            return d if isinstance(d, dict) else None
        else:
            data = {}
            with open(path, encoding="utf-8-sig") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        k, v = line.split("=", 1)
                        data[k.strip()] = v.strip()
            return data
    except Exception:
        return None


# Build modid set
all_modids = set()
for f in os.listdir(EN_DIR):
    modid = f.rsplit(".", 1)[0]
    all_modids.add(modid)

results = []
for modid in sorted(all_modids):
    en = None
    for ext in ("json", "lang"):
        en = parse_lang(os.path.join(EN_DIR, f"{modid}.{ext}"))
        if en is not None:
            break
    if en is None:
        continue

    jar_fr = None
    for ext in ("json", "lang"):
        jar_fr = parse_lang(os.path.join(JAR_FR_DIR, f"{modid}.{ext}"))
        if jar_fr is not None:
            break
    if jar_fr is None:
        jar_fr = {}

    kjs_fr = parse_lang(os.path.join(KJS, modid, "lang", "fr_fr.json")) or {}

    # Combined FR (kubejs has priority)
    combined = dict(jar_fr)
    combined.update(kjs_fr)

    untranslated = {}
    for k, en_v in en.items():
        if not isinstance(en_v, str) or not en_v.strip():
            continue
        if len(en_v.strip()) < 4:
            continue
        fr_v = combined.get(k)
        if isinstance(fr_v, str) and fr_v.strip() == en_v.strip():
            # Skip very short or proper-noun-likely entries
            # Heuristic: contains lowercase letter forming a word
            if re.search(r"[a-z]{3,}", en_v):
                untranslated[k] = en_v

    if untranslated:
        with open(os.path.join(OUT, f"{modid}.json"), "w", encoding="utf-8") as f:
            json.dump(untranslated, f, ensure_ascii=False, indent="\t", sort_keys=False)
        results.append((modid, len(untranslated)))

results.sort(key=lambda x: -x[1])
print(f"Total mods with untranslated FR keys: {len(results)}")
print(f"Total untranslated keys: {sum(n for _, n in results)}")
print()
print("Top 30:")
for modid, n in results[:30]:
    print(f"  {modid:<40s}  {n:5d}")

# Save list
with open(os.path.join(WS, "audit2", "untranslated_summary.json"), "w", encoding="utf-8") as f:
    json.dump([{"modid": m, "count": n} for m, n in results], f, ensure_ascii=False, indent=2)
