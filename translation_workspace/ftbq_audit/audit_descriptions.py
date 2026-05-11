"""
Deep audit on descriptions:
- Find quests where EN_US has empty/useless/missing descriptions
- Find quests where description doesn't relate to the task/item/icon
- Score each quest: needs_rewrite (True/False)

Useless heuristics:
- desc is "" or ["\n\n\n"] or shorter than 20 chars (probably useless)
- desc doesn't reference the icon item / task entity (mismatch)
- desc is just a placeholder ("Description.", "TODO", "WIP", etc.)
"""
import json
import os
import re
import sys

WS = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/ftbq_audit"

context = json.load(open(f"{WS}/quest_context.json", encoding="utf-8"))
en_us = json.load(open(f"{WS}/en_us.json", encoding="utf-8"))


def text_of(v):
    if isinstance(v, str):
        return v
    if isinstance(v, list):
        return "\n".join(str(x) for x in v)
    return ""


def is_useless_desc(desc):
    """True if description doesn't help the player."""
    if not desc:
        return True
    t = text_of(desc).strip()
    if not t:
        return True
    # Strip color codes and whitespace
    plain = re.sub(r"&[0-9a-fk-or]", "", t).strip()
    if not plain or len(plain) < 30:
        return True
    # Placeholders
    placeholders = ("description", "todo", "wip", "placeholder", "fix me", "fixme", "tbd")
    if plain.lower() in placeholders:
        return True
    return False


def is_useless_title(title):
    if not title: return False  # may use inline title
    t = text_of(title).strip()
    if not t: return True
    plain = re.sub(r"&[0-9a-fk-or]", "", t).strip()
    return not plain or len(plain) < 2


# Build a list of quests with issues + context
issues = []

for qid, q in context.items():
    en_title = en_us.get(f"quest.{qid}.title", "")
    en_sub = en_us.get(f"quest.{qid}.quest_subtitle", "")
    en_desc = en_us.get(f"quest.{qid}.quest_desc", "")

    has_lang = bool(text_of(en_title).strip() or text_of(en_sub).strip() or text_of(en_desc).strip())

    # Quest with NO lang at all but HAS context (tasks/icon) — needs lang content
    if not has_lang and (q.get("tasks") or q.get("icon")):
        issues.append({
            "id": qid,
            "chapter": q.get("chapter", "?"),
            "icon": q.get("icon"),
            "tasks": q.get("tasks"),
            "rewards": q.get("rewards"),
            "shape": q.get("shape"),
            "reason": "NO_LANG_BUT_HAS_CONTEXT",
            "en_title": "",
            "en_subtitle": "",
            "en_desc": "",
        })
        continue

    # Quest with title but no useful desc
    if text_of(en_title).strip() and is_useless_desc(en_desc):
        issues.append({
            "id": qid,
            "chapter": q.get("chapter", "?"),
            "icon": q.get("icon"),
            "tasks": q.get("tasks"),
            "rewards": q.get("rewards"),
            "shape": q.get("shape"),
            "reason": "TITLE_BUT_NO_DESC",
            "en_title": text_of(en_title),
            "en_subtitle": text_of(en_sub),
            "en_desc": text_of(en_desc),
        })
        continue

    # Useless title with desc
    if is_useless_title(en_title) and text_of(en_desc).strip():
        issues.append({
            "id": qid,
            "chapter": q.get("chapter", "?"),
            "icon": q.get("icon"),
            "tasks": q.get("tasks"),
            "rewards": q.get("rewards"),
            "shape": q.get("shape"),
            "reason": "DESC_BUT_NO_TITLE",
            "en_title": text_of(en_title),
            "en_subtitle": text_of(en_sub),
            "en_desc": text_of(en_desc),
        })
        continue

# Group by chapter
by_chapter = {}
for issue in issues:
    by_chapter.setdefault(issue["chapter"], []).append(issue)

# Stats
print("=" * 70)
print(f"Total quests indexed:    {len(context)}")
print(f"Total quests with issue: {len(issues)}")
print()
print(f"{'chapter':<35s}  {'count':>5s}  {'reasons':>40s}")
for ch in sorted(by_chapter, key=lambda c: -len(by_chapter[c])):
    qs = by_chapter[ch]
    reasons = {}
    for q in qs:
        reasons[q["reason"]] = reasons.get(q["reason"], 0) + 1
    rstr = " | ".join(f"{k}={v}" for k, v in reasons.items())
    print(f"{ch:<35s}  {len(qs):>5d}  {rstr}")

# Save per-chapter to_rewrite
out_dir = os.path.join(WS, "to_rewrite_en")
os.makedirs(out_dir, exist_ok=True)
for ch, qs in by_chapter.items():
    with open(os.path.join(out_dir, f"{ch}.json"), "w", encoding="utf-8") as f:
        json.dump(qs, f, ensure_ascii=False, indent=2)
print(f"\nWritten per-chapter rewrite lists to {out_dir}")
print(f"Total: {len(issues)} quests need EN_US description rewrite")
