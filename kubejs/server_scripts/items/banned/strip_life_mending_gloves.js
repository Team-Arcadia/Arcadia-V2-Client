// priority: 900

/*
    Strip apothic_enchanting:life_mending from Aether gloves in player inventories.
    Workaround for a crash (ArrayIndexOutOfBoundsException) that happens when
    a player heals while wearing Aether gloves enchanted with Life Mending.
    The datapack tag override prevents NEW applications, this handles EXISTING
    enchanted items still in circulation.
    Bug report: https://github.com/Shadows-of-Fire/Apothic-Enchanting/issues/75
    Compatible with KubeJS 7.x / MC 1.21.1 NeoForge.
*/

const LIFE_MENDING = 'apothic_enchanting:life_mending';

const AETHER_GLOVES = new Set([
  'aether:leather_gloves',
  'aether:chainmail_gloves',
  'aether:iron_gloves',
  'aether:golden_gloves',
  'aether:diamond_gloves',
  'aether:netherite_gloves',
  'aether:zanite_gloves',
  'aether:gravitite_gloves',
  'aether:neptune_gloves',
  'aether:phoenix_gloves',
  'aether:obsidian_gloves',
  'aether:valkyrie_gloves'
]);

function stripFromStack(stack) {
  if (stack.isEmpty()) return false;
  const id = String(stack.id);
  if (!AETHER_GLOVES.has(id)) return false;

  const level = stack.getEnchantmentLevel(LIFE_MENDING);
  if (level <= 0) return false;

  stack.removeEnchantment(LIFE_MENDING);
  return true;
}

function stripFromPlayer(player) {
  let inv = player.getInventory();
  let size = inv.getContainerSize();
  let found = false;

  for (let i = 0; i < size; i++) {
    if (stripFromStack(inv.getItem(i))) found = true;
  }

  if (found) player.inventoryMenu.broadcastChanges();
  return found;
}

// Instant detection when any inventory slot changes
PlayerEvents.inventoryChanged(event => {
  if (stripFromStack(event.item)) {
    event.player.tell(Text.yellow('⚠ Life Mending retire des gants Aether (bug connu - crash quand soigne).'));
    event.player.inventoryMenu.broadcastChanges();
  }
});

// Safety net: full scan every 5 minutes
PlayerEvents.tick(event => {
  if (event.player.tickCount % 6000 !== 0) return;
  if (stripFromPlayer(event.player)) {
    event.player.tell(Text.yellow('⚠ Life Mending retire de tes gants Aether (bug connu).'));
  }
});
