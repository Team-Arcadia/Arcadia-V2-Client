// Priority: 10
/*
    Mowzie's Mobs - Elokosa Paw crash fix
    ItemElokosaPaw.use() references client-only classes (Minecraft,
    ParticleHandler, AdvancedParticleBase) without side isolation. On a
    dedicated server, using any paw throws NoClassDefFoundError and crashes
    the server tick loop.
    Mowzie's Mobs 1.8.2 registers one item per moon phase and no plain
    "mowziesmobs:elokosa_paw" item, so every phase is listed here. The first
    version of this patch targeted that non-existent id and never fired.
    Using a paw on another player still goes through use(), so cancelling the
    right-click covers both cases.
    Author: vyrriox
*/

const ELOKOSA_PAWS = [
    'mowziesmobs:elokosa_paw_full',
    'mowziesmobs:elokosa_paw_gibbous',
    'mowziesmobs:elokosa_paw_half',
    'mowziesmobs:elokosa_paw_crescent',
    'mowziesmobs:elokosa_paw_new'
];

ELOKOSA_PAWS.forEach(pawId => {
    ItemEvents.rightClicked(pawId, event => {
        const { player, level } = event;
        if (level.isClientSide()) return;
        event.cancel();
        player.tell(Text.red("[Arcadia] Cet item est temporairement désactivé (bug serveur). | This item is temporarily disabled (server bug)."));
    });
});

console.info(`[Arcadia V2] Mowzie's Mobs Elokosa Paw crashfix loaded (${ELOKOSA_PAWS.length} paws).`);
