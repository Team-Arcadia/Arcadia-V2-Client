// Priority: 0
/*
    Auction House off on the event server
    Author: vyrriox

    Arcadia AH has no config switch to turn the market off. Its only kill
    switch is the admin command "/arcadia_ah disable", which flips the static
    flag AhGlobalFlags.AH_ENABLED. That flag starts at true on every boot and
    is never saved, so the event server came back with a working AH after each
    restart.

    The kubejs folder is shared by every server, so this script reads the
    arcadia-lib server id (config/arcadia/lib/server.toml, server_id) and only
    acts on the servers listed below. It runs once the server has loaded,
    after arcadia-lib has applied its config. Staff can still re-enable the AH
    for a session with "/arcadia_ah enable".

    Note: no const inside the try block below. Rhino build 85 throws
    "redeclaration of var" for a const declared in a try block.
*/

const AH_DISABLED_SERVER_IDS = ['serveurevent'];

ServerEvents.loaded(event => {
    let serverId = '';
    try {
        let ServerContext = Java.loadClass('com.arcadia.lib.ServerContext');
        serverId = String(ServerContext.SERVER_ID || '').toLowerCase();
    } catch (err) {
        console.warn('[Arcadia] AH guard: could not read the arcadia-lib server id: ' + err);
        return;
    }

    if (AH_DISABLED_SERVER_IDS.indexOf(serverId) < 0) return;

    try {
        let AhGlobalFlags = Java.loadClass('com.arcadia.ah.AhGlobalFlags');
        AhGlobalFlags.AH_ENABLED = false;
        console.info('[Arcadia] Auction House disabled on server "' + serverId + '" (flag now ' + AhGlobalFlags.AH_ENABLED + ').');
    } catch (err) {
        console.warn('[Arcadia] AH guard: could not disable the Auction House on "' + serverId + '": ' + err);
    }
});
