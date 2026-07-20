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
    event.add('c:ghast_tears', 'minecraft:ghast_tear');

    // 10. Currency (Dusty Decorations)
    event.add('c:currencies/gold_coins', 'dustydecorations:scattered_gold_coins');

    // 11. Bricks & Building
    event.add('c:end_stone_bricks', 'minecraft:end_stone_bricks');
    event.add('c:polished_blackstone_bricks', 'minecraft:polished_blackstone_bricks');
    event.add('c:prismarine_bricks', 'minecraft:prismarine_bricks');
    event.add('c:prismarine_shards', 'minecraft:prismarine_shard');

    // 12. Decoration & Containers
    event.add('c:flower_pots', 'minecraft:flower_pot');
    event.add('c:item_frames', 'minecraft:item_frame');

    // 13. Potions & Brewing
    event.add('c:magma_creams', 'minecraft:magma_cream');
    event.add('c:dragon_breaths', 'minecraft:dragon_breath');
    event.add('c:glass_bottles', 'minecraft:glass_bottle');

    // 14. Weapons
    event.add('c:bows', 'minecraft:bow');

    // 15. Redstone & Pistons
    event.add('c:observers', 'minecraft:observer');
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

// =============================================================================
// MOB FARM PROTECTION — Centralized Blacklist
// =============================================================================
// Applied to every mod-specific capture/farm mechanism in the modpack:
//   - Apothic Spawners (placing spawn egg into spawner)
//   - Ars Nouveau Drygmy (passive mob-drop farming)
//   - Ars Nouveau Jar (mob capture in jar)
//   - Ars Additions Source Spawner (passive spawner)
//   - Occultism Soul Gem (mob capture in gem)
//   - Supplementaries Bottle/Cage (mob capture)
//   - Carry On (carrying mob in hands)
//   - PneumaticCraft Vacuum Trap
//
// SYNC: a static mirror of this list lives in
//   kubejs/data/apothic_spawners/tags/entity_type/blacklisted_from_spawners.json
// (datapack fallback for Apothic Spawners if KubeJS fails to load). When you add or
// remove an entry here, update that file too — both must stay identical.
// =============================================================================
const ARCADIA_FARM_BLACKLIST = [
    // Animal Garden — passive animals (cosmetic, not for farms)
    'animalgarden_alligatorgar:alligatorgar',
    'animalgarden_bullshark:bullshark',
    'animalgarden_commonraven:commonraven',
    'animalgarden_fennecfox:fennecfox',
    'animalgarden_manatee:manatee',
    'animalgarden_meerkat:meerkat',
    'animalgarden_mouse:mouse',
    'animalgarden_porcupine:porcupine',
    'animalgarden_prairiedog:prairiedog',
    'animalgarden_redpanda:redpanda',
    'animalgarden_redpanda:himalayan_redpanda',
    'animalgarden_seaotter:seaotter',
    'animalgarden_spottedhyena:spottedhyena',
    'animalgarden_sugarglider:sugarglider',
    'animalgarden_westerngorilla:westerngorilla',
    'animalgarden_whiterhinoceros:whiterhinoceros',

    // Vanilla turtles + Aquaculture turtles (scute farms exploit)
    'minecraft:turtle',
    'aquaculture:arrau_turtle',
    'aquaculture:box_turtle',
    'aquaculture:starshell_turtle',

    // Crabber's Delight — crab drops crab_claw on death; spawner-farming floods the
    // server with thousands of claws. Block it from all capture/spawner mechanisms.
    'crabbersdelight:crab',

    // Bosses
    'minecraft:ender_dragon',
    'minecraft:wither',
    'twilightforest:naga',
    'twilightforest:lich',
    'twilightforest:minoshroom',
    'twilightforest:hydra',
    'twilightforest:knight_phantom',
    'twilightforest:ur_ghast',
    'twilightforest:yeti',
    'twilightforest:alpha_yeti',
    'twilightforest:snow_queen',
    'twilightforest:plateau_boss',
    'twilight_forest_final_boss:castle_keeper',
    'knightquest:netherman',
    'occultism:possessed_warden',
    'occultism:possessed_elder_guardian',
    'irons_spellbooks:pyromancer',
    'mowziesmobs:naga',
    'mowziesmobs:frostmaw',
    'mowziesmobs:ferrous_wroughtnaut',
    'mowziesmobs:umvuthi',
    'mowziesmobs:sculptor',
    'deep_aether:eots_controller',
    'deep_aether:eots_segment',
    'aether:slider',
    'aether:valkyrie_queen',
    'aether:sun_spirit',
    'ars_nouveau:wilden_boss',
    'irons_spellbooks:dead_king',
    'irons_spellbooks:dead_king_corpse',
    'irons_spellbooks:dead_king_soul',
    'irons_spellbooks:fire_boss',

    // Mutant Monsters (expanded inline instead of tag-forward for reliability)
    'mutantmonsters:mutant_creeper',
    'mutantmonsters:mutant_enderman',
    'mutantmonsters:mutant_skeleton',
    'mutantmonsters:mutant_snow_golem',
    'mutantmonsters:mutant_zombie',

    // Supplementaries — Plunderer spawns with a parrot on shoulder; parrots stack and lag the server
    'supplementaries:plunderer',

    // Ars Nouveau — utility/familiar mobs (free duplication exploit even with no drops)
    'ars_nouveau:wixie',
    'ars_nouveau:amethyst_golem',
    'ars_nouveau:bookwyrm',
    'ars_nouveau:alakarkinos',
    'ars_nouveau:starbuncle',
    'ars_nouveau:drygmy',
    'ars_nouveau:whirlisprig',

    // Easy NPC — every entity type (player-built NPCs, not farmable)
    'easy_npc:allay',
    'easy_npc:bogged',
    'easy_npc:cat',
    'easy_npc:cave_spider',
    'easy_npc:chicken',
    'easy_npc:creeper',
    'easy_npc:doppler',
    'easy_npc:drowned',
    'easy_npc:enderman',
    'easy_npc:evoker',
    'easy_npc:fairy',
    'easy_npc:fox',
    'easy_npc:ghast',
    'easy_npc:horse',
    'easy_npc:humanoid',
    'easy_npc:humanoid_slim',
    'easy_npc:husk',
    'easy_npc:illusioner',
    'easy_npc:iron_golem',
    'easy_npc:orc',
    'easy_npc:orc_warrior',
    'easy_npc:pig',
    'easy_npc:piglin',
    'easy_npc:piglin_brute',
    'easy_npc:pillager',
    'easy_npc:skeleton',
    'easy_npc:skeleton_horse',
    'easy_npc:slime',
    'easy_npc:spider',
    'easy_npc:stray',
    'easy_npc:vex',
    'easy_npc:villager',
    'easy_npc:vindicator',
    'easy_npc:witch',
    'easy_npc:wither_skeleton',
    'easy_npc:wolf',
    'easy_npc:zombie',
    'easy_npc:zombie_horse',
    'easy_npc:zombie_villager',
    'easy_npc:zombified_piglin'
];

ServerEvents.tags('entity_type', event => {
    // Apothic Spawners — placing spawn egg into Apothic Spawner block.
    // ApothicEnchanting's Ender Lead / Occult Ender Lead reuses this exact tag to
    // deny binding a leashed mob to a spawner, so this one entry covers both.
    event.add('apothic_spawners:blacklisted_from_spawners', ARCADIA_FARM_BLACKLIST);

    // Common "do not capture" tag. ApothicEnchanting's Ender Lead canLeash() denies
    // any entity in c:bosses OR c:capturing_not_supported, so this blocks leashing
    // our blacklist (e.g. irons_spellbooks:dead_king_corpse) into an Ender Lead in
    // the first place. Also respected by other capture mods that honor the tag.
    event.add('c:capturing_not_supported', ARCADIA_FARM_BLACKLIST);

    // Ars Nouveau Drygmy — passive mob-drop farming familiar
    event.add('ars_nouveau:drygmy_blacklist', ARCADIA_FARM_BLACKLIST);

    // Ars Nouveau Jar — capturing mobs in jar
    event.add('ars_nouveau:jar_blacklist', ARCADIA_FARM_BLACKLIST);

    // Ars Nouveau Jar Release — preventing release of captured mobs
    event.add('ars_nouveau:jar_release_blacklist', ARCADIA_FARM_BLACKLIST);

    // Ars Additions Source Spawner — Ars Nouveau spawner variant
    event.add('ars_additions:source_spawner_denylist', ARCADIA_FARM_BLACKLIST);

    // Occultism Soul Gem — capturing mobs in gem
    event.add('occultism:soul_gem_deny_list', ARCADIA_FARM_BLACKLIST);
    event.add('occultism:fragile_soul_gem_deny_list', ARCADIA_FARM_BLACKLIST);

    // Supplementaries — bottle / cage / soap mob capture
    event.add('supplementaries:capture_blacklist', ARCADIA_FARM_BLACKLIST);

    // Carry On — carrying mob in hands (also a farm exploit vector)
    event.add('carryon:entity_blacklist', ARCADIA_FARM_BLACKLIST);

    // PneumaticCraft — Vacuum Trap mob capture
    event.add('pneumaticcraft:vacuum_trap_blacklisted', ARCADIA_FARM_BLACKLIST);
});

// =============================================================================
// SPAWNER SPAWN SAFETY-NET (tag-independent)
// =============================================================================
// The tags above stop a blacklisted spawn egg from being PLACED into an Apothic
// Spawner (Apothic checks the apothic_spawners:blacklisted_from_spawners tag and
// cancels the right-click). That guard only fires for vanilla SpawnEggItems and
// relies on the entity_type tag binding at runtime. To guarantee the rule no
// matter how a spawner ends up holding a banned mob (non-vanilla egg, command,
// /data edit, a spawner created before this list existed, or a tag-binding
// failure), we also cancel the SPAWN itself: any blacklisted entity spawned with
// reason SPAWNER is denied. Reads the JS list directly, so it never depends on
// the tag system.
// =============================================================================
const ARCADIA_SPAWNER_DENY = new Set(ARCADIA_FARM_BLACKLIST);

EntityEvents.checkSpawn(event => {
    // MobSpawnType.SPAWNER.toString() === 'SPAWNER' on 1.21.1; only gate spawner spawns.
    if (String(event.getType()) !== 'SPAWNER') return;
    if (ARCADIA_SPAWNER_DENY.has(String(event.entity.type))) {
        event.cancel();
    }
});

// =============================================================================
// ENCHANTMENT LOOT CLEANUP
// =============================================================================
// Create Stuff & Additions ships the Gravity Gun enchant in the vanilla loot
// tags (on_random_loot / tradeable / non_treasure), so enchanted books for it
// keep showing up in chests and librarian trades. The config flag
// (enableGravityGunEnchant=false in create-stuff-additions.toml) only disables
// the EFFECT, not the loot/trade generation. Strip it from those tags so the
// books stop appearing. The Block Picker item it enchants is already banned.
// =============================================================================
ServerEvents.tags('enchantment', event => {
    [
        'minecraft:on_random_loot',
        'minecraft:tradeable',
        'minecraft:non_treasure',
    ].forEach(tag => event.remove(tag, 'create_sa:gravity_gun'));
});

console.info("[Arcadia V2] Global Tags Refined: Standardized tags + Farm protection blacklist (Apothic, Drygmy, Jar, Source Spawner, Soul Gem, Supplementaries, Carry On, Vacuum Trap) + spawner spawn safety-net + Gravity Gun enchant removed from loot tags.");
