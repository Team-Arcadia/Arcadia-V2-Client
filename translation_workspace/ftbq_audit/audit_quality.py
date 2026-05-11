"""
Audit FTB Quests translations for quality issues:
- Missing keys (per lang vs en_us)
- FR=EN (untranslated leak)
- Mojibake (encoding corruption)
- Empty values
- EN word density too high (untranslated paragraphs in FR/ES/PT/RU/ZH)
- Format code mismatch
"""
import json
import os
import re

WS = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/ftbq_audit"

LANGS = ["en_us", "en_gb", "fr_fr", "es_es", "pt_br", "ru_ru", "zh_cn"]
BASE = "en_us"

EN_WORDS = re.compile(
    r"\b(the|and|with|of|to|for|from|by|in|on|at|will|would|should|can|cannot|could|may|allow|prevent|increase|decrease|require|enable|disable|toggle|reduce|create|destroy|player|server|inventory|crafting|recipe|tooltip|cooldown|chance|amount|level|right-click|left-click|sneak|jump|sprint|every|always|never|sometimes|nothing|something|here|there|when|where|while|because|though|already|enough|been|using|this|that|these|those|complete|defeat|gather|collect|craft|find|build|reach|kill|obtain)\b",
    re.IGNORECASE,
)

MOJIBAKE = re.compile(r"[Ã][©®ª¨§¢«»]|â€™|â€œ|â€\x9d|Â[°§¨ª®©¶]|�")


def load_lang(lang):
    with open(os.path.join(WS, f"{lang}.json"), encoding="utf-8") as f:
        return json.load(f)


def text_of(v):
    if isinstance(v, str):
        return v
    if isinstance(v, list):
        return "\n".join(str(x) for x in v)
    return str(v)


def has_mojibake(s):
    return isinstance(s, str) and bool(MOJIBAKE.search(s))


def count_en_words(s):
    return len(EN_WORDS.findall(s))


def fmt_codes(s):
    if not isinstance(s, str):
        s = text_of(s)
    return tuple(sorted(re.findall(r"%[sd%]|%\d\$[sd]|\{\d+\}", s)))


def main():
    langs = {l: load_lang(l) for l in LANGS}
    base = langs[BASE]
    base_keys = set(base.keys())

    report = {l: {
        "total_keys": len(langs[l]),
        "missing_keys": [],
        "identical_to_base": [],
        "mojibake": [],
        "english_leak": [],
        "empty": [],
        "code_mismatch": [],
    } for l in LANGS if l != BASE}

    # Per-lang issues
    for lang in LANGS:
        if lang == BASE:
            continue
        lang_data = langs[lang]
        lang_keys = set(lang_data.keys())

        # Missing keys
        missing = base_keys - lang_keys
        report[lang]["missing_keys"] = sorted(missing)

        for k in lang_keys & base_keys:
            base_v = base[k]
            lang_v = lang_data[k]
            base_t = text_of(base_v)
            lang_t = text_of(lang_v)

            # Empty
            if not lang_t.strip():
                report[lang]["empty"].append(k)
                continue

            # Mojibake
            if has_mojibake(lang_t):
                report[lang]["mojibake"].append(k)

            # Identical to base (untranslated)
            if (
                lang_t.strip() == base_t.strip()
                and len(base_t.strip()) >= 5
                and not lang.startswith("en_")
            ):
                # Skip values that are intentional (numbers, proper nouns short)
                if re.search(r"[a-z]{3,}", base_t):
                    report[lang]["identical_to_base"].append(k)

            # English leak (only for non-English langs)
            if not lang.startswith("en_") and isinstance(lang_t, str):
                en_count = count_en_words(lang_t)
                if en_count >= 3 and len(lang_t) >= 30:
                    report[lang]["english_leak"].append(k)

            # Format code mismatch
            if isinstance(base_v, type(lang_v)) and fmt_codes(base_v) != fmt_codes(lang_v):
                report[lang]["code_mismatch"].append(k)

    # Print summary
    print("=" * 70)
    print("FTB QUESTS TRANSLATION AUDIT — SUMMARY")
    print("=" * 70)
    print(f"Base: {BASE} ({len(base)} keys)")
    print()
    print(f"{'lang':<8s} {'missing':>8s} {'unstrans':>9s} {'mojib':>6s} {'EN_leak':>8s} {'empty':>6s} {'fmt_mm':>7s}")
    for lang in LANGS:
        if lang == BASE:
            continue
        r = report[lang]
        print(
            f"{lang:<8s} "
            f"{len(r['missing_keys']):>8d} "
            f"{len(r['identical_to_base']):>9d} "
            f"{len(r['mojibake']):>6d} "
            f"{len(r['english_leak']):>8d} "
            f"{len(r['empty']):>6d} "
            f"{len(r['code_mismatch']):>7d}"
        )

    # Detailed dump per lang
    for lang in LANGS:
        if lang == BASE:
            continue
        r = report[lang]
        print()
        print(f"--- {lang} samples (first 5 per category) ---")
        for cat in ["missing_keys", "identical_to_base", "english_leak", "mojibake", "empty"]:
            items = r[cat][:5]
            if not items:
                continue
            print(f"  {cat}:")
            for k in items:
                if cat == "missing_keys":
                    base_v = base.get(k, "")
                    print(f"    [{k}] EN_US = {text_of(base_v)[:80]!r}")
                else:
                    lang_v = langs[lang].get(k, "")
                    print(f"    [{k}] {lang} = {text_of(lang_v)[:80]!r}")

    # Save full report
    with open(os.path.join(WS, "audit_report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print()
    print("Full report saved to audit_report.json")


if __name__ == "__main__":
    main()
