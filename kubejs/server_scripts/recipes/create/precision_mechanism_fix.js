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

    // Recreate identical to Create's default but using create:golden_sheet directly
    event.recipes.create.sequenced_assembly(
        [
            CreateItem.of('create:precision_mechanism', 120.0),
            CreateItem.of('create:golden_sheet', 8.0),
            CreateItem.of('create:andesite_alloy', 8.0),
            CreateItem.of('create:cogwheel', 5.0),
            CreateItem.of('minecraft:gold_nugget', 3.0),
            CreateItem.of('create:shaft', 2.0),
            CreateItem.of('create:crushed_raw_gold', 2.0),
            'minecraft:iron_ingot',
            'minecraft:clock'
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
