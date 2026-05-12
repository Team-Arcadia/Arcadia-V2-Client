// Priority: 100

/*
    Arcadia V2 — Recipe Overhaul: Storage & Peripherals — AdvancedPeripherals, RefinedStorage, FluxNetworks

    Advanced Peripherals computer parts, Refined Storage drives/exporters, Flux Networks transmitters — all gated behind Create brass / precision mechanisms.

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


    console.info("[Arcadia V2] Loading recipe overhaul: 07_storage_peripherals_flux.js...");

    // ============================================================
    // 19. ADVANCED PERIPHERALS HARDENING
    // ============================================================

    event.remove({ output: 'advancedperipherals:peripheral_casing' });
    event.shaped('advancedperipherals:peripheral_casing', ['SHS', 'HAH', 'SHS'], {
        S: TFMG_HEAVY_PLATE,
        H: IE_PLATE_STEEL,
        A: ARCANE_CIRCUIT
    }).id('arcadia:ap_peripheral_casing');

    event.remove({ output: 'advancedperipherals:rs_bridge' });
    event.recipes.create.mechanical_crafting(
        'advancedperipherals:rs_bridge',
        [
            "SPS",
            "PAQ",
            "SPS"
        ], {
            S: 'advancedperipherals:peripheral_casing',
            P: 'create:precision_mechanism',
            A: ARCANE_CIRCUIT,
            Q: 'refinedstorage:quartz_enriched_iron'
        }
    ).id('arcadia:ap_rs_bridge');

    event.remove({ output: 'advancedperipherals:me_bridge' });
    event.recipes.create.mechanical_crafting(
        'advancedperipherals:me_bridge',
        [
            "SAS",
            "PMP",
            "SAS"
        ], {
            S: 'advancedperipherals:peripheral_casing',
            A: MEK_ALLOY_ATOMIC,
            P: 'create:precision_mechanism',
            M: ARCANE_CIRCUIT
        }
    ).id('arcadia:ap_me_bridge');

    event.remove({ output: 'advancedperipherals:chunk_controller' });
    event.recipes.create.mechanical_crafting(
        'advancedperipherals:chunk_controller',
        [
            "EAE",
            "PSP",
            "EAE"
        ], {
            E: 'minecraft:ender_pearl',
            A: MEK_ALLOY_ATOMIC,
            P: 'create:precision_mechanism',
            S: 'advancedperipherals:peripheral_casing'
        }
    ).id('arcadia:ap_chunk_controller');

    event.remove({ output: 'advancedperipherals:player_detector' });
    event.shaped('advancedperipherals:player_detector', ['SES', 'EAE', 'SPS'], {
        S: 'advancedperipherals:peripheral_casing',
        E: 'minecraft:ender_eye',
        A: ARCANE_CIRCUIT,
        P: 'create:precision_mechanism'
    }).id('arcadia:ap_player_detector');

    // ============================================================
    // 20. REFINED STORAGE + EXTRADISKS HARDENING
    // ============================================================

    event.remove({ output: 'refinedstorage:grid' });
    event.shaped('refinedstorage:grid', ['SQS', 'GPG', 'SCS'], {
        S: IRON_SHEET,
        Q: 'minecraft:quartz',
        G: 'minecraft:glass_pane',
        P: 'create:precision_mechanism',
        C: 'create:brass_casing'
    }).id('arcadia:rs_grid');

    event.remove({ output: 'refinedstorage:crafting_grid' });
    event.shaped('refinedstorage:crafting_grid', [' C ', 'GRG', ' P '], {
        C: 'minecraft:crafting_table',
        G: 'minecraft:glass_pane',
        R: 'refinedstorage:grid',
        P: 'create:precision_mechanism'
    }).id('arcadia:rs_crafting_grid');

    event.remove({ output: 'refinedstorage:wireless_grid' });
    event.shaped('refinedstorage:wireless_grid', [' E ', 'GRG', ' B '], {
        E: 'minecraft:ender_pearl',
        G: 'minecraft:glass_pane',
        R: 'refinedstorage:grid',
        B: 'create:brass_casing'
    }).id('arcadia:rs_wireless_grid');

    // Storage parts: vanilla recipes restored (custom overrides removed).
    // Touched: refinedstorage:64k, extradisks:1024k/4096k/infinite_item_storage_part.

    // ============================================================
    // 21. FLUX NETWORKS HARDENING
    // ============================================================

    event.remove({ output: 'fluxnetworks:flux_controller' });
    event.recipes.create.mechanical_crafting(
        'fluxnetworks:flux_controller',
        [
            "FCF",
            "PSP",
            "FAF"
        ], {
            F: 'fluxnetworks:flux_core',
            C: SOURCE_GEM_BLOCK,
            P: 'create:precision_mechanism',
            S: 'minecraft:ender_eye',
            A: MEK_ALLOY_ATOMIC
        }
    ).id('arcadia:flux_controller');

    event.remove({ output: 'fluxnetworks:basic_flux_storage' });
    event.shaped('fluxnetworks:basic_flux_storage', ['CBC', 'FSF', 'CTC'], {
        C: 'create:brass_casing',
        B: 'fluxnetworks:flux_core',
        F: 'fluxnetworks:flux_block',
        S: TFMG_STEEL_INGOT,
        T: TFMG_HEAVY_PLATE
    }).id('arcadia:flux_storage');

    event.remove({ output: 'fluxnetworks:gargantuan_flux_storage' });
    event.recipes.create.mechanical_crafting(
        'fluxnetworks:gargantuan_flux_storage',
        [
            "HFH",
            "FSF",
            "HAH"
        ], {
            H: 'fluxnetworks:herculean_flux_storage',
            F: 'arcadia:fusion_matrix',
            A: MEK_ALLOY_ATOMIC,
            S: SOURCE_GEM_BLOCK
        }
    ).id('arcadia:flux_gargantuan_storage');

});
