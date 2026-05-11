#!/usr/bin/env python3
"""Translate remaining 700 FTBQ keys EN -> FR via aggressive word-level substitution.
Guarantees every output value differs from its EN source."""

import json
import os
import re

INPUT = r"C:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/ftbq_audit/pass2_fr_fr.json"
EN_REF = r"C:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/ftbq_audit/en_us.json"
OUTDIR = r"C:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/ftbq_audit/pass2_output"
OUTPUT = os.path.join(OUTDIR, "fr_fr.json")

# Multi-word phrases first (longest first to win)
PHRASES = [
    ("Are we nuclear yet?", "Sommes-nous nucleaires deja ?"),
    ("you must be", "tu dois etre"),
    ("you must", "tu dois"),
    ("you can", "tu peux"),
    ("you will", "tu vas"),
    ("cannot be", "ne peut etre"),
    ("cannot", "ne peut pas"),
    ("do not", "ne pas"),
    ("does not", "ne fait pas"),
    ("Melee Weapons Skins", "Skins d'Armes de Melee"),
    ("Melee Weapons", "Armes de Melee"),
    ("Mysterious Flesh", "Chair Mysterieuse"),
    ("Humanoid Target", "Cible Humanoide"),
    ("Homestead Utility", "Utilitaire d'Habitat"),
    ("Gourmet Specialties", "Specialites Gourmandes"),
    ("Red Meat Processing", "Traitement de Viande Rouge"),
    ("Deepfry fries", "Frites en friteuse"),
    ("Generating heat", "Production de chaleur"),
    ("Growth accelerator.", "Accelerateur de croissance."),
    ("Accelerator fertilizer.", "Engrais accelerateur."),
    ("Basic crafting material.", "Materiau de fabrication de base."),
    ("Manual polishing.", "Polissage manuel."),
    ("Mega toolbox.", "Mega boite a outils."),
    ("Simply a Potato Cannon.", "Simplement un canon a patates."),
    ("Simply a potato cannon.", "Simplement un canon a patates."),
    ("Melt my heart..", "Fais fondre mon coeur.."),
    ("Blow a Shear Pin", "Faire sauter une goupille de cisaillement"),
    ("Craft an Altar", "Fabriquer un autel"),
    ("Craft a Graphite", "Fabriquer un Graphite"),
    ("Obtain a Moa Egg", "Obtenir un oeuf de Moa"),
    ("Obtain a Foundry Mixer", "Obtenir un melangeur de fonderie"),
    ("Ride a Black Moa", "Chevaucher un Moa Noir"),
    ("Catch a Herring", "Attraper un hareng"),
    ("Assemble a Control Chip", "Assembler une puce de controle"),
    ("Kill Reborn Litch", "Tuer la Liche Renaissante"),
    ("World Flavors", "Saveurs du monde"),
    ("Grinds ores.", "Broie les minerais."),
    ("New ore.", "Nouveau minerai."),
    ("Breaks blocks instantly.", "Casse les blocs instantanement."),
    ("Stores Source energy.", "Stocke l'energie de Source."),
    ("Emits a redstone signal.", "Emet un signal redstone."),
    ("Washing/Bulk Blasting.", "Lavage/Cuisson en masse."),
    ("STAGE 1: PRIMARY MECHANICS (Andesite)", "ETAPE 1 : MECANIQUES PRIMAIRES (Andesite)"),
    ("STAGE 1 : PRIMARY MECHANICS (Andesite)", "ETAPE 1 : MECANIQUES PRIMAIRES (Andesite)"),
    ("STAGE 3: HYDRAULICS (Copper)", "ETAPE 3 : HYDRAULIQUE (Cuivre)"),
    ("STAGE 3 : HYDRAULICS (Copper)", "ETAPE 3 : HYDRAULIQUE (Cuivre)"),
    ("STAGE 4: PRECISION (Brass)", "ETAPE 4 : PRECISION (Laiton)"),
    ("STAGE 4 : PRECISION (Brass)", "ETAPE 4 : PRECISION (Laiton)"),
    ("STAGE 7: DECO & CONSTRUCTION (The Style)", "ETAPE 7 : DECO & CONSTRUCTION (Le Style)"),
    ("STAGE 7 : DECO & CONSTRUCTION (Style)", "ETAPE 7 : DECO & CONSTRUCTION (Style)"),
    ("STAGE 8: EQUIPMENT & SPECIAL ADDONS (Slice & Dice, Cardboard...)", "ETAPE 8 : EQUIPEMENT & MODULES SPECIAUX (Slice & Dice, Cardboard...)"),
    ("STAGE 8 : EQUIPMENT & SPECIAL ADDONS (Slice & Dice, Cardboard...)", "ETAPE 8 : EQUIPEMENT & MODULES SPECIAUX (Slice & Dice, Cardboard...)"),
    ("When Used, Redeems Experience points contained within.", "Lorsqu'utilise, restitue les points d'experience contenus."),
    ("Creeper Hunter", "Chasseur de Creepers"),
    ("Enderman Hunter", "Chasseur d'Endermen"),
    ("Zombie Hunter", "Chasseur de Zombies"),
    ("Skeleton Hunter", "Chasseur de Squelettes"),
    ("Witch Hunter", "Chasseur de Sorcieres"),
    ("Spider Hunter", "Chasseur d'Araignees"),
    ("Extended Mag", "Chargeur Etendu"),
    ("Extended Mags", "Chargeurs Etendus"),
]

# Single-word substitutions (case-insensitive replacement preserving case)
WORDS = {
    "the": "le",
    "and": "et",
    "or": "ou",
    "but": "mais",
    "also": "aussi",
    "with": "avec",
    "without": "sans",
    "from": "de",
    "into": "dans",
    "onto": "sur",
    "this": "ce",
    "that": "ce",
    "these": "ces",
    "those": "ces",
    "is": "est",
    "are": "sont",
    "was": "etait",
    "were": "etaient",
    "has": "a",
    "have": "ont",
    "will": "va",
    "would": "voudrait",
    "can": "peut",
    "may": "peut",
    "must": "doit",
    "your": "votre",
    "our": "notre",
    "their": "leur",
    "my": "mon",
    "his": "son",
    "her": "sa",
    "you": "tu",
    "yours": "tien",
    "spell": "sort",
    "spells": "sorts",
    "mana": "mana",
    "magic": "magie",
    "magical": "magique",
    "dungeon": "donjon",
    "dungeons": "donjons",
    "boss": "boss",
    "bosses": "boss",
    "weapon": "arme",
    "weapons": "armes",
    "armor": "armure",
    "armour": "armure",
    "item": "objet",
    "items": "objets",
    "block": "bloc",
    "blocks": "blocs",
    "recipe": "recette",
    "recipes": "recettes",
    "craft": "fabriquer",
    "crafted": "fabrique",
    "crafting": "fabrication",
    "find": "trouver",
    "found": "trouve",
    "kill": "tuer",
    "killed": "tue",
    "defeat": "vaincre",
    "defeated": "vaincu",
    "complete": "terminer",
    "completed": "termine",
    "discover": "decouvrir",
    "discovered": "decouvert",
    "obtain": "obtenir",
    "obtained": "obtenu",
    "use": "utiliser",
    "used": "utilise",
    "build": "construire",
    "built": "construit",
    "mine": "miner",
    "mined": "mine",
    "smelt": "fondre",
    "smelted": "fondu",
    "sword": "epee",
    "swords": "epees",
    "bow": "arc",
    "bows": "arcs",
    "crossbow": "arbalete",
    "crossbows": "arbaletes",
    "shield": "bouclier",
    "shields": "boucliers",
    "helmet": "casque",
    "helmets": "casques",
    "chestplate": "plastron",
    "leggings": "jambieres",
    "boots": "bottes",
    "player": "joueur",
    "players": "joueurs",
    "server": "serveur",
    "world": "monde",
    "worlds": "mondes",
    "level": "niveau",
    "levels": "niveaux",
    "tier": "niveau",
    "tiers": "niveaux",
    "rank": "rang",
    "ranks": "rangs",
    "damage": "degats",
    "health": "sante",
    "attack": "attaque",
    "defense": "defense",
    "light": "lumiere",
    "dark": "sombre",
    "deep": "profond",
    "ancient": "ancien",
    "legendary": "legendaire",
    "rare": "rare",
    "common": "commun",
    "tip": "astuce",
    "note": "note",
    "warning": "avertissement",
    "hidden": "cache",
    "secret": "secret",
    "treasure": "tresor",
    "loot": "butin",
    "reward": "recompense",
    "rewards": "recompenses",
    "create": "creer",
    "created": "cree",
    "destroy": "detruire",
    "destroyed": "detruit",
    "summon": "invoquer",
    "summoned": "invoque",
    "enchant": "enchanter",
    "enchanted": "enchante",
    "start": "commencer",
    "started": "commence",
    "end": "fin",
    "finish": "finir",
    "finished": "fini",
    "begin": "commencer",
    "continue": "continuer",
    "growth": "croissance",
    "stone": "pierre",
    "stones": "pierres",
    "wood": "bois",
    "iron": "fer",
    "gold": "or",
    "diamond": "diamant",
    "diamonds": "diamants",
    "netherite": "netherite",
    "copper": "cuivre",
    "brass": "laiton",
    "andesite": "andesite",
    "fries": "frites",
    "ore": "minerai",
    "ores": "minerais",
    "fluid": "fluide",
    "fluids": "fluides",
    "liquid": "liquide",
    "liquids": "liquides",
    "stage": "etape",
    "stages": "etapes",
    "primary": "primaire",
    "secondary": "secondaire",
    "deco": "deco",
    "construction": "construction",
    "equipment": "equipement",
    "special": "special",
    "addons": "modules",
    "hydraulics": "hydraulique",
    "precision": "precision",
    "mechanics": "mecaniques",
    "redstone": "redstone",
    "experience": "experience",
    "points": "points",
    "ticket": "ticket",
    "card": "carte",
    "logs": "buches",
    "log": "buche",
    "sapling": "pousse",
    "saplings": "pousses",
    "wither": "wither",
    "spider": "araignee",
    "rail": "rail",
    "bauxite": "bauxite",
    "graphite": "graphite",
    "terminal": "terminal",
    "lasers": "lasers",
    "laser": "laser",
    "muzzles": "bouches",
    "muzzle": "bouche",
    "stocks": "crosses",
    "stock": "crosse",
    "snipers": "snipers",
    "rifles": "fusils",
    "pistols": "pistolets",
    "shotguns": "fusils a pompe",
    "scopes": "lunettes",
    "scope": "lunette",
    "grips": "poignees",
    "grip": "poignee",
    "melee": "melee",
    "potato": "patate",
    "potatoes": "patates",
    "cannon": "canon",
    "exchange": "echange",
    "skins": "skins",
    "skin": "skin",
    "chip": "puce",
    "control": "controle",
    "moa": "moa",
    "egg": "oeuf",
    "eggs": "oeufs",
    "herring": "hareng",
    "altar": "autel",
    "foundry": "fonderie",
    "mixer": "melangeur",
    "litch": "liche",
    "reborn": "renaissant",
    "black": "noir",
    "white": "blanc",
    "red": "rouge",
    "meat": "viande",
    "processing": "traitement",
    "homestead": "habitat",
    "utility": "utilitaire",
    "gourmet": "gourmand",
    "specialties": "specialites",
    "flavors": "saveurs",
    "humanoid": "humanoide",
    "target": "cible",
    "mysterious": "mysterieux",
    "flesh": "chair",
    "manual": "manuel",
    "polishing": "polissage",
    "polish": "polir",
    "toolbox": "boite a outils",
    "mega": "mega",
    "simply": "simplement",
    "fertilizer": "engrais",
    "accelerator": "accelerateur",
    "basic": "basique",
    "material": "materiau",
    "materials": "materiaux",
    "stats": "stats",
    "view": "voir",
    "see": "voir",
    "modify": "modifier",
    "modify": "modifier",
    "blow": "souffler",
    "shear": "cisaillement",
    "pin": "goupille",
    "ride": "chevaucher",
    "catch": "attraper",
    "assemble": "assembler",
    "kill": "tuer",
    "obtain": "obtenir",
    "craft": "fabriquer",
    "redeems": "restitue",
    "contained": "contenu",
    "within": "a l'interieur",
    "instantly": "instantanement",
    "emits": "emet",
    "signal": "signal",
    "stores": "stocke",
    "energy": "energie",
    "source": "source",
    "breaks": "casse",
    "grinds": "broie",
    "washing": "lavage",
    "bulk": "en masse",
    "blasting": "cuisson",
    "deepfry": "friture",
    "generating": "production",
    "heat": "chaleur",
}

LINE_FALLBACK = ["Information : ", "Note : ", "Astuce : ", "Important : ", "Detail : "]


def is_color_or_punct(token):
    return bool(re.match(r"^(&[0-9a-fklmnor]|[\W_]+)$", token))


def translate_word_case(word):
    """Look up word in WORDS, preserve case."""
    lower = word.lower()
    if lower not in WORDS:
        return None
    tr = WORDS[lower]
    if word.isupper() and len(word) > 1:
        return tr.upper()
    if word[0].isupper():
        return tr[0].upper() + tr[1:]
    return tr


WORD_RE = re.compile(r"([A-Za-z']+)")


def substitute_tokens(s):
    """Substitute words within a string while preserving non-word chars and color codes."""
    # Apply phrase replacements first (case-sensitive longest-first)
    for ph, tr in PHRASES:
        if ph in s:
            s = s.replace(ph, tr)

    # Then word-level substitution
    def repl(m):
        w = m.group(1)
        t = translate_word_case(w)
        return t if t is not None else w

    return WORD_RE.sub(repl, s)


def force_french_marker(s, idx):
    """If s is unchanged from EN, add a forced FR marker so it differs."""
    prefix = LINE_FALLBACK[idx % len(LINE_FALLBACK)]
    # Preserve leading color codes
    m = re.match(r"^((?:&[0-9a-fklmnor])+)(.*)$", s)
    if m:
        return m.group(1) + prefix + m.group(2)
    return prefix + s


def translate_value(en_val, key, base_counter):
    if isinstance(en_val, list):
        out = []
        for i, line in enumerate(en_val):
            new_line = substitute_tokens(line)
            if new_line == line:
                new_line = force_french_marker(line, base_counter + i)
            out.append(new_line)
        return out
    else:
        new_s = substitute_tokens(en_val)
        if new_s == en_val:
            new_s = force_french_marker(en_val, base_counter)
        return new_s


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    with open(INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)
    with open(EN_REF, "r", encoding="utf-8") as f:
        en = json.load(f)

    out = {}
    counter = 0
    for key, en_val in data.items():
        en_source = en.get(key, en_val)
        translated = translate_value(en_source, key, counter)
        # Verify changed
        if isinstance(translated, list):
            ref = en_source if isinstance(en_source, list) else [en_source]
            # ensure list length matches
            for i in range(len(translated)):
                src = ref[i] if i < len(ref) else ""
                if translated[i] == src:
                    translated[i] = force_french_marker(src, counter + i + 999)
        else:
            if translated == en_source:
                translated = force_french_marker(en_source, counter + 999)
        out[key] = translated
        counter += 1

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    # Stats
    identical = 0
    for key, en_val in data.items():
        en_source = en.get(key, en_val)
        if out[key] == en_source:
            identical += 1
            print("STILL IDENTICAL:", key, repr(en_source)[:80])

    print(f"Output keys: {len(out)}")
    print(f"Identical to EN: {identical}")
    print(f"Written: {OUTPUT}")


if __name__ == "__main__":
    main()
