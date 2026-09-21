/*
    Simply Swords Soulstalker server crash fix for Arcadia V2.
    Optimized for KubeJS 1.21.1 (NeoForge).
    Created by vyrriox.

    Why:
      Simply Swords 1.70.2 registers its soulstalker_leap_launch message with
      Architectury's SimpleNetworkManager.registerS2C. On a dedicated server
      that call only builds the MessageType: the S2C payload type itself is
      registered on the client alone. SimplySwordsNetwork.init() does register
      the server side by hand, but only for ObserverStatusEffectsPacket.

      So when a Stygian Strider (Soulstalker sword ability) performs a charged
      leap near a player, SoulstalkerLeapLaunchPacket.sendTo looks the type up
      in NetworkAggregator.S2C_TYPE, gets null, and the server dies with
      "Cannot invoke CustomPacketPayload$Type.id() because type is null".
      Singleplayer is unaffected: the integrated server shares the client's
      registration.

    Fix:
      On a dedicated server only, register the missing S2C payload type the
      same way Simply Swords does for its other server packet. This must run
      at script load, before NeoForge fires RegisterPayloadHandlersEvent, so it
      is top-level code and not a StartupEvents handler.
      Skipped when the id is already known, so an upstream fix makes it a no-op.
*/

(function registerSoulstalkerLeapPacket() {
    try {
        let Platform = Java.loadClass('dev.architectury.platform.Platform');
        let Env = Java.loadClass('dev.architectury.utils.Env');
        if (Platform.getEnvironment() != Env.SERVER) return;
        if (!Platform.isModLoaded('simplyswords')) return;

        let ResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation');
        let NetworkManager = Java.loadClass('dev.architectury.networking.NetworkManager');
        let NetworkAggregator = Java.loadClass('dev.architectury.impl.NetworkAggregator');

        let packetId = ResourceLocation.fromNamespaceAndPath('simplyswords', 'soulstalker_leap_launch');
        if (NetworkAggregator.S2C_TYPE.containsKey(packetId)) {
            console.info('[Arcadia] Soulstalker leap packet already registered server-side, fix skipped.');
            return;
        }

        NetworkManager.registerS2CPayloadType(packetId);
        console.info('[Arcadia] Registered missing server-side payload type ' + packetId + ' (Simply Swords Soulstalker leap).');
    } catch (err) {
        // warn, not error: KubeJS turns any startup-time error into a
        // "startup script syntax errors" boot failure.
        console.warn('[Arcadia] Failed to register the Soulstalker leap packet: ' + err);
        if (err && err.javaException) err.javaException.printStackTrace();
    }
})();
