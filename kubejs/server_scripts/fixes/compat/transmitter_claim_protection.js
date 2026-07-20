// Priority: 10
/*
    Create Addons — Claim Interaction Protection

    Several Create addon blocks open configuration UIs on right-click WITHOUT
    checking FTB Chunks permissions:
    - Create Ender Transmission Item/Energy/Fluid Transmitters expose their
      frequency code, letting outsiders siphon a base's items/energy/fluids.
    - Create Dreams and Desires Omni Speed Controller and Smart Hopper let
      outsiders change speed values and filters (bug report #214).

    This patch gates right-click on those blocks through FTB Chunks'
    INTERACT_BLOCK protection: if the player is not allowed to interact with
    blocks in that claim, the interaction is cancelled before the UI ever opens.

    Author: vyrriox
    KubeJS 7.x / MC 1.21.1 NeoForge.
*/

(function () {
const FTBChunksAPI = Java.loadClass('dev.ftb.mods.ftbchunks.api.FTBChunksAPI');
const Protection = Java.loadClass('dev.ftb.mods.ftbchunks.api.Protection');

const PROTECTED_BLOCKS = [
    // Create Ender Transmission
    'createendertransmission:item_transmitter',
    'createendertransmission:energy_transmitter',
    'createendertransmission:fluid_transmitter',
    // Create Dreams and Desires (#214)
    'dndesires:omni_speed_controller',
    'dndesires:smart_hopper'
];

PROTECTED_BLOCKS.forEach(blockId => {
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
            player.tell(Text.red("[Arcadia] Vous n'avez pas la permission d'utiliser ce bloc dans ce claim ! | You don't have permission to use this block in this claim!"));
        }
    });
});

console.info("[Arcadia V2] Claim Protection Loaded: Ender Transmission transmitters and DnDesires blocks now respect FTB Chunks interact permissions.");
})();
