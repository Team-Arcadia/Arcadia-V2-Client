// priority: 900

/*
    Block the anvil from applying apothic_enchanting:life_mending on Aether gloves.
    The datapack tag fix prevents the enchanting table, but some setups bypass
    supported_items via the anvil. This handler cancels the anvil result whenever
    an Aether glove ends up with Life Mending on it.
    Paired with strip_life_mending_gloves.js for existing items already enchanted.
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

ItemEvents.anvilUpdate(event => {
  const output = event.output;
  if (!output || output.isEmpty()) return;

  const outId = String(output.id);
  if (!AETHER_GLOVES.has(outId)) return;

  let level = 0;
  try {
    level = output.getEnchantmentLevel(LIFE_MENDING);
  } catch (e) {
    return;
  }

  if (level > 0) {
    event.output = Item.of('minecraft:air');
  }
});
