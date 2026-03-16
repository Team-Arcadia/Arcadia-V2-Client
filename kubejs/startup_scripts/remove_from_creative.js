// Priority: -500

/*
    Script to remove banned items from Creative Tabs.
    Created by vyrriox for Arcadia V2.
*/

StartupEvents.modifyCreativeTab("minecraft:search", (event) => {
    const hiddenItems = [
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

        // Sophisticated Storage
        "sophisticatedstorage:infinity_upgrade",
        // ComputerCraft
        "computercraft:turtle_normal",
        "computercraft:turtle_advanced",
    ];

    hiddenItems.forEach((item) => event.remove(item));
});

// Also remove from their respective mod tabs
StartupEvents.modifyCreativeTab("mekanism:mekanism", (event) => {
    event.remove("mekanism:atomic_disassembler");
    event.remove("mekanism:scuba_mask");
    event.remove("mekanism:scuba_tank");
    event.remove("mekanism:free_runners");
    event.remove("mekanism:free_runners_armored");
    event.remove("mekanism:jetpack");
    event.remove("mekanism:jetpack_armored");
    event.remove("mekanism:mekasuit_helmet");
    event.remove("mekanism:mekasuit_bodyarmor");
    event.remove("mekanism:mekasuit_pants");
    event.remove("mekanism:mekasuit_boots");
    event.remove("mekanism:flamethrower");
    event.remove("mekanism:electric_bow");
    // Modules...
    event.remove("mekanism:module_color_modulation_unit");
    event.remove("mekanism:module_laser_dissipation_unit");
    event.remove("mekanism:module_radiation_shielding_unit");
    event.remove("mekanism:module_electrolytic_breathing_unit");
    event.remove("mekanism:module_inhalation_purification_unit");
    event.remove("mekanism:module_vision_enhancement_unit");
    event.remove("mekanism:module_nutritional_injection_unit");
    event.remove("mekanism:module_dosimeter_unit");
    event.remove("mekanism:module_geiger_unit");
    event.remove("mekanism:module_jetpack_unit");
    event.remove("mekanism:module_charge_distribution_unit");
    event.remove("mekanism:module_gravitational_modulating_unit");
    event.remove("mekanism:module_elytra_unit");
    event.remove("mekanism:module_locomotive_boosting_unit");
    event.remove("mekanism:module_gyroscopic_stabilization_unit");
    event.remove("mekanism:module_hydrostatic_repulsor_unit");
    event.remove("mekanism:module_motorized_servo_unit");
    event.remove("mekanism:module_hydraulic_propulsion_unit");
    event.remove("mekanism:module_magnetic_attraction_unit");
    event.remove("mekanism:module_frost_walker_unit");
    event.remove("mekanism:module_soul_surfer_unit");
    event.remove("mekanismgenerators:module_geothermal_generator_unit");
    event.remove("mekanismgenerators:module_solar_recharging_unit");
    event.remove("mekanism:module_teleportation_unit");
    event.remove("mekanism:module_vein_mining_unit");
    event.remove("mekanism:module_blasting_unit");
    event.remove("mekanism:module_energy_unit");
    event.remove("mekanism:module_excavation_escalation_unit");
    event.remove("mekanism:module_attack_amplification_unit");
    event.remove("mekanism:module_farming_unit");
    event.remove("mekanism:module_shearing_unit");
    event.remove("mekanism:module_silk_touch_unit");
    event.remove("mekanism:module_fortune_unit");
    event.remove("mekanism:dimensional_stabilizer");
    event.remove("mekanism:quantum_entangloporter");
    event.remove("mekanism:hdpe_elytra");
    event.remove("mekanism:hdpe_pellet");
    event.remove("mekanism:module_base");
    event.remove("mekanism:meka_tool");
    event.remove("mekanism:portable_teleporter");
    event.remove("mekanism:portable_qio_dashboard");
    event.remove("mekanism:gauge_dropper");
    event.remove("mekanism:canteen");
    event.remove("mekanism:creative_bin");
});

StartupEvents.modifyCreativeTab("biomesoplenty:main", (event) => {
    event.remove("biomesoplenty:anomaly");
    event.remove("biomesoplenty:unmapped_end_stone");
    event.remove("biomesoplenty:null_block");
    event.remove("biomesoplenty:null_leaves");
    event.remove("biomesoplenty:null_plant");
    event.remove("biomesoplenty:liquid_null_bucket");
});

StartupEvents.modifyCreativeTab("dndecor:dndecor_tab", (event) => {
    const dndecorItems = [
        "dndecor:lead_cross_bolt", "dndecor:lead_dash_bolt", "dndecor:lead_dot_bolt", "dndecor:lead_flat_bolt",
        "dndecor:tin_cross_bolt", "dndecor:tin_dash_bolt", "dndecor:tin_dot_bolt", "dndecor:tin_flat_bolt",
        "dndecor:uranium_cross_bolt", "dndecor:uranium_dash_bolt", "dndecor:uranium_flat_bolt", "dndecor:uranium_dot_bolt",
        "dndecor:aluminum_cross_bolt", "dndecor:aluminum_dash_bolt", "dndecor:aluminum_dot_bolt", "dndecor:aluminum_flat_bolt",
        "dndecor:nickel_cross_bolt", "dndecor:nickel_dash_bolt", "dndecor:nickel_dot_bolt", "dndecor:nickel_flat_bolt",
        "dndecor:steel_cross_bolt", "dndecor:steel_dash_bolt", "dndecor:steel_flat_bolt", "dndecor:steel_dot_bolt",
        "dndecor:bronze_cross_bolt", "dndecor:bronze_dash_bolt", "dndecor:bronze_dot_bolt", "dndecor:bronze_flat_bolt",
        "dndecor:cast_iron_cross_bolt", "dndecor:cast_iron_dash_bolt", "dndecor:cast_iron_dot_bolt", "dndecor:cast_iron_flat_bolt"
    ];
    dndecorItems.forEach(item => event.remove(item));
});

StartupEvents.modifyCreativeTab("computercraft:main", (event) => {
    event.remove("computercraft:turtle_normal");
    event.remove("computercraft:turtle_advanced");
});

StartupEvents.modifyCreativeTab("creategoggles:main", (event) => {
    event.remove("creategoggles:module_goggle_unit");
});

StartupEvents.modifyCreativeTab("sophisticatedbackpacks:backpacks", (event) => {
    event.remove("sophisticatedbackpacks:infinity_upgrade");
    event.remove("sophisticatedbackpacks:inception_upgrade");
});

StartupEvents.modifyCreativeTab("sophisticatedstorage:storage", (event) => {
    event.remove("sophisticatedstorage:infinity_upgrade");
});

StartupEvents.modifyCreativeTab("occultism:occultism", (event) => {
    event.remove("occultism:storage_controller");
    event.remove("occultism:storage_stabilizer_tier1");
    event.remove("occultism:storage_stabilizer_tier2");
    event.remove("occultism:storage_stabilizer_tier3");
    event.remove("occultism:storage_stabilizer_tier4");
    event.remove("occultism:storage_remote_inert");
    event.remove("occultism:storage_remote");
    event.remove("occultism:storage_controller_base");
    event.remove("occultism:ritual_dummy/craft_stabilizer_tier1");
    event.remove("occultism:ritual_dummy/craft_stabilizer_tier2");
    event.remove("occultism:ritual_dummy/craft_stabilizer_tier3");
    event.remove("occultism:ritual_dummy/craft_stabilizer_tier4");
    event.remove("occultism:ritual_dummy/craft_storage_controller_base");
    event.remove("occultism:ritual_dummy/craft_storage_remote");
    event.remove("occultism:ritual_dummy/summon_djinni_manage_machine");
    event.remove("occultism:stable_wormhole");
    event.remove("occultism:ritual_dummy/craft_stable_wormhole");
});

StartupEvents.modifyCreativeTab("createendertransmission:main", (event) => {
    event.remove("createendertransmission:chunk_loader");
});

StartupEvents.modifyCreativeTab("create_jetpack:main", (event) => {
    event.remove("create_jetpack:netherite_jetpack");
    event.remove("create_jetpack:jetpack");
});

StartupEvents.modifyCreativeTab("create_sa:main", (event) => {
    event.remove("create_sa:brass_jetpack_chestplate");
    event.remove("create_sa:andesite_jetpack_chestplate");
    event.remove("create_sa:copper_jetpack_chestplate");
    event.remove("create_sa:netherite_jetpack_chestplate");
    event.remove("create_sa:andesite_exoskeleton_chestplate");
    event.remove("create_sa:brass_exoskeleton_chestplate");
    event.remove("create_sa:copper_exoskeleton_chestplate");
    event.remove("create_sa:block_picker");
});
