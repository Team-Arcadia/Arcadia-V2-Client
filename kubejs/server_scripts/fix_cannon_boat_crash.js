// Priority: 1000
/*
    Fix for Supplementaries Cannon Boat crash with PlundererEntity.
    Prevents Plunderers from riding cannon boats and cleans up problematic entities.
    Author: vyrriox
*/

const CANNON_BOAT = 'supplementaries:cannon_boat';
const PLUNDERER_TYPE = 'friendsandfoes:plunderer'; // Probable ID, using partial match for safety

/**
 * Checks if an entity is a Plunderer.
 * @param {Internal.Entity} entity 
 * @returns {boolean}
 */
function isPlunderer(entity) {
    if (!entity) return false;
    let type = entity.type.toString();
    return type.includes('plunderer');
}

// 1. Core Protection: Eject any Plunderer from Cannon Boats when the boat spawns
EntityEvents.spawned(CANNON_BOAT, event => {
    let boat = event.entity;
    event.server.scheduleInTicks(1, () => {
        if (!boat || !boat.isAlive()) return;
        boat.passengers.forEach(passenger => {
            if (isPlunderer(passenger)) {
                passenger.stopRiding();
                console.info(`[Arcadia Fix] Ejected ${passenger.type} from ${CANNON_BOAT} on spawn.`);
            }
        });
    });
});

// 2. Continuous Safety Net: Periodically check all Cannon Boats for Plunderer passengers
// This covers cases where they might join after spawning or if the spawn event was missed.
// We run this every 100 ticks (5 seconds) to avoid overhead.
LevelEvents.tick(event => {
    if (event.level.time % 100 != 0) return;
    
    event.level.getEntities().filter(e => e.type == CANNON_BOAT).forEach(boat => {
        boat.passengers.forEach(passenger => {
            if (isPlunderer(passenger)) {
                passenger.stopRiding();
                console.info(`[Arcadia Fix] Forcefully ejected ${passenger.type} from ${boat.type} during periodic check.`);
            }
        });
    });
});

console.info("[Arcadia V2] Cannon Boat Crash Fix Loaded: Plunderer riding restricted.");
