// Priority: 800

/*
    Mob Stats Script
    Adjusts the attributes (Health, Damage, etc.) of specific mobs and enforces global caps.
    Author: vyrriox
*/

var CONFIG = {
    MAX_HEALTH: 10000,
    MAX_DAMAGE: 50
};

// Boss lists (declared once, globally)
var tfBosses = [
    "twilightforest:naga", "twilightforest:lich", "twilightforest:minoshroom", "twilightforest:hydra",
    "twilightforest:knight_phantom", "twilightforest:ur_ghast", "twilightforest:alpha_yeti", "twilightforest:snow_queen"
];
var aetherBosses = ["aether:slider", "aether:valkyrie_queen", "aether:sun_spirit"];
var arsNouveauBosses = ["ars_nouveau:wilden_boss", "ars_nouveau:wilden_guardian", "ars_nouveau:wilden_stalker", "ars_nouveau:wilden_hunter"];
var ddBosses = ["deeperdarker:shriek_worm", "deeperdarker:stalker", "deeperdarker:sculk_snapper", "deeperdarker:shattered"];
var issBosses = ["irons_spellbooks:dead_king", "irons_spellbooks:dead_king_corpse", "irons_spellbooks:archevoker", "irons_spellbooks:necromancer", "irons_spellbooks:priest", "irons_spellbooks:citadel_keeper"];
var mutantBosses = ["mutantmonsters:mutant_creeper", "mutantmonsters:mutant_zombie", "mutantmonsters:mutant_skeleton", "mutantmonsters:mutant_enderman", "mutantmonsters:mutant_snow_golem", "mutantmonsters:spider_pig"];
var mowzieBosses = ["mowziesmobs:ferrous_wroughtnaut", "mowziesmobs:frostmaw", "mowziesmobs:naga", "mowziesmobs:umvuthi"];
var knightQuestBosses = ["knightquest:netherman", "knightquest:eldknight", "knightquest:ratman", "knightquest:swampman"];

/**
 * Helper function to boost entity attributes safely.
 */
function boostEntity(entity, multiplier) {
    try {
        var h = entity.attributes.getBaseValue('minecraft:generic.max_health');
        if (h > 0) {
            entity.attributes.setBaseValue('minecraft:generic.max_health', h * multiplier);
            entity.health = h * multiplier;
        }
    } catch (e) { /* skip */ }

    try {
        var a = entity.attributes.getBaseValue('minecraft:generic.armor');
        if (a > 0) entity.attributes.setBaseValue('minecraft:generic.armor', a * multiplier);
    } catch (e) { /* skip */ }

    try {
        var d = entity.attributes.getBaseValue('minecraft:generic.attack_damage');
        if (d > 0) entity.attributes.setBaseValue('minecraft:generic.attack_damage', d * multiplier);
    } catch (e) { /* skip */ }
}

EntityEvents.spawned(function (event) {
    var entity = event.entity;

    // Skip non-living or players
    if (!entity.isLiving() || entity.isPlayer()) return;

    // --- Global Health & Damage Protection ---
    try {
        var maxHealthVal = entity.attributes.getBaseValue('minecraft:generic.max_health');
        if (maxHealthVal > CONFIG.MAX_HEALTH) {
            entity.attributes.setBaseValue('minecraft:generic.max_health', CONFIG.MAX_HEALTH);
        }
    } catch (e) { /* skip */ }

    try {
        var damageVal = entity.attributes.getBaseValue('minecraft:generic.attack_damage');
        if (damageVal > CONFIG.MAX_DAMAGE) {
            entity.attributes.setBaseValue('minecraft:generic.attack_damage', CONFIG.MAX_DAMAGE);
        }
    } catch (e) { /* skip */ }

    try {
        var armorVal = entity.attributes.getBaseValue('minecraft:generic.armor');
        if (armorVal > 50) {
            entity.attributes.setBaseValue('minecraft:generic.armor', 50);
        }
    } catch (e) { /* skip */ }

    // --- Conditional Boost Logic (Runs only once) ---
    if (!entity.persistentData.stats_boosted) {

        // Wither: 500 HP
        if (entity.type === "minecraft:wither") {
            try {
                entity.attributes.setBaseValue("minecraft:generic.max_health", 500);
                entity.health = 500;
            } catch (e) { /* skip */ }
        }

        // Ender Dragon: 2000 HP
        if (entity.type === "minecraft:ender_dragon") {
            try {
                entity.attributes.setBaseValue("minecraft:generic.max_health", 2000);
                entity.health = 2000;
            } catch (e) { /* skip */ }
        }

        // Warden: 1000 HP
        if (entity.type === "minecraft:warden") {
            try {
                entity.attributes.setBaseValue("minecraft:generic.max_health", 1000);
                entity.health = 1000;
            } catch (e) { /* skip */ }
        }

        // Twilight Forest Bosses
        if (tfBosses.includes(entity.type)) {
            boostEntity(entity, 1.2);
        }

        // Castle Keeper
        if (entity.type === "twilight_forest_final_boss:castle_keeper") {
            boostEntity(entity, 4.0);
        }

        // Aether Bosses
        if (aetherBosses.includes(entity.type)) {
            boostEntity(entity, 1.5);
        }

        // Ars Nouveau
        if (arsNouveauBosses.includes(entity.type)) {
            boostEntity(entity, 1.2);
        }

        // Deeper and Darker
        if (ddBosses.includes(entity.type)) {
            boostEntity(entity, 1.4);
        }

        // Iron's Spells 'n Spellbooks
        if (issBosses.includes(entity.type)) {
            boostEntity(entity, 1.2);
        }

        // Mutant Monsters
        if (mutantBosses.includes(entity.type)) {
            boostEntity(entity, 1.2);
        }

        // Mowzie's Mobs
        if (mowzieBosses.includes(entity.type)) {
            boostEntity(entity, 1.2);
        }

        // Knight Quest Bosses
        if (knightQuestBosses.includes(entity.type)) {
            boostEntity(entity, 1.2);
        }

        // Mark as boosted
        entity.persistentData.stats_boosted = true;
    }

    // --- Final Enforcement Clamp ---
    try {
        if (entity.maxHealth > CONFIG.MAX_HEALTH) {
            entity.attributes.setBaseValue('minecraft:generic.max_health', CONFIG.MAX_HEALTH);
        }
    } catch (e) { /* skip */ }

    if (entity.health > entity.maxHealth) {
        entity.health = entity.maxHealth;
    }

    try {
        var finalDmg = entity.attributes.getBaseValue('minecraft:generic.attack_damage');
        if (finalDmg > CONFIG.MAX_DAMAGE) {
            entity.attributes.setBaseValue('minecraft:generic.attack_damage', CONFIG.MAX_DAMAGE);
        }
    } catch (e) { /* skip */ }

    try {
        var finalArmor = entity.attributes.getBaseValue('minecraft:generic.armor');
        if (finalArmor > 50) {
            entity.attributes.setBaseValue('minecraft:generic.armor', 50);
        }
    } catch (e) { /* skip */ }
});

console.info("[Arcadia V2] Mob Stats Loaded.");
