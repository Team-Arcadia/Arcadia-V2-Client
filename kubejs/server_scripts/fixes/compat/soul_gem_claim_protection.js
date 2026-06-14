// Priority: 10
/*
    Occultism Soul Gem — Claim Interaction Protection

    Occultism's SoulGemItem.interactLivingEntity captures a mob on right-click and
    only checks its entity-type deny tags (SOUL_GEM_DENY_LIST etc.) — it never checks
    FTB Chunks permissions. A non-allied player could walk into someone else's claim
    and pocket their mobs (animals, golems, mounts, summons) with any tier of gem.

    This patch gates Soul Gem / Trinity Gem use-on-entity through FTB Chunks'
    INTERACT_ENTITY protection: if the player can't interact with entities in the
    claim the target stands in, the capture is cancelled. Covers all gem tiers
    (fragile / soul / trinity) and their empty/filled variants.

    Author: vyrriox
    KubeJS 7.x / MC 1.21.1 NeoForge.
*/

(function () {
const FTBChunksAPI = Java.loadClass('dev.ftb.mods.ftbchunks.api.FTBChunksAPI');
const Protection = Java.loadClass('dev.ftb.mods.ftbchunks.api.Protection');

// All capturing gem item IDs across every tier and empty/filled state. Filled gems
// don't capture, but gating them too is harmless and future-proofs against variants.
const SOUL_GEMS = [
    'occultism:soul_gem',
    'occultism:soul_gem_empty',
    'occultism:fragile_soul_gem',
    'occultism:fragile_soul_gem_empty',
    'occultism:trinity_gem',
    'occultism:trinity_gem_empty'
];

SOUL_GEMS.forEach(gemId => {
    ItemEvents.entityInteracted(gemId, event => {
        const player = event.getEntity();
        if (!player || !player.isPlayer()) return;
        // Creative/OP staff are handled by FTB Chunks' own bypass check below.

        const target = event.getTarget();
        if (!target) return;

        const api = FTBChunksAPI.api();
        if (!api.isManagerLoaded()) return;
        const manager = api.getManager();

        // Protect based on the chunk the TARGET entity occupies, not the player's.
        const pos = target.blockPosition();
        const hand = event.getHand();

        if (manager.shouldPreventInteraction(player, hand, pos, Protection.INTERACT_ENTITY, target)) {
            event.cancel();
            player.tell(Text.red("[Arcadia] Vous ne pouvez pas capturer une créature dans ce claim ! | You cannot capture a creature in this claim!"));
        }
    });
});

console.info("[Arcadia V2] Soul Gem Claim Protection Loaded: Occultism gems now respect FTB Chunks entity-interact permissions.");
})();
