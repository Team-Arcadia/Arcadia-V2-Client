// Priority: 50

/*
    Loot Nerf Script
    Nerfs spawn rates for Diamond, Netherite, Iron, Gold, and specific mods.
    Also removes banned items defined in remove_items.js from spawning in chests (Lootr support).
    Author: vyrriox
*/

LootJS.modifiers((event) => {
  /**
   * General Helper for Chest Loot
   */
  const chest = event.addTableModifier([LootType.CHEST, LootType.VAULT]);

  /**
   * =========================================
   * 0. LEATHER (50% Spawn / 50% Remove)
   * =========================================
   */
  event
    .addTableModifier([LootType.CHEST, LootType.VAULT])
    .removeLoot(
      Ingredient.of(
        /.*:leather_(helmet|chestplate|leggings|boots|horse_armor).*/,
      ),
    )
    .removeLoot("minecraft:leather")
    .randomChance(0.5);

  /**
   * =========================================
   * 1. WOOD (30% Spawn / 70% Remove)
   * =========================================
   */
  event
    .addTableModifier([LootType.CHEST, LootType.VAULT])
    .removeLoot(
      Ingredient.of(
        /.*:(wooden|wood)_(sword|pickaxe|axe|shovel|hoe|helmet|chestplate|leggings|boots|horse_armor).*/,
      ),
    )
    .randomChance(0.7);

  /**
   * =========================================
   * 2. STONE (10% Spawn / 90% Remove)
   * =========================================
   */
  event
    .addTableModifier([LootType.CHEST, LootType.VAULT])
    .removeLoot(
      Ingredient.of(
        /.*:stone_(sword|pickaxe|axe|shovel|hoe|helmet|chestplate|leggings|boots|horse_armor).*/,
      ),
    )
    .randomChance(0.9);

  /**
   * =========================================
   * 3. IRON (5% Spawn / 95% Remove)
   * =========================================
   */
  event
    .addTableModifier([LootType.CHEST, LootType.VAULT])
    .removeLoot(
      Ingredient.of(
        /.*:iron_(sword|pickaxe|axe|shovel|hoe|helmet|chestplate|leggings|boots|ingot|horse_armor).*/,
      ),
    )
    .randomChance(0.95);

  /**
   * =========================================
   * 4. CHAINMAIL (3% Spawn / 97% Remove)
   * =========================================
   */
  event
    .addTableModifier([LootType.CHEST, LootType.VAULT])
    .removeLoot(
      Ingredient.of(/.*:chainmail_(helmet|chestplate|leggings|boots).*/),
    )
    .randomChance(0.97);

  /**
   * =========================================
   * 5. GOLD (1% Spawn / 99% Remove)
   * =========================================
   */
  event
    .addTableModifier([LootType.CHEST, LootType.VAULT])
    .removeLoot(
      Ingredient.of(
        /.*:(golden?|gold)_(sword|pickaxe|axe|shovel|hoe|helmet|chestplate|leggings|boots|ingot|horse_armor).*/,
      ),
    )
    .randomChance(0.99);

  /**
   * =========================================
   * 6. DIAMOND (0.5% Spawn / 99.5% Remove)
   * =========================================
   */
  event
    .addTableModifier([LootType.CHEST, LootType.VAULT])
    .removeLoot([
      "minecraft:diamond",
      "minecraft:diamond_block",
      Ingredient.of(
        /.*:diamond_(sword|pickaxe|axe|shovel|hoe|helmet|chestplate|leggings|boots|horse_armor|shield|paxel|hammer|spear|glaive|cutlass|claymore|scythe|halberd).*/,
      ),
    ])
    .randomChance(0.995);

  /**
   * =========================================
   * 7. NETHERITE (0.01% Spawn / 99.99% Remove)
   * =========================================
   */
  event
    .addTableModifier([LootType.CHEST, LootType.VAULT])
    .removeLoot([
      "minecraft:netherite_ingot",
      "minecraft:netherite_scrap",
      "minecraft:netherite_block",
      Ingredient.of(
        /.*:netherite_(sword|pickaxe|axe|shovel|hoe|helmet|chestplate|leggings|boots|horse_armor|shield|paxel|hammer|spear|glaive|cutlass|claymore|scythe|halberd).*/,
      ),
    ])
    .randomChance(0.9999);

   /**
   * =========================================
   * 8. MODS & SPECIAL ITEMS (NERFS)
   * =========================================
   */
  // Magic/weapon mods loot: 5% drop rate in normal chests, 25% inside hard
  // structures (boss dungeons) listed below. Both modifiers target the same
  // items but are mutually exclusive via the structure condition, so the
  // rates never stack.
  const RARE_MOD_LOOT = [
      "@irons_spellbooks",
      "@ars_nouveau",
      "@simplyswords"
  ];

  const HARD_STRUCTURES = [
      // Vanilla endgame
      "minecraft:end_city",
      "minecraft:bastion_remnant",
      "minecraft:ancient_city",
      "minecraft:trial_chambers",
      "minecraft:mansion",
      "minecraft:fortress",
      // Twilight Forest boss structures
      "twilightforest:lich_tower",
      "twilightforest:labyrinth",
      "twilightforest:hydra_lair",
      "twilightforest:knight_stronghold",
      "twilightforest:dark_tower",
      "twilightforest:aurora_palace",
      "twilightforest:final_castle",
      // Deeper & Darker
      "deeperdarker:ancient_temple",
      // Dungeons Arise (major dungeons only)
      "dungeons_arise:abandoned_temple",
      "dungeons_arise:aviary",
      "dungeons_arise:bandit_towers",
      "dungeons_arise:bathhouse",
      "dungeons_arise:coliseum",
      "dungeons_arise:foundry",
      "dungeons_arise:heavenly_challenger",
      "dungeons_arise:heavenly_conqueror",
      "dungeons_arise:heavenly_rider",
      "dungeons_arise:illager_corsair",
      "dungeons_arise:illager_fort",
      "dungeons_arise:illager_galley",
      "dungeons_arise:infested_temple",
      "dungeons_arise:keep_kayra",
      "dungeons_arise:kisegi_sanctuary",
      "dungeons_arise:mechanical_nest",
      "dungeons_arise:mining_complex",
      "dungeons_arise:monastery",
      "dungeons_arise:mushroom_mines",
      "dungeons_arise:plague_asylum",
      "dungeons_arise:scorched_mines",
      "dungeons_arise:shiraz_palace",
      "dungeons_arise:thornborn_towers",
      "dungeons_arise:typhon",
      "dungeons_arise:undead_pirate_ship"
  ];

  // Outside hard structures: 95% removal (5% drop rate)
  event.addTableModifier([LootType.CHEST, LootType.VAULT])
    .removeLoot(RARE_MOD_LOOT)
    .matchCustomCondition({
      condition: "minecraft:inverted",
      term: {
        condition: "minecraft:location_check",
        predicate: { structures: HARD_STRUCTURES }
      }
    })
    .randomChance(0.95);

  // Inside hard structures: 75% removal (25% drop rate)
  event.addTableModifier([LootType.CHEST, LootType.VAULT])
    .removeLoot(RARE_MOD_LOOT)
    .matchStructure(HARD_STRUCTURES, false)
    .randomChance(0.75);

  // Sophisticated Backpacks nerf (15% drop rate)
  event.addTableModifier([LootType.CHEST, LootType.VAULT])
    .removeLoot("@sophisticatedbackpacks")
    .randomChance(0.85);

  // Twilight Forest loot: 20% drop rate outside the dimension, 50% inside it
  // (all TF structures live in the dimension, so exploring there pays off).
  // Both modifiers are mutually exclusive via the dimension condition.
  event.addTableModifier([LootType.CHEST, LootType.VAULT])
    .removeLoot("@twilightforest")
    .matchCustomCondition({
      condition: "minecraft:inverted",
      term: {
        condition: "minecraft:location_check",
        predicate: { dimension: "twilightforest:twilight_forest" }
      }
    })
    .randomChance(0.80);

  event.addTableModifier([LootType.CHEST, LootType.VAULT])
    .removeLoot("@twilightforest")
    .matchDimension("twilightforest:twilight_forest")
    .randomChance(0.50);

  // Artifacts (20% drop rate / 80% Remove)
  event.addTableModifier([LootType.CHEST, LootType.VAULT])
    .removeLoot("@artifacts")
    .randomChance(0.80);

  /**
   * =========================================
   * 9. BANNED ITEMS (Strict Removal / 100% Remove)
   * =========================================
   */
  const bannedItems = [
    // Biomes O' Plenty
    "biomesoplenty:anomaly",
    "biomesoplenty:unmapped_end_stone",
    "biomesoplenty:null_block",
    "biomesoplenty:null_leaves",
    "biomesoplenty:null_plant",
    "biomesoplenty:liquid_null_bucket",

    // Design n' Decor
    "dndecor:andesite_cross_bolt",
    "dndecor:andesite_dash_bolt",
    "dndecor:andesite_dot_bolt",
    "dndecor:andesite_flat_bolt",
    "dndecor:brass_cross_bolt",
    "dndecor:brass_dash_bolt",
    "dndecor:brass_dot_bolt",
    "dndecor:brass_flat_bolt",
    "dndecor:copper_cross_bolt",
    "dndecor:copper_dash_bolt",
    "dndecor:copper_dot_bolt",
    "dndecor:copper_flat_bolt",
    "dndecor:gold_cross_bolt",
    "dndecor:gold_dash_bolt",
    "dndecor:gold_dot_bolt",
    "dndecor:gold_flat_bolt",
    "dndecor:industrial_cross_bolt",
    "dndecor:industrial_dash_bolt",
    "dndecor:industrial_dot_bolt",
    "dndecor:industrial_flat_bolt",
    "dndecor:iron_cross_bolt",
    "dndecor:iron_dash_bolt",
    "dndecor:iron_dot_bolt",
    "dndecor:iron_flat_bolt",
    "dndecor:netherite_cross_bolt",
    "dndecor:netherite_dash_bolt",
    "dndecor:netherite_dot_bolt",
    "dndecor:netherite_flat_bolt",
    "dndecor:zinc_cross_bolt",
    "dndecor:zinc_dash_bolt",
    "dndecor:zinc_dot_bolt",
    "dndecor:zinc_flat_bolt",

    // Mekanism
    "mekanism:atomic_disassembler",
    "mekanism:scuba_mask",
    "mekanism:scuba_tank",
    "mekanism:free_runners",
    "mekanism:free_runners_armored",
    "mekanism:jetpack",
    "mekanism:jetpack_armored",
    "mekanism:mekasuit_helmet",
    "mekanism:mekasuit_bodyarmor",
    "mekanism:mekasuit_pants",
    "mekanism:mekasuit_boots",
    "mekanism:flamethrower",
    "mekanism:electric_bow",
    "mekanism:module_color_modulation_unit",
    "mekanism:module_laser_dissipation_unit",
    "mekanism:module_radiation_shielding_unit",
    "mekanism:module_electrolytic_breathing_unit",
    "mekanism:module_inhalation_purification_unit",
    "mekanism:module_vision_enhancement_unit",
    "mekanism:module_nutritional_injection_unit",
    "mekanism:module_dosimeter_unit",
    "mekanism:module_geiger_unit",
    "mekanism:module_jetpack_unit",
    "mekanism:module_charge_distribution_unit",
    "mekanism:module_gravitational_modulating_unit",
    "mekanism:module_elytra_unit",
    "mekanism:module_locomotive_boosting_unit",
    "mekanism:module_gyroscopic_stabilization_unit",
    "mekanism:module_hydrostatic_repulsor_unit",
    "mekanism:module_motorized_servo_unit",
    "mekanism:module_hydraulic_propulsion_unit",
    "mekanism:module_magnetic_attraction_unit",
    "mekanism:module_frost_walker_unit",
    "mekanism:module_soul_surfer_unit",
    "mekanismgenerators:module_geothermal_generator_unit",
    "mekanismgenerators:module_solar_recharging_unit",
    "mekanism:module_teleportation_unit",
    "mekanism:module_vein_mining_unit",
    "mekanism:module_blasting_unit",
    "mekanism:module_energy_unit",
    "mekanism:module_excavation_escalation_unit",
    "mekanism:module_attack_amplification_unit",
    "mekanism:module_farming_unit",
    "mekanism:module_shearing_unit",
    "mekanism:module_silk_touch_unit",
    "mekanism:module_fortune_unit",
    "mekanism:dimensional_stabilizer",
    "mekanism:quantum_entangloporter",
    "mekanism:hdpe_elytra",
    "mekanism:hdpe_sheet",
    "mekanism:hdpe_rod",
    "mekanism:hdpe_pellet",
    "bettercopper:copper_heart",
    "bettercopper:reversed_copper_heart",
    "mekanism:module_base",
    "mekanism:meka_tool",
    "mekanism:portable_teleporter",
    "mekanism:portable_qio_dashboard",
    "mekanism:gauge_dropper",
    "mekanism:canteen",
    "mekanism:creative_bin",
    "mekanism:cardboard_box",

    // Occultism
    "occultism:storage_controller",
    "occultism:storage_stabilizer_tier1",
    "occultism:storage_stabilizer_tier2",
    "occultism:storage_stabilizer_tier3",
    "occultism:storage_stabilizer_tier4",
    "occultism:storage_remote_inert",
    "occultism:storage_remote",
    "occultism:storage_controller_base",
    "occultism:ritual_dummy/craft_stabilizer_tier1",
    "occultism:ritual_dummy/craft_stabilizer_tier2",
    "occultism:ritual_dummy/craft_stabilizer_tier3",
    "occultism:ritual_dummy/craft_stabilizer_tier4",
    "occultism:ritual_dummy/craft_storage_controller_base",
    "occultism:ritual_dummy/craft_storage_remote",
    "occultism:ritual_dummy/summon_djinni_manage_machine",
    "occultism:stable_wormhole",
    "occultism:ritual_dummy/craft_stable_wormhole",

    // Create Ender Transmission
    "createendertransmission:chunk_loader",

    // Create Jetpacks & Stuff & Additions
    "create_jetpack:netherite_jetpack",
    "create_jetpack:jetpack",
    "create_sa:brass_jetpack_chestplate",
    "create_sa:andesite_jetpack_chestplate",
    "create_sa:copper_jetpack_chestplate",
    "create_sa:netherite_jetpack_chestplate",
    "create_sa:andesite_exoskeleton_chestplate",
    "create_sa:brass_exoskeleton_chestplate",
    "create_sa:copper_exoskeleton_chestplate",
    "create_sa:block_picker",

    // Create Goggles
    "creategoggles:module_goggle_unit",

    // Sophisticated Backpacks
    "sophisticatedbackpacks:infinity_upgrade",
    "sophisticatedbackpacks:inception_upgrade",
    "sophisticatedbackpacks:stack_upgrade_omega_tier",

    // Sophisticated Storage
    "sophisticatedstorage:infinity_upgrade",
    "sophisticatedstorage:stack_upgrade_omega_tier",

    // ComputerCraft
    "computercraft:turtle_normal",
    "computercraft:turtle_advanced",

    // Ars Nouveau
    "ars_nouveau:planarium",

    // Backtanks (Banned)
    "creategoggles:chainmail_backtank",
    "creategoggles:diamond_backtank",
    "creategoggles:golden_backtank",
    "creategoggles:iron_backtank",
    "creategoggles:leather_backtank",
    "create:netherite_backtank",

    // Advanced Peripherals (chunk loading exploit)
    "advancedperipherals:chunk_controller",

    // Ars Additions (server crash loop on use)
    "ars_additions:exploration_warp_scroll",

    // Supplementaries Cannon Boats (crash server on fire)
    "supplementaries:cannon_boat_oak",
    "supplementaries:cannon_boat_spruce",
    "supplementaries:cannon_boat_birch",
    "supplementaries:cannon_boat_jungle",
    "supplementaries:cannon_boat_acacia",
    "supplementaries:cannon_boat_dark_oak",
    "supplementaries:cannon_boat_mangrove",
    "supplementaries:cannon_boat_cherry",
    "supplementaries:cannon_raft_bamboo",

    // Easy Villagers (OP/exploit)
    "easy_villagers:iron_farm",

    // Occultism
    "occultism:iesnium_anvil",

    // DnDesires
    "dndesires:gold_mixer",

    // Aether (full invisibility even to spectators - staff cannot moderate)
    "aether:invisibility_cloak",
  ];
  // Strip banned items from chests/vaults AND mob drops + fishing (defense in depth).
  chest.removeLoot(bannedItems);
  event
    .addTableModifier([LootType.ENTITY, LootType.FISHING])
    .removeLoot(bannedItems);

  /**
   * =========================================
   * 10. MIMIC NERF (20% Artifact Drops)
   * =========================================
   */
  event
    .addTableModifier("artifacts:entities/mimic")
    .removeLoot(Ingredient.of(/.*/))
    .randomChance(0.80);

  console.info(
    "[Arcadia V2] Loot Nerf Applied: Global loot nerf active with probability tiers (0.01% to 50%, Artifacts 20%, Mimic 20%).",
  );
});
