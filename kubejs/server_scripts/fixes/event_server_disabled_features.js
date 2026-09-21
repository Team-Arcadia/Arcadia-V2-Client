// Priority: 0
/*
    Auction House and pets off on the event server
    Author: vyrriox

    Neither Arcadia AH nor Arcadia Pets has a config switch to turn the whole
    feature off. Each only has an admin kill switch ("/arcadia_ah disable",
    the pets "disable" command) that flips a static flag:
      - com.arcadia.ah.AhGlobalFlags.AH_ENABLED
      - com.arcadia.pets.PetsGlobalFlags.PETS_ENABLED
    Both flags start at true on every boot and are never saved, so the event
    server came back with a working AH and working pets after each restart.

    The kubejs folder is shared by every server, so this script reads the
    arcadia-lib server id (config/arcadia/lib/server.toml, server_id) and only
    acts on the servers listed below. It runs once the server has loaded,
    after arcadia-lib has applied its config. Staff can still re-enable a
    feature for one session with its admin "enable" command.

    Note: no const inside the try blocks below. Rhino build 85 throws
    "redeclaration of var" for a const declared in a try block.
*/

const EVENT_SERVER_IDS = ['serveurevent'];

const EVENT_DISABLED_FLAGS = [
    { label: 'Auction House', owner: 'com.arcadia.ah.AhGlobalFlags', field: 'AH_ENABLED' },
    { label: 'Pets', owner: 'com.arcadia.pets.PetsGlobalFlags', field: 'PETS_ENABLED' }
];

function readArcadiaServerId() {
    try {
        let ServerContext = Java.loadClass('com.arcadia.lib.ServerContext');
        return String(ServerContext.SERVER_ID || '').toLowerCase();
    } catch (err) {
        console.warn('[Arcadia] Event guard: could not read the arcadia-lib server id: ' + err);
        return '';
    }
}

function switchFlagOff(entry, serverId) {
    try {
        let owner = Java.loadClass(entry.owner);
        owner[entry.field] = false;
        console.info('[Arcadia] ' + entry.label + ' disabled on server "' + serverId + '" (' + entry.field + ' = ' + owner[entry.field] + ').');
    } catch (err) {
        console.warn('[Arcadia] Event guard: could not disable ' + entry.label + ' on "' + serverId + '": ' + err);
    }
}

ServerEvents.loaded(event => {
    let serverId = readArcadiaServerId();
    if (EVENT_SERVER_IDS.indexOf(serverId) < 0) return;

    EVENT_DISABLED_FLAGS.forEach(entry => switchFlagOff(entry, serverId));
});
