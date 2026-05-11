"""
Build master per-quest file combining:
  - quest_context (chapter, tasks, rewards)
  - en_us title/desc/subtitle (base reference)
  - fr_fr current values (to detect what's there or missing/broken)

Per chapter, output a file with all quests + lang fields needed for translation.
"""
import json
import os
import re

WS = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/ftbq_audit"

context = json.load(open(f"{WS}/quest_context.json", encoding="utf-8"))
en_us = json.load(open(f"{WS}/en_us.json", encoding="utf-8"))
fr_fr = json.load(open(f"{WS}/fr_fr.json", encoding="utf-8"))


def text_of(v):
    if isinstance(v, str):
        return v
    if isinstance(v, list):
        return "\n".join(str(x) for x in v)
    return ""


# Group quests by chapter
by_chapter = {}
for qid, q in context.items():
    ch = q.get("chapter", "unknown")
    by_chapter.setdefault(ch, {})[qid] = q


# For each quest, gather all relevant lang fields
def get_lang_fields(qid, lang_data):
    """Get title, subtitle, desc for a quest id from a lang dict."""
    return {
        "title": lang_data.get(f"quest.{qid}.title", ""),
        "subtitle": lang_data.get(f"quest.{qid}.quest_subtitle", ""),
        "desc": lang_data.get(f"quest.{qid}.quest_desc", ""),
    }


MOJIBAKE = re.compile(r"[Ã][©®ª¨§¢«»]|â€™|â€œ|â€\x9d|Â[°§¨ª®©¶]|�")
EN_HINTS = re.compile(
    r"\b(the|and|with|for|from|in|on|at|will|would|should|defeat|gather|complete|craft|find|reach|kill|obtain|player|server)\b",
    re.IGNORECASE,
)


def diagnose(en_v, fr_v):
    """Return list of issues for an FR translation."""
    issues = []
    if isinstance(fr_v, str) and not fr_v.strip():
        issues.append("EMPTY")
    if isinstance(en_v, type(fr_v)):
        et = text_of(en_v).strip()
        ft = text_of(fr_v).strip()
        if et and ft and et == ft and re.search(r"[a-z]{3,}", et):
            issues.append("IDENTICAL_TO_EN")
    if MOJIBAKE.search(text_of(fr_v)):
        issues.append("MOJIBAKE")
    ft = text_of(fr_v)
    if len(ft) >= 30 and len(EN_HINTS.findall(ft)) >= 3:
        issues.append("EN_LEAK")
    if not fr_v:
        issues.append("MISSING")
    return issues


master = {}
for chapter, quests in by_chapter.items():
    master[chapter] = []
    for qid, q in quests.items():
        en = get_lang_fields(qid, en_us)
        fr = get_lang_fields(qid, fr_fr)

        issues = {
            "title": diagnose(en["title"], fr["title"]),
            "subtitle": diagnose(en["subtitle"], fr["subtitle"]),
            "desc": diagnose(en["desc"], fr["desc"]),
        }

        entry = {
            "id": qid,
            "icon": q.get("icon"),
            "shape": q.get("shape"),
            "tasks": q.get("tasks", []),
            "rewards": q.get("rewards", []),
            "deps": q.get("deps", []),
            "en": en,
            "fr": fr,
            "issues": issues,
        }
        master[chapter].append(entry)

# Sort each chapter by quest position (y then x) for logical flow
for ch in master:
    master[ch].sort(key=lambda q: (q.get("y", 0), q.get("x", 0)))

# Save per-chapter
master_dir = os.path.join(WS, "per_chapter")
os.makedirs(master_dir, exist_ok=True)
for ch, quests in master.items():
    with open(os.path.join(master_dir, f"{ch}.json"), "w", encoding="utf-8") as o:
        json.dump(quests, o, ensure_ascii=False, indent=2)

# Summary per chapter
summary = {}
for ch, quests in master.items():
    cnt = {"total": len(quests), "issues": {"title": 0, "subtitle": 0, "desc": 0}}
    for q in quests:
        for f in ("title", "subtitle", "desc"):
            if q["issues"][f]:
                cnt["issues"][f] += 1
    summary[ch] = cnt

print("=== Chapter quality summary ===")
print(f"{'chapter':<35s} {'quests':>6s}  {'title bad':>9s}  {'sub bad':>7s}  {'desc bad':>9s}")
for ch in sorted(summary, key=lambda c: -summary[c]["total"]):
    s = summary[ch]
    i = s["issues"]
    print(f"{ch:<35s} {s['total']:>6d}  {i['title']:>9d}  {i['subtitle']:>7d}  {i['desc']:>9d}")

with open(os.path.join(WS, "master_summary.json"), "w", encoding="utf-8") as o:
    json.dump(summary, o, ensure_ascii=False, indent=2)

print("\nMaster files written to per_chapter/")
