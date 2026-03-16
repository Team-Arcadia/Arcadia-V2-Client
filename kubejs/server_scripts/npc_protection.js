// Priority: 900

/*
    NPC Protection Script (Ultra-Optimized)
    Prevents Easy NPC entities from being displaced by any means (Leads, Spells, Fishing Rods).
    Approach: Track NPCs in a list and freeze them every tick.
    Author: vyrriox
*/

(function() {
    const SPAWN_DIM = "arcadia:spawn";
    const FORBIDDEN_NPC_ITEMS = [
        "apothic_enchanting:ender_lead",
        "apothic_enchanting:flimsy_ender_lead",
        "apothic_enchanting:occult_ender_lead",
        "minecraft:lead",
        "minecraft:fishing_rod"
    ];

    let protectedNpcs = [];

    function isEasyNpc(entity) {
        if (!entity || !entity.type) return false;
        return String(entity.type).startsWith("easy_npc:");
    }

    function isInSpawn(entity) {
        if (!entity || !entity.level) return false;
        return String(entity.level.dimension) === SPAWN_DIM;
    }

    // --- TRACKING ---
    // Update list periodically to avoid memory leaks and find new NPCs
    LevelEvents.tick(event => {
        const { level, server } = event;
        
        // Comprehensive refresh every 5 seconds (100 ticks)
        if (server.tickCount % 100 === 0 && String(level.dimension) === SPAWN_DIM) {
            protectedNpcs = level.getEntities().filter(e => isEasyNpc(e));
        }

        // --- TICK ANCHORING ---
        // Run every tick but only on already filtered NPCs (Highly performant)
        if (String(level.dimension) === SPAWN_DIM) {
            protectedNpcs.forEach(entity => {
                if (!entity || !entity.isAlive()) return;

                // Eject passengers
                if (entity.isPassenger()) {
                    entity.stopRiding();
                }

                // Rigid Anchoring
                let vel = entity.deltaMovement;
                if (vel && (Math.abs(vel.x()) > 0.001 || Math.abs(vel.z()) > 0.001)) {
                    entity.setDeltaMovement(0, vel.y(), 0);
                    entity.setPosition(entity.x, entity.y, entity.z);
                }
            });
        }
    });

    // --- INTERACTION BLOCKING ---
    ItemEvents.entityInteracted(event => {
        const { item, target, player } = event;
        if (!isInSpawn(target)) return;
        
        const itemId = String(item.id);
        if (FORBIDDEN_NPC_ITEMS.some(id => itemId === id) && isEasyNpc(target)) {
            event.cancel();
            player.tell(Text.red(`[Arcadia] Impossible d'utiliser cet objet sur un PNJ ! | Practicality forbidden on NPCs!`));
        }
    });

})();

console.info("[Arcadia V2] NPC Anchoring system active (Ultra-Performance with Lead protection).");
