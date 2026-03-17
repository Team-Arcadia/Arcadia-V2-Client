// Priority: 800

/**
 * Mob Stats Script
 * Adjusts the attributes (Health, Damage, etc.) of specific mobs and enforces global caps.
 * Author: vyrriox
 * Optimized for KubeJS 1.21.1
 */

const CONFIG = {
    MAX_HEALTH: 10000,
    MAX_DAMAGE: 50,
    MAX_ARMOR: 50
};

// Boss data and multipliers for O(1) lookup
const BOSS_DATA = {
    // Vanilla
    'minecraft:wither': { hp: 500 },
    'minecraft:ender_dragon': { hp: 2000 },
    'minecraft:warden': { hp: 1000 },

    // Twilight Forest
    'twilightforest:naga': { mult: 1.2 },
    'twilightforest:lich': { mult: 1.2 },
    'twilightforest:minoshroom': { mult: 1.2 },
    'twilightforest:hydra': { mult: 1.2 },
    'twilightforest:knight_phantom': { mult: 1.2 },
    'twilightforest:ur_ghast': { mult: 1.2 },
    'twilightforest:alpha_yeti': { mult: 1.2 },
    'twilightforest:snow_queen': { mult: 1.2 },
    'twilight_forest_final_boss:castle_keeper': { mult: 4.0 },

    // Aether
    'aether:slider': { mult: 1.5 },
    'aether:valkyrie_queen': { mult: 1.5 },
    'aether:sun_spirit': { mult: 1.5 },

    // Ars Nouveau
    'ars_nouveau:wilden_boss': { mult: 1.2 },
    'ars_nouveau:wilden_guardian': { mult: 1.2 },
    'ars_nouveau:wilden_stalker': { mult: 1.2 },
    'ars_nouveau:wilden_hunter': { mult: 1.2 },

    // Deeper and Darker
    'deeperdarker:shriek_worm': { mult: 1.4 },
    'deeperdarker:stalker': { mult: 1.4 },
    'deeperdarker:sculk_snapper': { mult: 1.4 },
    'deeperdarker:shattered': { mult: 1.4 },

    // Iron's Spells 'n Spellbooks
    'irons_spellbooks:dead_king': { mult: 1.2 },
    'irons_spellbooks:dead_king_corpse': { mult: 1.2 },
    'irons_spellbooks:archevoker': { mult: 1.2 },
    'irons_spellbooks:necromancer': { mult: 1.2 },
    'irons_spellbooks:priest': { mult: 1.2 },
    'irons_spellbooks:citadel_keeper': { mult: 1.2 },

    // Mutant Monsters
    'mutantmonsters:mutant_creeper': { mult: 1.2 },
    'mutantmonsters:mutant_zombie': { mult: 1.2 },
    'mutantmonsters:mutant_skeleton': { mult: 1.2 },
    'mutantmonsters:mutant_enderman': { mult: 1.2 },
    'mutantmonsters:mutant_snow_golem': { mult: 1.2 },
    'mutantmonsters:spider_pig': { mult: 1.2 },

    // Mowzie's Mobs
    'mowziesmobs:ferrous_wroughtnaut': { mult: 1.2 },
    'mowziesmobs:frostmaw': { mult: 1.2 },
    'mowziesmobs:naga': { mult: 1.2 },
    'mowziesmobs:umvuthi': { mult: 1.2 },

    // Knight Quest
    'knightquest:netherman': { mult: 1.2 },
    'knightquest:eldknight': { mult: 1.2 },
    'knightquest:ratman': { mult: 1.2 },
    'knightquest:swampman': { mult: 1.2 }
};

/**
 * Helper function to boost entity attributes safely with capping.
 */
function applyStats(entity, data) {
    if (!entity.isLiving()) return;

    // Apply Health
    if (data.hp || data.mult) {
        let currentMax = entity.getAttributeValue('minecraft:generic.max_health');
        let newMax = data.hp ? data.hp : (currentMax * (data.mult || 1));
        
        // Clamp to global max
        newMax = Math.min(newMax, CONFIG.MAX_HEALTH);
        
        entity.setAttributeBaseValue('minecraft:generic.max_health', newMax);
        entity.health = newMax;
    }

    // Apply Attack Damage (only if mult exists and entity has the attribute)
    if (data.mult && entity.attributes.hasAttribute('minecraft:generic.attack_damage')) {
        let currentDmg = entity.getAttributeValue('minecraft:generic.attack_damage');
        let newDmg = Math.min(currentDmg * data.mult, CONFIG.MAX_DAMAGE);
        entity.setAttributeBaseValue('minecraft:generic.attack_damage', newDmg);
    }

    // Apply Armor (only if mult exists and entity has the attribute)
    if (data.mult && entity.attributes.hasAttribute('minecraft:generic.armor')) {
        let currentArmor = entity.getAttributeValue('minecraft:generic.armor');
        let newArmor = Math.min(currentArmor * data.mult, CONFIG.MAX_ARMOR);
        entity.setAttributeBaseValue('minecraft:generic.armor', newArmor);
    }
}

EntityEvents.spawned(event => {
    const entity = event.entity;

    // Skip non-living or players
    if (!entity || !entity.isLiving() || entity.isPlayer()) return;

    const entityId = entity.type.id;

    // --- Optimization: Check if already boosted or needs boosting ---
    if (!entity.persistentData.stats_boosted) {
        const bossData = BOSS_DATA[entityId];
        
        if (bossData) {
            applyStats(entity, bossData);
            console.log(`[Mob Stats] Boosted ${entityId} -> New Health: ${entity.health}`);
        } else {
            // Global clamping for non-bosses that might spawn with extreme stats
            let needsClamping = false;
            
            if (entity.getAttributeValue('minecraft:generic.max_health') > CONFIG.MAX_HEALTH) {
                entity.setAttributeBaseValue('minecraft:generic.max_health', CONFIG.MAX_HEALTH);
                entity.health = CONFIG.MAX_HEALTH;
                needsClamping = true;
            }

            if (entity.attributes.hasAttribute('minecraft:generic.attack_damage')) {
                if (entity.getAttributeValue('minecraft:generic.attack_damage') > CONFIG.MAX_DAMAGE) {
                    entity.setAttributeBaseValue('minecraft:generic.attack_damage', CONFIG.MAX_DAMAGE);
                    needsClamping = true;
                }
            }

            if (entity.attributes.hasAttribute('minecraft:generic.armor')) {
                if (entity.getAttributeValue('minecraft:generic.armor') > CONFIG.MAX_ARMOR) {
                    entity.setAttributeBaseValue('minecraft:generic.armor', CONFIG.MAX_ARMOR);
                    needsClamping = true;
                }
            }
            
            if (needsClamping) {
                console.log(`[Mob Stats] Clamped stats for ${entityId}`);
            }
        }

        entity.persistentData.stats_boosted = true;
    }
});

console.info("[Arcadia V2] Mob Stats Loaded.");

