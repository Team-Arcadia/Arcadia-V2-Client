"""
For each non-EN_US language file:
- Add the keys that EXIST in en_us but are MISSING in the lang file
- Use the EN_US value as a fallback so the key exists (joueur verra du EN, mieux que rien)
- DO NOT touch existing translated keys

After this, every lang has the SAME key set as en_us.
"""
import json
import os
import re
import shutil
import sys

WS = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/ftbq_audit"
LANG_DIR = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/config/ftbquests/quests/lang"
DEFAULT_LANG_DIR = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/defaultconfigs/ftbquests/quests/lang"

sys.path.insert(0, WS)
from parse_snbt import parse_snbt

# Build a map of key -> raw_lines from en_us to copy them verbatim into missing slots
def collect_raw_entries(snbt_path):
    """Parse and return list of (key, raw_lines) preserving insertion order."""
    with open(snbt_path, encoding="utf-8") as f:
        text = f.read()
    lines = text.split("\n")
    entries = []
    i = 0
    in_body = False
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()
        if stripped == "{":
            in_body = True
            i += 1
            continue
        if not in_body:
            i += 1
            continue
        if stripped == "}":
            break
        m = re.match(r'^(\t+)([^:\s]+):\s*(.*)$', line)
        if not m:
            i += 1
            continue
        key = m.group(2)
        rest = m.group(3)
        if rest.startswith("[") and not rest.endswith("]"):
            block = [line]
            i += 1
            while i < n:
                block.append(lines[i])
                if lines[i].strip().startswith("]"):
                    i += 1
                    break
                i += 1
            entries.append((key, block))
        else:
            entries.append((key, [line]))
            i += 1
    return entries


def write_snbt_with_added_keys(target_path, en_us_entries, lang_data):
    """Add to target SNBT: any key from en_us_entries that doesn't exist in lang_data."""
    lang_keys = set(lang_data.keys())
    # Find keys in en_us that are missing in lang
    en_keys_in_order = [k for k, _ in en_us_entries]
    missing = [k for k in en_keys_in_order if k not in lang_keys]
    if not missing:
        return 0

    # Open target file, find the closing `}`, insert new lines before it
    with open(target_path, encoding="utf-8") as f:
        text = f.read()
    lines = text.split("\n")
    # Find last `}` line index
    close_idx = None
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip() == "}":
            close_idx = i
            break
    if close_idx is None:
        return 0

    # Build the lines to insert
    en_us_map = dict(en_us_entries)
    insert_lines = []
    for k in missing:
        for ln in en_us_map[k]:
            insert_lines.append(ln)

    new_lines = lines[:close_idx] + insert_lines + lines[close_idx:]
    new_text = "\n".join(new_lines)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(new_text)
    return len(missing)


def main():
    en_us_path = os.path.join(LANG_DIR, "en_us.snbt")
    en_us_entries = collect_raw_entries(en_us_path)
    print(f"EN_US source has {len(en_us_entries)} entries")

    en_us_data = json.load(open(f"{WS}/en_us.json", encoding="utf-8"))

    for lang in ["en_gb", "es_es", "pt_br", "ru_ru", "zh_cn"]:
        lang_data = json.load(open(f"{WS}/{lang}.json", encoding="utf-8"))
        for d in (LANG_DIR, DEFAULT_LANG_DIR):
            tgt = os.path.join(d, f"{lang}.snbt")
            if not os.path.exists(tgt):
                continue
            # Backup once (only the live config, defaultconfigs can be overwritten freely)
            if d == LANG_DIR:
                backup = os.path.join(WS, f"{lang}_original_backup.snbt")
                if not os.path.exists(backup):
                    shutil.copy2(tgt, backup)
            added = write_snbt_with_added_keys(tgt, en_us_entries, lang_data)
            print(f"  {lang} ({os.path.basename(d)}): added {added} missing keys from EN_US")


if __name__ == "__main__":
    main()
