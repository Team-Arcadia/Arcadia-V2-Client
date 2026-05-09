"""
Deploy translated fr_fr.json files into kubejs/assets/<modid>/lang/fr_fr.json.

Strategy:
- If KubeJS already has a fr_fr.json for this modid, MERGE intelligently:
  * Keep existing translations (manual work has priority)
  * Add new keys from agent output that don't exist locally
- If no KubeJS file: copy agent output as-is.
- Validate JSON before writing.
- Save backup of merged files into translation_workspace/backups/.
"""
import json, os, sys, shutil
from datetime import datetime

WS = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace"
KJS = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/kubejs/assets"

src_dir = os.path.join(WS, "agent_output")
backup_dir = os.path.join(WS, "backups", datetime.now().strftime("%Y%m%d_%H%M%S"))
os.makedirs(backup_dir, exist_ok=True)

if not os.path.isdir(src_dir):
    print(f"FATAL: source dir missing: {src_dir}")
    sys.exit(1)

written_new = []
merged = []
parse_errors = []
total_keys_new = 0
total_keys_merged_added = 0

for fname in sorted(os.listdir(src_dir)):
    if not fname.endswith(".json"):
        continue
    modid = fname[:-5]
    src = os.path.join(src_dir, fname)

    try:
        with open(src, encoding="utf-8") as f:
            agent_data = json.load(f)
        if not isinstance(agent_data, dict) or not agent_data:
            parse_errors.append((modid, "empty or not dict"))
            continue
    except Exception as e:
        parse_errors.append((modid, f"agent_output: {e}"))
        continue

    target_dir = os.path.join(KJS, modid, "lang")
    target = os.path.join(target_dir, "fr_fr.json")
    os.makedirs(target_dir, exist_ok=True)

    if os.path.exists(target):
        # Merge: existing wins, add missing keys from agent
        try:
            with open(target, encoding="utf-8") as f:
                existing = json.load(f)
        except Exception as e:
            parse_errors.append((modid, f"existing: {e}"))
            continue

        # Backup existing
        shutil.copy2(target, os.path.join(backup_dir, f"{modid}_existing.json"))

        if not isinstance(existing, dict):
            parse_errors.append((modid, "existing not dict"))
            continue

        added = 0
        merged_data = dict(existing)  # priority: existing
        for k, v in agent_data.items():
            if k not in merged_data:
                merged_data[k] = v
                added += 1

        with open(target, "w", encoding="utf-8") as f:
            json.dump(merged_data, f, ensure_ascii=False, indent="\t", sort_keys=False)

        merged.append((modid, len(existing), len(agent_data), added, len(merged_data)))
        total_keys_merged_added += added
    else:
        # Fresh write
        shutil.copy2(src, target)
        written_new.append((modid, len(agent_data)))
        total_keys_new += len(agent_data)

print(f"=== DEPLOYMENT REPORT ===")
print(f"Fresh files written: {len(written_new)}  ({total_keys_new} keys)")
print(f"Merged into existing: {len(merged)}  ({total_keys_merged_added} new keys added)")
print(f"Parse errors: {len(parse_errors)}")
print()

if written_new:
    print("=== Fresh writes (top 25 by keys) ===")
    for m, n in sorted(written_new, key=lambda x: -x[1])[:25]:
        print(f"  {m:40s}  +{n:5d} keys")

if merged:
    print()
    print("=== Merged (top 20 by keys added) ===")
    for m, ex, ag, add, total in sorted(merged, key=lambda x: -x[3])[:20]:
        print(f"  {m:40s}  existing={ex:5d}  agent={ag:5d}  added={add:5d}  -> total={total}")

if parse_errors:
    print()
    print("=== Parse errors ===")
    for m, e in parse_errors:
        print(f"  {m}: {e[:80]}")

with open(os.path.join(WS, "deployment_manifest.json"), "w", encoding="utf-8") as f:
    json.dump({
        "fresh_writes": [{"modid": m, "keys": n} for m, n in written_new],
        "merged": [{"modid": m, "existing": ex, "agent": ag, "added": add, "total": total}
                   for m, ex, ag, add, total in merged],
        "parse_errors": [{"modid": m, "error": e} for m, e in parse_errors],
        "total_keys_fresh": total_keys_new,
        "total_keys_added_via_merge": total_keys_merged_added,
        "backup_dir": backup_dir,
    }, f, ensure_ascii=False, indent=2)

print()
print(f"Backup of existing files: {backup_dir}")
