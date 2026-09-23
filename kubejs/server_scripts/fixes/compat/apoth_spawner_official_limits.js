// Priority: 0
/*
    Player spawners: No AI and redstone control forced on the official servers

    Spawner farms built with Apotheosis runes were a steady TPS cost on the
    network: every spawned mob runs pathfinding and targeting, and a farm left
    running keeps spawning for nobody. On the official servers every spawner a
    player has placed or modified is forced to:
      - No AI: spawned mobs stand still (no pathfinding, no targeting, no
        pushing), the most expensive part of a mob;
      - Redstone control: the spawner only runs while powered, so players can
        switch a farm off;
      - No "ignore players": the Rune of Solitude is stripped and cannot be
        applied, so a farm only runs while a player stands within its
        activation range. Without this, force-loaded bases kept their farms
        spawning around the clock for nobody.

    "Player spawner" = an Apothic spawner a player placed (both stats are
    written on placement) or modified with a rune (hasBeenModified). Natural
    dungeon and structure spawners are never touched. Both stats are also
    re-applied on every spawn, so undoing them with Nether Quartz does not
    stick: a spawner found without redstone control gets it back and that
    spawn is cancelled.

    Solo and serverpack are not affected: the script only acts when the
    server_id written in arcadia-lib's server.toml is one of the official ids
    below (solo and serverpack leave it empty).

    Note: no const inside the try blocks below (Rhino build 85 bug).

    Author: vyrriox
    KubeJS 7.x / MC 1.21.1 NeoForge.
*/

(function () {
const OFFICIAL_SERVER_IDS = ['server1', 'server2', 'server3', 'server4', 'server5', 'serveurevent', 'servertest'];

// Reads the id written in config/arcadia/lib/server.toml, not ServerContext.SERVER_ID:
// when the file leaves it empty (solo, serverpack) arcadia-lib falls back to "server1",
// which would switch these limits on everywhere. Official servers all set it explicitly.
let serverId = null;
function isOfficialServer() {
    if (serverId === null) {
        try {
            let ServerIdConfig = Java.loadClass('com.arcadia.lib.config.ServerIdConfig');
            serverId = String(ServerIdConfig.SERVER_ID.get() || '').trim().toLowerCase();
        } catch (err) {
            serverId = '';
        }
    }
    return OFFICIAL_SERVER_IDS.indexOf(serverId) >= 0;
}

const EventPriority = Java.loadClass('net.neoforged.bus.api.EventPriority');
const FinalizeSpawnEvent = Java.loadClass('net.neoforged.neoforge.event.entity.living.FinalizeSpawnEvent');
const MobSpawnType = Java.loadClass('net.minecraft.world.entity.MobSpawnType');
const ApothSpawnerTile = Java.loadClass('dev.shadowsoffire.apothic_spawners.block.ApothSpawnerTile');
const SpawnerStats = Java.loadClass('dev.shadowsoffire.apothic_spawners.stats.SpawnerStats');

function isForced(tile, stat) {
    let value = tile.getStatsMap().get(stat);
    return value == true;
}

// Writes the forced stats on the tile. Returns true when something had to change.
function enforce(tile) {
    let changed = false;
    if (isForced(tile, SpawnerStats.IGNORE_PLAYERS)) {
        tile.getStatsMap().put(SpawnerStats.IGNORE_PLAYERS, false);
        changed = true;
    }
    if (!isForced(tile, SpawnerStats.NO_AI)) {
        tile.getStatsMap().put(SpawnerStats.NO_AI, true);
        changed = true;
    }
    if (!isForced(tile, SpawnerStats.REDSTONE_CONTROL)) {
        tile.getStatsMap().put(SpawnerStats.REDSTONE_CONTROL, true);
        changed = true;
    }
    if (changed) {
        tile.setChanged();
        let level = tile.getLevel();
        if (level) {
            let state = tile.getBlockState();
            level.sendBlockUpdated(tile.getBlockPos(), state, state, 3);
        }
    }
    return changed;
}

function isPlayerSpawner(tile) {
    return tile.hasBeenModified()
        || isForced(tile, SpawnerStats.NO_AI)
        || isForced(tile, SpawnerStats.REDSTONE_CONTROL);
}

BlockEvents.placed('minecraft:spawner', event => {
    if (!isOfficialServer()) return;
    let tile = event.block.entity;
    if (!(tile instanceof ApothSpawnerTile)) return;
    enforce(tile);
    if (event.player) {
        event.player.tell(Text.gold('Spawners on this server always run with No AI and need a redstone signal. / Sur ce serveur, les spawners tournent toujours sans IA et demandent un signal redstone.'));
    }
});

BlockEvents.rightClicked('minecraft:spawner', event => {
    if (!isOfficialServer()) return;
    if (event.item.id !== 'apotheosis:ignore_players_spawner_rune') return;
    event.player.tell(Text.red("The Rune of Solitude is disabled on this server: spawners need a player nearby. / La Rune de Solitude est désactivée sur ce serveur : les spawners ont besoin d'un joueur à proximité."));
    event.cancel();
});

NativeEvents.onEvent(EventPriority.LOW, FinalizeSpawnEvent, event => {
    if (event.getSpawnType() !== MobSpawnType.SPAWNER) return;
    if (!isOfficialServer()) return;
    let spawner = event.getSpawner();
    if (!spawner) return;
    let tile = spawner.left().orElse(null);
    if (!(tile instanceof ApothSpawnerTile) || !isPlayerSpawner(tile)) return;

    let hadRedstone = isForced(tile, SpawnerStats.REDSTONE_CONTROL);
    enforce(tile);
    event.getEntity().setNoAi(true);
    if (!hadRedstone) {
        event.setSpawnCancelled(true);
    }
});

ServerEvents.loaded(event => {
    if (isOfficialServer()) {
        console.info('[Arcadia] Spawner limits active on "' + serverId + '": No AI, redstone control and no Rune of Solitude on player spawners');
    } else {
        console.info('[Arcadia] Spawner limits inactive on "' + serverId + '" (solo or serverpack)');
    }
});
})();
