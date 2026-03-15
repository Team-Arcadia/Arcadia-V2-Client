// Author: vyrriox
// Complicated Netherite Block Decrafting System using Create Sequenced Assembly

ServerEvents.recipes(event => {
    console.info("[Arcadia V2] Loading Complicated Netherite Sequenced Assembly...");

    let incomplete = 'arcadia:incomplete_netherite_block';

    event.recipes.create.sequenced_assembly([
        Item.of("minecraft:netherite_ingot", 9)
    ], "minecraft:netherite_block", [
        // 1. Chauffer avec de la lave (Spout) pour ramollir l'alliage
        event.recipes.createFilling(incomplete, [incomplete, Fluid.of("minecraft:lava", 250)]),
        // 2. Écraser à la presse (Mechanical Press)
        event.recipes.createPressing(incomplete, incomplete),
        // 3. Découper à la scie (Mechanical Saw)
        event.recipes.createCutting(incomplete, incomplete).processingTime(200)
    ]).transitionalItem(incomplete).loops(4); // Le processus doit être complété 4 fois
});
