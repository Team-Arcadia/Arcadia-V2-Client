// Priority: 50

/*
    Mob Loot Nerf Script
    Reduces the chance of mobs dropping their equipment (Armor, Weapons, Tools) to 15%.
    Author: vyrriox
*/

LootJS.modifiers((event) => {
    // Target ENTITY loot tables (mobs)
    event
        .addTableModifier(LootType.ENTITY)
        .removeLoot(
            Ingredient.of(
                /.*:(sword|pickaxe|axe|shovel|hoe|helmet|chestplate|leggings|boots|shield|trident|bow|crossbow).*/,
            ),
        )
        .randomChance(0.95); // Remove 95% of items -> 5% Chance to drop

    console.info(
        "[Arcadia V2] Mob Loot Nerf Applied: Equipment drop rate reduced to 5%.",
    );

    // Wither: 1-2 Nether Stars (Default is 1)
    event
        .addTableModifier("minecraft:entities/wither")
        .removeLoot("minecraft:nether_star")
        .addLoot(
            LootEntry.of("minecraft:nether_star").apply((c) => {
                c.setCount([1, 2]); // [min, max] - Uniform distribution
            }),
        );

    // Ender Dragon: Guaranteed Dragon Head
    event
        .addTableModifier("minecraft:entities/ender_dragon")
        .addLoot("minecraft:dragon_head");

    // Ender Dragon: Simply Swords Nerf (10% Chance)
    event
        .addTableModifier("minecraft:entities/ender_dragon")
        .removeLoot(Ingredient.of(/simplyswords:.*/))
        .randomChance(0.9); // 90% chance to remove -> 10% chance to stay
});
