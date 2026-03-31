// priority: 999

/*
    Remove banned items from merchant trades (Wandering Trader, Red Merchant, etc.)
    Prevents turtles and other banned items from appearing in trade UIs.
    Created by vyrriox for Arcadia V2.

    Compatible with KubeJS 7.x / MC 1.21.1 NeoForge.
*/

const TRADE_BANNED_ITEMS = new Set([
  'computercraft:turtle_normal',
  'computercraft:turtle_advanced'
]);

const MERCHANT_TYPES = new Set([
  'minecraft:wandering_trader',
  'supplementaries:red_merchant'
]);

/**
 * Removes any trade offer that sells a banned item.
 * Uses AbstractVillager.getOffers() / MerchantOffer.getResult().
 */
function cleanMerchantTrades(entity) {
  try {
    if (!entity.isAlive()) return;
    let offers = entity.getOffers();
    if (!offers || offers.size() === 0) return;

    for (let i = offers.size() - 1; i >= 0; i--) {
      let offer = offers.get(i);
      let resultId = String(offer.getResult().id);
      if (TRADE_BANNED_ITEMS.has(resultId)) {
        offers.remove(i);
      }
    }
  } catch (e) {
    // Entity may not support trades yet
  }
}

// Queue merchants for cleaning on next tick (ensures trades are populated)
let pendingMerchants = [];

EntityEvents.spawned(event => {
  if (event.entity && MERCHANT_TYPES.has(String(event.entity.type))) {
    pendingMerchants.push(event.entity);
  }
});

ServerEvents.tick(event => {
  // Check once per second (20 ticks) instead of every tick
  if (event.server.tickCount % 20 !== 0) return;
  if (pendingMerchants.length === 0) return;
  let batch = pendingMerchants.splice(0);
  batch.forEach(e => cleanMerchantTrades(e));
});
