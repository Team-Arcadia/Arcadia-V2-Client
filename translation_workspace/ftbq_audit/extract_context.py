"""
Extract context per quest from chapter SNBT files:
- quest_id -> { chapter, tasks: [{type, item, entity}], rewards: [{type, item}], dependencies, x, y }

This lets us know WHAT the quest is about (kill X mob, craft Y item, etc.) so
that translations can be context-aware.
"""
import json
import os
import re

CHAPTERS_DIR = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/config/ftbquests/quests/chapters"
WS = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/ftbq_audit"


def parse_chapter_snbt(text):
    """Very lightweight SNBT walker focused on extracting quest data.
    Returns: {
        'filename': str,
        'chapter_id': str,
        'quests': { quest_id: { tasks: [...], rewards: [...], deps: [...], shape, x, y } }
    }
    """
    chap = {"filename": None, "chapter_id": None, "quests": {}}
    # Top-level chapter id and filename
    fn_m = re.search(r'filename:\s*"([^"]+)"', text)
    if fn_m:
        chap["filename"] = fn_m.group(1)
    # Chapter-level id (top-level, NOT inside quests)
    # Find first 'id: "X"' at lowest indent (top-level)
    for line in text.split("\n"):
        m = re.match(r'^\tid:\s*"([^"]+)"', line)
        if m:
            chap["chapter_id"] = m.group(1)
            break

    # Walk quests array — find each `{` block inside quests: [
    quests_start = text.find("\tquests: [")
    if quests_start < 0:
        return chap

    # Brute-force iterate each quest object: a quest object spans `\t\t{` to `\t\t}`
    depth = 0
    cur = []
    in_block = False
    after_quests = text[quests_start:]
    for line in after_quests.split("\n"):
        stripped = line.rstrip()
        if not in_block:
            if stripped == "\t\t{":
                in_block = True
                cur = []
                continue
            if stripped == "\t]":
                break
            continue
        if stripped == "\t\t}":
            # End of quest object - parse it
            block = "\n".join(cur)
            q = _parse_quest_block(block)
            if q and q.get("id"):
                chap["quests"][q["id"]] = q
            in_block = False
            cur = []
            continue
        cur.append(line)

    return chap


def _parse_quest_block(block):
    q = {}
    # ID
    m = re.search(r'\bid:\s*"([^"]+)"', block)
    if m:
        q["id"] = m.group(1)
    # Title (rare, usually in lang)
    m = re.search(r'\btitle:\s*"([^"]*)"', block)
    if m:
        q["inline_title"] = m.group(1)
    # Shape
    m = re.search(r'\bshape:\s*"([^"]+)"', block)
    if m:
        q["shape"] = m.group(1)
    # Position
    m = re.search(r"\bx:\s*([-\d.]+)d?", block)
    if m:
        q["x"] = float(m.group(1))
    m = re.search(r"\by:\s*([-\d.]+)d?", block)
    if m:
        q["y"] = float(m.group(1))
    # Icon (item shown in quest GUI)
    m = re.search(r'icon:\s*\{[^}]*?id:\s*"([^"]+)"', block, re.DOTALL)
    if m:
        q["icon"] = m.group(1)
    # Dependencies
    deps = re.findall(r'"([0-9A-F]{16})"', block)
    # Tasks
    q["tasks"] = []
    for tm in re.finditer(r"\{[^{}]*?\btype:\s*\"([^\"]+)\"[^{}]*?\}", block):
        task = tm.group(0)
        ttype = tm.group(1)
        entry = {"type": ttype}
        im = re.search(r'\bitem:\s*\{[^}]*?id:\s*"([^"]+)"', task, re.DOTALL)
        if im:
            entry["item"] = im.group(1)
        else:
            im = re.search(r'\bitem:\s*"([^"]+)"', task)
            if im:
                entry["item"] = im.group(1)
        em = re.search(r'\bentity:\s*"([^"]+)"', task)
        if em:
            entry["entity"] = em.group(1)
        bm = re.search(r'\bblock:\s*"([^"]+)"', task)
        if bm:
            entry["block"] = bm.group(1)
        am = re.search(r'\badvancement:\s*"([^"]+)"', task)
        if am:
            entry["advancement"] = am.group(1)
        countm = re.search(r"\bcount:\s*(\d+)L?", task)
        if countm:
            entry["count"] = int(countm.group(1))
        q["tasks"].append(entry)
    # Rewards
    q["rewards"] = []
    for rm in re.finditer(r"\{[^{}]*?\btype:\s*\"([^\"]+)\"[^{}]*?\}", block):
        # we already captured these as tasks too -- need a way to differentiate
        # Actually rewards are inside `rewards: [ ... ]` and tasks inside `tasks: [ ... ]`
        pass
    # Better: parse rewards block separately
    rw_m = re.search(r"rewards:\s*\[(.*?)\]", block, re.DOTALL)
    if rw_m:
        rw_content = rw_m.group(1)
        for rm in re.finditer(r"\{[^{}]*?\}", rw_content, re.DOTALL):
            piece = rm.group(0)
            tm2 = re.search(r'\btype:\s*"([^"]+)"', piece)
            if not tm2:
                continue
            entry = {"type": tm2.group(1)}
            im = re.search(r'\bitem:\s*\{[^}]*?id:\s*"([^"]+)"', piece, re.DOTALL)
            if im:
                entry["item"] = im.group(1)
            else:
                im = re.search(r'\bitem:\s*"([^"]+)"', piece)
                if im:
                    entry["item"] = im.group(1)
            xpm = re.search(r"\bxp:\s*(\d+)", piece)
            if xpm:
                entry["xp"] = int(xpm.group(1))
            xpl = re.search(r"\bxp_levels:\s*(\d+)", piece)
            if xpl:
                entry["xp_levels"] = int(xpl.group(1))
            q["rewards"].append(entry)
    # And re-parse tasks more strictly
    tk_m = re.search(r"tasks:\s*\[(.*?)\](?=\s*(?:rewards|x|y|shape|dependencies|hide|optional))", block, re.DOTALL)
    if tk_m:
        tk_content = tk_m.group(1)
        q["tasks"] = []
        for tm in re.finditer(r"\{[^{}]*?\}", tk_content, re.DOTALL):
            piece = tm.group(0)
            tm2 = re.search(r'\btype:\s*"([^"]+)"', piece)
            if not tm2:
                continue
            entry = {"type": tm2.group(1)}
            im = re.search(r'\bitem:\s*\{[^}]*?id:\s*"([^"]+)"', piece, re.DOTALL)
            if im:
                entry["item"] = im.group(1)
            else:
                im = re.search(r'\bitem:\s*"([^"]+)"', piece)
                if im:
                    entry["item"] = im.group(1)
            em = re.search(r'\bentity:\s*"([^"]+)"', piece)
            if em:
                entry["entity"] = em.group(1)
            am = re.search(r'\badvancement:\s*"([^"]+)"', piece)
            if am:
                entry["advancement"] = am.group(1)
            countm = re.search(r"\bcount:\s*(\d+)L?", piece)
            if countm:
                entry["count"] = int(countm.group(1))
            q["tasks"].append(entry)

    if deps:
        # Remove self id from deps
        if "id" in q:
            deps = [d for d in deps if d != q["id"]]
        # Limit to first few unique
        seen = set()
        cleaned = []
        for d in deps:
            if d not in seen:
                seen.add(d)
                cleaned.append(d)
        q["deps"] = cleaned[:10]
    return q


def main():
    os.makedirs(WS, exist_ok=True)
    all_context = {}  # quest_id -> {chapter_filename, ...}
    chapter_summary = {}
    for f in sorted(os.listdir(CHAPTERS_DIR)):
        if not f.endswith(".snbt"):
            continue
        path = os.path.join(CHAPTERS_DIR, f)
        with open(path, encoding="utf-8") as fp:
            text = fp.read()
        chap = parse_chapter_snbt(text)
        ch_filename = chap.get("filename") or f[:-5]
        ch_id = chap.get("chapter_id")
        chapter_summary[ch_filename] = {
            "id": ch_id,
            "filename": ch_filename,
            "n_quests": len(chap["quests"]),
        }
        for qid, q in chap["quests"].items():
            q["chapter"] = ch_filename
            q["chapter_id"] = ch_id
            all_context[qid] = q

    print(f"Total quests indexed: {len(all_context)}")
    print(f"Chapters processed: {len(chapter_summary)}")

    with open(os.path.join(WS, "quest_context.json"), "w", encoding="utf-8") as o:
        json.dump(all_context, o, ensure_ascii=False, indent=2)
    with open(os.path.join(WS, "chapter_summary.json"), "w", encoding="utf-8") as o:
        json.dump(chapter_summary, o, ensure_ascii=False, indent=2)

    print("\nChapters summary:")
    for k, v in sorted(chapter_summary.items()):
        print(f"  {v['filename']:35s} id={v['id']} quests={v['n_quests']}")


if __name__ == "__main__":
    main()
