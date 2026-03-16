// Priority: 100

/*
    Disable Guide Books Script
    Removes guide books/atlases that are given to players on join by certain mods
    where configuration options are missing or ineffective.
    Author: vyrriox
*/

PlayerEvents.loggedIn(event => {
    // We use a stage to persistentlly track if we've checked this player
    // This ensures we only do this once (on first join)
    if (!event.player.stages.has('starting_items_checked')) {
        event.player.stages.add('starting_items_checked');
        
        // Give a 1-second delay (20 ticks) to ensure the mod has already given the item
        event.server.scheduleInTicks(20, callback => {
            const player = callback.data.player;
            if (player) {
                // Remove Parcool Atlas
                player.inventory.clear('parcool:atlas');
                
                // Backup check for other potential Parcool items if the ID was different
                player.inventory.clear('parcool:parcool_guide');
                
                console.info(`[Arcadia V2] Cleared starting guide books for player ${player.username}`);
            }
        });
    }
});

console.info("[Arcadia V2] Disable Guide Books Script Loaded.");
