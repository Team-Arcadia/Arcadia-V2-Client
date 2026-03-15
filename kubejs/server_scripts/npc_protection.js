// Priority: 900

/*
    NPC Protection Script
    Prevents players from using Ender Leads (Apothic Enchanting) on Easy NPC entities.
    This stops players from displacing NPCs through lead mechanics.
    Author: vyrriox
*/

// All Ender Lead variants from Apothic Enchanting
const ENDER_LEAD_ITEMS = [
  "apothic_enchanting:ender_lead",
  "apothic_enchanting:flimsy_ender_lead",
  "apothic_enchanting:occult_ender_lead",
];

/**
 * Checks if an entity belongs to the Easy NPC mod.
 * Uses entity type namespace prefix for O(1) detection.
 * @param {string} entityType - The entity type ID (e.g. "easy_npc:villager")
 * @returns {boolean}
 */
function isEasyNpc(entityType) {
  return entityType.startsWith("easy_npc:");
}

// Block Ender Lead usage on Easy NPC entities
ItemEvents.entityInteracted((event) => {
  let itemId = event.item.id;

  // Fast exit if not an ender lead
  if (!ENDER_LEAD_ITEMS.includes(itemId)) return;

  // Check if target is an Easy NPC entity
  if (isEasyNpc(event.target.type)) {
    event.cancel();
    event.player.tell(
      Text.red(" Vous ne pouvez pas utiliser une Laisse de l'Ender sur les PNJ ! | You cannot use an Ender Lead on NPCs!"),
    );
  }
});

console.info("[Arcadia V2] NPC Protection Loaded: Ender Leads blocked on Easy NPC entities.");
