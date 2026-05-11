"""
Fill missing title/subtitle/desc for the 1438 orphan quests using fallback heuristics:
- If title missing: derive from subtitle (first 30 chars) or use generic
- If subtitle missing: use first line of desc or generic
- If desc missing: use subtitle as desc or generic

For each quest, generate the fill in all 7 languages.
Since most orphans are technical quests (mechanics tutorials, weapon tiers, hunter bounties),
the fallback is good enough — they already have at least 1 informative field.
"""
import json
import os
import re

WS = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/ftbq_audit"

qs = json.load(open(f"{WS}/phase3_to_complete/_orphan.json", encoding="utf-8"))


def strip_codes(s):
    return re.sub(r"&[0-9a-fk-or]", "", s).strip()


def truncate(s, n=30):
    s = s.strip()
    if len(s) <= n:
        return s
    return s[: n - 1].rstrip() + "…"


# Generic fallback strings per lang
GENERIC = {
    "en_us": {
        "title": "Discovery",
        "subtitle": "Knowledge awaits.",
        "desc": ["Hover over the icon or check the tasks panel for more information."],
    },
    "en_gb": {
        "title": "Discovery",
        "subtitle": "Knowledge awaits.",
        "desc": ["Hover over the icon or check the tasks panel for more information."],
    },
    "fr_fr": {
        "title": "Découverte",
        "subtitle": "Le savoir vous attend.",
        "desc": ["Passez la souris sur l'icône ou consultez le panneau des tâches pour plus d'informations."],
    },
    "es_es": {
        "title": "Descubrimiento",
        "subtitle": "El conocimiento espera.",
        "desc": ["Pasa el cursor sobre el icono o consulta el panel de tareas para más información."],
    },
    "pt_br": {
        "title": "Descoberta",
        "subtitle": "O conhecimento aguarda.",
        "desc": ["Passe o cursor sobre o ícone ou veja o painel de tarefas para mais informações."],
    },
    "ru_ru": {
        "title": "Открытие",
        "subtitle": "Знание ждёт.",
        "desc": ["Наведи курсор на иконку или проверь панель задач для дополнительной информации."],
    },
    "zh_cn": {
        "title": "发现",
        "subtitle": "知识在等待。",
        "desc": ["将鼠标悬停在图标上或查看任务面板以获取更多信息。"],
    },
}

# Subtitle prefix translations
SUBTITLE_HINTS = {
    "en_us": "About this quest.",
    "en_gb": "About this quest.",
    "fr_fr": "À propos de cette quête.",
    "es_es": "Acerca de esta misión.",
    "pt_br": "Sobre esta missão.",
    "ru_ru": "Об этом задании.",
    "zh_cn": "关于此任务。",
}


def fill_for(q):
    """Return {lang: {field: value}} for missing fields only."""
    t = q["current_title"].strip()
    s = q["current_subtitle"].strip()
    d = q["current_desc"].strip()
    plain_t = strip_codes(t)
    plain_s = strip_codes(s)
    plain_d = strip_codes(d)

    out = {}
    for lang, gen in GENERIC.items():
        out_lang = {}
        if not t:
            # Derive from subtitle first line if available
            if plain_s:
                out_lang["title"] = truncate(plain_s, 30)
            elif plain_d:
                first_line = plain_d.split("\n")[0]
                out_lang["title"] = truncate(first_line, 30)
            else:
                out_lang["title"] = gen["title"]
        if not s:
            if plain_t:
                out_lang["quest_subtitle"] = SUBTITLE_HINTS[lang]
            elif plain_d:
                first_line = plain_d.split("\n")[0]
                out_lang["quest_subtitle"] = truncate(first_line, 80)
            else:
                out_lang["quest_subtitle"] = gen["subtitle"]
        if not d:
            # Use subtitle as desc
            if s:
                out_lang["quest_desc"] = [s]
            elif t:
                out_lang["quest_desc"] = [t]
            else:
                out_lang["quest_desc"] = gen["desc"]
        if out_lang:
            out[lang] = out_lang
    return out


result = {}
for q in qs:
    fills = fill_for(q)
    if fills:
        result[q["id"]] = fills

print(f"Quests filled: {len(result)}")
# Stats per lang
per_lang = {l: 0 for l in GENERIC}
for qid, langs in result.items():
    for l, fields in langs.items():
        per_lang[l] += len(fields)
for l, c in per_lang.items():
    print(f"  {l}: {c} fields")

# Save
os.makedirs(f"{WS}/phase3_output", exist_ok=True)
with open(f"{WS}/phase3_output/bin_auto.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f"\nSaved to phase3_output/bin_auto.json")
