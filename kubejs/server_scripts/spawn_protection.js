// Priority: 900

/*
    Spawn Protection Script
    Prevents entities from taking damage by spells bypassing Yawp in spawn.
    Author: vyrriox
*/

// Protect passive animals/entities from spell damage in spawn. Monsters can still be killed.
// Using spawned event + Resistance 255 since EntityEvents.hurt is not fully registered in this KubeJS 1.21 version
EntityEvents.spawned(event => {
  if (String(event.level.dimension) !== "arcadia:spawn") return;

  let entity = event.entity;
  if (!entity || !entity.isLiving() || entity.isPlayer()) return;

  let typeStr = String(entity.type);

  // Protection for Animals ONLY (Regen + Resistance)
  const isAnimal = entity.isAnimal();
  const entityId = String(entity.type);
  const isEasyNpc = entityId.includes("easy_npc");

  if (isAnimal && !isEasyNpc) {
    // Apply Resistance 255 (Immune to almost all damage types)
    entity.potionEffects.add("minecraft:resistance", 9999999, 255, false, false);
    // Apply Regeneration
    entity.potionEffects.add("minecraft:regeneration", 9999999, 255, false, false);
  } else if (isEasyNpc) {
    // Ne pas protéger les PNJ d'Easy NPC pour qu'ils soient tuables s'ils sont des boss
    // Cleanup: Remove unintended protection from NPCs if they somehow got it
    if (entity.potionEffects.has("minecraft:regeneration")) {
      entity.potionEffects.remove("minecraft:regeneration");
    }
    if (entity.potionEffects.has("minecraft:resistance")) {
      entity.potionEffects.remove("minecraft:resistance");
    }
    if (entity.potionEffects.has("minecraft:invisibility")) {
      entity.potionEffects.remove("minecraft:invisibility");
    }
  }
});

console.info("[Arcadia V2] Spawn Protection Loaded: Animal damage disabled in arcadia:spawn. (Block protection managed by Yawp).");
