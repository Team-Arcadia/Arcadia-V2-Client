#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Translate FTB Quests phase2 keys from English to French.

Input:  translation_workspace/ftbq_audit/phase2_to_translate_fr_fr.json
Output: translation_workspace/ftbq_audit/phase2_output/fr_fr.json
"""

from __future__ import annotations
import json
import os
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
IN_PATH = HERE / "phase2_to_translate_fr_fr.json"
OUT_DIR = HERE / "phase2_output"
OUT_PATH = OUT_DIR / "fr_fr.json"


# ---------------------------------------------------------------------------
# Hardcoded full-string translations (highest priority).
# Keys are EXACT source strings. Values are the French translation.
# ---------------------------------------------------------------------------
FULL: dict[str, str] = {
    # generic UI / common
    "": "",
    "Guide": "Guide",
    "Addon": "Addon",
    "Exchange?": "Échanger ?",
    "Filters": "Filtres",
    "Filtres": "Filtres",
    "Funnels": "Entonnoirs",
    "Entonnoirs": "Entonnoirs",
    "Tuyau": "Tuyau",
    "Tuyau intelligent": "Tuyau intelligent",
    "Pompe": "Pompe",
    "Piston": "Piston",
    "Presse": "Presse",
    "Bassin": "Bassin",
    "Basin": "Bassin",
    "Valve": "Valve",
    "Vase": "Vase",
    "Conduit": "Conduit",
    "Embrayage": "Embrayage",
    "Inverseur": "Inverseur",
    "Manivelle": "Manivelle",
    "Charrue": "Charrue",
    "Catapulte": "Catapulte",
    "Sifflet": "Sifflet",
    "Foreuse": "Foreuse",
    "Scie": "Scie",
    "Meule": "Meule",
    "Ventilateur": "Ventilateur",
    "Ticket": "Ticket",
    "Drone": "Drone",
    "Terminal": "Terminal",
    "Hypertube": "Hypertube",
    "Tunnels": "Tunnels",
    "Gearshift": "Boîte de vitesse",
    "Flywheel": "Volant d'inertie",
    "Volant d'inertie": "Volant d'inertie",
    "Autocrafter": "Auto-Fabricateur",
    "Copycat": "Copycat",
    "Gyrodyne": "Gyrodyne",
    "Slider": "Slider",
    "Valkyrie": "Valkyrie",
    "Potion": "Potion",
    "Quartz": "Quartz",
    "Rails": "Rails",
    "Redstone": "Redstone",
    "Redstone sans fil": "Redstone sans fil",
    "Conducteur": "Conducteur",
    "Horaires": "Horaires",
    "Gare": "Gare",
    "Gants de Combat": "Gants de Combat",
    "Outils Indispensables": "Outils Indispensables",
    "Coffre fort": "Coffre fort",
    "Compteur de Vitesse": "Compteur de Vitesse",
    "Mesureur de Stress": "Mesureur de Stress",
    "Marcheur de Nuages": "Marcheur de Nuages",
    "Rouleau compresseur": "Rouleau compresseur",
    "Bec verseur": "Bec verseur",
    "Courroie/Tapis": "Courroie/Tapis",
    "Panneaux d'affichage": "Panneaux d'affichage",
    "Tubes d'affichage": "Tubes d'affichage",
    "Vitesse variable": "Vitesse variable",
    "Voir les stats.": "Voir les stats.",
    "Polissage manuel.": "Polissage manuel.",
    "Modifier les blocs.": "Modifier les blocs.",
    "Lavage/Cuisson.": "Lavage/Cuisson.",
    "Glues blocks together.": "Colle les blocs ensemble.",
    "Grinds ores.": "Broie les minerais.",
    "Broie les minerais.": "Broie les minerais.",
    "Nouveau minerai.": "Nouveau minerai.",
    "Carburant ultime": "Carburant ultime",
    "Farine du Nether": "Farine du Nether",
    "Permet d'extraire des liquides d'objets.": "Permet d'extraire des liquides d'objets.",
    "Construisez un cadre en Glowstone et versez de l'eau.": "Construisez un cadre en Glowstone et versez de l'eau.",
    "Capturer un Blaze": "Capturer un Blaze",
    "Assemblage du Train": "Assemblage du Train",
    "Automatisation Ferroviaire": "Automatisation Ferroviaire",
    "La Vapeur": "La Vapeur",
    "Moteur Vapeur": "Moteur Vapeur",
    "Tchou Tchou !": "Tchou Tchou !",
    "L'assemblage complexe": "L'assemblage complexe",
    "Le Gardien Aveugle": "Le Gardien Aveugle",
    "Le Seuil Interdit": "Le Seuil Interdit",
    "L'Appel des Profondeurs": "L'Appel des Profondeurs",
    "L'Archimage Absolu": "L'Archimage Absolu",
    "L'Ascension": "L'Ascension",
    "Les Boss": "Les Boss",
    "Ressource Sombre": "Ressource Sombre",
    "Silence de Mort": "Silence de Mort",
    "Roues de Broyage - Endgame": "Roues de Broyage - Endgame",
    "Forteresse d'Or": "Forteresse d'Or",
    "Temple d'Argent": "Temple d'Argent",
    "Ne te laisse pas emporter": "Ne te laisse pas emporter",
    "Je te surveille.": "Je te surveille.",
    "Puissance de Gravitite": "Puissance de Gravitite",
    "Panoplie de Zanite": "Panoplie de Zanite",
    "Gastronomie de l'Aether": "Gastronomie de l'Aether",
    "Arts Interdits (Ocultas)": "Arts Interdits (Ocultas)",
    "Poissons de l'oc00e9an arctique": "Poissons de l'océan arctique",
    "Arbre": "Arbre",
    # commands - keep as-is
    "/back": "/back",
    "/ftbchunks claim": "/ftbchunks claim",
    "/ftbchunks claim-radius": "/ftbchunks claim-radius",
    "/ftbchunks info": "/ftbchunks info",
    "/ftbchunks unclaim": "/ftbchunks unclaim",
    "/home": "/home",
    "/sethome": "/sethome",
    "/spawn": "/spawn",
    "/tpa": "/tpa",
    "/tpaccept": "/tpaccept",
    "/tpahere": "/tpahere",
    "/tpdeny": "/tpdeny",
    # identifiers / tags / mod IDs
    "Any #minecraft:logs": "Toute bûche #minecraft:logs",
    "Any #waystones:sharestones": "Toute sharestone #waystones:sharestones",
    "Any #waystones:waystones": "Toute waystone #waystones:waystones",
    "Any seat": "N'importe quel siège",
    "sliceanddice:slicer": "sliceanddice:slicer",
    "sliceanddice:sprinkler": "sliceanddice:sprinkler",
    # mods
    "Aquaculture": "Aquaculture",
    "Applied Energistics": "Applied Energistics",
    "Ars Nouveau": "Ars Nouveau",
    "Artifacts": "Artifacts",
    "Chipped": "Chipped",
    "Create": "Create",
    "Create I": "Create I",
    "Create II": "Create II",
    "Create III": "Create III",
    "Create IV": "Create IV",
    "Create V": "Create V",
    "Mekanism": "Mekanism",
    "Mowzie's Mobs": "Mowzie's Mobs",
    "Simply Swords": "Simply Swords",
    "Sophisticated": "Sophisticated",
    "Just Enough Items (JEI)": "Just Enough Items (JEI)",
    # chapter group sections
    "Beginning": "Débutant",
    "Advanced": "Avancé",
    "Expert": "Expert",
    "Experimental": "Expérimental",
    "Learning": "Apprentissage",
    "Progression": "Progression",
    "Nearly impossible": "Presque impossible",
    "Absolute perfection": "Perfection absolue",
    "Automation": "Automatisation",
    "Automated Collection": "Collecte automatisée",
    "Transmission": "Transmission",
    # mob / entity names
    "Creeper": "Creeper",
    "Zombie": "Zombie",
    "Enderman": "Enderman",
    "Ender Dragon": "Ender Dragon",
    "Warden": "Warden",
    "Wither": "Wither",
    "Flooder Creeper": "Creeper Inondateur",
    "Bastion Raider": "Pillard de Bastion",
    "Bastion Remnant": "Vestige de Bastion",
    "Humanoid Target": "Cible humanoïde",
    "Human Form": "Forme Humaine",
    "Grenadier Form": "Forme de Grenadier",
    "Swamp Fish": "Poisson des Marais",
    "Enderskog": "Enderskog",
    "Fungal Woods": "Bois Fongique",
    "Basalt Deltas": "Deltas de Basalte",
    "Hell's Gate": "Porte de l'Enfer",
    "Spooky Scary Skeletons": "Squelettes Effrayants",
    "Hold [W] My Brothers, Hold!": "Tiens [W] mes frères, tiens !",
    "Hostile Paradise": "Paradis Hostile",
    "Homestead Utility": "Utilitaire de Ferme",
    "Hearty Stews": "Ragoûts Copieux",
    "Cooking Equipment": "Équipement de Cuisine",
    "Gourmet Specialties": "Spécialités Gourmandes",
    "Banquets and Feasts": "Banquets et Festins",
    "The Bakery": "La Boulangerie",
    "The Pastry Chef": "Le Pâtissier",
    "Textile Crafting": "Travail du Textile",
    "Mechanical Farming": "Agriculture Mécanique",
    "Bronze Dungeon: The Slider": "Donjon de Bronze : Le Slider",
    "Don't hit it with a sword!": "Ne le frappe pas avec une épée !",
    "Hot Stuff": "Chaud Devant",
    "Inserting fuel ": "Insertion du carburant ",
    "Generating heat": "Génération de chaleur",
    "Generating thorium": "Génération de thorium",
    "Finally, nuclear": "Enfin, le nucléaire",
    "Basically electricity = speed": "En gros, électricité = vitesse",
    "Few most abudant ores...": "Quelques-uns des minerais les plus abondants...",
    "Get any non-dirty minerals dusts": "Obtenir n'importe quelle poussière de minerai propre",
    "High Carbon Density": "Forte densité de carbone",
    "Extinguished": "Éteint",
    "Fireproof": "Ignifuge",
    "Flashy": "Tape-à-l'œil",
    "Fan Nozzle": "Buse de Ventilateur",
    "Fluid Pipe": "Tuyau à Fluides",
    "Fluid Tank": "Réservoir à Fluides",
    "Fluid Valve": "Valve à Fluides",
    "Fireclay Furnace": "Four en Argile Réfractaire",
    "Graphite Molds": "Moules en Graphite",
    "Gray Paste": "Pâte Grise",
    "Gilded Blackstone": "Pierre Noire Dorée",
    "Hidden Debris": "Débris Cachés",
    "Crafters - Endgame": "Crafteurs - Endgame",
    "Baby Food": "Nourriture pour Bébé",
    "Bitterballen": "Bitterballen",
    "Armadillo Scute": "Écaille de Tatou",
    "Fluorite Gem": "Gemme de Fluorite",
    "Experience Bottle": "Fiole d'Expérience",
    "Epic Material": "Matériau Épique",
    "Exotic Hardware": "Matériel Exotique",
    "Basic crafting material.": "Matériau de base pour la fabrication.",
    "Gemcraft mastery.": "Maîtrise de la gemmerie.",
    "Arcane scholarship.": "Érudition arcanique.",
    "Grid access.": "Accès à la grille.",
    "Worm Farm": "Élevage de Vers",
    "Tackle Box": "Boîte de Pêche",
    "Iron Fishing Rod": "Canne à Pêche en Fer",
    "Gold Fishing Rod": "Canne à Pêche en Or",
    "Diamond Fishing Rod": "Canne à Pêche en Diamant",
    "Neptunium Helmet": "Casque en Neptunium",
    "Neptunium Chestplate": "Plastron en Neptunium",
    "Master of the rod.": "Maître de la canne.",
    "Aquatic treasures.": "Trésors aquatiques.",
    "The deep awaits.": "Les profondeurs t'attendent.",
    "Discover every Otherside biome.": "Découvre tous les biomes de l'Otherside.",
    "Loot a forgotten Otherside ruin.": "Pille une ruine oubliée de l'Otherside.",
    "Spend real time inside the Otherside.": "Passe du temps réel à l'intérieur de l'Otherside.",
    "Step through the gateway beyond the Deep Dark.": "Franchis le portail au-delà du Deep Dark.",
    "bauxite :o": "bauxite :o",
    "rail": "rail",
    # runes / glyphs (Apothic / Ars Nouveau)
    "Fire Rune": "Rune de Feu",
    "Holy Rune": "Rune Sacrée",
    "Evocation Rune": "Rune d'Évocation",
    # Iron's Spellbooks weapons (proper nouns kept)
    "&3Sonorous Staff": "&3Sonorous Staff",
    # Weapon proper names from Simply Swords / mods
    "&6Caelestis": "&6Caelestis",
    "&6Chompolotl": "&6Chompolotl",
    "&6Emberlash": "&6Emberlash",
    "&6Enigma": "&6Enigma",
    "&6Flamewind": "&6Flamewind",
    "&6Frostfall": "&6Frostfall",
    "&6Harbinger": "&6Harbinger",
    "&6Hearthflame": "&6Hearthflame",
    "&6Hiveheart": "&6Hiveheart",
    "&6Icewhisper": "&6Icewhisper",
    "&6Livyatan": "&6Livyatan",
    "&6Magiblade": "&6Magiblade",
    "&6Magiscythe": "&6Magiscythe",
    "&6Magispear": "&6Magispear",
    "&6Mjolnir": "&6Mjolnir",
    "&6Ribboncleaver": "&6Ribboncleaver",
    "&6Righteous Relic": "&6Righteous Relic",
    "&6Runic Grimoire": "&6Runic Grimoire",
    "&6Shadowsting": "&6Shadowsting",
    "&6Stars Edge": "&6Stars Edge",
    "&6Storms Edge": "&6Storms Edge",
    "&6Stormbringer": "&6Stormbringer",
    "&6Sunfire": "&6Sunfire",
    "&6Tainted Relic": "&6Tainted Relic",
    "&6Tempest": "&6Tempest",
    "&6Thunderbrand": "&6Thunderbrand",
    "&6Toxic Longsword": "&6Toxic Longsword",
    "&6Twisted Blade": "&6Twisted Blade",
    "&6Waxweaver": "&6Waxweaver",
    "&6Whisperwind": "&6Whisperwind",
    "&6Wickpiercer": "&6Wickpiercer",
    "&6Wraithfang": "&6Wraithfang",
    "Chompolotl": "Chompolotl",
    # untranslated headers / coloured proper nouns
    "&2Inventory": "&2Inventaire",
    "&9Runefused Gem": "&9Gemme Runefusée",
    "&dAncient Structure": "&dStructure Antique",
    "&bEaster Egg!": "&bEaster Egg !",
    "&bJust Enough Items (JEI)": "&bJust Enough Items (JEI)",
    "&b&oHostile  Paradise ": "&b&oParadis Hostile ",
    # hunter categories (kept names)
    "&3Hunter: Drowned&r": "&3Chasseur : Noyé&r",
    "&3Hunter: Drowned Elite&r": "&3Chasseur : Noyé Élite&r",
    "&6Hunter: Umvuthana&r": "&6Chasseur : Umvuthana&r",
    "&5Hunter: Troll&r": "&5Chasseur : Troll&r",
    "&fHunter: Ghast&r": "&fChasseur : Ghast&r",
    # chapter group descriptions / short labels (already-French ones kept)
    # ------------------------------------------------------------------
    # Ars Nouveau chapter banners (already partially translated in source)
    "§dBienvenue dans l'Arcane§r": "§dBienvenue dans l'Arcane§r",
    "§7Les premiers pas du mage§r": "§7Les premiers pas du mage§r",
    "§6Votre Premier Sort§r": "§6Votre Premier Sort§r",
    "§6Premiers Glyphes§r": "§6Premiers Glyphes§r",
    "§eLa Source de Magie§r": "§eLa Source de Magie§r",
    "§6La Table du Scribe§r": "§6La Table du Scribe§r",
    "§aL'Enchantement Arcanique§r": "§aL'Enchantement Arcanique§r",
    "§5Les Familiers Magiques§r": "§5Les Familiers Magiques§r",
    "§7Invoquer des compagnons arcaniques§r": "§7Invoquer des compagnons arcaniques§r",
    "§4Les Wilden Hostiles§r": "§4Les Wilden Hostiles§r",
    "§3L'Armure du Mage§r": "§3L'Armure du Mage§r",
    "§3L'Armure de l'Archimage§r": "§3L'Armure de l'Archimage§r",
    "§7Protection et puissance arcanique§r": "§7Protection et puissance arcanique§r",
    "§7Protection et puissance magiques ultimes§r": "§7Protection et puissance magiques ultimes§r",
    "§6Automation Arcanique§r": "§6Automation Arcanique§r",
    "§6Automation Arcanique Totale§r": "§6Automation Arcanique Totale§r",
    "§dLe Rituel Arcanique§r": "§dLe Rituel Arcanique§r",
    "§dLes Rituels Arcaniques§r": "§dLes Rituels Arcaniques§r",
    "§7Ascension vers l'Archimage§r": "§7Ascension vers l'Archimage§r",
    "§9Ars Ocultas : Magie Sombre§r": "§9Ars Ocultas : Magie Sombre§r",
    "§9Fusion Technomagique§r": "§9Fusion Technomagique§r",
    "§7Dominer Ars Ocultas§r": "§7Dominer Ars Ocultas§r",
    "§bArs Addition : Extensions Puissantes§r": "§bArs Addition : Extensions Puissantes§r",
    "§cGrand Chef Magique§r": "§cGrand Chef Magique§r",
    "§5§lLa perfection absolue§r": "§5§lLa perfection absolue§r",
    # English aquaculture / otherside banners (use replacement char)
    "§7Cast your line§r": "§7Lance ta ligne§r",
    "§7Reel in the big one§r": "§7Remonte le gros§r",
    "§7Gone fishing!§r": "§7Parti à la pêche !§r",
    "§7Aquatic treasures§r": "§7Trésors aquatiques§r",
    "§7The deep awaits§r": "§7Les profondeurs t'attendent§r",
    # Aquaculture descriptive lines
    "§bWorm Farm§r — Aquaculture brings fishing to life with new rods, tackle, and a bounty of unique fish to catch!":
        "§bÉlevage de Vers§r — Aquaculture redonne vie à la pêche avec de nouvelles cannes, du matériel et une abondance de poissons uniques à attraper !",
    "§bNeptunium Helmet§r — Aquaculture brings fishing to life with new rods, tackle, and a bounty of unique fish to catch!":
        "§bCasque en Neptunium§r — Aquaculture redonne vie à la pêche avec de nouvelles cannes, du matériel et une abondance de poissons uniques à attraper !",
    "§bNeptunium Chestplate§r — Aquaculture brings fishing to life with new rods, tackle, and a bounty of unique fish to catch!":
        "§bPlastron en Neptunium§r — Aquaculture redonne vie à la pêche avec de nouvelles cannes, du matériel et une abondance de poissons uniques à attraper !",
    "§bIron Fishing Rod§r — From arctic waters to tropical seas — every body of water hides something special.":
        "§bCanne à Pêche en Fer§r — Des eaux arctiques aux mers tropicales — chaque étendue d'eau cache quelque chose de spécial.",
    "§bBox Turtle§r — From arctic waters to tropical seas — every body of water hides something special.":
        "§bTortue-Boîte§r — Des eaux arctiques aux mers tropicales — chaque étendue d'eau cache quelque chose de spécial.",
    "§bDiamond Fishing Rod§r — The waters hold countless treasures. Upgrade your fishing gear and explore every biome's aquatic life.":
        "§bCanne à Pêche en Diamant§r — Les eaux recèlent d'innombrables trésors. Améliore ton équipement de pêche et explore la vie aquatique de chaque biome.",
    "§bGold Fishing Rod§r — The waters hold countless treasures. Upgrade your fishing gear and explore every biome's aquatic life.":
        "§bCanne à Pêche en Or§r — Les eaux recèlent d'innombrables trésors. Améliore ton équipement de pêche et explore la vie aquatique de chaque biome.",
    "§bTackle Box§r — The waters hold countless treasures. Upgrade your fishing gear and explore every biome's aquatic life.":
        "§bBoîte de Pêche§r — Les eaux recèlent d'innombrables trésors. Améliore ton équipement de pêche et explore la vie aquatique de chaque biome.",
    # Otherside descriptions
    "&5Enter the Otherside": "&5Entrer dans l'Otherside",
    "&5Otherside Survivor": "&5Survivant de l'Otherside",
    "&3Biomes of the Deep": "&3Biomes des Profondeurs",
    "&7Activate a portal made of &3Reinforced Echo Shards&7 and step into the &5Otherside&7 dimension.":
        "&7Active un portail fait de &3Fragments d'Écho Renforcés&7 et entre dans la dimension &5Otherside&7.",
    "&7This twisted realm is a corrupted End — floating sculk islands, glowing geodes and ancient ruins, all watched over by the &cWarden's&7 echo.":
        "&7Ce royaume tordu est un End corrompu — îles flottantes de sculk, géodes luminescentes et ruines antiques, le tout surveillé par l'écho du &cWarden&7.",
    "&cWarning:&r Once you enter, &dShriekers&7 will activate faster. Carry &fWool boots&7 and never sprint.":
        "&cAttention :&r Une fois entré, les &dShriekers&7 s'activeront plus vite. Porte des &fbottes en laine&7 et ne sprinte jamais.",
    "&7Prove you can live and breathe in the &5Otherside&7 — not just visit it.":
        "&7Prouve que tu peux vivre et respirer dans l'&5Otherside&7 — pas seulement le visiter.",
    "&7Set up a safe base, source food (sculk-tainted mobs drop edible meat), and farm &3Echo&7 and &3Sculk Crystals&7 for endgame gear.":
        "&7Établis une base sûre, trouve de la nourriture (les mobs corrompus par le sculk lâchent de la viande comestible) et farme l'&3Écho&7 et les &3Cristaux de Sculk&7 pour l'équipement de fin de jeu.",
    "&eTip:&r &dWarden Heart&7 grows here — protect it from despawning to harvest the &8Soul Elytra&7.":
        "&eAstuce :&r Le &dCœur de Warden&7 pousse ici — protège-le de la disparition pour récolter l'&8Élytre des Âmes&7.",
    "&7The &5Otherside&7 hides four distinct biomes — find them all to map the dimension.":
        "&7L'&5Otherside&7 cache quatre biomes distincts — trouve-les tous pour cartographier la dimension.",
    "&7Explore the &3Echoing Forest&7, the &8Blooming Caverns&7, the &5Otherside Vegetation&7 fields and the &fOvergrown Caverns&7. Each biome has unique flora, mobs and resources.":
        "&7Explore la &3Forêt Échoïque&7, les &8Cavernes Fleuries&7, les champs de &5Végétation de l'Otherside&7 et les &fCavernes Envahies&7. Chaque biome possède une flore, des mobs et des ressources uniques.",
    "&eTip:&r Use a &6Compass of the Lost&7 to ping nearby unexplored biomes.":
        "&eAstuce :&r Utilise une &6Boussole des Perdus&7 pour repérer les biomes inexplorés à proximité.",
    "&7Track down an &dAncient City Outpost&7 or &dOtherside Temple&7 hidden in the dimension.":
        "&7Localise un &dAvant-poste de Cité Antique&7 ou un &dTemple de l'Otherside&7 caché dans la dimension.",
    "&7These structures hold &6Echo Chests&7 with sculk-themed loot: &dSculk Catalyst Cores&7, ancient music discs and pre-enchanted Soul Tools.":
        "&7Ces structures contiennent des &6Coffres d'Écho&7 au butin thématique sculk : &dNoyaux de Catalyseur de Sculk&7, disques de musique antiques et Outils d'Âme pré-enchantés.",
    "&cWarning:&r Most structures spawn &dShriekers&7 — break them with &eSilk Touch&7 before scavenging.":
        "&cAttention :&r La plupart des structures font apparaître des &dShriekers&7 — casse-les avec &eToucher de Soie&7 avant de fouiller.",
    # Channel / Warden sword
    "&7Channel the &1Warden&7's scream.": "&7Canalise le cri du &1Warden&7.",
    "&7A fearsome weapon forged from the Heart and Souls to repel your enemies.":
        "&7Une arme redoutable forgée à partir du Cœur et des Âmes pour repousser tes ennemis.",
    # Bounty hunt quest_desc lines
    "&7Cleanse the depths.&r": "&7Purifie les profondeurs.&r",
    "&aBounty&r: Slay &eDrowned&r in rivers, oceans and ruined portals.":
        "&aPrime&r : Tue les &eNoyés&r dans les rivières, océans et portails en ruine.",
    "Drops include &fRotten Flesh&r, &bNautilus Shells&r and rarely &eTridents&r.":
        "Butin : &fChair Putréfiée&r, &bCoquillages Nautiles&r et plus rarement &eTridents&r.",
    "&6Reward&r: &b100 XP&r.": "&6Récompense&r : &b100 XP&r.",
    "&6Reward&r: &b700 XP&r.": "&6Récompense&r : &b700 XP&r.",
    "&6Reward&r: &b800 XP&r.": "&6Récompense&r : &b800 XP&r.",
    "&6Reward&r: &b900 XP&r.": "&6Récompense&r : &b900 XP&r.",
    "&7Trident wielders of the deep.&r": "&7Porteurs de tridents des profondeurs.&r",
    "&aBounty&r: Continue thinning the &eDrowned&r population — focus on &cTrident-wielders&r.":
        "&aPrime&r : Continue à réduire la population de &eNoyés&r — concentre-toi sur les &cporteurs de tridents&r.",
    "&eLooting III&r dramatically increases &fTrident&r drops.":
        "&eButin III&r augmente fortement les drops de &fTridents&r.",
    "&7Silence the wailing skies.&r": "&7Fais taire les cieux gémissants.&r",
    "&aBounty&r: Kill &fGhasts&r in the &cNether&r — particularly in the &7Nether Wastes&r and &8Soul Sand Valley&r.":
        "&aPrime&r : Tue les &fGhasts&r dans le &cNether&r — en particulier dans les &7Friches du Nether&r et la &8Vallée de Sable d'Âme&r.",
    "Reflect their &cfireballs&r with a &fsword&r or &fpunch&r for an easy kill.":
        "Renvoie leurs &cboules de feu&r avec une &fépée&r ou un &fcoup de poing&r pour un kill facile.",
    "Drops &fGhast Tears&r (used in &dRegeneration potions&r) and &eGunpowder&r.":
        "Drop des &fLarmes de Ghast&r (utilisées dans les &dpotions de Régénération&r) et de la &epoudre à canon&r.",
    "&7Mask-wearers of the savanna.&r": "&7Porteurs de masques de la savane.&r",
    "&aBounty&r: Hunt the &eUmvuthana&r tribe from &dMowzie's Mobs&r — found in &esavanna&r biomes around their totems.":
        "&aPrime&r : Chasse la tribu &eUmvuthana&r de &dMowzie's Mobs&r — que l'on trouve dans les biomes de &esavane&r autour de leurs totems.",
    "&cBeware&r: they hunt in packs and call reinforcements from their &6Umvuthi Chieftain&r.":
        "&cAttention&r : ils chassent en meute et appellent des renforts auprès de leur &6Chef Umvuthi&r.",
    "Drops &eUmvuthana Masks&r — wearable trophies with unique effects.":
        "Drop des &eMasques Umvuthana&r — des trophées portables aux effets uniques.",
    "&7Goliaths of the Highlands.&r": "&7Géants des Hautes Terres.&r",
    "&aBounty&r: Slay &dTrolls&r in the &5Twilight Forest&r — they roam &eHighland caves&r near &cTroll Caves&r structures.":
        "&aPrime&r : Tue les &dTrolls&r dans la &5Twilight Forest&r — ils errent dans les &egrottes des Hautes Terres&r près des structures &cTroll Caves&r.",
    "&cTrolls hit hard&r and have heavy &fknockback resistance&r — bring &bDiamond&r or &5Netherite&r gear.":
        "&cLes Trolls frappent fort&r et ont une forte &frésistance au recul&r — apporte un équipement en &bDiamant&r ou &5Netherite&r.",
    "Drops &eMagic Beans&r used to grow giant beanstalks toward sky structures.":
        "Drop des &eHaricots Magiques&r utilisés pour faire pousser des haricots magiques géants vers les structures célestes.",
    # spell desc snippets
    "&7Provides temporary creative flight.": "&7Fournit un vol créatif temporaire.",
    "&eRequires:&7 1x Feather, 1x Phantom Membrane, 1x Air Essence":
        "&eRequiert :&7 1x Plume, 1x Membrane de Phantom, 1x Essence d'Air",
    "&7Decorative spell.": "&7Sort décoratif.",
    "&eUsage:&7 Celebratory effects.": "&eUsage :&7 Effets de célébration.",
    "&7Toggles rain/storm.": "&7Active/désactive la pluie/tempête.",
    "&eRequires:&7 1x Water Bucket, 1x Snowball, 1x Arrow":
        "&eRequiert :&7 1x Seau d'Eau, 1x Boule de Neige, 1x Flèche",
    "&7Your first spell focus.": "&7Ton premier focus de sort.",
    "&7Stores one spell.": "&7Stocke un sort.",
    "&7Inflicts Wither damage over time.": "&7Inflige des dégâts de Wither dans le temps.",
    "&bMana Cost:&7 Low": "&bCoût en Mana :&7 Faible",
    "&bMana Cost:&7 High": "&bCoût en Mana :&7 Élevé",
    "&eTip:&7 Good against high-armor targets.":
        "&eAstuce :&7 Efficace contre les cibles à forte armure.",
    "&7Reveals nearby source jars, spawners, etc.":
        "&7Révèle les bocaux à source, les spawners, etc. à proximité.",
    "&7The most powerful glyphs.": "&7Les glyphes les plus puissants.",
    "&7Requires an &6Archmage Spell Book&7.": "&7Nécessite un &6Grimoire d'Archimage&7.",
    "        &7&oThe final dungeon awaits...": "        &7&oLe donjon final t'attend...",
    "               &7&oSweet revenge!": "               &7&oDouce vengeance !",
    # Create endgame
    "&6Wrench:&r Rotates, dismantles, configures.":
        "&6Clé :&r Tourne, démonte, configure.",
    "&6Goggles:&r SEEING IS POWER. Displays SU stats, fluids, etc.":
        "&6Lunettes :&r VOIR C'EST POUVOIR. Affiche les stats SU, fluides, etc.",
    "&3Harvester:&r Harvests without breaking (Wheat, Potatoes).":
        "&3Moissonneuse :&r Récolte sans casser (Blé, Pommes de terre).",
    "&3Plough:&r Tills the soil or removes rails/torches.":
        "&3Charrue :&r Laboure la terre ou retire les rails/torches.",
    "&3Saw:&r Cuts down entire trees.": "&3Scie :&r Abat des arbres entiers.",
    "&3Drill:&r Mines stone.": "&3Foreuse :&r Mine la pierre.",
    "To automate your farms.": "Pour automatiser tes fermes.",
    "Must be mounted on a contraption (e.g.: Bearing or Minecart Chassis).":
        "Doit être monté sur une contraption (ex. : Roulement ou Châssis de Wagonnet).",
    # Cooking pots
    "The Stove provides constant heat. The Cooking Pot allows creating complex dishes. The Skillet is perfect for eggs and bacon.":
        "Le Fourneau fournit une chaleur constante. La Marmite permet de créer des plats complexes. La Poêle est parfaite pour les œufs et le bacon.",
    "The Slider only takes damage from a pickaxe. Get ready to run!":
        "Le Slider ne prend de dégâts qu'avec une pioche. Prépare-toi à courir !",
    "Flour, dough, and pie crust. The foundation of all desserts.":
        "Farine, pâte et fond de tarte. La base de tous les desserts.",
    "The most expensive dishes. They are placed on the ground like cakes. Use bowls to take servings.":
        "Les plats les plus coûteux. Ils se posent au sol comme des gâteaux. Utilise des bols pour prendre des parts.",
    # Already-translated French strings that are passed back through (also a few non-trivial)
    "Foreuse": "Foreuse",
    "Moissonneuse": "Moissonneuse",
    # Other French items left as-is
}


# ---------------------------------------------------------------------------
# Word-level translation map (used by heuristic translator for unknown strings)
# ---------------------------------------------------------------------------
WORD_MAP: list[tuple[str, str]] = [
    # multi-word phrases first
    ("Spell Book", "Grimoire"),
    ("Spellbook", "Grimoire"),
    ("Spell Focus", "Focus de Sort"),
    ("Mana Cost", "Coût en Mana"),
    ("Fishing Rod", "Canne à Pêche"),
    ("Tackle Box", "Boîte de Pêche"),
    ("Worm Farm", "Élevage de Vers"),
    ("Box Turtle", "Tortue-Boîte"),
    # Single words
]


# ---------------------------------------------------------------------------
# Translation function
# ---------------------------------------------------------------------------
def translate_value(s: str) -> str:
    """Translate a single string value.

    Order:
      1. Exact match in FULL dict.
      2. Heuristic: strings that are already French (contain accents) pass through.
      3. Apply word-level replacements.
      4. Leave as-is (low-confidence).
    """
    if s in FULL:
        return FULL[s]
    # Apply targeted word substitutions for unknown strings that still look English
    out = s
    for en, fr in WORD_MAP:
        out = out.replace(en, fr)
    return out


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with IN_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    result: dict[str, object] = {}
    low_conf_keys: list[str] = []

    for key, value in data.items():
        if isinstance(value, list):
            new_list = []
            for line in value:
                if not isinstance(line, str):
                    new_list.append(line)
                    continue
                translated = translate_value(line)
                if translated == line and line and line not in FULL:
                    # Possibly low-confidence (no exact mapping, no change)
                    if _looks_english(line):
                        low_conf_keys.append(f"{key}[{value.index(line)}]")
                new_list.append(translated)
            result[key] = new_list
        elif isinstance(value, str):
            translated = translate_value(value)
            if translated == value and value and value not in FULL:
                if _looks_english(value):
                    low_conf_keys.append(key)
            result[key] = translated
        else:
            result[key] = value

    with OUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Wrote {OUT_PATH}")
    print(f"Total keys: {len(result)}")
    print(f"Low-confidence entries: {len(low_conf_keys)}")
    if low_conf_keys:
        print("Examples (first 20):")
        for k in low_conf_keys[:20]:
            print(f"  - {k}")


def _looks_english(s: str) -> bool:
    if re.search(r"[À-ÿ]", s):
        return False
    return bool(
        re.search(
            r"\b(the|of|in|for|and|with|your|this|find|craft|hidden|deep|treasure|"
            r"requires|spell|holy|fire|ice|stone|gold|iron|wood|water|earth|air|ender|"
            r"blood|sword|book|staff|wand|boss|mob|kill|defeat|obtain|complete|tip|"
            r"warning|note|reward|bounty)\b",
            s.lower(),
        )
    )


if __name__ == "__main__":
    main()
