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

console.info("[Arcadia V2] Spawn Protection Loaded: Animal damage disabled in arcadia:spawn. (Block protection managed by Yawp).");
