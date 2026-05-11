"""
Translate FTB Quests Phase 2 keys from English to Spanish (Spain).
Reads phase2_to_translate_es_es.json, writes phase2_output/es_es.json.
Handles BOTH strings and arrays of strings (descs).
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
INPUT_FILE = ROOT / "phase2_to_translate_es_es.json"
OUTPUT_DIR = ROOT / "phase2_output"
OUTPUT_FILE = OUTPUT_DIR / "es_es.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================
# EXACT full-string translations (after color-code stripping)
# =============================================================
EXACT = {
    # Chapter titles
    "The Ars Universe": "El Universo Ars",
    "Ars Nouveau": "Ars Nouveau",
    "Ars Nouveau: The Arcana": "Ars Nouveau: Los Arcanos",
    "Ars Nouveau: Complete Magic": "Ars Nouveau: Magia Completa",
    "Enchantment Industry": "Industria del Encantamiento",
    "Pump Dat Oil": "Bombea Ese Petróleo",
    "Apotheosis Gem": "Gema de Apotheosis",
    "Apotheosis Spawner": "Generador de Apotheosis",
    "Apothic Enchanting": "Encantamiento Apóctico",
    "Apothic Attributes": "Atributos Apócticos",
    "Create": "Create",
    "Create I": "Create I",
    "Create II": "Create II",
    "Create III": "Create III",
    "Create IV": "Create IV",
    "Create V": "Create V",
    "Create VI": "Create VI",
    "All of Create": "Todo Create",
    "Create Progression": "Progresión de Create",
    "Chipped": "Chipped",
    "Mekanism": "Mekanism",
    "Mekanism Reactor": "Reactor de Mekanism",
    "Mekanism Reactors": "Reactores de Mekanism",
    "Refined Storage": "Refined Storage",
    "Applied Energistics": "Applied Energistics",
    "Flux Networks": "Flux Networks",
    "Tutorial": "Tutorial",
    "Progression Guide": "Guía de Progresión",
    "How to Start?": "¿Cómo empezar?",
    "A New Beginning": "Un Nuevo Comienzo",
    "First Line of Code": "Primera Línea de Código",
    "Mowzie's Mobs": "Mowzie's Mobs",
    "Mutant Monsters": "Monstruos Mutantes",
    "Iron's Spells": "Hechizos de Iron",
    "Iron's Spells and Spellbooks": "Hechizos y Libros de Iron",
    "Simply Swords": "Simply Swords",
    "Twilight Forest": "Bosque Crepuscular",
    "The Aether": "El Aether",
    "Deeper and Darker": "Más Profundo y Oscuro",
    "Call from the Depths": "Llamada desde las Profundidades",
    "The Nether Call": "La Llamada del Nether",
    "Never End": "Nunca Termina",
    "Immersive Engineering": "Immersive Engineering",
    "Immersive Engineering II": "Immersive Engineering II",
    "Immersive Aircraft": "Immersive Aircraft",
    "Better Archeology": "Better Archeology",
    "Apotheosis": "Apotheosis",
    "Artifacts": "Artifacts",
    "Occultism": "Occultism",
    "Hunting Bounty": "Recompensa de Caza",
    "Fun Additions": "Adiciones Divertidas",
    "Addon Harmony": "Armonía de Complementos",
    "Taste of Tradition": "Sabor de la Tradición",
    "Elimination Protocol": "Protocolo de Eliminación",
    "Central Kitchen": "Cocina Central",
    "Metalurgia": "Metalurgia",
    "New Age": "Nueva Era",
    "To Know": "Para Saber",
    "The Farmer's Encyclopedia": "La Enciclopedia del Granjero",
    "Poultry and Fish": "Aves y Pescado",
    "Stepping Stones": "Piedras del Camino",
    "Cellar": "Bodega",
    "Shop": "Tienda",
    "Optical": "Óptico",
    "Connected": "Conectado",
    "Aquaculture": "Acuicultura",
    "Transport": "Transporte",
    "Automation": "Automatización",
    "Sophisticated": "Sofisticado",
    # Common quest text
    "Congrats!": "¡Felicidades!",
    "Book": "Libro",
    "Paper": "Papel",
    "Enchanted Book": "Libro Encantado",
    "Guide": "Guía",
    "Chapter Quest": "Misión de Capítulo",
    "Tier up!": "¡Sube de nivel!",
    "Beginning": "Inicio",
    "Start": "Inicio",
    "Beginnings": "Inicio",
    "Progression": "Progresión",
    "Progresion": "Progresión",
    "Advanced": "Avanzado",
    "Expert": "Experto",
    "Learning": "Aprendizaje",
    "End of the game": "Final del juego",
    "Nearly impossible": "Casi imposible",
    "Absolute perfection": "Perfección absoluta",
    "Optional": "Opcional",
    "Required": "Obligatorio",
    "Elevators": "Ascensores",
    "Shafts and Gears": "Ejes y Engranajes",
    "Level 2 Energy": "Energía Nivel 2",
    "Computers & Redstone": "Computadoras y Redstone",
    "Generate SU (Stress Units)": "Genera SU (Unidades de Estrés)",
    "It flies!": "¡Vuela!",
    "Essential for seeing": "Esencial para ver",
    "Prove your worth": "Demuestra tu valía",
    "Don't hit it with a sword!": "¡No lo golpees con una espada!",
    "The winged man's best friend": "El mejor amigo del hombre alado",
    "The more worn, the stronger!": "¡Cuanto más desgastado, más fuerte!",
    "The ultimate challenge (Optional)": "El desafío definitivo (Opcional)",
    "It's getting hot in here...": "Hace calor aquí...",
    "Capturer un Blaze": "Capturar un Blaze",
    "Technology Intelligente": "Tecnología Inteligente",
    "L'assemblage complexe": "El Ensamblaje Complejo",
    "Tchou Tchou !": "¡Chu Chu!",
    "Welcome to the Otherside": "Bienvenido al Otro Lado",
    "The Opening Ritual": "El Ritual de Apertura",
    "Frostfall": "Caída Helada",
    "Skyroot Origins": "Orígenes de Raíz Celeste",
    "Engineer's Workbench": "Banco de Trabajo del Ingeniero",
    "Read my description!": "¡Lee mi descripción!",
    "[Click to read]": "[Haz clic para leer]",
    "Click me!": "¡Haz clic en mí!",
    "Welcome to All of Create!": "¡Bienvenido a All of Create!",
    # Tips & warnings
    "Tip:": "Consejo:",
    "Warning:": "Advertencia:",
    "Note:": "Nota:",
    "WARNING:": "ADVERTENCIA:",
    "NOTE:": "NOTA:",
    "TIP:": "CONSEJO:",
}

# =============================================================
# Common short descriptions / flavor sentences (color-stripped)
# =============================================================
FLAVOR = {
    "A repeater that sends a pulse after a configurable amount of time.":
        "Un repetidor que envía un pulso tras un tiempo configurable.",
    "Beyond the portal.": "Más allá del portal.",
    "The block that manages train assembly and disassembly.":
        "El bloque que gestiona el ensamblaje y desensamblaje de trenes.",
    "Beyond cables.": "Más allá de los cables.",
    "Crushing Wheels - Endgame": "Ruedas Trituradoras - Final del juego",
    "Circuit Breaker": "Disyuntor",
    "Turbine Rotor": "Rotor de Turbina",
    "Neptunium Leggings": "Pantalones de Neptunio",
    "Jackal Form": "Forma de Chacal",
    "Smart Filter": "Filtro Inteligente",
    "Smart Fluid Pipe": "Tubería de Fluido Inteligente",
    "Mechanical Press": "Prensa Mecánica",
    "Mechanical Mixer": "Mezcladora Mecánica",
    "Mechanical Piston": "Pistón Mecánico",
    "Mechanical Drill": "Taladro Mecánico",
    "Mechanical Arm": "Brazo Mecánico",
    "Mechanical Bearing": "Rodamiento Mecánico",
    "Brass Casing": "Carcasa de Latón",
    "Copper Casing": "Carcasa de Cobre",
    "Grain and Fiber Bags": "Sacos de Grano y Fibra",
    "Hose Pulley": "Polea de Manguera",
    "Wither Skeleton Skull": "Calavera de Esqueleto Wither",
    "Fluid Tank": "Tanque de Fluidos",
    "Oil Tank": "Tanque de Petróleo",
    "Filter Upgrade": "Mejora de Filtro",
    "Any Train Track": "Cualquier Vía de Tren",
    "Train Tracks": "Vías de Tren",
    "Enter the Nether": "Entra al Nether",
    "Nature Rune": "Runa de la Naturaleza",
    "Blank Rune": "Runa en Blanco",
    "Rare Material": "Material Raro",
    "Common Material": "Material Común",
    "Uncommon Material": "Material Poco Común",
    "Epic Material": "Material Épico",
    "Mythic Material": "Material Mítico",
    "Legendary Material": "Material Legendario",
    "Stack Upgrade Tier 1": "Mejora de Pila Nivel 1",
    "Stack Upgrade Tier 2": "Mejora de Pila Nivel 2",
    "Stack Upgrade Tier 3": "Mejora de Pila Nivel 3",
    "Stack Upgrade Tier 4": "Mejora de Pila Nivel 4",
    "Millstone": "Muela",
    "Encased Fan": "Ventilador Encapsulado",
    "Rotation Speed Controller": "Controlador de Velocidad de Rotación",
    "Crafting Upgrade": "Mejora de Crafteo",
    "Pressure Disperser": "Dispersor de Presión",
    "Hell's Gate": "Puerta del Infierno",
    "Basic Control Circuit": "Circuito de Control Básico",
    "Ultimate Control Circuit": "Circuito de Control Definitivo",
    "Auto Blasting Upgrade": "Mejora de Fundición Automática",
    "Auto Smelting Upgrade": "Mejora de Fundición Automática",
    "Andesite, the Foundation": "Andesita, los Cimientos",
    "Advanced Void Upgrade": "Mejora de Vacío Avanzada",
    "Void Upgrade": "Mejora de Vacío",
    "Speed Upgrade": "Mejora de Velocidad",
    "Fluorite Gem": "Gema de Fluorita",
    "Item Drain": "Drenador de Objetos",
    "Deployer": "Desplegador",
    "Chalk White Impure": "Tiza Blanca Impura",
    "Hellshelf": "Estante Infernal",
    "Fan Nozzle": "Boquilla del Ventilador",
    "Electron Tube": "Tubo de Electrones",
    "Shaft": "Eje",
    "Bookshelf": "Estantería",
    "Fiery Ingot": "Lingote Ardiente",
    "Pickup Upgrade": "Mejora de Recogida",
    "Charm Of Life 1": "Amuleto de Vida 1",
    "Non-Portable Chainsaw": "Motosierra No Portátil",
    "Dragon Breath": "Aliento de Dragón",
    "Smoking Upgrade": "Mejora de Ahumado",
    "Advanced Jukebox Upgrade": "Mejora de Gramola Avanzada",
    "Bastion Raider": "Asaltante del Bastión",
    "Fungal Woods": "Bosques Fúngicos",
    "Echo Shard": "Fragmento de Eco",
    "Reinforced Echo Shard": "Fragmento de Eco Reforzado",
    "Mysterious Flesh": "Carne Misteriosa",
    "Smelting Upgrade": "Mejora de Fundición",
    "Blasting Upgrade": "Mejora de Fundición Rápida",
    "Advanced Feeding Upgrade": "Mejora de Alimentación Avanzada",
    "Feeding Upgrade": "Mejora de Alimentación",
    "Steam Engine": "Motor de Vapor",
    "Gearboxes": "Cajas de Engranajes",
    "Backpack": "Mochila",
    "Dough": "Masa",
    "Andesite Alloy": "Aleación de Andesita",
    "Chain Conveyor": "Transportador de Cadena",
    "Tarnished Helmet": "Casco Deslustrado",
    "Cogwheels": "Engranajes",
    "Knightmetal Ingot": "Lingote de Metal de Caballero",
    "Mine Iron": "Extrae Hierro",
    "Iron Ore": "Mineral de Hierro",
    "Advanced Pickup Upgrade": "Mejora de Recogida Avanzada",
    "Water Wheels": "Ruedas Hidráulicas",
    "Silence de Mort": "Silencio Mortal",
    "Chemical Oxidizer": "Oxidador Químico",
    "Blaze Burner": "Quemador de Blaze",
    "Stone Tools": "Herramientas de Piedra",
    "Stonecutter Upgrade": "Mejora de Cortapiedras",
    "Advanced Technomancy": "Tecnomancia Avanzada",
    "Advanced Compacting Upgrade": "Mejora de Compactación Avanzada",
    "Runefused Gem": "Gema Runafusionada",
    "Basic Chemical Tank": "Tanque Químico Básico",
    "Experience Bottle": "Botella de Experiencia",
    "Le Gardien Aveugle": "El Guardián Ciego",
    "Brush": "Cepillo",
    "Enchanting Apparatus": "Aparato de Encantamiento",
    "Casing": "Carcasa",
    "Prismarine Crystals": "Cristales de Prismarina",
    "Pump Upgrade": "Mejora de Bomba",
    "Tunnels": "Túneles",
    "Engineer's Goggles": "Gafas del Ingeniero",
    "Crying Obsidian": "Obsidiana Llorona",
    "Magnet Upgrade": "Mejora de Imán",
    "Advanced Pump Upgrade": "Mejora de Bomba Avanzada",
    "Heart of the Depths": "Corazón de las Profundidades",
    "Heart of the Deep": "Corazón de las Profundidades",
    "Advanced Alchemy Upgrade": "Mejora de Alquimia Avanzada",
    "Advanced Filter Upgrade": "Mejora de Filtro Avanzada",
    "Chain Drive": "Transmisión de Cadena",
    "Rod of Constant Rotation": "Vara de Rotación Constante",
    "Advanced Magnet Upgrade": "Mejora de Imán Avanzada",
    "Sigil Of Socketing": "Sigilo de Engaste",
    "Marine Form": "Forma Marina",
    "Refill Upgrade": "Mejora de Recarga",
    "Glyph Invisibility": "Glifo de Invisibilidad",
    "Soul Dust": "Polvo de Alma",
    "Soul Elytra": "Élitros del Alma",
    "Avatar of the Warden": "Avatar del Guardián",
    "Carapace of the Guardian": "Caparazón del Guardián",
    "Sonic Protection": "Protección Sónica",
    "Resonarium Forge": "Forja de Resonarium",
    "Resonarium Gear": "Equipo de Resonarium",
    "Age of Resonarium": "Era del Resonarium",
    "Sculk Transmission": "Transmisión Sculk",
    "Deadly Curiosity": "Curiosidad Mortal",
    "The Cursed Temple": "El Templo Maldito",
    "Epic Ink": "Tinta Épica",
    "Rare Ink": "Tinta Rara",
    "Legendary Ink": "Tinta Legendaria",
    "Precision Mechanism": "Mecanismo de Precisión",
    "Wrench": "Llave Inglesa",
    "Fission Fuel Assembly": "Ensamblaje de Combustible de Fisión",
    "Dormant Relic": "Reliquia Latente",
    "Call of the Void": "Llamada del Vacío",
    "Dark Cartographer": "Cartógrafo Oscuro",
    "Sonorous Staff": "Bastón Sonoro",
    "Arctic Fur": "Pelaje Ártico",
    "Arcane Essence": "Esencia Arcana",
    "Adjustable Gearshift": "Cambio de Marchas Ajustable",
    "Alloy Infused": "Aleación Infundida",
    "Addon": "Complemento",
    "Exchange?": "¿Intercambio?",
    # Common short flavor strings
    "Bone-chilling fight.": "Pelea escalofriante.",
    "Chair.": "Silla.",
    "Dark transformation.": "Transformación oscura.",
    "Ancient remains.": "Restos antiguos.",
    "Manipulate the essence.": "Manipula la esencia.",
    "Alter reality itself.": "Altera la propia realidad.",
    "Battle for glory.": "Lucha por la gloria.",
    "Wings of freedom.": "Alas de la libertad.",
    "Forbidden knowledge.": "Conocimiento prohibido.",
    "Harness ancient power.": "Aprovecha el poder antiguo.",
    "Blade of legend.": "Espada de leyenda.",
    "Discover lost relics.": "Descubre reliquias perdidas.",
    "One step closer.": "Un paso más cerca.",
    "Staring into the abyss...": "Mirando al abismo...",
    "The sky is the limit.": "El cielo es el límite.",
    "Every journey starts here.": "Todo viaje comienza aquí.",
    "Steel and valor.": "Acero y valor.",
    "The path of power.": "El camino del poder.",
    "Fearsome adversary.": "Adversario temible.",
    "Soar above it all.": "Vuela sobre todo.",
    "Gather what you need.": "Reúne lo que necesitas.",
    "History preserved.": "Historia preservada.",
    "A new dawn awaits.": "Te espera un nuevo amanecer.",
    "Airborne adventure.": "Aventura aérea.",
    "Arsenal of the Void": "Arsenal del Vacío",
    "Dark enchantments.": "Encantamientos oscuros.",
    "Beyond mortal limits.": "Más allá de los límites mortales.",
    "Spawner mastery awaits.": "Te espera la maestría del generador.",
    "Face the mutation.": "Enfrenta la mutación.",
    "Creature of legend.": "Criatura de leyenda.",
    "Forge the extraordinary.": "Forja lo extraordinario.",
    "Enhance and conquer.": "Mejora y conquista.",
    "A Sharp Start": "Un Comienzo Afilado",
    "Trophy of the hunt.": "Trofeo de la cacería.",
    "Fossils tell stories.": "Los fósiles cuentan historias.",
    "Prepare for the unknown.": "Prepárate para lo desconocido.",
    "Archaeological wonder.": "Maravilla arqueológica.",
    "Mutated menace.": "Amenaza mutada.",
    "Monstrous encounter.": "Encuentro monstruoso.",
    "Twisted creation.": "Creación retorcida.",
    "Abomination awaits.": "Te espera una abominación.",
    "Unearth the past.": "Desentierra el pasado.",
    "The beginning of greatness.": "El comienzo de la grandeza.",
    "Take your first steps.": "Da tus primeros pasos.",
    "Skeletal horror.": "Horror esquelético.",
    "Gemcraft mastery.": "Maestría en gemas.",
    "A key component.": "Un componente clave.",
    "Begin your adventure!": "¡Comienza tu aventura!",
    "Forge ahead.": "Avanza con fuerza.",
    "Weave the arcana.": "Teje los arcanos.",
    "Arcane discovery.": "Descubrimiento arcano.",
    "Spell of wonder.": "Hechizo de asombro.",
    "Channel the source.": "Canaliza la fuente.",
    "Summon your power.": "Invoca tu poder.",
    "Smart storage.": "Almacenamiento inteligente.",
    "Organize and thrive.": "Organiza y prospera.",
    "Pack it better.": "Empaca mejor.",
    "Backpack evolution.": "Evolución de la mochila.",
    "Carry the world.": "Lleva el mundo contigo.",
    "Upgrade your carry.": "Mejora tu capacidad de carga.",
    "Storage innovation.": "Innovación en almacenamiento.",
    "Upgrade installed.": "Mejora instalada.",
    "Ink and parchment.": "Tinta y pergamino.",
    "Unleash the elements.": "Desata los elementos.",
    "Arcane scholarship.": "Erudición arcana.",
    "Runic mysteries.": "Misterios rúnicos.",
    "Scribe of spells.": "Escriba de hechizos.",
    "Spellcraft mastery.": "Maestría en hechicería.",
    "The mage's arsenal.": "El arsenal del mago.",
    "Channel raw power.": "Canaliza poder puro.",
    "Process and refine.": "Procesa y refina.",
    "Science prevails.": "La ciencia prevalece.",
    "The Other side.": "El Otro Lado.",
    "Ore multiplication.": "Multiplicación de mineral.",
    "Industrial evolution.": "Evolución industrial.",
    "Spirits beckon.": "Los espíritus llaman.",
    "Demonic pact.": "Pacto demoníaco.",
    "Occult knowledge.": "Conocimiento oculto.",
    "Energy unlimited.": "Energía ilimitada.",
    "Summon and bind.": "Invoca y ata.",
    "Power of the atom.": "El poder del átomo.",
    "Handle with care.": "Manéjese con cuidado.",
    "Digital storage.": "Almacenamiento digital.",
    "Atomic precision.": "Precisión atómica.",
    "Spirit of the depths.": "Espíritu de las profundidades.",
    "Network node.": "Nodo de red.",
    "Energy at scale.": "Energía a escala.",
    "Mystical artifact.": "Artefacto místico.",
    "Trinket of the ancients.": "Talismán de los antiguos.",
    "Disk drive ambition.": "Ambición de unidad de disco.",
    "Inscribe your destiny.": "Inscribe tu destino.",
    "Hellfire forged.": "Forjado en fuego infernal.",
    "The arcane library.": "La biblioteca arcana.",
    "Grid access.": "Acceso a la red.",
    "Curio of wonder.": "Curiosidad de asombro.",
    "Critical mass.": "Masa crítica.",
    "Hidden power awaits.": "Te espera un poder oculto.",
    "Shelf of secrets.": "Estante de secretos.",
    "Nuclear dawn.": "Amanecer nuclear.",
    "Legendary treasure.": "Tesoro legendario.",
    "Knowledge is power.": "El conocimiento es poder.",
    "Digital revolution.": "Revolución digital.",
    "A rare find indeed.": "Un hallazgo realmente raro.",
    "Equip the extraordinary.": "Equípate con lo extraordinario.",
    "Enchant beyond limits.": "Encanta más allá de los límites.",
    "Mystic forest lore.": "Saber del bosque místico.",
    "Industrial revolution.": "Revolución industrial.",
    "A cog in the machine.": "Un engranaje de la máquina.",
    "Mechanical marvel.": "Maravilla mecánica.",
    "Nether mastery.": "Maestría en el Nether.",
    "Beyond the flames.": "Más allá de las llamas.",
    "The engineer's dream.": "El sueño del ingeniero.",
    "Gears of progress.": "Engranajes del progreso.",
    "Forest of wonder.": "Bosque de maravillas.",
    "Upgraded netherite.": "Netherita mejorada.",
    "Infernal upgrade.": "Mejora infernal.",
    "A collector's dream.": "El sueño de un coleccionista.",
    "Blazing ambition.": "Ambición ardiente.",
    "Dark metal.": "Metal oscuro.",
    "Powered by rotation.": "Impulsado por rotación.",
    "Bookshelf of wonders.": "Estantería de maravillas.",
    "Ancient enchantments.": "Encantamientos antiguos.",
    "Enchanted woods.": "Bosques encantados.",
    "Engineering at its finest.": "Ingeniería en su máxima expresión.",
    "Dark forest tales.": "Cuentos del bosque oscuro.",
    "Build. Automate. Conquer.": "Construye. Automatiza. Conquista.",
    "Twilight treasure.": "Tesoro crepuscular.",
    "Obtain this essential item.": "Obtén este objeto esencial.",
    "Boss trophy.": "Trofeo de jefe.",
    "Into the twilight.": "Hacia el crepúsculo.",
    "Progress awaits.": "El progreso espera.",
    "An important step forward.": "Un paso importante adelante.",
    "Socket your destiny.": "Engasta tu destino.",
    "Gear of legends.": "Equipo de leyendas.",
    "Forge your path forward.": "Forja tu camino hacia adelante.",
    "Twilight bound.": "Atado al crepúsculo.",
    "Rarity defines power.": "La rareza define el poder.",
    "The jeweler's art.": "El arte del joyero.",
    "Conquer or flee.": "Conquista o huye.",
    "Collect and conquer.": "Recolecta y conquista.",
    "Dig deeper.": "Cava más profundo.",
    "Mythic craftsmanship.": "Artesanía mítica.",
    "Climbing and Safety": "Escalada y Seguridad",
    "Face the beast.": "Enfrenta a la bestia.",
    "Ritual mastery.": "Maestría ritual.",
    "Chemical mastery.": "Maestría química.",
    "Nuclear ambition.": "Ambición nuclear.",
    "Magic flows through you.": "La magia fluye a través de ti.",
    "Master the glyphs.": "Domina los glifos.",
    "A novice's journey.": "El viaje de un novato.",
    "Automate your spells and rituals": "Automatiza tus hechizos y rituales",
    "Dark arts.": "Artes oscuras.",
    "Organize everything.": "Organízalo todo.",
    "Words of power.": "Palabras de poder.",
    "Nether's bounty.": "Recompensa del Nether.",
    "Sort and store.": "Ordena y almacena.",
    "Reactor engineering.": "Ingeniería de reactor.",
    "Fusion frontier.": "Frontera de la fusión.",
    "Autocrafting dreams.": "Sueños de crafteo automático.",
    "Cloud hopping.": "Saltando entre nubes.",
    "Levered Up!": "¡Apalancado!",
    "Full Steam Ahead!": "¡A Todo Vapor!",
    "Brush off the dust.": "Quita el polvo.",
    "Polished with sandpaper.": "Pulido con papel de lija.",
    "Learning the basics.": "Aprendiendo lo básico.",
    "When science surpasses magic.": "Cuando la ciencia supera a la magia.",
    "Redstone + Create = Complicated": "Redstone + Create = Complicado",
    "Glory to the hunter": "Gloria al cazador",
    "Predator's reward": "Recompensa del depredador",
    "Bounty hunter's mark": "Marca del cazarrecompensas",
    "Hunt or be hunted": "Caza o sé cazado",
    "The thrill of the chase": "La emoción de la persecución",
    "Fire and brimstone": "Fuego y azufre",
    "Kindled in the warmth of ancient hearths": "Avivado en el calor de hogares ancestrales",
    "The underworld beckons": "El inframundo llama",
    "Warp across the world": "Atraviesa el mundo",
    "The mage's arsenal": "El arsenal del mago",
    "Into the void": "Hacia el vacío",
    "Dragon's domain": "Dominio del dragón",
    "The final frontier": "La frontera final",
    "Master of Arcana": "Maestro de los Arcanos",
    "Evocation Rune": "Runa de Evocación",
    "All packages 10x12, 12x12...": "Todos los paquetes 10x12, 12x12...",
    "I'm so stressed! I need to measure it!": "¡Estoy muy estresado! ¡Necesito medirlo!",
    "Are they just gears, but named differently?": "¿No son solo engranajes con otro nombre?",
    "Don't wear this, it's not for clothes.": "No te lo pongas, no es para vestirse.",
    "This is not a Monkey Wrench": "Esto no es una llave inglesa",
    "It's really just a belt that doesn't move.": "En realidad es solo una cinta que no se mueve.",
    "A useful block for building contraptions.": "Un bloque útil para construir artefactos.",
    "Don't forget to superglue the pumpjack parts together.":
        "No olvides superpegar las partes del pumpjack.",
    "The underworld beckons": "El inframundo llama",
    # Glyph short descriptions
    "Used to mark blocks for rituals.": "Se usa para marcar bloques para rituales.",
    "Increases Max Mana and Regen.": "Aumenta el maná máximo y la regeneración.",
    "Delays the spell's effect.": "Retrasa el efecto del hechizo.",
    "Stores Source energy.": "Almacena energía de la Fuente.",
    "Used to craft new glyphs.": "Se usa para crear nuevos glifos.",
    "Crafts items from your inventory.": "Crea objetos desde tu inventario.",
    "Makes the spell effect last longer in place.": "Hace que el efecto del hechizo dure más en el sitio.",
    "Freezes nearby entities.": "Congela a las entidades cercanas.",
    "Generates Source from heat/burning.": "Genera Fuente a partir de calor/combustión.",
    "Raises undead minions.": "Levanta secuaces no-muertos.",
    "Speeds up time/growth.": "Acelera el tiempo/crecimiento.",
    "Condensed magical energy.": "Energía mágica condensada.",
    "Summons a Starbuncle to transport items.": "Invoca a un Starbuncle para transportar objetos.",
    "Strikes the target with lightning.": "Golpea al objetivo con un rayo.",
    "Awakens nearby blocks (e.g. Golems).": "Despierta bloques cercanos (p. ej. Gólems).",
    "Places a magical light source.": "Coloca una fuente de luz mágica.",
    "Conjures ores from the ground.": "Invoca minerales del suelo.",
    "Manipulates time to Moonrise.": "Manipula el tiempo hasta el amanecer lunar.",
    "Removes magical effects.": "Elimina los efectos mágicos.",
    "Grants flight to nearby players.": "Otorga vuelo a los jugadores cercanos.",
    "Summons a Wixie to automate crafting.": "Invoca a una Wixie para automatizar el crafteo.",
    "Throws items from inventory.": "Lanza objetos desde el inventario.",
    "Explodes into fireworks.": "Explota en fuegos artificiales.",
    "The ultimate spellbook.": "El libro de hechizos definitivo.",
    "Manipulates time to Sunrise.": "Manipula el tiempo hasta el amanecer.",
    "Summons a magical horse.": "Invoca un caballo mágico.",
    "Teleports you to a saved location.": "Te teletransporta a una ubicación guardada.",
    "Slows down targets.": "Ralentiza a los objetivos.",
    "Causes a magical explosion.": "Causa una explosión mágica.",
    "Phases through walls.": "Atraviesa paredes.",
    "Creates a temporary illusionary block.": "Crea un bloque ilusorio temporal.",
    "Launches the target into the air.": "Lanza al objetivo al aire.",
    "Prevents fall damage.": "Previene el daño por caída.",
    "Periodically grants random buffs.": "Otorga buffs aleatorios periódicamente.",
    "Launches entities with wind.": "Lanza entidades con viento.",
    "Generates Source from potions.": "Genera Fuente a partir de pociones.",
    "Deals direct magic damage.": "Inflige daño mágico directo.",
    "Damages all nearby entities.": "Daña a todas las entidades cercanas.",
    "Items are placed here for rituals.": "Aquí se colocan los objetos para los rituales.",
    "Draws permanent ritual circles.": "Dibuja círculos rituales permanentes.",
    "Swaps the target block with one from your inventory.":
        "Intercambia el bloque objetivo con uno de tu inventario.",
    "Controls magical servants.": "Controla a los sirvientes mágicos.",
    "Collects nearby items.": "Recoge los objetos cercanos.",
    "Emits a redstone signal.": "Emite una señal de redstone.",
    "Your first step into magic.": "Tu primer paso en la magia.",
    "Massively accelerates plant growth.": "Acelera enormemente el crecimiento de las plantas.",
    "Creates water source blocks.": "Crea bloques fuente de agua.",
    "Base block for magical structures.": "Bloque base para estructuras mágicas.",
    "Summons a decoy to distract enemies.": "Invoca un señuelo para distraer enemigos.",
    "Targets entities more precisely.": "Apunta a las entidades con más precisión.",
    "Increases spell damage.": "Aumenta el daño de los hechizos.",
    "Removes water/liquids.": "Elimina agua/líquidos.",
    "Breeds nearby animals.": "Cría a los animales cercanos.",
    "Splits the spell into multiple projectiles.": "Divide el hechizo en múltiples proyectiles.",
    "Simulates a right-click interaction.": "Simula una interacción de clic derecho.",
    "Upgraded spellbook for more power.": "Libro de hechizos mejorado para mayor poder.",
    "Locates nearby treasures/ores.": "Localiza tesoros/minerales cercanos.",
    "Controls the weather.": "Controla el clima.",
    "Makes you invisible.": "Te hace invisible.",
    "Names the target.": "Nombra al objetivo.",
    "Protects against magic.": "Protege contra la magia.",
    "Breaks trees in one go.": "Tala árboles de un solo golpe.",
    "Shoots a gust of air.": "Dispara una ráfaga de aire.",
    "Slows fall speed, allowing gliding.": "Reduce la velocidad de caída, permitiendo planear.",
    "Grow your own magical fibers.": "Cultiva tus propias fibras mágicas.",
    "Accelerates plant growth.": "Acelera el crecimiento de las plantas.",
    "Basic casting tool.": "Herramienta básica de lanzamiento.",
    "Summons a Drygmy to farm mobs.": "Invoca un Drygmy para granjear mobs.",
    "Sets targets on fire.": "Prende fuego a los objetivos.",
    "Generates Source from plant growth.": "Genera Fuente a partir del crecimiento de plantas.",
    "Your primary guide to magic. &7Read it carefully!":
        "Tu guía principal de magia. &7¡Léela con atención!",
    "Heals nearby entities.": "Cura a las entidades cercanas.",
    "Spells pierce through entities/walls.": "Los hechizos atraviesan entidades/paredes.",
    "Casts spells with arrows.": "Lanza hechizos con flechas.",
    "Increases gravity on the target.": "Aumenta la gravedad sobre el objetivo.",
    "Stores potions in bulk.": "Almacena pociones en grandes cantidades.",
    "Deals high physical damage.": "Inflige alto daño físico.",
    "Reflects spells.": "Refleja hechizos.",
    "Applies effects in an area.": "Aplica efectos en un área.",
    "Pulls enemies towards you.": "Atrae a los enemigos hacia ti.",
    "Casts the spell at your feet.": "Lanza el hechizo a tus pies.",
    "Freezes the target solid.": "Congela al objetivo por completo.",
    "Summons the Wilden Chimera boss.": "Invoca al jefe Quimera Wilden.",
    "Essential crafting material for robes.": "Material de crafteo esencial para túnicas.",
    "Breaks blocks instantly.": "Rompe bloques al instante.",
    "Reduces the duration of effects.": "Reduce la duración de los efectos.",
    "Slows down targets or projectiles.": "Ralentiza objetivos o proyectiles.",
    "Projectiles bounce off surfaces.": "Los proyectiles rebotan en las superficies.",
    "Magical wood for crafting.": "Madera mágica para el crafteo.",
    "Curses the target.": "Maldice al objetivo.",
    "Clears the surrounding area.": "Despeja el área circundante.",
    "Single-use spell scroll.": "Pergamino de hechizo de un solo uso.",
    "Summons a Whirlisprig for nature magic.": "Invoca a un Whirlisprig para la magia natural.",
    "Essential for performing rituals.": "Esencial para realizar rituales.",
    "Used for magical crafting and rituals.": "Se usa para el crafteo mágico y los rituales.",
    "Increases drop rates (Fortune).": "Aumenta las probabilidades de drop (Fortuna).",
    "Shears sheep or breaks leaves.": "Esquila ovejas o rompe hojas.",
    "Highlights magical blocks.": "Resalta los bloques mágicos.",
    "Allows floating in the air.": "Permite flotar en el aire.",
    "Launches you into the air.": "Te lanza al aire.",
    "Projectiles orbit around you.": "Los proyectiles orbitan a tu alrededor.",
    "Harvests and replants crops.": "Cosecha y replanta cultivos.",
    "Summons wolves to fight for you.": "Invoca lobos para luchar por ti.",
    "Places a rune trap on the ground.": "Coloca una trampa rúnica en el suelo.",
    "Generates Source from food/decomposition.": "Genera Fuente a partir de comida/descomposición.",
    "Binds entities in place.": "Inmoviliza a las entidades en su sitio.",
    "Increases the spell's power.": "Aumenta el poder del hechizo.",
    "Reduces spell power but increases control.":
        "Reduce el poder del hechizo pero aumenta el control.",
    "Generates Source from mob sacrifice/breeding.":
        "Genera Fuente a partir del sacrificio/cría de mobs.",
    "Applies the Wither effect.": "Aplica el efecto Wither.",
    "Converts items into magical variants.": "Convierte objetos en variantes mágicas.",
    "Increases duration of effects.": "Aumenta la duración de los efectos.",
    "Summons a Vex to fight for you.": "Invoca un Vex para luchar por ti.",
    "Summons a golem to harvest amethyst.": "Invoca un gólem para cosechar amatista.",
    "Unlock Tier 3 Glyphs.": "Desbloquea Glifos de Nivel 3.",
    "Teleports you a short distance.": "Te teletransporta una distancia corta.",
    "Smelts blocks or items.": "Funde bloques u objetos.",
    "Advanced Mana Regeneration.": "Regeneración avanzada de maná.",
    "Summons waves of enemies.": "Invoca oleadas de enemigos.",
    "Summons Evoker Fangs.": "Invoca Colmillos del Evocador.",
    "Extracts blocks gently (Silk Touch).": "Extrae bloques con cuidado (Toque de Seda).",
    "Unlock Tier 1 Glyphs.": "Desbloquea Glifos de Nivel 1.",
    "Restores health.": "Restaura salud.",
    "Unlock Tier 2 Glyphs.": "Desbloquea Glifos de Nivel 2.",
    "Places a block from your inventory.": "Coloca un bloque de tu inventario.",
    "Finds simple ores.": "Encuentra minerales simples.",
    "Reduces spell mana cost.": "Reduce el coste de maná del hechizo.",
    "Summons Spirit Wolves.": "Invoca Lobos Espirituales.",
    "Increases damage taken by the target.": "Aumenta el daño recibido por el objetivo.",
    "Tip: Deals partial armor-piercing damage.":
        "Consejo: Inflige daño parcial perforante de armadura.",
    "Congratulations! Now you can go ahead and mine trees.":
        "¡Felicidades! Ahora puedes ir a minar árboles.",
    "Use a Freezer and Icestone to freeze an accessory":
        "Usa un Congelador e Icestone para congelar un accesorio",
    "Acts as a blaze burner and yes, you can use it to make a steam engine, but be warned that you do need to pump the carbon dioxide out (through an exhaust pipe or something similar).":
        "Funciona como un quemador de blaze y sí, puedes usarlo para hacer un motor de vapor, pero ten en cuenta que necesitas bombear el dióxido de carbono al exterior (a través de un tubo de escape o similar).",
    "A scorching gust forged into blade form": "Una ráfaga abrasadora forjada en forma de espada",
    "A lever that can be set to output any redstone level. It's basically an upgraded version of the basic lever.":
        "Una palanca que puede configurarse para emitir cualquier nivel de redstone. Es básicamente una versión mejorada de la palanca básica.",
    "Strengthened by my experience in the Brass, I am ready. The Valkyries require 10 victory medals to open their dungeon.":
        "Fortalecido por mi experiencia en el Latón, estoy listo. Las Valquirias requieren 10 medallas de victoria para abrir su mazmorra.",
    "Washing/Bulk Blasting.": "Lavado/Fundición en masa.",
    "Finally, nuclear": "Por fin, nuclear",
    "Flatten, press, repeat": "Aplanar, presionar, repetir",
    "Creosote-soaked and industry-ready": "Empapado en creosota y listo para la industria",
}

# =============================================================
# Pre-translated description (multi-line) lookup by stripped line
# =============================================================
DESC_LINES = {
    # Common opening/section labels
    "Find:": "Encuentra:",
    "Craft:": "Crea:",
    "Obtain:": "Obtén:",
    "Defeat:": "Derrota:",
    "Requirements:": "Requisitos:",
    "Required:": "Requerido:",
    "Reward:": "Recompensa:",
    "Rewards:": "Recompensas:",
    "Recipe:": "Receta:",
    "Recipe": "Receta",
    "Info:": "Información:",
    "Goal:": "Objetivo:",
    "Goals:": "Objetivos:",
    "Steps:": "Pasos:",
    "Description:": "Descripción:",
    "Effect:": "Efecto:",
    "Effects:": "Efectos:",
    "Stats:": "Estadísticas:",
    "Notes:": "Notas:",
    "Warning!": "¡Advertencia!",
    "Usage:": "Uso:",
    "Setup:": "Configuración:",
    "Costs:": "Costes:",
    "Features:": "Características:",
    "Important recipes:": "Recetas importantes:",
    "Important drops:": "Drops importantes:",
    "Links with other mods:": "Enlaces con otros mods:",
    "Links with others:": "Enlaces con otros:",
    "Target production:": "Producción objetivo:",
    "Form Glyphs (How):": "Glifos de Forma (Cómo):",
    "Effect Glyphs (What):": "Glifos de Efecto (Qué):",
    "Augment Glyphs (Modify):": "Glifos de Aumento (Modificar):",
    "Combines with Ars Nouveau rituals": "Se combina con los rituales de Ars Nouveau",
    "Combines with Ars Nouveau spells": "Se combina con los hechizos de Ars Nouveau",
    "Create a complete magical automation system!":
        "¡Crea un sistema de automatización mágica completo!",
    # Common closing
    "Good luck!": "¡Buena suerte!",
    "Good hunt!": "¡Buena caza!",
    "Have fun!": "¡Diviértete!",
    # Categories
    "Base Magic": "Magia Base",
    "Alchemy": "Alquimia",
    "Extensions": "Extensiones",
    "Technology": "Tecnología",
    "Dark Magic": "Magia Oscura",
    "Cooking": "Cocina",
    "Power": "Poder",
    # Common short bullet items (use both - and • forms)
    "- Orbit: Orbits around you": "- Órbita: Orbita a tu alrededor",
    "- Harm: Deals damage": "- Daño: Inflige daño",
    "- Break: Breaks blocks": "- Romper: Rompe bloques",
    "- Summon: Summons creatures": "- Invocar: Invoca criaturas",
    "- Amplify: +50% power": "- Amplificar: +50% poder",
    "- Extend Time: +50% duration": "- Prolongar Tiempo: +50% duración",
    "• Orbit: Orbits around you": "• Órbita: Orbita a tu alrededor",
    "• Harm: Deals damage": "• Daño: Inflige daño",
    "• Break: Breaks blocks": "• Romper: Rompe bloques",
    "• Summon: Summons creatures": "• Invocar: Invoca criaturas",
    "• Amplify: +50% power": "• Amplificar: +50% poder",
    "• Extend Time: +50% duration": "• Prolongar Tiempo: +50% duración",
    "• Combines with Ars Nouveau rituals": "• Se combina con los rituales de Ars Nouveau",
    "• Combines with Ars Nouveau spells": "• Se combina con los hechizos de Ars Nouveau",
    "• Touch: Melee spell": "• Toque: Hechizo cuerpo a cuerpo",
    "• Projectile: Fires a projectile": "• Proyectil: Dispara un proyectil",
    "• Self: Applies to you": "• Personal: Se aplica a ti",
    "• Heal: Heals": "• Curar: Cura",
    "• Ignite: Sets on fire": "• Encender: Prende fuego",
    "• Freeze: Freezes entities": "• Congelar: Congela entidades",
    "• Pierce: Passes through targets": "• Perforar: Atraviesa objetivos",
    "• AOE: Area of effect": "• AOE: Área de efecto",
    "• Drygmy farm with 10+ different mobs":
        "• Granja Drygmy con más de 10 mobs distintos",
    "• Network of 20+ Starbuncles": "• Red de más de 20 Starbuncles",
    "• Automatic cultivation of all magical plants":
        "• Cultivo automático de todas las plantas mágicas",
    "• Spell Parchment: For creating reusable spells":
        "• Pergamino de Hechizo: Para crear hechizos reutilizables",
    "• Magebloom: For generating Source": "• Magebloom: Para generar Fuente",
    "• Can be enchanted normally": "• Se puede encantar normalmente",
    "• Growth Ritual: Accelerates crops in an area":
        "• Ritual de Crecimiento: Acelera los cultivos en un área",
    "• Aviary Ritual: Generates passive mobs":
        "• Ritual del Aviario: Genera mobs pasivos",
    "• Extraction Ritual: Mines automatically":
        "• Ritual de Extracción: Mina automáticamente",
    "• Manifestation Ritual: Complex automatic crafts":
        "• Ritual de Manifestación: Crafteos automáticos complejos",
    "• Automatically collects and transports items":
        "• Recoge y transporta objetos automáticamente",
    "• Can be linked to chests with a Starbuncle Charm":
        "• Se puede vincular a cofres con un Amuleto Starbuncle",
    "• Automatically cultivates and harvests plants":
        "• Cultiva y cosecha plantas automáticamente",
    "• Accelerates crop growth": "• Acelera el crecimiento de los cultivos",
    "• Perfect for automating your magical farms":
        "• Perfecto para automatizar tus granjas mágicas",
    "• Requires a Drygmy Charm and Wilden Horns":
        "• Requiere un Amuleto Drygmy y Cuernos Wilden",
    "• The more mobs around, the more it produces!":
        "• ¡Cuantos más mobs haya alrededor, más produce!",
    "• Using Source Berries": "• Usando Bayas de Fuente",
    "• Creating a network of Source Links": "• Creando una red de Enlaces de Fuente",
    "• Equip up to 10 spells simultaneously":
        "• Equipa hasta 10 hechizos simultáneamente",
    "• Stores 1000 Source internally": "• Almacena 1000 de Fuente internamente",
    "• -25% cost on all spells": "• -25% de coste en todos los hechizos",
    "• Can be enchanted with Unbreaking and Mending":
        "• Se puede encantar con Irrompibilidad y Reparación",
    "• 4x Wilden Tribute": "• 4x Tributo Wilden",
    "• 5000 Source": "• 5000 de Fuente",
    "• Forms: How the spell is cast (Projectile, Touch, Self...)":
        "• Formas: Cómo se lanza el hechizo (Proyectil, Toque, Personal...)",
    "• Effects: What the spell does (Harm, Heal, Break...)":
        "• Efectos: Lo que hace el hechizo (Daño, Curar, Romper...)",
    "• Augments: Modifies the spell (Amplify, Extend Time...)":
        "• Aumentos: Modifica el hechizo (Amplificar, Prolongar Tiempo...)",
    "• Wilden Stalker : Fast and aggressive, drops Wilden Spike":
        "• Acechador Wilden: Rápido y agresivo, suelta Púa Wilden",
    "• Wilden Hunter : Ranged attacker, drops Wilden Horn":
        "• Cazador Wilden: Atacante a distancia, suelta Cuerno Wilden",
    "• Wilden Guardian : Powerful tank, drops Wilden Wing":
        "• Guardián Wilden: Tanque poderoso, suelta Ala Wilden",
    "• Creating the Drygmy (requires Wilden Horn)":
        "• Crear al Drygmy (requiere Cuerno Wilden)",
    "• Ars Nouveau - Base Magic": "• Ars Nouveau - Magia Base",
    "• Ars Creo - Alchemy": "• Ars Creo - Alquimia",
    "• Ars Addition - Extensions": "• Ars Addition - Extensiones",
    "• Ars Technica - Technology": "• Ars Technica - Tecnología",
    "• Ars Ocultas - Dark Magic": "• Ars Ocultas - Magia Oscura",
    "• Supreme Grimoire crafted": "• Grimorio Supremo creado",
    "• Archmage Robes equipped": "• Túnicas de Archimago equipadas",
    "• Complete automation in place": "• Automatización completa establecida",
    "• Unlimited magical power": "• Poder mágico ilimitado",
    "• Respect from all other mages": "• Respeto de todos los demás magos",
    "• END OF ARS TUTORIAL - YOU ARE FREE •":
        "• FIN DEL TUTORIAL DE ARS - ERES LIBRE •",
    "• Alchemy Cauldron: Brews magical potions":
        "• Caldero de Alquimia: Prepara pociones mágicas",
    "• Alchemical Reagents: Special alchemical ingredients":
        "• Reactivos Alquímicos: Ingredientes alquímicos especiales",
    "• Transmutation Recipes: Converts raw materials":
        "• Recetas de Transmutación: Convierte materias primas",
    "• Alchemical Flasks: Stores and transports potions":
        "• Frascos Alquímicos: Almacenan y transportan pociones",
    "• Source Concoctions: Source-enhanced potions":
        "• Brebajes de Fuente: Pociones mejoradas con Fuente",
    "• Alchemical Dyes • Unique magical dyes":
        "• Tintes Alquímicos • Tintes mágicos únicos",
    "• Alchemical Compounds • Base materials":
        "• Compuestos Alquímicos • Materiales base",
    "• Ars Creo potions are used in Ars Delight":
        "• Las pociones de Ars Creo se usan en Ars Delight",
    # Numbered list lines
    "1. Place an Enchanting Apparatus in the center":
        "1. Coloca un Aparato de Encantamiento en el centro",
    "2. Surround it with 8 Arcane Pedestals (2 blocks away)":
        "2. Rodéalo con 8 Pedestales Arcanos (a 2 bloques de distancia)",
    "3. Connect everything with Arcane Cores underground":
        "3. Conecta todo con Núcleos Arcanos bajo tierra",
    "2. Add Arcane Pedestals around (specific pattern per ritual)":
        "2. Añade Pedestales Arcanos alrededor (patrón específico por ritual)",
    "4. Activate with a Dominion Wand": "4. Activa con una Varita de Dominio",
    "1. Place a Ritual Brazier on the ground":
        "1. Coloca un Brasero Ritual en el suelo",
    "3. Place a Ritual Tablet on the brazier":
        "3. Coloca una Tableta Ritual sobre el brasero",
    "2. Add glyphs in order: Form • Effect • Augments":
        "2. Añade los glifos en orden: Forma • Efecto • Aumentos",
    "3. Starbuncle Network : Automatic item transport":
        "3. Red Starbuncle: Transporte automático de objetos",
    "4. Whirlisprig Farm : Automatic Magebloom cultivation":
        "4. Granja Whirlisprig: Cultivo automático de Magebloom",
    "5. Active Ritual: Maintain at least one ritual permanently":
        "5. Ritual Activo: Mantén al menos un ritual de forma permanente",
    # Headers / titles
    "Augment Glyphs (How better):": "Glifos de Aumento (Cómo mejor):",
    "Ritual Setup:": "Configuración del Ritual:",
    "Useful rituals:": "Rituales útiles:",
    "Familiars are magical creatures that assist you!":
        "¡Los familiares son criaturas mágicas que te asisten!",
    "Starbuncle :": "Starbuncle:",
    "Whirlisprig :": "Whirlisprig:",
    "Drygmy :": "Drygmy:",
    "Source is the vital energy of all magic in Ars Nouveau.":
        "La Fuente es la energía vital de toda la magia en Ars Nouveau.",
    "Capabilities:": "Capacidades:",
    "Requires in the Enchanting Apparatus:":
        "Requiere en el Aparato de Encantamiento:",
    "Congratulations! You are now a true Archmage. Time to create devastating spells!":
        "¡Felicidades! Ahora eres un verdadero Archimago. ¡Es hora de crear hechizos devastadores!",
    "Glyphs are the foundation of every spell in Ars Nouveau.":
        "Los glifos son la base de cada hechizo en Ars Nouveau.",
    "There are 3 categories of glyphs:": "Hay 3 categorías de glifos:",
    "The Scribes Table is your spell creation workshop!":
        "¡La Mesa del Escriba es tu taller de creación de hechizos!",
    "Basic spell example:": "Ejemplo de hechizo básico:",
    "Projectile + Harm = Boule de feu basique":
        "Proyectil + Daño = Bola de fuego básica",
    "Projectile + Harm + Amplify = Boule de feu puissante !":
        "Proyectil + Daño + Amplificar = ¡Bola de fuego poderosa!",
    "The Wilden are hostile magical creatures that appear at night in forests.":
        "Los Wilden son criaturas mágicas hostiles que aparecen de noche en los bosques.",
    "3 types de Wilden :": "3 tipos de Wilden:",
    "These creatures drop components essential for:":
        "Estas criaturas sueltan componentes esenciales para:",
    "Congratulations! You have mastered Ars Nouveau automation!":
        "¡Felicidades! ¡Has dominado la automatización de Ars Nouveau!",
    "Secret bonus: Try combining Projectile + Orbit + Harm + Amplify + Pierce + AOE for a devastating spell!":
        "Bonus secreto: ¡Prueba a combinar Proyectil + Órbita + Daño + Amplificar + Perforar + AOE para un hechizo devastador!",
    "The Enchanting Apparatus transforms ordinary items into magical artifacts!":
        "¡El Aparato de Encantamiento transforma objetos ordinarios en artefactos mágicos!",
    "Final tip: Experiment! Combinations create unique and powerful spells!":
        "Consejo final: ¡Experimenta! ¡Las combinaciones crean hechizos únicos y poderosos!",
    "Mage armor protects you and boosts your magical abilities!":
        "¡La armadura de mago te protege e impulsa tus habilidades mágicas!",
    "3 armor tiers:": "3 niveles de armadura:",
    "Special bonuses:": "Bonificaciones especiales:",
    "Rituals allow you to perform powerful and automated magic!":
        "¡Los rituales te permiten realizar magia poderosa y automatizada!",
    "Pro tip: Combine rituals with your Drygmys for complete automation!":
        "Consejo pro: ¡Combina rituales con tus Drygmys para una automatización completa!",
    "You have reached the SUMMIT!": "¡Has llegado a la CIMA!",
    "Your journey recap:": "Resumen de tu viaje:",
    "Mastered: Glyphs, spells, rituals, familiars":
        "Dominado: Glifos, hechizos, rituales, familiares",
    "Mastered: Potions, transmutations, reagents":
        "Dominado: Pociones, transmutaciones, reactivos",
    "Mastered: Enchanted foods, permanent buffs":
        "Dominado: Comidas encantadas, buffs permanentes",
    "Mastered: New glyphs, creative mechanics":
        "Dominado: Nuevos glifos, mecánicas creativas",
    "Mastered: Automation, efficiency, magical loops":
        "Dominado: Automatización, eficiencia, bucles mágicos",
    "Rewards of your progression:": "Recompensas de tu progresión:",
    "The magical world is yours!": "¡El mundo mágico es tuyo!",
    "Create, experiment, explore without limits.":
        "Crea, experimenta, explora sin límites.",
    "The possibilities are infinite now.": "Las posibilidades ahora son infinitas.",
    "Secret bonus: Try impossible combos,": "Bonus secreto: prueba combos imposibles,",
    "mix mods creatively!": "¡mezcla los mods de forma creativa!",
    "Every discovery will be stunning.": "Cada descubrimiento será impresionante.",
    "Ars Creo adds a complete alchemy system!":
        "¡Ars Creo añade un sistema de alquimia completo!",
    "Main features:": "Características principales:",
}

# =============================================================
# Bounty / chapter tail descriptions — common templated tail text
# Looked up by the part AFTER the first " — " in a stripped line
# =============================================================
TAIL_TRANSLATIONS = {
    "Take on bounties to hunt dangerous mobs. Track your prey and claim your reward!":
        "Acepta recompensas para cazar mobs peligrosos. Rastrea a tu presa y reclama tu recompensa.",
    "Every creature has a bounty on its head. Prove your worth as the ultimate hunter.":
        "Cada criatura tiene una recompensa por su cabeza. Demuestra tu valía como el cazador definitivo.",
    "The occult arts demand sacrifice and knowledge. Perform rituals to summon increasingly powerful entities.":
        "Las artes ocultas exigen sacrificio y conocimiento. Realiza rituales para invocar entidades cada vez más poderosas.",
    "Apothic Enchanting expands the enchantment system far beyond vanilla limitations.":
        "Apothic Enchanting expande el sistema de encantamientos mucho más allá de los límites vanilla.",
    "Mekanism Reactors bring fusion and fission to Minecraft. Generate massive amounts of energy — but handle with extreme care!":
        "Los Reactores Mekanism traen fusión y fisión a Minecraft. Genera enormes cantidades de energía, ¡pero manéjalos con extremo cuidado!",
    "Occultism lets you summon and bind spirits to do your bidding. From mining to crafting — demons do it all!":
        "Occultism te permite invocar y vincular espíritus para hacer tu voluntad. De la minería al crafteo, ¡los demonios lo hacen todo!",
    "The Twilight Forest is a magical dimension filled with unique bosses, structures, and treasures. Every corner holds a new mystery!":
        "El Bosque Crepuscular es una dimensión mágica llena de jefes únicos, estructuras y tesoros. ¡Cada rincón guarda un nuevo misterio!",
    "Iron's Spells brings a complete spellcasting system to Minecraft. Learn spells, craft scrolls, and unleash magical devastation!":
        "Iron's Spells trae un sistema completo de lanzamiento de hechizos a Minecraft. ¡Aprende hechizos, crea pergaminos y desata la devastación mágica!",
    "Brave the flames and explore the Nether's expanded content. Fortune favors the bold!":
        "Desafía las llamas y explora el contenido ampliado del Nether. ¡La fortuna favorece a los audaces!",
    "Every spell school offers unique abilities. Study them all and become the ultimate mage.":
        "Cada escuela de hechizos ofrece habilidades únicas. Estúdialas todas y conviértete en el mago definitivo.",
    "Engineering excellence at its finest. This component is vital for your Create-powered factory.":
        "Excelencia en ingeniería en su máxima expresión. Este componente es vital para tu fábrica impulsada por Create.",
    "These aren't ordinary backpacks — they can filter, sort, and even auto-feed you while you explore.":
        "Estas no son mochilas ordinarias: pueden filtrar, ordenar e incluso alimentarte automáticamente mientras exploras.",
    "The winery brings viticulture to Minecraft. Grow grapes, ferment wine, and craft the perfect vintage!":
        "La bodega trae la viticultura a Minecraft. ¡Cultiva uvas, fermenta vino y elabora la cosecha perfecta!",
    "Archaeology and paleontology bring history to life. Brush off the dust and uncover the past!":
        "La arqueología y la paleontología dan vida a la historia. ¡Quita el polvo y descubre el pasado!",
    "The Nether is a hostile dimension of fire, lava, and dangerous mobs. Are you prepared?":
        "El Nether es una dimensión hostil de fuego, lava y mobs peligrosos. ¿Estás preparado?",
    "From vineyard to glass — master the art of winemaking with this delightful mod.":
        "De la viña a la copa: domina el arte de la vinificación con este encantador mod.",
    "Mutant Monsters are twisted versions of vanilla mobs with terrifying new abilities. Can you survive?":
        "Los Monstruos Mutantes son versiones retorcidas de los mobs vanilla con aterradoras habilidades nuevas. ¿Podrás sobrevivir?",
    "Apotheosis gear takes enchanting to the next level. Socket gems and forge legendary equipment!":
        "El equipo de Apotheosis lleva el encantamiento al siguiente nivel. ¡Engasta gemas y forja equipo legendario!",
    "From the Naga to the Lich King — the Twilight Forest's bosses demand cunning and strength to defeat.":
        "De la Naga al Rey Liche: los jefes del Bosque Crepuscular exigen astucia y fuerza para ser derrotados.",
    "Master Create's iconic components and build the foundations of your mechanical empire.":
        "Domina los componentes icónicos de Create y construye los cimientos de tu imperio mecánico.",
    "Power your factory with windmills, water wheels, and steam engines.":
        "Alimenta tu fábrica con molinos de viento, ruedas hidráulicas y motores de vapor.",
    "Automate every aspect of your base with Create's logistics tools.":
        "Automatiza cada aspecto de tu base con las herramientas logísticas de Create.",
    "Build the foundation of a complete magical automation system.":
        "Construye los cimientos de un sistema de automatización mágica completo.",
    "Apothic Spawners let you control mob spawning like never before.":
        "Apothic Spawners te permite controlar la generación de mobs como nunca antes.",
    "The Aether is a heavenly dimension full of floating islands, unique mobs, and divine treasures.":
        "El Aether es una dimensión celestial llena de islas flotantes, mobs únicos y tesoros divinos.",
    "Sophisticated Backpacks and Storage bring intelligent container solutions. Upgrade and customize your storage!":
        "Sophisticated Backpacks y Storage traen soluciones inteligentes de contenedores. ¡Mejora y personaliza tu almacenamiento!",
    "The waters hold countless treasures. Upgrade your fishing gear and explore every biome's aquatic life.":
        "Las aguas guardan incontables tesoros. Mejora tu equipo de pesca y explora la vida acuática de cada bioma.",
    "Harness rotational energy to automate your world!":
        "¡Aprovecha la energía rotacional para automatizar tu mundo!",
    "A key component in the Create mod's mechanical systems. Harness rotational energy to automate your world!":
        "Un componente clave en los sistemas mecánicos del mod Create. ¡Aprovecha la energía rotacional para automatizar tu mundo!",
    "Build a network of storage disks and crafters to automate your entire item management system.":
        "Construye una red de discos de almacenamiento y crafteadores para automatizar todo tu sistema de gestión de objetos.",
    "Craft Infused Alloy and an Advanced Control Circuit to unlock mid-tier Mekanism technology.":
        "Crea Aleación Infundida y un Circuito de Control Avanzado para desbloquear la tecnología de nivel medio de Mekanism.",
}

# Prefix item rarity names (Crown/Cog/Bevel/Sprocket/Sun) used in bounty headers
BOUNTY_RARITY_PREFIXES = {
    "Crown": "Corona",
    "Cog": "Engranaje",
    "Bevel": "Bisel",
    "Sprocket": "Piñón",
    "Sun": "Sol",
}

# =============================================================
# Mob names
# =============================================================
MOB_NAMES = {
    "Hoglin": "Hoglin",
    "Zombie": "Zombi",
    "Zombie Villager": "Aldeano Zombi",
    "Zombified Piglin": "Piglin Zombificado",
    "Skeleton": "Esqueleto",
    "Stray": "Vagabundo",
    "Wither Skeleton": "Esqueleto Wither",
    "Wither": "Wither",
    "Witch": "Bruja",
    "Warden": "Guardián",
    "Enderman": "Enderman",
    "Endermite": "Endermita",
    "Creeper": "Creeper",
    "Spider": "Araña",
    "Cave Spider": "Araña de Cueva",
    "Drowned": "Ahogado",
    "Ghast": "Ghast",
    "Phantom": "Fantasma",
    "Piglin": "Piglin",
    "Piglin Brute": "Piglin Bruto",
    "Pillager": "Saqueador",
    "Vindicator": "Vindicador",
    "Evoker": "Evocador",
    "Vex": "Vex",
    "Ravager": "Saqueador Bestial",
    "Silverfish": "Lepisma",
    "Slime": "Slime",
    "Magma Cube": "Cubo de Magma",
    "Elder Guardian": "Guardián Anciano",
    "Guardian": "Guardián",
    "Shulker": "Shulker",
    "Blaze": "Blaze",
    "Iron Golem": "Gólem de Hierro",
    "Snow Golem": "Gólem de Nieve",
    "Ender Dragon": "Dragón del End",
    "Bogged": "Atascado",
    "Breeze": "Brisa",
    "Zoglin": "Zoglin",
    "Naga": "Naga",
    "Lich": "Liche",
    "Hydra": "Hidra",
    "Ur-Ghast": "Ur-Ghast",
    "Snow Queen": "Reina de las Nieves",
    "Minoshroom": "Minoshroom",
    "Knight Phantom": "Caballero Fantasma",
    "Alpha Yeti": "Yeti Alfa",
    "Twilight Wraith": "Espectro Crepuscular",
    "Skeleton Druid": "Druida Esqueleto",
    "Redcap Goblin": "Goblin Caperuza Roja",
    "Redcap Sapper": "Zapador Caperuza Roja",
    "Kobold": "Kobold",
    "Cave Troll": "Troll de Cueva",
    "Goblin Knight": "Caballero Goblin",
    "Block and Chain Goblin": "Goblin Bola y Cadena",
    "Maze Slime": "Slime de Laberinto",
    "Slime Beetle": "Escarabajo Slime",
    "Pinch Beetle": "Escarabajo Pinza",
    "Towerwood Borer": "Taladrador Maderatorre",
    "Hedge Spider": "Araña de Seto",
    "Swarm Spider": "Araña Enjambre",
    "King Spider": "Rey Araña",
    "Helmet Crab": "Cangrejo Casco",
    "Mosquito Swarm": "Enjambre de Mosquitos",
    "Death Tome": "Tomo de la Muerte",
    "Carminite Ghastling": "Ghastling Carmín",
    "Carminite Golem": "Gólem Carmín",
    "Carminite Broodling": "Vástago Carmín",
    "Adherent": "Adherente",
    "Harbinger Cube": "Cubo Heraldo",
    "Roving Cube": "Cubo Errante",
    "Armored Giant": "Gigante Armado",
    "Giant Miner": "Minero Gigante",
    "Minotaur": "Minotauro",
    "Ice Core": "Núcleo de Hielo",
    "Fire Beetle": "Escarabajo de Fuego",
    "Snow Guardian": "Guardián de Nieve",
    "Stable Ice Core": "Núcleo de Hielo Estable",
    "Unstable Ice Core": "Núcleo de Hielo Inestable",
    "Foliaath": "Foliaath",
    "Barako": "Barako",
    "Barakoa": "Barakoa",
    "Barakoana": "Barakoana",
    "Umvuthana": "Umvuthana",
    "Umvuthi": "Umvuthi",
    "Ferrous Wroughtnaut": "Wroughtnaut Ferroso",
    "Frostmaw": "Fauces Heladas",
    "Grottol": "Grottol",
    "Lantern": "Linterna",
    "Sculptor": "Escultor",
    "Sun Bird": "Pájaro del Sol",
    "Mutant Creeper": "Creeper Mutante",
    "Mutant Skeleton": "Esqueleto Mutante",
    "Mutant Zombie": "Zombi Mutante",
    "Mutant Enderman": "Enderman Mutante",
    "Mutant Snow Golem": "Gólem de Nieve Mutante",
    "Cockatrice": "Cocatriz",
    "Phyg": "Phyg",
    "Flying Cow": "Vaca Voladora",
    "Aerwhale": "Aérbalena",
    "Aerbunny": "Aérconejo",
    "Moa": "Moa",
    "Whirlwind": "Torbellino",
    "Sliders": "Deslizadores",
    "Slider": "Deslizador",
    "Valkyrie": "Valquiria",
    "Sentry": "Centinela",
    "Zephyr": "Céfiro",
    "Swet": "Swet",
    "Mimic": "Mímico",
    "Stalkers": "Acechadores",
    "Stalker": "Acechador",
    "Wilden Chimera": "Quimera Wilden",
    "Wilden Stalker": "Acechador Wilden",
    "Wilden Hunter": "Cazador Wilden",
    "Wilden Guardian": "Guardián Wilden",
    "Wilden Defender": "Defensor Wilden",
    "Wilden Boss": "Jefe Wilden",
    "Drygmy": "Drygmy",
    "Whirlisprig": "Whirlisprig",
    "Starbuncle": "Starbuncle",
    "Sylph": "Sílfide",
    "Wixie": "Wixie",
    "Carbuncle": "Carbunclo",
    "Amethyst Golem": "Gólem de Amatista",
    "Sun Spirit": "Espíritu del Sol",
    "Valkyrie Queen": "Reina Valquiria",
}

# =============================================================
# Phrase-level word/idiom replacements applied as last resort.
# Longest first. Whole-word boundary aware. Color-code safe.
# =============================================================
PHRASE_REPLACEMENTS = [
    # Verbs / action openings (sentences)
    ("You must defeat", "Debes derrotar"),
    ("You will need", "Necesitarás"),
    ("You need to", "Necesitas"),
    ("You can find", "Puedes encontrar"),
    ("You can craft", "Puedes crear"),
    ("You can also", "También puedes"),
    ("You can", "Puedes"),
    ("Make sure to", "Asegúrate de"),
    ("Be careful", "Ten cuidado"),
    ("Beware of", "Cuidado con"),
    ("Don't forget", "No olvides"),
    ("Click to", "Haz clic para"),
    ("Right-click", "Haz clic derecho"),
    ("Right click", "Haz clic derecho"),
    ("Click on", "Haz clic en"),
    ("Use it to", "Úsalo para"),
    ("Used to", "Se usa para"),
    ("Used for", "Se usa para"),
    ("Allows you to", "Te permite"),
    ("Allows to", "Permite"),
    ("Enables you to", "Te permite"),
    ("Helps you", "Te ayuda a"),
    ("Lets you", "Te permite"),
    ("Can be used to", "Se puede usar para"),
    ("Can be found in", "Se puede encontrar en"),
    ("Can be obtained from", "Se puede obtener de"),
    ("Can be crafted with", "Se puede crear con"),
    ("Required to", "Necesario para"),
    ("Necessary to", "Necesario para"),
    ("Essential for", "Esencial para"),
    ("Essential to", "Esencial para"),
    ("Found in", "Se encuentra en"),
    ("Drops from", "Lo soltan"),
    # Verbs at start
    ("Craft a ", "Crea un "),
    ("Craft an ", "Crea un "),
    ("Craft the ", "Crea el "),
    ("Craft ", "Crea "),
    ("Build a ", "Construye un "),
    ("Build the ", "Construye el "),
    ("Build ", "Construye "),
    ("Find a ", "Encuentra un "),
    ("Find the ", "Encuentra el "),
    ("Find ", "Encuentra "),
    ("Defeat the ", "Derrota al "),
    ("Defeat a ", "Derrota a un "),
    ("Defeat ", "Derrota "),
    ("Kill the ", "Mata al "),
    ("Kill a ", "Mata a un "),
    ("Kill ", "Mata "),
    ("Obtain a ", "Obtén un "),
    ("Obtain the ", "Obtén el "),
    ("Obtain ", "Obtén "),
    ("Get a ", "Consigue un "),
    ("Get the ", "Consigue el "),
    ("Collect a ", "Recolecta un "),
    ("Collect the ", "Recolecta el "),
    ("Collect ", "Recolecta "),
    ("Place a ", "Coloca un "),
    ("Place the ", "Coloca el "),
    ("Place ", "Coloca "),
    ("Use the ", "Usa el "),
    ("Use a ", "Usa un "),
    ("Use ", "Usa "),
    ("Discover the ", "Descubre el "),
    ("Discover a ", "Descubre un "),
    ("Discover ", "Descubre "),
    ("Mine the ", "Mina el "),
    ("Mine a ", "Mina un "),
    ("Mine ", "Mina "),
    ("Harvest the ", "Cosecha el "),
    ("Harvest a ", "Cosecha un "),
    ("Harvest ", "Cosecha "),
    ("Smelt a ", "Funde un "),
    ("Smelt ", "Funde "),
    ("Capture a ", "Captura un "),
    ("Capture the ", "Captura el "),
    ("Visit the ", "Visita el "),
    ("Visit ", "Visita "),
    ("Explore the ", "Explora el "),
    ("Explore ", "Explora "),
    ("Hunt the ", "Caza al "),
    ("Hunt ", "Caza "),
    ("Summon the ", "Invoca al "),
    ("Summon a ", "Invoca un "),
    ("Summon ", "Invoca "),
    ("Forge the ", "Forja el "),
    ("Forge a ", "Forja un "),
    ("Forge ", "Forja "),
    ("Welcome to ", "Bienvenido a "),
    ("How to ", "Cómo "),
    # Common phrases
    ("Tip:", "Consejo:"),
    ("Warning:", "Advertencia:"),
    ("Note:", "Nota:"),
    ("WARNING:", "ADVERTENCIA:"),
    ("NOTE:", "NOTA:"),
    ("TIP:", "CONSEJO:"),
    ("Hunter:", "Cazador:"),
    ("Requires:", "Requiere:"),
    ("Required:", "Requerido:"),
    ("Reward:", "Recompensa:"),
    ("Rewards:", "Recompensas:"),
    ("Effect:", "Efecto:"),
    ("Stats:", "Estadísticas:"),
    ("Goal:", "Objetivo:"),
    ("Goals:", "Objetivos:"),
    ("Recipe:", "Receta:"),
    ("Description:", "Descripción:"),
    # Common nouns/multi-word
    ("Main Quest", "Misión Principal"),
    ("Side Quest", "Misión Secundaria"),
    ("World Boss", "Jefe del Mundo"),
    ("World Bosses", "Jefes del Mundo"),
    ("Boss Fight", "Batalla de Jefe"),
    ("Boss Battle", "Batalla de Jefe"),
    ("End of the game", "Final del juego"),
    ("Nearly impossible", "Casi imposible"),
    ("Absolute perfection", "Perfección absoluta"),
    ("The Beginning", "El Comienzo"),
    ("The End", "El End"),
    ("Getting Started", "Para Comenzar"),
    ("DECO & CONSTRUCTION", "DECO Y CONSTRUCCIÓN"),
    ("STAGE", "ETAPA"),
    # Items
    ("Item Frame", "Marco de Objeto"),
    ("Glass Bottle", "Botella de Cristal"),
    ("Ender Pearl", "Perla de Ender"),
    ("Eye of Ender", "Ojo de Ender"),
    ("Blaze Rod", "Vara de Blaze"),
    ("Blaze Powder", "Polvo de Blaze"),
    ("Nether Star", "Estrella del Nether"),
    ("Dragon Egg", "Huevo de Dragón"),
    ("Mob Spawner", "Generador de Monstruos"),
    ("Spawn Egg", "Huevo Generador"),
    ("Music Disc", "Disco de Música"),
    ("Redstone Dust", "Polvo de Redstone"),
    ("Redstone Block", "Bloque de Redstone"),
    ("Redstone Torch", "Antorcha de Redstone"),
    ("Iron Ingot", "Lingote de Hierro"),
    ("Iron Nugget", "Pepita de Hierro"),
    ("Gold Ingot", "Lingote de Oro"),
    ("Gold Nugget", "Pepita de Oro"),
    ("Copper Ingot", "Lingote de Cobre"),
    ("Diamond Block", "Bloque de Diamante"),
    ("Iron Block", "Bloque de Hierro"),
    ("Gold Block", "Bloque de Oro"),
    ("Netherite Ingot", "Lingote de Netherita"),
    ("Netherite Scrap", "Resto de Netherita"),
    ("Ancient Debris", "Restos Antiguos"),
    ("Ender Chest", "Cofre de Ender"),
    ("Crafting Table", "Mesa de Crafteo"),
    ("Blast Furnace", "Alto Horno"),
    ("Brewing Stand", "Soporte de Pociones"),
    ("Enchanting Table", "Mesa de Encantamientos"),
    ("Spell Book", "Libro de Hechizos"),
    ("Spellbook", "Grimorio"),
    ("Sculk Vein", "Vena Sculk"),
    ("Sculk Veins", "Venas Sculk"),
    ("Sculk Jaws", "Fauces Sculk"),
    ("Infested Sculk", "Sculk Infestado"),
    ("Soul Crystal", "Cristal de Alma"),
    ("Soul Crystals", "Cristales de Alma"),
    ("Ancient Vase", "Vasija Antigua"),
    ("Ancient Vases", "Vasijas Antiguas"),
    ("Reinforced Deepslate", "Pizarra Profunda Reforzada"),
    ("Deeplands", "Tierras Profundas"),
    ("Echoing Forest", "Bosque del Eco"),
    ("Overcast Columns", "Columnas Nubladas"),
    ("Blooming Caverns", "Cavernas Florecientes"),
    ("redstone signal", "señal de redstone"),
    ("redstone signals", "señales de redstone"),
    ("Sculk vibrations", "vibraciones Sculk"),
    # Items - Iron tools
    ("Iron Sword", "Espada de Hierro"),
    ("Iron Pickaxe", "Pico de Hierro"),
    ("Iron Axe", "Hacha de Hierro"),
    ("Iron Shovel", "Pala de Hierro"),
    ("Iron Hoe", "Azada de Hierro"),
    ("Iron Helmet", "Casco de Hierro"),
    ("Iron Chestplate", "Peto de Hierro"),
    ("Iron Leggings", "Pantalones de Hierro"),
    ("Iron Boots", "Botas de Hierro"),
    ("Diamond Sword", "Espada de Diamante"),
    ("Diamond Pickaxe", "Pico de Diamante"),
    ("Diamond Axe", "Hacha de Diamante"),
    ("Diamond Helmet", "Casco de Diamante"),
    ("Diamond Chestplate", "Peto de Diamante"),
    ("Diamond Leggings", "Pantalones de Diamante"),
    ("Diamond Boots", "Botas de Diamante"),
    ("Wooden Sword", "Espada de Madera"),
    ("Wooden Pickaxe", "Pico de Madera"),
    ("Wooden Axe", "Hacha de Madera"),
    ("Wooden Shovel", "Pala de Madera"),
    ("Stone Sword", "Espada de Piedra"),
    ("Stone Pickaxe", "Pico de Piedra"),
    ("Stone Axe", "Hacha de Piedra"),
    ("Golden Sword", "Espada de Oro"),
    ("Golden Pickaxe", "Pico de Oro"),
    ("Golden Axe", "Hacha de Oro"),
    ("Netherite Sword", "Espada de Netherita"),
    ("Netherite Pickaxe", "Pico de Netherita"),
    ("Netherite Axe", "Hacha de Netherita"),
    ("Netherite Helmet", "Casco de Netherita"),
    ("Netherite Chestplate", "Peto de Netherita"),
    ("Netherite Leggings", "Pantalones de Netherita"),
    ("Netherite Boots", "Botas de Netherita"),
    # General Minecraft words
    ("Mining", "Minería"),
    ("Smelting", "Fundición"),
    ("Crafting", "Crafteo"),
    ("Brewing", "Elaboración"),
    ("Fishing", "Pesca"),
    ("Farming", "Agricultura"),
    ("Cooking", "Cocina"),
    ("Storage", "Almacenamiento"),
    ("Upgrade", "Mejora"),
    ("Quest", "Misión"),
    ("Quests", "Misiones"),
    ("Welcome", "Bienvenido"),
    ("Beginner", "Principiante"),
    ("Advanced", "Avanzado"),
    ("Expert", "Experto"),
    ("Master", "Maestro"),
    ("Legendary", "Legendario"),
    ("Mythic", "Mítico"),
    ("Rare", "Raro"),
    ("Common", "Común"),
    ("Uncommon", "Poco Común"),
    ("Epic", "Épico"),
    ("Dungeon", "Mazmorra"),
    ("Dungeons", "Mazmorras"),
    ("Treasure", "Tesoro"),
    ("Treasures", "Tesoros"),
    ("Loot", "Botín"),
    ("Boss", "Jefe"),
    ("Bosses", "Jefes"),
    # Schools / elements (lowercase too)
    ("Spellbook", "Grimorio"),
    ("Spell Book", "Libro de Hechizos"),
    ("Mana ", "Maná "),
    ("Source ", "Fuente "),
    # Endings
    (" each", " cada uno"),
    (" optional", " opcional"),
    (" required", " requerido"),
    (" available", " disponible"),
    # Articles & connectors handled separately (avoid mass rewrites)
    ("the surrounding", "el entorno"),
    ("its chests", "sus cofres"),
    ("traps", "trampas"),
    ("trap", "trampa"),
    ("wirelessly", "de forma inalámbrica"),
    ("an exhaust pipe", "un tubo de escape"),
    ("Reinforced", "Reforzado"),
    ("Otherwise", "De lo contrario"),
    ("Otherwise,", "De lo contrario,"),
    # Specific Create mod
    ("Stress Units", "Unidades de Estrés"),
    ("Stress Unit", "Unidad de Estrés"),
    # General glue
    ("nearby", "cercano"),
    ("nearby ", "cercano "),
]


# =============================================================
# Generic per-line translation pipeline
# =============================================================
COLOR_CODE_RE = re.compile(r"[§&][0-9a-fk-orA-FK-OR]")


def strip_color(s: str) -> str:
    return COLOR_CODE_RE.sub("", s)


def split_color_codes(text: str):
    """Split off leading and trailing color code sequences. Returns (prefix, core, suffix)."""
    prefix = ""
    suffix = ""
    m = re.match(r"^((?:[§&][0-9a-fk-orA-FK-OR])+)", text)
    if m:
        prefix = m.group(1)
        text = text[m.end():]
    m = re.search(r"((?:[§&][0-9a-fk-orA-FK-OR])+)$", text)
    if m:
        suffix = m.group(1)
        text = text[:m.start()]
    return prefix, text, suffix


def is_proper_noun_or_id(text: str) -> bool:
    if not text:
        return True
    if text.startswith("/"):
        return True
    if re.match(r"^[a-z_]+:[a-z0-9_/]+$", text):
        return True
    return False


def color_safe_phrase_replace(text: str) -> str:
    out = text
    for en, es in PHRASE_REPLACEMENTS:
        # Build a regex tolerant of trailing punctuation but with word boundary on the left
        if en.endswith(" "):
            # phrase ending with space — only need left boundary
            pattern = re.compile(r"(?<![A-Za-z])" + re.escape(en))
        elif en.startswith(" "):
            pattern = re.compile(re.escape(en) + r"(?![A-Za-z])")
        else:
            pattern = re.compile(r"(?<![A-Za-z])" + re.escape(en) + r"(?![A-Za-z])")
        out = pattern.sub(es, out)
    return out


def translate_hunter(value: str):
    m = re.match(r"^Hunter:\s+(.+?)\s*\((\d+)\)\s*$", value)
    if not m:
        return None
    mob, num = m.group(1), m.group(2)
    mob_es = MOB_NAMES.get(mob, mob)
    return f"Cazador: {mob_es} ({num})"


TAIL_SPLIT_RE = re.compile(r"^(.*?)(\s+[—–]\s+)(.+)$")
LEADING_CODES = re.compile(r"^((?:[§&][0-9a-fk-orA-FK-OR])*)(.*?)((?:[§&][0-9a-fk-orA-FK-OR])*)$")


def translate_value_str(value: str) -> tuple[str, str]:
    """Translate a single string. Returns (translated, confidence)."""
    if not isinstance(value, str) or value == "":
        return value, "kept"

    # IDs / commands
    if is_proper_noun_or_id(value):
        return value, "kept"

    # Hunter
    h = translate_hunter(value)
    if h is not None:
        return h, "hunter"

    # Split color codes (leading/trailing)
    prefix, core, suffix = split_color_codes(value)
    stripped = core.strip()

    # Exact / flavor / desc lookups
    if stripped in EXACT:
        return prefix + EXACT[stripped] + suffix, "exact"
    if stripped in FLAVOR:
        return prefix + FLAVOR[stripped] + suffix, "flavor"
    if stripped in DESC_LINES:
        return prefix + DESC_LINES[stripped] + suffix, "flavor"

    # Stripped of ALL color codes (handles middle codes too).
    # If matched, reattach leading codes from original to preserve a color hint.
    fully_stripped = strip_color(value).strip()
    leading_match = re.match(r"^((?:[§&][0-9a-fk-orA-FK-OR])+)", value)
    leading = leading_match.group(1) if leading_match else ""
    if fully_stripped in EXACT:
        return leading + EXACT[fully_stripped], "exact"
    if fully_stripped in FLAVOR:
        return leading + FLAVOR[fully_stripped], "flavor"
    if fully_stripped in DESC_LINES:
        return leading + DESC_LINES[fully_stripped], "flavor"

    # Tail-template match: "X — TAIL" where TAIL is in TAIL_TRANSLATIONS
    # Try on both stripped variants
    for candidate in (stripped, fully_stripped):
        m = TAIL_SPLIT_RE.match(candidate)
        if m:
            head, sep, tail = m.group(1), m.group(2), m.group(3)
            if tail in TAIL_TRANSLATIONS:
                # Translate the head if it's a known item / rarity prefix
                head_es = BOUNTY_RARITY_PREFIXES.get(head.strip(), None)
                if head_es is None:
                    # Try existing lookups for head
                    if head.strip() in EXACT:
                        head_es = EXACT[head.strip()]
                    elif head.strip() in FLAVOR:
                        head_es = FLAVOR[head.strip()]
                if head_es is None:
                    # If head is a single Capitalized word, keep as-is (likely item proper noun)
                    head_es = head.strip()
                # Reconstruct using stripped form -> but try preserving original color codes around the value
                new_core_text = f"{head_es}{sep}{TAIL_TRANSLATIONS[tail]}"
                # Try to reapply prefix/suffix; if value had color codes, return prefix+core_translated+suffix
                # For broad reliability, just return prefix + new_core + suffix when starting from stripped
                if candidate is stripped:
                    return prefix + new_core_text + suffix, "flavor"
                else:
                    # Color codes are in the middle — return without code preservation
                    # but preserve any common leading code (e.g. "&c")
                    lead_match = re.match(r"^((?:[§&][0-9a-fk-orA-FK-OR])+)", value)
                    lead = lead_match.group(1) if lead_match else ""
                    # Use original codes pattern for head: re-wrap head with same leading codes if any
                    return lead + new_core_text, "flavor"

    # Header pattern: "&f—— X &f——"
    sep_match = re.match(r"^(&f—— )(.+?)( &f——)$", value)
    if sep_match:
        middle = sep_match.group(2)
        translated_middle, conf = translate_value_str(middle)
        if conf != "kept":
            return sep_match.group(1) + translated_middle + sep_match.group(3), conf

    # Phrase-level replacements
    new_core = color_safe_phrase_replace(core)
    if new_core != core:
        return prefix + new_core + suffix, "phrase"

    # Fallback: keep original English
    return value, "kept"


def translate_value(value):
    """Translate a string or list-of-strings. Returns (translated, confidences)."""
    if isinstance(value, str):
        out, conf = translate_value_str(value)
        return out, [conf]
    if isinstance(value, list):
        out_list = []
        confs = []
        for item in value:
            if isinstance(item, str):
                t, c = translate_value_str(item)
                out_list.append(t)
                confs.append(c)
            else:
                out_list.append(item)
                confs.append("kept")
        return out_list, confs
    return value, ["kept"]


# =============================================================
# BULK: Ars Nouveau tutorial chapter description lines (recurring)
# =============================================================
BULK = {
    "2. Add glyphs in order: Form → Effect → Augments":
        "2. Añade los glifos en orden: Forma → Efecto → Aumentos",
    "✦ Ars Nouveau - Base Magic": "✦ Ars Nouveau - Magia Base",
    "✦ Ars Creo - Alchemy": "✦ Ars Creo - Alquimia",
    "✦ Ars Addition - Extensions": "✦ Ars Addition - Extensiones",
    "✦ Ars Technica - Technology": "✦ Ars Technica - Tecnología",
    "✦ Ars Ocultas - Dark Magic": "✦ Ars Ocultas - Magia Oscura",
    "✓ Supreme Grimoire crafted": "✓ Grimorio Supremo creado",
    "✓ Archmage Robes equipped": "✓ Túnicas de Archimago equipadas",
    "✓ Complete automation in place": "✓ Automatización completa establecida",
    "✓ Unlimited magical power": "✓ Poder mágico ilimitado",
    "✓ Respect from all other mages": "✓ Respeto de todos los demás magos",
    "═ END OF ARS TUTORIAL - YOU ARE FREE ═":
        "═ FIN DEL TUTORIAL DE ARS - ERES LIBRE ═",
    "• Alchemical Dyes → Unique magical dyes":
        "• Tintes Alquímicos → Tintes mágicos únicos",
    "• Alchemical Compounds → Base materials":
        "• Compuestos Alquímicos → Materiales base",
    "• Reagents are used in Ars Addition recipes":
        "• Los reactivos se usan en las recetas de Ars Addition",
    "• Dyes enhance Ars Ocultas rituals":
        "• Los tintes potencian los rituales de Ars Ocultas",
    "Extreme Capabilities:": "Capacidades Extremas:",
    "• Equip 10 spells simultaneously (vs 10 for Novice)":
        "• Equipa 10 hechizos simultáneamente (vs 10 para Novato)",
    "• Stores 1000 Source internally (!)":
        "• Almacena 1000 de Fuente internamente (¡!)",
    "• -25% cost on ALL spells (monumental reduction)":
        "• -25% de coste en TODOS los hechizos (reducción monumental)",
    "• Compatible with Unbreaking and Mending":
        "• Compatible con Irrompibilidad y Reparación",
    "Required ingredients:": "Ingredientes requeridos:",
    "• 4x Wilden Tribute (intense combat!)":
        "• 4x Tributo Wilden (¡combate intenso!)",
    "• 5000 Source (HUGE reservoir)": "• 5000 de Fuente (reserva ENORME)",
    "Absurd advantages:": "Ventajas absurdas:",
    "• Cast complex spells fearlessly": "• Lanza hechizos complejos sin miedo",
    "• The -25% reduction stacks with armor":
        "• La reducción del -25% se acumula con la armadura",
    "• All your spells at your fingertips":
        "• Todos tus hechizos al alcance de tu mano",
    "• Enables impossible combos": "• Permite combos imposibles",
    "Integration with other mods:": "Integración con otros mods:",
    "• Uses Ars Creo powers": "• Usa los poderes de Ars Creo",
    "• Benefits from Ars Addition extensions":
        "• Se beneficia de las extensiones de Ars Addition",
    "• Automation via Ars Technica": "• Automatización vía Ars Technica",
    "• Dark magic from Ars Ocultas": "• Magia oscura de Ars Ocultas",
    "★ CONGRATULATIONS!": "★ ¡FELICIDADES!",
    "You are now a true ARCHMAGE!": "¡Ahora eres un verdadero ARCHIMAGO!",
    "The world of magic holds no more secrets for you.":
        "El mundo de la magia ya no tiene secretos para ti.",
    "It's time to create devastating spells!":
        "¡Es hora de crear hechizos devastadores!",
    "Ars Delight transforms cooking into magic!":
        "¡Ars Delight transforma la cocina en magia!",
    "Magical Foods:": "Comidas Mágicas:",
    "★ Sweet Berry Jam": "★ Mermelada de Bayas Dulces",
    "Slow but powerful regeneration": "Regeneración lenta pero poderosa",
    "Perfect for long exploration": "Perfecta para exploraciones largas",
    "★ Enchanted Bread": "★ Pan Encantado",
    "Instantly restores Source": "Restaura la Fuente al instante",
    "★ Spiced Meat": "★ Carne Especiada",
    "+20% damage for 2 minutes": "+20% de daño durante 2 minutos",
    "Temporary offensive boost": "Impulso ofensivo temporal",
    "★ Honey Cakes": "★ Pasteles de Miel",
    "PERMANENT magical buff": "Buff mágico PERMANENTE",
    "Persistent effect even after respawn":
        "Efecto persistente incluso tras reaparecer",
    "Advantages:": "Ventajas:",
    "• Portable and lightweight consumables":
        "• Consumibles portátiles y ligeros",
    "• Powerful and varied effects": "• Efectos poderosos y variados",
    "• Cumulative buffs (can eat multiple)":
        "• Buffs acumulativos (puedes comer varios)",
    "• Perfect for dangerous adventures":
        "• Perfecto para aventuras peligrosas",
    "Ars Technica fuses magic with automation!":
        "¡Ars Technica fusiona la magia con la automatización!",
    "Technological Components:": "Componentes Tecnológicos:",
    "• Runic Processor: Processes spells automatically":
        "• Procesador Rúnico: Procesa hechizos automáticamente",
    "Casts spells without player interaction":
        "Lanza hechizos sin interacción del jugador",
    "Magical keywords and logic circuits":
        "Palabras clave mágicas y circuitos lógicos",
    "• Arcane Relay: Transfers magical energy":
        "• Relé Arcano: Transfiere energía mágica",
    "• Enchantment Core: Reinforcement core":
        "• Núcleo de Encantamiento: Núcleo de refuerzo",
    "Enhances your artifact capabilities":
        "Mejora las capacidades de tus artefactos",
    "Connects your generators and consumers":
        "Conecta tus generadores y consumidores",
    "• Automation of repetitive spells":
        "• Automatización de hechizos repetitivos",
    "• Magical performance improvements":
        "• Mejoras en el rendimiento mágico",
    "• Creation of complex and efficient systems":
        "• Creación de sistemas complejos y eficientes",
    "System examples:": "Ejemplos de sistemas:",
    "• Automatic farm with Drygmy + Technica":
        "• Granja automática con Drygmy + Technica",
    "• Magical crafting chain": "• Cadena de crafteo mágico",
    "• Self-powered ritual": "• Ritual autoalimentado",
    "• Enhances Ars Addition efficiency":
        "• Aumenta la eficiencia de Ars Addition",
    "• Creates loops with Ars Ocultas": "• Crea bucles con Ars Ocultas",
    "Source is the very essence of all magic!":
        "¡La Fuente es la esencia misma de toda la magia!",
    "What is Source?": "¿Qué es la Fuente?",
    "• The vital energy that powers your spells":
        "• La energía vital que alimenta tus hechizos",
    "• Regenerates naturally through specific elements":
        "• Se regenera de forma natural mediante elementos específicos",
    "• Magebloom: Plant that passively generates Source":
        "• Magebloom: Planta que genera Fuente de forma pasiva",
    "• Source Berries: Edible magical berries":
        "• Bayas de Fuente: Bayas mágicas comestibles",
    "• Source Links: Energy transfer connections":
        "• Enlaces de Fuente: Conexiones de transferencia de energía",
    "Le Source Jar :": "Tarro de Fuente:",
    "Stores up to 10,000 units of Source.":
        "Almacena hasta 10.000 unidades de Fuente.",
    "Mowzie's Mobs introduces legendary creatures with unique attack patterns. Study their weaknesses and claim victory!":
        "Mowzie's Mobs introduce criaturas legendarias con patrones de ataque únicos. ¡Estudia sus debilidades y reclama la victoria!",
    "Rituals are the most powerful magic in Ars Nouveau!":
        "¡Los rituales son la magia más poderosa de Ars Nouveau!",
    "Designing a Ritual:": "Diseñando un Ritual:",
    "3. Connect with Arcane Cores buried underground":
        "3. Conecta con Núcleos Arcanos enterrados bajo tierra",
    "5. Activate with Dominion Wand by clicking":
        "5. Activa con la Varita de Dominio haciendo clic",
    "Available rituals:": "Rituales disponibles:",
    "★ Ritual of Flowering": "★ Ritual de Floración",
    "Massively accelerates crop growth":
        "Acelera enormemente el crecimiento de los cultivos",
    "x100 growth speed in the zone":
        "x100 de velocidad de crecimiento en la zona",
    "★ Ritual of Overgrowth": "★ Ritual de Sobrecrecimiento",
    "Automatically generates natural resources":
        "Genera recursos naturales automáticamente",
    "Creates ore, wood, flowers in the zone":
        "Crea mineral, madera y flores en la zona",
    "★ Ritual of Conjuration": "★ Ritual de Conjuración",
    "Summons passive or hostile mobs": "Invoca mobs pasivos u hostiles",
    "Ideal for mob farms": "Ideal para granjas de mobs",
    "★ Ritual of Extraction (Ars Technica)":
        "★ Ritual de Extracción (Ars Technica)",
    "Automatically mines ores": "Mina minerales automáticamente",
    "Useful with Ars Technica for automation":
        "Útil con Ars Technica para la automatización",
    "★ Ritual of Manifestation (Ars Addition)":
        "★ Ritual de Manifestación (Ars Addition)",
    "Performs crafts automatically": "Realiza crafteos automáticamente",
    "Combined with pipes = magical factory":
        "Combinado con tuberías = fábrica mágica",
    "• Ingredients: specific per ritual":
        "• Ingredientes: específicos por ritual",
    "• More powerful = more expensive in energy":
        "• Más potente = más costoso en energía",
    "Pro Tips:": "Consejos pro:",
    "• Combine multiple rituals for synergies":
        "• Combina varios rituales para obtener sinergias",
    "• Create separate ritual zones to avoid bugs":
        "• Crea zonas de ritual separadas para evitar bugs",
    "• Combines with Ars Technica for total automation":
        "• Se combina con Ars Technica para una automatización total",
    "• Uses Ars Creo reagents for power":
        "• Usa los reactivos de Ars Creo como potencia",
    "• Enhanced by Ars Ocultas for dark rituals":
        "• Potenciado por Ars Ocultas para rituales oscuros",
    "The Enchanting Apparatus turns your dreams into reality!":
        "¡El Aparato de Encantamiento convierte tus sueños en realidad!",
    "• Surround it with 8 Arcane Pedestals (exactly 2 blocks away)":
        "• Rodéalo con 8 Pedestales Arcanos (exactamente a 2 bloques)",
    "• Connect them with Arcane Cores buried underground":
        "• Conéctalos con Núcleos Arcanos enterrados bajo tierra",
    "Essential recipes:": "Recetas esenciales:",
    "• Spell Parchment: Creates reusable spells":
        "• Pergamino de Hechizo: Crea hechizos reutilizables",
    "• Magebloom: Passively generates Source":
        "• Magebloom: Genera Fuente de forma pasiva",
    "• Source Gems: Stores large amounts of energy":
        "• Gemas de Fuente: Almacenan grandes cantidades de energía",
    "• Mage Robes: Powerful magical equipment":
        "• Túnicas de Mago: Equipo mágico poderoso",
    "Each recipe consumes a large amount of Source.":
        "Cada receta consume una gran cantidad de Fuente.",
    "Plan your energy production!": "¡Planifica tu producción de energía!",
    "Important: This is where you'll create items for Ars Creo, Delight, Addition, Technica and Ocultas!":
        "Importante: ¡Aquí es donde crearás los objetos para Ars Creo, Delight, Addition, Technica y Ocultas!",
    "You will explore 6 extraordinary magical mods:":
        "Explorarás 6 mods mágicos extraordinarios:",
    "★ Ars Nouveau - The foundation: magic, glyphs and spells":
        "★ Ars Nouveau - La base: magia, glifos y hechizos",
    "★ Ars Creo - Alchemy: potions and transmutations":
        "★ Ars Creo - Alquimia: pociones y transmutaciones",
    "★ Ars Addition - Extensions: new mechanics":
        "★ Ars Addition - Extensiones: nuevas mecánicas",
    "★ Ars Technica - Technology: magical automation":
        "★ Ars Technica - Tecnología: automatización mágica",
    "★ Ars Ocultas - Dark Magic: advanced rituals":
        "★ Ars Ocultas - Magia Oscura: rituales avanzados",
    "Get it and embark on this magical adventure!":
        "¡Consíguelo y embárcate en esta aventura mágica!",
    "The Scribes Table is your magical creation workshop!":
        "¡La Mesa del Escriba es tu taller de creación mágica!",
    "2. Select glyphs: FORM → EFFECT → AUGMENT":
        "2. Selecciona los glifos: FORMA → EFECTO → AUMENTO",
    "4. Confirm and your spell is created!":
        "4. ¡Confirma y tu hechizo está creado!",
    "Simple combo examples:": "Ejemplos de combos simples:",
    "Projectile + Harm = Basic bolt": "Proyectil + Daño = Rayo básico",
    "Projectile + Harm + Amplify = Powerful bolt":
        "Proyectil + Daño + Amplificar = Rayo poderoso",
    "Projectile + Harm + AOE = Explosion":
        "Proyectil + Daño + AOE = Explosión",
    "Projectile + Harm + Pierce = Piercing arrow":
        "Proyectil + Daño + Perforar = Flecha perforante",
    "Book capabilities:": "Capacidades del libro:",
    "• Stores up to 10 different spells":
        "• Almacena hasta 10 hechizos distintos",
    "• Each spell can be progressively improved":
        "• Cada hechizo se puede mejorar progresivamente",
    "• Switch spells using hotkeys":
        "• Cambia de hechizo con teclas rápidas",
    "Glyphs are the fundamental building blocks of all spells!":
        "¡Los glifos son los bloques fundamentales de todos los hechizos!",
    "The 3 categories of glyphs:": "Las 3 categorías de glifos:",
    "• Touch: Direct melee contact": "• Toque: Contacto cuerpo a cuerpo directo",
    "• Projectile: Launches a projectile": "• Proyectil: Lanza un proyectil",
    "• Self: Applies to yourself": "• Personal: Se aplica a ti mismo",
    "◆ EFFECT Glyphs (What the spell does)":
        "◆ Glifos de EFECTO (Lo que hace el hechizo)",
    "• Heal: Heals damage": "• Curar: Cura el daño",
    "◆ AUGMENT Glyphs (Improves the effect)":
        "◆ Glifos de AUMENTO (Mejora el efecto)",
    "• Pierce: Passes through obstacles": "• Perforar: Atraviesa obstáculos",
    "• AOE: Wide area of effect": "• AOE: Área de efecto amplia",
    "Familiars are magical creature assistants!":
        "¡Los familiares son ayudantes mágicos!",
    "Starbuncle - The Collector": "Starbuncle - El Recolector",
    "• Automatically collects items": "• Recoge objetos automáticamente",
    "• Carries up to 5 stacks": "• Lleva hasta 5 pilas",
    "• Can be linked to chests with Starbuncle Charm":
        "• Se puede vincular a cofres con un Amuleto Starbuncle",
    "• Dominion Wand to configure paths":
        "• Varita de Dominio para configurar rutas",
    "• Loves gems and precious resources":
        "• Le encantan las gemas y los recursos preciosos",
    "Whirlisprig - The Farmer": "Whirlisprig - El Granjero",
    "• Automatically cultivates and harvests":
        "• Cultiva y cosecha automáticamente",
    "• Accelerates crop growth x3":
        "• Acelera el crecimiento de los cultivos x3",
    "• Ideal for Magebloom farms": "• Ideal para granjas de Magebloom",
    "• Feeds on plants around it": "• Se alimenta de las plantas a su alrededor",
    "• Can manage multiple crops at once":
        "• Puede gestionar varios cultivos a la vez",
    "Drygmy - The Generator": "Drygmy - El Generador",
    "• Generates resources from mobs": "• Genera recursos a partir de mobs",
    "• Requires Drygmy Charm and Wilden Horns":
        "• Requiere Amuleto Drygmy y Cuernos Wilden",
    "• Produces more with more mobs around":
        "• Produce más cuantos más mobs haya alrededor",
    "• Resource type depends on environment":
        "• El tipo de recurso depende del entorno",
    "• Can reach massive yields":
        "• Puede alcanzar rendimientos enormes",
    "2. Or craft their charms at the Enchanting Apparatus":
        "2. O crea sus amuletos en el Aparato de Encantamiento",
    "4. Wait for the familiar to appear":
        "4. Espera a que aparezca el familiar",
    "The armor of a true powerful mage!":
        "¡La armadura de un verdadero mago poderoso!",
    "3 Power Tiers:": "3 niveles de poder:",
    "★ Novice Robes (Tier 1)": "★ Túnicas de Novato (Nivel 1)",
    "• Perfect for beginners": "• Perfectas para principiantes",
    "★ Apprentice Robes (Tier 2)": "★ Túnicas de Aprendiz (Nivel 2)",
    "• Recommended for progression": "• Recomendadas para la progresión",
    "★ Archmage Robes (Tier 3)": "★ Túnicas de Archimago (Nivel 3)",
    "• For true high-level mages": "• Para magos auténticos de alto nivel",
    "Special abilities:": "Habilidades especiales:",
    "• Stores personal Source": "• Almacena Fuente personal",
    "• Reduces cost of ALL your spells":
        "• Reduce el coste de TODOS tus hechizos",
    "• Allows longer magic sessions":
        "• Permite sesiones de magia más largas",
    "• Compatible with Unbreaking and Mending enchantments":
        "• Compatible con los encantamientos Irrompibilidad y Reparación",
    "• Awesome appearance!": "• ¡Apariencia increíble!",
    "Enchanting upgrades:": "Mejoras de encantamiento:",
    "• Unbreaking III → Near-infinite durability":
        "• Irrompibilidad III → Durabilidad casi infinita",
    "• Mending → Self-repairs by collecting XP":
        "• Reparación → Se autorepara al recoger XP",
    "• Protection IV → Reduces damage taken":
        "• Protección IV → Reduce el daño recibido",
    "• Silk Touch → Useful for mining":
        "• Toque de Seda → Útil para la minería",
    "Start with Novice, progress to Archmage":
        "Comienza con Novato y progresa hasta Archimago",
    "Each tier builds upon the previous one!":
        "¡Cada nivel se construye sobre el anterior!",
    "• Armor works with all Ars mods":
        "• La armadura funciona con todos los mods Ars",
    "• Its enchantments come from the Enchanting Apparatus":
        "• Sus encantamientos vienen del Aparato de Encantamiento",
    "• Compatible with Ars Ocultas rituals":
        "• Compatible con los rituales de Ars Ocultas",
    "Ars Ocultas adds the most powerful and darkest magic!":
        "¡Ars Ocultas añade la magia más poderosa y oscura!",
    "Dark Glyphs:": "Glifos Oscuros:",
    "★ Glyph of Malefice": "★ Glifo de Maleficio",
    "Inflicts a powerful curse": "Inflige una poderosa maldición",
    "Weakness, Slowness, Blinding combined":
        "Debilidad, Lentitud y Ceguera combinadas",
    "High energy cost": "Alto coste de energía",
    "★ Glyph of Dark Venom": "★ Glifo de Veneno Oscuro",
    "Poison and magical corruption": "Veneno y corrupción mágica",
    "Constant damage-over-time": "Daño continuo a lo largo del tiempo",
    "Can poison blocks": "Puede envenenar bloques",
    "★ Glyph of Void Gaze": "★ Glifo de Mirada del Vacío",
    "Blindness and disorientation": "Ceguera y desorientación",
    "Forces the enemy to fight blind":
        "Obliga al enemigo a luchar a ciegas",
    "Very useful in PvP": "Muy útil en PvP",
    "★ Glyph of Witchcraft": "★ Glifo de Brujería",
    "Corrupt magic and transformations":
        "Magia corrupta y transformaciones",
    "Modifies the environment chaotically":
        "Modifica el entorno de forma caótica",
    "Unpredictable but powerful": "Impredecible pero poderoso",
    "Dark Rituals:": "Rituales Oscuros:",
    "★ Ritual of Soul Absorption": "★ Ritual de Absorción de Almas",
    "Absorbs creature souls": "Absorbe las almas de las criaturas",
    "Generates dark energy": "Genera energía oscura",
    "Increases ritual power": "Aumenta el poder del ritual",
    "★ Ritual of Corruption": "★ Ritual de Corrupción",
    "Corrupts blocks and entities": "Corrompe bloques y entidades",
    "Transforms the environment": "Transforma el entorno",
    "Creates dark zones": "Crea zonas oscuras",
    "★ Ritual of the Void": "★ Ritual del Vacío",
    "Creates a zone of total chaos": "Crea una zona de caos total",
    "Destroys, creates, transforms randomly":
        "Destruye, crea y transforma aleatoriamente",
    "Handle with care!": "¡Manéjese con cuidado!",
    "Special Materials:": "Materiales Especiales:",
    "• Dark Gems: Concentrated dark Source":
        "• Gemas Oscuras: Fuente oscura concentrada",
    "• Void Essences: Energy from nothingness":
        "• Esencias del Vacío: Energía de la nada",
    "• Corruption Shards: Fragments of chaos":
        "• Fragmentos de Corrupción: Fragmentos de caos",
    "• Cursed Ingredients: Cursed materials":
        "• Ingredientes Malditos: Materiales malditos",
    "Advantages and Risks:": "Ventajas y Riesgos:",
    "✓ Incredibly powerful spells": "✓ Hechizos increíblemente poderosos",
    "✓ Rituals with unique effects": "✓ Rituales con efectos únicos",
    "✓ Perfect fusion with Ars Technica":
        "✓ Fusión perfecta con Ars Technica",
    "✗ Very high energy costs": "✗ Costes de energía muy altos",
    "✗ Possible magic instability": "✗ Posible inestabilidad mágica",
    "✗ Unpredictable looping effects":
        "✗ Efectos de bucle impredecibles",
    "• Uses Ars Creo reagents": "• Usa los reactivos de Ars Creo",
    "• Combines with Ars Technica for control":
        "• Se combina con Ars Technica para el control",
    "• Potentiated by Ars Addition": "• Potenciado por Ars Addition",
    "• Complementary to Ars Nouveau": "• Complementario a Ars Nouveau",
    "The Wilden are the natural guardians of magic!":
        "¡Los Wilden son los guardianes naturales de la magia!",
    "Wilden Stalker - The Swift": "Acechador Wilden - El Veloz",
    "• Fast and aggressive": "• Rápido y agresivo",
    "• Drop: Wilden Spike": "• Drop: Púa Wilden",
    "• Health: low": "• Vida: baja",
    "• Attack: fast physical": "• Ataque: físico rápido",
    "Wilden Hunter - The Shooter": "Cazador Wilden - El Tirador",
    "• Ranged attacker": "• Atacante a distancia",
    "• Drop: Wilden Horn (crucial!)": "• Drop: Cuerno Wilden (¡crucial!)",
    "• Health: medium": "• Vida: media",
    "• Attack: magical projectiles": "• Ataque: proyectiles mágicos",
    "Wilden Guardian - The Tank": "Guardián Wilden - El Tanque",
    "• Extremely powerful tank": "• Tanque extremadamente poderoso",
    "• Drop: Wilden Wing": "• Drop: Ala Wilden",
    "• Health: very high": "• Vida: muy alta",
    "• Attack: massive and slow": "• Ataque: masivo y lento",
    "• Wilden Horn → Drygmy Essence (crucial!)":
        "• Cuerno Wilden → Esencia Drygmy (¡crucial!)",
    "• Wilden Wing → Equipment and potions":
        "• Ala Wilden → Equipo y pociones",
    "• Wilden Tribute → Ultimate ritual":
        "• Tributo Wilden → Ritual definitivo",
    "Combat strategy:": "Estrategia de combate:",
    "Projectile + Harm + AOE + Amplify = Explosion":
        "Proyectil + Daño + AOE + Amplificar = Explosión",
    "Simple spells aren't enough, be creative!":
        "Los hechizos simples no bastan, ¡sé creativo!",
    "Appearance:": "Aparición:",
    "Wilden appear at night in magical forests":
        "Los Wilden aparecen de noche en los bosques mágicos",
    "They guard Source-rich areas":
        "Custodian las zonas ricas en Fuente",
    "Ars Addition massively expands Ars Nouveau capabilities!":
        "¡Ars Addition amplía enormemente las capacidades de Ars Nouveau!",
    "New Mechanics:": "Nuevas Mecánicas:",
    "• Spell Prism: Creatively redirects spells":
        "• Prisma de Hechizo: Redirige hechizos de forma creativa",
    "Allows creating complex spell chains":
        "Permite crear cadenas de hechizos complejas",
    "• Enhanced Glyphs: More powerful glyphs":
        "• Glifos Mejorados: Glifos más poderosos",
    "Upgraded versions of base glyphs":
        "Versiones mejoradas de los glifos base",
    "• Spell Charging: Accumulates power":
        "• Carga de Hechizo: Acumula poder",
    "Hold click to increase damage":
        "Mantén pulsado el clic para aumentar el daño",
    "• Arcane Bypass: Increases casting speed":
        "• Bypass Arcano: Aumenta la velocidad de lanzamiento",
    "Cast spells faster": "Lanza hechizos más rápido",
    "• Glyph Overloading: Overloads spells":
        "• Sobrecarga de Glifo: Sobrecarga los hechizos",
    "Creates unpredictable but powerful effects":
        "Crea efectos impredecibles pero poderosos",
    "Possibilities:": "Posibilidades:",
    "• More complex spell combos":
        "• Combos de hechizos más complejos",
    "• Automatic spell chains":
        "• Cadenas automáticas de hechizos",
    "• Spells based on timing and energy":
        "• Hechizos basados en tiempo y energía",
    "• Limitless creativity": "• Creatividad sin límites",
    "• Works with Ars Nouveau rituals":
        "• Funciona con los rituales de Ars Nouveau",
    "• Combines with Ars Technica for automation":
        "• Se combina con Ars Technica para la automatización",
    "• Can use Ars Creo potions":
        "• Puede usar las pociones de Ars Creo",
    # Lower-count but still recurring
    "Search it in the engineer's manual":
        "Búscalo en el manual del ingeniero",
    "Indispensable for writing spells.":
        "Indispensable para escribir hechizos.",
    "Used in the Inscription Table or Scroll Forge.":
        "Se usa en la Mesa de Inscripción o la Forja de Pergaminos.",
    "Hold W on the item to see it's uses":
        "Mantén pulsado W sobre el objeto para ver sus usos",
    "Multiplies the effect of the spell.":
        "Multiplica el efecto del hechizo.",
    "Combo: Projectile + Split + Harm = Shotgun blast.":
        "Combo: Proyectil + Dividir + Daño = Disparo de escopeta.",
    "Equip in Curios slot.": "Equipa en la ranura de Curios.",
    "Vital for high-tier mage gameplay.":
        "Vital para la jugabilidad de mago de alto nivel.",
    "The basic offensive glyph.": "El glifo ofensivo básico.",
    "Adds a time delay before the next glyph activates.":
        "Añade un retraso temporal antes de que se active el siguiente glifo.",
    "The Scribe's Table is used to turn Glyph Formulas and materials into learned glyphs.":
        "La Mesa del Escriba se usa para convertir Fórmulas de Glifo y materiales en glifos aprendidos.",
    "Automates crafting of complex items.":
        "Automatiza el crafteo de objetos complejos.",
    "Usage: Can be used in spell turrets for auto-crafting setups.":
        "Uso: Se puede usar en torretas de hechizos para configuraciones de crafteo automático.",
    "Creates a lingering cloud of the spell.":
        "Crea una nube persistente del hechizo.",
    "Combo: Projectile + Linger + Harm = Poison Cloud.":
        "Combo: Proyectil + Persistir + Daño = Nube Venenosa.",
    "Chills enemies, slowing them down significantly.":
        "Enfría a los enemigos, ralentizándolos significativamente.",
    "Consumes burnable items (coal, wood) to make source.":
        "Consume objetos inflamables (carbón, madera) para producir fuente.",
    "Setup: Good for early game power.":
        "Configuración: Bueno para energía al principio del juego.",
    "Summons skeletons or zombies to fight for you.":
        "Invoca esqueletos o zombis para luchar por ti.",
    "Accelerates tile entities (furnaces, machines) and crop growth.":
        "Acelera las tile entities (hornos, máquinas) y el crecimiento de cultivos.",
    "Usage: Great for speeding up production lines.":
        "Uso: Excelente para acelerar las líneas de producción.",
    "Crystallized Source.": "Fuente cristalizada.",
    "Used in crafting and to power some machines.":
        "Se usa en el crafteo y para alimentar algunas máquinas.",
    "Starbuncles are magical creatures that move items between inventories.":
        "Los Starbuncles son criaturas mágicas que mueven objetos entre inventarios.",
    "2. Give them Sourceberries to speed them up.":
        "2. Dales Bayas de Fuente para acelerarlos.",
    "Summons a lightning bolt from the sky.":
        "Invoca un rayo desde el cielo.",
    "Creates a Mage Light block that emits light level 15.":
        "Crea un bloque de Luz de Mago que emite luz de nivel 15.",
    "Attempts to generate ores under the brazier.":
        "Intenta generar minerales bajo el brasero.",
    "Ritual that skips the day to dusk.":
        "Ritual que adelanta el día hasta el anochecer.",
    "Negates other spell effects or debuffs.":
        "Anula otros efectos o debuffs de hechizos.",
    "Usage: Useful for PvP or removing accidental spell walls.":
        "Uso: Útil en PvP o para eliminar muros de hechizos accidentales.",
    "Summons a water block.": "Invoca un bloque de agua.",
    "Usage: Infinite water everywhere, or flood your enemies.":
        "Uso: Agua infinita en todas partes, o inunda a tus enemigos.",
    "Provides temporary creative flight.":
        "Proporciona vuelo creativo temporal.",
    "2. Shift-right-click the cauldron with a recipe to set it.":
        "2. Haz Shift + clic derecho en el caldero con una receta para configurarlo.",
    "Boosts the effect of the previous glyph.":
        "Potencia el efecto del glifo anterior.",
    "Rapidly grows trees and crops in a wide area.":
        "Hace crecer rápidamente árboles y cultivos en un área amplia.",
    "Launches an item from your inventory.":
        "Lanza un objeto desde tu inventario.",
    "Usage: Automating item disposal or feeding.":
        "Uso: Para automatizar la eliminación o alimentación de objetos.",
    "Automatically breeds animals in range.":
        "Cría automáticamente a los animales en rango.",
    "Gives random positive potion effects.":
        "Otorga efectos de poción positivos aleatorios.",
    "Decorative spell.": "Hechizo decorativo.",
    "Usage: Celebratory effects.": "Uso: Efectos festivos.",
    "Equip in a Curios ring slot.":
        "Equipa en una ranura de anillo de Curios.",
    "Discount allows for more complex spells.":
        "El descuento permite hechizos más complejos.",
    "Ritual that skips the night to dawn.":
        "Ritual que adelanta la noche hasta el amanecer.",
    "Calls a temporary spirit horse.":
        "Llama a un caballo espíritu temporal.",
    "Applies the Slowness potion effect.":
        "Aplica el efecto de la poción de Lentitud.",
    "Creates an explosion at the target.":
        "Crea una explosión en el objetivo.",
    "The Intangible glyph allows you to pass through blocks temporarily.":
        "El glifo Intangible te permite atravesar bloques temporalmente.",
    "Flings the entity upwards.": "Lanza a la entidad hacia arriba.",
    "Usage: Cast Self + Launch for a super jump.":
        "Uso: Lanza Personal + Lanzar para un super salto.",
    "Grants Slow Falling effect.": "Otorga el efecto de Caída Lenta.",
    "Usage: Cast Self + Slowfall before hitting the ground.":
        "Uso: Lanza Personal + Caída Lenta antes de tocar el suelo.",
    "Knocks back enemies or items.":
        "Empuja a los enemigos u objetos hacia atrás.",
    "Usage: Good for spacing in combat.":
        "Uso: Bueno para mantener distancias en combate.",
    "Consumes potions to generate source.":
        "Consume pociones para generar fuente.",
    "Setup: Automate potion brewing and feed them to the link.":
        "Configuración: Automatiza la elaboración de pociones y suministrálas al enlace.",
    "Places a block that disappears after a short time.":
        "Coloca un bloque que desaparece tras un breve tiempo.",
    "Usage: Temporary bridges or shielding.":
        "Uso: Puentes o protecciones temporales.",
    "A powerful offensive glyph that hits everything around the target point.":
        "Un poderoso glifo ofensivo que golpea todo alrededor del punto objetivo.",
    "Makes buffs or debuffs last longer.":
        "Hace que los buffs o debuffs duren más.",
    "Example: Orbit + Extend Time keeps the shield up longer.":
        "Ejemplo: Órbita + Prolongar Tiempo mantiene el escudo activo más tiempo.",
    "Holds ingredients for the Enchanting Apparatus.":
        "Sostiene los ingredientes para el Aparato de Encantamiento.",
    "Replaces the block you're looking at with the one in your offhand/hotbar.":
        "Reemplaza el bloque que estás mirando con el de tu mano secundaria/barra rápida.",
    "Usage: Excellent for building or upgrading walls.":
        "Uso: Excelente para construir o mejorar muros.",
    "Picks up items in a radius around the target.":
        "Recoge objetos en un radio alrededor del objetivo.",
    "Combo: Self + Pickup = Magnet.":
        "Combo: Personal + Recoger = Imán.",
    "Your first spell focus.": "Tu primer foco de hechizos.",
    "Stores one spell.": "Almacena un hechizo.",
    "Causes spell projectiles to ricochet.":
        "Hace que los proyectiles de hechizo reboten.",
    "Usage: Tricky shots around corners.":
        "Uso: Tiros engañosos en las esquinas.",
    "Effectively a target dummy that draws aggro.":
        "Es prácticamente un muñeco que atrae la atención de los enemigos.",
    "Usage: Drop one and run away!":
        "Uso: ¡Suelta uno y huye!",
    "Homing projectile modifier.": "Modificador de proyectil teledirigido.",
    "Usage: Ensures your spells don't miss moving targets.":
        "Uso: Asegura que tus hechizos no fallen a objetivos en movimiento.",
    "Boosts the power of offensive spells.":
        "Potencia el poder de los hechizos ofensivos.",
    "Can also cast spells on hit.":
        "También puede lanzar hechizos al golpear.",
    "Evaporates water or lava in the area.":
        "Evapora agua o lava en el área.",
    "Usage: Clearing underground floods.":
        "Uso: Para limpiar inundaciones subterráneas.",
    "Combo: Projectile + Interact = Remote Control.":
        "Combo: Proyectil + Interactuar = Control Remoto.",
    "Calls forth fangs from the ground to bite enemies.":
        "Hace surgir colmillos del suelo para morder a los enemigos.",
    "Grants the Invisibility potion effect.":
        "Otorga el efecto de la poción de Invisibilidad.",
    "Renames a mob or item.": "Renombra un mob u objeto.",
    "Usage: Apply a name tag without the item cost.":
        "Uso: Aplica una etiqueta de nombre sin el coste del objeto.",
    "Passively blocks some magical damage.":
        "Bloquea pasivamente algo de daño mágico.",
    "Can reflect spells when blocking.":
        "Puede reflejar hechizos al bloquear.",
    "Chops down the entire tree when hitting a log.":
        "Tala el árbol entero al golpear un tronco.",
    "Pushes entities away or clears grass.":
        "Empuja a las entidades o limpia hierba.",
    "Usage: Cast while in the air to activate.":
        "Uso: Lanza mientras estás en el aire para activar.",
    "Instantly smelts the target block or item drops.":
        "Funde instantáneamente el bloque objetivo o los drops de objetos.",
    "Bonemeals the target area.":
        "Aplica harina de hueso al área objetivo.",
    "Combo: AOE + Grow = Instant farm.":
        "Combo: AOE + Crecer = Granja instantánea.",
    "Applies the vanilla fire effect to the target.":
        "Aplica el efecto de fuego vanilla al objetivo.",
    "Combo: Combine with Projectile for a fireball, or Touch for a lighter.":
        "Combo: Combínalo con Proyectil para una bola de fuego, o con Toque para un encendedor.",
    "Setup: Perfect for magical farms.":
        "Configuración: Perfecto para granjas mágicas.",
    "The Worn Notebook is the most important item for getting started.":
        "El Cuaderno Desgastado es el objeto más importante para empezar.",
    "- Teaches you how to craft spells.":
        "- Te enseña a crear hechizos.",
    "- Explains all glyphs and rituals.":
        "- Explica todos los glifos y rituales.",
    "- Guides you through tier upgrades.":
        "- Te guía a través de las mejoras de nivel.",
    "Press 'C' (default) to open your spellbook.":
        "Pulsa 'C' (por defecto) para abrir tu grimorio.",
    "Provides regeneration to players and passive mobs.":
        "Proporciona regeneración a los jugadores y mobs pasivos.",
    "Applies a spell to arrows fired.":
        "Aplica un hechizo a las flechas disparadas.",
    "Great for long-range delivery.":
        "Excelente para envíos a larga distancia.",
    "Makes entities fall faster and unable to jump.":
        "Hace que las entidades caigan más rápido y no puedan saltar.",
    "Usage: Ground flying mobs.":
        "Uso: Para derribar mobs voladores.",
    "Crushes the target with gravitational force.":
        "Aplasta al objetivo con fuerza gravitacional.",
    "A utility item that can reflect projectiles.":
        "Un objeto utilitario que puede reflejar proyectiles.",
    "Also grants self-cosmetic effects.":
        "También otorga efectos cosméticos propios.",
    "Any glyph following AOE applies to all targets in a radius.":
        "Cualquier glifo después de AOE se aplica a todos los objetivos en un radio.",
    "Usage: Touch + AOE + Harm.": "Uso: Toque + AOE + Daño.",
    "Yanks the target closer.": "Tira del objetivo acercándolo.",
    "Combo: Projectile + Pull = Hookshot.":
        "Combo: Proyectil + Atraer = Gancho.",
    "Targets the block directly under you.":
        "Apunta al bloque justo debajo de ti.",
    "Combo: Underfoot + Launch = Super Jump.":
        "Combo: Bajo los Pies + Lanzar = Super Salto.",
    "Encases the target in ice blocks.":
        "Encierra al objetivo en bloques de hielo.",
    "Summons the endgame boss of Ars Nouveau.":
        "Invoca al jefe final de Ars Nouveau.",
    "Shortens status effects on the target.":
        "Acorta los efectos de estado en el objetivo.",
    "Reduces the velocity of entities.":
        "Reduce la velocidad de las entidades.",
    "Calls forth a Vex spirit ally.":
        "Convoca un aliado espíritu Vex.",
    "These are no ordinary mobs. Each one is a boss-tier encounter that demands strategy and skill.":
        "Estos no son mobs ordinarios. Cada uno es un encuentro de nivel jefe que exige estrategia y habilidad.",
    "Destroys blocks in a radius (mining).":
        "Destruye bloques en un radio (minería).",
    "Whirlisprigs generate source from crops and trees.":
        "Los Whirlisprigs generan fuente a partir de cultivos y árboles.",
    "The core of your magical workshop.":
        "El núcleo de tu taller mágico.",
    "2. Put ingredients on pedestals.":
        "2. Coloca los ingredientes sobre los pedestales.",
    "3. Put the main item in the Apparatus.":
        "3. Coloca el objeto principal en el Aparato.",
    "Acts as Shears on the target.":
        "Actúa como Tijeras sobre el objetivo.",
    "Jar of Light: Summons a light source.":
        "Tarro de Luz: Invoca una fuente de luz.",
    "Void Jar: Destroys items.": "Tarro del Vacío: Destruye objetos.",
    "Grant creative-like flight at the cost of mana.":
        "Otorga vuelo similar al modo creativo a cambio de maná.",
    "Projectiles spin around the caster.":
        "Los proyectiles giran alrededor del lanzador.",
    "Combo: Orbit + Splitting + Harm = Shield of damaging projectiles.":
        "Combo: Órbita + Dividir + Daño = Escudo de proyectiles dañinos.",
    "Heals the target entity.": "Cura a la entidad objetivo.",
    "Combo: Self + Heal = Survival essential.":
        "Combo: Personal + Curar = Esencial de supervivencia.",
    "Points towards common ores like Iron and Coal.":
        "Apunta hacia minerales comunes como Hierro y Carbón.",
    "Usage: Cast a spell *into* the rune to store it. When triggered, the stored spell is released.":
        "Uso: Lanza un hechizo *dentro* de la runa para almacenarlo. Al activarse, se libera el hechizo guardado.",
    "Consumes food items to create source.":
        "Consume objetos de comida para crear fuente.",
    "Higher saturation = More source.":
        "Más saturación = Más fuente.",
    "Usage: Self + Ender Inventory = Portable storage.":
        "Uso: Personal + Inventario Ender = Almacenamiento portátil.",
    "Traps mobs near the ritual brazier.":
        "Atrapa a los mobs cerca del brasero ritual.",
    "Usage: Useful when you only want the secondary effects of a spell.":
        "Uso: Útil cuando solo quieres los efectos secundarios de un hechizo.",
    "Inflicts Wither damage over time.":
        "Inflige daño de Wither con el tiempo.",
    "Places a block from your hotbar.":
        "Coloca un bloque de tu barra rápida.",
    "Combo: Projectile + Place Block for remote building.":
        "Combo: Proyectil + Colocar Bloque para construir a distancia.",
    "The most powerful glyphs.": "Los glifos más poderosos.",
    "Instant transportation in the direction you are looking.":
        "Transporte instantáneo en la dirección a la que miras.",
    "Harvests blocks as if using a Silk Touch tool.":
        "Cosecha bloques como si usaras una herramienta de Toque de Seda.",
    "Combo: Touch + Extract = Glass/Ice harvester.":
        "Combo: Toque + Extraer = Cosechadora de Vidrio/Hielo.",
    "Starts a raid-like event. Survive for loot.":
        "Inicia un evento tipo asalto. Sobrevive para obtener botín.",
    "Every great machine starts with a single component. This one is essential.":
        "Toda gran máquina empieza con un solo componente. Este es esencial.",
    "Grants access to stronger glyphs.":
        "Otorga acceso a glifos más fuertes.",
}

# Merge bulk into FLAVOR (FLAVOR is checked in translate_value_str)
FLAVOR.update(BULK)


def main() -> None:
    with INPUT_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    output: dict = {}
    stats = {"exact": 0, "hunter": 0, "flavor": 0, "phrase": 0, "kept": 0}
    kept_samples: list[tuple[str, str]] = []

    for key, value in data.items():
        translated, confs = translate_value(value)
        output[key] = translated
        for c in confs:
            stats[c] += 1
        # Track kept items for review (non-ID English content)
        if isinstance(value, str) and confs[0] == "kept" and not is_proper_noun_or_id(value):
            if len(kept_samples) < 30:
                kept_samples.append((key, value))

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    total = sum(stats.values())
    translated_count = total - stats["kept"]
    pct = (translated_count / total * 100.0) if total else 0
    print(f"Input entries:  {len(data)}")
    print(f"Output entries: {len(output)}")
    print(f"Lines processed: {total}")
    print(f"Translated:     {translated_count} ({pct:.1f}%)")
    print(f"  exact:        {stats['exact']}")
    print(f"  hunter:       {stats['hunter']}")
    print(f"  flavor:       {stats['flavor']}")
    print(f"  phrase:       {stats['phrase']}")
    print(f"Kept (EN):      {stats['kept']} ({100 - pct:.1f}%)")

    missing = set(data) - set(output)
    extra = set(output) - set(data)
    print(f"\nKey parity: missing={len(missing)}, extra={len(extra)}")
    assert len(output) == len(data), "Output key count must equal input"


if __name__ == "__main__":
    main()
