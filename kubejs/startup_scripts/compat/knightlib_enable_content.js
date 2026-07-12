// Priority: 100
/*
    KnightLib content-usage enabler for Arcadia V2.
    Optimized for KubeJS 1.21.1 (NeoForge).
    Created by vyrriox.

    Why:
      KnightLib 1.5.2 gates its own grail / chalice / essence / homunculus
      content behind a KnightLib.Usage flag set. A RecipeManagerMixin strips
      every great_chalice, empty_grail, essence-conversion and homunculus
      recipe unless the matching Usage is enabled via KnightLib.initialize(...).
      Knight Quest 1.9.2 never calls initialize(), so the flag set stays empty
      and the whole progression collapses: no chalice, no grails, no filled
      grails, hence no craftable Knight armor/weapons and no homunculus mobs.

    Fix:
      Enable every Usage at startup (before datapacks load), so the mixin sees
      the content as enabled and keeps all recipes intact. This restores the
      full intended Knight Quest chain without duplicating any recipe.
*/

StartupEvents.postInit(() => {
    try {
        const KnightLib = Java.loadClass('dev.xylonity.knightlib.KnightLib');
        const Usage = Java.loadClass('dev.xylonity.knightlib.KnightLib$Usage');
        KnightLib.initialize(Usage.ALL);
        console.info('[Arcadia] KnightLib content enabled (ALL). Grail, chalice, essence and homunculus recipes restored.');
    } catch (err) {
        console.error('[Arcadia] Failed to enable KnightLib content: ' + err);
    }
});
