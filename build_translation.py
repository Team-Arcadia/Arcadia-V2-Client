#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Spanish translation for FTB Quests
This version creates a complete Spanish translation dictionary
"""

import re
import os

SOURCE_FILE = r"c:\Users\Jimmy\curseforge\minecraft\Instances\Arcadia V2\config\ftbquests\quests\lang\en_us.snbt"
OUTPUT_FILE = r"c:\Users\Jimmy\curseforge\minecraft\Instances\Arcadia V2\config\ftbquests\quests\lang\es_es.snbt"

# Comprehensive Spanish translation dictionary
# Built from analysis of the English quest file
TRANSLATION_MAP = {
    # ===== CHAPTERS (Chapter Titles) =====
    "New Age": "Nueva Era",
    "The Ars Universe": "El Universo Ars",
    "Ars Nouveau: The Arcana": "Ars Nouveau: El Arcana",
    "Enchantment Industry": "Industria del Encantamiento",
    "Pump Dat Oil": "Bombea ese Petroleo",
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

    # ===== CHAPTER GROUPS =====
    "Beginning": "Inicio",
    "End of the game": "Fin del Juego",
    "Advanced": "Avanzado",
    "Nearly impossible": "Casi Imposible",
    "Expert": "Experto",
    "Absolute perfection": "Perfeccion Absoluta",
    "Learning": "Aprendizaje",
    "Progression": "Progresion",

    # ===== QUEST TITLES & SUBTITLES =====
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
    "Moa Master": "Maestro Moa",
    "The Transmission Shaft": "El Eje de Transmision",
    "Gears": "Engranajes",
    "Farmer Utilities": "Utilidades del Granjero",
}

def translate_file(source_path, output_path):
    """Translate the SNBT file using the translation map"""
    print("Reading source file: {}".format(source_path))

    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    print("Total lines: {}".format(len(lines)))

    # Process each line
    output_lines = []
    translations_applied = 0

    for line in lines:
        output_line = line

        # For each translation pair, find and replace in the line
        for english, spanish in TRANSLATION_MAP.items():
            # Create a pattern to find the English text in quotes
            pattern = '"{}"'.format(re.escape(english))
            replacement = '"{}"'.format(spanish)

            # Count how many replacements we make
            new_line = output_line.replace(pattern, replacement)
            if new_line != output_line:
                translations_applied += 1
                output_line = new_line

        output_lines.append(output_line)

    # Write output
    print("Writing output file...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    # Verify
    output_line_count = len(output_lines)
    source_line_count = len(lines)

    print("=== TRANSLATION COMPLETE ===")
    print("Source lines: {}".format(source_line_count))
    print("Output lines: {}".format(output_line_count))
    print("Lines match: {}".format(source_line_count == output_line_count))
    print("Translations applied: {}".format(translations_applied))
    print("Output file: {}".format(output_path))

if __name__ == "__main__":
    try:
        translate_file(SOURCE_FILE, OUTPUT_FILE)
    except Exception as e:
        print("ERROR: {}".format(e))
        import traceback
        traceback.print_exc()
        exit(1)
