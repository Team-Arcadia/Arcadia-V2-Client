import json, os, re, sys

KJS = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/kubejs/assets"
WS = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace"

EN_HINT = re.compile(
    r"\b(the|and|with|this|that|these|those|when|where|while|because|though|already|enough|every|never|always|sometimes|nothing|someone|something|here|there|been|were|are|was|will|would|could|should|shall|may|might|must|have|has|had|does|did|use|used|using|allow|prevent|increase|decrease|require|provide|enable|disable|toggle|reduce|create|destroy|player|server|client|inventory|crafting|enchant|enchanted|enchantment|recipe|bonus|effect|cooldown|duration|chance|amount|level|right-click|left-click|sneak|jump|sprint|crouch)\b",
    re.IGNORECASE,
)

MOJIBAKE = re.compile(r"[Ã][©®ª¨§¢«»]|â€™|â€œ|â€|Â[°§¨ª®©¶]")


def looks_english(s):
    if not isinstance(s, str):
        return False
    s = s.strip()
    if len(s) < 8:
        return False
    if s[0] in ("§", "&", "%"):
        return False
    if s.startswith("\\"):
        return False
    matches = EN_HINT.findall(s)
    return len(matches) >= 2


def is_unchanged(en, fr):
    return isinstance(en, str) and isinstance(fr, str) and en.strip() == fr.strip() and len(en.strip()) >= 4


def has_mojibake(s):
    return isinstance(s, str) and bool(MOJIBAKE.search(s))


audit = []
total_files = 0
total_keys = 0

for modid in sorted(os.listdir(KJS)):
    fr_path = os.path.join(KJS, modid, "lang", "fr_fr.json")
    en_path = os.path.join(KJS, modid, "lang", "en_us.json")
    if not os.path.exists(fr_path):
        continue
    total_files += 1
    try:
        with open(fr_path, encoding="utf-8") as f:
            fr_data = json.load(f)
    except Exception as e:
        audit.append((modid, "PARSE_ERROR", str(e), 0, []))
        continue

    en_data = {}
    if os.path.exists(en_path):
        try:
            with open(en_path, encoding="utf-8") as f:
                en_data = json.load(f)
        except Exception:
            pass

    issues = []
    keys_count = 0
    if isinstance(fr_data, dict):
        for k, v in fr_data.items():
            if not isinstance(v, str):
                continue
            keys_count += 1
            en_v = en_data.get(k) if isinstance(en_data, dict) else None
            if en_v and is_unchanged(en_v, v):
                issues.append(("UNCHANGED", k, v[:80]))
            elif looks_english(v):
                issues.append(("ENGLISH", k, v[:80]))
            if has_mojibake(v):
                issues.append(("MOJIBAKE", k, v[:80]))
            if not v.strip():
                issues.append(("EMPTY", k, ""))

    total_keys += keys_count
    audit.append((modid, "OK" if not issues else "ISSUES", "", keys_count, issues))

out = {}
for modid, status, err, kc, issues in audit:
    out[modid] = {
        "status": status,
        "error": err,
        "keys_count": kc,
        "issue_count": len(issues),
        "issues": [{"type": t, "key": k, "value": v} for t, k, v in issues[:50]],
    }

with open(os.path.join(WS, "kubejs_fr_audit.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)

print(f"Total fr_fr.json files: {total_files}")
print(f"Total keys: {total_keys}")
print()
print("=== Mods with issues (top by count) ===")
for modid, status, err, kc, issues in sorted(audit, key=lambda x: -len(x[4]))[:30]:
    if status == "PARSE_ERROR":
        print(f"  {modid:40s}  PARSE ERROR: {err[:60]}")
        continue
    if not issues:
        continue
    types = {}
    for t, k, v in issues:
        types[t] = types.get(t, 0) + 1
    summary = " ".join(f"{t}={c}" for t, c in types.items())
    print(f"  {modid:40s}  keys={kc:5d}  issues={len(issues):4d}  ({summary})")

print()
print("=== Sample issues per type ===")
by_type = {"UNCHANGED": [], "ENGLISH": [], "MOJIBAKE": [], "EMPTY": []}
for modid, status, err, kc, issues in audit:
    for t, k, v in issues:
        if len(by_type[t]) < 8:
            by_type[t].append((modid, k, v))
for t, items in by_type.items():
    print(f"  -- {t} --")
    for m, k, v in items:
        print(f"     [{m}] {k} = '{v}'")
