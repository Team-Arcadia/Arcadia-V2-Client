/*
    Contraption brittle-block tracer for Arcadia V2 (tickets #218 and #233), TEMPORARY.
    Optimized for KubeJS 1.21.1 (NeoForge).
    Created by vyrriox.

    Why:
      Two reports point at the same family of blocks. #218: Redstone Links
      duplicate when a piston contraption turns back into blocks. #233: doors,
      beds, banners and bells vanish when a Steam 'n' Rails train is
      disassembled and reassembled, while copycat doors survive. Every block
      named in both reports sits in the create:brittle tag, and copycats do not,
      so the brittle half of Contraption's two-pass assembly and disassembly is
      the common suspect.

      Static reading of Create 6.0.10 narrowed it down but could not close it.
      Ruled out: the block-entity drop path (removeBlocksFromWorld calls
      removeBlockEntity before clearing the position, so IBE.onRemove never
      reaches SmartBlockEntity.destroy), and the rotation branch of
      addBlocksToWorld that destroys doors, ropes and pulley magnets, which only
      fires when transform.rotationAxis is horizontal; trains rotate around Y
      and pistons do not rotate at all.

    What it does, without changing anything:
      - Logs every watched block a contraption captures, at assembly, through a
        neutral MovementAllowedCheck.
      - Logs every watched item entity that spawns server side, with a filtered
        Java stack trace, so the exact caller is named.

      Read together they answer the question static analysis cannot: a block
      that is captured and later drops as an item points at a drop site in
      addBlocksToWorld, a block that is captured and never drops points at the
      silent iterator.remove() path in removeBlocksFromWorld, and a block that
      is never captured was lost at assembly.

    How to use:
      Reproduce once, then search logs/latest.log for [Arcadia][diag]. Set
      DIAG_ENABLED to false, or delete this file, once both tickets are closed.
*/

const DIAG_ENABLED = true;
const DIAG_MAX_DROP_REPORTS = 12;
const DIAG_MAX_CAPTURE_REPORTS = 60;
const DIAG_FRAME_LIMIT = 30;

// Everything named in the two reports, plus the rest of the brittle family that
// shares their placement path.
const DIAG_WATCHED_SUFFIXES = ['_door', '_bed', '_banner', 'bell'];
const DIAG_WATCHED_IDS = ['create:redstone_link'];

let diagDropReports = 0;
let diagCaptureReports = 0;

function isWatchedId(id) {
    for (let i = 0; i < DIAG_WATCHED_IDS.length; i++) {
        if (id === DIAG_WATCHED_IDS[i]) return true;
    }
    for (let i = 0; i < DIAG_WATCHED_SUFFIXES.length; i++) {
        const suffix = DIAG_WATCHED_SUFFIXES[i];
        if (id.length > suffix.length && id.indexOf(suffix, id.length - suffix.length) !== -1) return true;
    }
    return false;
}

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

function installContraptionTracer() {
    const BuiltInRegistries = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries');
    const ItemEntity = Java.loadClass('net.minecraft.world.entity.item.ItemEntity');
    const HashSet = Java.loadClass('java.util.HashSet');
    const Throwable = Java.loadClass('java.lang.Throwable');
    const EventPriority = Java.loadClass('net.neoforged.bus.api.EventPriority');
    const EntityJoinLevelEvent = Java.loadClass('net.neoforged.neoforge.event.entity.EntityJoinLevelEvent');
    const BlockMovementChecks = Java.loadClass('com.simibubi.create.api.contraption.BlockMovementChecks');
    const CheckResult = Java.loadClass('com.simibubi.create.api.contraption.BlockMovementChecks$CheckResult');

    const watchedBlocks = new HashSet();
    BuiltInRegistries.BLOCK.forEach(block => {
        if (isWatchedId(String(BuiltInRegistries.BLOCK.getKey(block)))) watchedBlocks.add(block);
    });

    const watchedItems = new HashSet();
    BuiltInRegistries.ITEM.forEach(item => {
        if (isWatchedId(String(BuiltInRegistries.ITEM.getKey(item)))) watchedItems.add(item);
    });

    if (watchedBlocks.isEmpty() || watchedItems.isEmpty()) {
        console.error('[Arcadia][diag] Contraption tracer inactive: ' + watchedBlocks.size() + ' block(s), ' + watchedItems.size() + ' item(s) resolved.');
        return;
    }

    // Assembly probe. Neutral: it only reports what a contraption captures.
    BlockMovementChecks.registerMovementAllowedCheck((state, level, pos) => {
        if (diagCaptureReports < DIAG_MAX_CAPTURE_REPORTS && !level.isClientSide() && watchedBlocks.contains(state.getBlock())) {
            diagCaptureReports++;
            console.info('[Arcadia][diag] Contraption captures ' + String(state)
                + ' at ' + pos.getX() + ' ' + pos.getY() + ' ' + pos.getZ()
                + ' tick ' + level.getGameTime());
        }
        return CheckResult.PASS;
    });

    // Disassembly probe, and any other drop of a watched item.
    NativeEvents.onEvent(EventPriority.LOWEST, EntityJoinLevelEvent, event => {
        if (diagDropReports >= DIAG_MAX_DROP_REPORTS) return;

        const level = event.getLevel();
        if (level === null || level.isClientSide()) return;

        const entity = event.getEntity();
        if (!ItemEntity.isInstance(entity)) return;

        const stack = entity.getItem();
        if (!watchedItems.contains(stack.getItem())) return;

        diagDropReports++;
        const pos = entity.blockPosition();
        console.info('[Arcadia][diag] Watched drop #' + diagDropReports
            + ' ' + String(BuiltInRegistries.ITEM.getKey(stack.getItem()))
            + ' x' + stack.getCount()
            + ' at ' + pos.getX() + ' ' + pos.getY() + ' ' + pos.getZ()
            + ' in ' + String(level.dimension())
            + ' tick ' + level.getGameTime()
            + ' | block there: ' + String(level.getBlockState(pos))
            + '\n' + formatDiagTrace(new Throwable()));

        if (diagDropReports === DIAG_MAX_DROP_REPORTS) {
            console.info('[Arcadia][diag] Drop report cap reached, tracer goes quiet until the next restart.');
        }
    });

    console.info('[Arcadia][diag] Contraption brittle-block tracer armed (tickets #218, #233): '
        + watchedBlocks.size() + ' blocks and ' + watchedItems.size() + ' items watched.');
}

StartupEvents.postInit(() => {
    if (!DIAG_ENABLED) return;

    try {
        installContraptionTracer();
    } catch (err) {
        console.error('[Arcadia][diag] Failed to install the contraption brittle-block tracer: ' + err);
    }
});
