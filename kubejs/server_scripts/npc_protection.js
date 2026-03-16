// Priority: 900

/*
    NPC Protection Script (Optimized & mortal)
    Prevents Easy NPC entities from being displaced by spells, items, or knockback.
    Performance: Uses EntityEvents.tick (local) instead of LevelEvents.tick (global scan).
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

    // --- OPTIMIZED ANCHORING ---
    // This event only triggers for the ticking entity, no global level scan.
    EntityEvents.tick(event => {
        const { entity } = event;
        
        // Quick filter
        if (!isEasyNpc(entity)) return;
        if (!isInSpawn(entity)) return;

        // Eject passengers (prevents using NPC as a carry-on vehicle)
        if (entity.isPassenger()) {
            entity.stopRiding();
        }

        // Freeze Position if velocity detected (Knockback, Spells, Pulling)
        let vel = entity.deltaMovement;
        if (vel && (Math.abs(vel.x()) > 0.005 || Math.abs(vel.z()) > 0.005)) {
            // Cancel horizontal velocity
            entity.setDeltaMovement(0, vel.y(), 0);
            // Snap back to precise coordinate to combat micro-displacements
            entity.setPosition(entity.x, entity.y, entity.z);
        }
    });
})();

console.info("[Arcadia V2] NPC Anchoring system active (Mortal but Immovable).");
