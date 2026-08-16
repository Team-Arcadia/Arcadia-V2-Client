// Priority: 100

/*
    Arcadia V2 — Recipe Overhaul: Cross-mod hardening — General compatibility & bridge components

    Cross-mod gating for storage/magic/tech modules, light cross-mod touches, and bridge components that connect mod ecosystems.

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


    console.info("[Arcadia V2] Loading recipe overhaul: 02_crossmod_general.js...");

    // ==========================================
    // 7. MOD COMPATIBILITY
    // ==========================================

    // Aether Gloves
    event.remove({ output: "aether:leather_gloves" });
    event.shaped("aether:leather_gloves", ["LL", "SS"], {
        L: "minecraft:leather",
        S: "minecraft:string",
    });
    event.remove({ output: "aether:iron_gloves" });
    event.shaped("aether:iron_gloves", ["PP", "PP"], { P: IRON_SHEET });
    event.remove({ output: "aether:golden_gloves" });
    event.shaped("aether:golden_gloves", ["PP", "PP"], { P: GOLD_SHEET });
    event.remove({ output: "aether:diamond_gloves" });
    event.shaped("aether:diamond_gloves", ["DD", "OO"], {
        D: "minecraft:diamond",
        O: REINFORCE_BLOCK,
    });
    event.remove({ output: "aether:netherite_gloves" });
    event.smithing(
        "aether:netherite_gloves",
        "minecraft:netherite_upgrade_smithing_template",
        "aether:diamond_gloves",
        "minecraft:netherite_ingot",
    );

    // Better Copper (Copper Sheets)
    const copperGear = [
        "bettercopper:copper_sword",
        "bettercopper:copper_axe",
        "bettercopper:copper_helmet",
        "bettercopper:copper_chestplate",
        "bettercopper:copper_leggings",
        "bettercopper:copper_boots",
        "bettercopper:copper_pickaxe",
        "bettercopper:copper_shovel",
        "bettercopper:copper_hoe",
    ];
    copperGear.forEach((item) => event.remove({ output: item }));
    event.shaped("bettercopper:copper_sword", ["C", "C", "S"], {
        C: COPPER_SHEET,
        S: "minecraft:stick",
    });
    event.shaped("bettercopper:copper_axe", ["CC", "CS", " S"], {
        C: COPPER_SHEET,
        S: "minecraft:stick",
    });
    event.shaped("bettercopper:copper_pickaxe", ["CCC", " S ", " S "], {
        C: COPPER_SHEET,
        S: "minecraft:stick",
    });
    event.shaped("bettercopper:copper_shovel", ["C", "S", "S"], {
        C: COPPER_SHEET,
        S: "minecraft:stick",
    });
    event.shaped("bettercopper:copper_hoe", ["CC", " S", " S"], {
        C: COPPER_SHEET,
        S: "minecraft:stick",
    });
    event.shaped("bettercopper:copper_helmet", ["CCC", "C C"], {
        C: COPPER_SHEET,
    });
    event.shaped("bettercopper:copper_chestplate", ["C C", "CCC", "CCC"], {
        C: COPPER_SHEET,
    });
    event.shaped("bettercopper:copper_leggings", ["CCC", "C C", "C C"], {
        C: COPPER_SHEET,
    });
    event.shaped("bettercopper:copper_boots", ["C C", "C C"], {
        C: COPPER_SHEET,
    });

    // Mekanism (Lapis Tools)
    event.remove({ output: "mekanismtools:lapis_lazuli_sword" });
    event.shaped("mekanismtools:lapis_lazuli_sword", ["L", "L", "S"], {
        L: "minecraft:lapis_lazuli",
        S: "minecraft:stick",
    });

    event.remove({ output: "mekanismtools:lapis_lazuli_shield" });
    event.shaped("mekanismtools:lapis_lazuli_shield", ["LIL", "LPL", " L "], {
        L: "minecraft:lapis_lazuli",
        I: IRON_SHEET,
        P: "#minecraft:planks",
    });

    const lapisArmor = [
        "mekanismtools:lapis_lazuli_helmet",
        "mekanismtools:lapis_lazuli_chestplate",
        "mekanismtools:lapis_lazuli_leggings",
        "mekanismtools:lapis_lazuli_boots",
    ];
    lapisArmor.forEach((item) => event.remove({ output: item }));
    event.shaped("mekanismtools:lapis_lazuli_helmet", ["LIL", "L L"], {
        L: "minecraft:lapis_lazuli",
        I: IRON_SHEET,
    });
    event.shaped("mekanismtools:lapis_lazuli_chestplate", ["I I", "LIL", "LLL"], {
        L: "minecraft:lapis_lazuli",
        I: IRON_SHEET,
    });
    event.shaped("mekanismtools:lapis_lazuli_leggings", ["LIL", "L L", "L L"], {
        L: "minecraft:lapis_lazuli",
        I: IRON_SHEET,
    });
    event.shaped("mekanismtools:lapis_lazuli_boots", ["I I", "L L"], {
        L: "minecraft:lapis_lazuli",
        I: IRON_SHEET,
    });

    // Mekanism Steel (Iron Sheets replacement)
    const mekanismSteel = [
        "mekanismtools:steel_pickaxe",
        "mekanismtools:steel_axe",
        "mekanismtools:steel_shovel",
        "mekanismtools:steel_hoe",
        "mekanismtools:steel_sword",
        "mekanismtools:steel_paxel",
    ];
    mekanismSteel.forEach((item) =>
        event.replaceInput({ output: item }, "minecraft:iron_ingot", IRON_SHEET),
    );

    // Create Whisk
    event.remove({ output: "create:whisk" });
    event.shaped("create:whisk", [" A ", "BAB", "BBB"], {
        A: "create:andesite_alloy",
        B: "minecraft:iron_bars",
    });

    // Create SA (Copper Sheets)
    const createSaCopper = [
        "create_sa:copper_helmet",
        "create_sa:copper_chestplate",
        "create_sa:copper_leggings",
        "create_sa:copper_boots",
        "create_sa:copper_pickaxe",
        "create_sa:copper_axe",
        "create_sa:copper_sword",
        "create_sa:copper_shovel",
        "create_sa:copper_hoe",
        "create_sa:copper_jetpack_chestplate",
        "create_sa:copper_exoskeleton_chestplate",
    ];
    createSaCopper.forEach((item) => {
        event.replaceInput(
            { output: item },
            "minecraft:copper_ingot",
            COPPER_SHEET,
        );
        event.replaceInput({ output: item }, "#forge:ingots/copper", COPPER_SHEET);
    });

    // Simply Swords
    const simplyIronWeapons = [
        "simplyswords:iron_claymore",
        "simplyswords:iron_greathammer",
        "simplyswords:iron_halberd",
        "simplyswords:iron_spear",
        "simplyswords:iron_glaive",
        "simplyswords:iron_warglaive",
        "simplyswords:iron_cutlass",
        "simplyswords:iron_sai",
        "simplyswords:iron_longsword",
        "simplyswords:iron_twinblade",
        "simplyswords:iron_rapier",
        "simplyswords:iron_katana",
        "simplyswords:iron_scythe",
        "simplyswords:iron_chakram",
        "simplyswords:iron_greataxe",
    ];
    simplyIronWeapons.forEach((item) =>
        event.replaceInput({ output: item }, "minecraft:iron_ingot", IRON_SHEET),
    );

    const simplyGoldWeapons = [
        "simplyswords:gold_claymore",
        "simplyswords:gold_greathammer",
        "simplyswords:gold_halberd",
        "simplyswords:gold_spear",
        "simplyswords:gold_glaive",
        "simplyswords:gold_warglaive",
        "simplyswords:gold_cutlass",
        "simplyswords:gold_sai",
        "simplyswords:gold_longsword",
        "simplyswords:gold_twinblade",
        "simplyswords:gold_rapier",
        "simplyswords:gold_katana",
        "simplyswords:gold_scythe",
        "simplyswords:gold_chakram",
        "simplyswords:gold_greataxe",
    ];
    simplyGoldWeapons.forEach((item) =>
        event.replaceInput({ output: item }, "minecraft:gold_ingot", GOLD_SHEET),
    );

    const simplyDiamondWeapons = [
        "simplyswords:diamond_claymore",
        "simplyswords:diamond_greathammer",
        "simplyswords:diamond_halberd",
        "simplyswords:diamond_spear",
        "simplyswords:diamond_glaive",
        "simplyswords:diamond_warglaive",
        "simplyswords:diamond_cutlass",
        "simplyswords:diamond_sai",
        "simplyswords:diamond_longsword",
        "simplyswords:diamond_twinblade",
        "simplyswords:diamond_rapier",
        "simplyswords:diamond_katana",
        "simplyswords:diamond_scythe",
        "simplyswords:diamond_chakram",
        "simplyswords:diamond_greataxe",
    ];
    simplyDiamondWeapons.forEach((item) =>
        event.replaceInput({ output: item }, "minecraft:stick", REINFORCE_BLOCK),
    );

    // Misc Items (Knives, etc.)
    const ironMisc = [
        "aquaculture:iron_fillet_knife",
        "aquaculture:iron_fishing_rod",
        "farmersdelight:iron_knife",
        "cosmeticweaponsmod:iron_knife",
    ];
    ironMisc.forEach((item) =>
        event.replaceInput({ output: item }, "minecraft:iron_ingot", IRON_SHEET),
    );

    const goldMisc = [
        "aquaculture:gold_fillet_knife",
        "aquaculture:gold_fishing_rod",
        "farmersdelight:golden_knife",
        "cosmeticweaponsmod:golden_knife",
    ];
    goldMisc.forEach((item) =>
        event.replaceInput({ output: item }, "minecraft:gold_ingot", GOLD_SHEET),
    );

    const diamondMisc = [
        "aquaculture:diamond_fillet_knife",
        "aquaculture:diamond_fishing_rod",
        "farmersdelight:diamond_knife",
        "cosmeticweaponsmod:diamond_knife",
    ];
    diamondMisc.forEach((item) =>
        event.replaceInput({ output: item }, "minecraft:stick", REINFORCE_BLOCK),
    );

    const copperMisc = ["create_things_and_misc:copper_knife"];
    copperMisc.forEach((item) => {
        event.replaceInput(
            { output: item },
            "minecraft:copper_ingot",
            COPPER_SHEET,
        );
        event.replaceInput({ output: item }, "#forge:ingots/copper", COPPER_SHEET);
    });

    const stoneMisc = [
        "aquaculture:stone_fillet_knife",
        "cosmeticweaponsmod:stone_knife",
    ];
    stoneMisc.forEach((item) =>
        event.replaceInput(
            { output: item },
            "minecraft:cobblestone",
            "minecraft:stone",
        ),
    );

    const woodMisc = [
        "aquaculture:wooden_fillet_knife",
        "cosmeticweaponsmod:wooden_knife",
    ];
    woodMisc.forEach((item) =>
        event.replaceInput(
            { output: item },
            "#minecraft:planks",
            "#minecraft:logs",
        ),
    );

    // DnDesires Gold Whisk
    event.replaceInput(
        { output: "dndesires:gold_whisk" },
        "minecraft:gold_ingot",
        "supplementaries:gold_gate",
    );
    event.replaceInput(
        { output: "dndesires:gold_whisk" },
        "#forge:plates/gold",
        "supplementaries:gold_gate",
    );
    event.replaceInput(
        { output: "dndesires:gold_whisk" },
        "create:golden_sheet",
        "supplementaries:gold_gate",
    );

    // Advanced Netherite (Mixer Recipes)
    const advNetherite = [
        "advancednetherite:netherite_iron_ingot",
        "advancednetherite:netherite_gold_ingot",
        "advancednetherite:netherite_emerald_ingot",
        "advancednetherite:netherite_diamond_ingot",
    ];
    advNetherite.forEach((item) => event.remove({ output: item }));

    // Iron Netherite (6 Iron + 1 Netherite)
    event.recipes.create
        .mixing("advancednetherite:netherite_iron_ingot", [
            "minecraft:netherite_ingot",
            "6x minecraft:iron_ingot",
        ])
        .heated();

    // Gold Netherite (6 Gold + 1 Iron Netherite)
    event.recipes.create
        .mixing("advancednetherite:netherite_gold_ingot", [
            "advancednetherite:netherite_iron_ingot",
            "6x minecraft:gold_ingot",
        ])
        .heated();

    // Emerald Netherite (6 Emerald + 1 Gold Netherite)
    event.recipes.create
        .mixing("advancednetherite:netherite_emerald_ingot", [
            "advancednetherite:netherite_gold_ingot",
            "6x minecraft:emerald",
        ])
        .heated();

    // Diamond Netherite (6 Diamond + 1 Emerald Netherite)
    event.recipes.create
        .mixing("advancednetherite:netherite_diamond_ingot", [
            "advancednetherite:netherite_emerald_ingot",
            "6x minecraft:diamond",
        ])
        .heated();

    // Restore the block decrafts: remove-by-ingot-output above also wiped the
    // mod's *_ingot_from_block recipes (same gotcha as minecraft:netherite_ingot)
    const advNetheriteTiers = ["iron", "gold", "emerald", "diamond"];
    advNetheriteTiers.forEach((tier) => {
        event
            .shapeless("9x advancednetherite:netherite_" + tier + "_ingot", [
                "advancednetherite:netherite_" + tier + "_block",
            ])
            .id("arcadia:netherite_" + tier + "_ingot_from_block");
    });

    // ============================================================
    // 10. CROSS-MOD HARDENING — Storage, Magic, Tech
    // ============================================================

    // --- STORAGE LECTERN (Ars) — APEX ENDGAME ---
    // Requires all 4 Arcadia bridges + Fusion Matrix (Arcadia tier 3 chain).
    // Forces completion of: Tech path (Industrial Heart), Magic path (Rune Matrix),
    // Arcane-tech bridge (Arcane Circuit), Occult bridge (Ethereal Alloy), Fusion chain.
    event.remove({ output: 'ars_nouveau:storage_lectern' });
    event.recipes.create.mechanical_crafting(
        'ars_nouveau:storage_lectern',
        [
            " ARA ",
            "EFPFE",
            "RPHPR",
            "EFPFE",
            " ARA "
        ], {
            A: ARCANE_CIRCUIT,
            R: RUNE_MATRIX,
            E: ETHEREAL_ALLOY,
            F: 'arcadia:fusion_matrix',
            P: 'create:precision_mechanism',
            H: INDUSTRIAL_HEART
        }
    ).id('arcadia:storage_lectern_apex');

    // --- ARS NOUVEAU cross-mod ---
    event.remove({ output: 'ars_nouveau:source_jar' });
    event.shaped('ars_nouveau:source_jar', [
        'GSG',
        'G G',
        'GBG'
    ], {
        G: 'minecraft:glass',
        S: 'ars_nouveau:source_gem',
        B: 'create:brass_ingot'
    }).id('arcadia:source_jar');

    // Imbuement Chamber: vanilla recipe restored (custom required source_gem_block which
    // soft-locked the Ars progression — source gems are made IN the imbuement chamber).

    event.remove({ output: 'ars_nouveau:relay' });
    event.shaped('ars_nouveau:relay', [
        ' S ',
        'GAG',
        ' M '
    ], {
        S: 'ars_nouveau:source_gem',
        G: 'create:golden_sheet',
        A: 'minecraft:amethyst_block',
        M: 'mekanism:alloy_infused'
    }).id('arcadia:relay');

    event.remove({ output: 'ars_nouveau:enchanting_apparatus' });
    event.recipes.create.mechanical_crafting(
        'ars_nouveau:enchanting_apparatus',
        [
            " GPG ",
            "GASAG",
            "PS SP",
            "GASAG",
            " GPG "
        ], {
            G: 'create:golden_sheet',
            P: 'create:precision_mechanism',
            A: '#c:logs/archwood',
            S: 'ars_nouveau:source_gem'
        }
    ).id('arcadia:enchanting_apparatus');

    // --- IRON'S SPELLBOOKS cross-mod ---
    event.remove({ output: 'irons_spellbooks:inscription_table' });
    event.shaped('irons_spellbooks:inscription_table', [
        'BIG',
        'SSS',
        'L L'
    ], {
        B: 'minecraft:book',
        I: 'minecraft:ink_sac',
        G: 'ars_nouveau:source_gem',
        S: 'create:golden_sheet',
        L: '#c:logs/archwood'
    }).id('arcadia:inscription_table');

    event.remove({ output: 'irons_spellbooks:scroll_forge' });
    event.shaped('irons_spellbooks:scroll_forge', [
        'G G',
        'SMS',
        'OOO'
    ], {
        G: 'ars_nouveau:source_gem',
        S: 'create:golden_sheet',
        M: 'mekanism:alloy_infused',
        O: 'minecraft:obsidian'
    }).id('arcadia:scroll_forge');

    event.remove({ output: 'irons_spellbooks:arcane_anvil' });
    event.recipes.create.mechanical_crafting(
        'irons_spellbooks:arcane_anvil',
        [
            "SSSSS",
            "  T  ",
            " TTT "
        ], {
            S: 'tfmg:steel_ingot',
            T: 'create:brass_casing'
        }
    ).id('arcadia:arcane_anvil');

    // --- OCCULTISM cross-mod ---
    event.remove({ output: 'occultism:golden_sacrificial_bowl' });
    event.shaped('occultism:golden_sacrificial_bowl', [
        'G G',
        'SAS',
        ' P '
    ], {
        G: 'create:golden_sheet',
        S: 'ars_nouveau:source_gem',
        A: 'minecraft:gold_block',
        P: 'create:precision_mechanism'
    }).id('arcadia:golden_sacrificial_bowl');

    event.remove({ output: 'occultism:chalk_white_impure' });
    event.shaped('occultism:chalk_white_impure', [
        ' M ',
        'BCB',
        ' M '
    ], {
        M: 'ars_nouveau:magebloom_fiber',
        B: 'minecraft:bone_meal',
        C: 'minecraft:calcite'
    }).id('arcadia:chalk_white_impure');

    // --- APOTHEOSIS cross-mod ---
    // hellshelf/seashelf removed from Apotheosis 1.21 — custom bookshelves handled by ApothicEnchanting instead.

    // --- RS + FLUX NETWORKS cross-mod ---
    event.remove({ output: 'refinedstorage:controller' });
    event.recipes.create.mechanical_crafting(
        'refinedstorage:controller',
        [
            " SPS ",
            "SQDQS",
            "PDRDP",
            "SQDQS",
            " SPS "
        ], {
            S: 'refinedstorage:quartz_enriched_iron',
            P: 'create:precision_mechanism',
            Q: 'create:brass_casing',
            D: 'minecraft:diamond',
            R: 'minecraft:redstone_block'
        }
    ).id('arcadia:rs_controller');

    event.remove({ output: 'fluxnetworks:flux_plug' });
    event.shaped('fluxnetworks:flux_plug', [
        'SFS',
        'FPF',
        'SFS'
    ], {
        S: 'tfmg:steel_ingot',
        F: 'fluxnetworks:flux_dust',
        P: 'create:precision_mechanism'
    }).id('arcadia:flux_plug');

    event.remove({ output: 'fluxnetworks:flux_point' });
    event.shaped('fluxnetworks:flux_point', [
        'SFS',
        'FBF',
        'SFS'
    ], {
        S: 'tfmg:steel_ingot',
        F: 'fluxnetworks:flux_dust',
        B: 'create:brass_casing'
    }).id('arcadia:flux_point');

    // ============================================================
    // 11. LIGHT CROSS-MOD — Small touches, not hard, just interconnected
    // ============================================================

    // --- Ars Nouveau: Novice Spellbook needs a touch of Create ---
    event.remove({ output: 'ars_nouveau:novice_spell_book' });
    event.shaped('ars_nouveau:novice_spell_book', [
        ' SG',
        'SBS',
        'LS '
    ], {
        S: 'ars_nouveau:source_gem',
        G: 'create:golden_sheet',
        B: 'minecraft:book',
        L: 'minecraft:leather'
    }).id('arcadia:novice_spell_book');

    // --- Ars: Scribes Table needs Create cogwheel ---
    event.remove({ output: 'ars_nouveau:scribes_table' });
    event.shaped('ars_nouveau:scribes_table', [
        'SBF',
        'LCL',
        'L L'
    ], {
        S: 'ars_nouveau:source_gem',
        B: 'minecraft:book',
        F: 'minecraft:feather',
        L: '#c:logs/archwood',
        C: COGWHEEL
    }).id('arcadia:scribes_table');

    // --- Ars: Wand needs brass ---
    event.remove({ output: 'ars_nouveau:wand' });
    event.shaped('ars_nouveau:wand', [
        '  S',
        ' B ',
        'G  '
    ], {
        S: 'ars_nouveau:source_gem',
        B: 'create:brass_ingot',
        G: 'create:golden_sheet'
    }).id('arcadia:ars_wand');

    // --- Irons: Alchemist Cauldron needs TFMG ---
    event.remove({ output: 'irons_spellbooks:alchemist_cauldron' });
    event.shaped('irons_spellbooks:alchemist_cauldron', [
        'T T',
        'T T',
        'TTT'
    ], {
        T: 'tfmg:steel_ingot'
    }).id('arcadia:alchemist_cauldron');

    // --- Occultism: Candle needs Ars magebloom ---
    event.remove({ output: 'occultism:large_candle_white' });
    event.shaped('4x occultism:large_candle_white', [
        'S',
        'M',
        'M'
    ], {
        S: 'minecraft:string',
        M: 'ars_nouveau:magebloom_fiber'
    }).id('arcadia:occultism_candle');

    // --- Occultism: Spirit Fire needs blaze + source gem ---
    event.remove({ output: 'occultism:spirit_fire' });
    event.shapeless('occultism:spirit_fire', [
        'minecraft:flint_and_steel',
        'ars_nouveau:source_gem',
        'minecraft:soul_sand'
    ]).id('arcadia:spirit_fire');

    // --- Waystones: Waystone needs Create + Ars ---
    event.remove({ output: 'waystones:waystone' });
    event.shaped('waystones:waystone', [
        ' S ',
        'EPE',
        'SSS'
    ], {
        S: 'minecraft:stone_bricks',
        E: 'minecraft:ender_pearl',
        P: 'ars_nouveau:source_gem'
    }).id('arcadia:waystone');

    // --- Waystones: Warp Stone needs source gem ---
    event.remove({ output: 'waystones:warp_stone' });
    event.shaped('waystones:warp_stone', [
        ' E ',
        'ESE',
        ' E '
    ], {
        E: 'minecraft:ender_pearl',
        S: 'ars_nouveau:source_gem'
    }).id('arcadia:warp_stone');

    // --- Farmers Delight: Cooking Pot needs Create sheets ---
    event.remove({ output: 'farmersdelight:cooking_pot' });
    event.shaped('farmersdelight:cooking_pot', [
        'S S',
        'SWS',
        'III'
    ], {
        S: IRON_SHEET,
        W: 'minecraft:water_bucket',
        I: 'minecraft:iron_ingot'
    }).id('arcadia:cooking_pot');

    // --- Farmers Delight: Stove needs TFMG steel ---
    event.remove({ output: 'farmersdelight:stove' });
    event.shaped('farmersdelight:stove', [
        'SSS',
        'ICI',
        'III'
    ], {
        S: 'tfmg:steel_ingot',
        I: 'minecraft:iron_ingot',
        C: 'minecraft:campfire'
    }).id('arcadia:stove');

    // --- RS: Disk Drive needs Create brass ---
    event.remove({ output: 'refinedstorage:disk_drive' });
    event.shaped('refinedstorage:disk_drive', [
        'BGB',
        'QRQ',
        'BGB'
    ], {
        B: 'create:brass_ingot',
        G: 'minecraft:glass',
        Q: 'refinedstorage:quartz_enriched_iron',
        R: 'minecraft:redstone'
    }).id('arcadia:rs_disk_drive');

    // --- RS: Importer needs Create brass ---
    event.remove({ output: 'refinedstorage:importer' });
    event.shaped('refinedstorage:importer', [
        ' B ',
        'QRQ',
        ' Q '
    ], {
        B: 'create:brass_ingot',
        Q: 'refinedstorage:quartz_enriched_iron',
        R: 'minecraft:redstone'
    }).id('arcadia:rs_importer');

    // --- RS: Exporter needs Create brass ---
    event.remove({ output: 'refinedstorage:exporter' });
    event.shaped('refinedstorage:exporter', [
        ' Q ',
        'QRQ',
        ' B '
    ], {
        B: 'create:brass_ingot',
        Q: 'refinedstorage:quartz_enriched_iron',
        R: 'minecraft:redstone'
    }).id('arcadia:rs_exporter');

    // --- RS: Crafter needs precision mechanism ---
    event.remove({ output: 'refinedstorage:autocrafter' });
    event.shaped('refinedstorage:autocrafter', [
        'QRQ',
        'RPR',
        'QRQ'
    ], {
        Q: 'refinedstorage:quartz_enriched_iron',
        R: 'minecraft:redstone',
        P: 'create:precision_mechanism'
    }).id('arcadia:rs_autocrafter');

    // --- RS: Wireless Transmitter needs ender + brass ---
    event.remove({ output: 'refinedstorage:wireless_transmitter' });
    event.shaped('refinedstorage:wireless_transmitter', [
        ' E ',
        'BQB',
        ' R '
    ], {
        E: 'minecraft:ender_pearl',
        B: 'create:brass_ingot',
        Q: 'refinedstorage:quartz_enriched_iron',
        R: 'minecraft:redstone_block'
    }).id('arcadia:rs_wireless_transmitter');

    // Sophisticatedbackpacks: vanilla recipes restored (custom overrides removed).

    // --- Building Gadgets: Gadget needs Create + Mek ---
    event.remove({ output: 'buildinggadgets2:gadget_building' });
    event.shaped('buildinggadgets2:gadget_building', [
        'SPS',
        'BRB',
        'SIS'
    ], {
        S: IRON_SHEET,
        P: 'create:precision_mechanism',
        B: 'create:brass_ingot',
        R: 'minecraft:redstone_block',
        I: 'mekanism:alloy_infused'
    }).id('arcadia:gadget_building');

    // --- Building Gadgets: Copy Paste needs more ---
    event.remove({ output: 'buildinggadgets2:gadget_copy_paste' });
    event.shaped('buildinggadgets2:gadget_copy_paste', [
        'SPS',
        'BRB',
        'SES'
    ], {
        S: IRON_SHEET,
        P: 'create:precision_mechanism',
        B: 'create:brass_ingot',
        R: 'minecraft:redstone_block',
        E: 'minecraft:ender_pearl'
    }).id('arcadia:gadget_copy_paste');

    // --- Building Gadgets: Cut Paste needs even more ---
    event.remove({ output: 'buildinggadgets2:gadget_cut_paste' });
    event.shaped('buildinggadgets2:gadget_cut_paste', [
        'SPS',
        'DRD',
        'SES'
    ], {
        S: IRON_SHEET,
        P: 'create:precision_mechanism',
        D: 'minecraft:diamond',
        R: 'minecraft:redstone_block',
        E: 'minecraft:ender_pearl'
    }).id('arcadia:gadget_cut_paste');

    // --- Building Gadgets: Destruction needs diamond + steel ---
    event.remove({ output: 'buildinggadgets2:gadget_destruction' });
    event.shaped('buildinggadgets2:gadget_destruction', [
        'DPD',
        'TRT',
        'DED'
    ], {
        D: 'minecraft:diamond',
        P: 'create:precision_mechanism',
        T: 'tfmg:steel_ingot',
        R: 'minecraft:redstone_block',
        E: 'minecraft:ender_pearl'
    }).id('arcadia:gadget_destruction');

    // --- Spyglass: Create brass ---
    event.remove({ output: 'minecraft:spyglass' });
    event.shaped('minecraft:spyglass', [
        ' A ',
        ' B ',
        ' B '
    ], {
        A: 'minecraft:amethyst_shard',
        B: 'create:brass_ingot'
    }).id('arcadia:spyglass');

    // --- Clock: Create cogwheel ---
    // Sequenced Assembly is excluded: KubeJS treats every entry of the "results" list as an
    // output, so a plain output filter also deletes recipes where the clock is only a random
    // by-product (create:sequenced_assembly/precision_mechanism).
    event.remove({ output: 'minecraft:clock', not: { type: 'create:sequenced_assembly' } });
    event.shaped('minecraft:clock', [
        ' G ',
        'GCG',
        ' G '
    ], {
        G: 'minecraft:gold_ingot',
        C: COGWHEEL
    }).id('arcadia:clock');

    // --- Compass: Create cogwheel ---
    // Same exclusion as the clock above: the compass is a by-product of
    // create_connected:sequenced_assembly/control_chip, and removing that recipe made the
    // Control Chip, and therefore the Sequenced Pulse Generator, uncraftable (ticket #250).
    event.remove({ output: 'minecraft:compass', not: { type: 'create:sequenced_assembly' } });
    event.shaped('minecraft:compass', [
        ' I ',
        'ICR',
        ' I '
    ], {
        I: 'minecraft:iron_ingot',
        C: COGWHEEL,
        R: 'minecraft:redstone'
    }).id('arcadia:compass');

    // --- Nature's Compass: Expensive exploration tool ---
    event.remove({ output: 'naturescompass:naturescompass' });
    event.recipes.create.mechanical_crafting(
        'naturescompass:naturescompass',
        [
            " LSL ",
            "LACAL",
            "SCPCS",
            "LACAL",
            " LSL "
        ], {
            L: '#minecraft:logs',
            S: '#minecraft:saplings',
            A: 'ars_nouveau:source_gem',
            C: 'minecraft:compass',
            P: 'create:precision_mechanism'
        }
    ).id('arcadia:natures_compass');

    // ============================================================
    // 12. BRIDGE COMPONENTS (cross-mod gate items)
    //     Used by sections 13-29 to harden mid/late-game crafts.
    // ============================================================


    // 12A. ARCANE CIRCUIT (Create + TFMG + Mekanism + Ars Nouveau)
    // MEDIUM tier bridge. Required by mid-game electronics and magic devices.
    event.recipes.create.mixing(
        ARCANE_CIRCUIT,
        [
            '2x create:precision_mechanism',
            '2x ' + SOURCE_GEM,
            '2x tfmg:transistor_item',
            MEK_ALLOY_INFUSED,
            Fluid.of('tfmg:creosote', 500)
        ]
    ).heated().id('arcadia:arcane_circuit');

    // 12B. ETHEREAL ALLOY (Ars + Mekanism + Occultism + Create)
    // HARD tier bridge. Required by soul-bound items.
    event.recipes.create.mixing(
        ETHEREAL_ALLOY,
        [
            '4x ' + SOURCE_GEM,
            '2x ' + MEK_ALLOY_REINFORCED,
            'occultism:spirit_attuned_gem',
            '2x ' + BRASS_SHEET,
            Fluid.of('minecraft:lava', 1000)
        ]
    ).heated().id('arcadia:ethereal_alloy');

    // 12C. INDUSTRIAL HEART (Create + TFMG + Mekanism + Immersive Engineering)
    // HARD tier bridge. Required by heavy industrial machinery.
    event.recipes.create.sequenced_assembly(
        [Item.of(INDUSTRIAL_HEART, 1)],
        TFMG_HEAVY_PLATE,
        [
            event.recipes.createDeploying('arcadia:incomplete_industrial_heart', ['arcadia:incomplete_industrial_heart', TFMG_STEEL_MECHANISM]),
            event.recipes.createDeploying('arcadia:incomplete_industrial_heart', ['arcadia:incomplete_industrial_heart', 'create:precision_mechanism']),
            event.recipes.createDeploying('arcadia:incomplete_industrial_heart', ['arcadia:incomplete_industrial_heart', MEK_ALLOY_REINFORCED]),
            event.recipes.createDeploying('arcadia:incomplete_industrial_heart', ['arcadia:incomplete_industrial_heart', IE_COMPONENT_STEEL]),
            event.recipes.createPressing('arcadia:incomplete_industrial_heart', 'arcadia:incomplete_industrial_heart')
        ]
    ).transitionalItem('arcadia:incomplete_industrial_heart').loops(4).id('arcadia:industrial_heart');

    // 12D. RUNE MATRIX (Ars + Occult + Create + Apotheosis)
    // ENDGAME tier bridge. Required by archmage-tier items and Apotheosis sockets.
    event.recipes.create.mechanical_crafting(
        RUNE_MATRIX,
        [
            "GMAMG",
            "MACAM",
            "ACECA",
            "MACAM",
            "GMAMG"
        ], {
            G: SOURCE_GEM_BLOCK,
            M: MAGEBLOOM_CLOTH,
            A: ARCANE_CIRCUIT,
            C: 'apotheosis:rare_material',
            E: 'minecraft:echo_shard'
        }
    ).id('arcadia:rune_matrix');

});
