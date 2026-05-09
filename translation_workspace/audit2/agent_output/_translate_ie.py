"""Translate Immersive Engineering missing keys EN -> FR."""
import json
import os
import re

INPUT = r'c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/audit2/missing_per_mod/immersiveengineering.json'
OUTPUT = r'c:/Users/Jimmy/curseforge/minecraft/Instances/Arcadia V2/translation_workspace/audit2/agent_output/immersiveengineering.json'

with open(INPUT, 'r', encoding='utf-8') as f:
    src = json.load(f)

# Color mapping (with gender-flexible adjective forms)
# We'll use the masculine form by default; specific patterns may swap.
COLOR_MASC = {
    'black': 'noir', 'blue': 'bleu', 'brown': 'marron', 'cyan': 'cyan',
    'gray': 'gris', 'green': 'vert', 'light_blue': 'bleu clair',
    'light_gray': 'gris clair', 'lime': 'vert clair', 'magenta': 'magenta',
    'orange': 'orange', 'pink': 'rose', 'purple': 'violet', 'red': 'rouge',
    'white': 'blanc', 'yellow': 'jaune',
}
COLOR_FEM = {
    'black': 'noire', 'blue': 'bleue', 'brown': 'marron', 'cyan': 'cyan',
    'gray': 'grise', 'green': 'verte', 'light_blue': 'bleu clair',
    'light_gray': 'gris clair', 'lime': 'vert clair', 'magenta': 'magenta',
    'orange': 'orange', 'pink': 'rose', 'purple': 'violette', 'red': 'rouge',
    'white': 'blanche', 'yellow': 'jaune',
}

# Banner pattern label translations (base name and grammatical gender)
# pattern_id -> (singular_label, gender 'm'/'f', plural? bool)
BANNER_PATTERNS = {
    'bevels': ('Biseaux', 'm', True),                    # Biseaux
    'hammer': ('Marteau', 'm', False),
    'hammer_grip': ('Manche de marteau', 'm', False),
    'hammer_head': ('Tête de marteau', 'f', False),
    'ornate': ('Ornement', 'm', False),
    'screwdriver': ('Tournevis', 'm', False),
    'screwdriver_grip': ('Manche de tournevis', 'm', False),
    'screwdriver_head': ('Tête de tournevis', 'f', False),
    'treated_wood': ('Bois traité', 'm', False),
    'warning': ('Panneau d\'avertissement', 'm', False),
    'warning_cat': ('Panneau chat', 'm', False),
    'warning_cold': ('Panneau froid', 'm', False),
    'warning_ear_defenders': ('Panneau protections auditives', 'm', False),
    'warning_electric': ('Panneau électrique', 'm', False),
    'warning_falling': ('Panneau chute', 'm', False),
    'warning_fire': ('Panneau feu', 'm', False),
    'warning_hot': ('Panneau chaud', 'm', False),
    'warning_magnet': ('Panneau aimant', 'm', False),
    'warning_sound': ('Panneau sonore', 'm', False),
    'warning_turret': ('Panneau tourelle', 'm', False),
    'warning_warden': ('Panneau warden', 'm', False),
    'windmill': ('Éolienne', 'f', False),
    'wirecutter': ('Coupe-fil', 'm', False),
    'wirecutter_grip': ('Manche de coupe-fil', 'm', False),
    'wirecutter_head': ('Tête de coupe-fil', 'f', False),
    'wolf': ('Loup', 'm', False),
    'wolf_l': ('Loup gauche', 'm', False),
    'wolf_r': ('Loup droit', 'm', False),
}


def translate_banner(key: str, en: str) -> str | None:
    # Format: block.minecraft.banner.immersiveengineering.<pattern>.<color>
    m = re.match(r'^block\.minecraft\.banner\.immersiveengineering\.([a-z_]+)\.([a-z_]+)$', key)
    if not m:
        return None
    pattern, color = m.group(1), m.group(2)
    label_data = BANNER_PATTERNS.get(pattern)
    if not label_data:
        # fallback
        label = pattern.replace('_', ' ').capitalize()
        gender = 'm'
        plural = False
    else:
        label, gender, plural = label_data
    if gender == 'f':
        col = COLOR_FEM.get(color, color)
    else:
        col = COLOR_MASC.get(color, color)
    if plural:
        # plural color forms
        col_plural_map = {
            'noir': 'noirs', 'bleu': 'bleus', 'marron': 'marron',
            'cyan': 'cyan', 'gris': 'gris', 'vert': 'verts',
            'bleu clair': 'bleu clair', 'gris clair': 'gris clair',
            'vert clair': 'vert clair', 'magenta': 'magenta',
            'orange': 'orange', 'rose': 'roses', 'violet': 'violets',
            'rouge': 'rouges', 'blanc': 'blancs', 'jaune': 'jaunes',
        }
        col = col_plural_map.get(col, col)
    # Motif de bannière X <color> -> per instructions: "Motif de bannière X" with color agreement
    # But these are banner block names not pattern items; keep style compact
    return f"Bannière {label} {col}"


# Hardcoded translations
HARDCODED = {
    # block.immersiveengineering
    'block.immersiveengineering.acetaldehyde_fluid_block': 'Acétaldéhyde',
    'block.immersiveengineering.aluminum_wall_hanging_sign': 'Pancarte suspendue en aluminium',
    'block.immersiveengineering.aluminum_wall_sign': 'Pancarte en aluminium',
    'block.immersiveengineering.biodiesel_fluid_block': 'Biodiesel',
    'block.immersiveengineering.chunk_loader': 'Observateur de Resonanz',
    'block.immersiveengineering.concrete_fluid_block': 'Béton liquide',
    'block.immersiveengineering.creosote_fluid_block': 'Huile de créosote',
    'block.immersiveengineering.ethanol_fluid_block': 'Éthanol',
    'block.immersiveengineering.herbicide_fluid_block': 'Herbicide',
    'block.immersiveengineering.high_power_biodiesel_fluid_block': 'Biodiesel haute cétane',
    'block.immersiveengineering.machine_interface': 'Interface de machine',
    'block.immersiveengineering.phenolic_resin_fluid_block': 'Résine phénolique',
    'block.immersiveengineering.plantoil_fluid_block': 'Huile végétale',
    'block.immersiveengineering.radio_tower': 'Tour radio',
    'block.immersiveengineering.redstone_acid_fluid_block': 'Acide de redstone',
    'block.immersiveengineering.shelf': 'Étagère pour caisses',
    'block.immersiveengineering.steel_wall_hanging_sign': 'Pancarte suspendue en acier',
    'block.immersiveengineering.steel_wall_sign': 'Pancarte en acier',
    'block.immersiveengineering.treated_wood_wall_hanging_sign': 'Pancarte suspendue en bois traité',
    'block.immersiveengineering.treated_wood_wall_sign': 'Pancarte en bois traité',

    # advancement
    'advancement.immersiveengineering.buy_oremap': 'X marque l\'emplacement',
    'advancement.immersiveengineering.buy_oremap.desc': 'Achetez une carte de gisement minéral à l\'ingénieur structurel',
    'advancement.immersiveengineering.buy_shaderbag': 'Frénésie de mode',
    'advancement.immersiveengineering.buy_shaderbag.desc': 'Achetez une pochette surprise de shaders au costumier',
    'advancement.immersiveengineering.chorus_cloche': 'Serre extraterrestre',
    'advancement.immersiveengineering.chorus_cloche.desc': 'Faites pousser un fruit du chorus dans la Cloche de jardin',
    'advancement.immersiveengineering.chute_bonk': 'Raccourci inconfortable',
    'advancement.immersiveengineering.chute_bonk.desc': 'Rebondissez dans les goulottes en tôle',
    'advancement.immersiveengineering.craft_batcher': 'Retenu',
    'advancement.immersiveengineering.craft_batcher.desc': 'Fabriquez un Lot d\'objets',
    'advancement.immersiveengineering.craft_drop_conveyor': 'Vers le bas',
    'advancement.immersiveengineering.craft_drop_conveyor.desc': 'Fabriquez un tapis convoyeur de chute',
    'advancement.immersiveengineering.craft_duroplast': 'Matériaux modernes',
    'advancement.immersiveengineering.craft_duroplast.desc': 'Fabriquez une feuille de duroplast',
    'advancement.immersiveengineering.craft_extract_conveyor': 'Déménagement',
    'advancement.immersiveengineering.craft_extract_conveyor.desc': 'Fabriquez un tapis convoyeur d\'extraction',
    'advancement.immersiveengineering.craft_powerpack': 'Particules portatives',
    'advancement.immersiveengineering.craft_powerpack.desc': 'Fabriquez le sac à dos accumulateur',
    'advancement.immersiveengineering.craft_router': 'Codé par couleur !',
    'advancement.immersiveengineering.craft_router.desc': 'Fabriquez un routeur d\'objets',
    'advancement.immersiveengineering.craft_sheetmetal': 'Décoratif et solide',
    'advancement.immersiveengineering.craft_sheetmetal.desc': 'Fabriquez de la tôle',
    'advancement.immersiveengineering.craft_treatedwood': 'Huilé et prêt à l\'emploi',
    'advancement.immersiveengineering.craft_treatedwood.desc': 'Fabriquez du bois traité',
    'advancement.immersiveengineering.creosote': 'Ne buvez pas ça...',
    'advancement.immersiveengineering.creosote.desc': 'Récoltez un seau d\'huile de créosote',
    'advancement.immersiveengineering.kill_illager': 'Armement supérieur',
    'advancement.immersiveengineering.kill_illager.desc': 'Tuez un illageois avec un Revolver, un Railgun ou un Lance-flammes chimique. Méfiez-vous des nouveaux pillards !',
    'advancement.immersiveengineering.liquid_concrete': 'Ce qui arrive aux balances...',
    'advancement.immersiveengineering.liquid_concrete.desc': 'Restez piégé avec les pieds dans le béton',
    'advancement.immersiveengineering.main_root': 'Immersive Engineering',
    'advancement.immersiveengineering.main_root.desc': 'RTFM !',
    'advancement.immersiveengineering.mb_cokeoven': 'Carbone concentré',
    'advancement.immersiveengineering.mb_cokeoven.desc': 'Formez le Four à coke',
    'advancement.immersiveengineering.mb_fermenter': 'Moonshine !',
    'advancement.immersiveengineering.mb_fermenter.desc': 'Formez le Fermenteur',
    'advancement.immersiveengineering.mb_mixer': 'Potions industrielles',
    'advancement.immersiveengineering.mb_mixer.desc': 'Formez le Mélangeur',
    'advancement.immersiveengineering.mb_refinery': 'Traitement chimique',
    'advancement.immersiveengineering.mb_refinery.desc': 'Formez la Raffinerie',
    'advancement.immersiveengineering.mb_squeezer': 'Peut-il faire du lait de noix ?',
    'advancement.immersiveengineering.mb_squeezer.desc': 'Formez le Pressoir',
    'advancement.immersiveengineering.mb_tank': 'Château d\'eau',
    'advancement.immersiveengineering.mb_tank.desc': 'Formez le Réservoir',
    'advancement.immersiveengineering.multiblocks_root': 'Multiblocs',
    'advancement.immersiveengineering.multiblocks_root.desc': 'De grandes machines pour de grandes usines',
    'advancement.immersiveengineering.place_dynamo': 'Moteur inversé',
    'advancement.immersiveengineering.place_dynamo.desc': 'Placez une Dynamo cinétique',
    'advancement.immersiveengineering.secret_achtung': 'ACHTUNG ! ACHTUNG !',
    'advancement.immersiveengineering.secret_achtung.desc': '39486 60170 24326 01064',
    'advancement.immersiveengineering.secret_bttf': '1.21 gigawatts !',
    'advancement.immersiveengineering.secret_bttf.desc': 'Quand cette merveille atteint 88 mph, vous allez voir des choses sérieus-',
    'advancement.immersiveengineering.secret_friedbird': 'Oiseau frit',
    'advancement.immersiveengineering.secret_friedbird.desc': 'Isolation indisponible',
    'advancement.immersiveengineering.secret_snake': 'Alerte !',
    'advancement.immersiveengineering.secret_snake.desc': 'Découvrez un intrus',
    'advancement.immersiveengineering.skyhook_distance': 'Booker, attrape !',
    'advancement.immersiveengineering.skyhook_distance.desc': 'Parcourez un total de 1 km avec le Skyhook',
    'advancement.immersiveengineering.tools_root': 'Outils & Améliorations',
    'advancement.immersiveengineering.tools_root.desc': 'L\'Établi de l\'ingénieur peut être utilisé pour modifier vos outils',
    'advancement.immersiveengineering.upgrade_powerpack': 'Le spécial Spengler & Stantz',
    'advancement.immersiveengineering.upgrade_powerpack.desc': 'Appliquez le maximum d\'améliorations au sac à dos accumulateur',
    'advancement.immersiveengineering.villager': 'Camarades ingénieurs',
    'advancement.immersiveengineering.villager.desc': 'Rencontrez un villageois ingénieur',

    # gui
    'gui.immersiveengineering.config.circuit_table.inputs': 'Entrées :',
    'gui.immersiveengineering.config.circuit_table.operator': 'Opérateur :',
    'gui.immersiveengineering.config.circuit_table.outputs': 'Sorties :',
    'gui.immersiveengineering.config.machine_interface.add': 'Ajouter une condition',
    'gui.immersiveengineering.config.machine_interface.check.arc_furnace.additives': 'Entrée d\'additif',
    'gui.immersiveengineering.config.machine_interface.check.arc_furnace.electrodes': 'Intégrité des électrodes',
    'gui.immersiveengineering.config.machine_interface.check.arc_furnace.slag': 'Sortie de scorie',
    'gui.immersiveengineering.config.machine_interface.check.assembler.tank_0': 'Premier réservoir d\'entrée',
    'gui.immersiveengineering.config.machine_interface.check.assembler.tank_1': 'Deuxième réservoir d\'entrée',
    'gui.immersiveengineering.config.machine_interface.check.assembler.tank_2': 'Troisième réservoir d\'entrée',
    'gui.immersiveengineering.config.machine_interface.check.basic.active': 'Machine active',
    'gui.immersiveengineering.config.machine_interface.check.basic.energy_storage': 'Stockage d\'énergie',
    'gui.immersiveengineering.config.machine_interface.check.basic.fluid_input': 'Entrée de fluide',
    'gui.immersiveengineering.config.machine_interface.check.basic.fluid_output': 'Sortie de fluide',
    'gui.immersiveengineering.config.machine_interface.check.basic.item_input': 'Entrée d\'objet',
    'gui.immersiveengineering.config.machine_interface.check.basic.item_output': 'Sortie d\'objet',
    'gui.immersiveengineering.config.machine_interface.check.mixer.tank': 'Fluide stocké',
    'gui.immersiveengineering.config.machine_interface.check.refinery.tank_left': 'Réservoir d\'entrée gauche',
    'gui.immersiveengineering.config.machine_interface.check.refinery.tank_right': 'Réservoir d\'entrée droit',
    'gui.immersiveengineering.config.machine_interface.check.sawmill.blade': 'Intégrité de la lame',
    'gui.immersiveengineering.config.machine_interface.input_color': 'Entrée du signal de contrôle :',
    'gui.immersiveengineering.config.machine_interface.not_connected': 'L\'interface de machine n\'est pas connectée à une machine valide.\nAssurez-vous que l\'interface est placée contre le port de contrôle redstone d\'un multibloc Immersive Engineering.',
    'gui.immersiveengineering.config.machine_interface.option.comparator': 'Sortie comparateur',
    'gui.immersiveengineering.config.machine_interface.option.empty': 'Vide',
    'gui.immersiveengineering.config.machine_interface.option.full': '100% rempli',
    'gui.immersiveengineering.config.machine_interface.option.half': '50% rempli',
    'gui.immersiveengineering.config.machine_interface.option.no': 'Non',
    'gui.immersiveengineering.config.machine_interface.option.quarter': '25% rempli',
    'gui.immersiveengineering.config.machine_interface.option.three_quarter': '75% rempli',
    'gui.immersiveengineering.config.machine_interface.option.yes': 'Oui',
    'gui.immersiveengineering.config.machine_interface.remove': 'Retirer la condition',
    'gui.immersiveengineering.config.output_threshold': 'Seuil de signal : ',
    'gui.immersiveengineering.config.radio_tower.frequency': 'Fréquence',
    'gui.immersiveengineering.config.radio_tower.khz': '%1$s kHz',
    'gui.immersiveengineering.config.radio_tower.load': 'Maj + clic pour charger',
    'gui.immersiveengineering.config.radio_tower.range': 'Portée',
    'gui.immersiveengineering.config.radio_tower.range_m': '%1$s m',
    'gui.immersiveengineering.config.radio_tower.save': 'Cliquer pour sauvegarder',
    'gui.immersiveengineering.config.radio_tower.saved_frequencies': 'Fréquences sauvegardées :',
    'gui.immersiveengineering.config.redstone_color_control': 'Couleur du signal de contrôle :',
    'gui.immersiveengineering.config.redstone_color_input': 'Couleur du signal d\'entrée :',
    'gui.immersiveengineering.config.redstone_color_output': 'Couleur du signal de sortie :',
    'gui.immersiveengineering.config.redstone_color_reset': 'Réinitialisation de la couleur du signal :',
    'gui.immersiveengineering.config.redstone_color_set': 'Définition de la couleur du signal :',
    'gui.immersiveengineering.config.redstone_require_control_signal': 'Nécessite un signal de contrôle',
    'gui.immersiveengineering.config.shelf.swap': 'Passer de l\'autre côté',
    'gui.immersiveengineering.config.siren.sound.buzzer': 'Sonnerie',
    'gui.immersiveengineering.config.siren.sound.klaxon': 'Klaxon',
    'gui.immersiveengineering.config.siren.sound.siren': 'Sirène',
    'gui.immersiveengineering.toast.eureka': 'EUREKA !!',
    'gui.immersiveengineering.toast.manual_unlocked': 'Entrée du Manuel débloquée !',

    # desc
    'desc.immersiveengineering.flavour.revolver.einhorn': 'Règle de §m6§r 8',
    'desc.immersiveengineering.flavour.toolupgrade_drill_fortune': 'Augmente les drops des minerais',
    'desc.immersiveengineering.flavour.toolupgrade_powerpack_antenna': 'Recharge le sac à dos accumulateur depuis les fils',
    'desc.immersiveengineering.flavour.toolupgrade_powerpack_induction': 'Recharge tout votre inventaire',
    'desc.immersiveengineering.flavour.toolupgrade_powerpack_magnet': 'Attire les objets à proximité',
    'desc.immersiveengineering.flavour.toolupgrade_powerpack_tesla': 'Électrocute vos attaquants',
    'desc.immersiveengineering.flavour.toolupgrade_skyhook_insulation': 'Empêche l\'électrocution lors d\'une utilisation du Skyhook sur des fils sous tension',
    'desc.immersiveengineering.flavour.toolupgrade_skyhook_mace': 'Inflige des dégâts grandement augmentés en tombant sur un ennemi',
    'desc.immersiveengineering.flavour.toolupgrade_skyhook_slope': 'Déplacez-vous plus rapidement dans les pentes avec le Skyhook',
    'desc.immersiveengineering.info.batched': 'Jusqu\'à %1$s à la fois',
    'desc.immersiveengineering.info.blueprint.automatons': 'Automates',
    'desc.immersiveengineering.info.blueprint.warning_sign': 'Panneaux d\'avertissement',
    'desc.immersiveengineering.info.circuit_table.btn.input_num': 'Entrée %1$s',
    'desc.immersiveengineering.info.circuit_table.btn.output': 'Sortie',
    'desc.immersiveengineering.info.circuit_table.field.name': 'Nom du circuit',
    'desc.immersiveengineering.info.circuit_table.slot.edit': 'Placez un circuit logique ici pour le modifier',
    'desc.immersiveengineering.info.filter.components': 'Filtre : Composants<br>Filtre les objets en fonction<br>de leurs composants de données additionnels.',
    'desc.immersiveengineering.info.filter.fluid_components': 'Filtre : Composants<br>Filtre les fluides en fonction<br>de leurs composants de données additionnels.',
    'desc.immersiveengineering.info.filter.tag.from_mod': 'Objet ajouté par : %1$s',
    'desc.immersiveengineering.info.filter.tag.none_available': '§o§8Aucun tag disponible, le filtrage se fera par objet à la place.§r',
    'desc.immersiveengineering.info.filter.tag.selected_scroll': '§6Tag sélectionné : §o§8(scroll pour changer)§r',
    'desc.immersiveengineering.info.mineral.alluvial_sift': 'Tamis alluvial',
    'desc.immersiveengineering.info.mineral.amethyst_crevasse': 'Crevasse d\'améthyste',
    'desc.immersiveengineering.info.mineral.ancient_seabed': 'Fond marin ancien',
    'desc.immersiveengineering.info.mineral.banded_iron': 'Fer rubané',
    'desc.immersiveengineering.info.mineral.cooled_lava_tube': 'Tube de lave refroidi',
    'desc.immersiveengineering.info.mineral.hardened_clay_pan': 'Croûte d\'argile durcie',
    'desc.immersiveengineering.info.mineral.lazulitic_intrusion': 'Intrusion lazulitique',
    'desc.immersiveengineering.info.mineral.nether_silt': 'Limon des âmes',
    'desc.immersiveengineering.info.mineral.rich_auricupride': 'Auricupride riche',
    'desc.immersiveengineering.info.noChargeOnArmor': 'Ne peut pas être rechargé lorsqu\'il est attaché à une armure',
    'desc.immersiveengineering.info.operator.imply': 'IMPLIQUE',
    'desc.immersiveengineering.info.operator.nimply': 'N\'IMPLIQUE PAS',
    'desc.immersiveengineering.info.redstone_level': 'Niveau de redstone : %1$s',
    'desc.immersiveengineering.info.redstone_level_on_channel': '%1$s sur %2$s',
    'desc.immersiveengineering.info.refinery.slot.catalyst': 'Catalyseur',
    'desc.immersiveengineering.info.shader.details.acepride': 'Faites des câlins à la place !',
    'desc.immersiveengineering.info.shader.details.bipride': 'Ce n\'est pas une phase.',
    'desc.immersiveengineering.info.shader.details.enbypride': 'Le genre n\'est pas binaire !',
    'desc.immersiveengineering.info.shader.details.gaypride': 'Même les pingouins le font !',
    'desc.immersiveengineering.info.shader.details.lesbianpride': 'Les archéologues les appelleront colocataires.',
    'desc.immersiveengineering.info.shader.details.transpride': 'Protégez les enfants trans ! Les droits trans sont des droits humains, maintenant et pour toujours !',
    'desc.immersiveengineering.jei.category.buckets': ' - Remplissage de seaux',
    'desc.immersiveengineering.jei.category.fertilizer': 'Fertilisant pour Cloche de jardin',
    'desc.immersiveengineering.jei.category.potions': ' - Potions',
    'desc.immersiveengineering.jei.category.recycling': ' - Recyclage',
    'desc.immersiveengineering.jei.cloche_modifier': 'Modificateur de croissance : %1$s',

    # subtitle
    'subtitle.immersiveengineering.alert': 'Alerte !',
    'subtitle.immersiveengineering.arc_furnace': 'Le four à arc provoque des éclairs',
    'subtitle.immersiveengineering.assembler': 'Mécanisme de l\'assembleur rythmique',
    'subtitle.immersiveengineering.bottling': 'L\'embouteilleuse remplit un récipient',
    'subtitle.immersiveengineering.buzzer': 'Avertissement de la sonnerie',
    'subtitle.immersiveengineering.buzzsaw_attack': 'La scie circulaire monte en régime',
    'subtitle.immersiveengineering.buzzsaw_harvest_grinding': 'Broyage',
    'subtitle.immersiveengineering.buzzsaw_harvest_sawing': 'Sciage',
    'subtitle.immersiveengineering.buzzsaw_motor': 'Moteur de la scie circulaire en marche',
    'subtitle.immersiveengineering.drill_attack': 'La foreuse monte en régime',
    'subtitle.immersiveengineering.drill_harvest': 'Forage',
    'subtitle.immersiveengineering.drill_motor': 'Moteur de la foreuse en marche',
    'subtitle.immersiveengineering.electromagnet': 'L\'électroaimant bourdonne',
    'subtitle.immersiveengineering.fermenter': 'Le fermenteur vrombit',
    'subtitle.immersiveengineering.glider': 'Le planeur subit des dégâts',
    'subtitle.immersiveengineering.klaxon': 'Klaxon retentissant',
    'subtitle.immersiveengineering.mill_creaking': 'La roue du moulin grince',
    'subtitle.immersiveengineering.mixer': 'Le mélangeur baratte et racle',
    'subtitle.immersiveengineering.ore_conveyor': 'L\'excavatrice transporte le minerai',
    'subtitle.immersiveengineering.ore_dump': 'L\'excavatrice déverse le minerai dans une trémie',
    'subtitle.immersiveengineering.preheater': 'Le préchauffeur souffle de l\'air',
    'subtitle.immersiveengineering.process_1': 'L\'établi automatique de l\'ingénieur perce',
    'subtitle.immersiveengineering.process_1_lift': 'L\'établi automatique de l\'ingénieur vrombit',
    'subtitle.immersiveengineering.process_2': 'L\'établi automatique de l\'ingénieur soude',
    'subtitle.immersiveengineering.process_2_lift': 'L\'établi automatique de l\'ingénieur vrombit',
    'subtitle.immersiveengineering.refinery': 'La raffinerie vrombit',
    'subtitle.immersiveengineering.saw_empty': 'La scierie tourne à vide',
    'subtitle.immersiveengineering.saw_full': 'La scierie hurle en coupant le bois',
    'subtitle.immersiveengineering.saw_shutdown': 'La lame de la scierie ralentit',
    'subtitle.immersiveengineering.saw_startup': 'La lame de la scierie accélère',
    'subtitle.immersiveengineering.siren': 'La sirène hurle',

    # entity
    'entity.immersiveengineering.chemthrower_shot': 'Gouttelette de Lance-flammes chimique',
    'entity.immersiveengineering.railgun_shot': 'Tige de Railgun',
    'entity.immersiveengineering.revolver_shot': 'Balle',
    'entity.immersiveengineering.revolver_shot_flare': 'Fusée éclairante',
    'entity.immersiveengineering.revolver_shot_homing': 'Balle à tête chercheuse',
    'entity.immersiveengineering.revolver_shot_wolfpack': 'Balle Meute de loups',
    'entity.immersiveengineering.sawblade': 'Lame de scie',
    'entity.minecraft.villager.electrician': 'Électricien',
    'entity.minecraft.villager.engineer': 'Ingénieur structurel',
    'entity.minecraft.villager.gunsmith': 'Armurier',
    'entity.minecraft.villager.immersiveengineering:electrician': 'Électricien',
    'entity.minecraft.villager.immersiveengineering:engineer': 'Ingénieur structurel',
    'entity.minecraft.villager.immersiveengineering:gunsmith': 'Armurier',
    'entity.minecraft.villager.immersiveengineering:machinist': 'Machiniste',
    'entity.minecraft.villager.immersiveengineering:outfitter': 'Costumier',
    'entity.minecraft.villager.machinist': 'Machiniste',
    'entity.minecraft.villager.outfitter': 'Costumier',

    # manual
    'manual.immersiveengineering.electrical_grids': 'Réseaux électriques',
    'manual.immersiveengineering.explosives_weaponry': 'Explosifs & Armement',
    'manual.immersiveengineering.heavy_machinery': 'Machinerie lourde',
    'manual.immersiveengineering.introduction': 'Introduction',
    'manual.immersiveengineering.multiblock_constructions': 'Constructions multiblocs',
    'manual.immersiveengineering.other_engineers': 'Autres ingénieurs',
    'manual.immersiveengineering.redstone_control': 'Contrôle redstone',
    'manual.immersiveengineering.resources': 'Ressources',
    'manual.immersiveengineering.storage_transport': 'Stockage & Transport',
    'manual.immersiveengineering.updates': '!!Nouvelles mises à jour !!',
    'manual.immersiveengineering.weird_science': 'Science étrange',
    'manual.immersiveengineering.workbenches_machinery': 'Établis & Machinerie',

    # fluid_type
    'fluid_type.immersiveengineering.acetaldehyde': 'Acétaldéhyde',
    'fluid_type.immersiveengineering.biodiesel': 'Biodiesel',
    'fluid_type.immersiveengineering.concrete': 'Béton liquide',
    'fluid_type.immersiveengineering.creosote': 'Huile de créosote',
    'fluid_type.immersiveengineering.ethanol': 'Éthanol',
    'fluid_type.immersiveengineering.herbicide': 'Herbicide',
    'fluid_type.immersiveengineering.high_power_biodiesel': 'Biodiesel haute cétane',
    'fluid_type.immersiveengineering.phenolic_resin': 'Résine phénolique',
    'fluid_type.immersiveengineering.plantoil': 'Huile végétale',
    'fluid_type.immersiveengineering.potion': 'Potion',
    'fluid_type.immersiveengineering.redstone_acid': 'Acide de redstone',

    # chat
    'chat.immersiveengineering.info.bottling_machine.completeFill': 'Conserver les récipients jusqu\'à plein',
    'chat.immersiveengineering.info.bottling_machine.partialFill': 'Autoriser le remplissage partiel',
    'chat.immersiveengineering.info.conveyor.stacksize': 'Extraira %1$s objets par seconde',
    'chat.immersiveengineering.info.crate_sealed': 'La caisse est maintenant scellée et peut être ramassée',
    'chat.immersiveengineering.info.drill_mode.multi': 'Creuser plusieurs blocs',
    'chat.immersiveengineering.info.drill_mode.single': 'Creuser un seul bloc',
    'chat.immersiveengineering.info.glider.too_fast': 'Cette vitesse est trop élevée et endommagera le planeur',
    'chat.immersiveengineering.info.light_level': 'Niveau de lumière : %1$s',
    'chat.immersiveengineering.info.redstone_level': 'Niveau de redstone : %1$s',
    'chat.immersiveengineering.warning.crate_unsealed': 'Cette caisse n\'est pas scellée',

    # item
    'item.immersiveengineering.bannerpattern_screwdriver.desc': 'Tournevis',
    'item.immersiveengineering.bannerpattern_warning.desc': 'Panneaux d\'avertissement',
    'item.immersiveengineering.bannerpattern_wirecutter.desc': 'Coupe-fil',
    'item.immersiveengineering.revolver.einhorn': 'Eu-K508 S \'Einhorn\'',
    'item.immersiveengineering.shader.name.acepride': 'L\'As',
    'item.immersiveengineering.shader.name.bipride': 'Aimer les deux',
    'item.immersiveengineering.shader.name.enbypride': 'NB',
    'item.immersiveengineering.shader.name.gaypride': 'Les garçons aiment les garçons',
    'item.immersiveengineering.shader.name.lesbianpride': 'Les filles aiment les filles',
    'item.immersiveengineering.shader.name.transpride': 'Brisez le cis-tème',

    # tag
    'tag.biome.forge.is_swamp': 'marécages',
    'tag.biome.immersiveengineering.generate_ancient_seabed': 'marécageux ou cultivant des coraux',
    'tag.biome.immersiveengineering.generate_hardened_clay_pan': 'plats et secs',
    'tag.biome.minecraft.is_badlands': 'badlands',
    'tag.biome.minecraft.is_mountain': 'montagneux',
    'tag.biome.minecraft.is_nether': 'dans le Nether',
    'tag.biome.minecraft.is_ocean': 'océaniques',
    'tag.biome.minecraft.is_overworld': 'dans l\'Overworld',
    'tag.biome.minecraft.is_river': 'rivières',
    'tag.biome.minecraft.is_taiga': 'taïgas',

    # config
    'config.jade.plugin_immersiveengineering.hemp': 'Croissance du chanvre industriel',
    'config.jade.plugin_immersiveengineering.multiblock_icon': 'Icônes des multiblocs',
    'config.jade.plugin_immersiveengineering.multiblock_inventory': 'Inventaire des multiblocs',
    'config.jade.plugin_immersiveengineering.multiblock_tank': 'Réservoir des multiblocs',

    # ie.manual
    'ie.manual.entry.minerals.biomes': '§l%1$s§r est un filon minéral trouvé dans des biomes qui sont %2$s.',
    'ie.manual.entry.minerals.biomes_and': '%1$s et sont %2$s',
    'ie.manual.entry.minerals.biomes_or': '%1$s ou %2$s',

    # stat
    'stat.immersiveengineering.skyhook_distance': 'Distance parcourue avec le Skyhook',
    'stat.immersiveengineering.wire_deaths': 'Morts dues aux fils',

    # effect
    'effect.immersiveengineering.incognito': 'Incognito',

    # immersiveengineering long string
    'immersiveengineering.optifinePoseStackWarning': "Immersive Engineering a détecté une version incompatible d'Optifine. À cause du processus de patching d'Optifine, cette version d'Optifine supprime les méthodes ajoutées par Forge qui sont utilisées, directement ou indirectement, par Immersive Engineering et de nombreux autres mods. En conséquence, vous risquez probablement un crash à des moments quasi aléatoires, par exemple lorsqu'une recherche correspond à certains objets. Il est recommandé de ne pas utiliser Optifine tant que ce problème n'est pas résolu.",
}


out = {}
missing = []

for key, en in src.items():
    if key in HARDCODED:
        out[key] = HARDCODED[key]
        continue
    banner = translate_banner(key, en)
    if banner is not None:
        out[key] = banner
        continue
    missing.append((key, en))

print(f"Translated: {len(out)} / {len(src)}")
print(f"Missing: {len(missing)}")
for k, v in missing[:20]:
    print(f"  MISSING {k} => {v}")

# Ensure correct count
assert len(out) == len(src), f"count mismatch: {len(out)} vs {len(src)}"

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
with open(OUTPUT, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
print(f"Wrote {OUTPUT} with {len(out)} keys")
