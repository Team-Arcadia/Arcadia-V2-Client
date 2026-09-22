// Priority: 10
/*
    Ars Nouveau Blink + Warp Scroll — destination preload (ticket #448, follows #231)

    Blink cast on another entity with a bound warp scroll in the off hand sends
    that entity to the scroll's destination through PortalTile.teleportEntityTo.
    Ars 5.13.1 reads the destination block (getBlockState) BEFORE it adds its
    chunk ticket, so a destination chunk that is not loaded is loaded
    synchronously on the server thread. With the chunk workers busy generating
    terrain for players exploring far out, that wait stalled Server1 for 4 min
    40 s on 2026-09-21 (22:13:23 to 22:18:04): every player timed out, just
    under the 300 s watchdog, so no crash report was written.

    This patch cancels the Blink warp while the destination chunk is not
    loaded, asks the server to load it in the background with the same PORTAL
    ticket Ars would add, and tells the caster to cast again. The second cast
    finds the chunk loaded and warps instantly. Self-cast Blink and Blink
    without a scroll are untouched.

    Not covered: a scroll held in the inventory of a spell turret (TileCaster
    path), which reaches the same code without an off-hand item.

    Author: vyrriox
    KubeJS 7.x / MC 1.21.1 NeoForge.
*/

(function () {
const EventPriority = Java.loadClass('net.neoforged.bus.api.EventPriority');
const EffectResolvePre = Java.loadClass('com.hollingsworth.arsnouveau.api.event.EffectResolveEvent$Pre');
const EffectBlink = Java.loadClass('com.hollingsworth.arsnouveau.common.spell.effect.EffectBlink');
const PortalTile = Java.loadClass('com.hollingsworth.arsnouveau.common.block.tile.PortalTile');
const DataComponentRegistry = Java.loadClass('com.hollingsworth.arsnouveau.setup.registry.DataComponentRegistry');
const EntityHitResult = Java.loadClass('net.minecraft.world.phys.EntityHitResult');
const ServerLevel = Java.loadClass('net.minecraft.server.level.ServerLevel');
const TicketType = Java.loadClass('net.minecraft.server.level.TicketType');
const ChunkPos = Java.loadClass('net.minecraft.world.level.ChunkPos');

NativeEvents.onEvent(EventPriority.HIGHEST, EffectResolvePre, event => {
    if (!(event.resolveEffect instanceof EffectBlink)) return;
    if (!(event.rayTraceResult instanceof EntityHitResult)) return;

    const world = event.world;
    if (!(world instanceof ServerLevel)) return;

    const shooter = event.shooter;
    const target = event.rayTraceResult.getEntity();
    if (!shooter || !target || target === shooter) return;

    const scroll = shooter.getOffhandItem().get(DataComponentRegistry.WARP_SCROLL.get());
    if (!scroll || !scroll.isValid() || !scroll.canTeleportWithDim(world)) return;

    const destLevel = PortalTile.getServerLevel(scroll.dimension(), world);
    if (!destLevel) return;

    const pos = scroll.pos().get();
    const chunk = new ChunkPos(pos);
    if (destLevel.getChunkSource().hasChunk(chunk.x, chunk.z)) return;

    event.setCanceled(true);
    destLevel.getChunkSource().addRegionTicket(TicketType.PORTAL, chunk, 3, pos);
    if (shooter.isPlayer()) {
        shooter.tell(Text.gold('The warp destination is loading, cast Blink again in a few seconds. / La destination se charge, relance Blink dans quelques secondes.'));
    }
    console.info(`[Arcadia] Blink warp delayed until ${scroll.dimension()} ${pos.getX()} ${pos.getY()} ${pos.getZ()} is loaded`);
});

console.info('[Arcadia] Ars Blink warp preload guard loaded');
})();
