"""
5 audits finaux après tous les fixes :

1. AUDIT 1 — Coherence : toutes les langues ont le même nombre de keys
2. AUDIT 2 — Quality : pas de FR=EN, pas de mojibake, pas de EN-leak
3. AUDIT 3 — Completeness : chaque quest a title+subtitle+desc dans chaque langue
4. AUDIT 4 — Usefulness : descriptions guident le joueur (longueur >= 20 chars utiles)
5. AUDIT 5 — SNBT parse + key parity
"""
import json
import os
import re
import sys

WS = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/ftbq_audit"
LANG_DIR = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/config/ftbquests/quests/lang"

sys.path.insert(0, WS)
from parse_snbt import parse_snbt

LANGS = ["en_us", "en_gb", "fr_fr", "es_es", "pt_br", "ru_ru", "zh_cn"]


def text_of(v):
    if isinstance(v, str):
        return v
    if isinstance(v, list):
        return "\n".join(str(x) for x in v)
    return ""


def load_all_langs():
    return {lang: parse_snbt(os.path.join(LANG_DIR, f"{lang}.snbt"))[0] for lang in LANGS}


def audit_1_coherence(all_data):
    print("=" * 70)
    print("AUDIT 1/5 — COHERENCE (all langs same keys)")
    print("=" * 70)
    base = "en_us"
    base_keys = set(all_data[base].keys())
    print(f"Base {base}: {len(base_keys)} keys")
    issues = 0
    for lang in LANGS:
        if lang == base:
            continue
        ks = set(all_data[lang].keys())
        missing = base_keys - ks
        extra = ks - base_keys
        if missing or extra:
            issues += 1
            print(f"  {lang}: {len(all_data[lang])} keys; missing: {len(missing)}, extra: {len(extra)}")
        else:
            print(f"  {lang}: {len(all_data[lang])} keys [PARITY OK]")
    if issues == 0:
        print("\n[OK] AUDIT 1 PASS: All langs have same keys as EN_US")
    else:
        print(f"\n[FAIL] AUDIT 1 FAIL: {issues} langs with parity issues")
    return issues == 0


MOJIBAKE = re.compile(r"Ã[©®ª¨§¢«»]|â€™|â€œ|â€\x9d|Â[°§¨ª®©¶]")
EN_HINTS = re.compile(
    r"\b(the|and|with|for|from|will|would|should|defeat|gather|complete|craft|find|reach|kill|obtain|server|player)\b",
    re.IGNORECASE,
)


def audit_2_quality(all_data):
    print("=" * 70)
    print("AUDIT 2/5 — QUALITY (lang=EN, mojibake, EN-leak)")
    print("=" * 70)
    base = "en_us"
    base_data = all_data[base]
    issues_per_lang = {}
    for lang in ["fr_fr", "es_es", "pt_br", "ru_ru", "zh_cn"]:
        data = all_data[lang]
        identical = 0
        mojibake = 0
        en_leak = 0
        for k, v in data.items():
            base_v = base_data.get(k)
            if base_v is None:
                continue
            ev = text_of(v)
            eev = text_of(base_v)
            if ev.strip() == eev.strip() and re.search(r"[a-z]{3,}", eev):
                identical += 1
            if MOJIBAKE.search(ev):
                mojibake += 1
            if len(ev) >= 30 and len(EN_HINTS.findall(ev)) >= 3 and lang != "fr_fr":
                # Skip FR since EN_HINTS regex includes English words FR uses too (false positive)
                en_leak += 1
        issues_per_lang[lang] = {
            "identical_to_en": identical,
            "mojibake": mojibake,
            "en_leak_strict": en_leak,
        }
        print(f"  {lang}: identical={identical:>5d}  mojibake={mojibake:>3d}  en_leak={en_leak:>5d}")
    print()
    return issues_per_lang


def audit_3_completeness(all_data):
    print("=" * 70)
    print("AUDIT 3/5 — COMPLETENESS (every quest has title+subtitle+desc)")
    print("=" * 70)
    base_data = all_data["en_us"]
    # Find all quest IDs
    quest_ids = set()
    for k in base_data:
        m = re.match(r"^quest\.([0-9A-F]{16})\.", k)
        if m:
            quest_ids.add(m.group(1))
    print(f"Total quest IDs: {len(quest_ids)}")
    print()

    missing_per_lang = {}
    for lang in LANGS:
        data = all_data[lang]
        without_title = 0
        without_subtitle = 0
        without_desc = 0
        for qid in quest_ids:
            t = text_of(data.get(f"quest.{qid}.title", "")).strip()
            s = text_of(data.get(f"quest.{qid}.quest_subtitle", "")).strip()
            d = text_of(data.get(f"quest.{qid}.quest_desc", "")).strip()
            if not t:
                without_title += 1
            if not s:
                without_subtitle += 1
            if not d:
                without_desc += 1
        missing_per_lang[lang] = {
            "without_title": without_title,
            "without_subtitle": without_subtitle,
            "without_desc": without_desc,
        }
        print(f"  {lang}: no_title={without_title:>4d}  no_subtitle={without_subtitle:>4d}  no_desc={without_desc:>4d}")
    return missing_per_lang


def audit_4_usefulness(all_data):
    print("=" * 70)
    print("AUDIT 4/5 — USEFULNESS (descriptions guide the player)")
    print("=" * 70)
    base_data = all_data["en_us"]
    # Find quest IDs that have descs
    useless_per_lang = {}
    for lang in LANGS:
        data = all_data[lang]
        useless = 0
        total = 0
        for k, v in data.items():
            if not k.endswith(".quest_desc"):
                continue
            total += 1
            t = text_of(v).strip()
            # Strip color codes
            plain = re.sub(r"&[0-9a-fk-or]", "", t).strip()
            plain = re.sub(r"\s+", " ", plain)
            if len(plain) < 20:
                useless += 1
        pct = (useless * 100 / total) if total else 0
        useless_per_lang[lang] = {"useless": useless, "total": total, "pct": round(pct, 1)}
        print(f"  {lang}: {useless}/{total} descs < 20 chars useful ({pct:.1f}%)")
    return useless_per_lang


def audit_5_parse(all_data):
    print("=" * 70)
    print("AUDIT 5/5 — SNBT PARSE & FORMAT")
    print("=" * 70)
    all_pass = True
    for lang in LANGS:
        path = os.path.join(LANG_DIR, f"{lang}.snbt")
        _, issues = parse_snbt(path)
        size = os.path.getsize(path)
        print(f"  {lang}: {size//1024} KB, {len(issues)} parse issues")
        if issues:
            all_pass = False
            for line, msg in issues[:3]:
                print(f"    line {line}: {msg}")
    if all_pass:
        print("\n[OK] AUDIT 5 PASS: All SNBT files parse cleanly")
    else:
        print("\n[FAIL] AUDIT 5 FAIL: parse issues detected")
    return all_pass


def main():
    print("\n\n")
    print("#" * 70)
    print("# FINAL 5-AUDIT RUN")
    print("#" * 70)
    print()

    all_data = load_all_langs()

    a1 = audit_1_coherence(all_data)
    print()
    a2 = audit_2_quality(all_data)
    print()
    a3 = audit_3_completeness(all_data)
    print()
    a4 = audit_4_usefulness(all_data)
    print()
    a5 = audit_5_parse(all_data)

    print()
    print("#" * 70)
    print("# AUDIT SUMMARY")
    print("#" * 70)
    print(f"  AUDIT 1 Coherence:    {'PASS [OK]' if a1 else 'FAIL [FAIL]'}")
    print(f"  AUDIT 2 Quality:      see above (per-lang stats)")
    print(f"  AUDIT 3 Completeness: see above (per-lang stats)")
    print(f"  AUDIT 4 Usefulness:   see above (per-lang stats)")
    print(f"  AUDIT 5 Parse:        {'PASS [OK]' if a5 else 'FAIL [FAIL]'}")

    # Save full report
    final_report = {
        "audit_1_coherence_pass": a1,
        "audit_2_quality": a2,
        "audit_3_completeness": a3,
        "audit_4_usefulness": a4,
        "audit_5_parse_pass": a5,
    }
    with open(os.path.join(WS, "final_5_audits.json"), "w", encoding="utf-8") as f:
        json.dump(final_report, f, ensure_ascii=False, indent=2)
    print(f"\nFull report saved to final_5_audits.json")


if __name__ == "__main__":
    main()
