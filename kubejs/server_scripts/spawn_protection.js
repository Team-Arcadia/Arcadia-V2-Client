// Priority: 900

/*
    Spawn Protection Script
    Prevents entities from taking damage by spells bypassing Yawp in spawn.
    Prevents torch placement via pickaxe enchantments in spawn.
    Author: vyrriox
*/

// Protect passive animals/entities from spell damage in spawn. Monsters can still be killed.
// Using spawned event + Resistance 255 since EntityEvents.hurt is not fully registered in this KubeJS 1.21 version
EntityEvents.spawned(event => {
  if (String(event.level.dimension) !== "arcadia:spawn") return;

  let entity = event.entity;
  if (!entity || !entity.isLiving() || entity.isPlayer()) return;

  let typeStr = String(entity.type);

  // Ne pas protéger les PNJ d'Easy NPC pour qu'ils soient tuables s'ils sont des boss
  if (typeStr.includes("easynpc")) return;

  // Cibler uniquement les entités passives / alliées (animaux, villageois, golems, allays)
  let isPassive = entity.isAnimal() || typeStr.includes("villager") || typeStr.includes("golem") || typeStr.includes("allay");

  if (isPassive) {
    // Apply Resistance 255 (Immune to almost all damage types)
    entity.potionEffects.add("minecraft:resistance", 9999999, 255, false, false);
    // Apply Regeneration
    entity.potionEffects.add("minecraft:regeneration", 9999999, 255, false, false);
  }
});

// Prevent any block placement from non-creative entities/players in spawn
BlockEvents.placed(event => {
  if (event.level.dimension.toString() !== "arcadia:spawn") return;

  let entity = event.entity;
  // If it's a player and not creative, or if there's no entity (placed by world/fake player), cancel
  if (!entity || (entity.isPlayer() && !entity.isCreative())) {
    event.cancel();
  }
});

// Helper function to check if an item is a pickaxe
function isPickaxe(item) {
  if (!item || item.isEmpty()) return false;
  let id = item.id.toString();
  return id.includes('pickaxe') || item.hasTag('minecraft:pickaxes') || item.hasTag('c:tools/pickaxes');
}

// Explicitly block right-clicking blocks with a pickaxe to prevent specific enchantment bypasses
BlockEvents.rightClicked(event => {
  if (event.level.dimension.toString() !== "arcadia:spawn") return;

  if (isPickaxe(event.item) && event.player && !event.player.isCreative()) {
    event.cancel();
    event.player.tell(Text.red(" L'utilisation de cet enchantement de pioche est bloquée au spawn ! | Pickaxe enchantments are blocked at spawn!"));
  }
});

// Explicitly block right-clicking air with a pickaxe
ItemEvents.rightClicked(event => {
  if (event.level.dimension.toString() !== "arcadia:spawn") return;

  if (isPickaxe(event.item) && event.player && !event.player.isCreative()) {
    event.cancel();
  }
});

console.info("[Arcadia V2] Spawn Protection Loaded: Animal damage and Pickaxe block placement disabled in arcadia:spawn.");
