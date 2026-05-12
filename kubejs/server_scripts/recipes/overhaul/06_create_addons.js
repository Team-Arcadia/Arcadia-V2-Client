// Priority: 100

/*
    Arcadia V2 — Recipe Overhaul: Create Addons — Addition, Nuclear, Diesel hardening

    Create Addition (electric), Create Nuclear, and Create Diesel Generators all reinforced with cross-mod bridges.

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


    console.info("[Arcadia V2] Loading recipe overhaul: 06_create_addons.js...");

    // ============================================================
    // 16. CREATE ADDITION HARDENING
    // ============================================================

    event.remove({ output: 'createaddition:capacitor' });
    event.shaped('createaddition:capacitor', ['BEB', 'GRG', 'GWG'], {
        B: 'create:brass_sheet',
        E: 'create:electron_tube',
        G: 'minecraft:gold_ingot',
        R: 'minecraft:redstone',
        W: 'createaddition:copper_wire'
    }).id('arcadia:ca_capacitor');

    event.remove({ output: 'createaddition:modular_accumulator' });
    event.recipes.create.mechanical_crafting(
        'createaddition:modular_accumulator',
        [
            "GCG",
            "CAC",
            "GCG"
        ], {
            G: GOLD_SHEET,
            C: 'createaddition:capacitor',
            A: ARCANE_CIRCUIT
        }
    ).id('arcadia:ca_modular_accumulator');

    // createaddition:charger item does not exist — removed.
    event.remove({ output: 'createaddition:portable_energy_interface' });
    event.shaped('createaddition:portable_energy_interface', ['SCS', 'PMP', 'SCS'], {
        S: IRON_SHEET,
        C: 'createaddition:capacitor',
        P: 'create:precision_mechanism',
        M: 'create:copper_casing'
    }).id('arcadia:ca_portable_energy');

    event.remove({ output: 'createaddition:tesla_coil' });
    event.recipes.create.mechanical_crafting(
        'createaddition:tesla_coil',
        [
            " W ",
            "CPC",
            "HAH"
        ], {
            W: 'createaddition:copper_spool',
            C: 'createaddition:capacitor',
            P: 'create:precision_mechanism',
            H: TFMG_HEAVY_PLATE,
            A: MEK_ALLOY_ATOMIC
        }
    ).id('arcadia:ca_tesla_coil');

    event.remove({ output: 'createaddition:alternator' });
    event.shaped('createaddition:alternator', ['BWB', 'WAW', 'BWB'], {
        B: 'create:brass_sheet',
        W: 'createaddition:copper_spool',
        A: 'create:andesite_casing'
    }).id('arcadia:ca_alternator');

    event.remove({ output: 'createaddition:rolling_mill' });
    event.shaped('createaddition:rolling_mill', [' S ', 'SCS', 'PBP'], {
        S: IRON_SHEET,
        C: COGWHEEL,
        P: 'create:precision_mechanism',
        B: 'create:brass_casing'
    }).id('arcadia:ca_rolling_mill');

    // ============================================================
    // 17. CREATE NUCLEAR HARDENING
    // ============================================================

    event.remove({ output: 'createnuclear:reactor_casing' });
    event.shaped('createnuclear:reactor_casing', ['HPH', 'PCP', 'HPH'], {
        H: TFMG_HEAVY_PLATE,
        P: 'create:precision_mechanism',
        C: 'createnuclear:steel_block'
    }).id('arcadia:cn_reactor_casing');

    event.remove({ output: 'createnuclear:reactor_controller' });
    event.recipes.create.mechanical_crafting(
        'createnuclear:reactor_controller',
        [
            "CAC",
            "PRP",
            "CAC"
        ], {
            C: 'createnuclear:reactor_casing',
            A: MEK_ALLOY_ATOMIC,
            P: 'create:precision_mechanism',
            R: RUNE_MATRIX
        }
    ).id('arcadia:cn_reactor_controller');

    event.remove({ output: 'createnuclear:reactor_core' });
    event.shaped('createnuclear:reactor_core', ['CPC', 'URU', 'CPC'], {
        C: 'createnuclear:reactor_casing',
        P: 'create:precision_mechanism',
        U: 'createnuclear:uranium_rod',
        R: 'createnuclear:reinforced_glass'
    }).id('arcadia:cn_reactor_core');

    event.remove({ output: 'createnuclear:reactor_frame' });
    event.shaped('createnuclear:reactor_frame', ['HPH', 'P P', 'HPH'], {
        H: 'createnuclear:lead_ingot',
        P: TFMG_HEAVY_PLATE
    }).id('arcadia:cn_reactor_frame');

    event.remove({ output: 'createnuclear:reinforced_glass' });
    event.shaped('createnuclear:reinforced_glass', ['LGL', 'GPG', 'LGL'], {
        L: 'createnuclear:lead_ingot',
        G: 'minecraft:glass',
        P: 'create:precision_mechanism'
    }).id('arcadia:cn_reinforced_glass');

    // ============================================================
    // 18. CREATE DIESEL GENERATORS HARDENING
    // ============================================================

    event.remove({ output: 'createdieselgenerators:diesel_engine' });
    event.recipes.create.mechanical_crafting(
        'createdieselgenerators:diesel_engine',
        [
            "SPS",
            "CHC",
            "SMS"
        ], {
            S: TFMG_HEAVY_PLATE,
            P: 'create:precision_mechanism',
            C: 'create:brass_casing',
            H: INDUSTRIAL_HEART,
            M: 'createaddition:copper_spool'
        }
    ).id('arcadia:cdg_diesel_engine');

    event.remove({ output: 'createdieselgenerators:large_diesel_engine' });
    event.recipes.create.mechanical_crafting(
        'createdieselgenerators:large_diesel_engine',
        [
            "SHS",
            "DID",
            "SPS"
        ], {
            S: TFMG_HEAVY_PLATE,
            H: INDUSTRIAL_HEART,
            D: 'createdieselgenerators:diesel_engine',
            I: TFMG_STEEL_MECHANISM,
            P: 'create:precision_mechanism'
        }
    ).id('arcadia:cdg_large_diesel_engine');

    event.remove({ output: 'createdieselgenerators:huge_diesel_engine' });
    event.recipes.create.mechanical_crafting(
        'createdieselgenerators:huge_diesel_engine',
        [
            "SHHHS",
            "HDIDH",
            "SHAHS",
            "HDIDH",
            "SHHHS"
        ], {
            S: TFMG_HEAVY_PLATE,
            H: INDUSTRIAL_HEART,
            D: 'createdieselgenerators:large_diesel_engine',
            I: TFMG_STEEL_MECHANISM,
            A: MEK_ALLOY_ATOMIC
        }
    ).id('arcadia:cdg_huge_diesel_engine');

    event.remove({ output: 'createdieselgenerators:distillation_controller' });
    event.shaped('createdieselgenerators:distillation_controller', ['HPH', 'CIC', 'HPH'], {
        H: TFMG_HEAVY_PLATE,
        P: 'create:precision_mechanism',
        C: 'create:brass_casing',
        I: TFMG_STEEL_MECHANISM
    }).id('arcadia:cdg_distillation_controller');

});
