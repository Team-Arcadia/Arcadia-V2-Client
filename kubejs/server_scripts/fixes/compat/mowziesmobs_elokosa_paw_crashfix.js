// Priority: 10
/*
    Mowzie's Mobs — ItemElokosaPaw crash fix
    The mod's ItemElokosaPaw.use() references client-only classes
    (TextureSheetParticle, Minecraft, ParticleHandler) without proper
    side isolation. On a dedicated server, calling use() throws
    NoClassDefFoundError and crashes the server tick loop.
    This patch cancels the right-click server-side so use() is never reached.
    Author: vyrriox
*/

ItemEvents.rightClicked('mowziesmobs:elokosa_paw', event => {
    const { player, level } = event;
    if (level.isClientSide()) return;
    event.cancel();
    player.tell(Text.red("[Arcadia] Cet item est temporairement désactivé (bug serveur). | This item is temporarily disabled (server bug)."));
});

console.info("[Arcadia V2] Mowzie's Mobs Elokosa Paw crashfix loaded.");
