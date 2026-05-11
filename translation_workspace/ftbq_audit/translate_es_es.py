"""
Translate FTB Quests titles and subtitles from English to Spanish (Spain).
Reads to_translate_es_es.json, writes agent_outputs_other/es_es.json.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
INPUT_FILE = ROOT / "to_translate_es_es.json"
OUTPUT_DIR = ROOT / "agent_outputs_other"
OUTPUT_FILE = OUTPUT_DIR / "es_es.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# Hard-coded full-string translations (case-insensitive lookup on stripped)
# -------------------------------------------------------------
EXACT = {
    # Chapter titles / common section names
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
    # Common quest text
    "Congrats!": "¡Felicidades!",
    "Book": "Libro",
    "Paper": "Papel",
    "Enchanted Book": "Libro Encantado",
    "Arctic Fur": "Pelaje Ártico",
    "Arcane Essence": "Esencia Arcana",
    "Oil Tank": "Tanque de Petróleo",
    "Adjustable Gearshift": "Cambio de Marchas Ajustable",
    "Sigil Of Socketing": "Sigilo de Engaste",
    "Marine Form": "Forma Marina",
    "Refill Upgrade": "Mejora de Recarga",
    "Glyph Invisibility": "Glifo de Invisibilidad",
    "Ritual mastery.": "Maestría ritual.",
    "Chemical mastery.": "Maestría química.",
    "Nuclear ambition.": "Ambición nuclear.",
    "Magic flows through you.": "La magia fluye a través de ti.",
    "Master the glyphs.": "Domina los glifos.",
    "A novice's journey.": "El viaje de un novato.",
    "Automate your spells and rituals": "Automatiza tus hechizos y rituales",
    "Heart of the Deep": "Corazón de las Profundidades",
    "Dark Cartographer": "Cartógrafo Oscuro",
    "Sonorous Staff": "Bastón Sonoro",
    "Welcome to the Otherside": "Bienvenido al Otro Lado",
    "The Opening Ritual": "El Ritual de Apertura",
    "Frostfall": "Caída Helada",
    "Skyroot Origins": "Orígenes de Raíz Celeste",
    "Engineer's Workbench": "Banco de Trabajo del Ingeniero",
    "Guide": "Guía",
    "Chapter Quest": "Misión de Capítulo",
    "Tier up!": "¡Sube de nivel!",
    # Recurring short flavor (titles/subtitles)
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
    "Epic Ink": "Tinta Épica",
    "The Cursed Temple": "El Templo Maldito",
    "Deadly Curiosity": "Curiosidad Mortal",
    "Sculk Transmission": "Transmisión Sculk",
    "Soul Dust": "Polvo de Alma",
    "Age of Resonarium": "Era del Resonarium",
    "Resonarium Forge": "Forja de Resonarium",
    "Resonarium Gear": "Equipo de Resonarium",
    "Sonic Protection": "Protección Sónica",
    "Carapace of the Guardian": "Caparazón del Guardián",
    "Reinforced Echo Shard": "Fragmento de Eco Reforzado",
    "Avatar of the Warden": "Avatar del Guardián",
    "Soul Elytra": "Élitros del Alma",
    "The Forager's Trail": "El Sendero del Recolector",
    "Sustainable Waste": "Residuos Sostenibles",
    "Milling and Kneading": "Moler y Amasar",
    "Forteresse d'Or": "Fortaleza de Oro",
    "The Soup Kitchen": "La Cocina de Sopa",
    "Master of the Skies": "Maestro de los Cielos",
    "World Flavors": "Sabores del Mundo",
    "Dark arts.": "Artes oscuras.",
    "Organize everything.": "Organízalo todo.",
    "Words of power.": "Palabras de poder.",
    "Nether's bounty.": "Recompensa del Nether.",
    "Sort and store.": "Ordena y almacena.",
    "Reactor engineering.": "Ingeniería de reactor.",
    "Fusion frontier.": "Frontera de la fusión.",
    "Autocrafting dreams.": "Sueños de crafteo automático.",
    "Smart Filter": "Filtro Inteligente",
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
    "Mechanical Arm": "Brazo Mecánico",
    "Exchange?": "¿Intercambio?",
    "Iron Ore": "Mineral de Hierro",
    "Twilight treasure.": "Tesoro crepuscular.",
    "Obtain this essential item.": "Obtén este objeto esencial.",
    "Boss trophy.": "Trofeo de jefe.",
    "Train Tracks": "Vías de Tren",
    "Into the twilight.": "Hacia el crepúsculo.",
    "Read my description!": "¡Lee mi descripción!",
    "Alloy Infused": "Aleación Infundida",
    "Progress awaits.": "El progreso espera.",
    "An important step forward.": "Un paso importante adelante.",
    "Socket your destiny.": "Engasta tu destino.",
    "Gear of legends.": "Equipo de leyendas.",
    "Forge your path forward.": "Forja tu camino hacia adelante.",
    "Twilight bound.": "Atado al crepúsculo.",
    "Addon": "Complemento",
    "Rare Ink": "Tinta Rara",
    "Legendary Ink": "Tinta Legendaria",
    "Click me!": "¡Haz clic en mí!",
    "Precision Mechanism": "Mecanismo de Precisión",
    "Rarity defines power.": "La rareza define el poder.",
    "The jeweler's art.": "El arte del joyero.",
    "Conquer or flee.": "Conquista o huye.",
    "Fission Fuel Assembly": "Ensamblaje de Combustible de Fisión",
    "Collect and conquer.": "Recolecta y conquista.",
    "Dig deeper.": "Cava más profundo.",
    "Wrench": "Llave Inglesa",
    "Mythic craftsmanship.": "Artesanía mítica.",
    "Climbing and Safety": "Escalada y Seguridad",
    "Face the beast.": "Enfrenta a la bestia.",
}

# More color-wrapped flavor and descriptions
SUBTITLE_FLAVOR_EXT2 = {
    "Protection et puissance magiques ultimes": "Protección y poder mágicos definitivos",
    "L'Armure de l'Archimage": "La Armadura del Archimago",
    "Advanced rituals and cursed spells": "Rituales avanzados y hechizos malditos",
    "Ars Ocultas : Magie Sombre": "Ars Ocultas: Magia Oscura",
    "Aggressive magical night creatures": "Criaturas mágicas nocturnas agresivas",
    "New mechanics and enhanced glyphs": "Nuevas mecánicas y glifos mejorados",
    "Ars Addition : Extensions Puissantes": "Ars Addition: Extensiones Poderosas",
    "Survive the heat": "Sobrevive al calor",
    "Hellish adventure": "Aventura infernal",
    "Aquatic treasures": "Tesoros acuáticos",
    "Cast your line": "Lanza tu sedal",
    "Gone fishing!": "¡A pescar!",
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
    # Glyph/spell descriptions
    "Launches the target into the air.": "Lanza al objetivo al aire.",
    "Prevents fall damage.": "Previene el daño por caída.",
    "Periodically grants random buffs.": "Otorga buffs aleatorios periódicamente.",
    "Launches entities with wind.": "Lanza entidades con viento.",
    "Generates Source from potions.": "Genera Fuente a partir de pociones.",
    "Deals direct magic damage.": "Inflige daño mágico directo.",
    "Damages all nearby entities.": "Daña a todas las entidades cercanas.",
    "Items are placed here for rituals.": "Aquí se colocan los objetos para los rituales.",
    "Draws permanent ritual circles.": "Dibuja círculos rituales permanentes.",
    "Swaps the target block with one from your inventory.": "Intercambia el bloque objetivo con uno de tu inventario.",
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
    "Your primary guide to magic. &7Read it carefully!": "Tu guía principal de magia. &7¡Léela con atención!",
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
    "Reduces spell power but increases control.": "Reduce el poder del hechizo pero aumenta el control.",
    "Generates Source from mob sacrifice/breeding.": "Genera Fuente a partir del sacrificio/cría de mobs.",
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
    # Boss / discovery flavor
    "Spawner mastery awaits.": "Te espera la maestría del generador.",
    "Face the mutation.": "Enfrenta la mutación.",
    "Creature of legend.": "Criatura de leyenda.",
    "Forge the extraordinary.": "Forja lo extraordinario.",
    "Enhance and conquer.": "Mejora y conquista.",
    "A Sharp Start": "Un Comienzo Afilado",
    "Trophy of the hunt.": "Trofeo de la cacería.",
    "Fossils tell stories.": "Los fósiles cuentan historias.",
    "Prepare for the unknown.": "Prepárate para lo desconocido.",
    "Craft it in the transmutation stone": "Créalo en la piedra de transmutación",
    "Archaeological wonder.": "Maravilla arqueológica.",
    "Mutated menace.": "Amenaza mutada.",
    "Can be found in any biome": "Se puede encontrar en cualquier bioma",
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
    "Infinite Light &8Infinite Void.": "Luz Infinita &8Vacío Infinito.",
    # Items
    "Brass Casing": "Carcasa de Latón",
    "Copper Casing": "Carcasa de Cobre",
    "Grain and Fiber Bags": "Sacos de Grano y Fibra",
    "Hose Pulley": "Polea de Manguera",
    "Mechanical Press": "Prensa Mecánica",
    "Mechanical Mixer": "Mezcladora Mecánica",
    "Wither Skeleton Skull": "Calavera de Esqueleto Wither",
    "Fluid Tank": "Tanque de Fluidos",
    "Filter Upgrade": "Mejora de Filtro",
    "Any Train Track": "Cualquier Vía de Tren",
    "Enter the Nether": "Entra al Nether",
    "Nature Rune": "Runa de la Naturaleza",
    "Rare Material": "Material Raro",
    "Millstone": "Muela",
    # Chapter / sub titles batch
    "Gastronomie de l'Aether": "Gastronomía del Aether",
    "The Great Harvest Boxes": "Las Grandes Cajas de Cosecha",
    "Treasures of the Ancients": "Tesoros de los Antiguos",
    "Textile Crafting": "Crafteo Textil",
    "Automated Collection": "Recolección Automatizada",
    "The Goodest Boy": "El Mejor Perrito",
    "The Pastry Chef": "El Pastelero",
    "The Banquet Master": "El Maestro del Banquete",
    "The Age of Forge and Blade": "La Era de la Forja y la Espada",
    "The Cutting Board": "La Tabla de Cortar",
    "Cooking Equipment": "Equipo de Cocina",
    "The Sacred Stone": "La Piedra Sagrada",
    "Wild Botany": "Botánica Salvaje",
    "Fuel of the heavens": "Combustible de los cielos",
    "Ambrosium Energy": "Energía de Ambrosio",
    "Seed Master": "Maestro de Semillas",
    "Soil Alchemy": "Alquimia del Suelo",
    "Butchery and Carving": "Carnicería y Tallado",
    "The Bakery": "La Panadería",
    "Logistics and Storage": "Logística y Almacenamiento",
    "Main Courses": "Platos Principales",
    "Farmer Utilities": "Utilidades del Granjero",
    "Animal Friends": "Amigos Animales",
    "Banquets and Feasts": "Banquetes y Festines",
    "Oriental Decoration": "Decoración Oriental",
    "Learning the basics.": "Aprendiendo lo básico.",
    # Items / blocks
    "Uncommon Material": "Material Poco Común",
    "Common Material": "Material Común",
    "Epic Material": "Material Épico",
    "Mythic Material": "Material Mítico",
    "Stack Upgrade Tier 1": "Mejora de Pila Nivel 1",
    "Stack Upgrade Tier 2": "Mejora de Pila Nivel 2",
    "Stack Upgrade Tier 3": "Mejora de Pila Nivel 3",
    "Creeper": "Creeper",
    "Spider": "Araña",
    "Enderman": "Enderman",
    "Wither": "Wither",
    "Encased Fan": "Ventilador Encapsulado",
    "Rotation Speed Controller": "Controlador de Velocidad de Rotación",
    "Crafting Upgrade": "Mejora de Crafteo",
    "Pressure Disperser": "Dispersor de Presión",
    "Mechanical Piston": "Pistón Mecánico",
    "Mechanical Drill": "Taladro Mecánico",
    "Hell's Gate": "Puerta del Infierno",
    "Blank Rune": "Runa en Blanco",
    "Basic Control Circuit": "Circuito de Control Básico",
    "Ultimate Control Circuit": "Circuito de Control Definitivo",
    "Auto Blasting Upgrade": "Mejora de Fundición Auto",
    "Andesite, the Foundation": "Andesita, los Cimientos",
    "Advanced Void Upgrade": "Mejora de Vacío Avanzada",
    "Fluorite Gem": "Gema de Fluorita",
    "Item Drain": "Drenador de Objetos",
    "Deployer": "Desplegador",
    "Polished with sandpaper.": "Pulido con papel de lija.",
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
    "Mysterious Flesh": "Carne Misteriosa",
    "Smelting Upgrade": "Mejora de Fundición",
    "Advanced Feeding Upgrade": "Mejora de Alimentación Avanzada",
    "Steam Engine": "Motor de Vapor",
    "Gearboxes": "Cajas de Engranajes",
    "Backpack": "Mochila",
    "Dough": "Masa",
    "Andesite Alloy": "Aleación de Andesita",
    "Brush off the dust.": "Quita el polvo.",
    "Chain Conveyor": "Transportador de Cadena",
    "Tarnished Helmet": "Casco Deslustrado",
    "Cogwheels": "Engranajes",
    "Knightmetal Ingot": "Lingote de Metal de Caballero",
    "Mine Iron": "Mina Hierro",
    "Cloud hopping.": "Saltando entre nubes.",
    "Advanced Pickup Upgrade": "Mejora de Recogida Avanzada",
    "Levered Up!": "¡Apalancado!",
    "Water Wheels": "Ruedas Hidráulicas",
    "Silence de Mort": "Silencio Mortal",
    "Auto Smelting Upgrade": "Mejora de Fundición Auto",
    "Chemical Oxidizer": "Oxidador Químico",
    "Blasting Upgrade": "Mejora de Fundición",
    "Void Upgrade": "Mejora de Vacío",
    "Speed Upgrade": "Mejora de Velocidad",
    "Blaze Burner": "Quemador de Blaze",
    "Full Steam Ahead!": "¡A Todo Vapor!",
    "Stone Tools": "Herramientas de Piedra",
    "Stonecutter Upgrade": "Mejora de Cortapiedras",
    "When science surpasses magic.": "Cuando la ciencia supera a la magia.",
    "Advanced Technomancy": "Tecnomancia Avanzada",
    "Advanced Compacting Upgrade": "Mejora de Compactación Avanzada",
    "Runefused Gem": "Gema Runafusionada",
    "Redstone + Create = Complicated": "Redstone + Create = Complicado",
    "Basic Chemical Tank": "Tanque Químico Básico",
    "Experience Bottle": "Botella de Experiencia",
    "Le Gardien Aveugle": "El Guardián Ciego",
    "Brush": "Cepillo",
    "Enchanting Apparatus": "Aparato de Encantamiento",
    "Casing": "Carcasa",
    "Prismarine Crystals": "Cristales de Prismarina",
    "Smart Fluid Pipe": "Tubería de Fluido Inteligente",
    "Feeding Upgrade": "Mejora de Alimentación",
    "Pump Upgrade": "Mejora de Bomba",
    "Tunnels": "Túneles",
    "Engineer's Goggles": "Gafas del Ingeniero",
    "Crying Obsidian": "Obsidiana Llorona",
    "Magnet Upgrade": "Mejora de Imán",
    "Advanced Pump Upgrade": "Mejora de Bomba Avanzada",
    "Heart of the Depths": "Corazón de las Profundidades",
    "Advanced Alchemy Upgrade": "Mejora de Alquimia Avanzada",
    "Advanced Filter Upgrade": "Mejora de Filtro Avanzada",
    "Chain Drive": "Transmisión de Cadena",
    "Rod of Constant Rotation": "Vara de Rotación Constante",
    "Advanced Magnet Upgrade": "Mejora de Imán Avanzada",
    "Heart of the Deep": "Corazón de las Profundidades",
    "The Transmission Shaft": "El Eje de Transmisión",
    "The Source: Windmill": "La Fuente: Molino de Viento",
    "Heat: The Blaze Burner": "Calor: El Quemador de Blaze",
    "L'Appel des Profondeurs": "La Llamada de las Profundidades",
    "L'Ascension": "El Ascenso",
    "The Zanite Crystal": "El Cristal de Zanita",
    "Bronze Dungeon: The Slider": "Mazmorra de Bronce: El Deslizador",
    "The Power of Gravitite": "El Poder de la Gravitita",
    "Silver Dungeon: The Valkyrie Queen": "Mazmorra de Plata: La Reina Valquiria",
    "Gold Dungeon: The Sun Spirit": "Mazmorra de Oro: El Espíritu del Sol",
    "Moa Master": "Maestro de Moas",
    # Short flavor / subtitles
    "Fearsome adversary.": "Adversario temible.",
    "Soar above it all.": "Vuela sobre todo.",
    "Gather what you need.": "Reúne lo que necesitas.",
    "It's really just a belt that doesn't move.": "En realidad es solo una cinta que no se mueve.",
    "History preserved.": "Historia preservada.",
    "A new dawn awaits.": "Te espera un nuevo amanecer.",
    "A useful block for building contraptions.": "Un bloque útil para construir artefactos.",
    "Airborne adventure.": "Aventura aérea.",
    "Arsenal of the Void": "Arsenal del Vacío",
    "Dark enchantments.": "Encantamientos oscuros.",
    "Beyond mortal limits.": "Más allá de los límites mortales.",
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
    "All packages 10x12, 12x12...": "Todos los paquetes 10x12, 12x12...",
    "I'm so stressed! I need to measure it!": "¡Estoy muy estresado! ¡Necesito medirlo!",
    "Are they just gears, but named differently?": "¿No son solo engranajes con otro nombre?",
    "Don't wear this, it's not for clothes.": "No te lo pongas, no es para vestirse.",
    "This is not a Monkey Wrench": "Esto no es una llave inglesa",
    "Dormant Relic": "Reliquia Latente",
    "Call of the Void": "Llamada del Vacío",
    "[Click to read]": "[Haz clic para leer]",
    "Welcome to All of Create!": "¡Bienvenido a All of Create!",
}

# Short embedded color-stripped flavor for ext3
SUBTITLE_FLAVOR_EXT3 = {
    "The underworld beckons": "El inframundo llama",
    "Warp across the world": "Atraviesa el mundo",
    "The mage's arsenal": "El arsenal del mago",
    "Into the void": "Hacia el vacío",
    "Dragon's domain": "Dominio del dragón",
    "The final frontier": "La frontera final",
    "Master of Arcana": "Maestro de los Arcanos",
    "Votre Premier Sort": "Tu Primer Hechizo",
    "Evocation Rune": "Runa de Evocación",
}

# -------------------------------------------------------------
# Color-wrapped flavor (matched on stripped core text)
# -------------------------------------------------------------
SUBTITLE_FLAVOR_EXT = {
    "Track and eliminate": "Rastrea y elimina",
    "The Supreme Grimoire": "El Grimorio Supremo",
    "La Source de Magie": "La Fuente de Magia",
    "Les Familiers Magiques": "Los Familiares Mágicos",
    "La Table du Scribe": "La Mesa del Escriba",
    "Les Wilden Hostiles": "Los Wilden Hostiles",
    "Bienvenue dans l'Arcane": "Bienvenido al Arcano",
    "The power of magical production": "El poder de la producción mágica",
    "Complete spell collection": "Colección completa de hechizos",
    "Master of Glyphs": "Maestro de los Glifos",
    "Les premiers pas du mage": "Los primeros pasos del mago",
    "Automation Arcanique": "Automatización Arcana",
    "Infusing magic into items": "Infundiendo magia en objetos",
    "L'Armure du Mage": "La Armadura del Mago",
    "Large-scale magic": "Magia a gran escala",
    "Le Rituel Arcanique": "El Ritual Arcano",
    "Invoquer des compagnons arcaniques": "Invocar compañeros arcanos",
    "Store arcane energy": "Almacena energía arcana",
    "Ascension vers l'Archimage": "Ascenso al Archimago",
    "Discover magic runes": "Descubre las runas mágicas",
    "Create and customize your spells": "Crea y personaliza tus hechizos",
    "Facing the guardians of magic": "Enfrentando a los guardianes de la magia",
    "Master all 6 mods in harmony": "Domina los 6 mods en armonía",
    "Complete Ars Master": "Maestro Ars Completo",
    "Potions, transmutations and chemical reactions": "Pociones, transmutaciones y reacciones químicas",
    "Ars Creo : L'Alchemy Magique": "Ars Creo: La Alquimia Mágica",
    "The pinnacle of magical power": "El pináculo del poder mágico",
    "Enchanted food with permanent effects": "Comida encantada con efectos permanentes",
    "Ars Technica : Technology Magique": "Ars Technica: Tecnología Mágica",
    "Collect and store arcane energy": "Recolecta y almacena energía arcana",
    "Permanent large-scale magic": "Magia permanente a gran escala",
    "Les Rituels Arcaniques": "Los Rituales Arcanos",
    "Advanced and powerful magical crafts": "Crafteos mágicos avanzados y poderosos",
    "Discover 6 interdependent magic mods": "Descubre 6 mods de magia interdependientes",
    "Welcome to the Arcana": "Bienvenido a los Arcanos",
    "Create your own custom spells": "Crea tus propios hechizos personalizados",
    "Discover the basic magic runes": "Descubre las runas mágicas básicas",
    "Creatures that work for you": "Criaturas que trabajan para ti",
}

# -------------------------------------------------------------
# Hunter mobs (proper nouns kept, some translated)
# -------------------------------------------------------------
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
    "Hoglin": "Hoglin",
    # Twilight Forest
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
    # Mowzie's Mobs
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
    "Naga": "Naga",
    "Sculptor": "Escultor",
    "Sun Bird": "Pájaro del Sol",
    # Mutant Monsters
    "Mutant Creeper": "Creeper Mutante",
    "Mutant Skeleton": "Esqueleto Mutante",
    "Mutant Zombie": "Zombi Mutante",
    "Mutant Enderman": "Enderman Mutante",
    "Mutant Snow Golem": "Gólem de Nieve Mutante",
    # Aether
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
}


def translate_hunter(value: str) -> str | None:
    """Translate 'Hunter: <Mob> (<N>)' to 'Cazador: <Mob ES> (<N>)'."""
    m = re.match(r"^Hunter:\s+(.+?)\s*\((\d+)\)\s*$", value)
    if not m:
        return None
    mob, num = m.group(1), m.group(2)
    mob_es = MOB_NAMES.get(mob, mob)  # keep proper noun if unknown
    return f"Cazador: {mob_es} ({num})"


# -------------------------------------------------------------
# Hunting bounty subtitles (recurring short flavor texts)
# -------------------------------------------------------------
SUBTITLE_FLAVOR = {
    "Glory to the hunter": "Gloria al cazador",
    "Predator's reward": "Recompensa del depredador",
    "Bounty hunter's mark": "Marca del cazarrecompensas",
    "Hunt or be hunted": "Caza o sé cazado",
    "The thrill of the chase": "La emoción de la persecución",
    "Fire and brimstone": "Fuego y azufre",
    "Kindled in the warmth of ancient hearths": "Avivado en el calor de hogares ancestrales",
    "Protection et puissance arcanique": "Protección y poder arcano",
    "Premiers Glyphes": "Primeros Glifos",
    "L'Enchantement Arcanique": "El Encantamiento Arcano",
    "Ars Delight : Cooking Magique": "Ars Delight: Cocina Mágica",
}

# -------------------------------------------------------------
# Word-level replacements (whole-word, case-aware via regex)
# Applied as a last-resort heuristic on remaining English text.
# Ordered: longest phrases first.
# -------------------------------------------------------------
PHRASE_REPLACEMENTS = [
    # Multi-word phrases
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
    ("Gold Ingot", "Lingote de Oro"),
    ("Copper Ingot", "Lingote de Cobre"),
    ("Diamond Block", "Bloque de Diamante"),
    ("Iron Block", "Bloque de Hierro"),
    ("Gold Block", "Bloque de Oro"),
    ("Netherite Ingot", "Lingote de Netherita"),
    ("Netherite Scrap", "Resto de Netherita"),
    ("Ancient Debris", "Restos Antiguos"),
    ("Ender Chest", "Cofre de Ender"),
    ("Crafting Table", "Mesa de Crafteo"),
    ("Furnace", "Horno"),
    ("Blast Furnace", "Alto Horno"),
    ("Smoker", "Ahumador"),
    ("Brewing Stand", "Soporte de Pociones"),
    ("Enchanting Table", "Mesa de Encantamientos"),
    ("Beacon", "Faro"),
    # Verbs and quest actions
    ("Craft a ", "Crea un "),
    ("Craft an ", "Crea un "),
    ("Craft the ", "Crea el "),
    ("Build a ", "Construye un "),
    ("Build the ", "Construye el "),
    ("Find a ", "Encuentra un "),
    ("Find the ", "Encuentra el "),
    ("Defeat the ", "Derrota al "),
    ("Defeat a ", "Derrota a un "),
    ("Kill the ", "Mata al "),
    ("Kill a ", "Mata a un "),
    ("Obtain a ", "Obtén un "),
    ("Obtain the ", "Obtén el "),
    ("Collect a ", "Recolecta un "),
    ("Collect the ", "Recolecta el "),
    ("Place a ", "Coloca un "),
    ("Place the ", "Coloca el "),
    ("Use the ", "Usa el "),
    ("Use a ", "Usa un "),
    ("Discover the ", "Descubre el "),
    ("Discover a ", "Descubre un "),
    ("Welcome to ", "Bienvenido a "),
    ("The Beginning", "El Comienzo"),
    ("The End", "El End"),
    ("Getting Started", "Para Comenzar"),
    ("How to ", "Cómo "),
    # Quest UI words
    ("Main Quest", "Misión Principal"),
    ("Side Quest", "Misión Secundaria"),
    ("World Boss", "Jefe del Mundo"),
    ("World Bosses", "Jefes del Mundo"),
    ("The Magical", "Lo Mágico"),
    ("The Mechanical", "Lo Mecánico"),
    ("The Gastronomy", "La Gastronomía"),
    ("The Storage", "El Almacenamiento"),
    ("The Style", "El Estilo"),
    ("DECO & CONSTRUCTION", "DECO Y CONSTRUCCIÓN"),
    ("STAGE", "ETAPA"),
    # Common single words at start of titles (item names)
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
    ("Mining", "Minería"),
    ("Smelting", "Fundición"),
    ("Crafting", "Crafteo"),
    ("Brewing", "Elaboración"),
    ("Fishing", "Pesca"),
    ("Farming", "Agricultura"),
    ("Cooking", "Cocina"),
    ("Storage", "Almacenamiento"),
    ("Upgrade", "Mejora"),
    ("Recipe", "Receta"),
    ("Reward", "Recompensa"),
    ("Rewards", "Recompensas"),
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
]


def color_safe_phrase_replace(text: str) -> str:
    """Apply phrase replacements while preserving color codes (&x, §x)."""
    out = text
    for en, es in PHRASE_REPLACEMENTS:
        # Whole-word boundary - tolerate color codes around
        pattern = re.compile(r"(?<![A-Za-z])" + re.escape(en) + r"(?![A-Za-z])")
        out = pattern.sub(es, out)
    return out


# Common color code prefix/suffix pattern (e.g. "&7text&r" or "§7text§r")
COLOR_WRAP_RE = re.compile(r"^([§&][0-9a-fk-orA-FK-OR](?:[§&][0-9a-fk-orA-FK-OR])*)(.*?)((?:[§&][0-9a-fk-orA-FK-OR])*)$")


def split_color_codes(text: str):
    """Split off leading and trailing color code sequences. Returns (prefix, core, suffix)."""
    prefix = ""
    suffix = ""
    # leading codes
    m = re.match(r"^((?:[§&][0-9a-fk-orA-FK-OR])+)", text)
    if m:
        prefix = m.group(1)
        text = text[m.end():]
    # trailing codes
    m = re.search(r"((?:[§&][0-9a-fk-orA-FK-OR])+)$", text)
    if m:
        suffix = m.group(1)
        text = text[:m.start()]
    return prefix, text, suffix


def is_proper_noun_or_id(text: str) -> bool:
    """Detect if text is a Minecraft ID like 'create:gantry_carriage' or a command."""
    if not text:
        return True
    if text.startswith("/"):
        return True
    if re.match(r"^[a-z_]+:[a-z0-9_/]+$", text):
        return True
    return False


def translate_one(value: str) -> tuple[str, str]:
    """Translate a single value. Returns (translated, confidence_level).
    confidence_level: 'exact' | 'hunter' | 'flavor' | 'phrase' | 'kept'
    """
    if not isinstance(value, str) or value == "":
        return value, "kept"

    # 1. Pure IDs / commands -> keep
    if is_proper_noun_or_id(value):
        return value, "kept"

    # 2. Hunter pattern
    h = translate_hunter(value)
    if h is not None:
        return h, "hunter"

    # 3. Split color codes for matching
    prefix, core, suffix = split_color_codes(value)

    # 4. Inner color codes (e.g., "&3The Opening Ritual" already handled by split)
    # Also handle middle codes? Most entries are simple prefix/suffix wrapped.

    # 5. Exact match on the core
    stripped = core.strip()
    if stripped in EXACT:
        return prefix + EXACT[stripped] + suffix, "exact"

    # Some entries have format like "—— &b&lMain Quest &f——" — handle "&f—— X &f——" wrappers
    sep_match = re.match(r"^(&f—— )(.+?)( &f——)$", value)
    if sep_match:
        middle = sep_match.group(2)
        # Translate middle
        translated_middle, conf = translate_one(middle)
        if conf != "kept":
            return sep_match.group(1) + translated_middle + sep_match.group(3), conf

    # 6. Flavor subtitle matching (handles inner color-wrapped flavor)
    if stripped in SUBTITLE_FLAVOR:
        return prefix + SUBTITLE_FLAVOR[stripped] + suffix, "flavor"
    if stripped in SUBTITLE_FLAVOR_EXT:
        return prefix + SUBTITLE_FLAVOR_EXT[stripped] + suffix, "flavor"
    if stripped in SUBTITLE_FLAVOR_EXT2:
        return prefix + SUBTITLE_FLAVOR_EXT2[stripped] + suffix, "flavor"
    if stripped in SUBTITLE_FLAVOR_EXT3:
        return prefix + SUBTITLE_FLAVOR_EXT3[stripped] + suffix, "flavor"

    # 7. "Ars Delight..." style with embedded text
    if "Ars Delight" in stripped and "Cooking Magique" in stripped:
        return prefix + "Ars Delight: Cocina Mágica" + suffix, "flavor"

    # 8. Phrase-level replacements (heuristic, may translate partially)
    new_core = color_safe_phrase_replace(core)
    if new_core != core:
        return prefix + new_core + suffix, "phrase"

    # 9. Fall back: keep original English (better than wrong Spanish)
    return value, "kept"


def main() -> None:
    with INPUT_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    output: dict[str, str] = {}
    stats = {"exact": 0, "hunter": 0, "flavor": 0, "phrase": 0, "kept": 0}
    low_confidence_samples: list[tuple[str, str]] = []

    for key, value in data.items():
        translated, conf = translate_one(value)
        output[key] = translated
        stats[conf] += 1
        if conf == "kept" and len(low_confidence_samples) < 30 and not is_proper_noun_or_id(value):
            low_confidence_samples.append((key, value))

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    total = sum(stats.values())
    translated_count = total - stats["kept"]
    pct = (translated_count / total * 100.0) if total else 0
    print(f"Input entries:  {len(data)}")
    print(f"Output entries: {len(output)}")
    print(f"Translated:     {translated_count} ({pct:.1f}%)")
    print(f"  exact:        {stats['exact']}")
    print(f"  hunter:       {stats['hunter']}")
    print(f"  flavor:       {stats['flavor']}")
    print(f"  phrase:       {stats['phrase']}")
    print(f"Kept (EN):      {stats['kept']} ({100 - pct:.1f}%)")
    print(f"\nLow-confidence (kept) samples:")
    for k, v in low_confidence_samples[:15]:
        print(f"  {k} = {v!r}")

    # Key parity check
    missing = set(data) - set(output)
    extra = set(output) - set(data)
    print(f"\nKey parity: missing={len(missing)}, extra={len(extra)}")


if __name__ == "__main__":
    main()
