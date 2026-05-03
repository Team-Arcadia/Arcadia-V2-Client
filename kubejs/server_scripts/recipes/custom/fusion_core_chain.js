// Priority: 500
/*
    FUSION CORE — Ultimate Hardcore Crafting Chain
    Requires: Create, Mekanism, TFMG, Immersive Engineering
    Created by vyrriox for Arcadia V2.

    Note: Create mixing max 64 items total per recipe.
    Uses small outputs to multiply resource costs through tiers.
*/

ServerEvents.recipes(event => {

    // ============================================================
    //  TIER 0 — PROCESSED MATERIALS
    //  High cost, low output = massive multiplication through tiers
    // ============================================================

    // 0A. ARCADIA ALLOY BLEND
    // 16 iron + 8 gold + 4 copper + 4 brass + 2 andesite alloy + lava -> 1
    event.recipes.create.mixing(
        'arcadia:alloy_blend',
        [
            '16x minecraft:iron_ingot',
            '8x minecraft:gold_ingot',
            '4x minecraft:copper_ingot',
            '4x create:brass_ingot',
            '2x create:andesite_alloy',
            Fluid.of('minecraft:lava', 1000)
        ]
    ).heated().id('arcadia:alloy_blend');

    // 0B. COMPRESSED DIAMOND MATRIX
    // 16 diamonds + 8 redstone + 4 lapis + 2 quartz -> 1
    event.recipes.create.mixing(
        'arcadia:diamond_matrix',
        [
            '16x minecraft:diamond',
            '8x minecraft:redstone',
            '4x minecraft:lapis_lazuli',
            '2x minecraft:quartz',
            Fluid.of('minecraft:lava', 500)
        ]
    ).heated().id('arcadia:diamond_matrix');

    // 0C. INFUSED STEEL BAR
    // 16 tfmg steel + 8 obsidian + 4 IE steel plates + 2 heavy plates -> 1
    event.recipes.create.mixing(
        'arcadia:infused_steel',
        [
            '16x tfmg:steel_ingot',
            '8x minecraft:obsidian',
            '4x immersiveengineering:plate_steel',
            '2x tfmg:heavy_plate',
            Fluid.of('tfmg:molten_steel', 500)
        ]
    ).heated().id('arcadia:infused_steel');

    // 0D. NETHER CONCENTRATE
    // 8 netherite scraps + 8 blaze rods + 4 magma cream + 4 gold -> 1
    event.recipes.create.mixing(
        'arcadia:nether_concentrate',
        [
            '8x minecraft:netherite_scrap',
            '8x minecraft:blaze_rod',
            '4x minecraft:magma_cream',
            '4x minecraft:gold_ingot',
            Fluid.of('minecraft:lava', 1000)
        ]
    ).heated().id('arcadia:nether_concentrate');

    // 0E. ENERGIZED DUST
    // 16 redstone + 8 glowstone + 4 osmium + 2 mek alloys -> 1
    event.recipes.create.mixing(
        'arcadia:energized_dust',
        [
            '16x minecraft:redstone',
            '8x minecraft:glowstone_dust',
            '4x mekanism:ingot_osmium',
            '2x mekanism:alloy_infused',
            Fluid.of('minecraft:water', 500)
        ]
    ).heated().id('arcadia:energized_dust');

    // 0F. WIRING BUNDLE (Mechanical Crafting 5x5)
    event.recipes.create.mechanical_crafting(
        'arcadia:wiring_bundle',
        [
            "WCGCW",
            "CGWGC",
            "GWCWG",
            "CGWGC",
            "WCGCW"
        ], {
            W: 'immersiveengineering:wirecoil_copper',
            C: 'minecraft:copper_ingot',
            G: 'minecraft:gold_ingot'
        }
    ).id('arcadia:wiring_bundle');

    // ============================================================
    //  TIER 1 — REFINED COMPONENTS
    //  Each eats 16-32 tier 0 items -> output 1
    // ============================================================

    // 1A. REFINED ALLOY INGOT
    // 16 alloy blend + 4 diamond matrix + 4 infused steel + 2 energized dust -> 1
    event.recipes.create.mixing(
        'arcadia:refined_alloy_ingot',
        [
            '16x arcadia:alloy_blend',
            '4x arcadia:diamond_matrix',
            '4x arcadia:infused_steel',
            '2x arcadia:energized_dust',
            Fluid.of('minecraft:lava', 1000)
        ]
    ).heated().id('arcadia:refined_alloy_ingot');

    // 1B. HARDENED STEEL COMPOUND
    // 16 infused steel + 8 alloy blend + 4 nether concentrate + 2 wiring -> 1
    event.recipes.create.mixing(
        'arcadia:hardened_steel_compound',
        [
            '16x arcadia:infused_steel',
            '8x arcadia:alloy_blend',
            '4x arcadia:nether_concentrate',
            '2x arcadia:wiring_bundle',
            Fluid.of('tfmg:molten_steel', 1000)
        ]
    ).heated().id('arcadia:hardened_steel_compound');

    // 1C. ENERGIZED CRYSTAL
    // 8 diamond matrix + 8 energized dust + 4 nether concentrate + 2 mek alloy -> 1
    event.recipes.create.mixing(
        'arcadia:energized_crystal',
        [
            '8x arcadia:diamond_matrix',
            '8x arcadia:energized_dust',
            '4x arcadia:nether_concentrate',
            '2x mekanism:alloy_reinforced',
            Fluid.of('minecraft:lava', 1000)
        ]
    ).heated().id('arcadia:energized_crystal');

    // 1D. TREATED COMPOSITE PLATE (Mechanical Crafting 5x5)
    event.recipes.create.mechanical_crafting(
        'arcadia:treated_composite_plate',
        [
            "SWBWS",
            "WABAW",
            "BASAB",
            "WABAW",
            "SWBWS"
        ], {
            S: 'arcadia:infused_steel',
            W: 'arcadia:wiring_bundle',
            B: 'arcadia:alloy_blend',
            A: 'immersiveengineering:plate_steel'
        }
    ).id('arcadia:treated_composite_plate');

    // ============================================================
    //  TIER 2 — ADVANCED COMPONENTS
    // ============================================================

    // 2A. QUANTUM CIRCUIT (Mechanical Crafting 5x5)
    event.recipes.create.mechanical_crafting(
        'arcadia:quantum_circuit',
        [
            "ERARE",
            "RCMCR",
            "AMUMA",
            "RCMCR",
            "ERARE"
        ], {
            E: 'arcadia:energized_crystal',
            R: 'arcadia:refined_alloy_ingot',
            A: 'mekanism:alloy_atomic',
            C: 'mekanism:ultimate_control_circuit',
            M: 'arcadia:diamond_matrix',
            U: 'minecraft:nether_star'
        }
    ).id('arcadia:quantum_circuit');

    // 2B. PLASMA CELL (Sequenced Assembly - 8 loops)
    event.recipes.create.sequenced_assembly(
        [Item.of('arcadia:plasma_cell', 1)],
        'arcadia:energized_crystal',
        [
            event.recipes.createDeploying('arcadia:incomplete_plasma_cell', ['arcadia:incomplete_plasma_cell', 'arcadia:refined_alloy_ingot']),
            event.recipes.createDeploying('arcadia:incomplete_plasma_cell', ['arcadia:incomplete_plasma_cell', 'arcadia:nether_concentrate']),
            event.recipes.createFilling('arcadia:incomplete_plasma_cell', ['arcadia:incomplete_plasma_cell', Fluid.of('minecraft:lava', 1000)]),
            event.recipes.createPressing('arcadia:incomplete_plasma_cell', 'arcadia:incomplete_plasma_cell'),
            event.recipes.createDeploying('arcadia:incomplete_plasma_cell', ['arcadia:incomplete_plasma_cell', 'minecraft:blaze_rod'])
        ]
    ).transitionalItem('arcadia:incomplete_plasma_cell').loops(8).id('arcadia:plasma_cell');

    // 2C. REINFORCED CASING (Sequenced Assembly - 8 loops)
    event.recipes.create.sequenced_assembly(
        [Item.of('arcadia:reinforced_casing', 1)],
        'arcadia:hardened_steel_compound',
        [
            event.recipes.createDeploying('arcadia:incomplete_reinforced_casing', ['arcadia:incomplete_reinforced_casing', 'arcadia:treated_composite_plate']),
            event.recipes.createDeploying('arcadia:incomplete_reinforced_casing', ['arcadia:incomplete_reinforced_casing', 'arcadia:infused_steel']),
            event.recipes.createFilling('arcadia:incomplete_reinforced_casing', ['arcadia:incomplete_reinforced_casing', Fluid.of('tfmg:molten_steel', 500)]),
            event.recipes.createPressing('arcadia:incomplete_reinforced_casing', 'arcadia:incomplete_reinforced_casing'),
            event.recipes.createDeploying('arcadia:incomplete_reinforced_casing', ['arcadia:incomplete_reinforced_casing', 'arcadia:wiring_bundle'])
        ]
    ).transitionalItem('arcadia:incomplete_reinforced_casing').loops(8).id('arcadia:reinforced_casing');

    // 2D. THERMAL CONDUCTOR
    event.recipes.create.mixing(
        'arcadia:thermal_conductor',
        [
            '8x arcadia:refined_alloy_ingot',
            '8x arcadia:nether_concentrate',
            '4x arcadia:energized_crystal',
            '8x minecraft:blaze_rod',
            Fluid.of('minecraft:lava', 2000)
        ]
    ).heated().id('arcadia:thermal_conductor');

    // ============================================================
    //  TIER 3 — ELITE COMPONENTS
    // ============================================================

    // 3A. FUSION MATRIX (Mechanical Crafting 7x7)
    event.recipes.create.mechanical_crafting(
        'arcadia:fusion_matrix',
        [
            " PQNQP ",
            "PQCSCQP",
            "QCSNSCP",
            "NCSNSCN",
            "QCSNSCP",
            "PQCSCQP",
            " PQNQP "
        ], {
            P: 'arcadia:plasma_cell',
            Q: 'arcadia:quantum_circuit',
            C: 'arcadia:energized_crystal',
            S: 'minecraft:nether_star',
            N: 'minecraft:netherite_block'
        }
    ).id('arcadia:fusion_matrix');

    // 3B. CONTAINMENT FIELD GENERATOR (Mechanical Crafting 7x7)
    event.recipes.create.mechanical_crafting(
        'arcadia:containment_field_generator',
        [
            " RTCTR ",
            "RTCHCTR",
            "TCHEHCT",
            "CHEAEHC",
            "TCHEHCT",
            "RTCHCTR",
            " RTCTR "
        ], {
            R: 'arcadia:reinforced_casing',
            T: 'arcadia:thermal_conductor',
            C: 'arcadia:treated_composite_plate',
            H: 'arcadia:hardened_steel_compound',
            E: 'immersiveengineering:wirecoil_electrum',
            A: 'mekanism:ultimate_control_circuit'
        }
    ).id('arcadia:containment_field_generator');

    // 3C. NEUTRON REFLECTOR (Sequenced Assembly - 10 loops)
    event.recipes.create.sequenced_assembly(
        [Item.of('arcadia:neutron_reflector', 1)],
        'arcadia:reinforced_casing',
        [
            event.recipes.createDeploying('arcadia:incomplete_neutron_reflector', ['arcadia:incomplete_neutron_reflector', 'minecraft:netherite_ingot']),
            event.recipes.createDeploying('arcadia:incomplete_neutron_reflector', ['arcadia:incomplete_neutron_reflector', 'minecraft:diamond_block']),
            event.recipes.createDeploying('arcadia:incomplete_neutron_reflector', ['arcadia:incomplete_neutron_reflector', 'arcadia:hardened_steel_compound']),
            event.recipes.createDeploying('arcadia:incomplete_neutron_reflector', ['arcadia:incomplete_neutron_reflector', 'arcadia:energized_crystal']),
            event.recipes.createFilling('arcadia:incomplete_neutron_reflector', ['arcadia:incomplete_neutron_reflector', Fluid.of('minecraft:lava', 1000)]),
            event.recipes.createPressing('arcadia:incomplete_neutron_reflector', 'arcadia:incomplete_neutron_reflector')
        ]
    ).transitionalItem('arcadia:incomplete_neutron_reflector').loops(10).id('arcadia:neutron_reflector');

    // ============================================================
    //  FINAL — FUSION CORE (Mechanical Crafting 9x9)
    // ============================================================

    event.recipes.create.mechanical_crafting(
        'arcadia:fusion_core',
        [
            "  NRHRN  ",
            " NFCMCFN ",
            "NFCQSQCFN",
            "RCQSFSQCR",
            "HMSFAFSMH",
            "RCQSFSQCR",
            "NFCQSQCFN",
            " NFCMCFN ",
            "  NRHRN  "
        ], {
            N: 'arcadia:neutron_reflector',
            R: 'arcadia:reinforced_casing',
            H: 'arcadia:hardened_steel_compound',
            F: 'arcadia:fusion_matrix',
            C: 'arcadia:containment_field_generator',
            Q: 'arcadia:quantum_circuit',
            S: 'minecraft:nether_star',
            M: 'minecraft:netherite_block',
            A: 'arcadia:plasma_cell'
        }
    ).id('arcadia:fusion_core');

    console.log('[Arcadia] FUSION CORE mega-chain loaded');
});
