// Priority: 10
/*
    Blaze Burner Exploit Patch
    Prevents Blaze Burners from being moved by Create contraptions (minecarts, etc.)
    and blocks picking them up with a wrench or breaking them in the Nether.
    Author: vyrriox
*/

ServerEvents.tags('block', event => {
    // Prevent Create contraptions from moving Blaze Burners
    event.add('create:unmovable', 'create:blaze_burner');
});

BlockEvents.rightClicked('create:blaze_burner', event => {
    const { player, level, block, hand, item } = event;
    
    // Check if player is holding a Create Wrench
    if (item.hasTag('create:wrench')) {
        // Block wrench interaction in the Nether to prevent picking up generated burners
        if (level.dimension === 'minecraft:the_nether') {
            if (!player.isCreative()) {
                event.cancel();
                player.tell(Text.red("[Arcadia] Vous ne pouvez pas ramasser ce Blaze Burner dans le Nether ! | You cannot pick up this Blaze Burner in the Nether!"));
            }
        }
    }
});

BlockEvents.broken('create:blaze_burner', event => {
    const { player, level, block } = event;
    
    // Prevent breaking Blaze Burners in the Nether (except in Creative)
    if (level.dimension === 'minecraft:the_nether') {
        if (!player.isCreative()) {
            event.cancel();
            player.tell(Text.red("[Arcadia] Le Blaze Burner est scellé dans cette dimension ! | The Blaze Burner is sealed in this dimension!"));
        }
    }
});

console.info("[Arcadia V2] Blaze Burner Exploit Patch Loaded: Unmovable tag added and Nether interactions restricted.");
