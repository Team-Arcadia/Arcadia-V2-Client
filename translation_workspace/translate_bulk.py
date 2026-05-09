# -*- coding: utf-8 -*-
"""
Bulk translator for Arcadia V2 untranslated keys.
Reads each input JSON, looks up existing FR jar file when available,
and emits translated output JSON.
"""
import os, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = 'c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/audit2'
SRC = ROOT + '/untranslated_per_mod/'
JAR_FR = ROOT + '/all_jar_fr/'
OUT = ROOT + '/agent_output/'

SKIP = {'occultism','pipeorgans','lootr','createfood','mcwpaintings','ars_nouveau',
        'immersiveengineering','create_sa','fancymenu','dungeons_arise','mekanism',
        'arcadiaguard','create_dragons_plus','ftbquests','handcrafted','create_confectionery'}

# Manual translations, exact-match per (modid, key) or (key) or (value).
# Built from inspection of all_untranslated.txt
TRANS = {
    # ====== UI / config common ======
    "Cape": "Cape",
    "Type": "Type",
    "Mode": "Mode",
    "Original": "Original",
    "Note": "Note",
    "Description": "Description",
    "Information": "Informations",
    "Configuration": "Configuration",
    "Modules": "Modules",
    "Minecraft": "Minecraft",
    "Performance": "Performance",
    "Vignette": "Vignette",
    "Audio": "Audio",
    "Options": "Options",
    "Volume": "Volume",
    "Volume: ": "Volume : ",
    "Zoom": "Zoom",
    "Position": "Position",
    "Rotation": "Rotation",
    "Saturation": "Saturation",
    "Visible": "Visible",
    "Dimension": "Dimension",
    "Biome": "Biome",
    "Distance": "Distance",
    "Source": "Source",
    "Page": "Page",
    "Page %s / %s": "Page %s / %s",
    "Page %s / %s ": "Page %s / %s ",
    "Total": "Total",
    "Public": "Public",
    "Admin": "Admin",
    "Endurance": "Endurance",
    "Rare": "Rare",
    "Unique": "Unique",
    "Mature": "Mature",
    "Wiki": "Wiki",
    "Discord": "Discord",
    "Texture": "Texture",
    "Textures": "Textures",
    "Charge": "Charge",
    "Chance": "Chance",
    "Chance: %s": "Chance : %s",
    "Chance: %s%%": "Chance : %s%%",
    "Mode:": "Mode :",
    "Modules": "Modules",
    "Section": "Section",
    "Sections": "Sections",
    "Auto": "Auto",
    "Zone": "Zone",
    "Pause": "Pause",
    "Vault": "Saut",
    "Wall Jump": "Saut mural",
    "Wall Slide": "Glisse murale",
    "Climb Up": "Escalade",
    "Dive": "Plongée",
    "Hang-Down Jump": "Saut suspendu",
    "Safety Tap": "Roulade",
    "Action": "Action",
    "Actions": "Actions",
    "Animation": "Animation",
    "Base": "Base",
    "Combat": "Combat",
    "Conditions": "Conditions",
    "Local": "Local",
    "Pose": "Posture",
    "Question": "Question",
    "Skin": "Apparence",
    "Limitations": "Limitations",
    "Config": "Config",
    "Statue": "Statue",
    "David": "David",
    "Ballet": "Ballet",
    "Zombie": "Zombie",
    "Acolyte": "Acolyte",
    "Mode": "Mode",
    "Stock": "Stock",
    "Charges %s / %s": "Charges %s / %s",
    "Rechargeable": "Rechargeable",
    "Second": "Second",
    "Refresh Rate": "Fréquence d'actualisation",
    "Construction": "Construction",
    "Destruction": "Destruction",
    "Modid": "modid",
    "modid": "modid",
    "transparent,alpha": "transparent,alpha",
    "Modonomicon": "Modonomicon",
    "Patchouli": "Patchouli",
    "Compost": "Compost",

    # ====== Item / block names common ======
    "Sushi": "Sushi",
    "Capitaine": "Capitaine",
    "Synodontis": "Synodontis",
    "Piranha": "Piranha",
    "Tambaqui": "Tambaqui",
    "Durable": "Durable",
    "Super Durable": "Super durable",
    "Rollmops": "Rollmops",
    "Bisque": "Bisque",
    "Bibimbap": "Bibimbap",
    "Tortilla": "Tortilla",
    "Taco": "Taco",
    "Popcorn": "Popcorn",
    "Elote": "Elote",
    "Empanada": "Empanada",
    "Bubble Tea": "Bubble Tea",
    "Toast": "Toast",
    "Toasts": "Toasts",
    "Ghasta": "Ghasta",
    "Cookie": "Cookie",
    "Sandwich": "Sandwich",
    "Hamburger": "Hamburger",
    "Wrap": "Wrap",
    "Antidote": "Antidote",
    "Poison": "Poison",
    "Gladius": "Gladius",
    "Slime": "Slime",
    "Ticket": "Ticket",
    "Radar": "Radar",

    # ====== Wines ======
    "Riesling": "Riesling",
    "Cabernet Sauvignon": "Cabernet Sauvignon",
    "Merlot": "Merlot",
    "Zinfandel": "Zinfandel",
    "Bordeaux": "Bordeaux",
    "Chardonnay": "Chardonnay",
    "Pinot Noir": "Pinot Noir",

    # ====== Mod names (kept) ======
    "Advanced Netherite": "Advanced Netherite",
    "Advanced Peripherals": "Advanced Peripherals",
    "Aether": "Aether",
    "Apotheosis": "Apotheosis",
    "Apothic Spawners": "Apothic Spawners",
    "AppleSkin": "AppleSkin",
    "Aquaculture": "Aquaculture",
    "Arcadia": "Arcadia",
    "Arcadia Spawn": "Arcadia Spawn",
    "Arcadia Prestige": "Arcadia Prestige",
    "Ars Additions": "Ars Additions",
    "Ars Creo": "Ars Creo",
    "Ars Technica": "Ars Technica",
    "Ars Nouveau's Flavors & Delight": "Saveurs & Délices d'Ars Nouveau",
    "Artifacts": "Artifacts",
    "Balm": "Balm",
    "Barbeque's Delight": "Barbeque's Delight",
    "Bells & Whistles": "Bells & Whistles",
    "Better Archeology": "Better Archeology",
    "Better Combat": "Better Combat",
    "BetterF3": "BetterF3",
    "Better Third Person": "Better Third Person",
    "Biomes O' Plenty": "Biomes O' Plenty",
    "BuildingGadgets2": "BuildingGadgets2",
    "Building Gadgets 2": "Building Gadgets 2",
    "Burger Mod": "Burger Mod",
    "Cable Facades": "Cable Facades",
    "Charging Gadgets": "Charging Gadgets",
    "Chat Heads": "Chat Heads",
    "Chef": "Chef",
    "Chipped": "Chipped",
    "Comforts": "Comforts",
    "ComputerCraft": "ComputerCraft",
    "Copper Deco": "Copper Deco",
    "Corn Delight": "Corn Delight",
    "Corpse": "Corps",
    "Items": "Objets",
    "Normal": "Normal",
    "CosmeticArmours": "CosmeticArmours",
    "CosmeticWeapons": "CosmeticWeapons",
    "AestheticArmaments": "AestheticArmaments",
    "ElegantArmaments": "ElegantArmaments",
    "​AestheticArmaments": "​AestheticArmaments",
    "Crabber's Delight": "Crabber's Delight",
    "Crate Delight": "Crate Delight",
    "Create: Aquatic Ambitions": "Create: Aquatic Ambitions",
    "Create: Central Kitchen": "Create: Central Kitchen",
    "Create: Connected": "Create: Connected",
    "Create: Easy Structures": "Create: Easy Structures",
    "Create: Enchantment Industry": "Create: Enchantment Industry",
    "Create: Hypertube": "Create: Hypertube",
    "Create: Integrated Farming": "Create: Integrated Farming",
    "Create: Diesel Generators": "Create: Diesel Generators",
    "Create Mechanical Extruder": "Create Mechanical Extruder",
    "Create Ender Transmission": "Create Ender Transmission",
    "Create Encased": "Create Encased",
    "Create : Encased": "Create : Encased",
    "Create": "Create",
    "Create Nuclear": "Create Nuclear",
    "Create Ore Excavation": "Create Ore Excavation",
    "Critter Armory": "Critter Armory",
    "Cuisine Delight": "Cuisine Delight",
    "Cultural Delights": "Cultural Delights",
    "Curios": "Curios",
    "Curio": "Curio",
    "Bracelet": "Bracelet",
    "Customizable Elytra": "Customizable Elytra",
    "Deeper and Darker": "Deeper and Darker",
    "Design n' Decor": "Design n' Decor",
    "Dusty Decor": "Dusty Decor",
    "Dusty Decorations": "Dusty Decorations",
    "Ecologics": "Ecologics",
    "Emojiful": "Emojiful",
    "Emotecraft": "Emotecraft",
    "Ender's Delight": "Ender's Delight",
    "End's Delight": "End's Delight",
    "EntityCulling": "EntityCulling",
    "Exposure": "Exposure",
    "Farmer's Delight": "Farmer's Delight",
    "Flux Networks": "Flux Networks",
    "FramedBlocks": "FramedBlocks",
    "FTB Chunks": "FTB Chunks",
    "FTB Filter System": "FTB Filter System",
    "FTB Teams": "FTB Teams",
    "Immersive Aircraft": "Immersive Aircraft",
    "Iris": "Iris",
    "Iron's Spells 'n Spellbooks": "Iron's Spells 'n Spellbooks",
    "Inventory Tweaks ReFoxed": "Inventory Tweaks ReFoxed",
    "Jade": "Jade",
    "Knight Quest": "Knight Quest",
    "Macaw's Bridges": "Macaw's Bridges",
    "Macaw's Doors": "Macaw's Doors",
    "Macaw's Fences & Walls": "Macaw's Fences & Walls",
    "Macaw's Furniture": "Macaw's Furniture",
    "Macaw's Paths & Pavings": "Macaw's Paths & Pavings",
    "Macaw's Roofs": "Macaw's Roofs",
    "Macaw's Stairs and Balconies": "Macaw's Stairs and Balconies",
    "Macaw's Trapdoors": "Macaw's Trapdoors",
    "Macaw's Windows": "Macaw's Windows",
    "Macaw's Windows Additions": "Macaw's Windows Additions",
    "Mechanicals": "Mechanicals",
    "Mekanism: Generators": "Mekanism: Generators",
    "Mekanism: Tools": "Mekanism: Tools",
    "ModernFix": "ModernFix",
    "Mowzie's Mobs": "Mowzie's Mobs",
    "Nature's Compass": "Nature's Compass",
    "Numismatics": "Numismatics",
    "Observable": "Observable",
    "Ocean's Delight": "Ocean's Delight",
    "ParCool!": "ParCool!",
    "ParCool": "ParCool",
    "Particle Core": "Particle Core",
    "Placebo": "Placebo",
    "Rechiseled": "Rechiseled",
    "Refined Storage": "Refined Storage",
    "RS Infinity Booster": "RS Infinity Booster",
    "SecurityCraft": "SecurityCraft",
    "Selfexpression": "Selfexpression",
    "Selfexpression: New Edge": "Selfexpression: New Edge",
    "Simple Hats": "Simple Hats",
    "Simply Swords": "Simply Swords",
    "Simply Tooltips": "Simply Tooltips",
    "Sophisticated Backpacks": "Sophisticated Backpacks",
    "Sophisticated Core": "Sophisticated Core",
    "Sophisticated Mods": "Sophisticated Mods",
    "Sophisticated Storage": "Sophisticated Storage",
    "Sophisticated Storage In Motion": "Sophisticated Storage In Motion",
    "Spice of Life Onion": "Spice of Life Onion",
    "Spyglass Improvements": "Spyglass Improvements",
    "Storage Delight": "Storage Delight",
    "Twilight Additions": "Twilight Additions",
    "Twilight's Flavors & Delight": "Saveurs & Délices de la Forêt Crépusculaire",
    "Twilight Flavors & Delight": "Saveurs & Délices de la Forêt Crépusculaire",
    "Trail&Tales Delight": "Trail&Tales Delight",
    "Torchmaster": "Torchmaster",
    "Twilight Forest: Bosses Resurrection": "Twilight Forest: Bosses Resurrection",
    "Create: The Factory Must Grow": "Create: The Factory Must Grow",
    "Waystones": "Waystones",
    "Waystone": "Pierre du voyage",
    "WaterFrames": "WaterFrames",
    "TrashSlot": "TrashSlot",
    "WorldEdit Items": "WorldEdit Items",
    "MIMI - Musical Instrument Minecraft Interface": "MIMI - Interface d'instruments de musique Minecraft",
    "Inventory": "Inventaire",
    "Just Zoom": "Just Zoom",
    "JEI (Overlays)": "JEI (Surcouches)",
    "JEI (Recipes)": "JEI (Recettes)",
    "JEI (Cheat Mode)": "JEI (Mode triche)",
    "JEI (Edit Mode)": "JEI (Mode édition)",
    "JEI (Search Filter)": "JEI (Filtre de recherche)",
    "JEI (Dev Tools)": "JEI (Outils dev)",
    "Interface": "Interface",

    # ====== Music / paintings ======
    "Noisestorm - Aether Tune": "Noisestorm - Aether Tune",
    "Emile van Krieken - Ascending Dawn": "Emile van Krieken - Ascending Dawn",
    "RENREN - chinchilla": "RENREN - chinchilla",
    "RENREN - high": "RENREN - high",
    "sunsette - klepto": "sunsette - klepto",
    "Emile van Krieken - A Morning Wish": "Emile van Krieken - A Morning Wish",
    "Quizzly - Above The Rain": "Quizzly - Above The Rain",
    "Aethyus - atta": "Aethyus - atta",
    "Quizzly - Cyclone": "Quizzly - Cyclone",
    "Aethyus - fænt": "Aethyus - fænt",
    "Aethyus - himininn": "Aethyus - himininn",
    "Emile van Krieken - Nabooru": "Emile van Krieken - Nabooru",
    "Kevin MacLeod - Casa Bossa Nova": "Kevin MacLeod - Casa Bossa Nova",
    "zeroregard - pocket factory": "zeroregard - pocket factory",
    "Pedro Ricardo": "Pedro Ricardo",
    "Plantkillable": "Plantkillable",
    "Gootastic": "Gootastic",
    "Kirill_Burnside": "Kirill_Burnside",
    "Limo_naranjo3008": "Limo_naranjo3008",

    # ====== mowziesmobs entities ======
    "Foliaath": "Foliaath",
    "Ferrous Wroughtnaut": "Maître Ferreux",
    "Umvuthana": "Umvuthana",
    "Frostmaw": "Frostmaw",
    "Grottol": "Grottol",
    "Naga": "Naga",
    "Boulder": "Rocher",
    "Bluff": "Faux-Semblant",
    "Mobs": "Mobs",
    "Sol Visage": "Visage du Soleil",
    "Heliomancer": "Héliomancien",
    "minutes": "minutes",

    # ====== aether entities ======
    "Phyg": "Phyg",
    "Slider": "Slider",
    "Valkyrie": "Valkyrie",
    "Ice Bucket Armor": "Armure de seau de glace",
    "Snoozebuncle": "Snoozebuncle",
    "Rune": "Rune",
    "Starbuncle": "Starbuncle",
    "source": "source",

    # ====== twilightforest ======
    "Trollber": "Trollber",
    "Trollsteinn": "Trollsteinn",
    "Trollvidr": "Trollvidr",
    "Kobold": "Kobold",
    "Minoshroom": "Minoshroom",
    "Troll": "Troll",
    "Ur-Ghast": "Ur-Ghast",
    "Carminite": "Carminite",
    "Maloberry": "Malobaie",
    "Tannin": "Tannin",
    "Sortingwood": "Bois de tri",

    # ====== sodium ======
    "Simple": "Simple",
    "Dynamic Lights": "Lumières dynamiques",

    # ====== chipped ======
    "Autumnkin": "Autumnkin",
    "Dewkin": "Dewkin",
    "Glassblower": "Souffleur de verre",
    "Goldkin": "Goldkin",
    "Kabotchkin": "Kabotchkin",
    "Pimpkin": "Pimpkin",
    "Rosekin": "Rosekin",
    "Barrels": "Tonneaux",
    "Bookshelves": "Bibliothèques",
    "Calcite": "Calcite",
    "Diorite": "Diorite",
    "Granite": "Granite",
    "Ladders": "Échelles",
    "Lanterns": "Lanternes",
    "Melons": "Melons",
    "Netherrack": "Netherrack",
    "Prismarine": "Prismarine",
    "Shroomlights": "Champilumières",
    "Torches": "Torches",
    "Craft": "Fabriquer",
    "Vertical": "Vertical",

    # ====== createnuclear ======
    "Autunite": "Autunite",
    "Uranium": "Uranium",
    "Danger": "Danger",
    "Radiation": "Radiation",
    "Yellowcake": "Yellowcake",

    # ====== createdieselgenerators ======
    "Biodiesel": "Biodiesel",
    "Diesel": "Diesel",
    "Ethanol": "Éthanol",
    "Gasoline": "Essence",
    "Sheet Metal Panel": "Panneau en tôle",
    "Distillation": "Distillation",
    "Burner Strength: %1$s": "Puissance du brûleur : %1$s",
    "Finding an Oil Chunk": "Trouver une nappe de pétrole",
    "Once you assemble the contraption ...": "Une fois la contraption assemblée...",
    "... you can extract the crude oil with a Mechanical Pump.": "... vous pouvez extraire le pétrole brut avec une Pompe mécanique.",
    "... finally, attach a Pumpjack Hole": "... enfin, attachez un trou de pompage",

    # ====== createaddition ======
    "Passive": "Passif",
    "None": "Aucun",
    "Accumulator": "Accumulateur",
    "High Current": "Courant élevé",

    # ====== Refined Storage ======
    "10 years!": "10 ans !",
    "Alternatives": "Alternatives",
    "%d total": "%d au total",

    # ====== arcadia_pets / arcadia_prestige ======
    "⚙ Arcadia Hub ⚙": "⚙ Arcadia Hub ⚙",
    "⚙ HUD Layout": "⚙ Disposition HUD",
    "✨ Evo: Tier II ★ MAX": "✨ Évo : Tier II ★ MAX",
    "Twerk": "Twerk",
    "Hotfix": "Hotfix",
    "✨ Pocket": "✨ Poche",
    "Aftershock": "Réplique",
    "⚡ Aftershock": "⚡ Réplique",
    "🐾 Portrait": "🐾 Portrait",
    "Champion": "Champion",
    "Jackpot": "Jackpot",
    "Invincible": "Invincible",
    "Slot %s": "Emplacement %s",
    "⚔ ELO & Duels": "⚔ ELO & Duels",
    "❆ Arcadia Prestige ❆": "❆ Arcadia Prestige ❆",
    "Aura": "Aura",
    "Dragon": "Dragon",
    "Pulsar": "Pulsar",
    "Nova": "Nova",
    "Sakura": "Sakura",
    "Spawn": "Spawn",
    "Lootbox": "Lootbox",
    "Homes": "Résidences",
    "Permanent": "Permanent",

    # ====== farmersdelight items ======
    # Already covered in items list

    # ====== knightquest ======
    "Uchigatana": "Uchigatana",
    "Kukri": "Kukri",
    "Gremlin": "Gremlin",
    "Bad Patch": "Bad Patch",
    "Lizzy": "Lizzy",
    "Samhain": "Samhain",
    "Swampman": "Homme des marais",
    "Ratman": "Homme-rat",

    # ====== iron's spells / simply swords ======
    "Claymore": "Claymore",
    "%d Mana/s": "%d Mana/s",
    "%d Mana": "%d Mana",
    "%d Projectiles": "%d Projectiles",
    "Ender": "Ender",
    "Nature": "Nature",
    "Ascension": "Ascension",
    "Acupuncture": "Acupuncture",
    "Wololo": "Wololo",
    "Sacrifice": "Sacrifice",
    "Immolation": "Immolation",
    "Potion": "Potion",
    "Necronomicon": "Necronomicon",
    "Intelligent": "Intelligent",
    "Mithril": "Mithril",
    "Pyrium": "Pyrium",
    "Stormbringer": "Stormbringer",
    "Mjolnir": "Mjolnir",
    "Livyatan": "Livyatan",
    "Enigma": "Énigme",
    "Caelestis": "Caelestis",
    "Resilience": "Résilience",
    "◆  Berserk": "◆  Berserk",
    " §dArcane": " §dArcane",
    "§6[Livyatan]§7": "§6[Livyatan]§7",
    "§6[Caelestis]§7": "§6[Caelestis]§7",
    "§6[Chomp'olotl]§7": "§6[Chomp'olotl]§7",
    "§b[Poison]§7": "§b[Poison]§7",

    # ====== easy_npc ======
    "Allay": "Allay",
    "Creeper": "Creeper",
    "Doppler": "Doppler",
    "Enderman": "Enderman",
    "Ghast": "Ghast",
    "Piglin": "Piglin",

    # ====== createframed ======
    "Pulpification": "Pulpification",

    # ====== mimi instruments ======
    "Kalimba": "Kalimba",
    "Ocarina": "Ocarina",
    "Trombone": "Trombone",
    "Tuba": "Tuba",
    "Banjo": "Banjo",
    "Harmonica": "Harmonica",
    "Piccolo": "Piccolo",
    "Glockenspiel": "Glockenspiel",
    "Xylophone": "Xylophone",
    "Vibraphone": "Vibraphone",
    "Marimba": "Marimba",
    "Didgeridoo": "Didgeridoo",
    "Piano": "Piano",
    "Triangle": "Triangle",
    "Vielle": "Vielle",

    # ====== deeperdarker ======
    "Shattered": "Shattered",
    "Stalker": "Stalker",
    "Abstraction": "Abstraction",
    "Adventure": "Aventure",
    "Back to Your Roots": "Retour aux sources",
    "Clouds": "Nuages",
    "Echoer": "Echoer",
    "Millipede": "Mille-pattes",
    "Ooze": "Suintement",

    # ====== aether2 / deep_aether ======
    "Clorite": "Clorite",
    "Iaspove": "Iaspove",

    # ====== exposure ======
    "Spooky Silly Skeletons": "Squelettes idiots et effrayants",

    # ====== amendments dyes ======
    "Orange": "Orange",
    "Magenta": "Magenta",
    "Cyan": "Cyan",
    "Cobalt": "Cobalt",
    "Beige": "Beige",
    "Jade": "Jade",

    # ====== bookshelf time units ======
    "Tick": "Tick",
    "Ticks": "Ticks",
    "Minute": "Minute",
    "Minutes": "Minutes",
    "Village - Temple": "Village - Temple",

    # ====== ftbessentials ======
    "%s kit(s)": "%s kit(s)",

    # ====== fluxnetworks ======
    "Flux Networks": "Flux Networks",

    # ====== chipped extras handled above ======

    # ====== ftblibrary ======
    "Info": "Info",

    # ====== sodium ======
    # Already covered

    # ====== sound_physics ======
    # Already covered

    # ====== voicechat ======
    # Already covered

    # ====== easyNPC config UI ======
    # Already covered

    # ====== other ======
    "Modonomicon": "Modonomicon",
    "Condition Root": "Racine de condition",
    "Compa...": "Compa...",
    "Jukebox": "Jukebox",
    "Batt.": "Batt.",
    "Tags": "Tags",
    "Restock": "Réapprovisionner",
    "Inception": "Inception",
    "<unnamed>": "<sans nom>",
    "You touch the waystone, but nothing happens.": "Vous touchez la pierre du voyage, mais rien ne se passe.",
    "Icons by JoeCreates (CC-BY-SA 3.0)": "Icônes par JoeCreates (CC-BY-SA 3.0)",
    "Orange Sharestone": "Pierre partagée orange",
    "Magenta Sharestone": "Pierre partagée magenta",
    "Cyan Sharestone": "Pierre partagée cyan",

    # ====== supplementaries ======
    "Cage": "Cage",
    "Globe": "Globe",
    "Lumisene": "Luminescène",
    "Pancake": "Crêpe",
    "Supplementaries": "Supplementaries",

    # ====== tfmg ======
    "Bauxite": "Bauxite",
    "Lignite": "Lignite",
    "Napalm": "Napalm",
    "Rotor": "Rotor",
    "Stator": "Stator",
    "Butane": "Butane",
    "Propane": "Propane",
    "Transistor": "Transistor",
    "Transmission": "Transmission",
    "Turbo": "Turbo",
    "Boxer": "Boxer",
    "Radial": "Radial",
    "Turbine": "Turbine",

    # ====== reactor / mekanismgenerators ======
    "Plasma: %1$s": "Plasma : %1$s",
    "Activation": "Activation",
    "Tritium": "Tritium",
    "Production: %1$s": "Production : %1$s",
    "Production": "Production",

    # ====== exposure_catalog ======
    "§8[Ctrl+E]": "§8[Ctrl+E]",
    "§8[Ctrl+M]": "§8[Ctrl+M]",
    "§8[Ctrl+R]": "§8[Ctrl+R]",
    "§8[Ctrl+F]": "§8[Ctrl+F]",

    # ====== fzzy_config ======
    "Ctrl + %s": "Ctrl + %s",
    "Ctrl %s": "Ctrl %s",
    "Ctrl Alt %s": "Ctrl Alt %s",
    "Ctrl": "Ctrl",

    # ====== various comments ======
    "Config Related Below": "Lié à la configuration ci-dessous",
    "Guidebook": "Guide",
    "Advancements": "Progrès",
    "Debug (for a debug mode, do not need translation)": "Debug (pour un mode debug, traduction non nécessaire)",
    "JEI Compat": "Compatibilité JEI",
    "Go Fish support https://www.curseforge.com/minecraft/mc-mods/go-fish": "Support Go Fish https://www.curseforge.com/minecraft/mc-mods/go-fish",
    "Shields+ https://www.curseforge.com/minecraft/mc-mods/shieldsplus": "Shields+ https://www.curseforge.com/minecraft/mc-mods/shieldsplus",
    "Grapple Mod https://www.curseforge.com/minecraft/mc-mods/grappling-hook-mod": "Grapple Mod https://www.curseforge.com/minecraft/mc-mods/grappling-hook-mod",
    "This is for Revive item description": "Description de l'objet Revive",
    "#Moon Phases": "#Phases lunaires",
    "Only for testing:": "Pour tests uniquement :",

    # ====== fancymenu / branding ======
    "Apothic Spawners": "Apothic Spawners",
    "Eterna, Quanta, Arcana": "Eterna, Quanta, Arcana",
    "Quanta": "Quanta",
    "Arcana": "Arcana",
    "Infusion": "Infusion",
    "Agile": "Agile",
    "netherite": "netherite",
    "Trident": "Trident",
    "Tridents": "Tridents",
    "Chronicle of Shadows": "Chronique des Ombres",
    "Guide to Apotheosis": "Guide d'Apotheosis",

    # ====== chat / messages ======
    "[§aBotany Pots§r] %s": "[§aBotany Pots§r] %s",
    "[KubeJS Tweaks] %s": "[KubeJS Tweaks] %s",
    "Comforts Networking Failure: %s": "Échec réseau Comforts : %s",
    "%s (max)": "%s (max)",
    "%s (via §d§nCristel Lib§r)": "%s (via §d§nCristel Lib§r)",

    # ====== refurbished_furniture ======
    "Paddle Ball": "Jeu de raquettes",
    "Marketplace": "Place de marché",
    "Coin Miner": "Mineur de pièces",

    # ====== exposure ======
    "Photograph": "Photographie",

    # ====== spiffyhud ======
    "Hotbar": "Barre d'accès rapide",

    # ====== strawstatues ======
    # Cape covered

    # ====== voicechat ======
    # Audio + Normal covered

    # ====== ParCool action.Tap ======
    # Above

    # ====== aether jukebox handled ======

    # ====== Snoozebuncle title etc handled ======

    # ====== pocket / turtle ======
    "Chatty": "Chatty",
    "Colony": "Colonie",
    "Chunky": "Chunky",
    "Compass": "Boussole",

    # ====== ars_additions ======
    # rune/starbuncle handled

    # ====== Crabber's Delight already ======

    # ====== Apotheosis enchanting ======
    " - Quanta: %s%%": " - Quanta : %s%%",
    " - Arcana: %s%%": " - Arcana : %s%%",
    " - Quanta: +%s%%": " - Quanta : +%s%%",
    " - Arcana: +%s%%": " - Arcana : +%s%%",
    "Quanta: %s%%": "Quanta : %s%%",
    "Arcana: %s%%": "Arcana : %s%%",

    # ====== ftbteams ======
    # Description covered

    # ====== framedblocks ======
    # Texture covered

    # ====== misc ======
    "FTB Chunks": "FTB Chunks",
    "Tinkers' Construct": "Tinkers' Construct",
    "Deep Resonance": "Deep Resonance",
    "Lootr": "Lootr",
    "9minecraft": "9minecraft",
    "CurseForge": "CurseForge",
    "Modrinth": "Modrinth",
    "Bastion [ATM]": "Bastion [ATM]",

    # ====== aquaculturedelight ======
    "Aquaculture Delight": "Aquaculture Delight",

    # ====== mvs ======
    # CurseForge / Modrinth above

    # ====== misc tooltips ======
    "&7Upgrade for turtles, that allows basic interaction with the world and teleportation in one dimension.": "&7Amélioration pour tortues, permettant l'interaction de base avec le monde et la téléportation dans une seule dimension.",
    "&7Can detect energy flow and acts as a resistor.": "&7Peut détecter le flux d'énergie et agit comme une résistance.",
    "&7Upgrade for turtles, that allows basic and advanced interactions with animals.": "&7Amélioration pour tortues, permettant des interactions de base et avancées avec les animaux.",
    "&7Upgrade for turtles, which makes turtles more useful.": "&7Amélioration qui rend les tortues plus utiles.",

    # ====== advancements ======
    "Is this core gluten-free?": "Ce noyau est-il sans gluten ?",
    "Collect a NBT storage and block reader. Now, all the world's secrets are open to you!": "Collectez un stockage NBT et un lecteur de blocs. Tous les secrets du monde s'offrent à vous !",
    "Every journey starts with the first block": "Tout voyage commence par le premier bloc",
    "The truth can't hide forever": "La vérité ne peut se cacher éternellement",
    "Does the afterlife exist in minecraft?": "L'au-delà existe-t-il dans Minecraft ?",
    "Geo Scanner": "Scanner géologique",
    "ME Bridge": "Pont ME",
    "RS Bridge": "Pont RS",
    "Computer Tool": "Outil informatique",
    "Snap!": "Clac !",
    "Lumen Nexus": "Nexus de Lumen",
    "Points": "Points",
    "Pulpification": "Pulpification",
    "Hopkirk": "Hopkirk",
    "Rosa Aurea": "Rosa Aurea",
    "Money Money Money,": "Money Money Money,",
    "Happy Feet": "Happy Feet",
    "Apothic Spawners": "Apothic Spawners",

    # ====== twilight_additions / various tabs ======
    # Already

    # ====== another_furniture ======
    "Another Furniture": "Another Furniture",
    "Extra": "Extra",

    # ====== amendments handled ======

    # ====== misc ======
    "Cosmetic Hunters": "Cosmetic Hunters",
    "Apothic Attributes": "Apothic Attributes",

    # ====== ars_technica ======
    "~%d source / %d": "~%d source / %d",
    "Transmutation": "Transmutation",

    # ====== keybindings labels (mod names) ======
    "Apotheosis": "Apotheosis",
    "Curios": "Curios",
    "Iris": "Iris",

    # ====== framedblocks specific ======

    # ====== easy_npc / easy_npc_config_ui handled ======

    # ====== exposure_polaroid ======
    # Zoom covered

    # ====== farmersdelight handled ======

    # ====== solonion ======
    # Covered

    # ====== fancymenu skipped ======

    # ====== ftbquests skipped ======

    # ====== cosmetic mods ======
    # All proper noun-like, kept

    # ====== refurbished_furniture handled ======

    # ====== misc misc ======
    "Spell Power": "Puissance de sort",
    "Mode": "Mode",

    # ====== aether jukebox covered ======

    # ====== effect.arsdelight.wilden ======
    "Wilden": "Wilden",

    # ====== misc placebo etc ======
    "Placebo": "Placebo",

    # ====== ftbessentials kit covered ======

    # ====== expression ======
    "Expression": "Expression",

    # ====== twilightdelight ======
    # Title covered

    # ====== sodium options ======
    "Vignette": "Vignette",

    # ====== misc waterframes ======
    "Projection": "Projection",

    # ====== voidtotem ======
    "Charm": "Breloque",

    # ====== mutantmonsters ======
    "Explosion": "Explosion",

    # ====== createendertransmission ======
    # Covered

    # ====== createcasing covered ======

    # ====== createnuclear covered ======

    # ====== misc supplementaries ======
    "Bombs": "Bombes",

    # ====== farmersdelight already ======

    # ====== invtweaks ======
    # Covered

    # ====== chargingadgets ======
    "Charging Gadgets": "Charging Gadgets",

    # ====== arcadiaadminpanel ======
    # Homes / Permanent covered

    # ====== more ======
    "Pizza Margherita": "Pizza Margherita",

    # ====== easy_npc_config_ui ======
    "Distance": "Distance",
    "Animation": "Animation",
    "Combat": "Combat",
    "Conditions": "Conditions",

    # ====== mcwwindows ======
    "Iron Bars Toggles": "Activation des barreaux en fer",

    # ====== mechanical_botany ======
    # Compost covered

    # ====== particle ======
    # Cascades
    "Cascades": "Cascades",

    # ====== owo ======
    # Sections covered

    # ====== sophisticatedstorage ======
    "Acacia": "Acacia",
    "Crimson": "Carmin",
    "Glowstone": "Pierre lumineuse",
    "Jungle": "Jungle",
    "Lapis Lazuli": "Lapis Lazuli",
    "Netherite": "Netherite",

    # ====== immersive_paintings ======
    "Pixelart": "Pixel Art",
    "%s%% dither": "%s%% tramage",
    "%s%% X offset": "%s%% décalage X",
    "%s%% Y offset": "%s%% décalage Y",
    "%s%% zoom": "%s%% zoom",
    "Datapacks": "Packs de données",
    "Vintage": "Vintage",
    "Graffiti": "Graffiti",
    "Thumbnail Size": "Taille des miniatures",

    # ====== createaddition tooltips ======
    # Already covered

    # ====== refinedstorage ======
    # Already covered

    # ====== Alhoon / hats ======
    "Artsy": "Artsy",
    "Aegis": "Égide",
    "Peppino": "Peppino",
    "The Noise": "The Noise",
    "Alhoon": "Alhoon",
    "Octodad": "Octodad",

    # ====== refurbished computer ======
    # Covered

    # ====== knightquest ======
    # Covered

    # ====== mowziesmobs effects ======
    # Covered

    # ====== ars_additions handled ======

    # ====== buildinggadgets2 ======
    "Surface": "Surface",
    "Render Block (DO NOT USE)": "Bloc de rendu (NE PAS UTILISER)",

    # ====== createendertransmission ======
    # Title only

    # ====== createnuclear ======
    # Above

    # ====== creategoggles tooltips - keep as item.X.X ======

    # ====== category ======
    "Category": "Catégorie",

    # ====== misc tab labels keep mod-name ======

    # ====== example_mod ======
    "client": "client",

    # ====== modernfix ======
    # Covered

    # ====== modonomicon ======
    # Covered

    # ====== ftbteams gui.create_party / Description / etc ======
    # Description covered

    # ====== curios ======
    # Covered

    # ====== createnuclear effect ======
    # Covered

    # ====== mowziesmobs grant_suns_blessing.text.1 ======
    # minutes -> minutes (kept)

    # ====== ftbchunks already ======

    # ====== mvs ======
    # Covered

    # ====== modonomicon book ======
    # Covered

    # ====== craftpresence ======
    # Refresh Rate covered

    # ====== sodium ======
    # Covered

    # ====== sodiumextras ======
    # Covered

    # ====== sound_physics_remastered ======
    # Performance covered

    # ====== solonion ======
    # Covered

    # ====== arcadia_lib hub ======
    # Covered

    # ====== arcadia_spawn hub.title ======
    # Covered

    # ====== arcadialootbox ======
    # Covered

    # ====== resourcefulconfig ======
    # Wiki covered

    # ====== fzzy_config search modifier ======
    # Covered

    # ====== exposure album ======
    # Note covered

    # ====== exposure photograph generation ======
    # Original covered

    # ====== arcadiaadminpanel detail ======
    # Covered

    # ====== rarities ======
    # Rare covered

    # ====== chat heads / chat ======
    # Covered

    # ====== balm ======
    "Balm": "Balm",

    # ====== bookshelf  ======
    # Covered above

    # ====== smiles ======

    # ====== blocks of dndecor ======
    "Gabbro": "Gabbro",

    # ====== misc fix ======
    "FTB Filter System": "FTB Filter System",
    "Filter": "Filtre",

    # ====== more ======
    "Trail&Tales Delight": "Trail&Tales Delight",

    # ====== twilightforest carminite/maloberry covered ======

    # ====== mod-name keep as-is ======
    "Apothic Enchanting": "Apothic Enchanting",

    # ====== buildinggadgets2 ======
    # Above

    # ====== Snoozebuncle handled ======

    # ====== another_furniture ======
    # Above

    # ====== Knight Quest handled ======

    # ====== invtweaks ======
    # Above

    # ====== iris ======
    # Above

    # ====== entityculling ======
    # Above

    # ====== modonomicon ======
    # Above

    # ====== misc placeable_food ======
    # Pizza Margherita above

    # ====== misc ======
    "Information": "Informations",

    # ====== occultengineering ======
    "Phlogiport": "Phlogiport",
    "Phlogiston": "Phlogiston",
    "Púcalith": "Púcalith",
    "Pentacles": "Pentacles",
    "Occult Engineering": "Occult Engineering",
    "- [*Phlogiport*](entry://occultengineering:encyclopedia_of_souls/getting_started/phlogiport)\n": "- [*Phlogiport*](entry://occultengineering:encyclopedia_of_souls/getting_started/phlogiport)\n",

    # ====== ftbchunks etc ======
    "Axolotls": "Axolotls",

    # ====== create_jetpack / immersive_aircraft ======
    "Jetpack": "Jetpack",
    "Quadrocopter": "Quadrocopter",
    "Gyroscope": "Gyroscope",

    # ====== sophisticated client ======
    "Client": "Client",

    # ====== advancednetherite ======
    "Instructions": "Instructions",

    # ====== arcadia_prestige staff names ======
    "§cJLPopeye §8(§4Admin§8)": "§cJLPopeye §8(§4Admin§8)",
    "§cYoupaX §8(§4Admin§8)": "§cYoupaX §8(§4Admin§8)",
    "§cSkaizenn §8(§4Admin§8)": "§cSkaizenn §8(§4Admin§8)",
    "§aBeuzed §8(§2Guide§8)": "§aBeuzed §8(§2Guide§8)",
    "§aNokhXyr §8(§2Guide§8)": "§aNokhXyr §8(§2Guide§8)",
    "§aSea6945 §8(§2Helper§8)": "§aSea6945 §8(§2Helper§8)",
    "§aRayser56 §8(§2Helper§8)": "§aRayser56 §8(§2Helper§8)",
    "§aNathinator_YTB §8(§2Helper§8)": "§aNathinator_YTB §8(§2Helper§8)",

    # ====== betterf3 ======
    "%s fps / %s fps %s": "%s fps / %s fps %s",
    "total": "total",
    "Shader": "Shader",
    "maximum": "maximum",
    "Off-Heap": "Off-Heap",

    # ====== biomesoplenty ======
    "Bayou": "Bayou",
    "Prairie": "Prairie",
    "Rose": "Rose",

    # ====== cloth-config2 ======
    "No Alpha Allowed!": "Alpha non autorisé !",
    "Not a valid value! (Alpha)": "Valeur invalide ! (Alpha)",
    "Not a valid value! (Red)": "Valeur invalide ! (Rouge)",
    "Not a valid value! (Green)": "Valeur invalide ! (Vert)",
    "Not a valid value! (Blue)": "Valeur invalide ! (Bleu)",
    "Not a valid color!": "Couleur invalide !",
    "Not a valid color! (Missing #)": "Couleur invalide ! (# manquant)",

    # ====== colorfulhearts ======
    "Colorful Hearts": "Colorful Hearts",
    "Absorption": "Absorption",

    # ====== computercraft ======
    "Proxy": "Proxy",
    "Port": "Port",

    # ====== create_things_and_misc ======
    "Create 2 0 2 2": "Create 2 0 2 2",
    "<BNBT:text:SpeakerText>": "<BNBT:text:SpeakerText>",
    "klaxon": "klaxon",

    # ====== creategoggles tooltips (literal placeholders) ======
    "item.CHAINMAIL_BACKTANK": "item.CHAINMAIL_BACKTANK",
    "item.DIAMOND_BACKTANK": "item.DIAMOND_BACKTANK",
    "item.GOGGLE_CARDBOARD_HELMET": "item.GOGGLE_CARDBOARD_HELMET",
    "item.GOGGLE_CHAINMAIL_HELMET": "item.GOGGLE_CHAINMAIL_HELMET",
    "item.GOGGLE_DIAMOND_HELMET": "item.GOGGLE_DIAMOND_HELMET",
    "item.GOGGLE_DIVING_HELMET": "item.GOGGLE_DIVING_HELMET",
    "item.GOGGLE_GOLDEN_HELMET": "item.GOGGLE_GOLDEN_HELMET",
    "item.GOGGLE_IRON_HELMET": "item.GOGGLE_IRON_HELMET",
    "item.GOGGLE_LEATHER_HELMET": "item.GOGGLE_LEATHER_HELMET",
    "item.GOGGLE_NETHERITE_DIVING_HELMET": "item.GOGGLE_NETHERITE_DIVING_HELMET",
    "item.GOGGLE_NETHERITE_HELMET": "item.GOGGLE_NETHERITE_HELMET",
    "item.GOGGLE_TURTLE_HELMET": "item.GOGGLE_TURTLE_HELMET",
    "item.GOLDEN_BACKTANK": "item.GOLDEN_BACKTANK",
    "item.IRON_BACKTANK": "item.IRON_BACKTANK",
    "item.LEATHER_BACKTANK": "item.LEATHER_BACKTANK",

    # ====== irons_spellbooks tooltip variant ======
    " %d Mana/s": " %d Mana/s",

    # ====== jade themes ======
    "One Probe": "One Probe",
    "Crafting++": "Crafting++",

    # ====== jei debug ======
    "Wooden doors allow you to block monsters from entering your building.\nTesting sentences.": "Les portes en bois permettent de bloquer l'entrée des monstres dans votre bâtiment.\nPhrases de test.",
    "Wooden doors allow you to block monsters from entering your building.\\nTesting sentences.": "Les portes en bois permettent de bloquer l'entrée des monstres dans votre bâtiment.\\nPhrases de test.",
    "Cabinet": "Armoire",
    "Max $number$ FE/t": "Max $number$ FE/t",
    "Clicking on a door changes its state from open to closed and vice versa.": "Cliquer sur une porte change son état d'ouvert à fermé et vice versa.",
    "Wooden doors can be opened/closed via redstone circuits.": "Les portes en bois peuvent être ouvertes/fermées via des circuits de redstone.",
    "Testing %s formatting replacements.": "Test des remplacements de formatage %s.",
    "Testing %s %s formatting replacements.": "Test des remplacements de formatage %s %s.",
    "%s nested": "%s imbriqué",
    "endangered": "menacé",

    # ====== jeresources ======
    "Bonus": "Bonus",

    # ====== justenoughprofessions ======
    "Professions": "Métiers",

    # ====== mynethersdelight ======
    "My Nether's Delight": "My Nether's Delight",

    # ====== notenoughanimations ======
    "Vanilla": "Vanilla",

    # ====== revive_me ======
    "Revive Me!": "Revive Me!",

    # ====== securitycraft ======
    "Laser": "Laser",
    "Mine": "Mine",
    "Protecto": "Protecto",
    "Taser": "Taser",
    "Debug camera reset tracing": "Traçage de la réinitialisation des caméras de débogage",
    "Frame feed view distance": "Distance d'affichage du flux des cadres",
    "Set the radius in which chunks viewed in a frame camera should be loaded and sent to players. If this config has a higher value than the \"view-distance\" server property or the vanilla \"Render Distance\" option of the player requesting the chunks, the smaller value is used instead.": "Définit le rayon dans lequel les chunks visibles via une caméra de cadre doivent être chargés et envoyés aux joueurs. Si cette valeur est supérieure à la propriété serveur \"view-distance\" ou à l'option \"Distance d'affichage\" du joueur, la valeur la plus petite est utilisée à la place.",
    "Team ownership precedence": "Priorité de propriété d'équipe",
    "Vanilla tool block breaking": "Casse de blocs avec outils vanilla",

    # ====== arcadia_pets achievement.no_damage_win.title 'Invincible' covered ======

    # ====== easy_npc Doppler covered ======

    # ====== sophisticated client config covered ======

    # ====== particular cascades covered ======

    # ====== nature's compass already ======

    # ====== refurbished marketplace etc covered ======

    # ====== misc bookshelf chest table ======

    # ====== misc occultengineering ======
    # All covered

    # ====== amendments dyes covered ======

    # ====== misc strings ======
    "Bonus": "Bonus",

    # ====== ftbessentials ======
    # Covered

    # ====== ftbteams ======
    "FTB Teams": "FTB Teams",

    # ====== sophisticatedstorage Acacia covered ======

    # ====== fancymenu skipped ======

    # ====== Apothic ======
    "Apothic Spawners": "Apothic Spawners",

    # ====== mowziesmobs.config Sol Visage covered ======

    # ====== misc ======
    "Audio": "Audio",
}

# Additions for cases not covered as exact match — handled in apply()
SUFFIX_RULES = []  # could add later

GLOSSARY = json.load(open(ROOT.replace('audit2','') + 'glossary_compact.json', encoding='utf-8'))


def lookup(modid: str, key: str, en: str, jar_fr: dict | None) -> str:
    """Translate a single value."""
    # 1. existing FR jar
    if jar_fr and key in jar_fr:
        v = jar_fr[key]
        if isinstance(v, str) and v.strip() and v.strip() != en.strip():
            return v
    # 2. exact-match TRANS
    if en in TRANS:
        return TRANS[en]
    # 3. glossary
    if en in GLOSSARY:
        return GLOSSARY[en]
    # 4. fallback: keep as-is (proper noun / unknown)
    return en


def main():
    os.makedirs(OUT, exist_ok=True)
    files = sorted(os.listdir(SRC))
    process = [f for f in files if f.replace('.json','') not in SKIP and f.endswith('.json')]
    written = 0
    total_keys = 0
    for f in process:
        modid = f.replace('.json','')
        try:
            inp = json.load(open(SRC + f, encoding='utf-8'))
        except Exception as e:
            print(f"FAIL read {f}: {e}")
            continue
        if not isinstance(inp, dict):
            print(f"SKIP {f}: not dict")
            continue
        # try to load jar_fr
        jar_fr = None
        jar_path = JAR_FR + f
        if os.path.exists(jar_path):
            try:
                jar_fr = json.load(open(jar_path, encoding='utf-8'))
            except Exception:
                jar_fr = None
        out = {}
        for k, v in inp.items():
            if not isinstance(v, str):
                out[k] = v
                continue
            out[k] = lookup(modid, k, v, jar_fr)
            total_keys += 1
        # write with tab indent
        with open(OUT + f, 'w', encoding='utf-8', newline='\n') as fout:
            json.dump(out, fout, ensure_ascii=False, indent='\t')
            fout.write('\n')
        written += 1
    print(f"WRITTEN {written} files, {total_keys} keys total")


if __name__ == '__main__':
    main()
