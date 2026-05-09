"""
Quality audit: scan ALL FR translations (jar + kubejs) for:
  1. Identical to EN (untranslated leak)
  2. Mojibake / encoding issues
  3. Empty values
  4. Suspect literal/word-by-word patterns (e.g. "de de", "en en", obvious word-level translation)
  5. Mismatched format codes (%s, %d count differs between EN and FR)
  6. Excessive English-only word density (heuristic)
"""
import json
import os
import re

WS = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace"
KJS = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/kubejs/assets"
EN_DIR = os.path.join(WS, "audit2", "all_en")
JAR_FR_DIR = os.path.join(WS, "audit2", "all_jar_fr")

EN_HINT = re.compile(
    r"\b(the|and|with|this|that|these|those|when|where|while|because|though|already|enough|every|never|always|sometimes|nothing|someone|something|here|there|been|were|will|would|could|should|shall|may|might|must|have|has|had|does|did|using|allow|prevent|increase|decrease|require|provide|enable|disable|toggle|reduce|create|destroy|player|server|client|inventory|crafting|enchant|enchanted|enchantment|recipe|bonus|effect|cooldown|duration|chance|amount|level|right-click|left-click|sneak|jump|sprint|crouch|on|off|of|to|from|by|for|in|out|into|onto|over|under|between|among|across|along|around|through|within|without|toward|towards|behind|before|after|since|until|upon|via|per|against|throughout|above|below|beside|besides|except|despite|regarding|concerning|including)\b",
    re.IGNORECASE,
)

MOJIBAKE = re.compile(r"[Ã][©®ª¨§¢«»]|â€™|â€œ|â€\x9d|Â[°§¨ª®©¶]")

DOUBLE_PREP = re.compile(r"\b(de|en|du|à|au|aux|le|la|les|une|un|et|ou)\s+\1\b", re.IGNORECASE)


def parse_lang(path):
    if not os.path.exists(path):
        return None
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
        return None


def fr_has_issues(en_v, fr_v):
    issues = []
    if not isinstance(fr_v, str):
        return issues
    fr_strip = fr_v.strip()

    # Empty
    if not fr_strip:
        issues.append("EMPTY")
        return issues

    # Mojibake
    if MOJIBAKE.search(fr_v):
        issues.append("MOJIBAKE")

    # Identical to EN (only if EN exists and is non-trivial)
    if isinstance(en_v, str) and len(en_v.strip()) >= 4 and en_v.strip() == fr_strip:
        # Allow some intentional cases: brand names (proper nouns)
        # Heuristic: if value contains a vowel and at least 3 letters and looks like real English, flag
        if re.search(r"[a-zA-Z]{3,}", fr_strip):
            # Skip if it's mostly numbers/symbols
            if len(re.findall(r"[a-zA-Z]", fr_strip)) >= len(fr_strip) // 2:
                issues.append("IDENTICAL_TO_EN")

    # Format code mismatch
    if isinstance(en_v, str):
        en_codes = re.findall(r"%[sd%]|%\d\$[sd]|\{\d+\}", en_v)
        fr_codes = re.findall(r"%[sd%]|%\d\$[sd]|\{\d+\}", fr_v)
        if sorted(en_codes) != sorted(fr_codes):
            issues.append(f"CODE_MISMATCH(en={en_codes}, fr={fr_codes})")

    # Double-preposition glitch (e.g. "Casque de de fer")
    if DOUBLE_PREP.search(fr_v):
        issues.append("DOUBLE_PREP")

    # English heavy
    if len(fr_v) >= 12:
        en_count = len(EN_HINT.findall(fr_v))
        if en_count >= 3:
            issues.append("ENGLISH_LEAK")

    # Suspicious patterns
    if "TODO" in fr_v.upper() or "FIXME" in fr_v.upper() or "PLACEHOLDER" in fr_v.upper():
        issues.append("PLACEHOLDER")

    return issues


# Build modid set from EN
all_modids = set()
for f in os.listdir(EN_DIR):
    modid = f.rsplit(".", 1)[0]
    all_modids.add(modid)

report = []
total_keys = 0
total_issues = 0
issue_by_type = {}

for modid in sorted(all_modids):
    # Load EN
    en = None
    for ext in ("json", "lang"):
        en = parse_lang(os.path.join(EN_DIR, f"{modid}.{ext}"))
        if en is not None:
            break
    if en is None:
        en = {}

    # Load FR (jar + kubejs)
    jar_fr = None
    for ext in ("json", "lang"):
        jar_fr = parse_lang(os.path.join(JAR_FR_DIR, f"{modid}.{ext}"))
        if jar_fr is not None:
            break
    if jar_fr is None:
        jar_fr = {}

    kjs_fr = parse_lang(os.path.join(KJS, modid, "lang", "fr_fr.json")) or {}

    combined_fr = {}
    combined_fr.update(jar_fr)
    combined_fr.update(kjs_fr)  # kubejs takes priority (more recent)

    if not combined_fr:
        continue

    issues = []
    for k, fr_v in combined_fr.items():
        en_v = en.get(k)
        flags = fr_has_issues(en_v, fr_v)
        for flag in flags:
            issues.append((flag, k, fr_v[:80] if isinstance(fr_v, str) else str(fr_v)[:80]))
            issue_by_type[flag.split("(")[0]] = issue_by_type.get(flag.split("(")[0], 0) + 1
        total_keys += 1
    total_issues += len(issues)

    if issues:
        report.append((modid, len(combined_fr), len(issues), issues))

# Sort by issue count
report.sort(key=lambda x: -x[2])

print(f"=== QUALITY AUDIT ===")
print(f"Total mods scanned: {len(all_modids)}")
print(f"Total FR keys checked: {total_keys}")
print(f"Total issues: {total_issues}")
print()
print("=== Issue type counts ===")
for t, c in sorted(issue_by_type.items(), key=lambda x: -x[1]):
    print(f"  {t:25s} {c:5d}")
print()
print("=== Top 30 mods with most issues ===")
print(f"{'modid':<40s} {'total_keys':>10s} {'issues':>8s}")
for modid, total, n, _ in report[:30]:
    print(f"{modid:<40s} {total:>10d} {n:>8d}")

# Save full
with open(os.path.join(WS, "audit2", "quality_report.json"), "w", encoding="utf-8") as f:
    out = {}
    for modid, total, n, issues in report:
        out[modid] = {
            "total_keys": total,
            "issue_count": n,
            "issues": [{"type": t, "key": k, "value": v} for t, k, v in issues[:200]],
        }
    json.dump(out, f, ensure_ascii=False, indent=2)

print()
print(f"Full report saved to audit2/quality_report.json")
print()
print("=== Sample issues per type (5 each) ===")
samples = {}
for modid, total, n, issues in report:
    for t, k, v in issues:
        cat = t.split("(")[0]
        samples.setdefault(cat, [])
        if len(samples[cat]) < 5:
            samples[cat].append((modid, k, v))
for t, items in samples.items():
    print(f"\n  -- {t} --")
    for m, k, v in items:
        print(f"     [{m}] {k} = '{v}'")
