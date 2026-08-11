// Priority: 500
/*
    STELLAR FORGE — Boss drop refining line
    Requires: Create, Occultism

    The Occultism Dimensional Battlefield hands out fragments instead of finished boss
    drops: its two custom tables are overridden in
    kubejs/data/occultism/loot_table/battlefield/minecraft/. This line turns the fragments
    back into the real thing, so the automated route costs an assembly line while the boss
    fight itself stays untouched.

    Fragment accounting: 1 fragment as the assembly base + 1 deployed per loop.
    With 3 loops that is 4 fragments per output, about 33 minutes of battlefield uptime
    on a single block at the current butcherLifeMultiplier.
*/

ServerEvents.recipes(event => {

    // ============================================================
    //  NETHER STAR — 4x arcadia:star_fragment
    // ============================================================
    event.recipes.create.sequenced_assembly(
        [Item.of('minecraft:nether_star', 1)],
        'arcadia:star_fragment',
        [
            event.recipes.createDeploying('arcadia:incomplete_nether_star', ['arcadia:incomplete_nether_star', 'arcadia:star_fragment']),
            event.recipes.createPressing('arcadia:incomplete_nether_star', 'arcadia:incomplete_nether_star'),
            event.recipes.createFilling('arcadia:incomplete_nether_star', ['arcadia:incomplete_nether_star', Fluid.of('minecraft:lava', 250)]),
            event.recipes.createPressing('arcadia:incomplete_nether_star', 'arcadia:incomplete_nether_star')
        ]
    ).transitionalItem('arcadia:incomplete_nether_star').loops(3).id('arcadia:nether_star_from_fragments');

    // ============================================================
    //  DRAGON EGG — 4x arcadia:dragon_shard
    // ============================================================
    event.recipes.create.sequenced_assembly(
        [Item.of('minecraft:dragon_egg', 1)],
        'arcadia:dragon_shard',
        [
            event.recipes.createDeploying('arcadia:incomplete_dragon_egg', ['arcadia:incomplete_dragon_egg', 'arcadia:dragon_shard']),
            event.recipes.createPressing('arcadia:incomplete_dragon_egg', 'arcadia:incomplete_dragon_egg'),
            event.recipes.createCutting('arcadia:incomplete_dragon_egg', 'arcadia:incomplete_dragon_egg'),
            event.recipes.createPressing('arcadia:incomplete_dragon_egg', 'arcadia:incomplete_dragon_egg')
        ]
    ).transitionalItem('arcadia:incomplete_dragon_egg').loops(3).id('arcadia:dragon_egg_from_shards');

    console.info('[Arcadia V2] Stellar Forge chain loaded: 4 fragments per boss drop.');
});
