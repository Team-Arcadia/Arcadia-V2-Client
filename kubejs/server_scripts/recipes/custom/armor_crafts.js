// Priority: 500
/*
    Crafting recipes for Adept & Heretic armor sets.
    Adept: Dark cultist robes — amethyst + leather + purple wool
    Heretic: Rebel cult armor — echo shards + chains + bone + red wool
    Author: vyrriox
*/

ServerEvents.recipes(event => {

    // ===== ADEPT ARMOR SET =====
    // Theme: ritualistic, uses amethyst, candles, purple dye, leather

    event.shaped('arcadia:adept_helmet', [
        'APA',
        'P P'
    ], {
        A: 'minecraft:amethyst_shard',
        P: 'minecraft:purple_wool'
    }).id('arcadia:adept_helmet');

    event.shaped('arcadia:adept_chestplate', [
        'P P',
        'APA',
        'LPL'
    ], {
        A: 'minecraft:amethyst_shard',
        P: 'minecraft:purple_wool',
        L: 'minecraft:leather'
    }).id('arcadia:adept_chestplate');

    event.shaped('arcadia:adept_leggings', [
        'APA',
        'L L',
        'P P'
    ], {
        A: 'minecraft:amethyst_shard',
        P: 'minecraft:purple_wool',
        L: 'minecraft:leather'
    }).id('arcadia:adept_leggings');

    event.shaped('arcadia:adept_boots', [
        'A A',
        'P P'
    ], {
        A: 'minecraft:amethyst_shard',
        P: 'minecraft:purple_wool'
    }).id('arcadia:adept_boots');

    // ===== HERETIC ARMOR SET =====
    // Theme: bloody, uses echo shards, chains, bone, red wool

    event.shaped('arcadia:heretic_helmet', [
        'ERE',
        'B B'
    ], {
        E: 'minecraft:echo_shard',
        R: 'minecraft:red_wool',
        B: 'minecraft:bone'
    }).id('arcadia:heretic_helmet');

    event.shaped('arcadia:heretic_chestplate', [
        'R R',
        'ECE',
        'RER'
    ], {
        E: 'minecraft:echo_shard',
        R: 'minecraft:red_wool',
        C: 'minecraft:chain'
    }).id('arcadia:heretic_chestplate');

    event.shaped('arcadia:heretic_leggings', [
        'ERE',
        'C C',
        'R R'
    ], {
        E: 'minecraft:echo_shard',
        R: 'minecraft:red_wool',
        C: 'minecraft:chain'
    }).id('arcadia:heretic_leggings');

    event.shaped('arcadia:heretic_boots', [
        'E E',
        'R R'
    ], {
        E: 'minecraft:echo_shard',
        R: 'minecraft:red_wool'
    }).id('arcadia:heretic_boots');

    console.log('[Arcadia] Adept & Heretic armor recipes loaded');
});
