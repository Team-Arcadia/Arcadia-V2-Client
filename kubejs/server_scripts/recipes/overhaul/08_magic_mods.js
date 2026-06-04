// Priority: 100

/*
    Arcadia V2 — Recipe Overhaul: Magic Mods — Ars Nouveau, Ars Creo/Technica, Iron's Spellbooks, Occultism

    Magic mod component hardening: spell foci, scribes tools, alchemy cauldrons, occult fundaments — all touched by Create / cross-mod bridges.

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


    console.info("[Arcadia V2] Loading recipe overhaul: 08_magic_mods.js...");

    // ============================================================
    // 22. ARS NOUVEAU EXTRAS HARDENING
    // ============================================================

    event.remove({ output: 'ars_nouveau:apprentice_spell_book' });
    event.shaped('ars_nouveau:apprentice_spell_book', ['MAM', 'NGN', 'MPM'], {
        M: MAGEBLOOM_CLOTH,
        A: ARCANE_CIRCUIT,
        N: SOURCE_GEM_BLOCK,
        G: 'ars_nouveau:novice_spell_book',
        P: 'create:precision_mechanism'
    }).id('arcadia:ars_apprentice_spellbook');

    event.remove({ output: 'ars_nouveau:archmage_spell_book' });
    event.recipes.create.mechanical_crafting(
        'ars_nouveau:archmage_spell_book',
        [
            "SAS",
            "ARA",
            "SAS"
        ], {
            S: SOURCE_GEM_BLOCK,
            A: MAGEBLOOM_CLOTH,
            R: RUNE_MATRIX
        }
    ).id('arcadia:ars_archmage_spellbook');

    event.remove({ output: 'ars_nouveau:enchanters_sword' });
    event.shaped('ars_nouveau:enchanters_sword', [' S ', ' S ', ' P '], {
        S: SOURCE_GEM_BLOCK,
        P: REINFORCE_BLOCK
    }).id('arcadia:ars_enchanters_sword');

    event.remove({ output: 'ars_nouveau:enchanters_shield' });
    event.shaped('ars_nouveau:enchanters_shield', ['SGS', 'SPS', ' S '], {
        S: SOURCE_GEM_BLOCK,
        G: ETHEREAL_ALLOY,
        P: 'create:precision_mechanism'
    }).id('arcadia:ars_enchanters_shield');

    event.remove({ output: 'ars_nouveau:enchanters_mirror' });
    event.shaped('ars_nouveau:enchanters_mirror', [' E ', 'SRS', ' P '], {
        E: 'minecraft:ender_eye',
        S: SOURCE_GEM_BLOCK,
        R: RUNE_MATRIX,
        P: 'create:precision_mechanism'
    }).id('arcadia:ars_enchanters_mirror');

    event.remove({ output: 'ars_nouveau:mob_jar' });
    event.shaped('ars_nouveau:mob_jar', ['GBG', 'EPE', 'GBG'], {
        G: 'minecraft:glass',
        B: 'create:brass_casing',
        E: ETHEREAL_ALLOY,
        P: 'create:precision_mechanism'
    }).id('arcadia:ars_mob_jar');

    event.remove({ output: 'ars_nouveau:alteration_table' });
    event.shaped('ars_nouveau:alteration_table', ['MAM', 'SFS', 'LLL'], {
        M: MAGEBLOOM_CLOTH,
        A: 'minecraft:feather',
        S: SOURCE_GEM,
        F: RUNE_MATRIX,
        L: ARCHWOOD
    }).id('arcadia:ars_alteration_table');

    event.remove({ output: 'ars_nouveau:agronomic_sourcelink' });
    event.shaped('ars_nouveau:agronomic_sourcelink', ['SAS', 'WCW', 'LLL'], {
        S: SOURCE_GEM_BLOCK,
        A: ARCHWOOD,
        W: 'minecraft:wheat',
        C: 'create:brass_casing',
        L: ARCHWOOD
    }).id('arcadia:ars_agronomic_sourcelink');

    // ============================================================
    // 23. ARS CREO / ARS TECHNICA HARDENING
    //     kinetic_sourcelink/source_crafter/source_mixer do not exist in these addon versions.
    //     Ars Creo adds starbuncle_wheel only; Ars Technica adds source_motor + armor sets.
    // ============================================================

    // ============================================================
    // 24. IRON'S SPELLBOOKS HARDENING
    // ============================================================

    event.remove({ output: 'irons_spellbooks:netherite_spell_book' });
    event.recipes.create.mechanical_crafting(
        'irons_spellbooks:netherite_spell_book',
        [
            "NAN",
            "DRD",
            "NPN"
        ], {
            N: 'minecraft:netherite_ingot',
            A: MEK_ALLOY_ATOMIC,
            D: 'irons_spellbooks:diamond_spell_book',
            R: RUNE_MATRIX,
            P: 'create:precision_mechanism'
        }
    ).id('arcadia:is_netherite_spellbook');

    event.remove({ output: 'irons_spellbooks:dragonskin_spell_book' });
    event.shaped('irons_spellbooks:dragonskin_spell_book', ['SNS', 'NRN', 'SNS'], {
        S: SOURCE_GEM_BLOCK,
        N: 'irons_spellbooks:netherite_spell_book',
        R: RUNE_MATRIX
    }).id('arcadia:is_dragonskin_spellbook');

    const archevokerArmor = [
        'irons_spellbooks:archevoker_helmet',
        'irons_spellbooks:archevoker_chestplate',
        'irons_spellbooks:archevoker_leggings',
        'irons_spellbooks:archevoker_boots'
    ];
    archevokerArmor.forEach(item => event.replaceInput({ output: item, allowEmpty: true }, 'irons_spellbooks:arcane_ingot', ETHEREAL_ALLOY));

    // ============================================================
    // 25. OCCULTISM HARDENING
    // ============================================================

    event.remove({ output: 'occultism:divination_rod' });
    event.shaped('occultism:divination_rod', [' GA', ' SG', 'S  '], {
        G: GOLD_SHEET,
        A: ARCANE_CIRCUIT,
        S: 'minecraft:stick'
    }).id('arcadia:occultism_divination_rod');

    event.remove({ output: 'occultism:infused_pickaxe' });
    event.shaped('occultism:infused_pickaxe', ['EEE', ' S ', ' S '], {
        E: ETHEREAL_ALLOY,
        S: REINFORCE_BLOCK
    }).id('arcadia:occultism_infused_pickaxe');

    event.remove({ output: 'occultism:otherworld_goggles' });
    event.shaped('occultism:otherworld_goggles', ['EGE', 'SES', ' O '], {
        E: ETHEREAL_ALLOY,
        G: GOLD_SHEET,
        S: SOURCE_GEM,
        O: 'minecraft:obsidian'
    }).id('arcadia:occultism_goggles');

    // soul_gem_empty is obtained via Djinni ritual only — not craftable, skipped.

    // ============================================================
    // 26. SIMPLY SWORDS HARDENING
    // ============================================================

    // Runic Grimoire (Patchouli guide book) ships with no recipe — add a thematic one.
    // Book + Runic Tablet (the mod's signature crafting item) -> the guide.
    // Patchouli guide books are produced by patchouli:guide_book carrying the
    // patchouli:book data component; KubeJS shapeless drops the component, so emit raw JSON.
    event.custom({
        type: 'minecraft:crafting_shapeless',
        category: 'misc',
        ingredients: [
            { item: 'minecraft:book' },
            { item: 'simplyswords:runic_tablet' }
        ],
        result: {
            id: 'patchouli:guide_book',
            components: {
                'patchouli:book': 'simplyswords:runic_grimoire'
            }
        }
    }).id('arcadia:simplyswords_runic_grimoire');

});
