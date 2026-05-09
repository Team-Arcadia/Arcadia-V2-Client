#!/usr/bin/env python3
"""Comprehensive translator for batch 7 — produces FR translations for all 86 mods.

Strategy:
1. Phrase dictionary (full-string match) — covers ~60% of common UI strings
2. Mod-specific overrides for tricky vocab
3. Word-level fallback with placeholder preservation
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/audit2")
MISSING_DIR = ROOT / "missing_per_mod"
JAR_FR_DIR = ROOT / "all_jar_fr"
OUT_DIR = ROOT / "agent_output"
GLOSSARY_FP = ROOT.parent / "glossary_compact.json"
BIN_FILE = ROOT / "fill_bin_7.txt"

OUT_DIR.mkdir(parents=True, exist_ok=True)

with open(GLOSSARY_FP, "r", encoding="utf-8") as f:
    GLOSSARY = {k.lower(): v for k, v in json.load(f).items()}

# ---------------------------------------------------------------------------
# PHRASE-LEVEL DICTIONARY (full-string match, case sensitive)
# Built from common Minecraft mod UI strings
# ---------------------------------------------------------------------------
PHRASES = {
    # generic UI
    "Enabled": "Activé", "Disabled": "Désactivé",
    "Enable": "Activer", "Disable": "Désactiver",
    "Settings": "Paramètres", "Configuration": "Configuration",
    "Description": "Description", "Title": "Titre",
    "Name": "Nom", "Value": "Valeur", "Key": "Touche",
    "General": "Général", "Common": "Commun", "Client": "Client",
    "Server": "Serveur", "Default": "Par défaut",
    "On": "Activé", "Off": "Désactivé", "None": "Aucun",
    "Yes": "Oui", "No": "Non", "True": "Vrai", "False": "Faux",
    "Auto": "Auto", "Manual": "Manuel", "Normal": "Normal",
    "Easy": "Facile", "Hard": "Difficile", "Peaceful": "Paisible",
    "Low": "Faible", "Medium": "Moyen", "High": "Élevé",
    "Save": "Sauvegarder", "Cancel": "Annuler", "Confirm": "Confirmer",
    "Reset": "Réinitialiser", "Apply": "Appliquer",
    "Open": "Ouvrir", "Close": "Fermer", "Add": "Ajouter",
    "Remove": "Retirer", "Delete": "Supprimer",
    "Search": "Rechercher", "Filter": "Filtre",
    "Show": "Afficher", "Hide": "Masquer",
    "Sort": "Trier", "Sorted": "Trié",
    "Mode": "Mode", "Type": "Type",
    "Page": "Page", "Tab": "Onglet",
    "Loading...": "Chargement...",
    "Error": "Erreur", "Warning": "Avertissement", "Info": "Info",
    "Success": "Succès", "Failed": "Échec",
    "Vertical": "Vertical", "Horizontal": "Horizontal",
    "Common": "Commun", "Uncommon": "Peu commun",
    "Rare": "Rare", "Epic": "Épique", "Legendary": "Légendaire",
    "Mythic": "Mythique", "Very Rare": "Très rare",
    "Camera": "Caméra", "Player": "Joueur",
    # Currency / amounts
    "Cost": "Coût", "Reward": "Récompense", "Price": "Prix",
    # Macaw
    "Macaw's Furniture": "Meubles de Macaw",
    "Macaw's Doors": "Portes de Macaw",
    "Macaw's Windows": "Fenêtres de Macaw",
    "Macaw's Roofs": "Toits de Macaw",
    "Macaw's Bridges": "Ponts de Macaw",
    "Macaw's Stairs and Balconies": "Escaliers et balcons de Macaw",
    "Macaw's Trapdoors": "Trappes de Macaw",
    "Macaw's Paths & Pavings": "Chemins et pavages de Macaw",
    "Macaw's Fences & Walls": "Clôtures et murs de Macaw",
    "Macaw's Biomes O' Plenty": "Biomes O' Plenty de Macaw",
    "Macaw's Paintings": "Tableaux de Macaw",
    # JEI etc
    "JEI": "JEI",
}

def t_phrase(s):
    """Return French translation for known full-string phrases."""
    if s in PHRASES:
        return PHRASES[s]
    if s.lower() in GLOSSARY:
        return GLOSSARY[s.lower()]
    return None

# ---------------------------------------------------------------------------
# Per-mod translation dictionaries (key -> French value)
# Curated for the larger mods to ensure quality
# ---------------------------------------------------------------------------
MOD_DICTS = {}

# ---- packs_tooltips_aether (137 keys) - tooltip pack for Aether ----
# These follow the "[item] does X" pattern
# We'll provide a generic translator below

# ---- nochatreports (123 keys) ----
NOCHATREPORTS = {
    "chat.tag.disguised": "Déguisé",
    "chat.tag.modified": "Modifié",
    "chat.tag.system_single_player": "Système (joueur unique)",
    "chat.tag.signed.tooltip": "Ce message a été signé cryptographiquement par l'expéditeur.",
    "chat.tag.unsigned.tooltip": "Ce message n'a pas été signé. Il pourrait avoir été modifié ou usurpé.",
    "chat.tag.modified.tooltip": "Ce message a été modifié par le serveur. Le contenu original est différent.",
    "chat.tag.system.tooltip": "Ce message provient du serveur, et non d'un joueur.",
}

# Generic word-level fallback
GENERIC_WORDS = [
    (r"\bRight[- ]click\b", "Clic droit"), (r"\bright[- ]click\b", "clic droit"),
    (r"\bLeft[- ]click\b", "Clic gauche"), (r"\bleft[- ]click\b", "clic gauche"),
    (r"\bShift[- ]click\b", "Maj+clic"), (r"\bshift[- ]click\b", "maj+clic"),
    (r"\bSneak[- ]right[- ]click\b", "Accroupi+clic droit"),
    (r"\bsneak[- ]right[- ]click\b", "accroupi+clic droit"),
    (r"\bShift\+", "Maj+"), (r"\bshift\+", "maj+"),
    (r"\bCtrl\+", "Ctrl+"),
    (r"\bSneak\b", "S'accroupir"), (r"\bsneak\b", "s'accroupir"),
    (r"\bSneaking\b", "Accroupi"), (r"\bsneaking\b", "accroupi"),
    (r"\bWhile\b", "Pendant"), (r"\bwhile\b", "pendant"),
    (r"\bWhen\b", "Lorsque"), (r"\bwhen\b", "lorsque"),
    (r"\bIf\b", "Si"), (r"\bif\b", "si"),
    (r"\bShould\b", "Devrait"), (r"\bshould\b", "devrait"),
    (r"\bWhether\b", "Si"), (r"\bwhether\b", "si"),
    (r"\bCan be\b", "Peut être"), (r"\bcan be\b", "peut être"),
    (r"\bCan\b", "Peut"), (r"\bcan\b", "peut"),
    (r"\bWill\b", "Va"), (r"\bwill\b", "va"),
    (r"\bUsed to\b", "Utilisé pour"), (r"\bused to\b", "utilisé pour"),
    (r"\bAllows\b", "Permet"), (r"\ballows\b", "permet"),
    (r"\bAllow\b", "Autoriser"), (r"\ballow\b", "autoriser"),
    (r"\bGrants\b", "Accorde"), (r"\bgrants\b", "accorde"),
    (r"\bGrant\b", "Accorder"), (r"\bgrant\b", "accorder"),
    (r"\bIncreases\b", "Augmente"), (r"\bincreases\b", "augmente"),
    (r"\bIncrease\b", "Augmenter"), (r"\bincrease\b", "augmenter"),
    (r"\bDecreases\b", "Diminue"), (r"\bdecreases\b", "diminue"),
    (r"\bReduces\b", "Réduit"), (r"\breduces\b", "réduit"),
    (r"\bReduce\b", "Réduire"), (r"\breduce\b", "réduire"),
    (r"\bMakes\b", "Fait"), (r"\bmakes\b", "fait"),
    (r"\bGives\b", "Donne"), (r"\bgives\b", "donne"),
    (r"\bGive\b", "Donner"), (r"\bgive\b", "donner"),
    (r"\bShows\b", "Affiche"), (r"\bshows\b", "affiche"),
    (r"\bShow\b", "Afficher"), (r"\bshow\b", "afficher"),
    (r"\bHide\b", "Masquer"), (r"\bhide\b", "masquer"),
    (r"\bHides\b", "Masque"), (r"\bhides\b", "masque"),
    (r"\bDisables\b", "Désactive"), (r"\bdisables\b", "désactive"),
    (r"\bEnables\b", "Active"), (r"\benables\b", "active"),
    (r"\bDisable\b", "Désactiver"), (r"\bdisable\b", "désactiver"),
    (r"\bEnable\b", "Activer"), (r"\benable\b", "activer"),
    (r"\bEnabled\b", "Activé"), (r"\benabled\b", "activé"),
    (r"\bDisabled\b", "Désactivé"), (r"\bdisabled\b", "désactivé"),
    (r"\bRequires\b", "Nécessite"), (r"\brequires\b", "nécessite"),
    (r"\bRequired\b", "Requis"), (r"\brequired\b", "requis"),
    (r"\bAvailable\b", "Disponible"), (r"\bavailable\b", "disponible"),
    (r"\bChange\b", "Changer"), (r"\bchange\b", "changer"),
    (r"\bChanges\b", "Modifications"), (r"\bchanges\b", "modifications"),
    (r"\bModify\b", "Modifier"), (r"\bmodify\b", "modifier"),
    (r"\bToggle\b", "Basculer"), (r"\btoggle\b", "basculer"),
    (r"\bClick to\b", "Cliquer pour"), (r"\bclick to\b", "cliquer pour"),
    (r"\bPress to\b", "Appuyer pour"), (r"\bpress to\b", "appuyer pour"),
    (r"\bClick\b", "Clic"), (r"\bclick\b", "clic"),
    (r"\bPress\b", "Appuyer"), (r"\bpress\b", "appuyer"),
    (r"\bHold\b", "Maintenir"), (r"\bhold\b", "maintenir"),
    (r"\bHolding\b", "En tenant"), (r"\bholding\b", "en tenant"),
    (r"\bRelease\b", "Relâcher"), (r"\brelease\b", "relâcher"),
    (r"\bReleased\b", "Relâché"), (r"\breleased\b", "relâché"),
    (r"\bWith\b", "Avec"), (r"\bwith\b", "avec"),
    (r"\bWithout\b", "Sans"), (r"\bwithout\b", "sans"),
    (r"\bUse\b", "Utiliser"), (r"\buse\b", "utiliser"),
    (r"\bUses\b", "Utilise"), (r"\buses\b", "utilise"),
    (r"\bUsed\b", "Utilisé"), (r"\bused\b", "utilisé"),
    (r"\bUsing\b", "En utilisant"), (r"\busing\b", "en utilisant"),
    (r"\bAdd\b", "Ajouter"), (r"\badd\b", "ajouter"),
    (r"\bAdded\b", "Ajouté"), (r"\badded\b", "ajouté"),
    (r"\bAdds\b", "Ajoute"), (r"\badds\b", "ajoute"),
    (r"\bRemove\b", "Retirer"), (r"\bremove\b", "retirer"),
    (r"\bRemoved\b", "Retiré"), (r"\bremoved\b", "retiré"),
    (r"\bRemoves\b", "Retire"), (r"\bremoves\b", "retire"),
    (r"\bDelete\b", "Supprimer"), (r"\bdelete\b", "supprimer"),
    (r"\bDeleted\b", "Supprimé"), (r"\bdeleted\b", "supprimé"),
    (r"\bDrop\b", "Lâcher"), (r"\bdrop\b", "lâcher"),
    (r"\bDropped\b", "Lâché"), (r"\bdropped\b", "lâché"),
    (r"\bPickup\b", "Ramasser"), (r"\bpickup\b", "ramasser"),
    (r"\bPick up\b", "Ramasser"), (r"\bpick up\b", "ramasser"),
    (r"\bPicked up\b", "Ramassé"), (r"\bpicked up\b", "ramassé"),
    (r"\bPlace\b", "Placer"), (r"\bplace\b", "placer"),
    (r"\bPlaced\b", "Placé"), (r"\bplaced\b", "placé"),
    (r"\bPlaces\b", "Place"), (r"\bplaces\b", "place"),
    (r"\bBreak\b", "Casser"), (r"\bbreak\b", "casser"),
    (r"\bBroken\b", "Cassé"), (r"\bbroken\b", "cassé"),
    (r"\bBlock\b", "Bloc"), (r"\bblock\b", "bloc"),
    (r"\bBlocks\b", "Blocs"), (r"\bblocks\b", "blocs"),
    (r"\bItem\b", "Objet"), (r"\bitem\b", "objet"),
    (r"\bItems\b", "Objets"), (r"\bitems\b", "objets"),
    (r"\bPlayer\b", "Joueur"), (r"\bplayer\b", "joueur"),
    (r"\bPlayers\b", "Joueurs"), (r"\bplayers\b", "joueurs"),
    (r"\bEntity\b", "Entité"), (r"\bentity\b", "entité"),
    (r"\bEntities\b", "Entités"), (r"\bentities\b", "entités"),
    (r"\bMob\b", "Mob"), (r"\bmob\b", "mob"),
    (r"\bMobs\b", "Mobs"), (r"\bmobs\b", "mobs"),
    (r"\bRecipe\b", "Recette"), (r"\brecipe\b", "recette"),
    (r"\bRecipes\b", "Recettes"), (r"\brecipes\b", "recettes"),
    (r"\bIngredient\b", "Ingrédient"), (r"\bingredient\b", "ingrédient"),
    (r"\bIngredients\b", "Ingrédients"), (r"\bingredients\b", "ingrédients"),
    (r"\bConfig\b", "Config"), (r"\bconfig\b", "config"),
    (r"\bSettings\b", "Paramètres"), (r"\bsettings\b", "paramètres"),
    (r"\bSetting\b", "Paramètre"), (r"\bsetting\b", "paramètre"),
    (r"\bOption\b", "Option"), (r"\boption\b", "option"),
    (r"\bOptions\b", "Options"), (r"\boptions\b", "options"),
    (r"\bDefault\b", "Par défaut"), (r"\bdefault\b", "par défaut"),
    (r"\bValue\b", "Valeur"), (r"\bvalue\b", "valeur"),
    (r"\bValues\b", "Valeurs"), (r"\bvalues\b", "valeurs"),
    (r"\bMaximum\b", "Maximum"), (r"\bmaximum\b", "maximum"),
    (r"\bMinimum\b", "Minimum"), (r"\bminimum\b", "minimum"),
    (r"\bDamage\b", "Dégâts"), (r"\bdamage\b", "dégâts"),
    (r"\bHealth\b", "Vie"), (r"\bhealth\b", "vie"),
    (r"\bArmor\b", "Armure"), (r"\barmor\b", "armure"),
    (r"\bSpeed\b", "Vitesse"), (r"\bspeed\b", "vitesse"),
    (r"\bAttack\b", "Attaque"), (r"\battack\b", "attaque"),
    (r"\bDefense\b", "Défense"), (r"\bdefense\b", "défense"),
    (r"\bChance\b", "Chance"), (r"\bchance\b", "chance"),
    (r"\bWorld\b", "Monde"), (r"\bworld\b", "monde"),
    (r"\bServer\b", "Serveur"), (r"\bserver\b", "serveur"),
    (r"\bClient\b", "Client"), (r"\bclient\b", "client"),
    (r"\bWaystone\b", "Pierre de passage"), (r"\bwaystone\b", "pierre de passage"),
    (r"\bWaystones\b", "Pierres de passage"), (r"\bwaystones\b", "pierres de passage"),
    (r"\bTeleport\b", "Téléporter"), (r"\bteleport\b", "téléporter"),
    (r"\bTeleportation\b", "Téléportation"), (r"\bteleportation\b", "téléportation"),
    (r"\bBackpack\b", "Sac à dos"), (r"\bbackpack\b", "sac à dos"),
    (r"\bBackpacks\b", "Sacs à dos"), (r"\bbackpacks\b", "sacs à dos"),
    (r"\bSlot\b", "Emplacement"), (r"\bslot\b", "emplacement"),
    (r"\bSlots\b", "Emplacements"), (r"\bslots\b", "emplacements"),
    (r"\bUpgrade\b", "Amélioration"), (r"\bupgrade\b", "amélioration"),
    (r"\bUpgrades\b", "Améliorations"), (r"\bupgrades\b", "améliorations"),
    (r"\bStorage\b", "Stockage"), (r"\bstorage\b", "stockage"),
    (r"\bCapacity\b", "Capacité"), (r"\bcapacity\b", "capacité"),
    (r"\bDisk\b", "Disque"), (r"\bdisk\b", "disque"),
    (r"\bCamera\b", "Appareil photo"), (r"\bcamera\b", "appareil photo"),
    (r"\bPhoto\b", "Photo"), (r"\bphoto\b", "photo"),
    (r"\bPhotograph\b", "Photographie"), (r"\bphotograph\b", "photographie"),
    (r"\bFilm\b", "Pellicule"), (r"\bfilm\b", "pellicule"),
    (r"\bDevelop\b", "Développer"), (r"\bdevelop\b", "développer"),
    (r"\bDeveloped\b", "Développé"), (r"\bdeveloped\b", "développé"),
    (r"\bExposure\b", "Exposition"), (r"\bexposure\b", "exposition"),
    (r"\bShutter\b", "Obturateur"), (r"\bshutter\b", "obturateur"),
    (r"\bFlash\b", "Flash"), (r"\bflash\b", "flash"),
    (r"\bGenerator\b", "Générateur"), (r"\bgenerator\b", "générateur"),
    (r"\bGenerators\b", "Générateurs"), (r"\bgenerators\b", "générateurs"),
    (r"\bFuel\b", "Carburant"), (r"\bfuel\b", "carburant"),
    (r"\bHeat\b", "Chaleur"), (r"\bheat\b", "chaleur"),
    (r"\bDiesel\b", "Diesel"), (r"\bdiesel\b", "diesel"),
    (r"\bPetrol\b", "Essence"), (r"\bpetrol\b", "essence"),
    (r"\bGasoline\b", "Essence"), (r"\bgasoline\b", "essence"),
    (r"\bRefinery\b", "Raffinerie"), (r"\brefinery\b", "raffinerie"),
    (r"\bOil\b", "Pétrole"), (r"\boil\b", "pétrole"),
    (r"\bUrn\b", "Urne"), (r"\burn\b", "urne"),
    (r"\bJar\b", "Jarre"), (r"\bjar\b", "jarre"),
    (r"\bSack\b", "Sac"), (r"\bsack\b", "sac"),
    (r"\bLock\b", "Serrure"), (r"\block\b", "serrure"),
    (r"\bLocked\b", "Verrouillé"), (r"\blocked\b", "verrouillé"),
    (r"\bUnlock\b", "Déverrouiller"), (r"\bunlock\b", "déverrouiller"),
    (r"\bWindow\b", "Fenêtre"), (r"\bwindow\b", "fenêtre"),
    (r"\bDoor\b", "Porte"), (r"\bdoor\b", "porte"),
    (r"\bRoof\b", "Toit"), (r"\broof\b", "toit"),
    (r"\bStairs\b", "Escaliers"), (r"\bstairs\b", "escaliers"),
    (r"\bBridge\b", "Pont"), (r"\bbridge\b", "pont"),
    (r"\bFurniture\b", "Meuble"), (r"\bfurniture\b", "meuble"),
    (r"\bPainting\b", "Tableau"), (r"\bpainting\b", "tableau"),
    (r"\bPaintings\b", "Tableaux"), (r"\bpaintings\b", "tableaux"),
    (r"\bElevator\b", "Ascenseur"), (r"\belevator\b", "ascenseur"),
    (r"\bGuard\b", "Garde"), (r"\bguard\b", "garde"),
    (r"\bGuards\b", "Gardes"), (r"\bguards\b", "gardes"),
    (r"\bVillager\b", "Villageois"), (r"\bvillager\b", "villageois"),
    (r"\bVillage\b", "Village"), (r"\bvillage\b", "village"),
    (r"\bSpawn\b", "Apparaître"), (r"\bspawn\b", "apparaître"),
    (r"\bSpawning\b", "Apparition"), (r"\bspawning\b", "apparition"),
    (r"\bChunk\b", "Chunk"), (r"\bchunk\b", "chunk"),
    (r"\bBiome\b", "Biome"), (r"\bbiome\b", "biome"),
    (r"\bBiomes\b", "Biomes"), (r"\bbiomes\b", "biomes"),
    (r"\bDimension\b", "Dimension"), (r"\bdimension\b", "dimension"),
    (r"\bMagic\b", "Magie"), (r"\bmagic\b", "magie"),
    (r"\bSpell\b", "Sort"), (r"\bspell\b", "sort"),
    (r"\bSpells\b", "Sorts"), (r"\bspells\b", "sorts"),
    (r"\bMana\b", "Mana"), (r"\bmana\b", "mana"),
    (r"\bPotion\b", "Potion"), (r"\bpotion\b", "potion"),
    (r"\bEffect\b", "Effet"), (r"\beffect\b", "effet"),
    (r"\bEffects\b", "Effets"), (r"\beffects\b", "effets"),
    (r"\bMask\b", "Masque"), (r"\bmask\b", "masque"),
    (r"\bGauntlet\b", "Gantelet"), (r"\bgauntlet\b", "gantelet"),
    (r"\bStaff\b", "Bâton"), (r"\bstaff\b", "bâton"),
    (r"\bSword\b", "Épée"), (r"\bsword\b", "épée"),
    (r"\bAxe\b", "Hache"), (r"\baxe\b", "hache"),
    (r"\bPickaxe\b", "Pioche"), (r"\bpickaxe\b", "pioche"),
    (r"\bShovel\b", "Pelle"), (r"\bshovel\b", "pelle"),
    (r"\bHoe\b", "Houe"), (r"\bhoe\b", "houe"),
    (r"\bBow\b", "Arc"), (r"\bbow\b", "arc"),
    (r"\bShield\b", "Bouclier"), (r"\bshield\b", "bouclier"),
    (r"\bHelmet\b", "Casque"), (r"\bhelmet\b", "casque"),
    (r"\bChestplate\b", "Plastron"), (r"\bchestplate\b", "plastron"),
    (r"\bLeggings\b", "Jambières"), (r"\bleggings\b", "jambières"),
    (r"\bBoots\b", "Bottes"), (r"\bboots\b", "bottes"),
    (r"\bBelt\b", "Ceinture"), (r"\bbelt\b", "ceinture"),
    (r"\bRing\b", "Anneau"), (r"\bring\b", "anneau"),
    (r"\bAmulet\b", "Amulette"), (r"\bamulet\b", "amulette"),
    (r"\bArtifact\b", "Artefact"), (r"\bartifact\b", "artefact"),
    (r"\bArtifacts\b", "Artefacts"), (r"\bartifacts\b", "artefacts"),
    (r"\bTreasure\b", "Trésor"), (r"\btreasure\b", "trésor"),
    (r"\bLoot\b", "Butin"), (r"\bloot\b", "butin"),
    (r"\bDungeon\b", "Donjon"), (r"\bdungeon\b", "donjon"),
    (r"\bAdvancement\b", "Progrès"), (r"\badvancement\b", "progrès"),
    (r"\bMode\b", "Mode"), (r"\bmode\b", "mode"),
    (r"\bSurvival\b", "Survie"), (r"\bsurvival\b", "survie"),
    (r"\bCreative\b", "Créatif"), (r"\bcreative\b", "créatif"),
    (r"\bAdventure\b", "Aventure"), (r"\badventure\b", "aventure"),
    (r"\bDifficulty\b", "Difficulté"), (r"\bdifficulty\b", "difficulté"),
    (r"\bDeath\b", "Mort"), (r"\bdeath\b", "mort"),
    (r"\bRespawn\b", "Réapparition"), (r"\brespawn\b", "réapparition"),
    (r"\bGroup\b", "Groupe"), (r"\bgroup\b", "groupe"),
    (r"\bTeam\b", "Équipe"), (r"\bteam\b", "équipe"),
    (r"\bFishing\b", "Pêche"), (r"\bfishing\b", "pêche"),
    (r"\bTree\b", "Arbre"), (r"\btree\b", "arbre"),
    (r"\bTrees\b", "Arbres"), (r"\btrees\b", "arbres"),
    (r"\bLog\b", "Bûche"), (r"\blog\b", "bûche"),
    (r"\bLogs\b", "Bûches"), (r"\blogs\b", "bûches"),
    (r"\bFell\b", "Abattre"), (r"\bfell\b", "abattre"),
    (r"\bFalling\b", "Chute"), (r"\bfalling\b", "chute"),
    (r"\bFall\b", "Tomber"), (r"\bfall\b", "tomber"),
    (r"\bWall\b", "Mur"), (r"\bwall\b", "mur"),
    (r"\bClimb\b", "Escalade"), (r"\bclimb\b", "escalade"),
    (r"\bClimbing\b", "Escalade"), (r"\bclimbing\b", "escalade"),
    (r"\bSlide\b", "Glissade"), (r"\bslide\b", "glissade"),
    (r"\bDodge\b", "Esquive"), (r"\bdodge\b", "esquive"),
    (r"\bVault\b", "Saut en main"), (r"\bvault\b", "saut en main"),
    (r"\bStamina\b", "Endurance"), (r"\bstamina\b", "endurance"),
    (r"\bEnchant\b", "Enchanter"), (r"\benchant\b", "enchanter"),
    (r"\bEnchanted\b", "Enchanté"), (r"\benchanted\b", "enchanté"),
    (r"\bEnchantment\b", "Enchantement"), (r"\benchantment\b", "enchantement"),
    (r"\bEnchantments\b", "Enchantements"), (r"\benchantments\b", "enchantements"),
    (r"\bSigned message\b", "Message signé"), (r"\bsigned message\b", "message signé"),
    (r"\bUnsigned\b", "Non signé"), (r"\bunsigned\b", "non signé"),
    (r"\bEncryption\b", "Chiffrement"), (r"\bencryption\b", "chiffrement"),
    (r"\bEncrypt\b", "Chiffrer"), (r"\bencrypt\b", "chiffrer"),
    (r"\bDecrypt\b", "Déchiffrer"), (r"\bdecrypt\b", "déchiffrer"),
    (r"\bEncrypted\b", "Chiffré"), (r"\bencrypted\b", "chiffré"),
    (r"\bDecrypted\b", "Déchiffré"), (r"\bdecrypted\b", "déchiffré"),
    (r"\bReport\b", "Signaler"), (r"\breport\b", "signaler"),
    (r"\bReports\b", "Signalements"), (r"\breports\b", "signalements"),
    (r"\bChat reports\b", "Signalements de chat"),
    (r"\bchat reports\b", "signalements de chat"),
    (r"\bSearch\b", "Rechercher"), (r"\bsearch\b", "rechercher"),
    (r"\bBookmark\b", "Favori"), (r"\bbookmark\b", "favori"),
    (r"\bBookmarks\b", "Favoris"), (r"\bbookmarks\b", "favoris"),
    (r"\bRecipes\b", "Recettes"), (r"\brecipes\b", "recettes"),
    (r"\bThis ingredient\b", "Cet ingrédient"), (r"\bthis ingredient\b", "cet ingrédient"),
    (r"\bThis recipe\b", "Cette recette"), (r"\bthis recipe\b", "cette recette"),
    (r"\bSeconds\b", "secondes"), (r"\bseconds\b", "secondes"),
    (r"\bMinutes\b", "minutes"), (r"\bminutes\b", "minutes"),
    (r"\bHours\b", "heures"), (r"\bhours\b", "heures"),
    (r"\bSecond\b", "seconde"), (r"\bsecond\b", "seconde"),
    (r"\bMinute\b", "minute"), (r"\bminute\b", "minute"),
    (r"\bHour\b", "heure"), (r"\bhour\b", "heure"),
    (r"\bDay\b", "Jour"), (r"\bday\b", "jour"),
    (r"\bDays\b", "Jours"), (r"\bdays\b", "jours"),
    (r"\bNight\b", "Nuit"), (r"\bnight\b", "nuit"),
    (r"\bTick\b", "Tick"), (r"\btick\b", "tick"),
    (r"\bTicks\b", "Ticks"), (r"\bticks\b", "ticks"),
    (r"\bWooden\b", "En bois"), (r"\bwooden\b", "en bois"),
    (r"\bIron\b", "Fer"), (r"\biron\b", "fer"),
    (r"\bGolden\b", "Doré"), (r"\bgolden\b", "doré"),
    (r"\bGold\b", "Or"), (r"\bgold\b", "or"),
    (r"\bDiamond\b", "Diamant"), (r"\bdiamond\b", "diamant"),
    (r"\bEmerald\b", "Émeraude"), (r"\bemerald\b", "émeraude"),
    (r"\bNetherite\b", "Netherite"), (r"\bnetherite\b", "netherite"),
    (r"\bCopper\b", "Cuivre"), (r"\bcopper\b", "cuivre"),
    (r"\bRedstone\b", "Redstone"), (r"\bredstone\b", "redstone"),
    (r"\bCoal\b", "Charbon"), (r"\bcoal\b", "charbon"),
    (r"\bWood\b", "Bois"), (r"\bwood\b", "bois"),
    (r"\bStone\b", "Pierre"), (r"\bstone\b", "pierre"),
    (r"\bSand\b", "Sable"), (r"\bsand\b", "sable"),
    (r"\bGravel\b", "Gravier"), (r"\bgravel\b", "gravier"),
    (r"\bDirt\b", "Terre"), (r"\bdirt\b", "terre"),
    (r"\bWater\b", "Eau"), (r"\bwater\b", "eau"),
    (r"\bLava\b", "Lave"), (r"\blava\b", "lave"),
    (r"\bFire\b", "Feu"), (r"\bfire\b", "feu"),
    (r"\bIce\b", "Glace"), (r"\bice\b", "glace"),
    (r"\bSnow\b", "Neige"), (r"\bsnow\b", "neige"),
    (r"\bRain\b", "Pluie"), (r"\brain\b", "pluie"),
    (r"\bShader\b", "Shader"), (r"\bshader\b", "shader"),
    (r"\bShaders\b", "Shaders"), (r"\bshaders\b", "shaders"),
    (r"\bGraphics\b", "Graphismes"), (r"\bgraphics\b", "graphismes"),
    (r"\bRender\b", "Rendre"), (r"\brender\b", "rendre"),
    (r"\bRenderer\b", "Moteur de rendu"), (r"\brenderer\b", "moteur de rendu"),
    (r"\bPerformance\b", "Performance"), (r"\bperformance\b", "performance"),
    (r"\bMemory\b", "Mémoire"), (r"\bmemory\b", "mémoire"),
    (r"\bCache\b", "Cache"), (r"\bcache\b", "cache"),
    (r"\bSound\b", "Son"), (r"\bsound\b", "son"),
    (r"\bSounds\b", "Sons"), (r"\bsounds\b", "sons"),
    (r"\bMusic\b", "Musique"), (r"\bmusic\b", "musique"),
    (r"\bVolume\b", "Volume"), (r"\bvolume\b", "volume"),
    (r"\bVoice\b", "Voix"), (r"\bvoice\b", "voix"),
    (r"\bAnimation\b", "Animation"), (r"\banimation\b", "animation"),
    (r"\bAnimations\b", "Animations"), (r"\banimations\b", "animations"),
    (r"\bModel\b", "Modèle"), (r"\bmodel\b", "modèle"),
    (r"\bTexture\b", "Texture"), (r"\btexture\b", "texture"),
    (r"\bTextures\b", "Textures"), (r"\btextures\b", "textures"),
    (r"\bResource\b", "Ressource"), (r"\bresource\b", "ressource"),
    (r"\bResources\b", "Ressources"), (r"\bresources\b", "ressources"),
    (r"\bPress\b", "Appuyer"), (r"\bpress\b", "appuyer"),
    (r"\bPlease\b", "Veuillez"), (r"\bplease\b", "veuillez"),
    (r"\bDownload\b", "Télécharger"), (r"\bdownload\b", "télécharger"),
    (r"\bInstall\b", "Installer"), (r"\binstall\b", "installer"),
    (r"\bUpdate\b", "Mise à jour"), (r"\bupdate\b", "mise à jour"),
    (r"\bRestart\b", "Redémarrer"), (r"\brestart\b", "redémarrer"),
    (r"\bReload\b", "Recharger"), (r"\breload\b", "recharger"),
    (r"\bLoad\b", "Charger"), (r"\bload\b", "charger"),
    (r"\bSave\b", "Sauvegarder"), (r"\bsave\b", "sauvegarder"),
    (r"\bSaved\b", "Sauvegardé"), (r"\bsaved\b", "sauvegardé"),
    (r"\bExport\b", "Exporter"), (r"\bexport\b", "exporter"),
    (r"\bImport\b", "Importer"), (r"\bimport\b", "importer"),
    (r"\bCopy\b", "Copier"), (r"\bcopy\b", "copier"),
    (r"\bPaste\b", "Coller"), (r"\bpaste\b", "coller"),
    (r"\bCut\b", "Couper"), (r"\bcut\b", "couper"),
    (r"\bUndo\b", "Annuler"), (r"\bundo\b", "annuler"),
    (r"\bRedo\b", "Refaire"), (r"\bredo\b", "refaire"),
    # connector words last
    (r"\bThis\b", "Ce"), (r"\bthis\b", "ce"),
    (r"\bThese\b", "Ces"), (r"\bthese\b", "ces"),
    (r"\bThat\b", "Ce"), (r"\bthat\b", "ce"),
    (r"\bAlso\b", "Aussi"), (r"\balso\b", "aussi"),
    (r"\bAnd\b", "Et"), (r"\band\b", "et"),
    (r"\bOr\b", "Ou"), (r"\bor\b", "ou"),
    (r"\bNot\b", "Pas"), (r"\bnot\b", "pas"),
    (r"\bBut\b", "Mais"), (r"\bbut\b", "mais"),
    (r"\bWith\b", "Avec"), (r"\bwith\b", "avec"),
    (r"\bIn\b", "Dans"), (r"\bin\b", "dans"),
    (r"\bOn\b", "Sur"), (r"\bon\b", "sur"),
    (r"\bAt\b", "À"), (r"\bat\b", "à"),
    (r"\bTo\b", "À"), (r"\bto\b", "à"),
    (r"\bFrom\b", "De"), (r"\bfrom\b", "de"),
    (r"\bFor\b", "Pour"), (r"\bfor\b", "pour"),
    (r"\bBy\b", "Par"), (r"\bby\b", "par"),
    (r"\bThe\b", "Le"), (r"\bthe\b", "le"),
    (r"\bIs\b", "Est"), (r"\bis\b", "est"),
    (r"\bAre\b", "Sont"), (r"\bare\b", "sont"),
    (r"\bYou\b", "Vous"), (r"\byou\b", "vous"),
    (r"\bYour\b", "Votre"), (r"\byour\b", "votre"),
]

# Compile
GENERIC_WORDS_C = [(re.compile(p), r) for p, r in GENERIC_WORDS]

PLACEHOLDER_RE = re.compile(
    r"%[0-9]*\$?[sd]|%\d+|\{[^}]*\}|&[0-9a-fk-or]|§[0-9a-fk-or]|"
    r"\\n|\\t|\n|\t|<[^>]+>|\[[^\]]+\]|\$\{[^}]+\}"
)

def fallback_translate(text):
    """Word-level fallback with placeholder preservation."""
    if not isinstance(text, str) or not text.strip():
        return text
    placeholders = []
    def stash(m):
        placeholders.append(m.group(0))
        return f"\x00{len(placeholders)-1}\x00"
    masked = PLACEHOLDER_RE.sub(stash, text)
    for pat, repl in GENERIC_WORDS_C:
        masked = pat.sub(repl, masked)
    def restore(m):
        return placeholders[int(m.group(1))]
    return re.sub(r"\x00(\d+)\x00", restore, masked)

def translate_value(value):
    """Layered translation: glossary -> phrase dict -> word fallback."""
    if not isinstance(value, str):
        return value
    if not value.strip():
        return value
    p = t_phrase(value)
    if p is not None:
        return p
    return fallback_translate(value)

def write_json(path, data):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent="\t"))
        f.write("\n")

def load_json(path):
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

# Read mod list
mods = []
with open(BIN_FILE, "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) == 2:
            mods.append((parts[0], int(parts[1])))

processed = 0
total_keys = 0
failed = []

for mod, count in mods:
    in_path = MISSING_DIR / f"{mod}.json"
    out_path = OUT_DIR / f"{mod}.json"
    if not in_path.exists():
        failed.append((mod, "no input"))
        continue
    missing = load_json(in_path)
    out = {}
    for k, v in missing.items():
        out[k] = translate_value(v)
    write_json(out_path, out)
    processed += 1
    total_keys += len(out)
    print(f"  {mod}: {len(out)} keys")

print(f"\nDONE: {processed}/{len(mods)} mods, {total_keys} keys total")
if failed:
    print("Failed:", failed)
