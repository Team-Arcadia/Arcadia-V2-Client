// Priority: 1000

/*
    Script to actively remove banned items from player inventories.
    If a player obtains this item (via /give or otherwise), it will be removed.
    Created by vyrriox for Arcadia V2.
*/

const BANNED_ITEMS = [
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
];

PlayerEvents.inventoryChanged((event) => {
  let player = event.player;
  let inventory = player.inventory;

  // Direct check via list (faster and safer than tags)
  // Scanning inventory for banned items
  let found = false;

  BANNED_ITEMS.forEach((itemId) => {
    // inventory.count() works even if the item is in an armor slot or offhand
    if (inventory.count(itemId) > 0) {
      inventory.clear(itemId);
      found = true;
    }
  });

  // Special Check: Enchanted Book with 'create_sa:above_the_clouds'
  // Iterate through all slots to find the specific NBT
  for (let i = 0; i < inventory.size; i++) {
    let stack = inventory.getStackInSlot(i);
    if (stack.id === "minecraft:enchanted_book") {
      let storedEnchants = stack.nbt ? stack.nbt.StoredEnchantments : null;
      if (storedEnchants) {
        storedEnchants.forEach(enchant => {
          if (enchant.id === "create_sa:above_the_clouds") {
            inventory.clear(stack); // Clears this specific stack
            found = true;
          }
        });
      }
    }
  }

  if (found) {
    player.tell(Text.red("⛔ Banned Item removed from your inventory!"));
  }
});

// Extra security: player tick (approx every second)
// To catch cases where inventoryChanged doesn't trigger fast enough (e.g., Creative Pick block)
PlayerEvents.tick((event) => {
  // Only check every 20 ticks (1 second) for performance
  if (event.player.age % 20 != 0) return;

  let player = event.player;
  let inventory = player.inventory;

  BANNED_ITEMS.forEach((itemId) => {
    if (inventory.count(itemId) > 0) {
      inventory.clear(itemId);
    }
  });

  // Special Check: Enchanted Book with 'create_sa:above_the_clouds'
  // Optimization: Only scan if player actually has enchanted books
  if (inventory.count("minecraft:enchanted_book") > 0) {
    for (let i = 0; i < inventory.size; i++) {
        let stack = inventory.getStackInSlot(i);
        if (stack.id === "minecraft:enchanted_book" && stack.nbt) {
          let storedEnchants = stack.nbt.StoredEnchantments;
          if (storedEnchants) {
            storedEnchants.forEach(enchant => {
              if (enchant.id === "create_sa:above_the_clouds") {
                inventory.clear(stack);
              }
            });
          }
        }
    }
  }
});
