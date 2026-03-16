// Priority: 900

/*
    NPC Protection Script (Fixed & Optimized)
    Prevents Easy NPC entities from being displaced by spells, items, or knockback.
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

    function isEasyNpc(entity) {
        if (!entity || !entity.type) return false;
        return String(entity.type).startsWith("easy_npc:");
    }

    function isInSpawn(entity) {
        if (!entity || !entity.level) return false;
        return String(entity.level.dimension) === SPAWN_DIM;
    }

    // --- INTERACTION BLOCKING ---
    ItemEvents.entityInteracted(event => {
        const { item, target, player } = event;
        if (!isInSpawn(target)) return;

        if (FORBIDDEN_NPC_ITEMS.includes(String(item.id)) && isEasyNpc(target)) {
            event.cancel();
            player.tell(Text.red(`[Arcadia] Impossible d'utiliser cet objet sur un PNJ ici !`));
        }
    });

    // --- KNOCKBACK PREVENTION (The most performant way) ---
    EntityEvents.hurt(event => {
        const { entity } = event;
        if (isEasyNpc(entity) && isInSpawn(entity)) {
            // Cancel knockback / displacement from damage
            event.entity.setDeltaMovement(0, 0, 0); 
        }
    });

    // --- PERIODIC ANCHORING (Safety check) ---
    LevelEvents.tick(event => {
        const { level, server } = event;
        
        // Check every 1 second (20 ticks) only in SPAWN
        if (server.tickCount % 20 !== 0) return;
        if (String(level.dimension) !== SPAWN_DIM) return;

        // Optimized scan: no logs, strict filtering
        level.getEntities().forEach(entity => {
            if (isEasyNpc(entity)) {
                // Eject passengers
                if (entity.isPassenger()) {
                    entity.stopRiding();
                }

                // Minor position correction if displaced (backup check)
                let vel = entity.deltaMovement;
                if (vel && (Math.abs(vel.x()) > 0.01 || Math.abs(vel.z()) > 0.01)) {
                    entity.setDeltaMovement(0, vel.y(), 0);
                    entity.setPosition(entity.x, entity.y, entity.z);
                }
            }
        });
    });
})();

console.info("[Arcadia V2] NPC protection system fixed (Compatibility and Performance).");
