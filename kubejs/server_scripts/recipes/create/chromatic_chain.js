// Priority: 15
/*
    CHROMATIC CHAIN RESTORATION — Create 6.0.10

    Create 6.0.10 still registers Chromatic Compound, Refined Radiance, Shadow Steel and their
    two casings, and it still ships the in-world conversion code
    (com.simibubi.create.content.legacy.ChromaticCompoundItem) plus its three server config
    switches (enableRefinedRadianceRecipe, enableShadowSteelRecipe,
    lightSourceCountForRefinedRadiance). Only the datapack side was dropped: the jar contains
    no recipe producing create:chromatic_compound, create:shadow_steel_casing or
    create:refined_radiance_casing.

    Consequence in Arcadia V2 (ticket #269): Create Encased ships 44 machine recipes that
    consume those two casings, so every Shadow Steel and Refined Radiance variant was
    unobtainable. Across all 443 jars, the only source of a Chromatic Compound was the
    create_easy_structures epic chest loot table.

    This script re-opens the whole chain:
      1. Chromatic Compound      superheated Mixing, Create's legacy ingredient pair
      2. Refined Radiance        superheated Mixing with glowstone (in-world light path kept)
      3. Shadow Steel            Haunting (in-world void path kept)
      4. Shadow / Radiant Casing Item Application on a Brass Casing, mirroring Create's own
                                 railway_casing recipe (brass casing + obsidian plate)

    Author: vyrriox
*/

ServerEvents.recipes(event => {

    // ============================================================
    //  1. CHROMATIC COMPOUND
    //  Cinder Flour (crushing netherrack) + Powdered Obsidian
    //  (crushing obsidian) in a superheated basin -> 1 compound.
    //  Both inputs are reachable in Arcadia V2; superheating needs a
    //  Blaze Cake, itself gated behind Cinder Flour.
    // ============================================================
    event.recipes.create.mixing(
        'create:chromatic_compound',
        [
            'create:cinder_flour',
            'create:powdered_obsidian'
        ]
    ).superheated().id('arcadia:chromatic_compound');

    // ============================================================
    //  2 & 3. REFINED RADIANCE / SHADOW STEEL
    //  Create still converts a dropped compound in-world (it eats
    //  lightSourceCountForRefinedRadiance light sources, or falls below
    //  the world floor), and both paths stay enabled in
    //  config/create-server.toml. Neither shows up in JEI, and the void
    //  path is out of reach on the servers, so players reported both
    //  items as uncraftable. These two recipes give a visible,
    //  automatable route; the in-world conversion still works on top.
    //    - Refined Radiance: superheated Mixing with glowstone, the
    //      light that the in-world recipe feeds on.
    //    - Shadow Steel: Haunting (fan through soul fire), the shadow
    //      counterpart of the void fall.
    // ============================================================
    event.recipes.create.mixing(
        'create:refined_radiance',
        [
            'create:chromatic_compound',
            '2x minecraft:glowstone'
        ]
    ).superheated().id('arcadia:refined_radiance');

    event.recipes.create.haunting(
        'create:shadow_steel',
        'create:chromatic_compound'
    ).id('arcadia:shadow_steel');

    // ============================================================
    //  4. CASINGS
    //  Item Application on a placed Brass Casing, same shape as
    //  create:item_application/railway_casing. Deployer-automatable,
    //  and consistent with how every other Create casing is made.
    // ============================================================
    event.recipes.create.item_application(
        'create:shadow_steel_casing',
        ['create:brass_casing', 'create:shadow_steel']
    ).id('arcadia:shadow_steel_casing');

    event.recipes.create.item_application(
        'create:refined_radiance_casing',
        ['create:brass_casing', 'create:refined_radiance']
    ).id('arcadia:refined_radiance_casing');

    console.info('[Arcadia V2] Chromatic chain restored: compound, radiance, shadow steel + casings.');
});
