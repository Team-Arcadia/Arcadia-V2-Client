// Priority: 900

/*
    NPC Protection Script
    Prevents players from displacing Easy NPC entities through various mechanics:
    - Ender Leads, Vanilla Leads, Fishing Rods
    - Vehicles (Boats/Minecarts)
    - Knockback/Attack displacement
    - Magic spells / Projectiles
    Author: vyrriox
*/

// Using an IIFE (Immediately Invoked Function Expression) to ensure absolute scope isolation
(function() {
  const SPAWN_DIM = "arcadia:spawn";

  // Items to block interaction with
  const FORBIDDEN_NPC_ITEMS = [
    "apothic_enchanting:ender_lead",
    "apothic_enchanting:flimsy_ender_lead",
    "apothic_enchanting:occult_ender_lead",
    "minecraft:lead",
    "minecraft:fishing_rod"
  ];

  function isEasyNpc(entity) {
    if (!entity || !entity.type) return false;
    return String(entity.type).startsWith("easy_npc:");
  }

  function isInSpawn(entity) {
      if (!entity || !entity.level) return false;
      return String(entity.level.dimension) === SPAWN_DIM;
  }

  // --- PASSIVE PROTECTION & IMMUNITY (Resistance 255) ---
  // Using EntityEvents.spawned as it's the most reliable for applying persistent state in this version
  EntityEvents.spawned(event => {
    const { entity } = event;
    if (!isInSpawn(entity) || !isEasyNpc(entity)) return;

    // Apply absolute protection attributes / effects
    // Resistance 255 makes the entity immune to almost all damage (and thus knockback)
    entity.potionEffects.add("minecraft:resistance", 9999999, 255, false, false);
    entity.potionEffects.add("minecraft:regeneration", 9999999, 255, false, false);
    
    // Attempt to set invulnerable directly if possible
    try {
        entity.setInvulnerable(true);
    } catch (e) { /* fallback to effects */ }
  });

  // --- INTERACTION BLOCKING ---
  ItemEvents.entityInteracted((event) => {
    const { item, target, player } = event;
    if (!isInSpawn(target)) return;

    if (FORBIDDEN_NPC_ITEMS.includes(String(item.id)) && isEasyNpc(target)) {
      event.cancel();
      player.tell(Text.red(`[Arcadia] Impossible d'utiliser cet objet sur un PNJ ici !`));
    }
  });

  // --- ANCHORING SYSTEM (Tick) ---
  LevelEvents.tick(event => {
      const { level, server } = event;
      
      // Perform check every 1 second (20 ticks)
      if (server.tickCount % 20 !== 0) return;
      if (String(level.dimension) !== SPAWN_DIM) return;

      level.getEntities().forEach(entity => {
          if (isEasyNpc(entity)) {
              // Eject passengers from PNJ (vehicle exploit)
              if (entity.isPassenger()) {
                  entity.stopRiding();
                  console.info(`[Arcadia V2] Ejected NPC ${entity.uuid} from vehicle.`);
              }

              // Freeze NPC precisely if any velocity detected
              let velocity = entity.deltaMovement;
              if (velocity && (Math.abs(velocity.x()) > 0.01 || Math.abs(velocity.z()) > 0.01)) {
                  entity.setDeltaMovement(0, velocity.y(), 0);
                  entity.setPosition(entity.x, entity.y, entity.z);
              }
              
              
              // Anchoring and passenger ejection logic continues below...
          }
      });
  });
})();

console.info("[Arcadia V2] NPC protection reinforced (Total Lockdown): Resistance 255, Anchoring, and Items blocked.");
