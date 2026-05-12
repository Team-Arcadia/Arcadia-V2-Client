// Priority: 100

/*
    Arcadia V2 — Recipe Overhaul: Mekanism — Tier-gated machine recipes

    T1 machines require Create gears (iron_sheet + Create parts) instead of raw ingots, escalating costs through T2/T3 tiers.

    Author: vyrriox
*/

ServerEvents.recipes((event) => {
    // --- Shared constants ---
    const IRON_SHEET = "create:iron_sheet";
    const GOLD_SHEET = "create:golden_sheet";
    const COPPER_SHEET = "create:copper_sheet";
    const COGWHEEL = "create:cogwheel";
    const REINFORCE_BLOCK = "minecraft:breeze_rod";

    // --- Bridge & cross-mod constants ---
    const ARCANE_CIRCUIT = 'arcadia:arcane_circuit';
    const ETHEREAL_ALLOY = 'arcadia:ethereal_alloy';
    const INDUSTRIAL_HEART = 'arcadia:industrial_heart';
    const RUNE_MATRIX = 'arcadia:rune_matrix';
    const MEK_ALLOY_INFUSED = 'mekanism:alloy_infused';
    const MEK_ALLOY_REINFORCED = 'mekanism:alloy_reinforced';
    const MEK_ALLOY_ATOMIC = 'mekanism:alloy_atomic';
    const TFMG_STEEL_INGOT = 'tfmg:steel_ingot';
    const TFMG_HEAVY_PLATE = 'tfmg:heavy_plate';
    const TFMG_STEEL_MECHANISM = 'tfmg:steel_mechanism';
    const IE_PLATE_STEEL = 'immersiveengineering:plate_steel';
    const IE_COMPONENT_STEEL = 'immersiveengineering:component_steel';
    const SOURCE_GEM = 'ars_nouveau:source_gem';
    const SOURCE_GEM_BLOCK = 'ars_nouveau:source_gem_block';
    const MAGEBLOOM_CLOTH = 'ars_nouveau:magebloom_fiber';
    const ARCHWOOD = '#c:logs/archwood';
    const BRASS_SHEET = 'create:brass_sheet';


    console.info("[Arcadia V2] Loading recipe overhaul: 03_mekanism.js...");

    // ============================================================
    // 13. MEKANISM HARDENING
    //     T1 machines + brass/cogwheel; T2/T3 + PM; endgame + AA + bridges.
    // ============================================================

    // T1 Machines — cross-mod Create gears (iron sheet + Create parts instead of raw ingots)
    event.replaceInput({ output: 'mekanism:enrichment_chamber' }, 'minecraft:redstone', IRON_SHEET);
    event.replaceInput({ output: 'mekanism:crusher' }, 'minecraft:redstone', COGWHEEL);
    event.replaceInput({ output: 'mekanism:metallurgic_infuser' }, 'minecraft:redstone', 'create:precision_mechanism');

    // osmium_compressor: original uses '#mekanism:alloys/infused', '#c:circuits/advanced', steel_casing, bucket.
    // Replace bucket with IRON_SHEET for a visible hardening.
    event.remove({ output: 'mekanism:osmium_compressor' });
    event.shaped('mekanism:osmium_compressor', ['ACA', 'SXS', 'ACA'], {
        A: '#mekanism:alloys/infused',
        C: '#c:circuits/advanced',
        S: IRON_SHEET,
        X: 'mekanism:steel_casing'
    }).id('arcadia:mek_osmium_compressor');

    // combiner: original uses '#mekanism:alloys/reinforced', '#c:circuits/elite', steel_casing, stone_crafting_materials tag.
    // Replace stone with deepslate (harder) for a visible hardening.
    event.remove({ output: 'mekanism:combiner' });
    event.shaped('mekanism:combiner', ['ACA', 'DXD', 'ACA'], {
        A: '#mekanism:alloys/reinforced',
        C: '#c:circuits/elite',
        D: 'minecraft:deepslate',
        X: 'mekanism:steel_casing'
    }).id('arcadia:mek_combiner');

    // T2 Machines — require TFMG Steel + PM (harder)
    event.remove({ output: 'mekanism:purification_chamber' });
    event.shaped('mekanism:purification_chamber', ['RPR', 'IEI', 'SCS'], {
        R: TFMG_STEEL_INGOT,
        P: 'create:precision_mechanism',
        I: 'mekanism:advanced_control_circuit',
        E: 'mekanism:enrichment_chamber',
        S: MEK_ALLOY_REINFORCED,
        C: 'mekanism:steel_casing'
    }).id('arcadia:mek_purification_chamber');

    event.remove({ output: 'mekanism:chemical_injection_chamber' });
    event.shaped('mekanism:chemical_injection_chamber', ['RPR', 'IEI', 'SCS'], {
        R: MEK_ALLOY_REINFORCED,
        P: 'create:precision_mechanism',
        I: 'mekanism:elite_control_circuit',
        E: 'mekanism:purification_chamber',
        S: TFMG_STEEL_INGOT,
        C: 'mekanism:steel_casing'
    }).id('arcadia:mek_chemical_injection_chamber');

    event.remove({ output: 'mekanism:pressurized_reaction_chamber' });
    event.recipes.create.mechanical_crafting(
        'mekanism:pressurized_reaction_chamber',
        [
            "SPS",
            "ACM",
            "SRS"
        ], {
            S: TFMG_STEEL_INGOT,
            P: 'create:precision_mechanism',
            A: 'mekanism:advanced_control_circuit',
            C: 'mekanism:steel_casing',
            M: ARCANE_CIRCUIT,
            R: MEK_ALLOY_REINFORCED
        }
    ).id('arcadia:mek_prc');

    event.replaceInput({ output: 'mekanism:thermal_evaporation_controller' }, 'minecraft:iron_ingot', TFMG_STEEL_INGOT);
    event.replaceInput({ output: 'mekanism:thermal_evaporation_controller' }, 'minecraft:redstone', 'create:brass_casing');

    event.replaceInput({ output: 'mekanism:solar_neutron_activator' }, 'minecraft:iron_ingot', MEK_ALLOY_ATOMIC);

    // T2 Control Circuit: vanilla recipes kept (table + infuser) — was too punishing as a hard gate.

    // T3 Control Circuit — single hardened recipe (replaces the vanilla table + infuser duplicates)
    // gated behind Arcane Circuit + reinforced alloy. Shapeless = lenient.
    event.remove({ output: 'mekanism:elite_control_circuit' });
    event.shapeless('mekanism:elite_control_circuit', [
        'mekanism:advanced_control_circuit', MEK_ALLOY_REINFORCED, ARCANE_CIRCUIT
    ]).id('arcadia:mek_elite_circuit');

    // T4/Endgame
    event.remove({ output: 'mekanism:ultimate_control_circuit' });
    event.recipes.create.sequenced_assembly(
        [Item.of('mekanism:ultimate_control_circuit', 1)],
        'mekanism:elite_control_circuit',
        [
            event.recipes.createDeploying('mekanism:elite_control_circuit', ['mekanism:elite_control_circuit', MEK_ALLOY_ATOMIC]),
            event.recipes.createDeploying('mekanism:elite_control_circuit', ['mekanism:elite_control_circuit', 'create:precision_mechanism']),
            event.recipes.createDeploying('mekanism:elite_control_circuit', ['mekanism:elite_control_circuit', ARCANE_CIRCUIT]),
            event.recipes.createPressing('mekanism:elite_control_circuit', 'mekanism:elite_control_circuit')
        ]
    ).transitionalItem('mekanism:elite_control_circuit').loops(4).id('arcadia:mek_ultimate_circuit');

    event.remove({ output: 'mekanism:digital_miner' });
    event.recipes.create.mechanical_crafting(
        'mekanism:digital_miner',
        [
            " HAH ",
            "AIPIA",
            "PRMRP",
            "AIPIA",
            " HAH "
        ], {
            H: INDUSTRIAL_HEART,
            A: MEK_ALLOY_ATOMIC,
            I: IE_PLATE_STEEL,
            P: 'create:precision_mechanism',
            R: RUNE_MATRIX,
            M: 'mekanism:robit'
        }
    ).id('arcadia:mek_digital_miner');

    event.remove({ output: 'mekanism:teleporter' });
    event.recipes.create.mechanical_crafting(
        'mekanism:teleporter',
        [
            " EAE ",
            "APCPA",
            "ACTCA",
            "APCPA",
            " EAE "
        ], {
            E: 'minecraft:ender_eye',
            A: MEK_ALLOY_ATOMIC,
            P: 'create:precision_mechanism',
            C: SOURCE_GEM_BLOCK,
            T: 'mekanism:teleportation_core'
        }
    ).id('arcadia:mek_teleporter');

    event.remove({ output: 'mekanism:teleportation_core' });
    event.recipes.create.mixing('mekanism:teleportation_core', [
        '4x minecraft:diamond',
        '4x minecraft:gold_ingot',
        '2x ' + MEK_ALLOY_ATOMIC,
        '2x minecraft:ender_pearl',
        SOURCE_GEM,
        Fluid.of('minecraft:lava', 1000)
    ]).heated().id('arcadia:mek_teleportation_core');

    event.remove({ output: 'mekanism:qio_drive_array' });
    event.recipes.create.mechanical_crafting(
        'mekanism:qio_drive_array',
        [
            "SASAS",
            "APCPA",
            "SCMCS",
            "APCPA",
            "SASAS"
        ], {
            S: IE_PLATE_STEEL,
            A: MEK_ALLOY_ATOMIC,
            P: 'create:precision_mechanism',
            C: 'mekanism:elite_control_circuit',
            M: ARCANE_CIRCUIT
        }
    ).id('arcadia:mek_qio_drive_array');

    event.remove({ output: 'mekanism:qio_dashboard' });
    event.shaped('mekanism:qio_dashboard', ['GAG', 'PDP', 'SCS'], {
        G: 'create:brass_casing',
        A: ARCANE_CIRCUIT,
        P: 'create:precision_mechanism',
        D: 'mekanism:qio_drive_array',
        S: MEK_ALLOY_ATOMIC,
        C: 'mekanism:elite_control_circuit'
    }).id('arcadia:mek_qio_dashboard');

    event.remove({ output: 'mekanism:antiprotonic_nucleosynthesizer' });
    event.recipes.create.mechanical_crafting(
        'mekanism:antiprotonic_nucleosynthesizer',
        [
            "  FAF  ",
            " FAPAF ",
            "FAMCNAF",
            "APCRCPA",
            "FANCMAF",
            " FAPAF ",
            "  FAF  "
        ], {
            F: 'arcadia:fusion_matrix',
            A: MEK_ALLOY_ATOMIC,
            P: 'create:precision_mechanism',
            M: ARCANE_CIRCUIT,
            C: 'mekanism:ultimate_control_circuit',
            N: 'minecraft:nether_star',
            R: RUNE_MATRIX
        }
    ).id('arcadia:mek_antiprotonic');

    event.remove({ output: 'mekanism:sps_casing' });
    event.shaped('mekanism:sps_casing', ['ARA', 'RCR', 'ARA'], {
        A: MEK_ALLOY_ATOMIC,
        R: 'mekanism:structural_glass',
        C: 'create:brass_casing'
    }).id('arcadia:mek_sps_casing');

    // MekanismGenerators apex — tied to Arcadia fusion chain
    event.remove({ output: 'mekanismgenerators:fusion_reactor_controller' });
    event.recipes.create.mechanical_crafting(
        'mekanismgenerators:fusion_reactor_controller',
        [
            "  FMF  ",
            " FCPCF ",
            "FCMAMCF",
            "MPAHAPM",
            "FCMAMCF",
            " FCPCF ",
            "  FMF  "
        ], {
            F: 'arcadia:fusion_matrix',
            M: 'arcadia:plasma_cell',
            C: 'arcadia:containment_field_generator',
            P: 'create:precision_mechanism',
            A: MEK_ALLOY_ATOMIC,
            H: INDUSTRIAL_HEART
        }
    ).id('arcadia:mek_fusion_controller');

    // MekanismTools refined tier — add breeze rod + source gem
    const mekRefinedTools = [
        'mekanismtools:refined_glowstone_sword', 'mekanismtools:refined_glowstone_pickaxe',
        'mekanismtools:refined_glowstone_axe', 'mekanismtools:refined_glowstone_shovel',
        'mekanismtools:refined_glowstone_hoe', 'mekanismtools:refined_glowstone_paxel',
        'mekanismtools:refined_obsidian_sword', 'mekanismtools:refined_obsidian_pickaxe',
        'mekanismtools:refined_obsidian_axe', 'mekanismtools:refined_obsidian_shovel',
        'mekanismtools:refined_obsidian_hoe', 'mekanismtools:refined_obsidian_paxel'
    ];
    mekRefinedTools.forEach(item => event.replaceInput({ output: item }, 'minecraft:stick', REINFORCE_BLOCK));

    const mekRefinedArmor = [
        'mekanismtools:refined_glowstone_helmet', 'mekanismtools:refined_glowstone_chestplate',
        'mekanismtools:refined_glowstone_leggings', 'mekanismtools:refined_glowstone_boots',
        'mekanismtools:refined_obsidian_helmet', 'mekanismtools:refined_obsidian_chestplate',
        'mekanismtools:refined_obsidian_leggings', 'mekanismtools:refined_obsidian_boots'
    ];
    mekRefinedArmor.forEach(item => event.replaceInput({ output: item, allowEmpty: true }, 'minecraft:leather', SOURCE_GEM));

    // HDPE ROD — harden: 4 pellets + 1 brass sheet (Create) in a 2x3 shaped craft.
    event.remove({ output: 'mekanism:hdpe_rod' });
    event.shaped('mekanism:hdpe_rod', ['PP', 'PP', 'B '], {
        P: 'mekanism:hdpe_pellet',
        B: BRASS_SHEET
    }).id('arcadia:hdpe_rod');

    // HDPE SHEET — endgame Create Sequenced Assembly (5 loops, 5 ingredients per loop + molten steel).
    // Default: 3 pellets in Enrichment Chamber. New: full Create + TFMG + Mek chain.
    // Per sheet: 1 hdpe_pellet + 5 hdpe_rods + 5 brass_sheets + 5 heavy_plates + 5 alloy_reinforced + 2500mb molten_steel.
    event.remove({ output: 'mekanism:hdpe_sheet' });
    event.recipes.create.sequenced_assembly(
        [Item.of('mekanism:hdpe_sheet', 1)],
        'mekanism:hdpe_pellet',
        [
            event.recipes.createDeploying('mekanism:hdpe_pellet', ['mekanism:hdpe_pellet', 'mekanism:hdpe_rod']),
            event.recipes.createDeploying('mekanism:hdpe_pellet', ['mekanism:hdpe_pellet', BRASS_SHEET]),
            event.recipes.createDeploying('mekanism:hdpe_pellet', ['mekanism:hdpe_pellet', TFMG_HEAVY_PLATE]),
            event.recipes.createDeploying('mekanism:hdpe_pellet', ['mekanism:hdpe_pellet', MEK_ALLOY_REINFORCED]),
            event.recipes.createFilling('mekanism:hdpe_pellet', ['mekanism:hdpe_pellet', Fluid.of('tfmg:molten_steel', 500)]),
            event.recipes.createPressing('mekanism:hdpe_pellet', 'mekanism:hdpe_pellet')
        ]
    ).transitionalItem('mekanism:hdpe_pellet').loops(5).id('arcadia:hdpe_sheet');

});
