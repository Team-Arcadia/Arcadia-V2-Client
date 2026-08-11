/*
    Redstone Link drop tracer for Arcadia V2 (ticket #218), TEMPORARY.
    Optimized for KubeJS 1.21.1 (NeoForge).
    Created by vyrriox.

    Why:
      Redstone Links are reported as duplicating when a Create piston
      contraption is turned back into blocks. Static analysis rules out the
      block-entity drop path: Contraption.removeBlocksFromWorld calls
      removeBlockEntity before clearing the position, so IBE.onRemove never
      reaches SmartBlockEntity.destroy, and LinkBehaviour drops nothing either.
      What is left are the three drop sites inside Contraption.addBlocksToWorld
      and a possible double capture, which cannot be told apart without seeing
      the call that actually spawns the item.

    What it does:
      Logs a stack trace for every redstone link item entity that spawns on the
      server, with its position and the block sitting there. One reproduction is
      enough to name the exact caller. Nothing is cancelled or altered.

    How to use:
      Reproduce the bug once, then read logs/latest.log and search for
      [Arcadia][diag]. Set ENABLED to false, or delete this file, once ticket
      #218 is closed.
*/

const DIAG_ENABLED = true;
const DIAG_MAX_REPORTS = 12;
const DIAG_TRACKED_ITEM = 'create:redstone_link';
const DIAG_FRAME_LIMIT = 30;

let diagReports = 0;

function formatDiagTrace(throwable) {
    const frames = throwable.getStackTrace();
    const lines = [];

    for (let i = 0; i < frames.length && lines.length < DIAG_FRAME_LIMIT; i++) {
        const frame = String(frames[i]);
        // Rhino, KubeJS and the event bus glue add dozens of frames that say
        // nothing about who spawned the item.
        if (frame.indexOf('dev.latvian') === 0) continue;
        if (frame.indexOf('net.neoforged.bus') === 0) continue;
        if (frame.indexOf('java.') === 0) continue;
        if (frame.indexOf('jdk.') === 0) continue;
        lines.push('    at ' + frame);
    }

    return lines.join('\n');
}

function installRedstoneLinkTracer() {
    const BuiltInRegistries = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries');
    const ResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation');
    const Items = Java.loadClass('net.minecraft.world.item.Items');
    const ItemEntity = Java.loadClass('net.minecraft.world.entity.item.ItemEntity');
    const Throwable = Java.loadClass('java.lang.Throwable');
    const EventPriority = Java.loadClass('net.neoforged.bus.api.EventPriority');
    const EntityJoinLevelEvent = Java.loadClass('net.neoforged.neoforge.event.entity.EntityJoinLevelEvent');

    const tracked = BuiltInRegistries.ITEM.get(ResourceLocation.parse(DIAG_TRACKED_ITEM));
    if (tracked === null || tracked === Items.AIR) {
        console.error('[Arcadia][diag] ' + DIAG_TRACKED_ITEM + ' not found, redstone link tracer inactive.');
        return;
    }

    NativeEvents.onEvent(EventPriority.LOWEST, EntityJoinLevelEvent, event => {
        if (diagReports >= DIAG_MAX_REPORTS) return;

        const level = event.getLevel();
        if (level === null || level.isClientSide()) return;

        const entity = event.getEntity();
        if (!ItemEntity.isInstance(entity)) return;

        const stack = entity.getItem();
        if (stack.getItem() !== tracked) return;

        diagReports++;
        const pos = entity.blockPosition();
        console.info('[Arcadia][diag] Redstone link drop #' + diagReports
            + ' x' + stack.getCount()
            + ' at ' + pos.getX() + ' ' + pos.getY() + ' ' + pos.getZ()
            + ' in ' + String(level.dimension())
            + ' tick ' + level.getGameTime()
            + ' | block there: ' + String(level.getBlockState(pos))
            + '\n' + formatDiagTrace(new Throwable()));

        if (diagReports === DIAG_MAX_REPORTS) {
            console.info('[Arcadia][diag] Report cap reached, redstone link tracer goes quiet until the next restart.');
        }
    });

    console.info('[Arcadia][diag] Redstone link drop tracer armed (ticket #218), up to ' + DIAG_MAX_REPORTS + ' reports.');
}

StartupEvents.postInit(() => {
    if (!DIAG_ENABLED) return;

    try {
        installRedstoneLinkTracer();
    } catch (err) {
        console.error('[Arcadia][diag] Failed to install the redstone link drop tracer: ' + err);
    }
});
