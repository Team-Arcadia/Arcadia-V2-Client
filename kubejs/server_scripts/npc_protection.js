// Priority: 900

/*
    NPC Protection Script (Optimized)
    Prevents Easy NPC entities from being displaced or used as vehicles.
    Performance: Uses EntityEvents.tick instead of scanning levels.
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

    // --- OPTIMIZED ANCHORING & EJECTION ---
    // Using tick on each entity individually is much more efficient than level.getEntities()
    EntityEvents.tick(event => {
        const { entity } = event;
        
        // Quick exit for most entities
        if (!isEasyNpc(entity)) return;
        if (!isInSpawn(entity)) return;

        // Eject passengers (prevent vehicle exploits)
        if (entity.isPassenger()) {
            entity.stopRiding();
        }

        // Freeze NPC if it moves
        let vel = entity.deltaMovement;
        if (vel && (Math.abs(vel.x()) > 0.005 || Math.abs(vel.z()) > 0.005)) {
            entity.setDeltaMovement(0, vel.y(), 0);
            entity.setPosition(entity.x, entity.y, entity.z);
        }
    });
})();

console.info("[Arcadia V2] NPC protection system optimized (Lags fixed).");
