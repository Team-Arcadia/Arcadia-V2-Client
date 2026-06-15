// Priority: 90

/*
    Arcadia V2 — Recipe Overhaul: Steel Arbitrage Lockdown

    Closes the cross-mod steel "laundering" loop. TFMG and Create Nuclear shipped
    their nugget/ingot/block (de)compacting recipes keyed on the GENERIC tags
    (c:ingots/steel, c:nuggets/steel, c:storage_blocks/steel) while outputting
    their OWN steel item. That let any mod's steel be converted into TFMG / CN
    steel for free, bypassing the intended TFMG (blast furnace / molten steel)
    and CN production chains.

    Fix: rewrite each offending recipe to require that mod's OWN item as input,
    mirroring how Immersive Engineering and Mekanism already gate their steel.
    Legitimate processing (dust->ingot smelting, crusher, IE blast furnace,
    TFMG casting) is left untouched.

    Create Nuclear's create:mixing steel (1 coal dust + 1 iron -> 1 steel ingot)
    is hardened rather than removed: now requires more inputs and heat.

    Author: vyrriox
*/

ServerEvents.recipes((event) => {
    console.info("[Arcadia V2] Loading recipe overhaul: 10_steel_arbitrage.js...");

    // --- Steel item ids ---
    const TFMG_INGOT = "tfmg:steel_ingot";
    const TFMG_NUGGET = "tfmg:steel_nugget";
    const TFMG_BLOCK = "tfmg:steel_block";

    const CN_INGOT = "createnuclear:steel_ingot";
    const CN_NUGGET = "createnuclear:steel_nugget";
    const CN_BLOCK = "createnuclear:steel_block";

    // ============================================================
    // 1. TFMG — lock (de)compacting to TFMG's own steel
    // ============================================================
    // Original recipes used generic c:* tags as input -> laundering vector.
    [
        "tfmg:crafting/materials/steel_ingot_from_compacting",
        "tfmg:crafting/materials/steel_ingot_from_decompacting",
        "tfmg:crafting/materials/steel_nugget_from_decompacting",
        "tfmg:crafting/materials/steel_block_from_compacting",
    ].forEach((id) => event.remove({ id: id }));

    // 9 TFMG nuggets -> 1 TFMG ingot
    event.shaped(TFMG_INGOT, ["###", "###", "###"], { "#": TFMG_NUGGET })
        .id("arcadia:steel/tfmg_ingot_from_nuggets");

    // 1 TFMG block -> 9 TFMG ingots
    event.shapeless(Item.of(TFMG_INGOT, 9), [TFMG_BLOCK])
        .id("arcadia:steel/tfmg_ingot_from_block");

    // 1 TFMG ingot -> 9 TFMG nuggets
    event.shapeless(Item.of(TFMG_NUGGET, 9), [TFMG_INGOT])
        .id("arcadia:steel/tfmg_nugget_from_ingot");

    // 9 TFMG ingots -> 1 TFMG block
    event.shaped(TFMG_BLOCK, ["###", "###", "###"], { "#": TFMG_INGOT })
        .id("arcadia:steel/tfmg_block_from_ingots");

    // ============================================================
    // 2. CREATE NUCLEAR — lock (de)compacting to CN's own steel
    // ============================================================
    // CN ships these recipes TWICE (crafting/crafting/* and crafting/*).
    // Remove both copies.
    [
        "createnuclear:crafting/crafting/steel_ingot_from_compacting",
        "createnuclear:crafting/crafting/steel_ingot_from_decompacting",
        "createnuclear:crafting/crafting/steel_nugget_from_decompacting",
        "createnuclear:crafting/crafting/steel_block_from_compacting",
        "createnuclear:crafting/steel_ingot_from_decompacting",
        "createnuclear:crafting/steel_nugget_from_decompacting",
    ].forEach((id) => event.remove({ id: id }));

    // 9 CN nuggets -> 1 CN ingot
    event.shaped(CN_INGOT, ["###", "###", "###"], { "#": CN_NUGGET })
        .id("arcadia:steel/cn_ingot_from_nuggets");

    // 1 CN block -> 9 CN ingots
    event.shapeless(Item.of(CN_INGOT, 9), [CN_BLOCK])
        .id("arcadia:steel/cn_ingot_from_block");

    // 1 CN ingot -> 9 CN nuggets
    event.shapeless(Item.of(CN_NUGGET, 9), [CN_INGOT])
        .id("arcadia:steel/cn_nugget_from_ingot");

    // 9 CN ingots -> 1 CN block
    event.shaped(CN_BLOCK, ["###", "###", "###"], { "#": CN_INGOT })
        .id("arcadia:steel/cn_block_from_ingots");

    // ============================================================
    // 3. CREATE NUCLEAR — harden the cheap mixing steel
    // ============================================================
    // Was: 1 coal dust + 1 iron ingot -> 1 CN steel ingot (trivial steel).
    // Now: heated, 4 coal dust + 2 iron ingots -> 1 CN steel ingot.
    event.remove({ id: "createnuclear:mixing/steel" });
    // NOTE: counted tag ingredients MUST use Ingredient.of('#tag', count).
    // The "Nx #tag" string form does not parse the count for tags here and
    // yields an empty ingredient (recipe never matches, empty JEI slots).
    event.recipes.create
        .mixing(CN_INGOT, [
            Ingredient.of("#c:dusts/coal", 4),
            Ingredient.of("#c:ingots/iron", 2),
        ])
        .heated()
        .id("arcadia:steel/cn_mixing_hardened");

    // ============================================================
    // NOTE — intentionally NOT touched (legitimate processing):
    //   - immersiveengineering blast_furnace (iron -> steel)
    //   - immersiveengineering / mekanism dust -> ingot smelting/blasting
    //   - mekanism / IE crusher/crushing (ingot -> dust)
    //   - tfmg casting (molten_steel -> ingot)
    //   - mekanism & IE nugget/ingot/block recipes (already require own item)
    // ============================================================
});
