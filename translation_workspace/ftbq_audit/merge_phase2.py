"""
Merge phase2_output/<lang>.json into <lang>.snbt files.
Handles both string and list[str] values (multi-line desc arrays).
"""
import json
import os
import re
import shutil
import sys

WS = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/ftbq_audit"
LANG_DIR = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/config/ftbquests/quests/lang"
DEFAULT_DIR = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/defaultconfigs/ftbquests/quests/lang"

sys.path.insert(0, WS)
from merge_other_langs import parse_snbt_to_entries


def escape_snbt_string(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")


def serialize_entry(k, v):
    """Return list of SNBT lines."""
    if isinstance(v, str):
        return [f'\t{k}: "{escape_snbt_string(v)}"']
    if isinstance(v, list):
        if k.endswith(".quest_desc") and len(v) > 1:
            out = [f'\t{k}: [']
            for line in v:
                if isinstance(line, str):
                    out.append(f'\t\t"{escape_snbt_string(line)}"')
                else:
                    out.append(f"\t\t{json.dumps(line, ensure_ascii=False)}")
            out.append(f"\t]")
            return out
        # Single-line array
        parts = []
        for x in v:
            if isinstance(x, str):
                parts.append(f'"{escape_snbt_string(x)}"')
            else:
                parts.append(json.dumps(x, ensure_ascii=False))
        return [f'\t{k}: [' + ", ".join(parts) + "]"]
    return [f"\t{k}: {json.dumps(v, ensure_ascii=False)}"]


def merge_lang(lang):
    phase2_path = os.path.join(WS, "phase2_output", f"{lang}.json")
    if not os.path.exists(phase2_path):
        print(f"  No phase2 output for {lang}")
        return
    fixes = json.load(open(phase2_path, encoding="utf-8"))
    print(f"  {lang}: {len(fixes)} fixes loaded")

    for d in (LANG_DIR, DEFAULT_DIR):
        tgt = os.path.join(d, f"{lang}.snbt")
        if not os.path.exists(tgt):
            continue
        # Backup once
        if d == LANG_DIR:
            backup = os.path.join(WS, f"{lang}_phase2_backup.snbt")
            if not os.path.exists(backup):
                shutil.copy2(tgt, backup)

        with open(tgt, encoding="utf-8") as f:
            text = f.read()
        prefix, entries, suffix = parse_snbt_to_entries(text)
        key_to_idx = {k: i for i, (k, _) in enumerate(entries)}
        applied = 0
        added = 0
        for k, v in fixes.items():
            new_lines = serialize_entry(k, v)
            if k in key_to_idx:
                entries[key_to_idx[k]] = (k, new_lines)
                applied += 1
            else:
                entries.append((k, new_lines))
                added += 1
        out_lines = prefix + [ln for _, blk in entries for ln in blk] + suffix
        with open(tgt, "w", encoding="utf-8") as f:
            f.write("\n".join(out_lines))
        print(f"    -> {os.path.basename(d)}/{lang}: applied {applied}, added {added}")


if __name__ == "__main__":
    os.makedirs(os.path.join(WS, "phase2_output"), exist_ok=True)
    for lang in ("fr_fr", "es_es", "pt_br", "ru_ru", "zh_cn"):
        merge_lang(lang)
