// Priority: 50

/*
    Occultism Dimensional Battlefield — boss drop rerouting
    Author: vyrriox

    The battlefield ships two dedicated loot tables that pay out a finished boss drop on
    every simulated kill: a nether star for the Wither, and a dragon egg (weight 1 against
    dragon breath weight 3) for the Ender Dragon. Both are replaced by fragments, which
    only become the real drop through the Stellar Forge assembly line.

    replaceLoot keeps the entry in place, so the dragon table keeps its 1:3 weighting
    against dragon breath. The vanilla boss loot tables are not touched here: killing a
    Wither by hand still drops its 1-2 stars from mob_damage_nerfs.js.
*/

LootJS.modifiers((event) => {
    event
        .addTableModifier("occultism:battlefield/minecraft/wither")
        .replaceLoot(
            "minecraft:nether_star",
            LootEntry.of("arcadia:star_fragment"),
            false,
        );

    event
        .addTableModifier("occultism:battlefield/minecraft/ender_dragon")
        .replaceLoot(
            "minecraft:dragon_egg",
            LootEntry.of("arcadia:dragon_shard"),
            false,
        );

    console.info(
        "[Arcadia V2] Battlefield boss drops rerouted: nether star -> star fragment, dragon egg -> dragon shard.",
    );
});
