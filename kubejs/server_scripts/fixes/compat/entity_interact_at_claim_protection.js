// Priority: 10
/*
    Entity "interact at" — Claim Interaction Protection

    FTB Chunks only covers half of the vanilla entity right-click path:
    - PlayerInteractEvent.EntityInteract (the INTERACT packet) is gated by its own
      architectury handler.
    - PlayerInteractEvent.EntityInteractSpecific (the INTERACT_AT packet) has no
      handler at all. Armor stands are covered instead by a mixin injected into
      ArmorStand.interactAt, which only helps entities that actually reach that
      method.

    Any mod that answers INTERACT_AT from the event itself therefore runs before
    the mixin and is never checked against the claim. Straw Statues does exactly
    that: StrawStatue.onUseEntityAt opens the statue menu (full equipment access)
    from a puzzleslib USE_ENTITY_AT listener, so sneak + empty hand let anyone
    strip a statue standing in someone else's claim (ticket #248). The same
    listener also lets a player head rewrite the statue's skin before the vanilla
    interactAt path is reached.

    This patch adds the missing half: INTERACT_AT is gated through the same
    FTB Chunks INTERACT_ENTITY protection the INTERACT path already uses, at
    HIGHEST priority so it lands before any mod listener consumes the event.

    Author: vyrriox
    KubeJS 7.x / MC 1.21.1 NeoForge.
*/

(function () {
const FTBChunksAPI = Java.loadClass('dev.ftb.mods.ftbchunks.api.FTBChunksAPI');
const Protection = Java.loadClass('dev.ftb.mods.ftbchunks.api.Protection');
const EventPriority = Java.loadClass('net.neoforged.bus.api.EventPriority');
const InteractionResult = Java.loadClass('net.minecraft.world.InteractionResult');
const InteractionHand = Java.loadClass('net.minecraft.world.InteractionHand');
const EntityInteractSpecific = Java.loadClass('net.neoforged.neoforge.event.entity.player.PlayerInteractEvent$EntityInteractSpecific');

NativeEvents.onEvent(EventPriority.HIGHEST, EntityInteractSpecific, event => {
    const level = event.getLevel();
    if (!level || level.isClientSide()) return;

    const player = event.getEntity();
    const target = event.getTarget();
    if (!player || !target) return;

    const api = FTBChunksAPI.api();
    if (!api.isManagerLoaded()) return;
    const manager = api.getManager();

    // Protect based on the chunk the TARGET entity occupies, not the player's.
    // shouldPreventInteraction respects team allies, public/private claim settings
    // and the player's admin bypass flag.
    const hand = event.getHand();
    if (!manager.shouldPreventInteraction(player, hand, target.blockPosition(), Protection.INTERACT_ENTITY, target)) return;

    event.setCanceled(true);
    event.setCancellationResult(InteractionResult.FAIL);

    // The client retries with the off hand once the main hand fails, so only the
    // main-hand pass talks, otherwise every blocked click prints twice.
    if (hand.equals(InteractionHand.MAIN_HAND)) {
        player.tell(Text.red("[Arcadia] Vous n'avez pas la permission d'interagir avec cette entité dans ce claim ! | You don't have permission to interact with this entity in this claim!"));
    }
});

console.info("[Arcadia V2] Entity Interact-At Claim Protection Loaded: INTERACT_AT now respects FTB Chunks entity-interact permissions (straw statues and any other interactAt-driven menu).");
})();
