// Priority: 50
/*
    Equipment Drop Cap
    Author: vyrriox

    Player report: stacking loot multipliers (Aether Skyroot sword double drops,
    Apotheosis Loot Pinata affix, Scavenger enchant, Snow Queen +225% cold-kill
    gem, Looting...) yields 8-16 copies of the SAME equipment piece per kill.

    Each multiplier is fine in isolation; the explosion comes from them stacking
    multiplicatively on the final drop list. Instead of nerfing each source (and
    breaking their identity), this caps identical equipment drops per kill.

    Cap = 2: preserves the Skyroot "double drops" fantasy (1 base + 1 double)
    while killing the x16 duplication. Non-equipment drops (leather, gunpowder,
    mob parts...) are untouched - farming resources with the combo stays viable.

    Note: counted by item ID, so two swords with different Apotheosis affixes
    still count as the same item. Works alongside the 5% equipment drop nerf
    from mob_damage_nerfs.js (LootJS operates on loot tables; this operates on
    the final LivingDropsEvent collection, after all multipliers).
*/

const EQUIPMENT_DROP_REGEX = /.*:(sword|pickaxe|axe|shovel|hoe|helmet|chestplate|leggings|boots|shield|trident|bow|crossbow).*/;
const MAX_IDENTICAL_EQUIPMENT_PER_KILL = 2;

EntityEvents.drops(event => {
    const drops = event.drops;
    if (drops.size() <= MAX_IDENTICAL_EQUIPMENT_PER_KILL) return;

    const counts = {};
    const kept = [];
    let removed = 0;

    drops.forEach(drop => {
        const id = drop.item.id;
        if (!EQUIPMENT_DROP_REGEX.test(id)) {
            kept.push(drop);
            return;
        }
        counts[id] = (counts[id] || 0) + drop.item.count;
        if (counts[id] <= MAX_IDENTICAL_EQUIPMENT_PER_KILL) {
            kept.push(drop);
        } else {
            removed++;
        }
    });

    if (removed > 0) {
        drops.clear();
        kept.forEach(d => drops.add(d));
        console.info(`[Arcadia] Equipment drop cap: removed ${removed} duplicate drop(s) from ${event.entity.type}`);
    }
});

console.info('[Arcadia V2] Equipment Drop Cap Loaded: max ' + MAX_IDENTICAL_EQUIPMENT_PER_KILL + ' identical equipment drops per kill.');
