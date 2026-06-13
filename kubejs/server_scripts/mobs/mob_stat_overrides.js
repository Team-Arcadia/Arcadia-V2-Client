// Priority: 800

/**
 * Mob Stats Script
 * Adjusts the attributes (Health, Damage, etc.) of specific mobs and enforces global caps.
 * Author: vyrriox
 * Optimized for KubeJS 1.21.1
 */

const CONFIG = {
    MAX_HEALTH: 10000.0,
    MAX_DAMAGE: 80.0,
    MAX_ARMOR: 50.0
};

// Boss data and multipliers for O(1) lookup
const BOSS_DATA = {
    'minecraft:wither': { hp: 500.0 },
    'minecraft:ender_dragon': { hp: 2000.0 },
    'minecraft:warden': { hp: 1000.0 },

    // --- Twilight Forest (Balanced for Arcadia V2) ---
    'twilightforest:naga': { mult: 2.5 },
    'twilightforest:lich': { mult: 2.5 },
    'twilightforest:minoshroom': { mult: 2.5 },
    'twilightforest:hydra': { mult: 2.5 },
    'twilightforest:knight_phantom': { mult: 2.5 },
    'twilightforest:ur_ghast': { mult: 2.5 },
    'twilightforest:alpha_yeti': { mult: 2.5 },
    'twilightforest:snow_queen': { mult: 2.5 },
    'twilight_forest_final_boss:castle_keeper': { mult: 16.0 },

    // --- Aether (Balanced for Arcadia V2) ---
    'aether:slider': { mult: 1.2 },
    'aether:valkyrie_queen': { mult: 6.0 },
    'aether:sun_spirit': { mult: 6.0 },

    // Ars Nouveau
    'ars_nouveau:wilden_boss': { mult: 1.2 },
    'ars_nouveau:wilden_guardian': { mult: 1.2 },
    'ars_nouveau:wilden_stalker': { mult: 1.2 },
    'ars_nouveau:wilden_hunter': { mult: 1.2 },

    // Deeper and Darker
    'deeperdarker:shriek_worm': { mult: 1.8 },
    'deeperdarker:stalker': { mult: 1.8 },
    'deeperdarker:sculk_snapper': { mult: 1.8 },
    'deeperdarker:shattered': { mult: 1.8 },

    // Iron's Spells 'n Spellbooks
    'irons_spellbooks:dead_king': { mult: 1.9 },
    'irons_spellbooks:dead_king_corpse': { mult: 1.9 },
    'irons_spellbooks:archevoker': { mult: 1.9 },
    'irons_spellbooks:necromancer': { mult: 1.9 },
    'irons_spellbooks:priest': { mult: 1.9 },
    'irons_spellbooks:citadel_keeper': { mult: 1.9 },

    // Mutant Monsters
    'mutantmonsters:mutant_creeper': { mult: 1.2 },
    'mutantmonsters:mutant_zombie': { mult: 1.2 },
    'mutantmonsters:mutant_skeleton': { mult: 1.2 },
    'mutantmonsters:mutant_enderman': { mult: 1.2 },
    'mutantmonsters:mutant_snow_golem': { mult: 1.2 },
    'mutantmonsters:spider_pig': { mult: 1.2 },

    // Mowzie's Mobs
    'mowziesmobs:ferrous_wroughtnaut': { mult: 8.0 },
    'mowziesmobs:frostmaw': { mult: 8.0 },
    'mowziesmobs:naga': { mult: 8.0 },
    'mowziesmobs:umvuthi': { mult: 8.0 },

    // Knight Quest
    'knightquest:netherman': { mult: 1.5 },
    'knightquest:eldknight': { mult: 1.5 },
    'knightquest:ratman': { mult: 1.5 },
    'knightquest:swampman': { mult: 1.5 }
};

// Toggle verbose per-boss spawn logging. Keep false on production servers:
// console.info on the spawn hot path is main-thread I/O. Set true only for debugging.
const DEBUG_LOG = false;

/**
 * Helper function to boost a known boss entity's attributes safely.
 * Only called for entities present in BOSS_DATA, behind the idempotency guard.
 */
function applyStats(entity, data) {
    // Apply Health (Max HP works more reliably as a property in 1.21)
    if (data.hp || data.mult) {
        let currentMax = entity.maxHealth;
        let newMax = data.hp ? data.hp : (currentMax * (data.mult || 1.0));

        newMax = Math.min(newMax, CONFIG.MAX_HEALTH);

        entity.maxHealth = newMax;
        entity.health = newMax;
    }

    // Apply Attack Damage
    let dmgAttr = entity.getAttribute('minecraft:generic.attack_damage');
    if (dmgAttr && data.mult) {
        dmgAttr.setBaseValue(Math.min(dmgAttr.getBaseValue() * data.mult, CONFIG.MAX_DAMAGE));
    }

    // Apply Armor
    let armorAttr = entity.getAttribute('minecraft:generic.armor');
    if (armorAttr && data.mult) {
        armorAttr.setBaseValue(Math.min(armorAttr.getBaseValue() * data.mult, CONFIG.MAX_ARMOR));
    }
}

EntityEvents.spawned(event => {
    const { entity } = event;

    // --- Cheapest rejects first (no allocation, no bridge string work) ---
    // Filters out item entities, XP orbs, projectiles, players, etc.
    if (!entity || !entity.isLiving() || entity.isPlayer()) return;

    // entity.type stringification is comparatively expensive (bridge + heap alloc),
    // so it is only computed once here, after the cheap living/player gate.
    const entityId = String(entity.type);
    const bossData = BOSS_DATA[entityId];

    if (bossData) {
        // --- BOSS PATH (rare) ---
        // The idempotency guard lives ONLY here. EntityEvents.spawned re-fires when a
        // chunk is reloaded from disk, and mult-based scaling compounds (mult^N) if
        // re-applied. The persistentData flag is serialized to the boss NBT so the
        // boost is applied exactly once across reloads/restarts. The boss population
        // is tiny, so the NBT cost is negligible (unlike writing it to every mob).
        if (!entity.persistentData.stats_boosted) {
            applyStats(entity, bossData);
            entity.persistentData.stats_boosted = true;
            if (DEBUG_LOG) {
                console.info(`[Mob Stats] Boosted boss: ${entityId} (Max Health: ${entity.maxHealth})`);
            }
        }
    } else {
        // --- GLOBAL CAP PATH (every other mob) ---
        // No persistentData read/write here: clamping is idempotent (Math.min / set to
        // cap), so re-running on a chunk reload is harmless and needs no guard. This
        // avoids forcing a CompoundTag allocation + NBT save bloat on every common mob.
        if (entity.maxHealth > CONFIG.MAX_HEALTH) {
            entity.maxHealth = CONFIG.MAX_HEALTH;
            entity.health = CONFIG.MAX_HEALTH;
        }
        let dmgAttr = entity.getAttribute('minecraft:generic.attack_damage');
        if (dmgAttr && dmgAttr.getBaseValue() > CONFIG.MAX_DAMAGE) {
            dmgAttr.setBaseValue(CONFIG.MAX_DAMAGE);
        }
    }
});

console.info("[Arcadia V2] Mob Stats Loaded.");
