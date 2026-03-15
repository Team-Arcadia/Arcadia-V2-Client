// Priority: 100

/*
    Fix for Ars Nouveau EntitySpellArrow crash due to missing caster (e.g. offline player).
    Author: vyrriox
*/

EntityEvents.spawned('ars_nouveau:spell_arrow', event => {
    let arrow = event.entity;
    
    let checkedForOwner = false;

    let checkArrow = () => {
        // If the arrow is already removed or dead, stop checking.
        if (!arrow || !arrow.isAlive() || arrow.isRemoved()) {
            return false;
        }
        
        // If the owner is missing (null)
        if (arrow.owner == null) {
            // Only check NBT once to see if it's an orphaned player arrow
            if (!checkedForOwner) {
                let nbt = arrow.nbt;
                if (nbt && nbt.hasUUID("Owner")) {
                    console.info("[Ars Nouveau Fix] Discarding orphaned spell_arrow to prevent server crash (Owner is disconnected or unloaded).");
                    arrow.discard();
                    return false; 
                }
                checkedForOwner = true;
            }
            // If we already checked and didn't discard, it might be a turret arrow.
            // We return false to stop the reschedule loop.
            return false;
        }
        return true; // Valid owner exists, continue checking
    };
    
    // Check immediately upon spawning
    if (!checkArrow()) {
        event.cancel(); // Cancel spawn if invalid
        return;
    }
    
    // Schedule a continuous check every tick while the arrow exists
    event.server.scheduleInTicks(1, callback => {
        if (checkArrow()) {
            callback.reschedule(1);
        }
    });
});

console.info("[Ars Nouveau Fix] Loaded: EntitySpellArrow null caster patch.");
