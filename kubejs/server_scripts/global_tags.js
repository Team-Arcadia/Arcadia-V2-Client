// Priority: 10
/*
    Global Tags for Item Sorting & Organization
    Adds common and custom tags to various items to facilitate sorting in storage systems.
    Author: vyrriox
*/

ServerEvents.tags('item', event => {
    // 1. Netherite
    event.add('c:netherite', [
        'minecraft:netherite_scrap',
        'minecraft:netherite_upgrade_smithing_template'
    ]);

    // 2. Ender
    event.add('c:ender', 'minecraft:ender_eye');

    // 3. Flint
    event.add('c:flint', 'minecraft:flint');

    // 4. Kelp
    event.add('c:kelp', 'minecraft:kelp');

    // 5. Mob Drops
    event.add('c:mob_drops', [
        'minecraft:magma_cream',
        'minecraft:blaze_powder',
        'minecraft:phantom_membrane'
    ]);

    // 6. Projectiles
    event.add('c:projectiles', [
        'minecraft:fire_charge',
        'minecraft:wind_charge'
    ]);

    // 7. Grasses
    event.add('c:grasses', [
        'minecraft:short_grass',
        'minecraft:tall_grass'
    ]);

    // 8. Honeycomb
    event.add('c:honeycomb', 'minecraft:honeycomb');

    // 9. Glistering Melon
    event.add('c:glistering_melon', 'minecraft:glistering_melon_slice');

    // 10. Magic & Valuable
    event.add('c:magic', [
        'minecraft:experience_bottle',
        'minecraft:totem_of_undying'
    ]);

    // 11. Utility
    event.add('c:utility', [
        'minecraft:name_tag',
        'minecraft:trial_key'
    ]);

    // 12. Smooth Basalt
    event.add('c:smooth_basalt', 'minecraft:smooth_basalt');

    // 13. Currency
    event.add('c:currency', 'dustydecorations:scattered_gold_coins');
    event.add('arcadia:is_item', 'dustydecorations:scattered_gold_coins'); // Grouping with other custom items

    // 14. Redstone Components
    event.add('c:redstone_components', [
        'minecraft:sticky_piston',
        'minecraft:piston',
        'minecraft:lever',
        'minecraft:comparator',
        'minecraft:repeater'
    ]);

    // 15. General Grouping (requested by user)
    event.add('arcadia:is_item', [
        'minecraft:netherite_scrap',
        'minecraft:ender_eye',
        'minecraft:flint',
        'minecraft:kelp',
        'minecraft:magma_cream',
        'minecraft:blaze_powder',
        'minecraft:fire_charge',
        'minecraft:phantom_membrane',
        'minecraft:wind_charge',
        'minecraft:short_grass',
        'minecraft:tall_grass',
        'minecraft:honeycomb',
        'minecraft:glistering_melon_slice',
        'minecraft:experience_bottle',
        'minecraft:name_tag',
        'minecraft:trial_key',
        'minecraft:netherite_upgrade_smithing_template',
        'minecraft:totem_of_undying',
        'minecraft:smooth_basalt',
        'minecraft:sticky_piston',
        'minecraft:piston',
        'minecraft:lever',
        'minecraft:comparator',
        'minecraft:repeater'
    ]);
});

console.info("[Arcadia V2] Global Tags for Sorting Loaded Successfully.");
