#!/usr/bin/env python3
"""Bulk translate FTB Quests EN -> ES (Spanish) for Arcadia V2.

Strategy:
- Phrase-level dictionary first (longest matches).
- Word-level dictionary for residue.
- Color codes (&x, %s/%d/%1$s) preserved.
- Proper nouns kept as-is.
"""
import json
import re
import os
from pathlib import Path

ROOT = Path(r"C:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/ftbq_audit")
INPUT = ROOT / "full_to_translate_es_es.json"
OUTPUT = ROOT / "full_output" / "es_es.json"

# --------------------------------------------------------------------
# Phrase-level translations (longest first ordering applied later)
# Keys are lowercase patterns, values are Spanish.
# --------------------------------------------------------------------
PHRASES = {
    # Generic instructions
    "click to continue": "Haz clic para continuar",
    "hold w on the item to see it's uses": "Mantén W sobre el objeto para ver sus usos",
    "hold w on the item to see its uses": "Mantén W sobre el objeto para ver sus usos",
    "right click to open": "Clic derecho para abrir",
    "right-click to open": "Clic derecho para abrir",
    "right click": "Clic derecho",
    "left click": "Clic izquierdo",
    "shift right click": "Shift + clic derecho",
    "hold shift": "Mantén Shift",
    "double click": "Doble clic",
    # Action verbs (imperative) - "to X" form often appears in descriptions
    "increases the spell's power": "Aumenta el poder del hechizo",
    "increases spell power": "Aumenta el poder del hechizo",
    "reduces spell power but increases": "Reduce el poder del hechizo pero aumenta",
    "places a magical light source": "Coloca una fuente de luz mágica",
    "names the target": "Asigna un nombre al objetivo",
    "single-use spell scroll": "Pergamino de hechizo de un solo uso",
    "slows down targets": "Ralentiza a los objetivos",
    "accelerates plant growth": "Acelera el crecimiento de las plantas",
    "controls magical servants": "Controla a los sirvientes mágicos",
    "breaks blocks instantly": "Rompe bloques al instante",
    "makes you invisible": "Te vuelve invisible",
    "breaks trees in one go": "Tala árboles de un solo golpe",
    "a basic filter": "Un filtro básico",
    "a more configurable chute": "Una tolva más configurable",
    "give it some power and then scan for oil": "Dale algo de energía y luego escanea en busca de petróleo",
    "finally sleep in the aether": "Por fin duerme en el Aether",
    "makes plates below": "Fabrica placas debajo",
    "teleports you a short distance": "Te teletransporta una corta distancia",
    "when placed in front of": "Cuando se coloca frente a",
    "forged in resonarium, this gear offers superior protection": "Forjado en Resonarium, este equipo ofrece una protección superior",
    "refine resonarium into usable plates": "Refina Resonarium en placas utilizables",
    "you are ready to face greater dangers": "Estás listo para enfrentar mayores peligros",
    "is death itself": "es la muerte misma",
    "this charm is your": "Este amuleto es tu",
    "only hope": "única esperanza",
    "of withstanding the sound that shatters bones": "para resistir el sonido que rompe los huesos",
    # Quest verbs (titles often start with these)
    "find ": "Encuentra ",
    "craft ": "Crea ",
    "create ": "Crea ",
    "build ": "Construye ",
    "defeat ": "Derrota ",
    "kill ": "Mata ",
    "obtain ": "Obtén ",
    "discover ": "Descubre ",
    "complete ": "Completa ",
    "unlock ": "Desbloquea ",
    "collect ": "Recolecta ",
    "gather ": "Recolecta ",
    "explore ": "Explora ",
    "place ": "Coloca ",
    "use ": "Usa ",
    "make ": "Fabrica ",
    "summon ": "Invoca ",
    "fight ": "Combate ",
    "smelt ": "Funde ",
    "brew ": "Prepara ",
    "enchant ": "Encanta ",
    "upgrade ": "Mejora ",
    "tame ": "Doma ",
    "breed ": "Cría ",
    "mine ": "Mina ",
    "harvest ": "Cosecha ",
    "trade ": "Comercia ",
    "fish ": "Pesca ",
    "drink ": "Bebe ",
    "eat ": "Come ",
    "wear ": "Equípate ",
    "equip ": "Equipa ",
    "open ": "Abre ",
    "activate ": "Activa ",
    "power ": "Alimenta ",
    "construct ": "Construye ",
    "assemble ": "Ensambla ",
    "research ": "Investiga ",
    "study ": "Estudia ",
    "read ": "Lee ",
    "learn ": "Aprende ",
    "master ": "Domina ",
    "reach ": "Alcanza ",
    "travel ": "Viaja a ",
    "venture ": "Aventúrate ",
    "enter ": "Entra en ",
    "visit ": "Visita ",
    "slay ": "Aniquila ",
    "vanquish ": "Vence ",
    "conquer ": "Conquista ",
}

# --------------------------------------------------------------------
# Word-level dictionary (case-insensitive whole word)
# --------------------------------------------------------------------
WORDS = {
    # Articles / pronouns / particles
    "the": "el", "a": "un", "an": "un",
    "and": "y", "or": "o", "but": "pero", "of": "de",
    "to": "a", "with": "con", "for": "para", "from": "desde",
    "in": "en", "on": "en", "at": "en", "by": "por",
    "your": "tu", "you": "tú", "yours": "tuyo",
    "this": "este", "that": "ese", "these": "estos", "those": "esos",
    "is": "es", "are": "son", "was": "era", "were": "eran",
    "be": "ser", "been": "sido", "being": "siendo",
    "has": "tiene", "have": "tener", "had": "tenía",
    "can": "puede", "will": "será", "would": "sería", "should": "debería",
    "must": "debe", "may": "puede", "might": "podría",
    "not": "no", "no": "no", "yes": "sí",
    "all": "todo", "every": "cada", "any": "cualquier",
    "some": "algunos", "many": "muchos", "few": "pocos",
    "more": "más", "less": "menos", "most": "la mayoría",
    "very": "muy", "too": "demasiado",
    "also": "también", "only": "solo", "just": "solo",
    "now": "ahora", "then": "entonces", "when": "cuando",
    "where": "donde", "what": "qué", "how": "cómo", "why": "por qué",
    "if": "si", "while": "mientras",
    "before": "antes", "after": "después", "during": "durante",
    "above": "arriba", "below": "abajo", "under": "bajo", "over": "sobre",
    "into": "en", "onto": "sobre", "through": "a través de",
    "between": "entre", "among": "entre", "around": "alrededor de",
    "first": "primero", "second": "segundo", "third": "tercero",
    "next": "siguiente", "previous": "anterior", "last": "último",
    "new": "nuevo", "old": "viejo",
    "good": "bueno", "bad": "malo", "best": "mejor", "worst": "peor",
    "high": "alto", "low": "bajo", "great": "gran",
    "small": "pequeño", "big": "grande", "large": "grande", "huge": "enorme",
    "tiny": "diminuto", "giant": "gigante", "mega": "mega",
    "long": "largo", "short": "corto", "tall": "alto",
    "fast": "rápido", "slow": "lento", "quick": "rápido",
    "strong": "fuerte", "weak": "débil",
    "hot": "caliente", "cold": "frío", "warm": "cálido",
    "deep": "profundo", "shallow": "poco profundo",
    "dark": "oscuro", "light": "luz", "bright": "brillante",
    "easy": "fácil", "hard": "difícil", "difficult": "difícil",
    "simple": "sencillo", "complex": "complejo", "advanced": "avanzado",
    "basic": "básico", "rare": "raro", "common": "común",
    "epic": "épico", "legendary": "legendario", "mythic": "mítico",
    "ancient": "antiguo", "modern": "moderno",
    "magical": "mágico", "magic": "magia", "mystical": "místico",
    "arcane": "arcano", "divine": "divino", "holy": "sagrado",
    "cursed": "maldito", "blessed": "bendito", "evil": "maligno",
    "celestial": "celestial", "infernal": "infernal", "demonic": "demoníaco",
    "elemental": "elemental", "primal": "primigenio",
    "eternal": "eterno", "infinite": "infinito",
    "powerful": "poderoso", "mighty": "poderoso",
    "ultimate": "definitivo", "supreme": "supremo",
    "secret": "secreto", "hidden": "oculto",
    "lost": "perdido", "forgotten": "olvidado",

    # Categories / subjects
    "mod": "mod", "mods": "mods", "modpack": "modpack",
    "quest": "misión", "quests": "misiones",
    "chapter": "capítulo", "chapters": "capítulos",
    "task": "tarea", "tasks": "tareas",
    "reward": "recompensa", "rewards": "recompensas",
    "tutorial": "tutorial", "guide": "guía",
    "tip": "Consejo", "warning": "Advertencia", "note": "Nota",
    "info": "Información", "details": "Detalles",
    "objective": "objetivo", "goal": "meta",
    "progress": "progreso", "stage": "etapa", "phase": "fase",
    "level": "nivel", "tier": "nivel", "rank": "rango",
    "world": "mundo", "dimension": "dimensión",
    "biome": "bioma", "structure": "estructura",
    "village": "aldea", "town": "ciudad", "city": "ciudad",
    "dungeon": "mazmorra", "ruins": "ruinas", "ruin": "ruina",
    "temple": "templo", "tomb": "tumba", "shrine": "santuario",
    "tower": "torre", "castle": "castillo", "fortress": "fortaleza",
    "cave": "cueva", "caves": "cuevas", "mine": "mina", "mines": "minas",
    "ocean": "océano", "sea": "mar", "lake": "lago", "river": "río",
    "forest": "bosque", "jungle": "selva", "desert": "desierto",
    "mountain": "montaña", "mountains": "montañas",
    "swamp": "pantano", "tundra": "tundra", "plains": "llanuras",
    "underground": "subterráneo", "underworld": "inframundo",
    "sky": "cielo", "heaven": "paraíso", "hell": "infierno",
    "nether": "Nether", "end": "End", "overworld": "Overworld",
    "aether": "Aether", "twilight": "Crepúsculo",
    # Combat
    "boss": "jefe", "bosses": "jefes",
    "enemy": "enemigo", "enemies": "enemigos",
    "monster": "monstruo", "monsters": "monstruos",
    "mob": "criatura", "mobs": "criaturas",
    "creature": "criatura", "creatures": "criaturas",
    "beast": "bestia", "beasts": "bestias",
    "dragon": "dragón", "dragons": "dragones",
    "demon": "demonio", "demons": "demonios",
    "ghost": "fantasma", "ghosts": "fantasmas",
    "skeleton": "esqueleto", "skeletons": "esqueletos",
    "zombie": "zombi", "zombies": "zombis",
    "spider": "araña", "spiders": "arañas",
    "creeper": "creeper", "creepers": "creepers",
    "wither": "Wither", "warden": "Warden",
    "golem": "gólem", "golems": "gólems",
    "witch": "bruja", "witches": "brujas",
    "wizard": "mago", "wizards": "magos",
    "knight": "caballero", "knights": "caballeros",
    "warrior": "guerrero", "warriors": "guerreros",
    "hunter": "cazador", "hunters": "cazadores",
    "guardian": "guardián", "guardians": "guardianes",
    # Loot / treasure
    "loot": "botín", "treasure": "tesoro",
    "drop": "drop", "drops": "drops",
    "chest": "cofre", "chests": "cofres",
    "key": "llave", "keys": "llaves",
    "coin": "moneda", "coins": "monedas",
    "gold": "oro", "silver": "plata", "copper": "cobre",
    "iron": "hierro", "diamond": "diamante", "diamonds": "diamantes",
    "emerald": "esmeralda", "emeralds": "esmeraldas",
    "netherite": "netherita",
    "obsidian": "obsidiana", "redstone": "redstone",
    "lapis": "lapislázuli", "quartz": "cuarzo",
    "amethyst": "amatista", "ruby": "rubí", "sapphire": "zafiro",
    "crystal": "cristal", "crystals": "cristales",
    "gem": "gema", "gems": "gemas",
    "ore": "mineral", "ores": "minerales",
    "ingot": "lingote", "ingots": "lingotes",
    "plate": "placa", "plates": "placas",
    "block": "bloque", "blocks": "bloques",
    "item": "objeto", "items": "objetos",
    "tool": "herramienta", "tools": "herramientas",
    "weapon": "arma", "weapons": "armas",
    "armor": "armadura", "armour": "armadura",
    "shield": "escudo", "shields": "escudos",
    "sword": "espada", "swords": "espadas",
    "bow": "arco", "bows": "arcos",
    "crossbow": "ballesta", "crossbows": "ballestas",
    "arrow": "flecha", "arrows": "flechas",
    "axe": "hacha", "axes": "hachas",
    "pickaxe": "pico", "pickaxes": "picos",
    "shovel": "pala", "shovels": "palas",
    "hoe": "azada", "hoes": "azadas",
    "helmet": "casco", "helmets": "cascos",
    "chestplate": "peto", "chestplates": "petos",
    "leggings": "pantalones",
    "boots": "botas",
    "gauntlet": "guantelete", "gauntlets": "guanteletes",
    "ring": "anillo", "rings": "anillos",
    "necklace": "collar", "amulet": "amuleto", "amulets": "amuletos",
    "charm": "amuleto", "charms": "amuletos",
    "talisman": "talismán", "talismans": "talismanes",
    "belt": "cinturón", "cloak": "capa",
    "potion": "poción", "potions": "pociones",
    "scroll": "pergamino", "scrolls": "pergaminos",
    "book": "libro", "books": "libros",
    "tome": "tomo", "tomes": "tomos",
    "spellbook": "grimorio",
    "wand": "varita", "wands": "varitas",
    "staff": "bastón", "staves": "bastones",
    "spell": "hechizo", "spells": "hechizos",
    "glyph": "glifo", "glyphs": "glifos",
    "rune": "runa", "runes": "runas",
    "mana": "Maná",
    "stamina": "resistencia", "energy": "energía",
    "health": "salud", "heart": "corazón", "hearts": "corazones",
    "damage": "daño", "defense": "defensa", "defence": "defensa",
    "attack": "ataque", "speed": "velocidad",
    "strength": "fuerza", "power": "poder",
    "magic": "magia", "magical": "mágico",
    # Common minecraft / mod terms
    "experience": "experiencia", "xp": "EXP",
    "enchanting": "encantamiento", "enchantment": "encantamiento",
    "enchantments": "encantamientos",
    "anvil": "yunque", "furnace": "horno",
    "smithing": "herrería", "smithing table": "mesa de herrería",
    "table": "mesa", "crafting": "fabricación",
    "recipe": "receta", "recipes": "recetas",
    "ingredient": "ingrediente", "ingredients": "ingredientes",
    "material": "material", "materials": "materiales",
    "resource": "recurso", "resources": "recursos",
    "food": "comida", "drink": "bebida",
    "bread": "pan", "meat": "carne", "fish": "pez",
    "vegetable": "verdura", "fruit": "fruta",
    "seed": "semilla", "seeds": "semillas",
    "crop": "cultivo", "crops": "cultivos",
    "plant": "planta", "plants": "plantas",
    "flower": "flor", "flowers": "flores",
    "tree": "árbol", "trees": "árboles",
    "wood": "madera", "log": "tronco", "logs": "troncos",
    "stone": "piedra", "rock": "roca",
    "dirt": "tierra", "sand": "arena",
    "water": "agua", "lava": "lava", "fire": "fuego",
    "ice": "hielo", "snow": "nieve",
    "wind": "viento", "earth": "tierra", "air": "aire",
    "light": "luz", "shadow": "sombra", "darkness": "oscuridad",
    "soul": "alma", "souls": "almas",
    "life": "vida", "death": "muerte",
    "blood": "sangre", "bone": "hueso", "bones": "huesos",
    # Mod/tech
    "machine": "máquina", "machines": "máquinas",
    "generator": "generador", "generators": "generadores",
    "battery": "batería", "batteries": "baterías",
    "engine": "motor", "engines": "motores",
    "pump": "bomba", "pumps": "bombas",
    "pipe": "tubería", "pipes": "tuberías",
    "cable": "cable", "cables": "cables",
    "wire": "alambre", "wires": "alambres",
    "circuit": "circuito", "circuits": "circuitos",
    "drill": "taladro", "drills": "taladros",
    "saw": "sierra", "saws": "sierras",
    "fan": "ventilador", "fans": "ventiladores",
    "belt": "cinta", "belts": "cintas",
    "conveyor": "transportador",
    "factory": "fábrica", "industrial": "industrial",
    "automation": "automatización",
    "storage": "almacenamiento",
    "system": "sistema", "systems": "sistemas",
    "network": "red", "networks": "redes",
    "core": "núcleo", "cores": "núcleos",
    "card": "tarjeta", "cards": "tarjetas",
    "module": "módulo", "modules": "módulos",
    "component": "componente", "components": "componentes",
    "part": "pieza", "parts": "piezas",
    "piece": "pieza", "pieces": "piezas",
    "fragment": "fragmento", "fragments": "fragmentos",
    "shard": "fragmento", "shards": "fragmentos",
    "essence": "esencia", "essences": "esencias",
    "spirit": "espíritu", "spirits": "espíritus",
    "elixir": "elixir", "elixirs": "elixires",
    "potion": "poción",
    # Misc
    "way": "camino", "path": "sendero",
    "door": "puerta", "doors": "puertas",
    "gate": "portón", "gates": "portones",
    "wall": "muro", "walls": "muros",
    "floor": "suelo", "ceiling": "techo",
    "room": "habitación", "rooms": "habitaciones",
    "hall": "salón", "halls": "salones",
    "page": "página", "pages": "páginas",
    "line": "línea", "lines": "líneas",
    "word": "palabra", "words": "palabras",
    "name": "nombre", "names": "nombres",
    "color": "color", "colour": "color", "colors": "colores",
    "size": "tamaño", "shape": "forma",
    "type": "tipo", "types": "tipos",
    "kind": "tipo", "kinds": "tipos",
    "form": "forma", "forms": "formas",
    "version": "versión",
    "above": "encima", "below": "debajo",
    "left": "izquierda", "right": "derecha",
    "up": "arriba", "down": "abajo",
    "north": "norte", "south": "sur", "east": "este", "west": "oeste",
    "place": "lugar", "places": "lugares",
    "time": "tiempo", "times": "veces",
    "day": "día", "days": "días",
    "night": "noche", "nights": "noches",
    "hour": "hora", "hours": "horas",
    "minute": "minuto", "minutes": "minutos",
    "second": "segundo", "seconds": "segundos",
    "year": "año", "years": "años",
    "again": "de nuevo", "back": "atrás",
    "yet": "todavía", "still": "aún",
    "well": "bien", "fine": "bien",
    "true": "verdadero", "false": "falso",
    "open": "abrir", "close": "cerrar", "closed": "cerrado",
    "start": "iniciar", "stop": "detener", "end": "fin",
    "begin": "comenzar", "finish": "terminar",
    "win": "ganar", "lose": "perder",
    "live": "vivir", "die": "morir", "dead": "muerto",
    "alive": "vivo",
    "help": "ayuda", "support": "soporte",
    "danger": "peligro", "safe": "seguro",
    "alert": "alerta", "caution": "precaución",
    "fail": "fallar", "failed": "fallido",
    "success": "éxito", "succeeded": "exitoso",
    "complete": "completar", "completed": "completado",
    "incomplete": "incompleto", "done": "hecho",
    "ready": "listo", "set": "establecer",
    "build": "construir", "built": "construido",
    "make": "hacer", "made": "hecho",
    "use": "usar", "used": "usado",
    "give": "dar", "given": "dado",
    "take": "tomar", "taken": "tomado",
    "get": "obtener", "got": "obtenido",
    "put": "poner", "place": "colocar", "placed": "colocado",
    "remove": "quitar", "removed": "quitado",
    "add": "añadir", "added": "añadido",
    "increase": "aumentar", "decrease": "disminuir",
    "improve": "mejorar", "enhance": "mejorar",
    "reduce": "reducir", "boost": "potenciar",
    "summary": "resumen", "description": "descripción",
    "introduction": "introducción", "conclusion": "conclusión",
    "title": "título", "subtitle": "subtítulo",
    "welcome": "Bienvenido", "hello": "Hola",
    "goodbye": "Adiós", "thanks": "Gracias",
    "please": "Por favor",
    # Direction/movement
    "go": "ir", "come": "venir", "move": "mover",
    "run": "correr", "walk": "caminar", "jump": "saltar",
    "fly": "volar", "swim": "nadar",
    "climb": "escalar", "fall": "caer",
    "push": "empujar", "pull": "tirar",
    "send": "enviar", "receive": "recibir",
    # Pronouns/possessives - already covered, redundant ok
    "them": "ellos", "they": "ellos", "their": "su",
    "his": "su", "her": "su", "its": "su",
    "he": "él", "she": "ella", "it": "ello",
    "me": "mí", "my": "mi", "mine": "mío",
    "us": "nosotros", "we": "nosotros", "our": "nuestro",
    # Tech specific words
    "creative": "creativo", "survival": "supervivencia",
    "hardcore": "hardcore", "peaceful": "pacífico",
    "easy": "fácil", "normal": "normal", "hard": "difícil",
    "default": "predeterminado", "custom": "personalizado",
    "config": "configuración", "configuration": "configuración",
    "settings": "ajustes", "options": "opciones",
    "menu": "menú", "screen": "pantalla",
    "button": "botón", "key": "tecla",
    "input": "entrada", "output": "salida",
    "fluid": "fluido", "fluids": "fluidos",
    "gas": "gas", "gases": "gases",
    "liquid": "líquido", "liquids": "líquidos",
    "steam": "vapor", "smoke": "humo",
    "oil": "petróleo", "fuel": "combustible",
    "coal": "carbón", "wood": "madera",
    # Misc verbs
    "scan": "escanea", "scanner": "escáner",
    "detect": "detecta", "detection": "detección",
    "drop": "soltar", "spawn": "aparecer",
    "spawner": "generador",
    "trade": "comerciar", "trader": "comerciante",
    "villager": "aldeano", "villagers": "aldeanos",
    "merchant": "mercader",
    "wandering": "errante",
    "baby": "bebé", "child": "niño",
    "adult": "adulto",
    # Roles/classes
    "mage": "mago", "sorcerer": "hechicero",
    "necromancer": "nigromante", "alchemist": "alquimista",
    "engineer": "ingeniero",
    "miner": "minero",
    "farmer": "granjero",
    "fisher": "pescador", "fisherman": "pescador",
    # Mod-specific kept proper (no translation)
    # ---- left intentionally untranslated below ----
}

# Words we explicitly should NOT translate (proper nouns / mod terms)
KEEP_AS_IS = {
    # Mods
    "create","mekanism","botania","tinkers","construct","thaumcraft","ars","nouveau","occultism",
    "twilight","forest","aether","aquaculture","apothic","apotheosis","cataclysm","cataclysmic",
    "alex","alex's","caves","mobs","oh","the","biomes","you'll","go","biomesoplenty","byg",
    "domesticationinnovation","industrial","foregoing","mahou","tsukai","modonomicon",
    "patchouli","jei","emi","rei","resourceful","tools","silentgear","silent","gear","relics",
    "irons","spellbooks","iron's","silver","spellbook","betterend","betternether","quark",
    "supplementaries","farmers","delight","sophisticatedstorage","sophisticated","backpacks",
    "chipped","macaw","macaws","handcrafted","ftb","quests","library","minecraft","forge",
    "neoforge","kubejs","jade","rftools","appliedenergistics","ae2","refined","refinedstorage",
    "ic2","gregtech","blood","magic","evilcraft","botany","pots","gardens","jeresources",
    "mowzies","alexs","alex's","alexscaves","irons","irons_spellbooks","ars_nouveau","ars_elemental",
    # Item / boss names
    "resonarium","drygmy","wixie","whirlisprig","starbuncle","sylph","bookwyrm","amethyst",
    "celestial","jade","foliaath","naga","yeti","hydra","ur-ghast","ur","ghast","lich","minoshroom",
    "kobold","cinderworm","wadjet","cyclops","necromancer","piglins","piglin","brute",
    "warden","creeper","enderman","endermen","blaze","ghast","piglin","villager","zombie",
    "skeleton","spider","wither","ravager","pillager","vindicator","evoker",
    "merlot","brimstone","claymore","lichblade","awakened","mechanical","pumpjack",
    "augmenting","solar","precision","fabrication",
    # Modpack
    "arcadia","arcadian","echoes","power","fusion","core",
}

# --------------------------------------------------------------------
# Color/format token preservation
# --------------------------------------------------------------------
TOKEN_RE = re.compile(r"(&[0-9a-fk-or]|%(?:\d+\$)?[sd]|\{[^}]+\}|§[0-9a-fk-or])", re.IGNORECASE)


def split_tokens(text: str):
    """Split text into (segments, tokens) preserving order: tokens between segments."""
    parts = []
    last = 0
    for m in TOKEN_RE.finditer(text):
        if m.start() > last:
            parts.append(("text", text[last:m.start()]))
        parts.append(("tok", m.group(0)))
        last = m.end()
    if last < len(text):
        parts.append(("text", text[last:]))
    return parts


# Build longest-first ordered phrase list
PHRASE_ITEMS = sorted(PHRASES.items(), key=lambda kv: -len(kv[0]))

WORD_RE = re.compile(r"[A-Za-z][A-Za-z']*")


def translate_segment(seg: str) -> str:
    """Translate a plain text segment (no color codes)."""
    if not seg or not seg.strip():
        return seg

    # Apply phrase replacements (case-insensitive). Preserve case of first letter.
    out = seg
    low = out.lower()
    # Repeatedly apply phrases (longest first)
    changed = True
    safety = 0
    while changed and safety < 3:
        changed = False
        safety += 1
        for ph, repl in PHRASE_ITEMS:
            idx = low.find(ph)
            if idx == -1:
                continue
            # Replace all occurrences of this phrase
            new_out = []
            new_low = []
            last = 0
            i = 0
            while True:
                j = low.find(ph, i)
                if j == -1:
                    new_out.append(out[i:])
                    new_low.append(low[i:])
                    break
                new_out.append(out[i:j])
                new_low.append(low[i:j])
                # Match capitalisation of first letter of original
                src = out[j:j+len(ph)]
                if src and src[0].isupper():
                    r = repl[:1].upper() + repl[1:]
                else:
                    r = repl
                new_out.append(r)
                new_low.append(r.lower())
                i = j + len(ph)
            out = "".join(new_out)
            low = "".join(new_low)
            changed = True
            break  # restart loop with updated text

    # Word-level translation
    def word_repl(m: re.Match) -> str:
        w = m.group(0)
        wl = w.lower()
        # Strip leading apostrophe etc
        if wl in KEEP_AS_IS:
            return w
        # Drop possessive trailing 's
        base = wl
        suffix = ""
        if base.endswith("'s"):
            base = base[:-2]
            suffix = ""  # we'll handle possessive differently below
            if base in KEEP_AS_IS:
                return w  # keep "Warden's" untouched
        if base in WORDS:
            tr = WORDS[base]
            # Preserve initial capitalisation
            if w[:1].isupper():
                tr = tr[:1].upper() + tr[1:]
            # If original had possessive 's keep it
            if wl.endswith("'s"):
                return tr + " de"  # poor man's possessive; rarely hit
            return tr
        return w

    out = WORD_RE.sub(word_repl, out)
    return out


def translate_string(text: str) -> str:
    if not isinstance(text, str):
        return text
    if text == "":
        return ""
    # Quick pass: if string is just a resource id like create:xxx, keep
    if re.fullmatch(r"[a-z0-9_]+:[a-z0-9_/.]+", text):
        return text
    parts = split_tokens(text)
    result = []
    for kind, val in parts:
        if kind == "tok":
            result.append(val)
        else:
            result.append(translate_segment(val))
    return "".join(result)


def translate_value(v):
    if isinstance(v, list):
        return [translate_string(x) if isinstance(x, str) else x for x in v]
    if isinstance(v, str):
        return translate_string(v)
    return v


def main():
    data = json.loads(INPUT.read_text(encoding="utf-8"))
    out = {}
    for k, v in data.items():
        out[k] = translate_value(v)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(out)} entries to {OUTPUT}")


if __name__ == "__main__":
    main()
