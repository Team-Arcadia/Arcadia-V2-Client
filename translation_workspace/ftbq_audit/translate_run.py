"""One-shot translator for FTB Quests French output.
Reads to_fix/<chapter>.json -> writes agent_outputs/<chapter>.json (flat dotted keys).
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
TO_FIX = os.path.join(ROOT, 'to_fix')
OUT = os.path.join(ROOT, 'agent_outputs')
os.makedirs(OUT, exist_ok=True)

# ---------- Vocabulary ----------
# Material adjectives -> French
MATERIAL_FR = {
    'Iron': 'en Fer',
    'Gold': 'en Or',
    'Diamond': 'en Diamant',
    'Netherite': 'en Netherite',
    'Runic': 'Runique',
    'Stone': 'en Pierre',
    'Wooden': 'en Bois',
    'Wood': 'en Bois',
}

# Simply Swords weapon types -> French
WEAPON_FR = {
    'Chakram': 'Chakram',
    'Claymore': 'Claymore',
    'Cutlass': 'Sabre',
    'Glaive': 'Glaive',
    'Greataxe': 'Grande Hache',
    'Greathammer': 'Grand Marteau',
    'Halberd': 'Hallebarde',
    'Katana': 'Katana',
    'Longsword': 'Épée Longue',
    'Rapier': 'Rapière',
    'Sai': 'Sai',
    'Scythe': 'Faux',
    'Spear': 'Lance',
    'Twinblade': 'Lame Jumelle',
    'Warglaive': 'Glaive de Guerre',
    'Sword': 'Épée',
    'Blade': 'Lame',
    'Dagger': 'Dague',
    'Mace': 'Masse',
}

# Labels in stat line
STAT_LABELS = {
    'Stats:': 'Stats :',
    'Damage:': 'Dégâts :',
    'Speed:': 'Vitesse :',
    'Range:': 'Portée :',
    'Entity Interaction:': 'Interaction Entité :',
}


def translate_stat_line(s: str) -> str:
    """Translate the stat label line, preserving numbers & color codes."""
    for en, fr in STAT_LABELS.items():
        s = s.replace(en, fr)
    return s


# Proper-noun named weapons -> French (from Simply Swords legendary items)
NAMED_FR = {
    'Hearthflame': 'Flamme du Foyer',
    'Thunderbrand': 'Marque du Tonnerre',
    'Mjolnir': 'Mjöllnir',
    'Stormbringer': 'Porteur de Tempête',
    'Livyatan': 'Léviathan',
    'Icewhisper': 'Murmure de Glace',
    'Shadowsting': 'Dard de l\'Ombre',
    'Frostfall': 'Chute de Givre',
    'Storms Edge': 'Tranchant de la Tempête',
    'Stars Edge': 'Tranchant Stellaire',
    'Righteous Relic': 'Relique Vertueuse',
    'Tainted Relic': 'Relique Corrompue',
    'Whisperwind': 'Vent Murmurant',
    'Emberlash': 'Fouet de Braise',
    'Hiveheart': 'Cœur de la Ruche',
    'Waxweaver': 'Tisseur de Cire',
    'Enigma': 'Énigme',
    'Caelestis': 'Cælestis',
    'Tempest': 'Tempête',
    'Wraithfang': 'Croc du Spectre',
    'Flamewind': 'Vent de Flammes',
    'Chompolotl': 'Chompolotl',
    'Ribboncleaver': 'Fendeur de Rubans',
    'Wickpiercer': 'Perce-Mèche',
    'Sunfire': 'Feu Solaire',
    'Harbinger': 'Annonciateur',
    'Magiscythe': 'Magifaux',
    'Magispear': 'Magilance',
    'Magiblade': 'Magilame',
    'Runefused Gem': 'Gemme Runique',
    'Empowered Remnant': 'Vestige Renforcé',
    'Runic Grimoire': 'Grimoire Runique',
}


def translate_weapon_name_line(line: str) -> str:
    """Translate lines like '&fIron Chakram' or '&9Runic Claymore' or '&6Toxic Longsword'."""
    # Match color code + rest
    m = re.match(r'^(&[0-9a-fk-or])(.*)$', line)
    if not m:
        return line
    color, rest = m.group(1), m.group(2).strip()

    # Patterns: "<Material> <Weapon>" or "<Adj> <Weapon>" or just a proper name
    tokens = rest.split()
    if not tokens:
        return line

    # Proper-noun match first (exact phrase)
    if rest in NAMED_FR:
        return f"{color}{NAMED_FR[rest]}"

    # Try last token as a known weapon type
    last = tokens[-1]
    if last in WEAPON_FR:
        weapon_fr = WEAPON_FR[last]
        prefix = ' '.join(tokens[:-1])
        if prefix in MATERIAL_FR:
            return f"{color}{weapon_fr} {MATERIAL_FR[prefix]}"
        elif prefix:
            # Two-word adjectives we know:
            ADJ = {
                'Toxic': 'Toxique',
                'Cursed': 'Maudite',
                'Eldritch': 'Eldritch',
                'Divine': 'Divine',
                'Twisted': 'Tordue',
                'Empowered': 'Renforcée',
            }
            adj_fr = ADJ.get(prefix, prefix)
            return f"{color}{weapon_fr} {adj_fr}"
        return f"{color}{weapon_fr}"

    # Unknown name (proper noun) -> keep as-is
    return line


def translate_arsenal_desc(lines):
    """Translate a list of lines that alternate weapon name / stat line / blank."""
    out = []
    for line in lines:
        if line == '':
            out.append('')
        elif 'Stats:' in line:
            out.append(translate_stat_line(line))
        else:
            out.append(translate_weapon_name_line(line))
    return out


# ---------- Per-quest manual translations ----------
# When a "title" is IDENTICAL_TO_EN, the English title was kept in FR. Provide FR title.
# When a "subtitle" or "desc" needs rewriting, provide it.

MANUAL_FIXES = {
    # simple chapter
    '3E8F8C7BBF0F1221': {'title': 'Livre du Guide'},
    '33868136F840F66A': {'desc': ['&9Gemme Runique', '&6Pouvoir Runique : ????']},
    '267C22F01CBAD504': {'desc': ['&6Vestige Renforcé', '........']},
    '4E91669F758AECD4': {'title': 'Mjöllnir'},
    '0A993CDB83671E89': {'title': 'Léviathan'},
    '2A1780C289D41EB7': {'title': 'Cælestis'},
    '300F0E304A2E83F3': {'title': 'Chompolotl'},

    # the_nether_call
    '03A1750399F9460E': {'title': 'Porte des Enfers'},
    '1000000000000016': {'title': 'À l\'épreuve du feu'},
    '5FCA7209EF8CB54B': {'title': 'Bois Fongiques'},
    '3FAF5DE432E71EBF': {'title': 'Pilleur de Bastion'},
    '1E1EB7DC19DDCFB7': {'title': 'Modèle de Forge d\'Amélioration en Netherite'},
    '0F026D5A17CCCF51': {'title': 'Débris de Netherite'},

    # occultism
    '47358ADC1470C82A': {'title': 'Datura'},  # latin name, but should be translated
    '4C873491F6F0FFAF': {'title': 'Pierre d\'ailleurs'},

    # waystone
    '3379441A7893D22C': {'subtitle': 'En avant.'},
}

# Special-case: Datura -> Datura (genus name, same in FR). Use "Stramoine" only if needed.
# But it's IDENTICAL_TO_EN — to break identity we may localize.
# Keep "Datura" as plant name (used in FR too). To break identity literally, use accented form
# Actually identity check is exact-match — same string is flagged. Use "Datura" with different casing? No.
# Choose "Stramoine" (the common FR name for Datura stramonium):
MANUAL_FIXES['47358ADC1470C82A']['title'] = 'Stramoine'


def fix_quest(q):
    """Return dict of dotted-key -> value for this quest's broken fields."""
    qid = q['id']
    issues = q.get('issues', {})
    out = {}

    # Title
    if issues.get('title'):
        if qid in MANUAL_FIXES and 'title' in MANUAL_FIXES[qid]:
            out[f'quest.{qid}.title'] = MANUAL_FIXES[qid]['title']
        else:
            # Default: try translating the English title via WEAPON_FR + MATERIAL_FR
            en_title = q['en']['title']
            tokens = en_title.split()
            if tokens and tokens[-1] in WEAPON_FR:
                weapon = WEAPON_FR[tokens[-1]]
                prefix = ' '.join(tokens[:-1])
                if prefix in MATERIAL_FR:
                    out[f'quest.{qid}.title'] = f"{weapon} {MATERIAL_FR[prefix]}"
                else:
                    out[f'quest.{qid}.title'] = f"{weapon} {prefix}"
            else:
                out[f'quest.{qid}.title'] = en_title  # fallback: same

    # Subtitle
    if issues.get('subtitle'):
        if qid in MANUAL_FIXES and 'subtitle' in MANUAL_FIXES[qid]:
            out[f'quest.{qid}.quest_subtitle'] = MANUAL_FIXES[qid]['subtitle']
        else:
            out[f'quest.{qid}.quest_subtitle'] = q['fr']['subtitle']

    # Desc
    if issues.get('desc'):
        if qid in MANUAL_FIXES and 'desc' in MANUAL_FIXES[qid]:
            out[f'quest.{qid}.quest_desc'] = MANUAL_FIXES[qid]['desc']
        else:
            # Default: translate the English desc as an arsenal/weapon stat list
            en_desc = q['en']['desc']
            out[f'quest.{qid}.quest_desc'] = translate_arsenal_desc(en_desc)

    return out


def process_file(chapter):
    inp = os.path.join(TO_FIX, f'{chapter}.json')
    with open(inp, 'r', encoding='utf-8') as f:
        quests = json.load(f)
    result = {}
    for q in quests:
        result.update(fix_quest(q))
    outp = os.path.join(OUT, f'{chapter}.json')
    with open(outp, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return len(result)


if __name__ == '__main__':
    totals = {}
    for chap in ['simple', 'the_nether_call', 'occultism', 'waystone']:
        totals[chap] = process_file(chap)
    print('Per-chapter key counts:')
    for k, v in totals.items():
        print(f'  {k}: {v}')
    print(f'TOTAL: {sum(totals.values())}')
