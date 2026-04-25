// Priority: 15
/*
    Fix for Create 6.0.10 Precision Mechanism recipe loading bug.
    Upstream issue: https://github.com/Creators-of-Create/Create/issues/10203
    The Either-codec in Create 6.0.10 mis-parses tag-based ingredients as fluid ingredients,
    causing the default precision_mechanism Sequenced Assembly to fail silently.
    This script recreates the recipe using direct item references (no tag).
    Author: vyrriox
*/

ServerEvents.recipes(event => {
    // Remove any stale/broken registration (no-op if absent)
    event.remove({ id: 'create:sequenced_assembly/precision_mechanism' });
    event.remove({ output: 'create:precision_mechanism' });

    const incomplete = 'create:incomplete_precision_mechanism';

    // Recreate identical to Create's default but using create:golden_sheet directly.
    // KubeJS 7 CreateItem.of expects chance in 0.0-1.0 range (not the 0-100 scale used in
    // Create's native JSON). Primary output is guaranteed (1.0); bonuses keep original %.
    event.recipes.create.sequenced_assembly(
        [
            CreateItem.of('create:precision_mechanism', 1.0),
            CreateItem.of('create:golden_sheet', 0.08),
            CreateItem.of('create:andesite_alloy', 0.08),
            CreateItem.of('create:cogwheel', 0.05),
            CreateItem.of('minecraft:gold_nugget', 0.03),
            CreateItem.of('create:shaft', 0.02),
            CreateItem.of('create:crushed_raw_gold', 0.02)
        ],
        'create:golden_sheet',
        [
            event.recipes.createDeploying(incomplete, [incomplete, 'create:cogwheel']),
            event.recipes.createDeploying(incomplete, [incomplete, 'create:large_cogwheel']),
            event.recipes.createDeploying(incomplete, [incomplete, 'minecraft:iron_nugget'])
        ]
    ).transitionalItem(incomplete).loops(5).id('arcadia:precision_mechanism_fix');

    console.info('[Arcadia V2] Precision Mechanism recipe re-registered (Create 6.0.10 bug fix).');
});
