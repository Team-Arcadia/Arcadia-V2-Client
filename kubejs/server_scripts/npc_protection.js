// Priority: 900

/*
    NPC Protection Script
    Prevents Easy NPC entities from being interacted with via Leads, Ender Leads, Fishing Rods.
    NPCs must remain KILLABLE - never apply Resistance/Regeneration to them.
    Spell blocking (Ars Nouveau, Iron's Spells, Simply Swords) is handled by spawn_movement_block.js.
    Author: vyrriox
*/

(function() {
    const SPAWN_DIM = "arcadia:spawn";
    const FORBIDDEN_NPC_ITEMS_SET = new Set([
        "apothic_enchanting:ender_lead",
        "apothic_enchanting:flimsy_ender_lead",
        "apothic_enchanting:occult_ender_lead",
        "minecraft:lead",
        "minecraft:fishing_rod"
    ]);

    // Effects to strip on spawn (safety net - root cause fixed in spawn_protection.js)
    const NPC_HARMFUL_EFFECTS = [
        "minecraft:resistance",
        "minecraft:regeneration",
        "minecraft:invisibility",
        "minecraft:levitation",
        "minecraft:slow_falling"
    ];

    function isEasyNpc(entity) {
        if (!entity || !entity.type) return false;
        return String(entity.type).startsWith("easy_npc:");
    }

    // --- EFFECT CLEANUP: Strip harmful effects when NPCs spawn ---
    EntityEvents.spawned(event => {
        if (!event.entity || !event.entity.level) return;
        if (String(event.entity.level.dimension) !== SPAWN_DIM) return;
        if (!isEasyNpc(event.entity)) return;

        for (let i = 0; i < NPC_HARMFUL_EFFECTS.length; i++) {
            try { event.entity.potionEffects.remove(NPC_HARMFUL_EFFECTS[i]); } catch (e) {}
        }
    });

    // --- INTERACTION BLOCKING ---
    ItemEvents.rightClicked(event => {
        if (!event.level || String(event.level.dimension) !== SPAWN_DIM) return;
        if (String(event.item.id).includes("ender_lead")) {
            event.cancel();
            event.player.tell(Text.red("[Arcadia] Les Ender Leads sont interdits au spawn ! | Ender Leads are forbidden at spawn!"));
        }
    });

    BlockEvents.rightClicked(event => {
        if (!event.block || String(event.block.dimension) !== SPAWN_DIM) return;
        if (String(event.item.id).includes("ender_lead")) {
            event.cancel();
            event.player.tell(Text.red("[Arcadia] Les Ender Leads sont interdits au spawn ! | Ender Leads are forbidden at spawn!"));
        }
    });

    ItemEvents.entityInteracted(event => {
        const { item, target, player } = event;
        if (!target || !target.level || String(target.level.dimension) !== SPAWN_DIM) return;

        const itemId = String(item.id);

        if (itemId.includes("ender_lead")) {
            event.cancel();
            player.tell(Text.red("[Arcadia] Les Ender Leads sont interdits au spawn ! | Ender Leads are forbidden at spawn!"));
            return;
        }

        if (FORBIDDEN_NPC_ITEMS_SET.has(itemId) && isEasyNpc(target)) {
            event.cancel();
            player.tell(Text.red("[Arcadia] Impossible d'utiliser cet objet sur un PNJ ! | Cannot use this item on NPCs!"));
        }
    });

})();

console.info("[Arcadia V2] NPC Protection active (interaction blocking + effect cleanup on spawn).");
