// Priority: 1000
/*
    Fix for Supplementaries Cannon Boat server crash.
    The CannonBoatEntity crashes during tick when a player fires the cannon.
    This is a Supplementaries mod bug - the only fix is to prevent cannon boats from existing.
    Author: vyrriox

    Strategy:
    - Kill cannon boat entities on spawn (prevents the crash entirely)
    - Eject any passengers before killing
    - Ban item handled separately in ban_items.js
*/

// Kill cannon boats immediately on spawn - prevents crash during entity tick
EntityEvents.spawned('supplementaries:cannon_boat', event => {
    let boat = event.entity;

    // Eject all passengers first (so players don't get killed with it)
    if (boat.passengers && boat.passengers.length > 0) {
        for (let i = 0; i < boat.passengers.length; i++) {
            let passenger = boat.passengers[i];
            if (passenger) {
                passenger.stopRiding();
                if (passenger.isPlayer()) {
                    passenger.tell(Text.red("[Arcadia] Les Cannon Boats sont interdits (crash serveur) ! | Cannon Boats are banned (server crash)!"));
                }
            }
        }
    }

    // Kill the entity to prevent the crash
    boat.discard();
    console.info("[Arcadia Fix] Cannon boat destroyed on spawn to prevent server crash.");
});

console.info("[Arcadia V2] Cannon Boat Crash Fix Loaded: Cannon boats are killed on spawn.");
