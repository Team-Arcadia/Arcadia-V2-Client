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
      "minecraft:netherite_upgrade_smithing_template",
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
  const modNerf = event.addTableModifier([LootType.CHEST, LootType.VAULT]);

  // General mods nerf (5% drop rate)
  modNerf.removeLoot([
      "@irons_spellbooks",
      "@ars_nouveau",
      "@simplyswords"
  ]).randomChance(0.95);

  // Sophisticated Backpacks nerf (15% drop rate)
  event.addTableModifier([LootType.CHEST, LootType.VAULT])
    .removeLoot("@sophisticatedbackpacks")
    .randomChance(0.85);

  // Twilight Forest nerf (20% drop rate)
  event.addTableModifier([LootType.CHEST, LootType.VAULT])
    .removeLoot("@twilightforest")
    .randomChance(0.80);

  // Artifacts Removal - ABSOLUTE (0% drop rate)
  event.addTableModifier([LootType.CHEST, LootType.VAULT])
    .removeLoot("@artifacts");

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
    "dndecor:lead_cross_bolt",
    "dndecor:lead_dash_bolt",
    "dndecor:lead_dot_bolt",
    "dndecor:lead_flat_bolt",
    "dndecor:tin_cross_bolt",
    "dndecor:tin_dash_bolt",
    "dndecor:tin_dot_bolt",
    "dndecor:tin_flat_bolt",
    "dndecor:uranium_cross_bolt",
    "dndecor:uranium_dash_bolt",
    "dndecor:uranium_flat_bolt",
    "dndecor:uranium_dot_bolt",
    "dndecor:aluminum_cross_bolt",
    "dndecor:aluminum_dash_bolt",
    "dndecor:aluminum_dot_bolt",
    "dndecor:aluminum_flat_bolt",
    "dndecor:nickel_cross_bolt",
    "dndecor:nickel_dash_bolt",
    "dndecor:nickel_dot_bolt",
    "dndecor:nickel_flat_bolt",
    "dndecor:steel_cross_bolt",
    "dndecor:steel_dash_bolt",
    "dndecor:steel_flat_bolt",
    "dndecor:steel_dot_bolt",
    "dndecor:bronze_cross_bolt",
    "dndecor:bronze_dash_bolt",
    "dndecor:bronze_dot_bolt",
    "dndecor:bronze_flat_bolt",
    "dndecor:cast_iron_cross_bolt",
    "dndecor:cast_iron_dash_bolt",
    "dndecor:cast_iron_dot_bolt",
    "dndecor:cast_iron_flat_bolt",

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
  ];
  chest.removeLoot(bannedItems);

  /**
   * =========================================
   * 10. MIMIC NERF (No Artifact Drops)
   * =========================================
   */
  event
    .addTableModifier("artifacts:entities/mimic")
    .removeLoot(Ingredient.of(/.*/))
    .randomChance(0.99);

  console.info(
    "[Arcadia V2] Loot Nerf Applied: Global loot nerf active with probability tiers (0.01% to 50%).",
  );
});
