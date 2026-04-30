// priority: 1000

/*
    Script to remove recipes for banned items.
    Created by vyrriox for Arcadia V2.

    Compatible with KubeJS 7.x / MC 1.21.1 NeoForge.
*/

ServerEvents.recipes(event => {
  const itemsToRemove = [
    // Biomes O' Plenty
    'biomesoplenty:anomaly',
    'biomesoplenty:unmapped_end_stone',
    'biomesoplenty:null_block',
    'biomesoplenty:null_leaves',
    'biomesoplenty:null_plant',
    'biomesoplenty:liquid_null_bucket',

    // Design n' Decor
    'dndecor:lead_cross_bolt',
    'dndecor:lead_dash_bolt',
    'dndecor:lead_dot_bolt',
    'dndecor:lead_flat_bolt',
    'dndecor:tin_cross_bolt',
    'dndecor:tin_dash_bolt',
    'dndecor:tin_dot_bolt',
    'dndecor:tin_flat_bolt',
    'dndecor:uranium_cross_bolt',
    'dndecor:uranium_dash_bolt',
    'dndecor:uranium_flat_bolt',
    'dndecor:uranium_dot_bolt',
    'dndecor:aluminum_cross_bolt',
    'dndecor:aluminum_dash_bolt',
    'dndecor:aluminum_dot_bolt',
    'dndecor:aluminum_flat_bolt',
    'dndecor:nickel_cross_bolt',
    'dndecor:nickel_dash_bolt',
    'dndecor:nickel_dot_bolt',
    'dndecor:nickel_flat_bolt',
    'dndecor:steel_cross_bolt',
    'dndecor:steel_dash_bolt',
    'dndecor:steel_flat_bolt',
    'dndecor:steel_dot_bolt',
    'dndecor:bronze_cross_bolt',
    'dndecor:bronze_dash_bolt',
    'dndecor:bronze_dot_bolt',
    'dndecor:bronze_flat_bolt',
    'dndecor:cast_iron_cross_bolt',
    'dndecor:cast_iron_dash_bolt',
    'dndecor:cast_iron_dot_bolt',
    'dndecor:cast_iron_flat_bolt',

    // Mekanism
    'mekanism:atomic_disassembler',
    'mekanism:scuba_mask',
    'mekanism:scuba_tank',
    'mekanism:free_runners',
    'mekanism:free_runners_armored',
    'mekanism:jetpack',
    'mekanism:jetpack_armored',
    'mekanism:mekasuit_helmet',
    'mekanism:mekasuit_bodyarmor',
    'mekanism:mekasuit_pants',
    'mekanism:mekasuit_boots',
    'mekanism:flamethrower',
    'mekanism:electric_bow',
    'mekanism:module_color_modulation_unit',
    'mekanism:module_laser_dissipation_unit',
    'mekanism:module_radiation_shielding_unit',
    'mekanism:module_electrolytic_breathing_unit',
    'mekanism:module_inhalation_purification_unit',
    'mekanism:module_vision_enhancement_unit',
    'mekanism:module_nutritional_injection_unit',
    'mekanism:module_dosimeter_unit',
    'mekanism:module_geiger_unit',
    'mekanism:module_jetpack_unit',
    'mekanism:module_charge_distribution_unit',
    'mekanism:module_gravitational_modulating_unit',
    'mekanism:module_elytra_unit',
    'mekanism:module_locomotive_boosting_unit',
    'mekanism:module_gyroscopic_stabilization_unit',
    'mekanism:module_hydrostatic_repulsor_unit',
    'mekanism:module_motorized_servo_unit',
    'mekanism:module_hydraulic_propulsion_unit',
    'mekanism:module_magnetic_attraction_unit',
    'mekanism:module_frost_walker_unit',
    'mekanism:module_soul_surfer_unit',
    'mekanismgenerators:module_geothermal_generator_unit',
    'mekanismgenerators:module_solar_recharging_unit',
    'mekanism:module_teleportation_unit',
    'mekanism:module_vein_mining_unit',
    'mekanism:module_blasting_unit',
    'mekanism:module_energy_unit',
    'mekanism:module_excavation_escalation_unit',
    'mekanism:module_attack_amplification_unit',
    'mekanism:module_farming_unit',
    'mekanism:module_shearing_unit',
    'mekanism:module_silk_touch_unit',
    'mekanism:module_fortune_unit',
    'mekanism:dimensional_stabilizer',
    'mekanism:quantum_entangloporter',
    'mekanism:hdpe_elytra',
    'bettercopper:copper_heart',
    'bettercopper:reversed_copper_heart',
    'mekanism:module_base',
    'mekanism:meka_tool',
    'mekanism:portable_teleporter',
    'mekanism:portable_qio_dashboard',
    'mekanism:canteen',
    'mekanism:creative_bin',
    'mekanism:cardboard_box',

    // Occultism
    'occultism:storage_controller',
    'occultism:storage_stabilizer_tier1',
    'occultism:storage_stabilizer_tier2',
    'occultism:storage_stabilizer_tier3',
    'occultism:storage_stabilizer_tier4',
    'occultism:storage_remote_inert',
    'occultism:storage_remote',
    'occultism:storage_controller_base',
    'occultism:ritual_dummy/craft_stabilizer_tier1',
    'occultism:ritual_dummy/craft_stabilizer_tier2',
    'occultism:ritual_dummy/craft_stabilizer_tier3',
    'occultism:ritual_dummy/craft_stabilizer_tier4',
    'occultism:ritual_dummy/craft_storage_controller_base',
    'occultism:ritual_dummy/craft_storage_remote',
    'occultism:ritual_dummy/summon_djinni_manage_machine',
    'occultism:stable_wormhole',
    'occultism:ritual_dummy/craft_stable_wormhole',
    'occultism:iesnium_anvil',

    // Create Ender Transmission
    'createendertransmission:chunk_loader',

    // Create Jetpacks & Stuff & Additions
    'create_jetpack:netherite_jetpack',
    'create_jetpack:jetpack',
    'create_sa:brass_jetpack_chestplate',
    'create_sa:andesite_jetpack_chestplate',
    'create_sa:copper_jetpack_chestplate',
    'create_sa:netherite_jetpack_chestplate',
    'create_sa:andesite_exoskeleton_chestplate',
    'create_sa:brass_exoskeleton_chestplate',
    'create_sa:copper_exoskeleton_chestplate',
    'create_sa:block_picker',

    // Create Goggles
    'creategoggles:module_goggle_unit',

    // Sophisticated Backpacks
    'sophisticatedbackpacks:infinity_upgrade',
    'sophisticatedbackpacks:inception_upgrade',
    'sophisticatedbackpacks:stack_upgrade_omega_tier',

    // Sophisticated Storage
    'sophisticatedstorage:infinity_upgrade',
    'sophisticatedstorage:stack_upgrade_omega_tier',

    // ComputerCraft
    'computercraft:turtle_normal',
    'computercraft:turtle_advanced',

    // Ars Nouveau
    'ars_nouveau:planarium',

    // Supplementaries Cannon Boats (crash server on fire)
    'supplementaries:cannon_boat_oak',
    'supplementaries:cannon_boat_spruce',
    'supplementaries:cannon_boat_birch',
    'supplementaries:cannon_boat_jungle',
    'supplementaries:cannon_boat_acacia',
    'supplementaries:cannon_boat_dark_oak',
    'supplementaries:cannon_boat_mangrove',
    'supplementaries:cannon_boat_cherry',
    'supplementaries:cannon_boat_bamboo',

    // Backtanks (Banned)
    'creategoggles:chainmail_backtank',
    'creategoggles:diamond_backtank',
    'creategoggles:golden_backtank',
    'creategoggles:iron_backtank',
    'creategoggles:leather_backtank',
    'create:netherite_backtank',

    // Easy Villagers (OP/exploit)
    'easy_villagers:iron_farm',

    // Advanced Peripherals (chunk loading exploit)
    'advancedperipherals:chunk_controller',

    // Ars Additions (server crash loop on use)
    'ars_additions:exploration_warp_scroll',

    // DnDesires
    'dndesires:gold_mixer'
  ];

  // Disable vanilla item repair recipe (prevents dual-wield weapons from merging)
  event.remove({ type: 'minecraft:crafting_special_repairitem' });

  let removed = 0;
  for (let i = 0; i < itemsToRemove.length; i++) {
    try {
      event.remove({ output: itemsToRemove[i] });
      removed++;
    } catch (e) {
      // Item doesn't exist in this modpack version, skip silently
    }
  }

  console.info('[Arcadia V2] Removed recipes for ' + removed + '/' + itemsToRemove.length + ' banned items.');
});
