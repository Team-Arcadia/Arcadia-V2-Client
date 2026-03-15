// Priority: 100
/*
    ReviveMe & Sophisticated Backpacks Feeding Fix
    Prevents the Feeding Upgrade from infinitely consuming food when a player is in the fallen state.
    This works by stabilizing the player's hunger/saturation levels while downed.
    Author: vyrriox
*/

PlayerEvents.tick(event => {
    const { player, level, server } = event;
    
    // Only run on server and every 20 ticks to save performance (once per second)
    if (level.isClientSide() || server.tickCount % 20 !== 0) return;

    // Detect if player is downed using effects (much faster than NBT check)
    // ReviveMe usually applies slowness 3+ and blindness
    let isFallen = false;
    
    if (player.hasEffect('minecraft:slowness') && 
        player.getEffect('minecraft:slowness').amplifier >= 3 && 
        player.hasEffect('minecraft:blindness')) {
        isFallen = true;
    }

    // Fallback to NBT only if effects are not present, to ensure compatibility
    if (!isFallen) {
        let nbt = player.nbt;
        if (nbt) {
            isFallen = nbt.contains('reviveme:fallen') || 
                       nbt.getBoolean('reviveme_fallen') || 
                       nbt.getBoolean('reviveme:is_fallen');
        }
    }

    if (isFallen) {
        // Stabilize hunger to prevent feeding upgrade from firing
        if (player.foodLevel < 20) {
            player.foodLevel = 20;
            player.saturation = 20;
        }
    }
});

console.info("[Arcadia V2] ReviveMe Feeding Fix Loaded.");
