// priority: 1000

/*
    Script to actively remove banned items from player inventories.
    If a player obtains this item (via /give or otherwise), it will be removed.
    Created by vyrriox for Arcadia V2.

    Compatible with KubeJS 7.x / MC 1.21.1 NeoForge.
    Uses manual slot iteration (getItem/removeItemNoUpdate) for reliability.
*/

const BANNED_ITEMS = [
  // Biomes O' Plenty
  'biomesoplenty:anomaly',
  'biomesoplenty:unmapped_end_stone',
  'biomesoplenty:null_block',
  'biomesoplenty:null_leaves',
  'biomesoplenty:null_plant',
  'biomesoplenty:liquid_null_bucket',

  // Design n' Decor — decorative metal bolts (clutter). These are the IDs that
  // actually exist in the mod (andesite/brass/copper/gold/industrial/iron/netherite/zinc).
  'dndecor:andesite_cross_bolt',
  'dndecor:andesite_dash_bolt',
  'dndecor:andesite_dot_bolt',
  'dndecor:andesite_flat_bolt',
  'dndecor:brass_cross_bolt',
  'dndecor:brass_dash_bolt',
  'dndecor:brass_dot_bolt',
  'dndecor:brass_flat_bolt',
  'dndecor:copper_cross_bolt',
  'dndecor:copper_dash_bolt',
  'dndecor:copper_dot_bolt',
  'dndecor:copper_flat_bolt',
  'dndecor:gold_cross_bolt',
  'dndecor:gold_dash_bolt',
  'dndecor:gold_dot_bolt',
  'dndecor:gold_flat_bolt',
  'dndecor:industrial_cross_bolt',
  'dndecor:industrial_dash_bolt',
  'dndecor:industrial_dot_bolt',
  'dndecor:industrial_flat_bolt',
  'dndecor:iron_cross_bolt',
  'dndecor:iron_dash_bolt',
  'dndecor:iron_dot_bolt',
  'dndecor:iron_flat_bolt',
  'dndecor:netherite_cross_bolt',
  'dndecor:netherite_dash_bolt',
  'dndecor:netherite_dot_bolt',
  'dndecor:netherite_flat_bolt',
  'dndecor:zinc_cross_bolt',
  'dndecor:zinc_dash_bolt',
  'dndecor:zinc_dot_bolt',
  'dndecor:zinc_flat_bolt',

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
  'supplementaries:cannon_raft_bamboo',
/*  */
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
  'dndesires:gold_mixer',

  // Aether (full invisibility even to spectators - staff cannot moderate)
  'aether:invisibility_cloak'
];

// O(1) lookup
const BANNED_SET = new Set(BANNED_ITEMS);

/**
 * Scans all inventory slots and removes banned items.
 * Uses vanilla Container API (getItem/removeItemNoUpdate) for 1.21 compatibility.
 * Returns true if any item was removed.
 */
function removeBannedFromPlayer(player) {
  let inv = player.getInventory();
  let size = inv.getContainerSize();
  let removed = false;

  for (let i = 0; i < size; i++) {
    let stack = inv.getItem(i);
    if (stack.isEmpty()) continue;

    let id = String(stack.id);
    if (BANNED_SET.has(id) || id.startsWith('supplementaries:cannon_boat')) {
      inv.removeItemNoUpdate(i);
      removed = true;
    }
  }

  if (removed) {
    player.inventoryMenu.broadcastChanges();
  }
  return removed;
}

// --- INSTANT DETECTION: fires when any slot changes ---
PlayerEvents.inventoryChanged(event => {
  let id = String(event.item.id);

  if (BANNED_SET.has(id) || id.startsWith('supplementaries:cannon_boat')) {
    removeBannedFromPlayer(event.player);
    event.player.tell(Text.red('\u26D4 Banned Item removed from your inventory!'));
  }
});

// --- SAFETY NET: full scan every 5 minutes (6000 ticks) ---
// Single global server-tick handler instead of PlayerEvents.tick. The previous
// approach crossed the Java->Rhino bridge once per online player every tick (20 Hz x
// 30-50 players = 600-1000 callbacks/sec) only to evaluate a modulo gate. This fires
// the callback exactly once per tick, gates on the server tick counter, and iterates
// the online players in JS only on the matching tick (every 6000 ticks).
const SAFETY_SCAN_INTERVAL = 6000;

ServerEvents.tick(event => {
  if (event.server.tickCount % SAFETY_SCAN_INTERVAL !== 0) return;

  event.server.players.forEach(player => {
    if (removeBannedFromPlayer(player)) {
      player.tell(Text.red('\u26D4 Banned Item removed from your inventory!'));
    }
  });
});
