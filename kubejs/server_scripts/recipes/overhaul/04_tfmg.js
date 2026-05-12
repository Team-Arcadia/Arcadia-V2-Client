// Priority: 100

/*
    Arcadia V2 — Recipe Overhaul: TFMG — Industrial component hardening

    TFMG steel and industrial components require Create bridging.

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


    console.info("[Arcadia V2] Loading recipe overhaul: 04_tfmg.js...");

    // ============================================================
    // 14. TFMG HARDENING
    // ============================================================

    event.replaceInput({ output: 'tfmg:converter' }, 'minecraft:copper_ingot', 'createaddition:copper_spool');
    event.replaceInput({ output: 'tfmg:converter' }, 'createaddition:copper_wire', 'createaddition:copper_spool');

    // Transistor: original sequenced_assembly uses '#c:wires/copper' tag. Rewrite to force copper_spool.
    event.remove({ id: 'tfmg:sequenced_assembly/transistor' });
    event.remove({ output: 'tfmg:transistor_item' });
    const incompleteTransistor = 'tfmg:unfinished_transistor';
    event.recipes.create.sequenced_assembly(
        [ Item.of('tfmg:transistor_item', 4) ],
        'tfmg:plastic_sheet',
        [
            event.recipes.createDeploying(incompleteTransistor, [incompleteTransistor, 'createaddition:copper_spool']),
            event.recipes.createDeploying(incompleteTransistor, [incompleteTransistor, 'tfmg:n_semiconductor']),
            event.recipes.createDeploying(incompleteTransistor, [incompleteTransistor, 'tfmg:p_semiconductor']),
            event.recipes.createDeploying(incompleteTransistor, [incompleteTransistor, 'tfmg:n_semiconductor'])
        ]
    ).transitionalItem(incompleteTransistor).loops(1).id('arcadia:tfmg_transistor_fix');

    event.remove({ output: 'tfmg:industrial_mixer' });
    event.recipes.create.mechanical_crafting(
        'tfmg:industrial_mixer',
        [
            "SCS",
            "PMP",
            "SHS"
        ], {
            S: TFMG_HEAVY_PLATE,
            C: COGWHEEL,
            P: 'create:precision_mechanism',
            M: 'create:mechanical_mixer',
            H: 'create:brass_casing'
        }
    ).id('arcadia:tfmg_industrial_mixer');

    event.remove({ output: 'tfmg:centrifuge' });
    event.recipes.create.mechanical_crafting(
        'tfmg:centrifuge',
        [
            "SPS",
            "CHC",
            "SMS"
        ], {
            S: TFMG_HEAVY_PLATE,
            P: 'create:precision_mechanism',
            C: 'create:brass_casing',
            H: TFMG_STEEL_MECHANISM,
            M: MEK_ALLOY_REINFORCED
        }
    ).id('arcadia:tfmg_centrifuge');

    event.remove({ output: 'tfmg:heavy_machinery_casing' });
    event.shaped('tfmg:heavy_machinery_casing', ['HPH', 'PHP', 'HPH'], {
        H: TFMG_HEAVY_PLATE,
        P: INDUSTRIAL_HEART
    }).id('arcadia:tfmg_heavy_machinery_casing');

    event.remove({ output: 'tfmg:large_engine' });
    event.shaped('tfmg:large_engine', ['HHH', 'PIP', 'CMC'], {
        H: TFMG_HEAVY_PLATE,
        P: 'create:precision_mechanism',
        I: INDUSTRIAL_HEART,
        C: 'createaddition:copper_spool',
        M: TFMG_STEEL_MECHANISM
    }).id('arcadia:tfmg_large_engine');

    event.remove({ output: 'tfmg:radial_engine' });
    event.shaped('tfmg:radial_engine', ['HCH', 'PIP', 'HMH'], {
        H: TFMG_HEAVY_PLATE,
        C: 'create:brass_casing',
        P: 'create:precision_mechanism',
        I: INDUSTRIAL_HEART,
        M: TFMG_STEEL_MECHANISM
    }).id('arcadia:tfmg_radial_engine');

    event.remove({ output: 'tfmg:turbine_engine' });
    event.shaped('tfmg:turbine_engine', ['HCH', 'IMI', 'HCH'], {
        H: TFMG_HEAVY_PLATE,
        C: 'create:brass_casing',
        I: INDUSTRIAL_HEART,
        M: 'create:precision_mechanism'
    }).id('arcadia:tfmg_turbine_engine');

    event.remove({ output: 'tfmg:steel_distillation_controller' });
    event.shaped('tfmg:steel_distillation_controller', ['HPH', 'CMC', 'HPH'], {
        H: TFMG_HEAVY_PLATE,
        P: 'create:precision_mechanism',
        C: 'create:brass_casing',
        M: TFMG_STEEL_MECHANISM
    }).id('arcadia:tfmg_distillation_controller');

    event.replaceInput({ output: 'tfmg:blast_furnace_hatch' }, 'minecraft:iron_ingot', TFMG_HEAVY_PLATE);

});
