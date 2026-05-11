"""
Parse FTB Quests lang .snbt files into a clean key=value dict.
SNBT format here is simple: each line is
    key: value
or
    key: ["multi", "line", "array"]
or
    key: ["single line array"]

We handle:
- single-line strings:   `quest.X.title: "Some title"`
- single-line arrays:    `quest.X.desc: ["line1", "line2"]`
- multi-line arrays (rare in FTBQ langs but possible)
- chapter group titles:  `chapter_group.X.title: "..."`
- task / reward / etc fields

Output: JSON dict {key: value} where value is either str or list[str].
"""

import json
import os
import re
import sys

WS = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/ftbq_audit"
FTBQ_LANG = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/config/ftbquests/quests/lang"


def parse_snbt(path):
    """Parse FTB Quests SNBT lang file -> {key: str|list[str]}"""
    data = {}
    issues = []
    with open(path, encoding="utf-8") as f:
        text = f.read()

    # Skip the wrapping `{` and `}`
    text = text.strip()
    if text.startswith("{"):
        text = text[1:]
    if text.endswith("}"):
        text = text[:-1]
    text = text.strip()

    # Tokenize by walking; lines look like:
    #   key: value
    # value can span lines if it's a multi-line array
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        # Find first colon (but not inside quotes!)
        m = re.match(r'^\s*([^:\s]+):\s*(.*)$', line)
        if not m:
            i += 1
            continue
        key = m.group(1).strip()
        value_part = m.group(2)

        # Determine value type
        if value_part.startswith('"'):
            # Single-line string
            # Find matching closing quote (handle \" escapes)
            val = _parse_quoted_string(value_part)
            if val is None:
                issues.append((i + 1, f"Cannot parse string for {key}: {value_part[:80]}"))
            else:
                data[key] = val
            i += 1
        elif value_part.startswith("[") and value_part.endswith("]"):
            # Single-line array
            inner = value_part[1:-1].strip()
            val = _parse_array_inner(inner)
            data[key] = val
            i += 1
        elif value_part == "[":
            # Multi-line array
            arr = []
            i += 1
            while i < len(lines):
                aline = lines[i].rstrip()
                if aline.strip().startswith("]"):
                    i += 1
                    break
                s = _parse_quoted_string(aline.strip().rstrip(","))
                if s is not None:
                    arr.append(s)
                i += 1
            data[key] = arr
        else:
            # Non-string value (int, bool, etc) - skip
            i += 1
    return data, issues


def _parse_quoted_string(s):
    """Parse a quoted string like "hello" -> hello, handling \" escapes."""
    s = s.strip().rstrip(",")
    if not s.startswith('"'):
        return None
    # Find the closing quote
    result = []
    i = 1
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            nxt = s[i + 1]
            if nxt == "n":
                result.append("\n")
            elif nxt == "t":
                result.append("\t")
            elif nxt == "\\":
                result.append("\\")
            elif nxt == '"':
                result.append('"')
            else:
                result.append(c)
                result.append(nxt)
            i += 2
        elif c == '"':
            return "".join(result)
        else:
            result.append(c)
            i += 1
    # No closing quote
    return None


def _parse_array_inner(s):
    """Parse the inside of [ ... ] - comma-separated quoted strings."""
    result = []
    depth = 0
    cur = []
    in_str = False
    esc = False
    for c in s:
        if esc:
            cur.append(c)
            esc = False
            continue
        if c == "\\":
            cur.append(c)
            esc = True
            continue
        if c == '"':
            in_str = not in_str
            cur.append(c)
            continue
        if not in_str and c == ",":
            piece = "".join(cur).strip()
            if piece:
                val = _parse_quoted_string(piece)
                if val is not None:
                    result.append(val)
            cur = []
            continue
        cur.append(c)
    piece = "".join(cur).strip()
    if piece:
        val = _parse_quoted_string(piece)
        if val is not None:
            result.append(val)
    return result


def main():
    os.makedirs(WS, exist_ok=True)
    all_data = {}
    for f in sorted(os.listdir(FTBQ_LANG)):
        if not f.endswith(".snbt"):
            continue
        lang = f[:-5]
        path = os.path.join(FTBQ_LANG, f)
        data, issues = parse_snbt(path)
        all_data[lang] = data
        print(f"{lang}: parsed {len(data)} keys, {len(issues)} parse issues")
        with open(os.path.join(WS, f"{lang}.json"), "w", encoding="utf-8") as o:
            json.dump(data, o, ensure_ascii=False, indent=1)

    # Cross-lang key analysis
    print("\n=== Cross-lang key analysis ===")
    base = "en_us"
    if base not in all_data:
        print(f"FATAL: {base} not found")
        sys.exit(1)
    base_keys = set(all_data[base].keys())
    print(f"{base}: {len(base_keys)} keys")
    for lang in all_data:
        if lang == base:
            continue
        ks = set(all_data[lang].keys())
        only_base = base_keys - ks
        only_lang = ks - base_keys
        print(f"  {lang}: {len(ks)} keys; missing vs base: {len(only_base)}; extra: {len(only_lang)}")

    return all_data


if __name__ == "__main__":
    main()
