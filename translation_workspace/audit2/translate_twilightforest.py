#!/usr/bin/env python3
"""Translate twilightforest.json EN -> FR.

Architecture: per-prefix translators using hardcoded dicts + pattern matching.
"""
import json
import re
from pathlib import Path

INPUT = Path(r'c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/audit2/missing_per_mod/twilightforest.json')
OUTPUT = Path(r'c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/audit2/agent_output/twilightforest.json')

# ============================================================
# CORE NOUN/ENTITY DICTIONARIES (canonical FR names)
# ============================================================

# Entity / mob names (EN -> FR)
ENTITIES = {
    "Naga": "Naga",
    "Lich": "Liche",
    "Lich clone": "Clone de la Liche",
    "Lich Minion": "Serviteur de la Liche",
    "Hydra": "Hydre",
    "Ur-Ghast": "Ur-Ghast",
    "Snow Queen": "Reine des Neiges",
    "Minoshroom": "Minoshroom",
    "Minotaur": "Minotaure",
    "Alpha Yeti": "Yéti Alpha",
    "Yeti": "Yéti",
    "Quest Ram": "Bélier des Quêtes",
    "Questing Ram": "Bélier des Quêtes",
    "Knight Phantom": "Chevalier Fantôme",
    "Knight Phantoms": "Chevaliers Fantômes",
    "Goblin Knight": "Chevalier Gobelin",
    "Upper Goblin Knight": "Chevalier Gobelin Supérieur",
    "Lower Goblin Knight": "Chevalier Gobelin Inférieur",
    "Muffled Goblin Knight": "Chevalier Gobelin étouffé",
    "Block and Chain Goblin": "Gobelin au Bloc et Chaîne",
    "Hostile Wolf": "Loup Hostile",
    "Mist Wolf": "Loup de la Brume",
    "Hedge Spider": "Araignée des Haies",
    "Swarm Spider": "Araignée d'Essaim",
    "King Spider": "Reine des Araignées",
    "Slime Beetle": "Coléoptère Visqueux",
    "Fire Beetle": "Coléoptère de Feu",
    "Pinch Beetle": "Coléoptère",
    "Mosquito": "Moustique",
    "Mosquitoes": "Moustiques",
    "Mosquito Swarm": "Essaim de Moustiques",
    "Death Tome": "Tome de Mort",
    "Ice Crystal": "Cristal de Glace",
    "Ice Core": "Cœur de Glace",
    "Helmet Crab": "Casque-Crabe",
    "Maze Slime": "Slime du Labyrinthe",
    "Loyal Zombie": "Zombie Loyal",
    "Skeleton Druid": "Squelette Druide",
    "Carminite Broodling": "Couveuse Carminite",
    "Carminite Golem": "Golem Carminite",
    "Carminite Ghastguard": "Garde Ghast Carminite",
    "Carminite Ghastling": "Petit Ghast Carminite",
    "Bighorn Sheep": "Mouflon d'Amérique",
    "Dwarf Rabbit": "Lapin Nain",
    "Tiny Bird": "Petit Oiseau",
    "Squirrel": "Écureuil",
    "Penguin": "Manchot",
    "Raven": "Corbeau",
    "Cicada": "Cigale",
    "Firefly": "Luciole",
    "Moonworm": "Ver de Lune",
    "Redcap": "Casquette Rouge",
    "Redcap Sapper": "Sapeur à Casquette Rouge",
    "Sapper": "Sapeur",
    "Kobold": "Kobold",
    "Boggard": "Boggard",
    "Slider": "Glisseur",
    "Giant": "Géant",
    "Armored Giant": "Géant en Armure",
    "Giant Miner": "Mineur Géant",
    "Troll": "Troll",
    "Goblin": "Gobelin",
    "Boar": "Sanglier",
    "Deer": "Cerf",
    "Bird": "Oiseau",
    "Parrot": "Perroquet",
    "Mob": "Créature",
    "Roving Cube": "Cube Errant",
    "Harbinger Cube": "Cube Précurseur",
    "Reappearing Block": "Bloc Réapparaissant",
    "Vanishing Block": "Bloc Disparaissant",
    "Built Block": "Bloc Construit",
}

# Item / block / object names (used as nouns inside descriptions)
NOUNS = {
    "Twilight Forest Portal": "Portail de la Forêt du Crépuscule",
    "Twilight Forest": "Forêt du Crépuscule",
    "Dark Tower": "Tour Sombre",
    "Aurora Palace": "Palais d'Aurore",
    "Goblin Stronghold": "Forteresse Gobeline",
    "Knight Stronghold": "Forteresse des Chevaliers",
    "Hollow Hill": "Colline Creuse",
    "Hollow Hills": "Collines Creuses",
    "Hedge Maze": "Labyrinthe de Haies",
    "Lich Tower": "Tour de la Liche",
    "Naga Court": "Cour du Naga",
    "Naga Courtyard": "Cour du Naga",
    "Druid Hut": "Hutte de Druide",
    "Yeti Lair": "Antre du Yéti",
    "Yeti Cave": "Antre du Yéti",
    "Troll Caves": "Grottes des Trolls",
    "Troll Cave": "Grotte des Trolls",
    "Final Castle": "Château Final",
    "Mushroom Castle": "Château des Champignons",
    "Hydra Lair": "Antre de l'Hydre",
    "Minotaur Labyrinth": "Labyrinthe du Minotaure",
    "Carminite Reactor": "Réacteur Carminite",
    "Carminite Builder": "Constructeur Carminite",
    "Trophy Pedestal": "Piédestal à Trophée",
    "Boss Chest": "Coffre du Boss",
    "Keepsake Casket": "Cercueil Souvenir",
    "Casket": "Cercueil",
    "Uncrafting Table": "Table de Décraftage",
    "Drying Rack": "Séchoir",
    "Fire Jet": "Jet de Feu",
    "Ghast Trap": "Piège à Ghast",
    "Tree of Transformation": "Arbre de Transformation",
    "Tree of Time": "Arbre du Temps",
    "Fortification Shield": "Bouclier de Fortification",
    "Charm of Keeping": "Charme de Préservation",
    "Charm of Life": "Charme de Vie",
    "Block and Chain": "Bloc et Chaîne",
    "Cube of Annihilation": "Cube d'Annihilation",
    "Crumble Horn": "Corne en Ruine",
    "Magic Map": "Carte Magique",
    "Maze Map": "Carte du Labyrinthe",
    "Ore Map": "Carte des Minerais",
    "Ore Meter": "Compteur de Minerais",
    "Ore Magnet": "Aimant à Minerais",
    "Moon Dial": "Cadran Lunaire",
    "Lifedrain Scepter": "Sceptre de Vol de Vie",
    "Life Scepter": "Sceptre de Vie",
    "Twilight Scepter": "Sceptre du Crépuscule",
    "Zombie Scepter": "Sceptre Zombie",
    "Fortification Scepter": "Sceptre de Fortification",
    "Twilight Pearl": "Perle du Crépuscule",
    "Ice Bomb": "Bombe de Glace",
    "Lamp of Cinders": "Lampe de Cendres",
    "Peacock Feather Fan": "Éventail en Plume de Paon",
    "Peacock Fan": "Éventail de Paon",
    "Potion Flask": "Fiole de Potion",
    "Brittle Flask": "Fiole Friable",
    "Sliding Trap": "Piège Coulissant",
    "Castle Door": "Porte de Château",
    "Towerwood Door": "Porte de Bois de Tour",
    "Skull Chest": "Coffre Crâne",
    "Candelabra": "Candélabre",
    "Chiseled Bookshelf": "Bibliothèque Sculptée",
    "Boss music": "Musique de Boss",
    "Iron": "Fer",
    "Knightmetal Armor": "Armure de Métal des Chevaliers",
    "Map": "Carte",
    "Tear": "Larme",
    "Belt": "Ceinture",
    "Side Step": "Pas de Côté",
    "Double Jump": "Double Saut",
    "Traveller's Goggles": "Lunettes du Voyageur",
    "Torchberries": "Baies-Torches",
    "Acid rain": "Pluie acide",
    "Ground": "Sol",
    "Naga Scales": "Écailles de Naga",
    "Hydra Flame": "Flamme d'Hydre",
    "Lich Crown": "Couronne de la Liche",
    "Carminite Border": "Bordure Carminite",
    "Quest Ram Swirls": "Spirales du Bélier des Quêtes",
    "Questing Ram Swirls": "Spirales du Bélier des Quêtes",
    "Alpha Yeti Face": "Visage du Yéti Alpha",
    "Knight Helmet": "Casque de Chevalier",
    "Minoshroom Axes": "Haches du Minoshroom",
    "Snowflake": "Flocon de neige",
    "Naga Movement": "Mouvement du Naga",
    "Jar": "Pot",
}

# Materials (lowercase + capitalized variants)
MATERIALS = {
    "Mazestone": "Pierre du labyrinthe",
    "Knightmetal": "Métal des chevaliers",
    "Ironwood": "Bois de fer",
    "Steeleaf": "Feuille d'acier",
    "Trollsteinn": "Trollsteinn",
    "Carminite": "Carminite",
    "Borer Essence": "Essence de foreur",
    "Magic Beans": "Haricots magiques",
    "Twilight Glow": "Lueur Crépusculaire",
    "Wrought Iron": "Fer forgé",
    "Arctic Fur": "Fourrure arctique",
    "Alpha Yeti Fur": "Fourrure de Yéti Alpha",
    "Fiery Blood": "Sang ardent",
    "Fiery Tears": "Larmes ardentes",
    "Towerwood": "Bois de tour",
    "Castle Brick": "Brique de château",
    "Deadrock": "Pierre morte",
    "Nagastone": "Pierre du Naga",
    "Mushroom": "Champignon",
    "Twilight Oak": "Chêne du Crépuscule",
    "Rainbow Oak": "Chêne arc-en-ciel",
    "Canopy": "Canopée",
    "Mangrove": "Palétuvier",
    "Dark Wood": "Bois sombre",
    "Darkwood": "Bois sombre",
    "Mining Wood": "Bois minier",
    "Minewood": "Bois minier",
    "Sorting Wood": "Bois de tri",
    "Time Wood": "Bois du temps",
    "Transformation Wood": "Bois de transformation",
}

# Adjective/material variants used inside item names
ADJ_MAT = {
    # Material adjectives (when used like "Fiery Sword")
    "Fiery": "ardent",  # to be agreed with feminine form via post-process
    "Mazestone": "en pierre du labyrinthe",
    "Knightmetal": "en métal des chevaliers",
    "Ironwood": "en bois de fer",
    "Steeleaf": "en feuille d'acier",
    "Carminite": "carminite",
    "Towerwood": "en bois de tour",
    "Naga": "du Naga",
    "Minotaur": "du Minotaure",
    "Diamond Minotaur": "en diamant du Minotaure",
}

# Colors with proper masculine form (default; we'll handle agreement separately)
COLORS_M = {
    "Black": "noir",
    "Blue": "bleu",
    "Brown": "marron",
    "Cyan": "cyan",
    "Gray": "gris",
    "Green": "vert",
    "Light Blue": "bleu clair",
    "Light Gray": "gris clair",
    "Lime": "vert clair",
    "Magenta": "magenta",
    "Orange": "orange",
    "Pink": "rose",
    "Purple": "violet",
    "Red": "rouge",
    "White": "blanc",
    "Yellow": "jaune",
}
COLORS_F = {
    "Black": "noire",
    "Blue": "bleue",
    "Brown": "marron",
    "Cyan": "cyan",
    "Gray": "grise",
    "Green": "verte",
    "Light Blue": "bleue clair",
    "Light Gray": "grise clair",
    "Lime": "vert clair",
    "Magenta": "magenta",
    "Orange": "orange",
    "Pink": "rose",
    "Purple": "violette",
    "Red": "rouge",
    "White": "blanche",
    "Yellow": "jaune",
}
COLORS_FP = {  # feminine plural (e.g. "Écailles ... noires")
    "Black": "noires",
    "Blue": "bleues",
    "Brown": "marron",
    "Cyan": "cyan",
    "Gray": "grises",
    "Green": "vertes",
    "Light Blue": "bleues clair",
    "Light Gray": "grises clair",
    "Lime": "vert clair",
    "Magenta": "magenta",
    "Orange": "orange",
    "Pink": "roses",
    "Purple": "violettes",
    "Red": "rouges",
    "White": "blanches",
    "Yellow": "jaunes",
}
COLORS_MP = {  # masculine plural
    "Black": "noirs",
    "Blue": "bleus",
    "Brown": "marron",
    "Cyan": "cyan",
    "Gray": "gris",
    "Green": "verts",
    "Light Blue": "bleus clair",
    "Light Gray": "gris clair",
    "Lime": "vert clair",
    "Magenta": "magenta",
    "Orange": "orange",
    "Pink": "roses",
    "Purple": "violets",
    "Red": "rouges",
    "White": "blancs",
    "Yellow": "jaunes",
}

COLOR_RE_PATTERN = r"^(Black|Blue|Brown|Cyan|Gray|Green|Light Blue|Light Gray|Lime|Magenta|Orange|Pink|Purple|Red|White|Yellow)\s+(.+)$"

# ============================================================
# HARDCODED FULL-VALUE OVERRIDES
# ============================================================
HARDCODED = {
    # Advancements
    'advancement.twilightforest.full_mettle_alchemist': 'Alchimiste à plein métal',
    'advancement.twilightforest.craft_travellers_gear': 'Le tour de la Forêt en 80 jours',
    'advancement.twilightforest.modify_travellers_gear': "L'habit fait souvent le moine",
    'advancement.twilightforest.chicken_jerky': 'JERKY DE POULET !',
    'advancement.twilightforest.uncraft_uncrafting_table': "Briser le cycle",
    'advancement.twilightforest.uncraft_uncrafting_table.desc': "Décrafter une Table de Décraftage",
    'advancement.twilightforest.arctic_dyed.desc': "Teindre quatre pièces uniques d'armure arctique",
    'advancement.twilightforest.beanstalk.desc': "Obtenir des %s dans les grottes des trolls et les utiliser sur le sol lumineux sous les nuages",
    'advancement.twilightforest.craft_travellers_gear.desc': "Fabriquer une pièce d'équipement de voyageur",
    'advancement.twilightforest.fiery_set.desc': "Manier un outil ou une arme ardent en ayant au moins une pièce d'armure ardente dans l'inventaire",
    'advancement.twilightforest.full_mettle_alchemist.desc': "Boire trois doses de Dégâts II d'une fiole de potion en moins de 6 secondes et survivre",
    'advancement.twilightforest.hedge.desc': "Vaincre une araignée dans un Labyrinthe de Haies",
    'advancement.twilightforest.hill1.desc': "Vaincre un %s dans une Petite Colline Creuse",
    'advancement.twilightforest.hill2.desc': "Vaincre un %s dans une Colline Creuse Moyenne",
    'advancement.twilightforest.hill3.desc': "Vaincre un %s dans une Grande Colline Creuse",
    'advancement.twilightforest.hydra_chop.desc': "Se régaler d'un %s quand la barre de faim est vide",
    'advancement.twilightforest.kill_cicada.desc': "Tuer une Cigale",
    'advancement.twilightforest.kill_hydra.desc': "Vaincre la puissante %s et acquérir sa puissance",
    'advancement.twilightforest.kill_lich.desc': "Tuer la %s au sommet de sa tour et récupérer un sceptre pour éliminer les moustiques venimeux du Marécage, voir à travers les ténèbres aveuglantes de la malédiction de la Forêt Sombre, et résister au froid de la Forêt Enneigée",
    'advancement.twilightforest.kill_naga.desc': "Tuer le %s dans sa cour de la forêt et obtenir un %s pour franchir la barrière magique entourant la Tour de la Liche",
    'advancement.twilightforest.lich_scepters.desc': "Acquérir les quatre sceptres de pouvoir",
    'advancement.twilightforest.maze_map.desc': "Fabriquer la %s après avoir obtenu le focus du labyrinthe",
    'advancement.twilightforest.mazebreaker.desc': "Trouver la pioche %s dans la chambre forte secrète du labyrinthe",
    'advancement.twilightforest.modify_travellers_gear.desc': "Ajouter un modificateur à une pièce d'équipement de voyageur",
    'advancement.twilightforest.naga_armors.desc': "Fabriquer un %s et un %s",
    'advancement.twilightforest.ore_map.desc': "Fabriquer la %s",
    'advancement.twilightforest.progress_glacier.desc': "Vaincre la %s au sommet du Palais d'Aurore",
    'advancement.twilightforest.progress_knights.desc': "Apaiser les fantômes agités dans la tombe des chevaliers et les dispositifs de la Tour Carminite vous obéiront",
    'advancement.twilightforest.progress_labyrinth.desc': "Manger le Stroganoff de Meef pour acclimater votre corps à la chaleur dangereuse du Marécage de Feu",
    'advancement.twilightforest.progress_merge.desc': "Tuer le %s, le %s et le %s pour dissiper la pluie acide et vous endurcir pour les Hauts Plateaux",
    'advancement.twilightforest.progress_troll.desc': "Trouver le %s dans les Grottes des Trolls, et vous pourrez brûler les barrières d'épines",
    'advancement.twilightforest.progress_trophy_pedestal.desc': "Réclamer votre titre en plaçant un trophée sur le piédestal des ruines de la Forêt Sombre",
    'advancement.twilightforest.progress_ur_ghast.desc': "Vaincre l'%s au sommet de la Tour Sombre et libérer le ciel de la pluie acide",
    'advancement.twilightforest.progress_yeti.desc': "Vaincre le %s dans son antre et obtenir sa fourrure pour braver le froid mortel du glacier",
    'advancement.twilightforest.quest_ram.desc': "Donner toutes les couleurs de laine au %s",
    'advancement.twilightforest.root.desc': "Voyager dans la Forêt du Crépuscule",
    'advancement.twilightforest.troll.desc': "Trouver les Grottes des Trolls",
    'advancement.twilightforest.twilight_dining.desc': "Manger un repas dans la Forêt du Crépuscule",
    'advancement.twilightforest.twilight_hunter.desc': "Tuer une créature hostile dans la Forêt du Crépuscule",

    # Biome / dimension
    'biome.twilightforest.highlands_underground': "Grottes des Trolls",
    'dimension.twilightforest.twilight_forest': "Forêt du Crépuscule",
    'itemGroup.twilightforest.food': "Forêt du Crépuscule : Nourriture",

    # Enchantments
    'enchantment.twilightforest.destruction': "Destruction",
    'enchantment.twilightforest.renewal': "Renouvellement",
    'enchantment.twilightforest.renewal.desc': "Recharge automatiquement les sceptres lorsqu'ils sont à court de charges si le porteur a les objets de recharge dans son inventaire.",

    # Travellers gear
    'travellers_gear.ability': "Capacité : %s",
    'travellers_gear.broken': " (Cassé)",
    'travellers_gear.info_indent': "  ",
    'travellers_gear.shift_info': "Maintenir [SHIFT] pour les détails",
    'travellers_gear.modifier.empty': "Vide",

    # Game rules
    'gamerule.playersTfPortalCreativeDelay': "Délai du portail de la Forêt du Crépuscule en mode créatif",
    'gamerule.playersTfPortalCreativeDelay.description': "Temps (en ticks) qu'un joueur en mode créatif doit rester dans le Portail de la Forêt du Crépuscule avant de changer de dimension.",
    'gamerule.playersTfPortalDefaultDelay': "Délai du portail de la Forêt du Crépuscule en mode non-créatif",
    'gamerule.playersTfPortalDefaultDelay.description': "Temps (en ticks) qu'un joueur en mode non-créatif doit rester dans le Portail de la Forêt du Crépuscule avant de changer de dimension.",
    'gamerule.tfEnforcedProgression': "Forêt du Crépuscule : Progression imposée",
    'gamerule.tfEnforcedProgression.description': "Certains biomes de la Forêt du Crépuscule sont verrouillés tant que vous n'avez pas vaincu certains boss dans la dimension. Consultez vos avancements pour l'ordre de progression.",

    # Tag fluid
    'tag.fluid.twilightforest.fire_jet_fuel': "Carburant de Jet de Feu",

    # Jade
    'jade.drying_rack.remaining': "%s restant",
    'config.jade.plugin_twilightforest.chiseled_bookshelf_spawner': "Apparitions de la Bibliothèque sculptée en canopée",
    'config.jade.plugin_twilightforest.drying_rack': "Temps de séchage",
    'config.jade.plugin_twilightforest.quest_ram_wool': "Laine du Bélier des Quêtes",

    # Magic painting
    'magic_painting.twilightforest.castaway_paradise.author': "HexaBlu",
    'magic_painting.twilightforest.castaway_paradise.title': "Paradis du naufragé",
    'magic_painting.twilightforest.darkness.author': "???",
    'magic_painting.twilightforest.darkness.title': "Ténèbres",
    'magic_painting.twilightforest.lucid_lands.author': "Androsa",
    'magic_painting.twilightforest.lucid_lands.title': "Terres lucides",

    # Jukebox
    'jukebox_song.twilightforest.findings': "MrCompost - Findings",
    'jukebox_song.twilightforest.home': "MrCompost - Home",
    'jukebox_song.twilightforest.maker': "MrCompost - Maker",
    'jukebox_song.twilightforest.motion': "MrCompost - Motion",
    'jukebox_song.twilightforest.radiance': "Rotch Gwylt - Radiance",
    'jukebox_song.twilightforest.superstitious': "Lemonade - Superstitious",
    'jukebox_song.twilightforest.tower': "Lemonade - Tower",
    'jukebox_song.twilightforest.untamed': "Lemonade - Untamed",
    'jukebox_song.twilightforest.wandering': "Lemonade - Wandering",

    # Keys
    'key.twilightforest.categories.travellers_gear': "Forêt du Crépuscule (Équipement de voyageur)",
    'key.twilightforest.item_display_map_cycle': "Parcourir les cartes stockées de l'Affichage d'objet",
    'key.twilightforest.red_thread_vision': "Voir le fil rouge avec les lunettes",
    'key.twilightforest.swap_hotbar': "Échanger la barre d'outils",
    'key.twilightforest.zoom': "Zoomer avec les lunettes",

    # Stats
    'stat.twilightforest.blocks_crumbled': "Blocs émiettés",
    'stat.twilightforest.bugs_squished': "Insectes écrasés",
    'stat.twilightforest.e115_slices_eaten': "Tranches d'Expérience 115 mangées",
    'stat.twilightforest.keeping_charms_activated': "Charmes de Préservation utilisés",
    'stat.twilightforest.life_charms_activated': "Charmes de Vie utilisés",

    # GUI
    'gui.twilightforest.drying_ticks': "%s ticks",
    'gui.twilightforest.drying_minute': "%s minute",
    'gui.twilightforest.drying_minutes': "%s minutes",
    'gui.twilightforest.drying_second': "%s seconde",
    'gui.twilightforest.drying_seconds': "%s secondes",
    'gui.twilightforest.drying_jei': "Séchoir",
    'gui.twilightforest.crumble_horn_jei': "Corne en ruine",
    'gui.twilightforest.optifine.title': "AVERTISSEMENT : OPTIFINE DÉTECTÉ",
    'gui.twilightforest.optifine.message': "Avant de continuer, veuillez noter qu'Optifine est connu pour causer des plantages, des bugs visuels d'entités multipart et de nombreux autres problèmes.\n\nAvant de signaler un bug, veuillez d'abord retirer Optifine et vérifier à nouveau si le bug est toujours présent.\n\nLes problèmes liés à Optifine ne peuvent pas être résolus du côté de la Forêt du Crépuscule !\n\nCet écran peut être désactivé dans la configuration client.",
    'gui.twilightforest.optifine.continue': "Continuer",
    'gui.twilightforest.optifine.disable': "Ne plus afficher",
    'gui.twilightforest.optifine.quit': "Quitter le jeu",

    # Misc
    'misc.twilightforest.biome_locked': "Biome verrouillé !",
    'misc.twilightforest.magic_map_fail': "La magie a faibli. Peut-être qu'elle ne fonctionne pas ici ?",
    'misc.twilightforest.ore_meter_header_block': "Bloc",
    'misc.twilightforest.ore_meter_header_count': "Nombre",
    'misc.twilightforest.ore_meter_new_range': "Portée définie à %s chunks",
    'misc.twilightforest.ore_meter_targeted_block': "Bloc ciblé : %s",
    'misc.twilightforest.ore_meter_total': "Total des blocs scannés : %s",
    'misc.twilightforest.firefly_spawner_radius': "Rayon des particules de luciole : %s blocs",

    # Container
    'container.twilightforest.uncrafting_table': "Table de décraftage",
    'container.twilightforest.uncrafting_table.cycle_back_ingredient': "Ingrédients de décraftage précédents",
    'container.twilightforest.uncrafting_table.cycle_back_recipe': "Recette de craftage précédente",
    'container.twilightforest.uncrafting_table.cycle_back_uncraft': "Recette de décraftage précédente",
    'container.twilightforest.uncrafting_table.cycle_next_ingredient': "Ingrédients de décraftage suivants",
    'container.twilightforest.uncrafting_table.cycle_next_recipe': "Recette de craftage suivante",
    'container.twilightforest.uncrafting_table.cycle_next_uncraft': "Recette de décraftage suivante",

    # Tag items
    'tag.item.c.gems.carminite': "Gemmes de carminite",
    'tag.item.c.ingots.fiery': "Lingots ardents",
    'tag.item.c.ingots.ironwood': "Lingots de bois de fer",
    'tag.item.c.ingots.knightmetal': "Lingots de métal des chevaliers",
    'tag.item.c.ingots.steeleaf': "Lingots de feuille d'acier",
    'tag.item.c.ingots.wrought_iron': "Lingots de fer forgé",
    'tag.item.c.paper': "Papiers",
    'tag.item.c.raw_materials.ironwood': "Bois de fer brut",
    'tag.item.c.raw_materials.knightmetal': "Métal des chevaliers brut",
    'tag.item.c.storage_blocks.arctic_fur': "Blocs de stockage de fourrure arctique",
    'tag.item.c.storage_blocks.carminite': "Blocs de stockage de carminite",
    'tag.item.c.storage_blocks.fiery': "Blocs de stockage ardents",
    'tag.item.c.storage_blocks.ironwood': "Blocs de stockage de bois de fer",
    'tag.item.c.storage_blocks.knightmetal': "Blocs de stockage de métal des chevaliers",
    'tag.item.c.storage_blocks.steeleaf': "Blocs de stockage de feuille d'acier",
    'tag.item.twilightforest.repairs_giant_tools': "Répare les outils géants",
    'tag.item.twilightforest.tiny_bird_tempt_items': "Appâts pour Petits Oiseaux",
    'tag.item.twilightforest.canopy_logs': "Bûches de canopée",
    'tag.item.twilightforest.scepters': "Sceptres",
    'tag.item.twilightforest.mining_logs': "Bûches de bois minier",
    'tag.item.twilightforest.fiery_vial': "Fioles ardentes",
    'tag.item.twilightforest.towerwood': "Blocs de bois de tour",
    'tag.item.twilightforest.arctic_fur': "Fourrure arctique",

    # Museum curator
    'museumcurator.animalhusbandry.twilightforest.bugs': "Insectes",
    'museumcurator.architecture.twilightforest.aurorablocks': "Blocs d'aurore",
    'museumcurator.architecture.twilightforest.banisters': "Rampes",
    'museumcurator.architecture.twilightforest.castlebrick': "Brique de château",
    'museumcurator.architecture.twilightforest.giantblocks': "Blocs géants",
    'museumcurator.botany.twilightforest.beanstalk': "Haricot magique",
    'museumcurator.botany.twilightforest.canopytree': "Arbre canopée",
    'museumcurator.botany.twilightforest.darkwoodtree': "Arbre sombre",
    'museumcurator.botany.twilightforest.mangrovetree': "Palétuvier",
    'museumcurator.botany.twilightforest.miningtree': "Arbre minier",
    'museumcurator.equipment.twilightforest.scepters': "Sceptres de pouvoir",
    'museumcurator.lithology.twilightforest.deadrock': "Pierre morte",
    'museumcurator.lithology.twilightforest.mazestone': "Pierre du labyrinthe",
    'museumcurator.lithology.twilightforest.nagastone': "Pierre du Naga",
    'museumcurator.machinery.twilightforest.carminitemachines': "Mécanismes carminites",
    'museumcurator.metallurgy.twilightforest.fiery': "Métal ardent",
    'museumcurator.metallurgy.twilightforest.ironwood': "Bois de fer",
    'museumcurator.metallurgy.twilightforest.knightmetal': "Métal des chevaliers",

    # Configuration
    'twilightforest.configuration.client': "Client",
    'twilightforest.configuration.common': "Commun",
    'twilightforest.configuration.server': "Serveur",
    'twilightforest.configuration.dimension': "Dimension",
    'twilightforest.configuration.shaders': "Shaders",
    'twilightforest.configuration.section.twilightforest.client.toml': "Paramètres client",
    'twilightforest.configuration.section.twilightforest.client.toml.title': "Paramètres client",
    'twilightforest.configuration.section.twilightforest.common.toml': "Paramètres communs",
    'twilightforest.configuration.section.twilightforest.common.toml.title': "Paramètres communs",
    'twilightforest.configuration.title': "Configuration de la Forêt du Crépuscule",

    # ==== TIPS ====
    'twilightforest.tips.alpha_yeti': "Le saccage du Yéti Alpha provoque la chute de blocs depuis le plafond. Attention aux glaçons qui tombent !",
    'twilightforest.tips.anvil_squashing': "Les insectes peuvent être écrasés par les enclumes.",
    'twilightforest.tips.arctic_armor': "L'armure arctique peut être teinte de n'importe quelle couleur.",
    'twilightforest.tips.baby_jockey': "Des bébés Squelettes Druides peuvent être trouvés chevauchant des Araignées d'Essaim.",
    'twilightforest.tips.banister_shape': "Les rampes peuvent être cliquées droit avec une hache pour changer leur hauteur.",
    'twilightforest.tips.berry_bushes': "Des buissons de baies se trouvent partout dans la Forêt du Crépuscule.",
    'twilightforest.tips.block_and_chain': "Enchanter un Bloc et Chaîne avec Destruction lui permet de casser des blocs.",
    'twilightforest.tips.boggard': "C'est quoi un Boggard ?",
    'twilightforest.tips.bugs_on_head': "Les insectes resteront volontiers sur votre tête.",
    'twilightforest.tips.burnt_thorns': "Les épines brûlées se désintègrent quand on marche dessus.",
    'twilightforest.tips.candelabra': "Utiliser de la poudre de redstone sur un candélabre rendra ses flammes rouges et émettra un signal de redstone.",
    'twilightforest.tips.carminite_builder': "Les Constructeurs Carminite placent des blocs temporaires dans la direction où vous regardez.",
    'twilightforest.tips.casket_logging': "Le Cercueil Souvenir peut être rempli d'eau, de lave, ou enchâssé dans un bloc s'il est victime d'une interaction fluide.",
    'twilightforest.tips.casket_usage': "Le Cercueil Souvenir agit comme une pierre tombale à usage limité. S'il est dans votre inventaire à votre mort, il se placera tout seul et conservera tous vos objets à l'intérieur.",
    'twilightforest.tips.charm_of_keeping': "Un Charme de Préservation rendra une partie de votre inventaire après votre mort.",
    'twilightforest.tips.charm_of_life': "Un Charme de Vie peut vous sauver d'un coup fatal.",
    'twilightforest.tips.clouds': "Les Nuages Pluvieux et Neigeux peuvent être utilisés pour simuler des effets météo !",
    'twilightforest.tips.craft_travellers_gear': "L'équipement de voyageur peut être fabriqué en séchant du Cuir Traité pour le transformer en Cuir Tanné.",
    'twilightforest.tips.crumble_horn': "La Corne en Ruine détériore les blocs proches lorsqu'elle est utilisée.",
    'twilightforest.tips.druid_hut': "Les Huttes de Druide ont parfois des sous-sols cachés.",
    'twilightforest.tips.e115_pickup': "Sneak + clic droit sur de l'Expérience 115 placée pour la récupérer.",
    'twilightforest.tips.e115_sprinkle': "On peut saupoudrer de la redstone sur l'Expérience 115.",
    'twilightforest.tips.emperors_cloth': "Le Tissu d'Empereur empêche l'armure d'être affichée lorsqu'on l'utilise pour la fabriquer.",
    'twilightforest.tips.essence_charge': "L'Essence Exanime rechargera complètement n'importe quel sceptre fabriqué avec elle.",
    'twilightforest.tips.experiment_115': "Quelqu'un sait ce qu'est vraiment l'Expérience 115 ?",
    'twilightforest.tips.feather_fan': "L'Éventail en Plume de Paon peut être utilisé pour repousser les créatures, ou vous propulser dans les airs si utilisé en sautant. Il fonctionne aussi très bien avec l'Élytre et la Masse !",
    'twilightforest.tips.fiery_pickaxe': "Une Pioche Ardente fait fondre tous les blocs qu'elle casse.",
    'twilightforest.tips.ghast_trap': "Tuer des Petits Ghasts Carminite près d'un Piège à Ghast le chargera.",
    'twilightforest.tips.giant_block': "Miner une zone 4x4x4 du même bloc avec une Pioche de Géant fera tomber 1 bloc géant à la place.",
    'twilightforest.tips.glass_sword': "Les Épées de Verre se brisent après un seul coup.",
    'twilightforest.tips.hollow_log': "Diverses choses peuvent être placées à l'intérieur des Bûches Creuses : neige, mousse ou échelles.",
    'twilightforest.tips.hollow_oak_sapling': "Des pousses qui font pousser de gigantesques arbres creux se trouvent dans les Huttes de Druide.",
    'twilightforest.tips.hollow_oak_tree': "Les arbres de Chêne Creux ont parfois des pièces de type donjon avec un butin unique dans leurs feuilles.",
    'twilightforest.tips.hydra_chop': "Les Tranches d'Hydre remplissent complètement votre barre de faim quand on les mange.",
    'twilightforest.tips.hydra_heads': "Pour chaque tête tuée, l'Hydre en fera repousser deux à sa place !",
    'twilightforest.tips.hydra_mortars': "Vous pouvez dévier l'attaque de mortier de l'Hydre.",
    'twilightforest.tips.ice_core': "Les Cœurs de Glace et les Gardiens des Neiges fondent dans les biomes chauds.",
    'twilightforest.tips.jars': "Les Lucioles et les Cigales peuvent être mises dans des pots.",
    'twilightforest.tips.jerky': "La viande peut être séchée en jerky en utilisant les Séchoirs.",
    'twilightforest.tips.key_biome_locations': "Les groupes de biomes de progression sont générés à environ 600 blocs les uns des autres, ce qui signifie que le prochain boss n'est jamais trop loin.",
    'twilightforest.tips.key_biomes': "Les biomes de progression sont générés en groupes de 4 mini-boss entourant un boss normal.",
    'twilightforest.tips.kobold': "Kobold",
    'twilightforest.tips.labyrinth_vault': "Le Labyrinthe contient une pièce secrète.",
    'twilightforest.tips.lich_deflection': "La Liche du Crépuscule déviera les éclairs du Sceptre du Crépuscule une fois ses boucliers tombés.",
    'twilightforest.tips.lich_scepters': "La Liche fait tomber une variété de sceptres magiques.",
    'twilightforest.tips.liveroot': "La Racine Vivante se trouve sous la plupart des arbres.",
    'twilightforest.tips.magic_beans': "Planter des Haricots Magiques sur de la Terre Bénie fait pousser un puissant haricot magique.",
    'twilightforest.tips.magic_leaves': "Les Feuilles d'Arbre Magique ne donnent pas de pousses lorsqu'elles sont cassées.",
    'twilightforest.tips.magic_map': "Les Cartes Magiques sont utilisées pour localiser facilement les structures.",
    'twilightforest.tips.magic_saplings': "Des pousses magiques spéciales se trouvent à l'intérieur des arbres de Chêne Creux.",
    'twilightforest.tips.maze_map_focus': "Les Minotaures peuvent occasionnellement faire tomber des Focus de Carte du Labyrinthe, qui peuvent être utilisés pour fabriquer des Cartes du Labyrinthe.",
    'twilightforest.tips.mazebreaker': "Le Mazebreaker peut casser les blocs de Pierre du labyrinthe 16 fois plus vite et ne subit pas de dégâts de durabilité supplémentaires.",
    'twilightforest.tips.mining_tree': "L'Arbre du Mineur fait remonter les minerais à la surface.",
    'twilightforest.tips.minion_buff': "Si la Liche du Crépuscule frappe un de ses serviteurs avec un projectile, le serviteur deviendra plus fort et plus rapide.",
    'twilightforest.tips.minoshroom': "Le Minoshroom effectuera une attaque de fracas si un joueur reste trop près de lui.",
    'twilightforest.tips.modify_travellers_gear': "Chaque pièce d'équipement de voyageur a 1 capacité intégrée, et jusqu'à 3 autres peuvent être ajoutées par pièce.",
    'twilightforest.tips.moon_dial': "Le Cadran Lunaire indique la phase actuelle de la lune.",
    'twilightforest.tips.moonworm_queen': "La Reine des Vers de Lune peut être nourrie de Baies-Torches.",
    'twilightforest.tips.mushglooms': "Les Mushglooms ne peuvent pas être transformés en champignons géants avec de la poudre d'os. Cependant, les placer sur de la Terre Bénie les fera grandir.",
    'twilightforest.tips.music_disc': "Les Disques de Musique se trouvent en dehors des donjons.",
    'twilightforest.tips.mystic_crown': "La Couronne Mystique améliore légèrement les sceptres lorsqu'elle est portée.",
    'twilightforest.tips.naga': "Le Naga peut être étourdi en le faisant heurter quelque chose de dur !",
    'twilightforest.tips.nether_bushes': "Avec d'autres objets et matériaux étrangers, une végétation étrange s'est établie dans la Tour Sombre.",
    'twilightforest.tips.netherite_axe': "Il n'y aura jamais de Hache de Minotaure en Netherite.",
    'twilightforest.tips.ominous_fire': "Le feu inquiétant peut transformer les créatures en mort-vivants.",
    'twilightforest.tips.ore_magnet': "L'Aimant à Minerais peut faire remonter des veines de minerai à la surface.",
    'twilightforest.tips.ore_meter': "Le Compteur de Minerais affiche tous les minerais à proximité une fois activé. Il peut aussi cibler certains blocs en faisant shift+clic droit dessus, et n'affichera alors qu'un compte de ces blocs à proximité.",
    'twilightforest.tips.oreberries': "Des buissons de baies métalliques apparaissent rarement sous terre.",
    'twilightforest.tips.parrying': "Un blocage de bouclier bien chronométré peut renvoyer un projectile sur une créature.",
    'twilightforest.tips.peacock_feather_fan': "L'Éventail en Plume de Paon peut être utilisé pour éteindre les Bougies.",
    'twilightforest.tips.phantom_armor': "L'Armure Fantôme est automatiquement conservée à la mort.",
    'twilightforest.tips.phantoms': "Les Chevaliers Fantômes prennent beaucoup moins de dégâts s'ils sont invisibles. Essayez de cibler le visible quand vous les combattez !",
    'twilightforest.tips.pocket_watch': "La Montre de Poche du Lapin accorde de la vitesse supplémentaire dans la barre d'outils, et augmente la vitesse de minage quand elle est tenue.",
    'twilightforest.tips.potion_flask': "Les Fioles de Potion peuvent contenir jusqu'à 3 doses de la même potion.",
    'twilightforest.tips.quest_ram': "Le Bélier des Quêtes récompensera quiconque lui donnera ce qu'il manque.",
    'twilightforest.tips.red_thread': "Le Fil Rouge peut être vu à travers les murs.",
    'twilightforest.tips.redcap': "Les Casquettes Rouges peuvent placer et allumer de la TNT.",
    'twilightforest.tips.renewal': "Les sceptres enchantés avec Renouvellement se rechargeront automatiquement avec les objets requis dans l'inventaire du joueur.",
    'twilightforest.tips.skull_candle': "Les bougies peuvent être placées sur les têtes de créatures pour créer une jolie source de lumière.",
    'twilightforest.tips.sorting_tree': "L'Arbre de Tri triera les coffres à côté de lui dans d'autres coffres à proximité.",
    'twilightforest.tips.spooky_forest': "La Forêt effrayante n'a pas pour thème Halloween.",
    'twilightforest.tips.structure_conquering': "Tuer un boss empêchera l'apparition de créatures dans cette structure.",
    'twilightforest.tips.structure_spawning': "Les structures apparaissent selon un motif en grille.",
    'twilightforest.tips.the_lore': "L'histoire est toute là, il vous suffit de la découvrir vous-même !",
    'twilightforest.tips.the_walls': "Les Tomes de Mort sont dans vos murs. Ils sont dans vos murs.",
    'twilightforest.tips.time_tree': "L'Arbre du Temps accélère la croissance des cultures à proximité.",
    'twilightforest.tips.torchberries': "Nous avons fait les baies lumineuses en premier !",
    'twilightforest.tips.towerwood': "Les Planches de Bois de Tour sont très résistantes au feu, mais pas immunisées.",
    'twilightforest.tips.transformation_tree': "L'Arbre de Transformation convertira la zone autour de lui en Forêt Enchantée.",
    'twilightforest.tips.trollber_ripening': "Tuer un Troll fait mûrir les Trollbers à proximité.",
    'twilightforest.tips.trophy_pedestal': "Les Piédestaux à Trophée ne peuvent être minés qu'après avoir été activés.",
    'twilightforest.tips.twilight_portal': "Lancez un diamant dans une mare d'eau entourée de fleurs.",
    'twilightforest.tips.uncrafting_table': "La Table de Décraftage ne sert pas qu'à décrafter des objets. Elle peut aussi recrafter des objets en d'autres, réparer des outils et armures, et transférer des enchantements entre les équipements !",
    'twilightforest.tips.ur_ghast': "L'Ur-Ghast peut être tiré du ciel à l'aide de Pièges à Ghast.",
    'twilightforest.tips.vanishing_block': "Les Blocs Disparaissants disparaissent pour toujours quand ils sont activés.",
    'twilightforest.tips.worldgen_features': "La forêt est remplie de nombreuses ruines. Certaines peuvent même contenir des objets uniques.",
    'twilightforest.tips.wrought_iron': "Les Barreaux de Fer Forgé ne peuvent pas être obtenus normalement. Ils ne peuvent être obtenus qu'en décraftant des blocs faits avec.",
    'twilightforest.tips.yeti': "Les Yétis adorent lancer des choses.",
    'twilightforest.tips.zombie_healing': "Les Zombies invoqués avec un Sceptre Zombie peuvent être guéris avec de la Chair Putréfiée.",

    # ==== CONFIG ====
    'config.twilightforest.animate_trophies': "Animer les trophées",
    'config.twilightforest.animate_trophies.tooltip': "Faire tourner les têtes de Trophée sur le modèle d'objet. N'a aucun impact sur les performances. Pour ceux qui n'aiment pas s'amuser.",
    'config.twilightforest.aurora_biomes': "Biomes du shader d'aurore",
    'config.twilightforest.aurora_biomes.button': "Modifier les biomes",
    'config.twilightforest.aurora_biomes.tooltip': "Définit dans quels biomes l'effet de shader d'aurore apparaîtra. Laisser la liste vide pour désactiver l'effet.",
    'config.twilightforest.boss_drop_chests': "Coffres de butin du boss",
    'config.twilightforest.boss_drop_chests.tooltip': "Si vrai, les boss de la Forêt du Crépuscule placeront leurs récompenses dans un coffre à l'endroit où ils sont apparus au lieu de les laisser tomber directement.\nNotez que les Chevaliers Fantômes ne sont pas affectés car leurs récompenses fonctionnent différemment.",
    'config.twilightforest.casket_uuid_locking': "Verrouillage UUID des cercueils",
    'config.twilightforest.casket_uuid_locking.tooltip': "Si vrai, les Cercueils Souvenir générés à la mort d'un joueur ne seront pas accessibles aux autres joueurs. Utilisez ceci si vous ne voulez pas que les gens prennent des cercueils des autres.\nREMARQUE : les opérateurs du serveur pourront toujours ouvrir les cercueils verrouillés.",
    'config.twilightforest.check_portal_placement': "Vérifier le placement du portail",
    'config.twilightforest.check_portal_placement.tooltip': "Détermine si les nouveaux portails doivent être pré-vérifiés pour la sécurité. Si faux, les portails échoueront à se former plutôt que de rediriger vers une destination alternative sûre.\nNotez que désactiver ceci réduit aussi la fréquence à laquelle les vérifications de formation de portail sont effectuées.",
    'config.twilightforest.cloud_precipitation': "Distance de précipitation des nuages",
    'config.twilightforest.cloud_precipitation.tooltip': "Dicte combien de blocs en dessous d'un bloc de nuage la logique de jeu doit vérifier pour gérer le code lié à la météo.\nDiminuez si vous avez un faible taux de tick. Mettez à 0 pour désactiver toute la logique de précipitation des nuages.",
    'config.twilightforest.default_item_enchantments': "Enchantements d'objets par défaut",
    'config.twilightforest.default_item_enchantments.tooltip': "Si faux, les objets qui sont enchantés à la fabrication (comme l'équipement en bois de fer ou feuille d'acier) ne seront pas affichés ainsi dans l'inventaire créatif.\nNotez que cela n'affecte pas les recettes de craftage elles-mêmes, vous aurez besoin d'un datapack pour les modifier.",
    'config.twilightforest.destructive_portal_lighting': "Foudre destructrice",
    'config.twilightforest.destructive_portal_lighting.tooltip': "Mettez ceci à faux si vous voulez que la foudre qui frappe le portail ne mette pas le feu aux choses. Pour ceux qui n'aiment pas s'amuser.",
    'config.twilightforest.dim_settings': "Paramètres de dimension",
    'config.twilightforest.dim_settings.tooltip': "Paramètres qui ne sont pas réversibles sans conséquences.",
    'config.twilightforest.disable_portal': "Désactiver la création de portail",
    'config.twilightforest.disable_portal.tooltip': "Désactive entièrement la création de portail de la Forêt du Crépuscule. Fourni pour les opérateurs de serveur cherchant à restreindre l'accès à la dimension.",
    'config.twilightforest.disable_skull_candles': "Désactiver les Bougies à Crâne",
    'config.twilightforest.disable_skull_candles.tooltip': "Si vrai, désactive la possibilité de fabriquer des Bougies à Crâne en faisant clic droit sur un crâne vanilla avec une bougie. Activez ceci si vous avez des problèmes de conflit de mods.",
    'config.twilightforest.disable_uncrafting': "Désactiver le décraftage",
    'config.twilightforest.disable_uncrafting.tooltip': "Désactive la fonction de décraftage de la table de décraftage. Recommandé en dernier recours s'il y a trop de choses à changer dans son comportement (ou si vous êtes juste paresseux, je ne juge pas).\nNotez que les recettes spéciales de décraftage ne sont pas désactivées car le mod en dépend pour d'autres choses.",
    'config.twilightforest.disable_uncrafting_table': "Désactiver la Table de Décraftage",
    'config.twilightforest.disable_uncrafting_table.tooltip': "Désactive toute utilisation de la table de décraftage, et l'empêche d'apparaître dans le butin ou en craft.\nNotez que la table a plus d'usages que le simple décraftage, vous pouvez les lire ici ! http://benimatic.com/tfwiki/index.php?title=Uncrafting_Table\nIl est fortement recommandé de garder la table activée car le mod a des recettes exclusives au décraftage, mais l'option reste pour les gens qui ne veulent pas que la table soit fonctionnelle du tout.\nSi vous voulez juste empêcher les recettes normales de craftage d'être inversées, envisagez d'utiliser l'option 'disableUncrafting' à la place.",
    'config.twilightforest.first_person_glove_overlay': "Surcouche de gant en première personne",
    'config.twilightforest.first_person_glove_overlay.tooltip': "Permet aux Gants du Voyageur d'apparaître sur votre main en vue à la première personne.",
    'config.twilightforest.giant_skin_uuid_list': "Skins de Géants",
    'config.twilightforest.giant_skin_uuid_list.button': "Modifier les skins",
    'config.twilightforest.giant_skin_uuid_list.tooltip': "Liste d'UUID de joueurs dont les skins doivent être utilisés par les Géants. Laisser la liste vide pour utiliser le skin du joueur les regardant.",
    'config.twilightforest.ingredient_switching': "Désactiver le changement d'ingrédients",
    'config.twilightforest.ingredient_switching.tooltip': "Si vrai, la table de décraftage ne permettra plus de changer entre les ingrédients si une recette utilise un tag pour la fabrication.\nCeci supprimera la fonctionnalité pour TOUTES LES RECETTES !\nSi vous voulez empêcher certains ingrédients d'apparaître en premier lieu, utilisez le tag \"twilightforest:banned_uncrafting_ingredients\".",
    'config.twilightforest.item_display': "Paramètres du modificateur d'affichage d'objet",
    'config.twilightforest.item_display.tooltip': "Contrôle où divers éléments sont rendus lors de l'utilisation du Modificateur d'Affichage d'Objet sur l'équipement de voyageur.",
    'config.twilightforest.locked_toasts': "Désactiver les toasts de biome verrouillé",
    'config.twilightforest.locked_toasts.tooltip': "Désactive les toasts qui apparaissent lors de l'entrée dans un biome verrouillé. Non recommandé si vous n'êtes pas familier avec la progression.",
    'config.twilightforest.magic_trees': "Arbres magiques",
    'config.twilightforest.magic_trees.tooltip': "Paramètres pour tout ce qui concerne les arbres magiques.",
    'config.twilightforest.manual_travellers_wings_gradual_glide': "Plané graduel manuel",
    'config.twilightforest.manual_travellers_wings_gradual_glide.tooltip': "Lorsque cette option est désactivée, la chute lente est par défaut. Maintenir la touche s'accroupir vous fait tomber à vitesse normale. Lorsque cette option est activée, la chute normale est par défaut. Maintenir la touche s'accroupir active la chute lente.",
    'config.twilightforest.max_portal_size': "Taille maximale du portail",
    'config.twilightforest.max_portal_size.tooltip': "Le nombre maximum d'espaces d'eau que le mod vérifiera lors de la création d'un portail. Des nombres très élevés peuvent causer des problèmes de performance.",
    'config.twilightforest.mining_range': "Portée de l'Arbre du Mineur",
    'config.twilightforest.mining_range.tooltip': "Définit le rayon auquel le Cœur de Bois Minier fonctionne. Peut être un nombre entre 1 et 128.\nMettez à 0 pour empêcher le Cœur de Bois Minier de fonctionner.",
    'config.twilightforest.multiplayer_fight_adjuster': "Ajusteur de combat multijoueur",
    'config.twilightforest.multiplayer_fight_adjuster.more_health': "Plus de vie",
    'config.twilightforest.multiplayer_fight_adjuster.more_loot': "Plus de butin",
    'config.twilightforest.multiplayer_fight_adjuster.more_loot_and_health': "Plus de butin et de vie",
    'config.twilightforest.multiplayer_fight_adjuster.none': "Aucun",
    'config.twilightforest.multiplayer_fight_adjuster.tooltip': "Détermine comment les boss doivent s'ajuster aux combats multijoueurs. Il y a 4 valeurs possibles :\nNONE : ne fait rien quand plusieurs personnes participent à un combat de boss. Les boss agissent comme en solo.\nMORE_LOOT : ajoute des récompenses supplémentaires à la table de butin du boss en fonction du nombre de joueurs participants. Entièrement contrôlé via la table de butin de l'entité, en utilisant la fonction de butin `twilightforest:multiplayer_multiplier`. Notez que cette fonction n'affectera que les entités incluses dans le tag `twilightforest:multiplayer_inclusive_entities`.\nMORE_HEALTH : augmente la vie de chaque boss de 20 cœurs pour chaque joueur à proximité au début du combat.\nMORE_LOOT_AND_HEALTH : combine les deux options précédentes.",
    'config.twilightforest.optifine': "Écran Optifine",
    'config.twilightforest.optifine.tooltip': "Désactive l'écran d'avertissement quand OptiFine est installé.",
    'config.twilightforest.origin_dimension': "Dimension d'origine",
    'config.twilightforest.origin_dimension.tooltip': "La dimension depuis laquelle vous pouvez toujours voyager vers la Forêt du Crépuscule, ainsi que la dimension à laquelle vous reviendrez. Par défaut l'overworld. (domaine:nomreg).",
    'config.twilightforest.parry_non_twilight': "Parer les projectiles non-TF",
    'config.twilightforest.parry_non_twilight.tooltip': "Mettez à vrai pour parer les projectiles non-Crépusculaires.",
    'config.twilightforest.parry_window': "Fenêtre de parade",
    'config.twilightforest.parry_window.tooltip': "Le nombre de ticks après avoir levé un bouclier permettant de parer un projectile. (1 tick = 1/20 seconde)",
    'config.twilightforest.portal_for_new_player': "Créer un portail de retour pour les joueurs",
    'config.twilightforest.portal_for_new_player.tooltip': "Si vrai, le portail de retour apparaîtra pour les nouveaux joueurs envoyés dans la Forêt du Crépuscule si `newPlayersSpawnInTF` est vrai.",
    'config.twilightforest.portal_permission': "Permission de création de portail",
    'config.twilightforest.portal_permission.tooltip': "Permet aux personnes ayant la permission spécifiée ou supérieure de créer des portails. Basé sur le système de permissions de Vanilla.\nVous pouvez en savoir plus ici : https://minecraft.wiki/w/Permission_level",
    'config.twilightforest.portal_return': "Verrouiller le portail de retour",
    'config.twilightforest.portal_return.tooltip': "Si faux, le portail de retour nécessitera l'objet d'activation.",
    'config.twilightforest.portal_settings': "Paramètres du portail",
    'config.twilightforest.portal_settings.tooltip': "Tous les paramètres concernant le Portail de la Forêt du Crépuscule sont ici.",
    'config.twilightforest.portal_unlocked_by_advancement': "Avancement de déverrouillage du portail",
    'config.twilightforest.portal_unlocked_by_advancement.tooltip': "Utilisez un emplacement de ressource d'avancement valide en tant que chaîne. Par exemple, utiliser \"minecraft:story/mine_diamond\" verrouillera le portail derrière l'avancement \"Diamants !\". Les ID d'avancement invalides/vides laisseront le portail entièrement déverrouillé.",
    'config.twilightforest.portals_in_other_dimensions': "Créer des portails dans d'autres dimensions",
    'config.twilightforest.portals_in_other_dimensions.tooltip': "Permet aux portails vers la Forêt du Crépuscule d'être créés en dehors de la dimension 'd'origine'. Peut être considéré comme un exploit.",
    'config.twilightforest.prettify_ore_meter_gui': "Embellir l'interface du Compteur de Minerais",
    'config.twilightforest.prettify_ore_meter_gui.tooltip': "Aligne les tirets et pourcentages dans l'interface du Compteur de Minerais.",
    'config.twilightforest.ram_indicator': "Indicateur de laine du Bélier des Quêtes",
    'config.twilightforest.ram_indicator.tooltip': "Affiche une coche ou un X au-dessus de votre viseur en tenant de la laine au-dessus du Bélier des Quêtes selon que cette couleur a déjà été donnée ou non.",
    'config.twilightforest.repairing_xp_cost': "Multiplicateur de coût de réparation",
    'config.twilightforest.repairing_xp_cost.tooltip': "Multiplie le coût total en XP pour réparer un objet et arrondit à l'entier supérieur.\nDes valeurs plus élevées signifient que la recette coûtera plus cher à réparer, plus basse signifie moins. Mettez à 0 pour désactiver complètement le coût.",
    'config.twilightforest.screen_offset_x': "Décalage X de l'affichage",
    'config.twilightforest.screen_offset_x.tooltip': "Définit le décalage Y de départ pour tous les modificateurs d'affichage à l'écran.",
    'config.twilightforest.screen_offset_y': "Décalage Y de l'affichage",
    'config.twilightforest.screen_offset_y.tooltip': "Définit le décalage Y de départ pour tous les modificateurs d'affichage à l'écran.",
    'config.twilightforest.screen_scale': "Échelle d'affichage",
    'config.twilightforest.screen_scale.tooltip': "Définit l'échelle de tous les modificateurs d'affichage à l'écran.",
    'config.twilightforest.screen_shake': "Tremblement d'écran du haricot magique",
    'config.twilightforest.screen_shake.tooltip': "Contrôle si l'écran tremble lorsqu'un Haricot Magique est en train de pousser.",
    'config.twilightforest.shapeless_uncrafting': "Décraftage sans forme",
    'config.twilightforest.shapeless_uncrafting.tooltip': "Si vrai, la table de décraftage permettra aussi de décrafter les recettes sans forme.\nLa table était à l'origine destinée à ne prendre que les recettes avec forme, mais cette option reste pour les gens qui souhaitent garder cette fonctionnalité.",
    'config.twilightforest.shield': "Interactions du bouclier",
    'config.twilightforest.shield.tooltip': "Nous recommandons de télécharger le mod Shield Parry pour la parade, mais ces contrôles restent sans.",
    'config.twilightforest.shield_indicator': "Indicateur de bouclier de fortification",
    'config.twilightforest.shield_indicator.tooltip': "Affiche le nombre de boucliers de fortification actuellement actifs sur votre joueur au-dessus de votre barre d'armure.\n\"Désactivez ceci si d'autres mods rendent au-dessus/en-dessous.",
    'config.twilightforest.shield_indicator_creative': "Indicateur de bouclier de fortification (créatif)",
    'config.twilightforest.shield_indicator_creative.tooltip': "Active l'indicateur de bouclier de fortification en mode créatif pour le débogage.",
    'config.twilightforest.silent_cicadas': "Cigales silencieuses",
    'config.twilightforest.silent_cicadas.tooltip': "Rend les Cigales silencieuses pour ceux qui ont des problèmes de bibliothèque sonore ou les trouvent agaçantes.",
    'config.twilightforest.silent_cicadas_on_head': "Cigales silencieuses sur la tête",
    'config.twilightforest.silent_cicadas_on_head.tooltip': "Rend les Cigales silencieuses quand elles sont sur votre tête. Si l'option ci-dessus est à vrai, ceci n'aura aucun effet.",
    'config.twilightforest.sorting_range': "Portée de l'Arbre de Tri",
    'config.twilightforest.sorting_range.tooltip': "Définit le rayon auquel le Cœur de Bois de Tri fonctionne. Peut être un nombre entre 1 et 128.\nMettez à 0 pour empêcher le Cœur de Bois de Tri de fonctionner.",
    'config.twilightforest.spawn_in_tf': "Apparaître dans la Forêt du Crépuscule",
    'config.twilightforest.spawn_in_tf.tooltip': "Si vrai, les joueurs apparaissant pour la première fois apparaîtront dans la Forêt du Crépuscule.",
    'config.twilightforest.time_range': "Portée de l'Arbre du Temps",
    'config.twilightforest.time_range.tooltip': "Définit le rayon auquel le Cœur de Bois du Temps fonctionne. Peut être un nombre entre 1 et 128.\nMettez à 0 pour empêcher le Cœur de Bois du Temps de fonctionner.",
    'config.twilightforest.totem_charm_animation': "Animation de Charme de Totem d'Immortalité",
    'config.twilightforest.totem_charm_animation.tooltip': "Fait que les Charmes activés s'affichent comme le Totem d'Immortalité au lieu de nos propres effets.",
    'config.twilightforest.transformation_range': "Portée de l'Arbre de Transformation",
    'config.twilightforest.transformation_range.tooltip': "Définit le rayon auquel le Cœur de Transformation fonctionne. Peut être un nombre entre 1 et 128.\nMettez à 0 pour empêcher le Cœur de Transformation de fonctionner.",
    'config.twilightforest.twenty_four_hour_format': "Format 24 heures",
    'config.twilightforest.twenty_four_hour_format.tooltip': "Si activé, l'amélioration d'horloge affiche l'heure au format 24 heures au lieu du format 12 heures.",
    'config.twilightforest.uncrafting': "Table de décraftage",
    'config.twilightforest.uncrafting.tooltip': "Paramètres pour tout ce qui concerne la Table de Décraftage.",
    'config.twilightforest.uncrafting_mod_id_flip': "Liste noire d'ID de mod",
    'config.twilightforest.uncrafting_mod_id_flip.tooltip': "Si vrai, ceci inversera l'option ci-dessus d'une liste noire à une liste blanche.",
    'config.twilightforest.uncrafting_mod_ids': "ID de mod désactivés",
    'config.twilightforest.uncrafting_mod_ids.tooltip': "Ici, vous pouvez désactiver tous les objets de certains mods d'être décraftés.\nEntrez un ID de mod valide pour désactiver toutes les recettes de décraftage de ce mod.\nExemple : \"twilightforest\" désactivera toutes les recettes de décraftage de ce mod.",
    'config.twilightforest.uncrafting_recipes': "Recettes désactivées",
    'config.twilightforest.uncrafting_recipes.tooltip': "Si vous ne voulez pas désactiver le décraftage entièrement, et préférez désactiver certaines recettes, c'est pour vous.\nPour ajouter une recette, ajoutez l'ID du mod suivi du nom de la recette. Vous pouvez le vérifier dans des choses comme JEI.\nExemple : \"twilightforest:firefly_particle_spawner\" désactivera le décraftage du générateur de particules en pot de luciole, luciole et coquelicot.\nSi un objet a plusieurs recettes de craftage et que vous voulez toutes les désactiver, ajoutez l'objet au tag d'objet \"twilightforest:banned_uncraftables\".\nSi vous avez un ingrédient problématique, comme le bois de tour infesté par exemple, ajoutez l'objet au tag d'objet \"twilightforest:banned_uncrafting_ingredients\".",
    'config.twilightforest.uncrafting_recipes_flip': "Liste noire de recettes",
    'config.twilightforest.uncrafting_recipes_flip.tooltip': "Si vrai, ceci inversera la liste de recettes de décraftage ci-dessus d'une liste noire à une liste blanche.",
    'config.twilightforest.uncrafting_xp_cost': "Multiplicateur de coût de décraftage",
    'config.twilightforest.uncrafting_xp_cost.tooltip': "Multiplie le coût total en XP pour décrafter un objet et arrondit à l'entier supérieur.\nDes valeurs plus élevées signifient que la recette coûtera plus cher à décrafter, plus basse signifie moins. Mettez à 0 pour désactiver complètement le coût.\nNotez que ceci n'affecte que les recettes de craftage inversées, les recettes de décraftage utiliseront toujours le coût normal.",

    # ==== BLOCKS ====
    'block.twilightforest.antibuilder': "Anti-constructeur",
    'block.twilightforest.antibuilt_block': "Bloc Anti-construit",
    'block.twilightforest.arctic_fur_block.desc': "Réduit les dégâts de chute de 90 %",
    'block.twilightforest.brazier': "Brasero",
    'block.twilightforest.built_block': "Bloc Construit",
    'block.twilightforest.casket.locked': "Ce cercueil ne peut être ouvert que par %s !",
    'block.twilightforest.chipped_keepsake_casket': "Cercueil Souvenir ébréché",
    'block.twilightforest.cinder_wood': "Bois de cendres",
    'block.twilightforest.creeper_wall_skull_candle': "Bougie de crâne de creeper murale",
    'block.twilightforest.damaged_keepsake_casket': "Cercueil Souvenir endommagé",
    'block.twilightforest.dark_tower_miniature_structure': "Tour Sombre miniature",
    'block.twilightforest.dark_wood': "Bois sombre",
    'block.twilightforest.fake_diamond': "Bloc de diamant",
    'block.twilightforest.fake_gold': "Bloc d'or",
    'block.twilightforest.final_boss_boss_spawner': "Générateur de boss final",
    'block.twilightforest.hardened_dark_leaves': "Feuilles épaisses de bois sombre",
    'block.twilightforest.knightmetal_block.desc': "Inflige de forts dégâts au contact",
    'block.twilightforest.lich_tower_miniature_structure': "Tour de la Liche miniature",
    'block.twilightforest.minotaur_labyrinth_miniature_structure': "Labyrinthe du Minotaure miniature",
    'block.twilightforest.naga_courtyard_miniature_structure': "Cour du Naga miniature",
    'block.twilightforest.ominous_fire': "Feu inquiétant",
    'block.twilightforest.piglin_wall_skull_candle': "Bougie de crâne de piglin murale",
    'block.twilightforest.player_skull_candle.named': "Tête de %s avec Bougies",
    'block.twilightforest.player_wall_skull_candle': "Bougie de crâne de joueur murale",
    'block.twilightforest.potted_canopy_sapling': "Pousse de canopée en pot",
    'block.twilightforest.potted_darkwood_sapling': "Pousse de bois sombre en pot",
    'block.twilightforest.potted_dead_thorn': "Épine brûlée en pot",
    'block.twilightforest.potted_fiddlehead': "Crosse de fougère en pot",
    'block.twilightforest.potted_green_thorn': "Épine verte en pot",
    'block.twilightforest.potted_hollow_oak_sapling': "Pousse de chêne du Crépuscule robuste en pot",
    'block.twilightforest.potted_mangrove_sapling': "Pousse de palétuvier en pot",
    'block.twilightforest.potted_mayapple': "Podophylle en pot",
    'block.twilightforest.potted_mining_sapling': "Pousse de l'Arbre du Mineur en pot",
    'block.twilightforest.potted_mushgloom': "Mushgloom en pot",
    'block.twilightforest.potted_rainbow_oak_sapling': "Pousse de chêne arc-en-ciel en pot",
    'block.twilightforest.potted_sorting_sapling': "Pousse de l'Arbre de Tri en pot",
    'block.twilightforest.potted_thorn': "Épine en pot",
    'block.twilightforest.potted_time_sapling': "Pousse de l'Arbre du Temps en pot",
    'block.twilightforest.potted_transformation_sapling': "Pousse de l'Arbre de Transformation en pot",
    'block.twilightforest.potted_twilight_oak_sapling': "Pousse de chêne du Crépuscule maladive en pot",
    'block.twilightforest.reactor_debris': "Débris de réacteur",
    'block.twilightforest.skeleton_skull_candle': "Bougie de crâne de squelette",
    'block.twilightforest.skeleton_wall_skull_candle': "Bougie de crâne de squelette murale",
    'block.twilightforest.stripped_dark_log': "Bûche de bois sombre écorcée",
    'block.twilightforest.twilight_portal_miniature_structure': "Portail de la Forêt du Crépuscule miniature",
    'block.twilightforest.unbreakable_vanishing_block': "Bloc Disparaissant",
    'block.twilightforest.uncrafting_table.disabled': "Ce bloc a été désactivé.",
    'block.twilightforest.wither_skeleton_wall_skull_candle': "Bougie de crâne de Wither Skeleton murale",
    'block.twilightforest.wrought_iron_fence.cap': "Shift + clic droit sur le même bloc pour placer un fleuron",
    'block.twilightforest.zombie_wall_skull_candle': "Bougie de crâne de zombie murale",

    # ==== ITEMS ====
    'item.twilightforest.adherent_spawn_egg': "Œuf d'apparition d'adhérent",
    'item.twilightforest.alpha_yeti_banner_pattern.desc': "Visage du Yéti Alpha",
    'item.twilightforest.arctic_armor.desc': "Teignable",
    'item.twilightforest.boarkchop': "Côtelette de sanglier crue",
    'item.twilightforest.emperors_cloth.desc': "Voilé",
    'item.twilightforest.fiery_armor.desc': "Brûle les attaquants",
    'item.twilightforest.fiery_pickaxe.desc': "Auto-fonte",
    'item.twilightforest.fiery_sword.desc': "Brûle les cibles",
    'item.twilightforest.flask.empty': "Vide",
    'item.twilightforest.flask.empty_description': "Peut contenir plusieurs doses de potion",
    'item.twilightforest.flask.no_refill': "Ne peut pas être remplie",
    'item.twilightforest.four_leaf_clover': "Trèfle à quatre feuilles",
    'item.twilightforest.giant_pickaxe.desc': "Casse les blocs géants",
    'item.twilightforest.glass_sword.desc': "Mode créatif uniquement",
    'item.twilightforest.harbinger_cube_spawn_egg': "Œuf d'apparition de Cube Précurseur",
    'item.twilightforest.hydra_banner_pattern.desc': "Flamme d'Hydre",
    'item.twilightforest.knight_phantom_banner_pattern.desc': "Casque de Chevalier",
    'item.twilightforest.knightmetal_axe.desc': "Dégâts supplémentaires aux cibles non blindées",
    'item.twilightforest.knightmetal_pickaxe.desc': "Dégâts supplémentaires aux cibles blindées",
    'item.twilightforest.knightmetal_sword.desc': "Dégâts supplémentaires aux cibles blindées",
    'item.twilightforest.lich_banner_pattern.desc': "Couronne de la Liche",
    'item.twilightforest.magic_painting': "Tableau magique",
    'item.twilightforest.maze_map.y_level': "Niveau Y %s",
    'item.twilightforest.minoshroom_banner_pattern.desc': "Haches du Minoshroom",
    'item.twilightforest.minotaur_axe.desc': "Dégâts supplémentaires lors de la charge",
    'item.twilightforest.moon_dial.phase_0': "Pleine Lune",
    'item.twilightforest.moon_dial.phase_1': "Lune gibbeuse décroissante",
    'item.twilightforest.moon_dial.phase_2': "Dernier quartier",
    'item.twilightforest.moon_dial.phase_3': "Dernier croissant",
    'item.twilightforest.moon_dial.phase_4': "Nouvelle Lune",
    'item.twilightforest.moon_dial.phase_5': "Premier croissant",
    'item.twilightforest.moon_dial.phase_6': "Premier quartier",
    'item.twilightforest.moon_dial.phase_7': "Lune gibbeuse croissante",
    'item.twilightforest.moon_dial.phase_unknown': "Phase de lune indéterminée",
    'item.twilightforest.moon_dial.phase_unknown_fools': "404 lune introuvable",
    'item.twilightforest.moonworm_queen.jei_info_message': "Les Baies-Torches restaurent 64 de durabilité chacune",
    'item.twilightforest.naga_banner_pattern.desc': "Écailles de Naga",
    'item.twilightforest.phantom_armor.desc': "Jamais perdue à la mort",
    'item.twilightforest.pocket_watch.desc': "Elle semble toujours en retard",
    'item.twilightforest.quest_ram_banner_pattern.desc': "Spirales du Bélier des Quêtes",
    'item.twilightforest.scepter.desc': "%s charges restantes",
    'item.twilightforest.shika_senbei': "Shika Senbei",
    'item.twilightforest.skull_candle.desc': "A : %s Bougie %s",
    'item.twilightforest.skull_candle.desc.multiple': "A : %s Bougies %s",
    'item.twilightforest.snow_queen_banner_pattern.desc': "Flocon de neige",
    'item.twilightforest.stale_bread': "Pain rassis",
    'item.twilightforest.travellers_gloves.desc': "Cosmétique",
    'item.twilightforest.triple_bow': "Tri-Arc",
    'item.twilightforest.ur_ghast_banner_pattern.desc': "Bordure Carminite",
    'item.twilightforest.yeti_armor.desc': "Refroidit les attaquants",

    # ==== TRAVELLERS GEAR MODIFIERS ====
    'travellers_gear.modifier.twilightforest.agile_ranger': "Ranger Agile",
    'travellers_gear.modifier.twilightforest.agile_ranger.description': "Permet un mouvement normal lors de l'utilisation d'objets de type arc",
    'travellers_gear.modifier.twilightforest.all_night_goggles': "Lunettes Nocturnes",
    'travellers_gear.modifier.twilightforest.all_night_goggles.description': "Empêche l'insomnie et l'agression de l'Enderman",
    'travellers_gear.modifier.twilightforest.aquatic_agility': "Agilité Aquatique",
    'travellers_gear.modifier.twilightforest.aquatic_agility.description': "Respiration et Affinité aquatique en un",
    'travellers_gear.modifier.twilightforest.arrow_magnetism': "Magnétisme à Flèches",
    'travellers_gear.modifier.twilightforest.arrow_magnetism.description': "Récupère les flèches manquées",
    'travellers_gear.modifier.twilightforest.auto_repair': "Auto-Réparation",
    'travellers_gear.modifier.twilightforest.auto_repair.description': "Répare la durabilité avec le temps",
    'travellers_gear.modifier.twilightforest.double_jump': "Double Saut",
    'travellers_gear.modifier.twilightforest.double_jump.description': "Vous permet de faire un second saut en l'air",
    'travellers_gear.modifier.twilightforest.efficient_eater': "Mangeur Efficient",
    'travellers_gear.modifier.twilightforest.efficient_eater.description': "Réduit la perte de faim due au mouvement",
    'travellers_gear.modifier.twilightforest.gradual_glide': "Plané Graduel (s'accroupir pour activer)",
    'travellers_gear.modifier.twilightforest.gradual_glide.description': "Permet de planer dans les airs",
    'travellers_gear.modifier.twilightforest.haste': "Hâte",
    'travellers_gear.modifier.twilightforest.haste.description': "Confère Hâte II",
    'travellers_gear.modifier.twilightforest.high_jump': "Saut en Hauteur",
    'travellers_gear.modifier.twilightforest.item_display': "Affichage d'Objet (raccourci : ${tfkeybinds/key.twilightforest.item_display_map_cycle})",
    'travellers_gear.modifier.twilightforest.item_display.clock.unknown': "Heure inconnue",
    'travellers_gear.modifier.twilightforest.item_display.compass.lodestone': "%s (à %s blocs)",
    'travellers_gear.modifier.twilightforest.item_display.description': "Clic droit sur les objets dans les Lunettes pour ajouter des affichages",
    'travellers_gear.modifier.twilightforest.perfect_dodge': "Esquive Parfaite",
    'travellers_gear.modifier.twilightforest.perfect_dodge.description': "30 % de chance d'esquiver les projectiles",
    'travellers_gear.modifier.twilightforest.red_thread_vision': "Vision du Fil Rouge (raccourci : ${tfkeybinds/key.twilightforest.red_thread_vision})",
    'travellers_gear.modifier.twilightforest.red_thread_vision.description': "Permet de voir le Fil Rouge placé",
    'travellers_gear.modifier.twilightforest.side_step': "Pas de Côté",
    'travellers_gear.modifier.twilightforest.side_step.description': "Double-tap %s ou %s pour effectuer un dash",
    'travellers_gear.modifier.twilightforest.slimy_soles': "Semelles Visqueuses",
    'travellers_gear.modifier.twilightforest.slimy_soles.description': "Empêche les dégâts de chute en vous faisant rebondir",
    'travellers_gear.modifier.twilightforest.stealth': "Furtivité (s'accroupir pour activer)",
    'travellers_gear.modifier.twilightforest.stealth.description': "S'accroupir pour devenir invisible",
    'travellers_gear.modifier.twilightforest.step_up': "Marche en Hauteur",
    'travellers_gear.modifier.twilightforest.straight_ahead': "Tout Droit",
    'travellers_gear.modifier.twilightforest.straight_ahead.description': "Augmente la vitesse de déplacement vers l'avant",
    'travellers_gear.modifier.twilightforest.swap_hotbar': "Échanger la Barre d'Outils (raccourci : ${tfkeybinds/key.twilightforest.swap_hotbar})",
    'travellers_gear.modifier.twilightforest.swap_hotbar.description': "Permet de stocker et récupérer votre barre d'outils",
    'travellers_gear.modifier.twilightforest.swap_hotbar_ability': "Échanger la Barre d'Outils (raccourci : ${tfkeybinds/key.twilightforest.swap_hotbar})",
    'travellers_gear.modifier.twilightforest.swift_swim': "Nage Rapide",
    'travellers_gear.modifier.twilightforest.unrestrained': "Libre",
    'travellers_gear.modifier.twilightforest.unrestrained.description': "Empêche les blocs de vous ralentir",
    'travellers_gear.modifier.twilightforest.water_walk': "Marche sur l'Eau",
    'travellers_gear.modifier.twilightforest.water_walk.description': "Vous permet de marcher sur l'eau",
    'travellers_gear.modifier.twilightforest.zoom': "Zoom (raccourci : ${tfkeybinds/key.twilightforest.zoom})",

    # ==== STRUCTURES ====
    'structure.twilightforest.aurora_palace': "Palais d'Aurore",
    'structure.twilightforest.dark_tower': "Tour Sombre",
    'structure.twilightforest.final_castle': "Château du Plateau Final",
    'structure.twilightforest.hedge_maze': "Labyrinthe de Haies",
    'structure.twilightforest.hydra_lair': "Antre de l'Hydre",
    'structure.twilightforest.knight_stronghold': "Forteresse des Chevaliers",
    'structure.twilightforest.labyrinth': "Labyrinthe du Minotaure",
    'structure.twilightforest.large_hollow_hill': "Grande Colline Creuse",
    'structure.twilightforest.lich_tower': "Tour de la Liche",
    'structure.twilightforest.medium_hollow_hill': "Colline Creuse Moyenne",
    'structure.twilightforest.mushroom_tower': "Château des Champignons",
    'structure.twilightforest.naga_courtyard': "Cour du Naga",
    'structure.twilightforest.quest_grove': "Bosquet des Quêtes",
    'structure.twilightforest.small_hollow_hill': "Petite Colline Creuse",
    'structure.twilightforest.troll_cave': "Grotte des Trolls",
    'structure.twilightforest.yeti_cave': "Antre du Yéti",

    # ==== COMMANDS ====
    'commands.tffeature.ability_modifier': "Les capacités ne peuvent pas être ajoutées ou retirées de l'équipement de voyageur",
    'commands.tffeature.added_modifier': "%s ajouté à %s !",
    'commands.tffeature.biomepng.counts_header': "Comptes approximatifs de blocs de biome dans une région %sx%s",
    'commands.tffeature.biomepng.progress': "%s%% terminé de la cartographie",
    'commands.tffeature.biomepng.save_failed': "Impossible d'enregistrer l'image ! Veuillez signaler ceci !",
    'commands.tffeature.biomepng.save_success': "Image enregistrée !",
    'commands.tffeature.display_pieces.missing_key': "clé manquante",
    'commands.tffeature.generator_radius.center_chunk': "Chunk central de la structure",
    'commands.tffeature.generator_radius.radius': "Rayon depuis le chunk central : %s",
    'commands.tffeature.has_modifier': "Cette pièce d'équipement de voyageur a déjà %s",
    'commands.tffeature.info.wip': "Cette commande est encore en cours de développement, certaines choses peuvent être cassées.",
    'commands.tffeature.invalid_modifier': "%s n'est pas un modificateur d'équipement de voyageur valide",
    'commands.tffeature.no_modifier': "%s n'est pas appliqué à cette pièce d'équipement de voyageur",
    'commands.tffeature.not_player': "Cette commande doit être exécutée par un joueur valide !",
    'commands.tffeature.not_travellers_gear': "Vous ne tenez pas de pièce d'équipement de voyageur",
    'commands.tffeature.removed_modifier': "%s retiré de %s !",
    'commands.tffeature.structure.boundaries': "Limites de la structure : %s",
    'commands.tffeature.teleport.dimension_missing': "La dimension Forêt du Crépuscule est indisponible.",
    'commands.tffeature.teleport.player_only': "La commande doit être exécutée par un joueur.",
    'commands.tffeature.teleport.success': "Téléporté à la Forêt du Crépuscule à %s %s %s",
    'commands.tffeature.too_many_modifiers': "Cette pièce d'équipement de voyageur a déjà le nombre maximum de modificateurs",
    'commands.tffeature.usage': "/%s <info | reactivate | conquer | center>",
    'commands.tffeature.wrong_modifier_slot': "%s n'est pas autorisé sur cette pièce d'équipement de voyageur",

    # ==== MISC ====
    'misc.twilightforest.advancement_hidden': "<Avancement caché>",
    'misc.twilightforest.advancement_required': "Avancement requis :",
    'misc.twilightforest.biome_locked': "Biome verrouillé !",
    'misc.twilightforest.biome_locked_2': "Vérifiez vos avancements",
    'misc.twilightforest.core_disabled': "%s est désactivé via la configuration",
    'misc.twilightforest.firefly_spawner_radius': "Rayon des particules de luciole : %s blocs",
    'misc.twilightforest.magic_map_fail': "La magie a faibli. Peut-être qu'elle ne fonctionne pas ici ?",
    'misc.twilightforest.ore_meter_header_block': "Bloc",
    'misc.twilightforest.ore_meter_header_count': "Nombre",
    'misc.twilightforest.ore_meter_header_ratio': "Ratio",
    'misc.twilightforest.ore_meter_loading': "Chargement",
    'misc.twilightforest.ore_meter_new_range': "Portée définie à %s chunks",
    'misc.twilightforest.ore_meter_no_blocks': "Aucun bloc trouvé à proximité",
    'misc.twilightforest.ore_meter_range': "Rayon : %s, Origine : [%s, %s]",
    'misc.twilightforest.ore_meter_ratio': "(%s%%)",
    'misc.twilightforest.ore_meter_separator': "-",
    'misc.twilightforest.ore_meter_set_block': "Bloc ciblé défini sur %s",
    'misc.twilightforest.ore_meter_targeted_block': "Bloc ciblé : %s",
    'misc.twilightforest.ore_meter_total': "Total des blocs scannés : %s",
    'misc.twilightforest.pedestal_ineligible': "Vous êtes indigne.",
    'misc.twilightforest.portal_unsafe': "Cela ne semble pas sûr ici...",
    'misc.twilightforest.portal_unworthy': "Le bassin du Portail ne répond pas. Peut-être quelque chose a-t-il été négligé ?",
    'misc.twilightforest.wip': "Cette fonctionnalité est en cours de développement et peut avoir des bugs ou des effets non intentionnels qui pourraient endommager votre monde",

    # ==== ENTITIES ====
    'entity.twilightforest.adherent': "Adhérent",
    'entity.twilightforest.chain_block': "Bloc et Chaîne",
    'entity.twilightforest.charm_effect': "Effet de Charme",
    'entity.twilightforest.cube_of_annihilation': "Cube d'Annihilation",
    'entity.twilightforest.falling_ice': "Glace Tombante",
    'entity.twilightforest.harbinger_cube': "Cube Précurseur",
    'entity.twilightforest.hydra_mortar': "Mortier d'Hydre",
    'entity.twilightforest.ice_arrow': "Flèche de Glace",
    'entity.twilightforest.ice_snowball': "Boule de Neige Givrée",
    'entity.twilightforest.knight_phantom.plural': "Chevaliers Fantômes",
    'entity.twilightforest.lich_bolt': "Éclair de la Liche",
    'entity.twilightforest.lich_bomb': "Éclair Explosif de la Liche",
    'entity.twilightforest.magic_painting': "Tableau Magique",
    'entity.twilightforest.moonworm_shot': "Ver de Lune",
    'entity.twilightforest.nature_bolt': "Éclair de Nature",
    'entity.twilightforest.protection_box': "Boîte de Protection de Progression",
    'entity.twilightforest.rising_zombie': "Zombie",
    'entity.twilightforest.roving_cube': "Cube Errant",
    'entity.twilightforest.seeker_arrow': "Flèche Chercheuse",
    'entity.twilightforest.slider': "Piège Coulissant Mobile",
    'entity.twilightforest.slime_blob': "Boule de Slime",
    'entity.twilightforest.thrown_block': "Bloc Lancé",
    'entity.twilightforest.thrown_ice': "Bombe de Glace",
    'entity.twilightforest.thrown_wep': "Arme Lancée",
    'entity.twilightforest.tome_bolt': "Éclair de Tome de Mort",
    'entity.twilightforest.wand_bolt': "Éclair du Sceptre du Crépuscule",

    # ==== TRIM MATERIALS ====
    'trim_material.twilightforest.carminite': "Matériau de garniture en carminite",
    'trim_material.twilightforest.fiery': "Matériau de garniture ardent",
    'trim_material.twilightforest.ironwood': "Matériau de garniture en bois de fer",
    'trim_material.twilightforest.knightmetal': "Matériau de garniture en métal des chevaliers",
    'trim_material.twilightforest.naga_scale': "Matériau de garniture en écaille de Naga",
    'trim_material.twilightforest.steeleaf': "Matériau de garniture en feuille d'acier",

    # ==== BOOK ====
    'twilightforest.book.author': "un explorateur oublié",
    'twilightforest.book.darktower': "Notes sur une Tour de Bois",
    'twilightforest.book.hydralair': "Notes sur le Marécage de Feu",
    'twilightforest.book.hydralair.1': "§8[[Le carnet d'un explorateur, écrit sur du papier ignifuge]]§0\n\nLe feu est un obstacle trivial pour un maître explorateur tel que moi. J'ai traversé des mers de feu, et nagé dans des océans de lave. L'air brûlant ici est une variation intéressante, mais",
    'twilightforest.book.hydralair.2': "finalement aucun obstacle.\n\nCe qui m'arrête cependant, c'est que j'ai rencontré un autre sortilège de protection, cette fois entourant une puissante créature qui doit être le roi de ce marécage de feu. Ce n'est pas le premier sortilège de protection que je rencontre, et je",
    'twilightforest.book.hydralair.3': "commence à percer les mystères de leur fonctionnement.\n\nSi ce sortilège est comme les autres, il sera maintenu par une puissante créature à proximité. Autour du marécage de feu, il y a plusieurs marécages humides, et sous ces marécages se trouvent des labyrinthes pleins de minotaures.",
    'twilightforest.book.hydralair.4': "Le choix logique pour lier un tel sortilège serait une sorte de minotaure puissant, différent d'une certaine manière des autres qui l'entourent...",
    'twilightforest.book.icetower': "Notes sur la Fortification Aurorale",
    'twilightforest.book.icetower.1': "§8[[Le carnet d'un explorateur, recouvert de glace]]§0\n\nJ'ai surmonté un blizzard, pour rencontrer cette terrible tempête de glace au sommet du glacier. Mes explorations m'ont montré la splendeur d'un palais de glace, brillant des couleurs de",
    'twilightforest.book.icetower.2': "l'aurore polaire. Tout cela semble protégé par une sorte de malédiction.\n\n§8[[Entrée suivante]]§0\n\nJe ne suis pas novice. Cette malédiction est alimentée par le pouvoir d'une créature à proximité. La cause de la malédiction entourant le marécage de feu était construite sur le pouvoir du",
    'twilightforest.book.icetower.3': "chef des minotaures à proximité.\n\nAutour de ce glacier, il y a des masses de yétis. Peut-être que les yétis ont une sorte de chef...",
    'twilightforest.book.labyrinth': "Notes sur un Labyrinthe Marécageux",
    'twilightforest.book.labyrinth.1': "§8[[Le carnet d'un explorateur, écrit sur du papier imperméable]]§0\n\nLes moustiques de ce marécage sont vexants, mais étranges. La grande majorité d'entre eux ne semble avoir aucune source naturelle, ni aucun rôle dans l'écologie locale. J'ai commencé à soupçonner qu'ils sont",
    'twilightforest.book.labyrinth.2': "une sorte de malédiction magique.\n\n§8[[Entrée suivante]]§0\n\nMaintenant que j'ai rencontré un sortilège de protection sur le labyrinthe en ruines ici, je considère mes soupçons confirmés. Le sortilège de protection et les moustiques sont une",
    'twilightforest.book.labyrinth.3': "malédiction. Cette malédiction semble avoir une source différente des autres que j'ai rencontrées. Je devrai faire plus de recherches...\n\n§8[[Entrée suivante]]§0\n\nLa malédiction semble être d'un type trop puissant pour qu'un seul être puisse",
    'twilightforest.book.labyrinth.4': "produire. Plusieurs sorciers travaillant en combinaison seraient nécessaires.\n\nSi l'un des sorciers cessait de contribuer, l'ensemble de la malédiction sur tout le marécage tomberait. Étrangement, mes divinations ne montrent aucun signe de sorciers vivants à proximité.",
    'twilightforest.book.labyrinth.5': "J'ai vu quelque chose d'intéressant dans une des tours à toit pointu à proximité...",
    'twilightforest.book.lichtower': "Notes sur une Tour Pointue",
    'twilightforest.book.lichtower.1': "§8[Le carnet d'un explorateur, mâchouillé par des monstres]§0\n\nJ'ai commencé à examiner l'aura étrange entourant cette tour. Les briques de la tour sont protégées par une malédiction, plus puissante que toute celle que j'ai vue auparavant. La magie de la malédiction émane dans",
    'twilightforest.book.lichtower.2': "la zone environnante.\n\nDans mon pays natal, j'aurais de nombreuses options pour gérer cette magie, mais ici mes ressources sont limitées. Je devrai faire des recherches...",
    'twilightforest.book.lichtower.3': "§8[[Plusieurs entrées plus tard]]§0\n\nUne percée ! Lors de mes voyages, j'ai aperçu un énorme monstre serpentiforme dans une cour décorée. À proximité, j'ai ramassé une écaille verte usée et abandonnée.\n\nLa magie de l'écaille semble avoir les propriétés brise-malédiction",
    'twilightforest.book.lichtower.4': "dont j'ai besoin, mais la magie est trop faible. Je devrai peut-être acquérir un spécimen plus frais, directement de la créature.",
    'twilightforest.book.tfstronghold': "Notes sur une Forteresse",
    'twilightforest.book.tfstronghold.1': "§8[[Le carnet d'un explorateur, écrit sur du papier faiblement luminescent]]§0\n\nLes tendrils d'obscurité entourant cette zone ne sont qu'une manifestation d'un sortilège de protection sur toute la forêt sombre. Le sortilège cause la cécité, ce qui est très vexant. J'ai vu plusieurs",
    'twilightforest.book.tfstronghold.2': "choses intéressantes dans la zone et j'aimerais continuer à explorer.\n\n§8[[Entrée suivante]]§0\n\nJ'ai trouvé des ruines dans la forêt sombre. Elles appartiennent à une forteresse, d'un type généralement habité par des chevaliers. Plutôt que des chevaliers, cette forteresse est pleine de",
    'twilightforest.book.tfstronghold.3': "gobelins. Ils portent une armure chevaleresque, mais leur comportement est très peu chevaleresque.\n\n§8[[Entrée suivante]]§0\n\nProfondément dans les ruines, j'ai trouvé un piédestal. Le piédestal semble être d'un type sur lequel les chevaliers placeraient des trophées pour prouver leur force.",
    'twilightforest.book.tfstronghold.4': "Obtenir un sceptre puissant semblerait affaiblir la malédiction sur la forêt sombre, et placer un trophée associé à une créature puissante sur le piédestal accorderait probablement l'accès à la partie principale de la forteresse.",
    'twilightforest.book.trollcave': "Notes sur les Hauts Plateaux",
    'twilightforest.book.trollcave.1': "§8[[Le carnet d'un explorateur, endommagé par l'acide]]§0\n\nIl ne semble y avoir aucun moyen de me protéger de la tempête toxique entourant cette zone. Lors de mes brèves excursions, j'ai aussi rencontré un autre sortilège de protection, similaire aux autres que j'ai",
    'twilightforest.book.trollcave.2': "observés. Le sortilège doit être lié à la tempête toxique d'une certaine manière. Plus de recherches à venir...\n\n§8[[Entrée suivante]]§0\n\nUne telle magie météorologique suprême doit être le résultat de plusieurs grands maux invaincus dans ce monde. Mes études contiennent",
    'twilightforest.book.trollcave.3': "plusieurs indices pointant vers un marécage brûlant, une forêt enveloppée de profondes ténèbres, et un royaume couvert de neige.",
    'twilightforest.book.unknown': "Notes sur l'Inexpliqué",
    'twilightforest.book.unknown.1': "§8[[Ce livre montre des signes d'avoir été copié plusieurs fois]]§0\n\nJe ne peux expliquer le champ entourant cette structure, mais la magie est puissante. Si cette malédiction est comme les autres, alors la réponse pour la déverrouiller se trouve ailleurs. Peut-être qu'il y a quelque chose que j'ai laissé",
    'twilightforest.book.unknown.2': "inachevé, ou un monstre que je dois encore vaincre. Je devrai faire demi-tour. Je reviendrai à cet endroit plus tard, pour voir si quelque chose a changé.",
    'twilightforest.book.yeticave': "Notes sur une Grotte Glacée",
    'twilightforest.book.yeticave.1': "§8[[Le carnet d'un explorateur, couvert de givre]]§0\n\nLe blizzard entourant ces terres enneigées est incessant. Ce n'est pas une chute de neige ordinaire — c'est un phénomène magique. Je devrai mener des expériences pour découvrir ce qui est capable de",
    'twilightforest.book.yeticave.2': "causer un tel effet.\n\n§8[[Entrée suivante]]§0\n\nLa malédiction semble être d'un type trop puissant pour qu'un seul être puisse produire. Plusieurs sorciers travaillant en combinaison seraient nécessaires. Si l'un des sorciers cessait",
    'twilightforest.book.yeticave.3': "de contribuer, le blizzard se calmerait. Étrangement, mes divinations ne montrent aucun signe de sorciers vivants à proximité. J'ai vu quelque chose d'intéressant dans une des tours à toit pointu à proximité...",

    # ==== HOLLOW LOGS (vanilla wood) ====
    'block.twilightforest.hollow_acacia_log_climbable': "Bûche d'acacia creuse",
    'block.twilightforest.hollow_acacia_log_horizontal': "Bûche d'acacia creuse",
    'block.twilightforest.hollow_acacia_log_vertical': "Bûche d'acacia creuse",
    'block.twilightforest.hollow_birch_log_climbable': "Bûche de bouleau creuse",
    'block.twilightforest.hollow_birch_log_horizontal': "Bûche de bouleau creuse",
    'block.twilightforest.hollow_birch_log_vertical': "Bûche de bouleau creuse",
    'block.twilightforest.hollow_canopy_log_climbable': "Bûche de Canopée creuse",
    'block.twilightforest.hollow_canopy_log_horizontal': "Bûche de Canopée creuse",
    'block.twilightforest.hollow_canopy_log_vertical': "Bûche de Canopée creuse",
    'block.twilightforest.hollow_cherry_log_climbable': "Bûche de cerisier creuse",
    'block.twilightforest.hollow_cherry_log_horizontal': "Bûche de cerisier creuse",
    'block.twilightforest.hollow_cherry_log_vertical': "Bûche de cerisier creuse",
    'block.twilightforest.hollow_crimson_stem_climbable': "Tige cramoisie creuse",
    'block.twilightforest.hollow_crimson_stem_horizontal': "Tige cramoisie creuse",
    'block.twilightforest.hollow_crimson_stem_vertical': "Tige cramoisie creuse",
    'block.twilightforest.hollow_dark_log_climbable': "Bûche de bois sombre creuse",
    'block.twilightforest.hollow_dark_log_horizontal': "Bûche de bois sombre creuse",
    'block.twilightforest.hollow_dark_log_vertical': "Bûche de bois sombre creuse",
    'block.twilightforest.hollow_dark_oak_log_climbable': "Bûche de chêne noir creuse",
    'block.twilightforest.hollow_dark_oak_log_horizontal': "Bûche de chêne noir creuse",
    'block.twilightforest.hollow_dark_oak_log_vertical': "Bûche de chêne noir creuse",
    'block.twilightforest.hollow_jungle_log_climbable': "Bûche d'acajou creuse",
    'block.twilightforest.hollow_jungle_log_horizontal': "Bûche d'acajou creuse",
    'block.twilightforest.hollow_jungle_log_vertical': "Bûche d'acajou creuse",
    'block.twilightforest.hollow_mangrove_log_climbable': "Bûche de palétuvier creuse",
    'block.twilightforest.hollow_mangrove_log_horizontal': "Bûche de palétuvier creuse",
    'block.twilightforest.hollow_mangrove_log_vertical': "Bûche de palétuvier creuse",
    'block.twilightforest.hollow_mining_log_climbable': "Bûche de bois minier creuse",
    'block.twilightforest.hollow_mining_log_horizontal': "Bûche de bois minier creuse",
    'block.twilightforest.hollow_mining_log_vertical': "Bûche de bois minier creuse",
    'block.twilightforest.hollow_oak_log_climbable': "Bûche de chêne creuse",
    'block.twilightforest.hollow_oak_log_horizontal': "Bûche de chêne creuse",
    'block.twilightforest.hollow_oak_log_vertical': "Bûche de chêne creuse",
    'block.twilightforest.hollow_sorting_log_climbable': "Bûche de bois de tri creuse",
    'block.twilightforest.hollow_sorting_log_horizontal': "Bûche de bois de tri creuse",
    'block.twilightforest.hollow_sorting_log_vertical': "Bûche de bois de tri creuse",
    'block.twilightforest.hollow_spruce_log_climbable': "Bûche de sapin creuse",
    'block.twilightforest.hollow_spruce_log_horizontal': "Bûche de sapin creuse",
    'block.twilightforest.hollow_spruce_log_vertical': "Bûche de sapin creuse",
    'block.twilightforest.hollow_time_log_climbable': "Bûche de bois du temps creuse",
    'block.twilightforest.hollow_time_log_horizontal': "Bûche de bois du temps creuse",
    'block.twilightforest.hollow_time_log_vertical': "Bûche de bois du temps creuse",
    'block.twilightforest.hollow_transformation_log_climbable': "Bûche de bois de transformation creuse",
    'block.twilightforest.hollow_transformation_log_horizontal': "Bûche de bois de transformation creuse",
    'block.twilightforest.hollow_transformation_log_vertical': "Bûche de bois de transformation creuse",
    'block.twilightforest.hollow_twilight_oak_log_climbable': "Bûche de chêne du Crépuscule creuse",
    'block.twilightforest.hollow_twilight_oak_log_horizontal': "Bûche de chêne du Crépuscule creuse",
    'block.twilightforest.hollow_twilight_oak_log_vertical': "Bûche de chêne du Crépuscule creuse",
    'block.twilightforest.hollow_vangrove_log_climbable': "Bûche de palétuvier creuse",
    'block.twilightforest.hollow_vangrove_log_horizontal': "Bûche de palétuvier creuse",
    'block.twilightforest.hollow_vangrove_log_vertical': "Bûche de palétuvier creuse",
    'block.twilightforest.hollow_warped_stem_climbable': "Tige biscornue creuse",
    'block.twilightforest.hollow_warped_stem_horizontal': "Tige biscornue creuse",
    'block.twilightforest.hollow_warped_stem_vertical': "Tige biscornue creuse",

    # ==== ADDITIONAL DEATH MESSAGES ====
    'death.attack.twilightforest.yeeted': "%1$s a été yeeté pour la dernière fois",
    'death.attack.twilightforest.yeeted.entity': "%1$s a été yeeté pour la dernière fois par %2$s",
    'death.attack.twilightforest.yeeted.item': "%1$s a été yeeté pour la dernière fois par %2$s tenant d'une manière ou d'une autre %3$s",
    'death.attack.twilightforest.lostWords': "%1$s n'a su que dire après avoir été tué par %2$s",
    'death.attack.twilightforest.lostWords.item': "%1$s n'a su que dire après avoir été tué par %2$s avec %3$s",
    'death.attack.twilightforest.haunt': "%1$s a rejoint la hantise du %2$s",
    'death.attack.twilightforest.haunt.player': "%1$s a rejoint la hantise du %2$s en fuyant",
    'death.attack.twilightforest.haunt.item': "%1$s a rejoint la hantise du %2$s après avoir été tué par %3$s",
    'death.attack.twilightforest.hydraBite': "La peau de %1$s a été arrachée par l'Hydre",
    'death.attack.twilightforest.hydraBite.player': "La peau de %1$s a été arrachée par l'Hydre en fuyant %2$s",
    'death.attack.twilightforest.hydraFire': "%1$s a été rôti vivant par l'Hydre",
    'death.attack.twilightforest.hydraFire.player': "%1$s a été rôti vivant par l'Hydre en fuyant %2$s",
    'death.attack.twilightforest.lichBolt': "La visée de la Liche était meilleure que celle de %1$s",
    'death.attack.twilightforest.lichBolt.player': "La Liche et %2$s ont mieux visé que %1$s",
    'death.attack.twilightforest.ominous': "%1$s a été consumé par le feu inquiétant",
    'death.attack.twilightforest.ominousFire': "%1$s a été consumé par le feu inquiétant",
    'death.attack.twilightforest.ominousFire.player': "%1$s a été consumé par le feu inquiétant en fuyant %2$s",
    'death.attack.twilightforest.ominousFire.zombified_player': "%1$s a été tué par les restes zombifiés de %2$s",
    'death.attack.twilightforest.ominousFire.zombified_player.self': "%1$s a été tué par ses propres restes zombifiés",
    'death.attack.twilightforest.oreberry': "%1$s a été poignardé à mort par un buisson de baies de minerai",
    'death.attack.twilightforest.oreberry.player': "%1$s a été poignardé à mort par un buisson de baies de minerai en fuyant %2$s",
    'death.attack.twilightforest.squish': "%1$s a été écrasé par la Reine des Neiges",
    'death.attack.twilightforest.squish.player': "%1$s a été écrasé par la Reine des Neiges en fuyant %2$s",
    'death.attack.twilightforest.thorns': "%1$s a marché dans des épines",
    'death.attack.twilightforest.thorns.player': "%1$s a marché dans des épines en fuyant %2$s",
    'death.attack.twilightforest.thrownAxe': "%1$s a été décapité par une hache lancée",
    'death.attack.twilightforest.thrownAxe.player': "%1$s a été décapité par une hache lancée en fuyant %2$s",
    'death.attack.twilightforest.thrownBlock': "%1$s a été écrasé par un bloc lancé",
    'death.attack.twilightforest.thrownBlock.player': "%1$s a été écrasé par un bloc lancé en fuyant %2$s",
    'death.attack.twilightforest.thrownPickaxe': "%1$s a été décapité par une pioche lancée",
    'death.attack.twilightforest.thrownPickaxe.player': "%1$s a été décapité par une pioche lancée en fuyant %2$s",
    'death.attack.twilightforest.slider': "%1$s a été tranché par un Piège Coulissant",
    'death.attack.twilightforest.slider.player': "%1$s a été tranché par un Piège Coulissant en fuyant %2$s",
    'death.attack.twilightforest.ghastTear': "%1$s a été ébouillanté par les larmes ardentes",
    'death.attack.twilightforest.ghastTear.player': "%1$s a été ébouillanté par les larmes ardentes en fuyant %2$s",
    'death.attack.twilightforest.knightmetal': "%1$s a été embroché par un bloc de Métal des Chevaliers",
    'death.attack.twilightforest.knightmetal.player': "%1$s a été embroché par un bloc de Métal des Chevaliers en fuyant %2$s",
    'death.attack.twilightforest.frozen': "%1$s a été gelé par %2$s avec une Bombe de Glace",
    'death.attack.twilightforest.frozen.player': "%1$s a été gelé par %2$s avec une Bombe de Glace en fuyant %3$s",
    'death.attack.twilightforest.frozen.item': "%1$s a été gelé par %2$s avec %3$s",
    'death.attack.twilightforest.leafBrain': "Le cerveau de %1$s a été transformé en feuilles par %2$s",
    'death.attack.twilightforest.leafBrain.player': "Le cerveau de %1$s a été transformé en feuilles par %2$s en fuyant %3$s",
    'death.attack.twilightforest.leafBrain.item': "Le cerveau de %1$s a été transformé en feuilles par %2$s avec %3$s",
    'death.attack.twilightforest.lifedrain': "La vie de %1$s a été drainée par %2$s",
    'death.attack.twilightforest.lifedrain.player': "La vie de %1$s a été drainée par %2$s en fuyant %3$s",
    'death.attack.twilightforest.lifedrain.item': "La vie de %1$s a été drainée par %2$s avec %3$s",
    'death.attack.twilightforest.moonworm': "%1$s a été tiré par un Ver de Lune",
    'death.attack.twilightforest.moonworm.player': "%1$s a été tiré par un Ver de Lune en fuyant %2$s",
    'death.attack.twilightforest.spiked': "%1$s a été embroché par %2$s",
    'death.attack.twilightforest.spiked.player': "%1$s a été embroché par %2$s en fuyant %3$s",
    'death.attack.twilightforest.spiked.item': "%1$s a été embroché par %2$s avec %3$s",
    'death.attack.twilightforest.stale_sandwich': "%1$s a été transformé en sandwich rassis par %2$s",
    'death.attack.twilightforest.stale_sandwich.player': "%1$s a été transformé en sandwich rassis par %2$s en fuyant %3$s",
    'death.attack.twilightforest.expired': "La vie de %1$s a expiré",
    'death.attack.twilightforest.expired.player': "La vie de %1$s a expiré",

    # ==== ADDITIONAL GUI / MISC ====
    'gui.twilightforest.progression_end.title': "Fin de la progression",
    'gui.twilightforest.progression_end.message': "C'est ici la fin de la progression pour le moment. Le Château Final qui attend sur le plateau est encore inachevé et en cours de développement.",
    'gui.twilightforest.optifine.suggestions': "Voici une sélection de mods que nous recommandons d'utiliser à la place.",
    'gui.twilightforest.ominous_fire_jei': "Feu inquiétant",
    'advancement.twilightforest.progression_end': "Fin du voyage",
    'advancement.twilightforest.progression_end.desc': "Tout ce qui se trouve au-delà de ce point dans les Hauts Plateaux est en cours de développement. Cela sera terminé à l'avenir.",
    'container.twilightforest.uncrafting_table.disabled_item': "Le décraftage de cet objet est désactivé.",

    # ==== MAGIC PAINTINGS additional ====
    'magic_painting.twilightforest.music_in_the_mire.title': "Musique dans la fange",
    'magic_painting.twilightforest.music_in_the_mire.author': "HexaBlu",
    'magic_painting.twilightforest.the_hostile_paradise.title': "Le Paradis Hostile",
    'magic_painting.twilightforest.the_hostile_paradise.author': "HexaBlu",
}

# ============================================================
# SUBTITLE TRANSLATION
# ============================================================
# Subtitle pattern: "<Subject> <verb-phrase>" or "<Subject>" (e.g., "Cicada screams")
# Build a per-full-string dict for unique subtitles.

SUBTITLE_LOOKUP = {
    # Block subtitles
    "Ground rumbles": "Le sol gronde",
    "Boss Chest appears": "Le Coffre du Boss apparaît",
    "Bug gets squished :(": "Insecte écrasé :(",
    "Carminite Builder creates block": "Le Constructeur Carminite crée un bloc",
    "Carminite Builder deactivates": "Le Constructeur Carminite se désactive",
    "Carminite Builder activates": "Le Constructeur Carminite s'active",
    "Built Block expires": "Le Bloc Construit expire",
    "Candelabra dims": "Le Candélabre s'atténue",
    "Candelabra sparks": "Le Candélabre crépite",
    "Keepsake Casket closes": "Le Cercueil Souvenir se ferme",
    "Keepsake Casket clicks": "Le Cercueil Souvenir clique",
    "Keepsake Casket opens": "Le Cercueil Souvenir s'ouvre",
    "Keepsake Casket repaired": "Le Cercueil Souvenir est réparé",
    "Chiseled Bookshelf converts": "La Bibliothèque sculptée se convertit",
    "Cicada screams": "La Cigale crie",
    "Changed jar lid": "Couvercle de pot changé",
    "Fire Jet activates": "Le Jet de Feu s'active",
    "Fire Jet flares": "Le Jet de Feu jaillit",
    "Fire Jet pops": "Le Jet de Feu éclate",
    "Tree of Transformation hums": "L'Arbre de Transformation fredonne",
    "Tree of Time ticks": "L'Arbre du Temps fait tic-tac",
    "Flame Whooshes Ominously": "La flamme siffle de manière inquiétante",
    "Drying Rack Empties": "Le Séchoir se vide",
    "Drying Rack Fills": "Le Séchoir se remplit",
    "Sliding Trap creaks": "Le Piège Coulissant grince",
    "Castle Door clicks": "La Porte de Château clique",
    "Castle Door reappears": "La Porte de Château réapparaît",
    "Castle Door vanishes": "La Porte de Château disparaît",
    "Skull Chest closes": "Le Coffre Crâne se ferme",
    "Skull Chest opens": "Le Coffre Crâne s'ouvre",
    "Towerwood door unlocks": "La Porte de Bois de Tour se déverrouille",
    "Reappearing Block disappears": "Le Bloc Réapparaissant disparaît",
    "Reappearing Block reappears": "Le Bloc Réapparaissant réapparaît",
    "Vanishing Block vanishes": "Le Bloc Disparaissant disparaît",
    "Block dissolves": "Le bloc se dissout",
    "Item inserted into jar": "Objet inséré dans le pot",
    "Item removed from jar": "Objet retiré du pot",
    "Jar wiggles": "Le pot frétille",
    "Trophy Pedestal accepts trophy": "Le Piédestal accepte le trophée",
    "Twilight Forest Portal beckons": "Le Portail de la Forêt du Crépuscule attire",

    # Misc actions
    "Boss music plays": "Musique de boss",
    "Acid rain scalds": "La pluie acide brûle",
    "Charm of Keeping returns items": "Le Charme de Préservation rend les objets",
    "Charm of Keeping regenerates": "Le Charme de Préservation se régénère",
    "Map swaps": "La carte change",
    "Mob transforms": "La créature se transforme",
    "Side Step performed": "Pas de Côté effectué",
    "Side Step recharged": "Pas de Côté rechargé",
    "Double Jump performed": "Double Saut effectué",
    "Attack dodged": "Attaque esquivée",
    "Loyal Zombie summoned": "Zombie Loyal invoqué",
    "Belt rustles": "La ceinture bruisse",

    # Items
    "Block and Chain hits block": "Bloc et Chaîne frappe un bloc",
    "Block and Chain hits entity": "Bloc et Chaîne frappe une entité",
    "Block and Chain thrown": "Bloc et Chaîne lancé",
    "Brittle Flask cracks": "La Fiole Friable craque",
    "Brittle Flask shatters": "La Fiole Friable se brise",
    "Potion Flask fills": "La Fiole de Potion se remplit",
    "Tear shatters": "La larme se brise",
    "Torchberries pop": "Les Baies-Torches éclatent",
    "Twilight Pearl hits mob": "La Perle du Crépuscule frappe une créature",
    "Twilight Scepter throws pearl": "Le Sceptre du Crépuscule lance une perle",
    "Life Scepter drains": "Le Sceptre de Vie aspire",
    "Lamp of Cinders ignites area": "La Lampe de Cendres enflamme la zone",
    "Peacock Feather Fan blows": "L'Éventail en Plume de Paon souffle",
    "Ore Magnet pulls up ore": "L'Aimant à Minerais attire le minerai",
    "Ore Meter wipes information": "Le Compteur de Minerais efface les informations",
    "Ice Bomb thrown": "Bombe de Glace lancée",
    "Ice Core crackles": "Le Cœur de Glace crépite",
    "Ice Core shoots snowball": "Le Cœur de Glace tire une boule de neige",
    "Iron clanks": "Le fer claque",
    "Knightmetal Armor clanks": "L'Armure de Métal des Chevaliers claque",
    "Fortification Shield breaks": "Le Bouclier de Fortification se brise",
    "Fortification Shield deflects": "Le Bouclier de Fortification dévie",
    "Fortification Shield expires": "Le Bouclier de Fortification expire",
    "Fortification Shield spawns": "Le Bouclier de Fortification apparaît",
    "Moonworm fires": "Le Ver de Lune tire",
    "Ghast Trap buzzes": "Le Piège à Ghast bourdonne",
    "Ghast Trap dings": "Le Piège à Ghast tinte",
    "Ghast Trap shuts off": "Le Piège à Ghast s'éteint",
    "Ghast Trap warms up": "Le Piège à Ghast chauffe",
    "Carminite Reactor whooshes": "Le Réacteur Carminite vrombit",
    "Traveller's Goggles zoom in": "Les Lunettes du Voyageur zooment",
    "Traveller's Goggles zoom out": "Les Lunettes du Voyageur dézooment",
    "Map swaps Map swaps": "La carte change",

    # Specific entity-action subtitles (where word order matters)
    "Bird takes off": "L'oiseau s'envole",
    "Hydra prepares to bite": "L'Hydre se prépare à mordre",
    "Hydra spews fire": "L'Hydre crache du feu",
    "Hydra shoots mortar": "L'Hydre lance un mortier",
    "Hydra roars in defeat": "L'Hydre rugit, vaincue",
    "Fire Beetle spews flames": "Le Coléoptère de Feu crache des flammes",
    "Naga rattles": "Le Naga sissse",
    "Lich summons new minion": "La Liche invoque un nouveau serviteur",
    "Lich absorbs mob": "La Liche absorbe une créature",
    "Lich teleports": "La Liche se téléporte",
    "Lich breathes": "La Liche respire",
    "Lich clone ignores attack": "Le Clone de la Liche ignore l'attaque",
    "Snow Queen deflects attack": "La Reine des Neiges dévie l'attaque",
    "Knight Phantom throws axe": "Le Chevalier Fantôme lance une hache",
    "Knight Phantom throws pickaxe": "Le Chevalier Fantôme lance une pioche",
    "Minoshroom slams ground": "Le Minoshroom frappe le sol",
    "Minoshroom attacks": "Le Minoshroom attaque",
    "Minotaur attacks": "Le Minotaure attaque",
    "Death Tome falls apart": "Le Tome de Mort se désagrège",
    "Death Tome creases": "Le Tome de Mort se froisse",
    "Death Tome flips pages": "Le Tome de Mort tourne ses pages",
    "Yeti grabs": "Le Yéti agrippe",
    "Alpha Yeti grabs": "Le Yéti Alpha agrippe",
    "Alpha Yeti pants": "Le Yéti Alpha halète",
    "Alpha Yeti throws": "Le Yéti Alpha lance",
    "Alpha Yeti throws ice": "Le Yéti Alpha lance de la glace",
    "Alpha Yeti takes notice": "Le Yéti Alpha remarque",
    "Yeti throws": "Le Yéti lance",
    "Maze Slime squishes": "Le Slime du Labyrinthe rebondit",
    "Helmet Crab snips": "Le Casque-Crabe pince",
    "Pinch Beetle clamps": "Le Coléoptère pince",
    "Mosquitoes buzz": "Les Moustiques bourdonnent",
    "Tiny Bird sings": "Le Petit Oiseau chante",
    "Tiny Bird chirps": "Le Petit Oiseau pépie",
    "Raven caws": "Le Corbeau croasse",
    "Penguin honks": "Le Manchot klaxonne",
    "Dwarf Rabbit squeaks": "Le Lapin Nain couine",
    "Boar oinks": "Le Sanglier grogne",
    "Deer eats": "Le Cerf mange",
    "Deer moos": "Le Cerf brame",
    "Bighorn Sheep bleats": "Le Mouflon d'Amérique bêle",
    "Questing Ram bleats": "Le Bélier des Quêtes bêle",
    "Goblin Knight chuckles": "Le Chevalier Gobelin ricane",
    "Goblin Knight groans in agony": "Le Chevalier Gobelin gémit d'agonie",
    "Goblin Knight screeches in pain": "Le Chevalier Gobelin hurle de douleur",
    "Muffled Goblin Knight groans in agony": "Le Chevalier Gobelin étouffé gémit d'agonie",
    "Muffled Goblin Knight screeches in pain": "Le Chevalier Gobelin étouffé hurle de douleur",
    "Block and Chain Goblin chuckles": "Le Gobelin au Bloc et Chaîne ricane",
    "Block and Chain Goblin screams": "Le Gobelin au Bloc et Chaîne crie",
    "Kobold grumbles": "Le Kobold grommelle",
    "Kobold munches": "Le Kobold mâche",
    "Loyal Zombie groans": "Le Zombie Loyal gémit",
    "Lich Minion groans": "Le Serviteur de la Liche gémit",
    "Carminite Broodling hisses": "La Couveuse Carminite siffle",
    "Carminite Ghastguard cries": "Le Garde Ghast Carminite pleure",
    "Carminite Ghastling cries": "Le Petit Ghast Carminite pleure",
    "Carminite Ghastguard hurts": "Le Garde Ghast Carminite est blessé",
    "Carminite Ghastguard screams": "Le Garde Ghast Carminite crie",
    "Carminite Golem swings": "Le Golem Carminite balance",
    "Hedge Spider hisses": "L'Araignée des Haies siffle",
    "Hedge Spider hurts": "L'Araignée des Haies est blessée",
    "Troll grabs rock": "Le Troll attrape un rocher",
    "Troll throws rock": "Le Troll lance un rocher",
    "Ur-Ghast wails": "L'Ur-Ghast gémit",
}

# Generic per-verb subtitle templates (apply when full lookup fails)
ACTION_TEMPLATES = {
    # verb -> ("masc-template", "fem-template") with %s for subject
    "growls": ("{subj} grogne", "{subj} grogne"),
    "growl": ("Grognement de {subj}", "Grognement de {subj}"),
    "roars": ("{subj} rugit", "{subj} rugit"),
    "roar": ("Rugissement de {subj}", "Rugissement de {subj}"),
    "hisses": ("{subj} siffle", "{subj} siffle"),
    "hiss": ("Sifflement de {subj}", "Sifflement de {subj}"),
    "dies": ("{subj} meurt", "{subj} meurt"),
    "die": ("{subj} meurt", "{subj} meurt"),
    "hurts": ("{subj} est blessé", "{subj} est blessée"),
    "hurt": ("{subj} blessé", "{subj} blessée"),
    "moos": ("{subj} meugle", "{subj} meugle"),
    "moo": ("Meuglement de {subj}", "Meuglement de {subj}"),
    "screams": ("{subj} crie", "{subj} crie"),
    "scream": ("Cri de {subj}", "Cri de {subj}"),
    "shoots": ("{subj} tire", "{subj} tire"),
    "shoot": ("Tir de {subj}", "Tir de {subj}"),
    "rattles": ("{subj} cliquette", "{subj} cliquette"),
    "rattle": ("Cliquetis de {subj}", "Cliquetis de {subj}"),
    "step": ("Pas de {subj}", "Pas de {subj}"),
    "steps": ("Pas de {subj}", "Pas de {subj}"),
    "ambient": ("{subj} (son ambiant)", "{subj} (son ambiant)"),
    "chitters": ("{subj} chuinte", "{subj} chuinte"),
    "chuckles": ("{subj} ricane", "{subj} ricane"),
    "clanks": ("{subj} cliquette", "{subj} cliquette"),
    "buzzes": ("{subj} bourdonne", "{subj} bourdonne"),
    "buzz": ("Bourdonnement de {subj}", "Bourdonnement de {subj}"),
    "caws": ("{subj} croasse", "{subj} croasse"),
    "chirps": ("{subj} pépie", "{subj} pépie"),
    "honks": ("{subj} klaxonne", "{subj} klaxonne"),
    "squeaks": ("{subj} couine", "{subj} couine"),
    "oinks": ("{subj} grogne", "{subj} grogne"),
    "bleats": ("{subj} bêle", "{subj} bêle"),
    "sings": ("{subj} chante", "{subj} chante"),
    "munches": ("{subj} mâche", "{subj} mâche"),
    "eats": ("{subj} mange", "{subj} mange"),
    "drinks": ("{subj} boit", "{subj} boit"),
    "fires": ("{subj} tire", "{subj} tire"),
    "wails": ("{subj} gémit", "{subj} gémit"),
    "groans": ("{subj} gémit", "{subj} gémit"),
    "grumbles": ("{subj} grommelle", "{subj} grommelle"),
    "snips": ("{subj} pince", "{subj} pince"),
    "clamps": ("{subj} pince", "{subj} pince"),
    "snorts": ("{subj} renifle", "{subj} renifle"),
    "bites": ("{subj} mord", "{subj} mord"),
    "swings": ("{subj} balance", "{subj} balance"),
    "teleports": ("{subj} se téléporte", "{subj} se téléporte"),
    "vanishes": ("{subj} disparaît", "{subj} disparaît"),
    "disappears": ("{subj} disparaît", "{subj} disparaît"),
    "reappears": ("{subj} réapparaît", "{subj} réapparaît"),
    "thunks": ("{subj} fait un bruit sourd", "{subj} fait un bruit sourd"),
    "creaks": ("{subj} grince", "{subj} grince"),
    "cracks": ("{subj} craque", "{subj} craque"),
    "shatters": ("{subj} se brise", "{subj} se brise"),
    "crackles": ("{subj} crépite", "{subj} crépite"),
    "creases": ("{subj} se froisse", "{subj} se froisse"),
    "cries": ("{subj} pleure", "{subj} pleure"),
    "expires": ("{subj} expire", "{subj} expire"),
    "appears": ("{subj} apparaît", "{subj} apparaît"),
    "spawns": ("{subj} apparaît", "{subj} apparaît"),
    "transforms": ("{subj} se transforme", "{subj} se transforme"),
    "summoned": ("{subj} invoqué", "{subj} invoquée"),
    "performed": ("{subj} effectué", "{subj} effectué"),
    "recharged": ("{subj} rechargé", "{subj} rechargée"),
    "dodged": ("{subj} esquivé", "{subj} esquivée"),
    "thrown": ("{subj} lancé", "{subj} lancée"),
    "drains": ("{subj} aspire", "{subj} aspire"),
    "blows": ("{subj} souffle", "{subj} souffle"),
    "swaps": ("{subj} change", "{subj} change"),
    "fills": ("{subj} se remplit", "{subj} se remplit"),
    "rumbles": ("{subj} gronde", "{subj} gronde"),
    "creates": ("{subj} crée", "{subj} crée"),
    "deactivates": ("{subj} se désactive", "{subj} se désactive"),
    "activates": ("{subj} s'active", "{subj} s'active"),
    "appears": ("{subj} apparaît", "{subj} apparaît"),
    "expires": ("{subj} expire", "{subj} expire"),
    "closes": ("{subj} se ferme", "{subj} se ferme"),
    "opens": ("{subj} s'ouvre", "{subj} s'ouvre"),
    "clicks": ("{subj} clique", "{subj} clique"),
    "repaired": ("{subj} réparé", "{subj} réparée"),
    "converts": ("{subj} se convertit", "{subj} se convertit"),
    "dims": ("{subj} s'atténue", "{subj} s'atténue"),
    "sparks": ("{subj} crépite", "{subj} crépite"),
    "lights": ("{subj} s'allume", "{subj} s'allume"),
    "flares": ("{subj} jaillit", "{subj} jaillit"),
    "pops": ("{subj} éclate", "{subj} éclate"),
    "hums": ("{subj} fredonne", "{subj} fredonne"),
    "ticks": ("{subj} fait tic-tac", "{subj} fait tic-tac"),
    "rustles": ("{subj} bruisse", "{subj} bruisse"),
    "scalds": ("{subj} brûle", "{subj} brûle"),
    "wiggles": ("{subj} frétille", "{subj} frétille"),
    "whooshes": ("{subj} vrombit", "{subj} vrombit"),
    "freezes": ("{subj} gèle", "{subj} gèle"),
    "burns": ("{subj} brûle", "{subj} brûle"),
    "explodes": ("{subj} explose", "{subj} explose"),
    "stomps": ("{subj} piétine", "{subj} piétine"),
    "yelps": ("{subj} glapit", "{subj} glapit"),
    "gasps": ("{subj} halète", "{subj} halète"),
    "pants": ("{subj} halète", "{subj} halète"),
    "chimes": ("{subj} carillonne", "{subj} carillonne"),
    "dings": ("{subj} tinte", "{subj} tinte"),
    "drips": ("{subj} goutte", "{subj} goutte"),
    "splashes": ("{subj} éclabousse", "{subj} éclabousse"),
    "throws": ("{subj} lance", "{subj} lance"),
    "grabs": ("{subj} agrippe", "{subj} agrippe"),
    "slithers": ("{subj} glisse", "{subj} glisse"),
    "attacks": ("{subj} attaque", "{subj} attaque"),
    "summons": ("{subj} invoque", "{subj} invoque"),
    "absorbs": ("{subj} absorbe", "{subj} absorbe"),
    "ignores": ("{subj} ignore", "{subj} ignore"),
    "deflects": ("{subj} dévie", "{subj} dévie"),
    "breaks": ("{subj} se brise", "{subj} se brise"),
    "breathes": ("{subj} respire", "{subj} respire"),
    "spits": ("{subj} crache", "{subj} crache"),
    "spews": ("{subj} crache", "{subj} crache"),
    "imitates": ("{subj} imite", "{subj} imite"),
    "thuds": ("{subj} fait un bruit sourd", "{subj} fait un bruit sourd"),
    "unlocks": ("{subj} se déverrouille", "{subj} se déverrouille"),
    "dissolves": ("{subj} se dissout", "{subj} se dissout"),
    "pulls": ("{subj} attire", "{subj} attire"),
    "wipes": ("{subj} efface", "{subj} efface"),
}

# Subjects that are feminine in French
FEMININE_SUBJECTS = {
    "Hydra", "Hydre", "Lich", "Liche", "Snow Queen", "Reine des Neiges",
    "Cicada", "Cigale", "Hedge Spider", "Araignée des Haies",
    "Mosquito", "Mosquitoes", "Moustiques",
    "Carminite Broodling", "Couveuse Carminite",
    "Door", "Porte", "Castle Door", "Porte de Château",
    "Bell", "Cloche",
    "Tear", "Larme",
    "Belt", "Ceinture",
    "Brittle Flask", "Fiole Friable",
    "Potion Flask", "Fiole de Potion",
    "Lich clone", "Clone de la Liche",
    "Acid rain", "Pluie acide",
    "Lamp of Cinders", "Lampe de Cendres",
    "Map", "Carte",
    "King Spider", "Reine des Araignées",
    "Knightmetal Armor", "Armure de Métal des Chevaliers",
}

# ============================================================
# Banner translation (color + descriptor)
# ============================================================
BANNER_DESCRIPTORS = {
    # En descriptor -> (FR descriptor, gender, plurality)
    # ("Snowflake" => "Flocon de neige", masc sing)
    "Alpha Yeti Face": ("Visage du Yéti Alpha", "m", "s"),
    "Carminite Border": ("Bordure Carminite", "f", "s"),
    "Hydra Flame": ("Flamme d'Hydre", "f", "s"),
    "Knight Helmet": ("Casque de Chevalier", "m", "s"),
    "Lich Crown": ("Couronne de la Liche", "f", "s"),
    "Minoshroom Axes": ("Haches du Minoshroom", "f", "p"),
    "Naga Scales": ("Écailles de Naga", "f", "p"),
    "Questing Ram Swirls": ("Spirales du Bélier des Quêtes", "f", "p"),
    "Snowflake": ("Flocon de neige", "m", "s"),
}

# ============================================================
# Death messages
# ============================================================
DEATH_LOOKUP = {
    "%1$s went dancing in the acid rain": "%1$s est allé danser sous la pluie acide",
    "%1$s was squashed like an ant by %2$s": "%1$s a été écrasé comme une fourmi par %2$s",
    "%1$s was squashed like an ant by %2$s holding %3$s": "%1$s a été écrasé comme une fourmi par %2$s tenant %3$s",
    "%1$s was chopped up by %2$s": "%1$s a été haché par %2$s",
    "%1$s was chopped up by %2$s using %3$s": "%1$s a été haché par %2$s avec %3$s",
    "%1$s was frozen to death by the Snow Queen": "%1$s a été gelé à mort par la Reine des Neiges",
    "%1$s was frozen to death by the Snow Queen while escaping %2$s": "%1$s a été gelé à mort par la Reine des Neiges en fuyant %2$s",
    "%1$s was squeezed to death by %2$s": "%1$s a été écrasé à mort par %2$s",
    "%1$s was squeezed to death by %2$s using %3$s": "%1$s a été écrasé à mort par %2$s avec %3$s",
    "%1$s's life expired": "La vie de %1$s a expiré",
    "%1$s failed to show their mettle and drank themselves to death": "%1$s n'a pas su prouver son courage et s'est tué en buvant",
    "%1$s walked onto a Fiery block": "%1$s a marché sur un bloc Ardent",
    "%1$s walked onto a Fiery block while escaping %2$s": "%1$s a marché sur un bloc Ardent en fuyant %2$s",
    "%1$s accidentally walked into a Fire Jet": "%1$s a accidentellement marché dans un Jet de Feu",
    "%1$s accidentally walked into a Fire Jet while escaping %2$s": "%1$s a accidentellement marché dans un Jet de Feu en fuyant %2$s",
    "%1$s stood too close to a Carminite Reactor": "%1$s s'est tenu trop près d'un Réacteur Carminite",
    "%1$s stood too close to a Carminite Reactor while escaping %2$s": "%1$s s'est tenu trop près d'un Réacteur Carminite en fuyant %2$s",
    "%1$s succumbed to the Lich's explosive magic": "%1$s a succombé à la magie explosive de la Liche",
    "%1$s succumbed to the Lich's explosive magic while escaping %2$s": "%1$s a succombé à la magie explosive de la Liche en fuyant %2$s",
    "%1$s was scorched by %2$s": "%1$s a été brûlé par %2$s",
    "%1$s was scorched by %2$s using %3$s": "%1$s a été brûlé par %2$s avec %3$s",
    "%1$s was schooled by %2$s": "%1$s a été instruit par %2$s",
    "%1$s was schooled by %2$s using %3$s": "%1$s a été instruit par %2$s avec %3$s",
    "%1$s was skewered by a Knightmetal block": "%1$s a été embroché par un bloc de Métal des Chevaliers",
    "%1$s was skewered by a Knightmetal block while escaping %2$s": "%1$s a été embroché par un bloc de Métal des Chevaliers en fuyant %2$s",
    "%1$s was killed by a Carminite Reactor while escaping %2$s": "%1$s a été tué par un Réacteur Carminite en fuyant %2$s",
    "%1$s was crushed by %2$s": "%1$s a été écrasé par %2$s",
    "%1$s was crushed by %2$s using %3$s": "%1$s a été écrasé par %2$s avec %3$s",
    "%1$s was hurled to their death by %2$s": "%1$s a été projeté à mort par %2$s",
    "%1$s was hurled to their death by %2$s using %3$s": "%1$s a été projeté à mort par %2$s avec %3$s",
    "%1$s tasted the wrath of an Ur-Ghast": "%1$s a goûté à la colère d'un Ur-Ghast",
    "%1$s tasted the wrath of an Ur-Ghast while escaping %2$s": "%1$s a goûté à la colère d'un Ur-Ghast en fuyant %2$s",
    "%1$s drowned in glacial waters": "%1$s s'est noyé dans les eaux glaciales",
    "%1$s drowned in glacial waters while escaping %2$s": "%1$s s'est noyé dans les eaux glaciales en fuyant %2$s",
    "%1$s was frozen to death": "%1$s a été gelé à mort",
    "%1$s was frozen to death while escaping %2$s": "%1$s a été gelé à mort en fuyant %2$s",
    "%1$s was crushed by a falling icicle": "%1$s a été écrasé par un glaçon tombant",
    "%1$s was crushed by a falling icicle while escaping %2$s": "%1$s a été écrasé par un glaçon tombant en fuyant %2$s",
    "%1$s was tickled to death by a Cicada": "%1$s a été chatouillé à mort par une Cigale",
    "%1$s was tickled to death by a Cicada while escaping %2$s": "%1$s a été chatouillé à mort par une Cigale en fuyant %2$s",
    "%1$s was poisoned by a Skeleton Druid": "%1$s a été empoisonné par un Squelette Druide",
    "%1$s was poisoned by a Skeleton Druid while escaping %2$s": "%1$s a été empoisonné par un Squelette Druide en fuyant %2$s",
    "%1$s was annihilated by %2$s": "%1$s a été anéanti par %2$s",
    "%1$s was annihilated by %2$s using %3$s": "%1$s a été anéanti par %2$s avec %3$s",
    "%1$s was struck by a Lich's bolt": "%1$s a été frappé par un éclair de la Liche",
    "%1$s was struck by a Lich's bolt while escaping %2$s": "%1$s a été frappé par un éclair de la Liche en fuyant %2$s",
    "%1$s was zombified by a Lich's bolt": "%1$s a été zombifié par un éclair de la Liche",
    "%1$s was zombified by a Lich's bolt while escaping %2$s": "%1$s a été zombifié par un éclair de la Liche en fuyant %2$s",
    "%1$s was infected by a Mosquito Swarm": "%1$s a été infecté par un Essaim de Moustiques",
    "%1$s was infected by a Mosquito Swarm while escaping %2$s": "%1$s a été infecté par un Essaim de Moustiques en fuyant %2$s",
    "%1$s was burned to a crisp by a Fire Beetle": "%1$s a été brûlé par un Coléoptère de Feu",
    "%1$s was burned to a crisp by a Fire Beetle while escaping %2$s": "%1$s a été brûlé par un Coléoptère de Feu en fuyant %2$s",
    "%1$s was eaten by an Hydra": "%1$s a été dévoré par une Hydre",
    "%1$s was eaten by an Hydra while escaping %2$s": "%1$s a été dévoré par une Hydre en fuyant %2$s",
    "%1$s was assassinated by a Phantom Knight": "%1$s a été assassiné par un Chevalier Fantôme",
    "%1$s was assassinated by a Phantom Knight while escaping %2$s": "%1$s a été assassiné par un Chevalier Fantôme en fuyant %2$s",
    "%1$s couldn't escape the Naga's coils": "%1$s n'a pas pu échapper aux anneaux du Naga",
    "%1$s couldn't escape the Naga's coils while escaping %2$s": "%1$s n'a pas pu échapper aux anneaux du Naga en fuyant %2$s",
    "%1$s was clamped": "%1$s a été pincé",
    "%1$s was clamped using %2$s": "%1$s a été pincé avec %2$s",
    "%1$s was clamped while escaping %2$s": "%1$s a été pincé en fuyant %2$s",
    "%1$s was clamped using %2$s while escaping %3$s": "%1$s a été pincé avec %2$s en fuyant %3$s",
    "%1$s was hammered to death by %2$s": "%1$s a été martelé à mort par %2$s",
    "%1$s was hammered to death by %2$s using %3$s": "%1$s a été martelé à mort par %2$s avec %3$s",
    "%1$s was knocked over by %2$s": "%1$s a été renversé par %2$s",
    "%1$s was knocked over by %2$s using %3$s": "%1$s a été renversé par %2$s avec %3$s",
    "%1$s was tamed to death by a Quest Ram": "%1$s a été apprivoisé à mort par un Bélier des Quêtes",
    "%1$s was tamed to death by a Quest Ram while escaping %2$s": "%1$s a été apprivoisé à mort par un Bélier des Quêtes en fuyant %2$s",
}

# ============================================================
# Helper functions
# ============================================================

def replace_canonical(value):
    """Replace canonical proper nouns / structures / materials in a value.
    Apply longest-first to avoid partial overlaps. Case-sensitive primary;
    lowercased fallbacks for inline use.
    """
    pairs = []
    for d in (NOUNS, ENTITIES, MATERIALS):
        for en, fr in d.items():
            pairs.append((en, fr))
    # Sort by length desc
    pairs.sort(key=lambda p: -len(p[0]))
    out = value
    for en, fr in pairs:
        out = out.replace(en, fr)
    # Generic standalone words (after named entities)
    aux = [
        ("Twilight", "Crépuscule"),
        ("twilight", "crépuscule"),
        ("Fiery", "Ardent"),
        ("fiery", "ardent"),
    ]
    for en, fr in aux:
        out = out.replace(en, fr)
    return out


def get_subject_french(subj_en):
    """Map an English subject (entity/object) to its French canonical name."""
    # Try direct lookup
    for d in (ENTITIES, NOUNS, MATERIALS):
        if subj_en in d:
            return d[subj_en]
    # Try replacing canonical terms inside it
    return replace_canonical(subj_en)


def is_feminine(subj_en, subj_fr):
    if subj_en in FEMININE_SUBJECTS or subj_fr in FEMININE_SUBJECTS:
        return True
    # Heuristic: ends with 'e' and not ending with 'ée'
    return False


def translate_subtitle(value):
    """Translate a subtitle entry."""
    # Direct lookup
    if value in SUBTITLE_LOOKUP:
        return SUBTITLE_LOOKUP[value]
    # Try splitting "<subject> <verb>"
    words = value.split()
    if not words:
        return value
    last = words[-1].rstrip('.,!?')
    # Try last word as a verb
    if last in ACTION_TEMPLATES:
        subj_en = ' '.join(words[:-1])
        subj_fr = get_subject_french(subj_en)
        if subj_fr:
            article = "La " if is_feminine(subj_en, subj_fr) else "Le "
            # If subject already starts with article-able phrase, prepend article
            if subj_fr[0].isupper():
                # Check if subj is plural-feminine
                tmpl = ACTION_TEMPLATES[last][1] if is_feminine(subj_en, subj_fr) else ACTION_TEMPLATES[last][0]
                return tmpl.format(subj=article + subj_fr)
    # Fallback: just replace canonical names
    return replace_canonical(value)


def translate_banner(value):
    """Translate banner names: '<Color> <Descriptor>'."""
    m = re.match(COLOR_RE_PATTERN, value)
    if not m:
        return replace_canonical(value)
    color_en = m.group(1)
    descriptor_en = m.group(2)
    if descriptor_en in BANNER_DESCRIPTORS:
        descr_fr, gender, plur = BANNER_DESCRIPTORS[descriptor_en]
        if gender == "f" and plur == "p":
            color_fr = COLORS_FP[color_en]
        elif gender == "f":
            color_fr = COLORS_F[color_en]
        elif plur == "p":
            color_fr = COLORS_MP[color_en]
        else:
            color_fr = COLORS_M[color_en]
        return f"{descr_fr} {color_fr}"
    # Unknown descriptor: do generic
    return f"{COLORS_M[color_en]} {replace_canonical(descriptor_en)}"


def translate_block(value):
    """Translate a twilightforest block name."""
    out = replace_canonical(value)
    # Vanilla wood map (used in Hollow X Log)
    wood_map = {
        'Acacia': 'acacia', 'Birch': 'bouleau', 'Cherry': 'cerisier',
        'Crimson': 'cramoisi', 'Dark Oak': 'chêne noir', 'Jungle': 'jungle',
        'Mangrove': 'palétuvier', 'Oak': 'chêne', 'Spruce': 'sapin',
        'Warped': 'biscornu', 'Cinder': 'cendres',
    }
    # Special hollow logs first
    def hollow_log_repl(m):
        species = m.group(1)
        # Already-translated material handled
        translation_map_lower = {
            'birch': 'bouleau', 'acacia': "d'acacia", 'cherry': 'cerisier',
            'jungle': 'jungle', 'oak': 'chêne', 'spruce': 'sapin',
            'dark oak': 'chêne noir', 'crimson': 'cramoisi', 'warped': 'biscornu',
            'sortingwood': "de tri", 'timewood': "du temps", 'transwood': "de transformation",
            'canopée tree': 'canopée', 'chêne du crépuscule': "de chêne du Crépuscule",
            'palétuvier': 'palétuvier', 'bois sombre': 'bois sombre', 'bois minier': 'bois minier',
        }
        sp_lower = species.lower()
        if sp_lower in translation_map_lower:
            tr = translation_map_lower[sp_lower]
        else:
            tr = species.lower()
        # Build correct phrase
        if tr.startswith("d'") or tr.startswith("de "):
            return f"Bûche {tr} creuse"
        return f"Bûche de {tr} creuse"

    out = re.sub(r'Hollow Twilight Oak Log', "Bûche de Chêne du Crépuscule creuse", out)
    out = re.sub(r'Hollow Canopy Tree Log', "Bûche de Canopée creuse", out)
    out = re.sub(r'Hollow Dark Oak Log', "Bûche de Chêne Noir creuse", out)
    out = re.sub(r'Hollow (.+?) Log', hollow_log_repl, out)
    out = re.sub(r'Hollow Crimson Stem', "Tige Cramoisie creuse", out)
    out = re.sub(r'Hollow Warped Stem', "Tige Biscornue creuse", out)
    out = re.sub(r'Stripped (.+?) Log', lambda m: f"Bûche de {m.group(1).lower()} écorcée", out)
    out = re.sub(r'Stripped (.+?) Wood', lambda m: f"Bois de {m.group(1).lower()} écorcé", out)
    # Ominous candles
    out = re.sub(r'Ominous (Black|Blue|Brown|Cyan|Gray|Green|Light Blue|Light Gray|Lime|Magenta|Orange|Pink|Purple|Red|White|Yellow) Candle',
                 lambda m: f"Bougie inquiétante {COLORS_F[m.group(1)]}", out)
    out = re.sub(r'Ominous Candle', "Bougie inquiétante", out)
    # Generic post-processing
    out = re.sub(r'\bCandle\b', 'Bougie', out)
    out = re.sub(r'\bAxe\b', 'Hache', out)
    out = re.sub(r'\bPickaxe\b', 'Pioche', out)
    out = re.sub(r'\bSword\b', 'Épée', out)
    out = re.sub(r'\bShovel\b', 'Pelle', out)
    out = re.sub(r'\bHoe\b', 'Houe', out)
    out = re.sub(r'\bSlab\b', 'Dalle', out)
    out = re.sub(r'\bStairs\b', 'Escalier', out)
    out = re.sub(r'\bBanister\b', 'Rampe', out)
    return out


def translate_block_desc(value):
    """For things like '%s ticks' or 'Right-click ...'."""
    repls = {
        "Right-click with axe to cycle": "Clic droit avec une hache pour changer la hauteur",
        "Deals strong contact damage": "Inflige de forts dégâts au contact",
        "This Casket can only be opened by %s!": "Ce cercueil ne peut être ouvert que par %s !",
        "This Casket has been claimed by %s!": "Ce cercueil a été réclamé par %s !",
        "This Casket can no longer be repaired.": "Ce cercueil ne peut plus être réparé.",
        "This Casket is locked!": "Ce cercueil est verrouillé !",
    }
    if value in repls:
        return repls[value]
    return replace_canonical(value)


def translate_item(value):
    out = replace_canonical(value)
    out = re.sub(r'\bAxe\b', 'Hache', out)
    out = re.sub(r'\bPickaxe\b', 'Pioche', out)
    out = re.sub(r'\bSword\b', 'Épée', out)
    out = re.sub(r'\bShovel\b', 'Pelle', out)
    out = re.sub(r'\bHoe\b', 'Houe', out)
    out = re.sub(r'\bBow\b', 'Arc', out)
    out = re.sub(r'\bHelmet\b', 'Casque', out)
    out = re.sub(r'\bChestplate\b', 'Plastron', out)
    out = re.sub(r'\bLeggings\b', 'Jambières', out)
    out = re.sub(r'\bBoots\b', 'Bottes', out)
    out = re.sub(r'\bIngot\b', 'Lingot', out)
    return out


def translate_entity(value):
    return replace_canonical(value)


def translate_tag(value):
    return replace_canonical(value)


def translate_structure(value):
    return replace_canonical(value)


def translate_death(value):
    if value in DEATH_LOOKUP:
        return DEATH_LOOKUP[value]
    # Fallback: replace canonical names then return
    return replace_canonical(value)


def translate_advancement(value):
    """Translate advancement title or desc."""
    # Replace canonical
    out = replace_canonical(value)
    return out


def translate_tip(value):
    """Translate twilightforest.tips entries (sentences)."""
    out = replace_canonical(value)
    return out


def translate_book(value):
    """Translate book content."""
    out = replace_canonical(value)
    return out


def translate_config(value):
    """Translate config option labels and tooltips."""
    out = replace_canonical(value)
    return out


def translate_command(value):
    out = replace_canonical(value)
    return out


def translate_misc(value):
    out = replace_canonical(value)
    return out


def translate_gui(value):
    out = replace_canonical(value)
    return out


def translate_modifier(value):
    out = replace_canonical(value)
    return out


def translate_default(value):
    return replace_canonical(value)


# ============================================================
# Dispatcher
# ============================================================

def translate(key, value):
    if key in HARDCODED:
        return HARDCODED[key]
    if key.startswith('subtitles.twilightforest.'):
        return translate_subtitle(value)
    if key.startswith('block.minecraft.banner.'):
        return translate_banner(value)
    if key.startswith('death.attack.'):
        return translate_death(value)
    if key.startswith('block.twilightforest.'):
        # Choose block name vs description
        if key.endswith('.desc') or key.endswith('.cycle') or key.endswith('.locked') or key.endswith('.claimed') or key.endswith('.no_repair'):
            return translate_block_desc(value)
        return translate_block(value)
    if key.startswith('item.twilightforest.'):
        return translate_item(value)
    if key.startswith('entity.twilightforest.'):
        return translate_entity(value)
    if key.startswith('tag.item.') or key.startswith('tag.fluid.'):
        return translate_tag(value)
    if key.startswith('structure.twilightforest.'):
        return translate_structure(value)
    if key.startswith('advancement.twilightforest.'):
        return translate_advancement(value)
    if key.startswith('twilightforest.tips.'):
        return translate_tip(value)
    if key.startswith('twilightforest.book.'):
        return translate_book(value)
    if key.startswith('config.twilightforest.') or key.startswith('config.jade.'):
        return translate_config(value)
    if key.startswith('commands.tffeature.'):
        return translate_command(value)
    if key.startswith('misc.twilightforest.'):
        return translate_misc(value)
    if key.startswith('gui.twilightforest.'):
        return translate_gui(value)
    if key.startswith('travellers_gear.modifier.'):
        return translate_modifier(value)
    if key.startswith('container.twilightforest.'):
        return translate_default(value)
    if key.startswith('biome.twilightforest.'):
        return translate_default(value)
    if key.startswith('museumcurator.'):
        return translate_default(value)
    if key.startswith('magic_painting.twilightforest.'):
        return translate_default(value)
    if key.startswith('jukebox_song.twilightforest.'):
        return translate_default(value)
    if key.startswith('trim_material.twilightforest.'):
        return translate_default(value)
    return translate_default(value)


def main():
    src = json.loads(INPUT.read_text(encoding='utf-8'))
    out = {}
    for k, v in src.items():
        out[k] = translate(k, v)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')

    # Validate
    reread = json.loads(OUTPUT.read_text(encoding='utf-8'))
    print(f"Wrote {len(reread)} keys to {OUTPUT}")
    assert len(reread) == len(src), f"COUNT MISMATCH: {len(reread)} != {len(src)}"
    print("OK: counts match")


if __name__ == '__main__':
    main()
