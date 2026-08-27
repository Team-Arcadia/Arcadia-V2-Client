// Priority: 10
/*
    Magnetic Jammer — anti-magnet field
    Author: vyrriox

    A placed arcadia:magnet_jammer suppresses item magnets in a 5 chunk radius around
    itself: same dimension, full height, an 11x11 chunk square. Ground items inside the
    field get the NeoForge PreventRemoteMovement flag, which every magnet that follows
    the convention reads before pulling an item:
      - sophisticatedcore MagnetUpgradeWrapper, so both the Backpacks and the Storage
        magnet upgrades, basic and advanced
      - Immersive Engineering powerpack magnet
      - Occultism greedy familiar

    Manual pickup is untouched, the flag only blocks remote collection.

    create_sa:copper_magnet does not read the flag, it just pushes item entities around
    with setDeltaMovement, so it gets its own counter-push. That part costs one small
    entity query per tick per player actually holding one inside a field, and it can be
    switched off with COUNTER_PUSH_MAGNETS.

    Fields are tracked in server persistent data, same approach as
    fixes/compat/blaze_burner_patch.js, stored as one JSON string.
*/

const JAMMER_ID = 'arcadia:magnet_jammer';
const JAMMER_STORE_KEY = 'arcadiaMagnetJammers';
const FLAG = 'PreventRemoteMovement';

// Chebyshev radius in chunks. 5 gives an 11x11 chunk square, 176x176 blocks.
const RADIUS_CHUNKS = 5;

// Ticks between two sweeps flagging items that drifted in or predate the jammer.
const SWEEP_INTERVAL = 40;
const SWEEP_RANGE = 32;

// Magnets that ignore the flag are countered by stripping the horizontal velocity they
// hand to nearby items. Set to false to leave them alone.
const COUNTER_PUSH_MAGNETS = true;
const PUSH_MAGNETS = ['create_sa:copper_magnet'];
const PUSH_MAGNET_RANGE = 16;

const MAGNETIC_ENTITIES = ['minecraft:item', 'minecraft:experience_orb'];

// Cached view of the store: [{ d: dimension, x, y, z }]
let jammers = [];

function loadJammers(server) {
    const raw = server.persistentData.getString(JAMMER_STORE_KEY);
    if (!raw) {
        jammers = [];
        return;
    }
    try {
        jammers = JSON.parse(raw);
    } catch (err) {
        console.error('[Arcadia V2] Magnet jammer store is corrupt, starting empty: ' + err);
        jammers = [];
    }
}

function saveJammers(server) {
    server.persistentData.putString(JAMMER_STORE_KEY, JSON.stringify(jammers));
}

// Chunk coordinate of a block coordinate. Floor division, negatives included.
function toChunk(coord) {
    return Math.floor(coord) >> 4;
}

function inField(dimension, x, z) {
    const cx = toChunk(x);
    const cz = toChunk(z);
    for (let i = 0; i < jammers.length; i++) {
        const j = jammers[i];
        if (j.d !== dimension) continue;
        if (Math.abs(toChunk(j.x) - cx) > RADIUS_CHUNKS) continue;
        if (Math.abs(toChunk(j.z) - cz) > RADIUS_CHUNKS) continue;
        return true;
    }
    return false;
}

function jamEntity(entity) {
    entity.persistentData.putBoolean(FLAG, true);
}

ServerEvents.loaded(event => {
    loadJammers(event.server);
    console.info('[Arcadia V2] Magnetic Jammer: ' + jammers.length + ' field(s) restored.');
});

BlockEvents.placed(JAMMER_ID, event => {
    const { level, block, server, player } = event;

    jammers.push({
        d: String(level.dimension),
        x: block.pos.x,
        y: block.pos.y,
        z: block.pos.z,
    });
    saveJammers(server);

    if (player) {
        player.tell(Text.gold('[Arcadia] Champ anti-aimant actif sur ' + (RADIUS_CHUNKS * 2 + 1) + 'x' + (RADIUS_CHUNKS * 2 + 1) + ' chunks. | Anti-magnet field active over ' + (RADIUS_CHUNKS * 2 + 1) + 'x' + (RADIUS_CHUNKS * 2 + 1) + ' chunks.'));
    }
});

BlockEvents.broken(JAMMER_ID, event => {
    const { level, block, server, player } = event;
    const dimension = String(level.dimension);

    const before = jammers.length;
    jammers = jammers.filter(j => !(
        j.d === dimension &&
        j.x === block.pos.x &&
        j.y === block.pos.y &&
        j.z === block.pos.z
    ));

    if (jammers.length !== before) {
        saveJammers(server);
        if (player) {
            player.tell(Text.gray('[Arcadia] Champ anti-aimant retiré. | Anti-magnet field removed.'));
        }
    }
});

// Anything dropping inside a field is flagged the moment it exists.
MAGNETIC_ENTITIES.forEach(id => {
    EntityEvents.spawned(id, event => {
        if (jammers.length === 0) return;
        const entity = event.entity;
        if (!inField(String(entity.level.dimension), entity.x, entity.z)) return;
        jamEntity(entity);
    });
});

ServerEvents.tick(event => {
    // No field placed: one length check per tick and nothing else.
    if (jammers.length === 0) return;

    const server = event.server;

    // Sweep around players standing in a field. Magnets only reach around a player, so
    // that is exactly the area worth covering, and it never touches unloaded chunks.
    if (server.tickCount % SWEEP_INTERVAL === 0) {
        server.players.forEach(player => {
            if (!inField(String(player.level.dimension), player.x, player.z)) return;

            player.level
                .getEntitiesWithin(AABB.ofSize([player.x, player.y, player.z], SWEEP_RANGE, SWEEP_RANGE, SWEEP_RANGE))
                .forEach(entity => {
                    if (MAGNETIC_ENTITIES.indexOf(String(entity.type)) === -1) return;
                    jamEntity(entity);
                });
        });
    }

    if (!COUNTER_PUSH_MAGNETS) return;

    server.players.forEach(player => {
        if (!inField(String(player.level.dimension), player.x, player.z)) return;

        const main = String(player.mainHandItem.id);
        const off = String(player.offHandItem.id);
        if (PUSH_MAGNETS.indexOf(main) === -1 && PUSH_MAGNETS.indexOf(off) === -1) return;

        player.level
            .getEntitiesWithin(AABB.ofSize([player.x, player.y, player.z], PUSH_MAGNET_RANGE, PUSH_MAGNET_RANGE, PUSH_MAGNET_RANGE))
            .forEach(entity => {
                if (String(entity.type) !== 'minecraft:item') return;
                // Keep the vertical component so items still fall normally.
                entity.setDeltaMovement([0, entity.deltaMovement.y, 0]);
            });
    });
});

console.info('[Arcadia V2] Magnetic Jammer loaded: radius ' + RADIUS_CHUNKS + ' chunks.');
