// Priority: 100
/*
    KnightLib content-usage enabler for Arcadia V2.
    Optimized for KubeJS 1.21.1 (NeoForge).
    Created by vyrriox.

    Why:
      KnightLib gates its own grail / chalice / essence / homunculus content
      behind a KnightLib.Usage flag set. RecipeManagerMixin strips every
      great_chalice, empty_grail, small_essence, great_essence and homunculus
      recipe whose matching Usage is not enabled.

      Knight Quest 1.9.3 does call KnightLib.initialize() itself, unlike 1.9.2
      which never did, but it enables only three of the five values:
      COPPER_GRAILS, GREAT_CHALICE and GREEN_ESSENCES. HOMUNCULUS is left out,
      so the homunculus recipes are still stripped without this script.

    Fix:
      The no-argument overload enables Usage.ALL, and isEnabled() answers true
      for every value once ALL is in the set, so the homunculus content comes
      back with it.

      Ordering against Knight Quest does not matter: initialize() copies the
      current set, adds what is missing and never removes anything, so the two
      calls accumulate whichever runs first.

    Verified against knightlib 2.0.1 and knightquest 1.9.3 by reading the
    bytecode of KnightLib.initialize, KnightLib.isEnabled, RecipeManagerMixin
    and KnightQuestCommon.init.
*/

StartupEvents.postInit(() => {
    try {
        // Rhino 2101.2.7 mis-handles const declarations directly inside try
        // blocks. The no-argument overload enables Usage.ALL without locals.
        Java.loadClass('dev.xylonity.knightlib.KnightLib').initialize();
        console.info('[Arcadia] KnightLib content enabled (ALL). Homunculus recipes kept, which Knight Quest does not enable on its own.');
    } catch (err) {
        console.error('[Arcadia] Failed to enable KnightLib content: ' + err);
    }
});
