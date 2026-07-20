// Priority: 1000
/*
    Safety net: guarantee creepers become charged when hit by any lightning damage.
    Author: vyrriox

    Player report: creepers struck by lightning (vanilla lightning rod during a
    thunderstorm, or Iron's Spellbooks lightning spells) take damage but do not
    appear charged.

    Static analysis of all 443 mods found no handler cancelling the vanilla
    Creeper#thunderHit path, so the charge most likely IS applied server-side
    (the aura may simply not render with some shaderpacks). This script makes
    the mechanic bulletproof regardless: any lightning-typed damage on a living
    creeper forces the vanilla `powered` flag.

    Covered damage type msgIds:
    - "lightningBolt"   (vanilla minecraft:lightning_bolt)
    - "lightning_magic" (Iron's Spellbooks lightning school)
    - any other modded id containing "lightning" (Ars Nouveau, etc.)
*/

EntityEvents.afterHurt(event => {
    const entity = event.entity;
    if (String(entity.type) !== 'minecraft:creeper') return;
    if (entity.health <= 0) return;

    const msgId = String(event.source.msgId || '').toLowerCase();
    if (!msgId.includes('lightning')) return;

    // Already charged: nothing to do (vanilla thunderHit ran as expected)
    if (entity.nbt.getBoolean('powered')) return;

    entity.mergeNbt({ powered: true });
    console.info(`[Arcadia Fix] Force-charged creeper at ${entity.blockPosition()} (damage type: ${msgId})`);
});

console.info('[Arcadia V2] Creeper Lightning Charge Fix Loaded: lightning damage always charges creepers.');
