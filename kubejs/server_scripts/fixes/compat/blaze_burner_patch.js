// Priority: 10
/*
    Blaze Burner Exploit Patch
    Nether structures generate pre-filled Blaze Burners; harvesting them skips the
    intended blaze-capture progression. Instead of sealing every burner in the
    Nether, player-placed burners are tracked in server persistent data so players
    can freely break or wrench-pick THEIR OWN burners, while structure-generated
    ones stay sealed. Contraption relocation stays blocked via tags.
    Author: vyrriox
*/

const BURNER_STORE_KEY = 'arcadiaPlacedBlazeBurners';

function burnerPosKey(level, pos) {
    return String(level.dimension) + '|' + pos.x + '|' + pos.y + '|' + pos.z;
}

function getBurnerStore(server) {
    return server.persistentData.getCompound(BURNER_STORE_KEY);
}

function saveBurnerStore(server, store) {
    server.persistentData.put(BURNER_STORE_KEY, store);
}

ServerEvents.tags('block', event => {
    // Prevent Create contraptions from moving Blaze Burners
    event.add('create:unmovable', 'create:blaze_burner');

    // Additional tags to prevent relocation by various mods
    event.add('create:relocation_not_supported', 'create:blaze_burner');
    event.add('forge:relocation_not_supported', 'create:blaze_burner');
    event.add('forbidden_arcanus:non_movable', 'create:blaze_burner');
});

BlockEvents.rightClicked('create:cart_assembler', event => {
    const { block, player } = event;
    const up = block.up;

    // Check if there is a Blaze Burner on top of the assembler
    if (up.id === 'create:blaze_burner') {
        if (!player.isCreative()) {
            event.cancel();
            player.tell(Text.red("[Arcadia] Impossible d'assembler un Blaze Burner ici ! | Cannot assemble a Blaze Burner here!"));
        }
    }
});

// Track burners placed by players in the Nether so they stay retrievable
BlockEvents.placed('create:blaze_burner', event => {
    const { level, block, server } = event;
    if (String(level.dimension) !== 'minecraft:the_nether') return;

    const store = getBurnerStore(server);
    store.putBoolean(burnerPosKey(level, block.pos), true);
    saveBurnerStore(server, store);
});

BlockEvents.rightClicked('create:blaze_burner', event => {
    const { player, level, block, item, server } = event;

    // Only the sneak + wrench interaction picks the burner up; rotation stays free
    if (!item.hasTag('create:wrench') || !player.crouching) return;
    if (String(level.dimension) !== 'minecraft:the_nether') return;
    if (player.isCreative()) return;

    const store = getBurnerStore(server);
    const key = burnerPosKey(level, block.pos);
    if (store.getBoolean(key)) {
        // Player-placed burner: allow the pickup and forget the position
        store.remove(key);
        saveBurnerStore(server, store);
        return;
    }

    event.cancel();
    player.tell(Text.red("[Arcadia] Ce Blaze Burner appartient à la structure, il est scellé ! | This Blaze Burner belongs to the structure and is sealed!"));
});

BlockEvents.broken('create:blaze_burner', event => {
    const { player, level, block, server } = event;

    if (String(level.dimension) !== 'minecraft:the_nether') return;
    if (player.isCreative()) return;

    const store = getBurnerStore(server);
    const key = burnerPosKey(level, block.pos);
    if (store.getBoolean(key)) {
        // Player-placed burner: allow the break and forget the position
        store.remove(key);
        saveBurnerStore(server, store);
        return;
    }

    event.cancel();
    player.tell(Text.red("[Arcadia] Ce Blaze Burner appartient à la structure, il est scellé ! | This Blaze Burner belongs to the structure and is sealed!"));
});

console.info("[Arcadia V2] Blaze Burner Exploit Patch Loaded: structure burners sealed, player-placed burners retrievable.");
