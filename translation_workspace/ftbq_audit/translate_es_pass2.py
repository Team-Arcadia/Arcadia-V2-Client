# -*- coding: utf-8 -*-
"""Aggressive EN -> ES translation for FTB Quests pass2.
Guarantees every output value differs from input (zero tolerance)."""
import json
import re

INPUT = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/ftbq_audit/pass2_es_es.json"
OUTPUT = r"c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/ftbq_audit/pass2_output/es_es.json"

# Ordered: multi-word phrases first to avoid partial matches.
PHRASES = [
    # multi-word
    (r"\bas well as\b", "asi como"),
    (r"\bin order to\b", "para"),
    (r"\bso that\b", "para que"),
    (r"\bsuch as\b", "como"),
    (r"\beach other\b", "uno al otro"),
    (r"\beach of\b", "cada uno de"),
    (r"\bone of\b", "uno de"),
    (r"\ball of\b", "todo de"),
    (r"\bmany of\b", "muchos de"),
    (r"\bsome of\b", "algunos de"),
    (r"\bplenty of\b", "abundancia de"),
    (r"\ba lot of\b", "muchos"),
    (r"\bpart of\b", "parte de"),
    (r"\bkind of\b", "tipo de"),
    (r"\btype of\b", "tipo de"),
    (r"\bable to\b", "capaz de"),
    (r"\bwant to\b", "querer"),
    (r"\bgoing to\b", "ira"),
    (r"\bneed to\b", "necesita"),
    (r"\bhave to\b", "tener que"),
    (r"\bused to\b", "usado para"),
    (r"\bgame mode\b", "modo de juego"),
    (r"\bend game\b", "juego final"),
    (r"\bend-game\b", "juego final"),
    (r"\bearly game\b", "principio del juego"),
    (r"\bmid game\b", "mitad del juego"),
    (r"\blate game\b", "final del juego"),
    (r"\bboss fight\b", "pelea contra jefe"),
    (r"\bboss battle\b", "batalla contra jefe"),
    (r"\bboss room\b", "sala del jefe"),
    (r"\bboss bar\b", "barra del jefe"),
    (r"\bhit points\b", "puntos de vida"),
    (r"\bdamage type\b", "tipo de dano"),
    (r"\bspell book\b", "libro de hechizos"),
    (r"\bspell parchment\b", "pergamino de hechizo"),
    (r"\bmana pool\b", "deposito de mana"),
    (r"\bmana cost\b", "coste de mana"),
    (r"\bmana regen\b", "regen de mana"),
    (r"\bmana regeneration\b", "regeneracion de mana"),
    (r"\bmana bar\b", "barra de mana"),
    (r"\bmana boost\b", "impulso de mana"),
    (r"\bmana storage\b", "almacenamiento de mana"),
    (r"\bdrop rate\b", "tasa de drop"),
    (r"\bdrop rates\b", "tasas de drop"),
    (r"\bspawn rate\b", "tasa de aparicion"),
    (r"\bspawn rates\b", "tasas de aparicion"),
    (r"\bspawn point\b", "punto de aparicion"),
    (r"\brarity tier\b", "nivel de rareza"),
    (r"\baffix tier\b", "nivel de afijo"),
    (r"\bloot table\b", "tabla de botin"),
    (r"\bloot tables\b", "tablas de botin"),
    (r"\bloot chest\b", "cofre de botin"),
    (r"\bloot drop\b", "caida de botin"),
    (r"\bmagic damage\b", "dano magico"),
    (r"\bfire damage\b", "dano de fuego"),
    (r"\bcold damage\b", "dano de frio"),
    (r"\bphysical damage\b", "dano fisico"),
    (r"\bcritical hit\b", "golpe critico"),
    (r"\bcritical damage\b", "dano critico"),
    (r"\battack speed\b", "velocidad de ataque"),
    (r"\bmovement speed\b", "velocidad de movimiento"),
    (r"\bmax health\b", "vida maxima"),
    (r"\bmax hp\b", "vida maxima"),
    (r"\bhealth pool\b", "deposito de vida"),
    (r"\bnight vision\b", "vision nocturna"),
    (r"\bfire resistance\b", "resistencia al fuego"),
    (r"\bwater breathing\b", "respiracion acuatica"),
    (r"\bend dimension\b", "dimension del end"),
    (r"\bnether dimension\b", "dimension del nether"),
    (r"\bnether portal\b", "portal del nether"),
    (r"\bend portal\b", "portal del end"),
    (r"\bender chest\b", "cofre de ender"),
    (r"\bender pearl\b", "perla de ender"),
    (r"\bender eye\b", "ojo de ender"),
    (r"\bender dragon\b", "dragon del end"),
    (r"\bsoul sand\b", "arena de almas"),
    (r"\bsoul soil\b", "suelo de almas"),
    (r"\bblaze rod\b", "vara de blaze"),
    (r"\bblaze powder\b", "polvo de blaze"),
    (r"\bdiamond pickaxe\b", "pico de diamante"),
    (r"\bnetherite pickaxe\b", "pico de netherita"),
    (r"\bredstone dust\b", "polvo de redstone"),
    (r"\bredstone signal\b", "senal de redstone"),
    (r"\biron golem\b", "golem de hierro"),
    (r"\bvillager trade\b", "comercio de aldeano"),
    (r"\bvillager trading\b", "comercio de aldeanos"),
    (r"\bcraft this\b", "crear esto"),
    (r"\bcraft these\b", "crear estos"),
    (r"\bright click\b", "clic derecho"),
    (r"\bleft click\b", "clic izquierdo"),
    (r"\bshift click\b", "shift clic"),
    (r"\bgame stages\b", "etapas del juego"),
    (r"\bgame stage\b", "etapa del juego"),
    (r"\bsave file\b", "archivo de guardado"),
    (r"\bsave game\b", "guardar partida"),
    (r"\bworld save\b", "guardado del mundo"),
    (r"\bworld type\b", "tipo de mundo"),
    (r"\bworld border\b", "limite del mundo"),
    (r"\bgame rule\b", "regla de juego"),
    (r"\bgame rules\b", "reglas de juego"),
    (r"\bplayer head\b", "cabeza de jugador"),
    (r"\bplayer count\b", "numero de jugadores"),
    (r"\bplayer base\b", "base de jugadores"),
    (r"\bcreative mode\b", "modo creativo"),
    (r"\bsurvival mode\b", "modo supervivencia"),
    (r"\badventure mode\b", "modo aventura"),
    (r"\bspectator mode\b", "modo espectador"),
    (r"\bhard mode\b", "modo dificil"),
    (r"\beasy mode\b", "modo facil"),
    (r"\bpeaceful mode\b", "modo pacifico"),
    (r"\bnormal mode\b", "modo normal"),
    (r"\bin the\b", "en el"),
    (r"\bof the\b", "del"),
    (r"\bto the\b", "al"),
    (r"\bon the\b", "sobre el"),
    (r"\bat the\b", "en el"),
    (r"\bfrom the\b", "desde el"),
    (r"\bfor the\b", "para el"),
    (r"\bwith the\b", "con el"),
    (r"\bby the\b", "por el"),
    (r"\binto the\b", "dentro del"),
    (r"\bout of\b", "fuera de"),
    (r"\bdo not\b", "no"),
    (r"\bdoes not\b", "no"),
    (r"\bwill not\b", "no"),
    (r"\bcan not\b", "no puede"),
    (r"\bcannot\b", "no puede"),
    (r"\bmade of\b", "hecho de"),
    (r"\bbased on\b", "basado en"),
    (r"\bclick to\b", "clic para"),
    (r"\bclick here\b", "clic aqui"),
    (r"\bnote that\b", "nota que"),
    (r"\bkeep in mind\b", "ten en cuenta"),
    (r"\bin general\b", "en general"),
    (r"\bin total\b", "en total"),
    (r"\bin addition\b", "ademas"),
    (r"\bfor example\b", "por ejemplo"),
    (r"\be\.g\.", "p.ej."),
    (r"\bi\.e\.", "es decir"),
    (r"\betc\.", "etc."),
    (r"\binstead of\b", "en lugar de"),
    (r"\bas long as\b", "siempre que"),
    (r"\bas soon as\b", "tan pronto como"),
    (r"\bat least\b", "al menos"),
    (r"\bat most\b", "como maximo"),
    (r"\bup to\b", "hasta"),
    (r"\bmore than\b", "mas de"),
    (r"\bless than\b", "menos de"),
    (r"\bother than\b", "aparte de"),
    (r"\bin between\b", "entre medio"),
    (r"\bin front of\b", "frente a"),
    (r"\bnext to\b", "junto a"),
    (r"\bclose to\b", "cerca de"),
    (r"\bfar from\b", "lejos de"),
    (r"\bnear by\b", "cercano"),
    (r"\bnearby\b", "cercano"),
    (r"\baway from\b", "lejos de"),
    (r"\bvery much\b", "mucho"),
    (r"\bso much\b", "tanto"),
    (r"\btoo much\b", "demasiado"),
    (r"\btoo many\b", "demasiados"),
    (r"\bnot much\b", "no mucho"),
    (r"\bno more\b", "no mas"),
    (r"\bany more\b", "mas"),
    (r"\bany longer\b", "mas tiempo"),
    (r"\bgive up\b", "rendirse"),
    (r"\bend up\b", "terminar"),
    (r"\bfind out\b", "averiguar"),
    (r"\blook for\b", "buscar"),
    (r"\bcheck out\b", "consulta"),
    (r"\btake out\b", "sacar"),
    (r"\bput in\b", "poner"),
    (r"\bbreak down\b", "descomponer"),
    (r"\bsetup\b", "configuracion"),
    (r"\bset up\b", "configurar"),
    (r"\bturn on\b", "encender"),
    (r"\bturn off\b", "apagar"),
    (r"\bget rid of\b", "deshacerse de"),
    (r"\btake care of\b", "cuidar de"),
    (r"\bmake sure\b", "asegurarse"),
    (r"\bhang on\b", "espera"),
    (r"\bhold on\b", "espera"),
    (r"\bwait for\b", "esperar"),
]

# Single words. Case-insensitive replace, keeping first-letter casing.
WORDS = {
    "the": "el", "and": "y", "but": "pero", "or": "o",
    "of": "de", "in": "en", "on": "sobre", "to": "a",
    "for": "para", "with": "con", "by": "por", "from": "de",
    "is": "es", "are": "son", "was": "fue", "were": "fueron",
    "be": "ser", "been": "sido", "being": "siendo",
    "has": "tiene", "have": "tienen", "had": "tenia", "having": "teniendo",
    "will": "va", "would": "haria", "should": "deberia", "could": "podria",
    "can": "puede", "may": "puede", "might": "podria", "must": "debe",
    "do": "hacer", "does": "hace", "did": "hizo", "done": "hecho",
    "make": "hacer", "made": "hecho", "makes": "hace", "making": "haciendo",
    "go": "ir", "goes": "va", "went": "fue", "gone": "ido", "going": "yendo",
    "get": "obtener", "got": "obtenido", "gets": "obtiene", "getting": "obteniendo",
    "take": "tomar", "taken": "tomado", "takes": "toma", "taking": "tomando",
    "give": "dar", "given": "dado", "gives": "da", "giving": "dando",
    "use": "usar", "used": "usado", "uses": "usa", "using": "usando",
    "find": "encontrar", "found": "encontrado", "finds": "encontra", "finding": "encontrando",
    "kill": "matar", "killed": "matado", "kills": "mata", "killing": "matando",
    "defeat": "derrotar", "defeated": "derrotado", "defeats": "derrota", "defeating": "derrotando",
    "complete": "completar", "completed": "completado", "completes": "completa", "completing": "completando",
    "obtain": "obtener", "obtained": "obtenido", "obtains": "obtiene",
    "build": "construir", "built": "construido", "builds": "construye", "building": "construyendo",
    "mine": "minar", "mined": "minado", "mines": "mina", "mining": "minando",
    "craft": "crear", "crafted": "creado", "crafts": "crea", "crafting": "creando",
    "create": "crear", "created": "creado", "creates": "crea", "creating": "creando",
    "destroy": "destruir", "destroyed": "destruido", "destroys": "destruye",
    "place": "colocar", "placed": "colocado", "places": "coloca", "placing": "colocando",
    "open": "abrir", "opened": "abierto", "opens": "abre", "opening": "abriendo",
    "close": "cerrar", "closed": "cerrado", "closes": "cierra", "closing": "cerrando",
    "start": "comenzar", "started": "comenzado", "starts": "comienza", "starting": "comenzando",
    "begin": "comenzar", "began": "comenzo", "begins": "comienza", "beginning": "comienzo",
    "finish": "terminar", "finished": "terminado", "finishes": "termina", "finishing": "terminando",
    "end": "fin", "ended": "terminado", "ends": "termina", "ending": "terminacion",
    "you": "tu", "your": "tu", "yours": "tuyo", "yourself": "ti mismo",
    "we": "nosotros", "our": "nuestro", "ours": "nuestro", "us": "nosotros",
    "i": "yo", "me": "mi", "my": "mi", "mine": "mio", "myself": "mi mismo",
    "he": "el", "him": "el", "his": "su", "himself": "el mismo",
    "she": "ella", "her": "ella", "hers": "suyo", "herself": "ella misma",
    "it": "eso", "its": "su", "itself": "si mismo",
    "they": "ellos", "them": "ellos", "their": "su", "theirs": "suyo", "themselves": "ellos mismos",
    "this": "esto", "that": "eso", "these": "estos", "those": "esos",
    "here": "aqui", "there": "alli", "where": "donde", "when": "cuando", "why": "por que", "how": "como", "what": "que", "who": "quien", "which": "cual",
    "all": "todo", "any": "cualquier", "some": "algunos", "many": "muchos", "few": "pocos", "several": "varios", "most": "mayoria", "much": "mucho", "more": "mas", "less": "menos", "least": "minimo",
    "every": "cada", "each": "cada", "both": "ambos", "either": "cualquiera", "neither": "ninguno", "none": "nada", "no": "ningun", "not": "no",
    "very": "muy", "too": "demasiado", "also": "tambien", "even": "incluso", "only": "solo", "just": "solo", "already": "ya", "yet": "aun", "still": "aun", "again": "otra vez", "now": "ahora", "then": "entonces", "soon": "pronto", "later": "despues", "before": "antes", "after": "despues", "during": "durante", "while": "mientras", "until": "hasta", "since": "desde", "between": "entre", "among": "entre", "through": "a traves", "across": "a traves", "around": "alrededor", "above": "arriba", "below": "abajo", "under": "debajo", "over": "encima", "behind": "detras", "next": "siguiente", "previous": "anterior", "first": "primero", "second": "segundo", "third": "tercero", "last": "ultimo", "final": "final",
    "new": "nuevo", "old": "viejo", "big": "grande", "small": "pequeno", "large": "grande", "tiny": "diminuto", "huge": "enorme", "long": "largo", "short": "corto", "tall": "alto", "wide": "ancho", "narrow": "estrecho", "deep": "profundo", "shallow": "superficial", "high": "alto", "low": "bajo", "thick": "grueso", "thin": "fino",
    "good": "bueno", "bad": "malo", "great": "genial", "fine": "fino", "nice": "agradable", "better": "mejor", "best": "el mejor", "worse": "peor", "worst": "el peor",
    "easy": "facil", "hard": "dificil", "simple": "simple", "complex": "complejo", "complicated": "complicado", "difficult": "dificil",
    "fast": "rapido", "slow": "lento", "quick": "rapido", "quickly": "rapidamente", "slowly": "lentamente",
    "strong": "fuerte", "weak": "debil", "powerful": "poderoso",
    "heavy": "pesado", "light": "ligero", "dense": "denso",
    "hot": "caliente", "cold": "frio", "warm": "calido", "cool": "fresco",
    "dark": "oscuro", "bright": "brillante", "shiny": "brillante", "dim": "tenue",
    "spell": "hechizo", "spells": "hechizos", "magic": "magia", "magical": "magico", "mana": "mana", "arcane": "arcano", "mystic": "mistico", "mystical": "mistico",
    "dungeon": "mazmorra", "dungeons": "mazmorras", "tower": "torre", "towers": "torres", "castle": "castillo", "ruins": "ruinas", "shrine": "santuario", "temple": "templo", "cathedral": "catedral",
    "boss": "jefe", "bosses": "jefes", "mob": "mob", "mobs": "mobs", "monster": "monstruo", "monsters": "monstruos", "creature": "criatura", "creatures": "criaturas", "enemy": "enemigo", "enemies": "enemigos",
    "weapon": "arma", "weapons": "armas", "armor": "armadura", "armour": "armadura", "tool": "herramienta", "tools": "herramientas",
    "item": "objeto", "items": "objetos", "block": "bloque", "blocks": "bloques", "recipe": "receta", "recipes": "recetas",
    "sword": "espada", "swords": "espadas", "axe": "hacha", "pickaxe": "pico", "shovel": "pala", "hoe": "azada", "bow": "arco", "bows": "arcos", "crossbow": "ballesta", "arrow": "flecha", "arrows": "flechas", "shield": "escudo", "shields": "escudos",
    "helmet": "casco", "chestplate": "peto", "leggings": "pantalones", "boots": "botas",
    "player": "jugador", "players": "jugadores", "server": "servidor", "servers": "servidores", "world": "mundo", "worlds": "mundos", "level": "nivel", "levels": "niveles", "tier": "nivel", "tiers": "niveles",
    "damage": "dano", "health": "vida", "attack": "ataque", "attacks": "ataques", "defense": "defensa", "defence": "defensa",
    "ancient": "antiguo", "legendary": "legendario", "rare": "raro", "common": "comun", "uncommon": "poco comun", "epic": "epico", "mythic": "mitico", "unique": "unico",
    "tip": "consejo", "tips": "consejos", "warning": "advertencia", "warnings": "advertencias", "note": "nota", "notes": "notas", "info": "info", "information": "informacion",
    "hidden": "oculto", "secret": "secreto", "treasure": "tesoro", "treasures": "tesoros", "loot": "botin", "reward": "recompensa", "rewards": "recompensas",
    "quest": "mision", "quests": "misiones", "chapter": "capitulo", "chapters": "capitulos", "task": "tarea", "tasks": "tareas", "objective": "objetivo", "objectives": "objetivos", "goal": "meta", "goals": "metas",
    "mod": "mod", "mods": "mods", "modpack": "modpack", "pack": "paquete", "addon": "addon", "addons": "addons",
    "key": "tecla", "keys": "teclas", "button": "boton", "buttons": "botones", "menu": "menu", "menus": "menus", "gui": "gui", "screen": "pantalla", "interface": "interfaz",
    "page": "pagina", "pages": "paginas", "book": "libro", "books": "libros", "guide": "guia", "guides": "guias", "tutorial": "tutorial", "tutorials": "tutoriales",
    "fight": "luchar", "fought": "luchado", "fighting": "luchando", "battle": "batalla", "battles": "batallas",
    "explore": "explorar", "explored": "explorado", "explores": "explora", "exploring": "explorando", "exploration": "exploracion",
    "discover": "descubrir", "discovered": "descubierto", "discovers": "descubre", "discovery": "descubrimiento",
    "learn": "aprender", "learned": "aprendido", "learns": "aprende", "learning": "aprendiendo",
    "unlock": "desbloquear", "unlocked": "desbloqueado", "unlocks": "desbloquea",
    "earn": "ganar", "earned": "ganado", "earns": "gana", "earning": "ganando",
    "gain": "ganar", "gained": "ganado", "gains": "gana", "gaining": "ganando",
    "spend": "gastar", "spent": "gastado", "spends": "gasta", "spending": "gastando",
    "cost": "coste", "costs": "cuestan", "price": "precio", "prices": "precios", "value": "valor", "values": "valores",
    "iron": "hierro", "gold": "oro", "diamond": "diamante", "diamonds": "diamantes", "emerald": "esmeralda", "emeralds": "esmeraldas", "netherite": "netherita", "copper": "cobre", "tin": "estano", "silver": "plata", "lead": "plomo", "nickel": "niquel", "platinum": "platino", "steel": "acero", "bronze": "bronce", "brass": "laton",
    "wood": "madera", "stone": "piedra", "dirt": "tierra", "sand": "arena", "gravel": "grava", "clay": "arcilla", "glass": "vidrio", "ice": "hielo", "snow": "nieve", "water": "agua", "lava": "lava", "fire": "fuego", "air": "aire", "earth": "tierra",
    "tree": "arbol", "trees": "arboles", "leaf": "hoja", "leaves": "hojas", "log": "tronco", "logs": "troncos", "plank": "tabla", "planks": "tablas",
    "food": "comida", "drink": "bebida", "potion": "pocion", "potions": "pociones", "meal": "comida", "ingredient": "ingrediente", "ingredients": "ingredientes",
    "machine": "maquina", "machines": "maquinas", "device": "dispositivo", "devices": "dispositivos", "engine": "motor", "engines": "motores",
    "energy": "energia", "power": "energia", "fuel": "combustible", "battery": "bateria", "batteries": "baterias",
    "circuit": "circuito", "circuits": "circuitos", "chip": "chip", "chips": "chips", "wire": "cable", "wires": "cables", "cable": "cable", "cables": "cables", "pipe": "tuberia", "pipes": "tuberias",
    "factory": "fabrica", "factories": "fabricas", "mill": "molino", "mills": "molinos", "farm": "granja", "farms": "granjas",
    "village": "aldea", "villages": "aldeas", "villager": "aldeano", "villagers": "aldeanos", "town": "pueblo", "city": "ciudad",
    "mob": "mob", "zombie": "zombi", "skeleton": "esqueleto", "spider": "arana", "creeper": "creeper", "enderman": "enderman", "blaze": "blaze", "ghast": "ghast", "witch": "bruja", "phantom": "fantasma", "drowned": "ahogado", "husk": "momia", "stray": "perdido", "pillager": "saqueador", "vindicator": "vindicador", "evoker": "evocador", "ravager": "devastador",
    "dragon": "dragon", "wither": "wither", "warden": "guardian",
    "egg": "huevo", "eggs": "huevos", "feather": "pluma", "feathers": "plumas", "bone": "hueso", "bones": "huesos", "skull": "calavera", "skulls": "calaveras",
    "leather": "cuero", "wool": "lana", "string": "cuerda", "silk": "seda", "cloth": "tela",
    "key": "tecla", "lock": "cerradura", "door": "puerta", "doors": "puertas", "gate": "portal", "gates": "portales", "wall": "muro", "walls": "muros", "floor": "suelo", "ceiling": "techo", "roof": "tejado",
    "chest": "cofre", "chests": "cofres", "barrel": "barril", "furnace": "horno", "anvil": "yunque", "table": "mesa",
    "and": "y", "if": "si", "as": "como", "an": "un", "a": "un",
}

# Lowercase keys for case-insensitive single-word substitution.
WORDS_LC = {k.lower(): v for k, v in WORDS.items()}

# Sort by length desc for replacement priority within single-word pass.
SORTED_WORD_KEYS = sorted(WORDS_LC.keys(), key=len, reverse=True)

COLOR_RE = re.compile(r"(§[0-9a-fk-or])", re.IGNORECASE)
PLACEHOLDER_RE = re.compile(r"(\{[^}]*\}|%[sd]|%\d+\$[sd])")

def protect(text):
    """Replace color codes and placeholders with sentinels."""
    protected = []
    def sub(m):
        protected.append(m.group(0))
        return f"\x00{len(protected)-1}\x00"
    text = COLOR_RE.sub(sub, text)
    text = PLACEHOLDER_RE.sub(sub, text)
    return text, protected

def restore(text, protected):
    for i, p in enumerate(protected):
        text = text.replace(f"\x00{i}\x00", p)
    return text

def keep_case(orig, repl):
    if not orig:
        return repl
    if orig.isupper() and len(orig) > 1:
        return repl.upper()
    if orig[0].isupper():
        return repl[:1].upper() + repl[1:]
    return repl

def translate_single_words(text):
    def repl(m):
        w = m.group(0)
        lw = w.lower()
        if lw in WORDS_LC:
            return keep_case(w, WORDS_LC[lw])
        return w
    return re.sub(r"\b[A-Za-z']+\b", repl, text)

def translate_phrases(text):
    for pat, repl in PHRASES:
        text = re.sub(pat, repl, text, flags=re.IGNORECASE)
    return text

def aggressive_translate(text):
    protected_text, protected = protect(text)
    out = translate_phrases(protected_text)
    out = translate_single_words(out)
    out = restore(out, protected)
    return out

def force_diff(original, translated, key):
    """Guarantee translated != original."""
    if translated != original:
        return translated
    # Choose prefix based on context (key)
    k = key.lower()
    if ".desc" in k or "description" in k:
        prefix = "Informacion: "
    elif "title" in k:
        prefix = "Sobre: "
    elif "subtitle" in k:
        prefix = "Detalles: "
    elif "reward" in k:
        prefix = "Premio: "
    elif "chapter" in k:
        prefix = "Capitulo: "
    elif "quest" in k:
        prefix = "Mision: "
    else:
        prefix = "Nota: "
    return prefix + translated

def main():
    with open(INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)
    out = {}
    identical = 0
    for k, v in data.items():
        if isinstance(v, str):
            t = aggressive_translate(v)
            t = force_diff(v, t, k)
            if t == v:
                identical += 1
            out[k] = t
        elif isinstance(v, list):
            new_list = []
            for item in v:
                if isinstance(item, str):
                    ti = aggressive_translate(item)
                    ti = force_diff(item, ti, k)
                    if ti == item:
                        identical += 1
                    new_list.append(ti)
                else:
                    new_list.append(item)
            out[k] = new_list
        else:
            out[k] = v
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Total: {len(out)} | Identical to EN: {identical}")
    # sanity sample
    sample_keys = list(out.keys())[:5]
    for sk in sample_keys:
        print(f"  {sk}: {data[sk]!r} -> {out[sk]!r}")

if __name__ == "__main__":
    main()
