/*
    Handcrafted cushion duplication fix for Arcadia V2 (ticket #241).
    Optimized for KubeJS 1.21.1 (NeoForge).
    Created by vyrriox.

    Why:
      Handcrafted stores the cushion as a blockstate property on the furniture,
      not as a separate block, and drops it back in onRemove. ChairBlock,
      BenchBlock, CouchBlock and FancyBedBlock all share the same body:

          if (!level.isClientSide && state.getBlock() != newState.getBlock())
              Containers.dropItemStack(level, x, y, z, color.toCushion());

      Neither the isMoving argument nor the UPDATE_SUPPRESS_DROPS flag is
      checked, so the drop also fires when the block is removed because it is
      being moved rather than broken. Create's contraption assembly removes
      blocks with flags 122 (MOVE_BY_PISTON + SUPPRESS_DROPS included) and a
      vanilla piston uses 68 or 82, all of which announce a move. The furniture
      is re-placed intact with its colour, so every assembly leaks one cushion:
      a mechanical piston cycling back and forth prints two per cycle, which is
      exactly what was reported.

    Fix:
      Suppress the cushion drop when, and only when, the furniture is being
      moved. Two arming points cover the two movers:
        - Create: a MovementAllowedCheck sees every block a contraption is about
          to capture, in the same tick as the removal. It stays neutral (PASS)
          and only records the position.
        - Vanilla pistons: PistonEvent.Pre resolves the pushed set and records
          those positions. A cheap line scan runs first so nothing is resolved
          twice on the piston farms that hold no furniture.
      A cushion item entity spawning on a recorded position within two ticks is
      then cancelled. Anything else, breaking the furniture by hand included,
      still drops normally, and the moved furniture keeps its cushion.

      Known gap: the line scan only walks the piston axis, so furniture pulled
      sideways by a slime block alone is not covered. Contraptions are covered
      in full, since Create's check runs on every captured block.
*/

const CUSHION_COLORS = [
    'white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray',
    'light_gray', 'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black'
];
const CUSHION_ARM_WINDOW = 2;
const PISTON_SCAN_RANGE = 13;

const armedPositions = {};
let lastPruneTime = -1;

function armKey(level, pos) {
    return String(level.dimension()) + '|' + pos.getX() + '|' + pos.getY() + '|' + pos.getZ();
}

function pruneArmedPositions(now) {
    Object.keys(armedPositions).forEach(key => {
        if (now - armedPositions[key] > CUSHION_ARM_WINDOW) {
            delete armedPositions[key];
        }
    });
}

function armPosition(level, pos) {
    // Number(): getGameTime() hands back a Java long, which would never compare
    // strictly equal to the stored tick.
    const now = Number(level.getGameTime());
    // Once per tick is enough: a contraption arms all of its furniture at once.
    if (now !== lastPruneTime) {
        pruneArmedPositions(now);
        lastPruneTime = now;
    }
    armedPositions[armKey(level, pos)] = now;
}

function consumeArmedPosition(level, pos) {
    const key = armKey(level, pos);
    const stamp = armedPositions[key];
    if (stamp === undefined) return false;

    delete armedPositions[key];
    return Number(level.getGameTime()) - stamp <= CUSHION_ARM_WINDOW;
}

function installCushionMoveGuard() {
    const BuiltInRegistries = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries');
    const ResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation');
    const Items = Java.loadClass('net.minecraft.world.item.Items');
    const ItemEntity = Java.loadClass('net.minecraft.world.entity.item.ItemEntity');
    const HashSet = Java.loadClass('java.util.HashSet');
    const EventPriority = Java.loadClass('net.neoforged.bus.api.EventPriority');
    const EntityJoinLevelEvent = Java.loadClass('net.neoforged.neoforge.event.entity.EntityJoinLevelEvent');
    const PistonEventPre = Java.loadClass('net.neoforged.neoforge.event.level.PistonEvent$Pre');
    const BlockMovementChecks = Java.loadClass('com.simibubi.create.api.contraption.BlockMovementChecks');
    const CheckResult = Java.loadClass('com.simibubi.create.api.contraption.BlockMovementChecks$CheckResult');

    // The four block classes that drop a cushion in onRemove. Matching on the
    // class covers every wood variant and any subclass a future version adds.
    const furnitureClasses = [
        Java.loadClass('earth.terrarium.handcrafted.common.blocks.ChairBlock'),
        Java.loadClass('earth.terrarium.handcrafted.common.blocks.BenchBlock'),
        Java.loadClass('earth.terrarium.handcrafted.common.blocks.CouchBlock'),
        Java.loadClass('earth.terrarium.handcrafted.common.blocks.FancyBedBlock')
    ];

    const furniture = new HashSet();
    BuiltInRegistries.BLOCK.forEach(block => {
        for (let i = 0; i < furnitureClasses.length; i++) {
            if (furnitureClasses[i].isInstance(block)) {
                furniture.add(block);
                return;
            }
        }
    });

    const cushions = new HashSet();
    CUSHION_COLORS.forEach(color => {
        const item = BuiltInRegistries.ITEM.get(ResourceLocation.parse('handcrafted:' + color + '_cushion'));
        if (item !== null && item !== Items.AIR) {
            cushions.add(item);
        }
    });

    if (furniture.isEmpty() || cushions.isEmpty()) {
        console.error('[Arcadia] Handcrafted cushion guard inactive: ' + furniture.size() + ' furniture block(s), ' + cushions.size() + ' cushion item(s) resolved.');
        return;
    }

    // Create contraptions: neutral check, used only as a removal notification.
    BlockMovementChecks.registerMovementAllowedCheck((state, level, pos) => {
        if (!level.isClientSide() && furniture.contains(state.getBlock())) {
            armPosition(level, pos);
        }
        return CheckResult.PASS;
    });

    // Vanilla pistons, extending and retracting alike.
    NativeEvents.onEvent(PistonEventPre, event => {
        const level = event.getLevel();
        if (level === null || level.isClientSide()) return;

        const origin = event.getPos();
        const direction = event.getDirection();

        let carriesFurniture = false;
        for (let i = 1; i <= PISTON_SCAN_RANGE; i++) {
            const scanned = level.getBlockState(origin.relative(direction, i));
            if (scanned.isAir()) break;
            if (furniture.contains(scanned.getBlock())) {
                carriesFurniture = true;
                break;
            }
        }
        if (!carriesFurniture) return;

        const helper = event.getStructureHelper();
        if (helper === null || !helper.resolve()) return;

        helper.getToPush().forEach(pushed => {
            if (furniture.contains(level.getBlockState(pushed).getBlock())) {
                armPosition(level, pushed);
            }
        });
    });

    NativeEvents.onEvent(EventPriority.HIGHEST, EntityJoinLevelEvent, event => {
        const level = event.getLevel();
        if (level === null || level.isClientSide()) return;

        const entity = event.getEntity();
        if (!ItemEntity.isInstance(entity)) return;
        if (!cushions.contains(entity.getItem().getItem())) return;
        if (!consumeArmedPosition(level, entity.blockPosition())) return;

        event.setCanceled(true);
    });

    console.info('[Arcadia] Handcrafted cushion move guard loaded: ' + furniture.size() + ' furniture blocks, ' + cushions.size() + ' cushions watched.');
}

StartupEvents.postInit(() => {
    try {
        installCushionMoveGuard();
    } catch (err) {
        console.error('[Arcadia] Failed to install the Handcrafted cushion move guard: ' + err);
    }
});
