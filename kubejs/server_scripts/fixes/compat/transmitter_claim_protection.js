// Priority: 10
/*
    Create Ender Transmission — Claim Interaction Protection

    The Item / Energy / Fluid Transmitter blocks open a configuration screen on
    right-click (ItemTransmitterBlock.useItemOn -> displayScreen) WITHOUT checking
    FTB Chunks permissions. A non-allied player could right-click a transmitter
    inside someone else's claim, read its frequency code, and then siphon the base's
    items / energy / fluids from their own matching transmitter elsewhere.

    This patch gates right-click on all three transmitters through FTB Chunks'
    INTERACT_BLOCK protection: if the player is not allowed to interact with blocks
    in that claim, the interaction is cancelled before the screen ever opens.

    Author: vyrriox
    KubeJS 7.x / MC 1.21.1 NeoForge.
*/

(function () {
const FTBChunksAPI = Java.loadClass('dev.ftb.mods.ftbchunks.api.FTBChunksAPI');
const Protection = Java.loadClass('dev.ftb.mods.ftbchunks.api.Protection');

const PROTECTED_TRANSMITTERS = [
    'createendertransmission:item_transmitter',
    'createendertransmission:energy_transmitter',
    'createendertransmission:fluid_transmitter'
];

PROTECTED_TRANSMITTERS.forEach(blockId => {
    BlockEvents.rightClicked(blockId, event => {
        const player = event.getEntity();
        // Only gate real server players; fake players / non-players are out of scope here.
        if (!player || !player.isPlayer()) return;
        // Creative/OP staff are handled by FTB Chunks' own bypass check below.

        const api = FTBChunksAPI.api();
        if (!api.isManagerLoaded()) return;
        const manager = api.getManager();

        const pos = event.getBlock().getPos();
        const hand = event.getHand();

        // shouldPreventInteraction respects team allies, public/private claim settings
        // and the player's admin bypass flag.
        if (manager.shouldPreventInteraction(player, hand, pos, Protection.INTERACT_BLOCK, null)) {
            event.cancel();
            player.tell(Text.red("[Arcadia] Vous n'avez pas la permission d'utiliser ce transmetteur dans ce claim ! | You don't have permission to use this transmitter in this claim!"));
        }
    });
});

console.info("[Arcadia V2] Transmitter Claim Protection Loaded: Create Ender Transmission transmitters now respect FTB Chunks interact permissions.");
})();
