"""
Deploy v2: merge audit2/agent_output into kubejs/assets/<modid>/lang/fr_fr.json.
- For each agent_output file: load it.
- Load existing kubejs fr_fr.json (if any).
- Merge: NEW translations (from agent_output) take priority over existing kubejs entries
  (because agent_output may contain re-translated/fixed entries).
- BUT only add keys that don't already have a "good" translation. Heuristic: existing key
  whose value is identical to en_us is bad → replace with agent's version.
- Validate JSON.
- Write into kubejs.
- Backup kubejs originals.
"""
import json
import os
import shutil
from datetime import datetime

WS = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace"
KJS = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/kubejs/assets"
SRC = os.path.join(WS, "audit2", "agent_output")
EN_DIR = os.path.join(WS, "audit2", "all_en")
JAR_FR_DIR = os.path.join(WS, "audit2", "all_jar_fr")
BACKUP = os.path.join(WS, "audit2", "kubejs_backup_" + datetime.now().strftime("%Y%m%d_%H%M%S"))


def parse_lang(path):
    if not path or not os.path.exists(path):
        return {}
    try:
        if path.endswith(".json"):
            with open(path, encoding="utf-8-sig") as f:
                d = json.load(f)
            return d if isinstance(d, dict) else {}
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
        return {}


written = []
parse_errors = []
total_keys_added = 0
total_keys_replaced = 0

os.makedirs(BACKUP, exist_ok=True)

for fname in sorted(os.listdir(SRC)):
    if not fname.endswith(".json"):
        continue
    modid = fname[:-5]
    src_path = os.path.join(SRC, fname)
    try:
        with open(src_path, encoding="utf-8") as f:
            agent_data = json.load(f)
        if not isinstance(agent_data, dict) or not agent_data:
            parse_errors.append((modid, "empty or not dict"))
            continue
    except Exception as e:
        parse_errors.append((modid, str(e)))
        continue

    target_dir = os.path.join(KJS, modid, "lang")
    target = os.path.join(target_dir, "fr_fr.json")
    os.makedirs(target_dir, exist_ok=True)

    existing = parse_lang(target) if os.path.exists(target) else {}

    # Get EN to detect "FR == EN" entries to replace
    en_data = {}
    for ext in ("json", "lang"):
        en_data = parse_lang(os.path.join(EN_DIR, f"{modid}.{ext}"))
        if en_data:
            break

    # Backup existing if it had content
    if existing and os.path.exists(target):
        shutil.copy2(target, os.path.join(BACKUP, f"{modid}.json"))

    # Merge logic:
    #  - Start with existing
    #  - For each agent key:
    #      if key not in existing: add it (count "added")
    #      elif existing[key] == en_data.get(key, '_NONE_'): replace it (count "replaced")
    #      else: keep existing (manual translation has priority)
    merged = dict(existing)
    added = 0
    replaced = 0
    for k, v in agent_data.items():
        if k not in merged:
            merged[k] = v
            added += 1
        elif (
            isinstance(merged[k], str)
            and isinstance(en_data.get(k), str)
            and merged[k].strip() == en_data[k].strip()
            and len(en_data[k].strip()) >= 4
        ):
            # Existing was just an EN copy — replace with agent's translation
            merged[k] = v
            replaced += 1
        # else: keep existing

    if added or replaced:
        with open(target, "w", encoding="utf-8") as f:
            json.dump(merged, f, ensure_ascii=False, indent="\t", sort_keys=False)
        written.append((modid, added, replaced, len(merged)))
        total_keys_added += added
        total_keys_replaced += replaced

# Report
print(f"=== DEPLOY V2 REPORT ===")
print(f"Files updated: {len(written)}")
print(f"Total keys added (new): {total_keys_added}")
print(f"Total keys replaced (FR=EN -> proper FR): {total_keys_replaced}")
print(f"Parse errors: {len(parse_errors)}")
print(f"Backup: {BACKUP}")
print()

if written:
    written.sort(key=lambda x: -(x[1] + x[2]))
    print("Top 30 by changes:")
    for m, a, r, t in written[:30]:
        print(f"  {m:<35s}  +{a:5d} added  ~{r:5d} replaced  total={t}")

if parse_errors:
    print()
    print("Errors:")
    for m, e in parse_errors[:20]:
        print(f"  {m}: {e[:80]}")

# Save manifest
with open(os.path.join(WS, "audit2", "deploy_v2_manifest.json"), "w", encoding="utf-8") as f:
    json.dump({
        "written": [{"modid": m, "added": a, "replaced": r, "total": t} for m, a, r, t in written],
        "errors": [{"modid": m, "error": e} for m, e in parse_errors],
        "total_added": total_keys_added,
        "total_replaced": total_keys_replaced,
        "backup_dir": BACKUP,
    }, f, ensure_ascii=False, indent=2)
