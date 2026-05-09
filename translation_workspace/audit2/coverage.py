"""
Compute translation coverage per modid:
  - en_keys = set of keys in en_us (from jar)
  - jar_fr_keys = set of keys in fr_fr (from jar, if any)
  - kubejs_fr_keys = set of keys in fr_fr (from kubejs/assets/<modid>/lang/, if any)
  - total_fr_keys = jar_fr_keys ∪ kubejs_fr_keys
  - missing = en_keys - total_fr_keys
"""
import json
import os
import sys

WS = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace"
KJS = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/kubejs/assets"
EN_DIR = os.path.join(WS, "audit2", "all_en")
JAR_FR_DIR = os.path.join(WS, "audit2", "all_jar_fr")
OUT = os.path.join(WS, "audit2")


def parse_lang(path):
    if not os.path.exists(path):
        return {}
    try:
        if path.endswith(".json"):
            with open(path, encoding="utf-8-sig") as f:
                d = json.load(f)
            return d if isinstance(d, dict) else {}
        else:  # .lang
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
    except Exception as e:
        return {"__parse_error__": str(e)}


# Build modid set from EN_DIR
mod_files = {}  # modid -> (en_path, jar_fr_path)
for f in os.listdir(EN_DIR):
    if f.endswith(".json") or f.endswith(".lang"):
        modid = f.rsplit(".", 1)[0]
        mod_files.setdefault(modid, [None, None])
        mod_files[modid][0] = os.path.join(EN_DIR, f)
for f in os.listdir(JAR_FR_DIR):
    if f.endswith(".json") or f.endswith(".lang"):
        modid = f.rsplit(".", 1)[0]
        mod_files.setdefault(modid, [None, None])
        mod_files[modid][1] = os.path.join(JAR_FR_DIR, f)

results = []
total_en = 0
total_fr = 0
total_missing = 0

for modid in sorted(mod_files):
    en_path, jar_fr_path = mod_files[modid]
    en = parse_lang(en_path) if en_path else {}
    jar_fr = parse_lang(jar_fr_path) if jar_fr_path else {}

    # KubeJS may have the file
    kubejs_path = os.path.join(KJS, modid, "lang", "fr_fr.json")
    kubejs_fr = parse_lang(kubejs_path)

    if "__parse_error__" in en or "__parse_error__" in jar_fr or "__parse_error__" in kubejs_fr:
        results.append({
            "modid": modid,
            "en_keys": 0,
            "jar_fr_keys": 0,
            "kubejs_fr_keys": 0,
            "total_fr_keys": 0,
            "missing_count": 0,
            "missing_sample": [],
            "parse_error": en.get("__parse_error__") or jar_fr.get("__parse_error__") or kubejs_fr.get("__parse_error__"),
        })
        continue

    en_keys = set(en.keys()) - {"__parse_error__"}
    jar_fr_keys = set(jar_fr.keys()) - {"__parse_error__"}
    kubejs_fr_keys = set(kubejs_fr.keys()) - {"__parse_error__"}
    total_fr_keys = jar_fr_keys | kubejs_fr_keys
    missing = en_keys - total_fr_keys

    total_en += len(en_keys)
    total_fr += len(en_keys & total_fr_keys)
    total_missing += len(missing)

    results.append({
        "modid": modid,
        "en_keys": len(en_keys),
        "jar_fr_keys": len(jar_fr_keys),
        "kubejs_fr_keys": len(kubejs_fr_keys),
        "total_fr_keys": len(en_keys & total_fr_keys),
        "missing_count": len(missing),
        "missing_sample": sorted(missing)[:30],
    })

# Sort: most missing first
results.sort(key=lambda x: -x["missing_count"])

# Save full report
with open(os.path.join(OUT, "coverage_full.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# Print summary
print(f"=== COVERAGE SUMMARY ===")
print(f"Total mods: {len(results)}")
print(f"Total EN keys across all mods: {total_en}")
print(f"Total covered by FR (jar+kubejs): {total_fr} ({total_fr*100//max(1,total_en)}%)")
print(f"Total MISSING: {total_missing}")
print()

# Top 30 mods with most missing keys
print(f"=== TOP 40 MODS WITH MISSING TRANSLATIONS ===")
print(f"{'modid':<40s} {'EN':>5s} {'jar_FR':>7s} {'kjs_FR':>7s} {'covered':>8s} {'missing':>8s}")
for r in results[:40]:
    if r["missing_count"] == 0:
        break
    print(f"{r['modid']:<40s} {r['en_keys']:>5d} {r['jar_fr_keys']:>7d} {r['kubejs_fr_keys']:>7d} {r['total_fr_keys']:>8d} {r['missing_count']:>8d}")

# Total mods with 0 missing
fully_covered = sum(1 for r in results if r["missing_count"] == 0 and r["en_keys"] > 0)
print(f"\nMods fully covered (0 missing): {fully_covered}")

# Mods with parse errors
parse_errors = [r for r in results if r.get("parse_error")]
if parse_errors:
    print(f"\n=== {len(parse_errors)} parse errors ===")
    for r in parse_errors[:20]:
        print(f"  {r['modid']}: {r['parse_error']}")

# Save list of mods with missing keys for next step
todo = [r for r in results if r["missing_count"] > 0]
with open(os.path.join(OUT, "missing_to_fill.json"), "w", encoding="utf-8") as f:
    json.dump(todo, f, ensure_ascii=False, indent=2)
print(f"\nMods needing fill: {len(todo)} (saved to missing_to_fill.json)")
