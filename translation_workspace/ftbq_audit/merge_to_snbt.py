"""
Merge agent_outputs/*.json fixes back into the fr_fr.snbt file.

Strategy:
1. Parse the current fr_fr.snbt into an ordered list of (key, value) entries
2. For each fix in agent_outputs, replace the value for that key (or add if missing)
3. Re-serialize back to SNBT format respecting FTB Quests style:
   - One key per line, tab-indented
   - String values: key: "value"
   - Single-line array: key: ["a", "b"]  (used when array fits on one line in original)
   - Multi-line array: key: [<NL>\t\t"a"<NL>\t\t"b"<NL>\t]

We try to preserve formatting as much as possible by tracking the original
line span of each key in the original file.
"""
import json
import os
import re
import sys

WS = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/ftbq_audit"
SNBT_PATH = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/config/ftbquests/quests/lang/fr_fr.snbt"
DEFAULT_PATH = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/defaultconfigs/ftbquests/quests/lang/fr_fr.snbt"
OUTPUT_DIR = os.path.join(WS, "agent_outputs")


def escape_snbt_string(s):
    """Escape a Python string for SNBT serialization."""
    # Replace backslash first, then double-quote, then control chars
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")


def serialize_value(v):
    """Serialize a Python value to its SNBT representation as a single line (if possible)."""
    if isinstance(v, str):
        return '"' + escape_snbt_string(v) + '"'
    if isinstance(v, list):
        # All strings? -> array
        if all(isinstance(x, str) for x in v):
            return "[" + ", ".join('"' + escape_snbt_string(x) + '"' for x in v) + "]"
    # Fallback
    return json.dumps(v, ensure_ascii=False)


def parse_snbt_to_entries(text):
    """Parse SNBT into a list of (key, raw_lines) tuples preserving line order.
    Each entry has the EXACT original line text(s) so we can preserve formatting.
    Returns:
        prefix: lines before any key entry (the opening `{`)
        entries: list of (key, lines_list)
        suffix: lines after last entry (the closing `}`)
    """
    lines = text.split("\n")
    n = len(lines)
    prefix = []
    entries = []
    suffix = []

    i = 0
    # Find the opening `{`
    while i < n:
        stripped = lines[i].strip()
        if stripped == "{":
            prefix.append(lines[i])
            i += 1
            break
        prefix.append(lines[i])
        i += 1

    # Now parse entries until we hit the closing `}`
    while i < n:
        line = lines[i]
        stripped = line.strip()
        if stripped == "}":
            suffix.append(line)
            i += 1
            # Capture trailing newlines/EOF
            while i < n:
                suffix.append(lines[i])
                i += 1
            break

        # Each entry starts with `\tkey: ...`
        m = re.match(r'^(\t+)([^:\s]+):\s*(.*)$', line)
        if not m:
            # Blank line or stray; attach to previous if any
            if entries:
                entries[-1][1].append(line)
            else:
                prefix.append(line)
            i += 1
            continue

        key = m.group(2)
        rest = m.group(3)

        if rest.startswith("[") and not rest.endswith("]"):
            # Multi-line array — collect until closing `]`
            entry_lines = [line]
            i += 1
            while i < n:
                entry_lines.append(lines[i])
                if lines[i].strip().startswith("]"):
                    i += 1
                    break
                i += 1
            entries.append((key, entry_lines))
        else:
            # Single-line entry
            entries.append((key, [line]))
            i += 1

    return prefix, entries, suffix


def detect_indent(prefix):
    """The original uses tab indentation; verify."""
    return "\t"


def reserialize_entry(key, value, multiline_array=False, indent="\t"):
    """Produce SNBT lines for a key:value entry."""
    if isinstance(value, list) and multiline_array and len(value) > 0:
        lines = [f"{indent}{key}: ["]
        for v in value:
            if isinstance(v, str):
                lines.append(f'{indent}\t"{escape_snbt_string(v)}"')
            else:
                lines.append(f"{indent}\t{json.dumps(v, ensure_ascii=False)}")
        lines.append(f"{indent}]")
        return lines
    return [f"{indent}{key}: {serialize_value(value)}"]


def merge_fixes():
    # Read current fr_fr
    with open(SNBT_PATH, encoding="utf-8") as f:
        text = f.read()

    prefix, entries, suffix = parse_snbt_to_entries(text)
    print(f"Parsed {len(entries)} entries from fr_fr.snbt")

    # Build current key -> idx map
    key_to_idx = {k: i for i, (k, _) in enumerate(entries)}

    # Load all agent fixes
    all_fixes = {}
    for fname in sorted(os.listdir(OUTPUT_DIR)):
        if not fname.endswith(".json"):
            continue
        try:
            d = json.load(open(os.path.join(OUTPUT_DIR, fname), encoding="utf-8"))
        except Exception as e:
            print(f"  Cannot parse {fname}: {e}")
            continue
        if not isinstance(d, dict):
            print(f"  Skipping {fname}: not a dict")
            continue
        for k, v in d.items():
            all_fixes[k] = v
    print(f"Total fixes loaded: {len(all_fixes)}")

    # Apply fixes
    applied = 0
    added = 0
    for key, value in all_fixes.items():
        # Detect if value should be multi-line array
        if isinstance(value, list) and len(value) >= 2:
            multiline = True
        else:
            multiline = False

        new_lines = reserialize_entry(key, value, multiline_array=multiline, indent="\t")

        if key in key_to_idx:
            idx = key_to_idx[key]
            old_lines = entries[idx][1]
            # Check if the old entry was multi-line — preserve that style if possible
            was_multiline = len(old_lines) > 1
            if isinstance(value, list) and was_multiline:
                multiline = True
                new_lines = reserialize_entry(key, value, multiline_array=True, indent="\t")
            entries[idx] = (key, new_lines)
            applied += 1
        else:
            # Add at end
            entries.append((key, new_lines))
            added += 1

    print(f"Applied to existing keys: {applied}")
    print(f"Added new keys: {added}")

    # Reserialize
    out_lines = []
    out_lines.extend(prefix)
    for key, lines in entries:
        out_lines.extend(lines)
    out_lines.extend(suffix)

    output_text = "\n".join(out_lines)

    # Write to a temp file first for verification
    temp_path = os.path.join(WS, "fr_fr_new.snbt")
    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(output_text)
    print(f"\nWrote new file to: {temp_path}")
    print(f"  Original size: {os.path.getsize(SNBT_PATH)} bytes")
    print(f"  New size:      {os.path.getsize(temp_path)} bytes")

    return temp_path, applied, added


if __name__ == "__main__":
    merge_fixes()
