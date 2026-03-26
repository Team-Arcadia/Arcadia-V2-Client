// Priority: 10
/*
    Global Tags for Item Sorting & Organization (Refined)
    Adds standard and descriptive tags to various items.
    Author: vyrriox
*/

ServerEvents.tags('item', event => {
    // 1. Netherite & Valuables
    event.add('c:netherite_scraps', 'minecraft:netherite_scrap');
    event.add('c:smithing_templates', 'minecraft:netherite_upgrade_smithing_template');
    event.add('c:valuables', [
        'minecraft:netherite_scrap',
        'minecraft:totem_of_undying',
        'minecraft:ender_eye',
        'minecraft:netherite_upgrade_smithing_template'
    ]);

    // 2. Ender
    event.add('c:ender_eyes', 'minecraft:ender_eye');

    // 3. Minerals & Flint
    event.add('c:flints', 'minecraft:flint');
    event.add('c:smooth_basalts', 'minecraft:smooth_basalt');

    // 4. Flora
    event.add('c:kelps', 'minecraft:kelp');
    event.add('c:grasses', ['minecraft:short_grass', 'minecraft:tall_grass']);

    // 5. Mob Drops (Specific)
    event.add('c:mob_drops/magma', 'minecraft:magma_cream');
    event.add('c:mob_drops/blaze', 'minecraft:blaze_powder');
    event.add('c:mob_drops/phantom', 'minecraft:phantom_membrane');

    // 6. Projectiles
    event.add('c:projectiles/fire', 'minecraft:fire_charge');
    event.add('c:projectiles/wind', 'minecraft:wind_charge');

    // 7. Utility & Tools
    event.add('c:honeycombs', 'minecraft:honeycomb');
    event.add('c:glistering_melons', 'minecraft:glistering_melon_slice');
    event.add('c:experience_bottles', 'minecraft:experience_bottle');
    event.add('c:name_tags', 'minecraft:name_tag');
    event.add('c:trial_keys', 'minecraft:trial_key');
    event.add('c:totems', 'minecraft:totem_of_undying');

    // 8. End & Sculk
    event.add('c:saddles', 'minecraft:saddle');
    event.add('c:sculk', ['minecraft:sculk', 'minecraft:sculk_catalyst', 'minecraft:sculk_shrieker', 'minecraft:sculk_vein']);
    event.add('c:sculk_sensors', 'minecraft:sculk_sensor');
    event.add('c:shulker_shells', 'minecraft:shulker_shell');
    event.add('c:popped_chorus_fruits', 'minecraft:popped_chorus_fruit');
    event.add('c:end_rods', 'minecraft:end_rod');
    event.add('c:echo_shards', 'minecraft:echo_shard');
    event.add('c:respawn_anchors', 'minecraft:respawn_anchor');

    // 9. Brewing & Misc
    event.add('c:fermented_spider_eyes', 'minecraft:fermented_spider_eye');
    event.add('c:hoppers', 'minecraft:hopper');

    // 10. Currency (Dusty Decorations)
    event.add('c:currencies/gold_coins', 'dustydecorations:scattered_gold_coins');

    // 11. Redstone & Pistons
    event.add('c:pistons', ['minecraft:sticky_piston', 'minecraft:piston']);
    event.add('c:levers', 'minecraft:lever');
    event.add('c:redstone_components', [
        'minecraft:comparator',
        'minecraft:repeater'
    ]);
    event.add('c:redstone_devices', [
        'minecraft:piston',
        'minecraft:sticky_piston',
        'minecraft:lever',
        'minecraft:comparator',
        'minecraft:repeater'
    ]);
});

console.info("[Arcadia V2] Global Tags Refined: Standardized tags applied.");
