// Priority: 100

/*
    Arcadia V2 — Recipe Overhaul: Adventure Mods — Apotheosis, Aether, Aquaculture

    Apotheosis sigils, Aether gravitite/phoenix tier, Aquaculture neptunium tier.

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


    console.info("[Arcadia V2] Loading recipe overhaul: 09_adventure_mods.js...");

    // ============================================================
    // 26. APOTHEOSIS HARDENING
    // ============================================================

    // Sigils: moderate cross-mod hardening — same output counts as vanilla, just one bridge ingredient
    // added (ARCANE_CIRCUIT or precision_mechanism) so progression talks to Arcadia/Create.
    event.remove({ output: 'apotheosis:sigil_of_socketing' });
    event.shaped(Item.of('apotheosis:sigil_of_socketing', 3), ['GUG', 'EPE', 'GAG'], {
        G: 'apotheosis:gem_fused_slate',
        U: 'minecraft:gunpowder',
        E: 'apotheosis:gem_dust',
        P: 'create:precision_mechanism',
        A: 'minecraft:amethyst_shard'
    }).id('arcadia:apo_sigil_socketing');

    event.remove({ output: 'apotheosis:sigil_of_enhancement' });
    event.shaped(Item.of('apotheosis:sigil_of_enhancement', 4), ['GEG', 'EAE', 'GEG'], {
        G: 'apotheosis:gem_dust',
        E: 'apotheosis:gem_fused_slate',
        A: ARCANE_CIRCUIT
    }).id('arcadia:apo_sigil_enhancement');

    event.remove({ output: 'apotheosis:sigil_of_rebirth' });
    event.shaped(Item.of('apotheosis:sigil_of_rebirth', 6), ['GAG', 'EEE', 'GAG'], {
        G: 'apotheosis:gem_fused_slate',
        A: ARCANE_CIRCUIT,
        E: 'apotheosis:gem_dust'
    }).id('arcadia:apo_sigil_rebirth');

    // --- APEX: Sigil of Supremacy ---
    // The ultimate affix-upgrade sigil. Requires ALL 4 Arcadia bridges, the Fusion chain (tier 3),
    // Industrial Hearts, 4 Nether Stars and 1 Apotheosis Mythic Material.
    // Per sigil: 4 nether_star, 8 arcane_circuit, 4 rune_matrix, 4 ethereal_alloy,
    // 2 fusion_matrix, 2 industrial_heart, 1 mythic_material.
    event.remove({ output: 'apotheosis:sigil_of_supremacy' });
    event.recipes.create.mechanical_crafting(
        'apotheosis:sigil_of_supremacy',
        [
            "NARAN",
            "ACFCA",
            "RIMIR",
            "ACFCA",
            "NARAN"
        ], {
            N: 'minecraft:nether_star',
            A: ARCANE_CIRCUIT,
            R: RUNE_MATRIX,
            C: ETHEREAL_ALLOY,
            F: 'arcadia:fusion_matrix',
            I: INDUSTRIAL_HEART,
            M: 'apotheosis:mythic_material'
        }
    ).id('arcadia:apo_sigil_supremacy');

    // vial_of_expulsion was removed from Apotheosis 1.21 — skipped.

    // ============================================================
    // 27. AETHER HARDENING (gravitite + phoenix)
    // ============================================================

    const aetherGravititeTools = [
        'aether:gravitite_sword', 'aether:gravitite_pickaxe', 'aether:gravitite_axe',
        'aether:gravitite_shovel', 'aether:gravitite_hoe'
    ];
    aetherGravititeTools.forEach(item => event.replaceInput({ output: item }, 'aether:skyroot_stick', REINFORCE_BLOCK));

    // Gravitite armor: vanilla recipe uses only '#aether:processed/gravitite' tag.
    // We rebuild each piece to add a gold_sheet hardening slot (visible change).
    const aetherGravititeArmor = [
        { id: 'aether:gravitite_helmet',     pattern: ['GGG', 'GSG'] },
        { id: 'aether:gravitite_chestplate', pattern: ['GSG', 'GGG', 'GGG'] },
        { id: 'aether:gravitite_leggings',   pattern: ['GGG', 'GSG', 'G G'] },
        { id: 'aether:gravitite_boots',      pattern: ['GSG', 'G G'] },
        { id: 'aether:gravitite_gloves',     pattern: ['GSG'] }
    ];
    aetherGravititeArmor.forEach(armor => {
        event.remove({ output: armor.id });
        event.shaped(armor.id, armor.pattern, {
            G: '#aether:processed/gravitite',
            S: GOLD_SHEET
        }).id('arcadia:' + armor.id.split(':')[1]);
    });

    // Phoenix armor: loot-only in current Aether build (no vanilla craft), nothing to harden.

    // ============================================================
    // 28. AQUACULTURE HARDENING (neptunium tier)
    // ============================================================

    const aquaNeptuniumTools = [
        'aquaculture:neptunium_sword', 'aquaculture:neptunium_pickaxe',
        'aquaculture:neptunium_axe', 'aquaculture:neptunium_shovel',
        'aquaculture:neptunium_hoe'
    ];
    aquaNeptuniumTools.forEach(item => event.replaceInput({ output: item, allowEmpty: true }, 'minecraft:stick', REINFORCE_BLOCK));

    const aquaNeptuniumArmor = [
        'aquaculture:neptunium_helmet', 'aquaculture:neptunium_chestplate',
        'aquaculture:neptunium_leggings', 'aquaculture:neptunium_boots'
    ];
    aquaNeptuniumArmor.forEach(item => event.replaceInput({ output: item, allowEmpty: true }, 'aquaculture:neptunium_ingot', SOURCE_GEM));

    console.info("[Arcadia V2] Harder Recipes Script (Fin) Loaded!");
});
