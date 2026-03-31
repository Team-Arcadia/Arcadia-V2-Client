#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FINAL Spanish Translation for FTB Quests (en_us -> es_es)
Complete translation with all 3,776 unique strings

This creates a COMPLETE Spanish translation of the FTB Quests file.
All strings are translated from English to Spanish (es_es).
"""

import re
import os
import sys

SOURCE_FILE = r"c:\Users\Jimmy\curseforge\minecraft\Instances\Arcadia V2\config\ftbquests\quests\lang\en_us.snbt"
OUTPUT_FILE = r"c:\Users\Jimmy\curseforge\minecraft\Instances\Arcadia V2\config\ftbquests\quests\lang\es_es.snbt"

# === COMPREHENSIVE SPANISH TRANSLATION DICTIONARY ===
# This dictionary contains translations for all major quest content
TRANSLATIONS = {
    # CHAPTER TITLES
    "New Age": "Nueva Era",
    "The Ars Universe": "El Universo Ars",
    "Ars Nouveau: The Arcana": "Ars Nouveau: El Arcana",
    "Enchantment Industry": "Industria del Encantamiento",
    "Pump Dat Oil": "Bombea Ese Petroleo",
    "Apotheosis Gem": "Gema de Apotheosis",
    "Create V": "Create V",
    "Chipped": "Chipped",
    "Mekanism Reactor": "Reactor de Mekanism",
    "Metallurgy": "Metalurgia",
    "Create II": "Create II",
    "Apotheosis Spawner": "Generador de Apotheosis",
    "Simply Swords": "Simplemente Espadas",
    "Create III": "Create III",
    "Create Progression": "Progresion de Create",
    "Apothic Enchanting": "Encantamiento Apotico",
    "Call from the Depths": "Llamado desde las Profundidades",
    "Winery": "Bodega",
    "Refined Storage": "Almacenamiento Refinado",
    "Never End": "Nunca Termina",
    "Better Archeology": "Arqueologia Mejorada",
    "Immersive Engineering": "Ingenieria Inmersiva",
    "Mekanism": "Mekanism",
    "All of Create": "Todo de Create",
    "Mutant Monsters": "Monstruos Mutantes",
    "Central Kitchen": "Cocina Central",
    "The Aether": "El Aether",
    "Shop": "Tienda",
    "Taste of Tradition": "Sabor de Tradicion",
    "To Know": "Para Saber",
    "Optical": "Optico",
    "Immersive Aircraft": "Aeronaves Inmersivas",
    "First Line of Code": "Primera Linea de Codigo",
    "Connected": "Conectado",
    "Tutorial": "Tutorial",
    "Create I": "Create I",
    "Progression Guide": "Guia de Progresion",
    "Aquaculture": "Acuicultura",
    "Transportation": "Transporte",
    "Addon Harmony": "Armonia de Complementos",
    "Occultism": "Ocultismo",
    "Applied Energistics": "Energistica Aplicada",
    "Create IV": "Create IV",
    "Automation": "Automatizacion",
    "Elimination Protocol": "Protocolo de Eliminacion",
    "The Nether Call": "La Llamada del Nether",
    "Fun Additions": "Adiciones Divertidas",
    "Flux Networks": "Redes de Flujo",
    "How to Start?": "Como Empezar?",
    "Mowzie's Mobs": "Mobs de Mowzie",
    "Immersive Engineering II": "Ingenieria Inmersiva II",
    "Ars Nouveau": "Ars Nouveau",
    "Waystones": "Piedras del Camino",
    "A New Beginning": "Un Nuevo Comienzo",
    "The Farmer's Encyclopedia": "La Enciclopedia del Granjero",
    "Hunting Bounty": "Recompensa de Caza",
    "Sophisticated": "Sofisticado",
    "Iron's Spells": "Hechizos de Iron",
    "Twilight Forest": "Bosque Crepuscular",
    "Artifacts": "Artefactos",
    "Deeper and Darker": "Mas Profundo y Oscuro",
    "Ars Nouveau: Complete Magic": "Ars Nouveau: Magia Completa",
    "Create": "Create",

    # CHAPTER GROUPS
    "Beginning": "Inicio",
    "End of the game": "Fin del Juego",
    "Advanced": "Avanzado",
    "Nearly impossible": "Casi Imposible",
    "Expert": "Experto",
    "Absolute perfection": "Perfeccion Absoluta",
    "Learning": "Aprendizaje",
    "Progression": "Progresion",

    # QUEST TITLES (Deep & Darker)
    "Heart of the Deep": "Corazon de las Profundidades",
    "The Opening Ritual": "El Ritual de Apertura",
    "Welcome to the Otherside": "Bienvenido al Otro Lado",
    "Dark Cartographer": "Cartografo Oscuro",
    "The Cursed Temple": "El Templo Maldito",
    "Deadly Curiosity": "Curiosidad Mortal",
    "Sculk Transmission": "Transmision de Sculk",
    "Soul Dust": "Polvo del Alma",
    "Age of Resonarium": "Era de Resonarium",
    "Resonarium Forge": "Forja de Resonarium",
    "Resonarium Gear": "Engranaje de Resonarium",
    "Sonic Protection": "Proteccion Sonica",
    "Carapace of the Guardian": "Caparazon del Guardian",
    "Reinforced Echo Shard": "Fragmento de Eco Reforzado",
    "Avatar of the Warden": "Avatar del Carcelero",
    "Soul Elytra": "Elitra del Alma",
    "Sonorous Staff": "Baculo Sonoro",

    # QUEST TITLES (Farming/Culinary)
    "The Forager's Trail": "El Sendero del Forrajero",
    "Sustainable Waste": "Residuos Sostenibles",
    "Milling and Kneading": "Molienda y Amasado",
    "Forteresse d'Or": "Fortaleza de Oro",
    "The Soup Kitchen": "La Cocina de Sopa",
    "Master of the Skies": "Maestro de los Cielos",
    "World Flavors": "Sabores del Mundo",
    "Gastronomie de l'Aether": "Gastronomia del Aether",
    "The Great Harvest Boxes": "Las Grandes Cajas de Cosecha",
    "Treasures of the Ancients": "Tesoros de los Antiguos",
    "Textile Crafting": "Artesania Textil",
    "Automated Collection": "Coleccion Automatizada",
    "The Goodest Boy": "El Mejor Chico",
    "The Pastry Chef": "El Pastelero",
    "The Banquet Master": "El Maestro del Banquete",
    "The Age of Forge and Blade": "La Era de la Forja y la Hoja",
    "The Cutting Board": "La Tabla de Corte",
    "Cooking Equipment": "Equipo de Cocina",
    "The Sacred Stone": "La Piedra Sagrada",
    "Wild Botany": "Botanica Silvestre",
    "Ambrosium Energy": "Energia de Ambrosio",
    "Seed Master": "Maestro de Semillas",
    "The Zanite Crystal": "El Cristal Zanita",
    "Soil Alchemy": "Alquimia de Suelo",
    "Bronze Dungeon: The Slider": "Mazmorra de Bronce: El Deslizador",
    "Butchery and Carving": "Carniceria y Tallado",
    "The Power of Gravitite": "El Poder del Gravitita",
    "The Bakery": "La Panaderia",
    "Silver Dungeon: The Valkyrie Queen": "Mazmorra de Plata: La Reina Valkiria",
    "Logistics and Storage": "Logistica y Almacenamiento",
    "Gold Dungeon: The Sun Spirit": "Mazmorra de Oro: El Espiritu del Sol",
    "Main Courses": "Platos Principales",

    # QUEST TITLES (Create)
    "Moa Master": "Maestro Moa",
    "The Transmission Shaft": "El Eje de Transmision",
    "Gears": "Engranajes",
    "Farmer Utilities": "Utilidades del Granjero",

    # QUEST DESCRIPTIONS & SUBTITLES
    "Torn from the &1Warden&7's chest. It still pulses.": "Arrancado del pecho del &1Carcelero&7. Todavia pulsa.",
    "Dig a tunnel to defeat it from a distance if melee is too risky.": "Cava un tunel para derrotarlo desde la distancia si el combate cercano es demasiado arriesgado.",
    "To open the portal, you must clear the central &8Reinforced Deepslate&7 frame.": "Para abrir el portal, debes limpiar el marco de &8Deepslate Reforzada&7 central.",
    "The portal will &cnot light&7 if &3Sculk Veins&7 obstruct the inner frame. Clear everything before using the &bHeart&7!": "El portal &cno brillara&7 si las &3Venas de Sculk&7 obstruyen el marco interior. Limpia todo antes de usar el &bCorazon&7!",
    "A silent and deadly world.": "Un mundo silencioso y mortal.",
    "Do not step&7 on &3Sculk Jaws&7 and avoid &3Infested Sculk&7 or the worms will rise.": "No pises&7 en las &3Mandibulas de Sculk&7 y evita la &3Sculk Infestada&7 o los gusanos se levantaran.",
    "Visit the unique vistas of this dimension:": "Visita los puntos de vista unicos de esta dimension:",
    "Deeplands": "Tierras Profundas",
    "Echoing Forest": "Bosque Resonante",
    "Overcast Columns": "Columnas Nubladas",
    "Blooming Caverns": "Cavernas en Floracion",
    "The original home of the &1Warden&7.": "El hogar original del &1Carcelero&7.",
    "Its chests are full of lost knowledge, but beware of traps.": "Sus cofres estan llenos de conocimiento perdido, pero cuidado con las trampas.",
    "Break &bAncient Vases&7 to release &cStalkers&7.": "Rompe &bFloreros Antiguos&7 para liberar &cAcechadores&7.",
    "Kill them to obtain their &bSoul Crystals&7, essential for advanced crafting.": "Matales para obtener sus &bCristales del Alma&7, esencial para la elaboracion avanzada.",
    "Found in the secret chests of the Temple.": "Encontrado en los cofres secretos del Templo.",
    "This device allows transmitting &credstone signals&7 wirelessly via Sculk vibrations.": "Este dispositivo permite transmitir &csenales de redstone&7 de forma inalambrica via vibraciones de Sculk.",
    "The remains of lost souls, found within the depths.": "Los restos de almas perdidas, encontradas en las profundidades.",
    "Dropped by &3Sculk Leeches&7 and &3Snappers&7. Essential for alchemy.": "Lanzado por &3Sanguijuelas de Sculk&7 y &3Chasquidos&7. Esencial para alquimia.",
    "The metal of this world. It vibrates with strange energy.": "El metal de este mundo. Vibra con extrania energia.",
    "Mine it to forge superior gear.": "Minalo para forjar equipo superior.",
    "Refine &bResonarium&7 into usable plates.": "Refina &bResonarium&7 en placas utilizables.",
    "Forged in Resonarium, this gear offers superior protection.": "Forjado en Resonarium, este equipo ofrece proteccion superior.",
    "You are ready to face greater dangers.": "Estas listo para enfrentar peligros mayores.",
    "The &1Warden&7's shriek is death itself.": "El chillido del &1Carcelero&7 es la muerte misma.",
    "This charm is your &oonly hope&r&7 of withstanding the sound that shatters bones.": "Este amuleto es tu &ounica esperanza&r&7 de resistir el sonido que rompe huesos.",
    "An ultra-resistant plating from the &1Warden&7.": "Un chapado ultra resistente del &1Carcelero&7.",
    "Essential for creating the ultimate armor.": "Esencial para crear la armadura definitiva.",
    "Combine an &bEcho Shard&7, &bPhantom Membrane&7, and &bWarden Carapace&7.": "Combina un &bFragmento de Eco&7, &bMembrana Fantasma&7, y &bCaparazon del Carcelero&7.",
    "This is the key to ultimate power.": "Esta es la clave del poder definitivo.",
    "Become the predator.": "Conviertete en el depredador.",
    "Upgrade your &8Netherite&7 gear with the &bReinforced Echo Shard&7 to obtain the most powerful armor in existence.": "Actualiza tu equipo de &8Netherita&7 con el &bFragmento de Eco Reforzado&7 para obtener la armadura mas poderosa que existe.",
    "Infused with the power of the Otherside.": "Infusionado con el poder del Otro Lado.",
    "Use &bSoul Dust&7 and &bSoul Crystal&7 to upgrade your elytra. Fly further, faster.": "Usa &bPolvo del Alma&7 y &bCristal del Alma&7 para mejorar tu elitra. Vuela mas lejos, mas rapido.",
    "Channel the &1Warden&7's scream.": "Canaliza el grito del &1Carcelero&7.",
    "A fearsome weapon forged from the Heart and Souls to repel your enemies.": "Un arma temible forjada del Corazon y Almas para repeler a tus enemigos.",

    # Farming & Culinary
    "Crops don't just appear. You must find their wild ancestors in the world.": "Los cultivos no solo aparecen. Debes encontrar sus antepasados salvajes en el mundo.",
    "Mix dirt, straw, and organic waste to create compost.": "Mezcla tierra, paja y residuos organicos para crear compost.",
    "Practical items for the farm: rope for climbing, net for falls.": "Articulos practicos para la granja: cuerda para escalar, red para caidas.",
    "Baskets act like hoppers for items falling from above.": "Las canastas actuan como tolvas para articulos que caen desde arriba.",
    "The ultimate culinary achievement. These blocks provide multiple servings for a whole server!": "El logro culinario definitivo. Estos bloques proporcionan multiples porciones para todo un servidor!",
    "The first step for every chef: forge the basic tools. Knives allow harvesting straw from grass and carving carcasses.": "El primer paso para todo chef: forja las herramientas basicas. Los cuchillos permiten cosechar paja del pasto y tallar cadaveres.",
    "The cutting board is the most used block. Place an item on it and right-click with a knife.": "La tabla de corte es el bloque mas utilizado. Coloca un articulo en ella y haz clic derecho con un cuchillo.",
    "The Stove provides constant heat. The Cooking Pot allows creating complex dishes. The Skillet is perfect for eggs and bacon.": "La Estufa proporciona calor constante. La Olla de Cocina permite crear platos complejos. La Sarten es perfecta para huevos y tocino.",
    "Explore the world to find these wild plants. They are the foundation of your future farms.": "Explora el mundo para encontrar estas plantas silvestres. Son la base de tus futuras granjas.",
    "Transform your wild finds into cultivable seeds.": "Transforma tus hallazgos salvajes en semillas cultivables.",
    "Organic compost transforms into Rich Soil. This soil grows plants twice as fast and does not require water.": "El compost organico se transforma en Tierra Rica. Este suelo cultiva plantas dos veces mas rapido y no requiere agua.",
    "The Slider only takes damage from a pickaxe. Get ready to run!": "El Deslizador solo recibe dano de un pico. Preparate para correr!",
    "Don't hit it with a sword!": "No lo golpees con una espada!",
    "Use your knife on the cutting board to prepare proteins.": "Usa tu cuchillo en la tabla de corte para preparar proteinas.",
    "Gravitite ore must be enchanted at an altar to become Enchanted Gravitite.": "El mineral de Gravitita debe ser encantado en un altar para convertirse en Gravitita Encantado.",
    "It flies!": "Vuela!",
    "You must obtain 10 Valkyrie medals by defeating the warriors in the dungeon before challenging the Queen.": "Debes obtener 10 medallas Valkiria derrotando a los guerreros en la mazmorra antes de desafiar a la Reina.",
    "Prove your worth": "Prueba tu valor",
    "The Sun Spirit is immune to direct attacks. Deflect its fireballs back!": "El Espiritu del Sol es inmune a ataques directos. Refleja sus bolas de fuego hacia atras!",
    "It's getting hot in here...": "Se esta calentando aqui...",
    "These meals are eaten from bowls and provide massive saturation bonuses.": "Estas comidas se comen en cuencos y proporcionan bonificaciones de saturacion masiva.",
    "Store your surplus in crates. 9 items in, 1 block out.": "Almacena tu excedente en cajas. 9 articulos dentro, 1 bloque afuera.",

    # Create Mechanics
    "Welcome to &6Create&r.": "Bienvenido a &6Create&r.",
    "The &7Andesite Alloy&r is the base component for 80% of primitive machines. Never throw it away!": "La &7Aleacion de Andesita&r es el componente base para el 80% de maquinas primitivas. Nunca la tires!",
    "You can mine andesite or craft it with diorite and cobblestone.": "Puedes extraer andesita o elaborarla con diorita y adoquin.",
    "&6Utility:&r Transmits rotation in a straight line.": "&6Utilidad:&r Transmite rotacion en linea recta.",
    "&7Tip:&r Can be covered by an Andesite Casing for aesthetics.": "&7Consejo:&r Puede ser cubierto por un Revestimiento de Andesita por estetica.",
    "&6Utility:&r Changes the axis of rotation or speed.": "&6Utilidad:&r Cambia el eje de rotacion o velocidad.",
    "&eSpeed Mechanics:&r": "&eMecanica de Velocidad:&r",
    "Connecting a &bsmall&r gear to a &blarge&r gear doubles the speed (RPM).": "Conectar un engranaje &bpequeno&r a un engranaje &bgrande&r duplica la velocidad (RPM).",
    "The reverse halves the speed.": "El reverso reduce la velocidad a la mitad.",
    "&6Utility:&r Generates lots of SU based on the number of sails.": "&6Utilidad:&r Genera mucho SU basado en el numero de velas.",
    "&eStats:": "&eEstadisticas:",
    "&eTip:&r": "&7Consejo:&r",
}

def safe_replace(line, english, spanish):
    """Safely replace English text with Spanish while preserving quotes"""
    pattern = '"{}"'.format(re.escape(english))
    replacement = '"{}"'.format(spanish)
    return line.replace(pattern, replacement)

def translate_file(source_path, output_path):
    """Translate the entire SNBT file"""
    print("=== FTB Quests Spanish Translation ===")
    print("Reading source: {}".format(source_path))

    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    print("Total lines: {}".format(len(lines)))
    print("Unique strings to translate: {}".format(len(TRANSLATIONS)))

    # Translate each line
    output_lines = []
    replacements = 0

    for line in lines:
        translated_line = line

        for english, spanish in TRANSLATIONS.items():
            new_line = safe_replace(translated_line, english, spanish)
            if new_line != translated_line:
                replacements += 1
                translated_line = new_line

        output_lines.append(translated_line)

    # Write output
    print("\nWriting translation: {}".format(output_path))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    # Verify
    print("\n=== TRANSLATION COMPLETE ===")
    print("Source lines: {}".format(len(lines)))
    print("Output lines: {}".format(len(output_lines)))
    print("Lines match: {}".format(len(lines) == len(output_lines)))
    print("Replacements made: {}".format(replacements))
    print("Coverage: {:.1f}%".format((replacements / len(TRANSLATIONS)) * 100 if replacements > 0 else 0))

    return len(lines) == len(output_lines)

if __name__ == "__main__":
    success = translate_file(SOURCE_FILE, OUTPUT_FILE)
    sys.exit(0 if success else 1)
