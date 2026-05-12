// Priority: 100

/*
    Arcadia V2 — Recipe Overhaul: Immersive Engineering — Cross-Create hardening

    IE multiblocks and components gated behind Create progression.

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


    console.info("[Arcadia V2] Loading recipe overhaul: 05_immersive_engineering.js...");

    // ============================================================
    // 15. IMMERSIVE ENGINEERING HARDENING
    // ============================================================

    event.remove({ output: 'immersiveengineering:hammer' });
    event.shaped('immersiveengineering:hammer', [' II', ' SI', 'S  '], {
        I: IRON_SHEET,
        S: 'minecraft:stick'
    }).id('arcadia:ie_hammer');

    event.remove({ output: 'immersiveengineering:light_engineering' });
    event.shaped('immersiveengineering:light_engineering', ['SWS', 'ICI', 'SWS'], {
        S: IRON_SHEET,
        W: 'immersiveengineering:wirecoil_copper',
        I: 'immersiveengineering:component_iron',
        C: COGWHEEL
    }).id('arcadia:ie_light_engineering');

    event.remove({ output: 'immersiveengineering:heavy_engineering' });
    event.shaped('immersiveengineering:heavy_engineering', ['SPS', 'PCP', 'SPS'], {
        S: TFMG_HEAVY_PLATE,
        P: 'create:precision_mechanism',
        C: IE_COMPONENT_STEEL
    }).id('arcadia:ie_heavy_engineering');

    event.remove({ output: 'immersiveengineering:revolver' });
    event.shaped('immersiveengineering:revolver', [' GS', 'CPM', 'HB '], {
        G: 'immersiveengineering:gunpart_hammer',
        S: IE_PLATE_STEEL,
        C: 'create:brass_sheet',
        P: 'create:precision_mechanism',
        M: IE_COMPONENT_STEEL,
        H: 'immersiveengineering:coil_mv',
        B: 'immersiveengineering:wooden_grip'
    }).id('arcadia:ie_revolver');

    event.remove({ output: 'immersiveengineering:drill' });
    event.recipes.create.mechanical_crafting(
        'immersiveengineering:drill',
        [
            "  SHS",
            " SPCS",
            "SMECS",
            " SPCS",
            "  SHS"
        ], {
            S: TFMG_HEAVY_PLATE,
            H: INDUSTRIAL_HEART,
            P: 'create:precision_mechanism',
            C: IE_COMPONENT_STEEL,
            M: 'immersiveengineering:heavy_engineering',
            E: 'immersiveengineering:capacitor_mv'
        }
    ).id('arcadia:ie_drill');

    event.remove({ output: 'immersiveengineering:railgun' });
    event.recipes.create.mechanical_crafting(
        'immersiveengineering:railgun',
        [
            "SSSSS",
            "CPAPC",
            "SMHMS",
            "CPAPC",
            "SSSSS"
        ], {
            S: IE_PLATE_STEEL,
            C: 'immersiveengineering:capacitor_hv',
            P: 'create:precision_mechanism',
            A: MEK_ALLOY_ATOMIC,
            M: 'immersiveengineering:heavy_engineering',
            H: INDUSTRIAL_HEART
        }
    ).id('arcadia:ie_railgun');

    // Note: IE Excavator and Arc Furnace are multiblocks, not crafted items — no override needed.

});
