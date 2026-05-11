"""
Merge phase3_output/bin_*.json (multi-lang structure) into SNBT files.
Format expected:
  {
    "<quest_id>": {
      "en_us": {"title": "...", "quest_subtitle": "...", "quest_desc": [...]},
      "fr_fr": {...},
      ...
    }
  }
"""
import json
import os
import re
import sys

WS = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/ftbq_audit"
LANG_DIR = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/config/ftbquests/quests/lang"
DEFAULT_DIR = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/defaultconfigs/ftbquests/quests/lang"

sys.path.insert(0, WS)
from merge_other_langs import parse_snbt_to_entries
from merge_phase2 import serialize_entry


def main():
    # Aggregate per-lang fills
    per_lang = {l: {} for l in ("en_us", "en_gb", "fr_fr", "es_es", "pt_br", "ru_ru", "zh_cn")}
    bins_dir = os.path.join(WS, "phase3_output")
    if not os.path.isdir(bins_dir):
        print(f"No phase3_output dir: {bins_dir}")
        return
    for f in sorted(os.listdir(bins_dir)):
        if not f.endswith(".json"):
            continue
        d = json.load(open(os.path.join(bins_dir, f), encoding="utf-8"))
        for qid, langs in d.items():
            for lang, fields in langs.items():
                if lang not in per_lang:
                    continue
                if "title" in fields:
                    per_lang[lang][f"quest.{qid}.title"] = fields["title"]
                if "quest_subtitle" in fields:
                    per_lang[lang][f"quest.{qid}.quest_subtitle"] = fields["quest_subtitle"]
                if "quest_desc" in fields:
                    per_lang[lang][f"quest.{qid}.quest_desc"] = fields["quest_desc"]

    for lang, fills in per_lang.items():
        if not fills:
            print(f"  {lang}: no fills")
            continue
        print(f"\n{lang}: {len(fills)} fills")
        for d in (LANG_DIR, DEFAULT_DIR):
            tgt = os.path.join(d, f"{lang}.snbt")
            with open(tgt, encoding="utf-8") as fp:
                text = fp.read()
            prefix, entries, suffix = parse_snbt_to_entries(text)
            key_to_idx = {k: i for i, (k, _) in enumerate(entries)}
            applied = added = 0
            for k, v in fills.items():
                new_lines = serialize_entry(k, v)
                if k in key_to_idx:
                    entries[key_to_idx[k]] = (k, new_lines)
                    applied += 1
                else:
                    entries.append((k, new_lines))
                    added += 1
            out_lines = prefix + [ln for _, blk in entries for ln in blk] + suffix
            with open(tgt, "w", encoding="utf-8") as fp:
                fp.write("\n".join(out_lines))
            print(f"  {os.path.basename(d)}/{lang}: applied={applied}, added={added}")


if __name__ == "__main__":
    main()
