"""
Merge agent_outputs_other/<lang>.json fixes back into <lang>.snbt for ES/PT/RU/ZH.

Pattern: same as fr_fr merge but per-lang.
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
from parse_snbt import parse_snbt


def escape_snbt_string(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")


def parse_snbt_to_entries(text):
    lines = text.split("\n")
    n = len(lines)
    prefix, entries, suffix = [], [], []
    i = 0
    while i < n:
        if lines[i].strip() == "{":
            prefix.append(lines[i]); i += 1; break
        prefix.append(lines[i]); i += 1
    while i < n:
        line = lines[i]
        stripped = line.strip()
        if stripped == "}":
            suffix.append(line); i += 1
            while i < n: suffix.append(lines[i]); i += 1
            break
        m = re.match(r'^(\t+)([^:\s]+):\s*(.*)$', line)
        if not m:
            if entries: entries[-1][1].append(line)
            else: prefix.append(line)
            i += 1; continue
        key = m.group(2); rest = m.group(3)
        if rest.startswith("[") and not rest.endswith("]"):
            block = [line]; i += 1
            while i < n:
                block.append(lines[i])
                if lines[i].strip().startswith("]"):
                    i += 1; break
                i += 1
            entries.append((key, block))
        else:
            entries.append((key, [line])); i += 1
    return prefix, entries, suffix


def reserialize_entry(key, value):
    """Single-line entry."""
    if isinstance(value, str):
        return f'\t{key}: "{escape_snbt_string(value)}"'
    if isinstance(value, list):
        return f'\t{key}: [' + ", ".join(f'"{escape_snbt_string(v)}"' for v in value) + ']'
    return f'\t{key}: {json.dumps(value, ensure_ascii=False)}'


def merge_lang(lang):
    fixes_path = os.path.join(WS, "agent_outputs_other", f"{lang}.json")
    if not os.path.exists(fixes_path):
        print(f"  No fixes for {lang}")
        return 0
    fixes = json.load(open(fixes_path, encoding="utf-8"))
    print(f"  {lang}: {len(fixes)} fixes loaded")

    for d in (LANG_DIR, DEFAULT_DIR):
        tgt = os.path.join(d, f"{lang}.snbt")
        if not os.path.exists(tgt):
            continue
        with open(tgt, encoding="utf-8") as f:
            text = f.read()
        prefix, entries, suffix = parse_snbt_to_entries(text)
        key_to_idx = {k: i for i, (k, _) in enumerate(entries)}
        applied = 0
        added = 0
        for k, v in fixes.items():
            new_line = reserialize_entry(k, v)
            if k in key_to_idx:
                entries[key_to_idx[k]] = (k, [new_line])
                applied += 1
            else:
                entries.append((k, [new_line]))
                added += 1
        out_lines = prefix + [ln for _, blk in entries for ln in blk] + suffix
        with open(tgt, "w", encoding="utf-8") as f:
            f.write("\n".join(out_lines))
        print(f"    -> wrote {os.path.basename(d)}/{lang}.snbt: applied {applied}, added {added}")
    return len(fixes)


if __name__ == "__main__":
    for lang in ["es_es", "pt_br", "ru_ru", "zh_cn"]:
        merge_lang(lang)
