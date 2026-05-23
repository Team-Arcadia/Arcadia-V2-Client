// Priority: 100
//
// TFMG ships a crushing recipe (create:crushing/limestone) that ONLY drops
// limesand. Create Ultimate Factory ships a compat recipe with the same input
// (create:limestone) that drops limesand + quartz (12.5%) + lapis (8%).
//
// Both recipes match the same input — Create picks one per crushing pass and
// the TFMG one wins, so JEI advertises lapis/quartz but the wheel never drops
// them.
//
// Fix: drop the TFMG-only recipe so the CUF compat recipe is the sole match.

ServerEvents.recipes(event => {
    event.remove({ id: 'create:crushing/limestone' });
    console.info('[Arcadia V2] TFMG limestone crushing fix: removed limesand-only recipe so CUF compat (limesand + quartz + lapis) runs.');
});
