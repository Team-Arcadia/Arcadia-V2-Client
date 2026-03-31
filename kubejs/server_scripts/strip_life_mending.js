// priority: 950

/*
    Strip apothic_enchanting:life_mending from player inventories.
    ItemEnchantments is immutable in 1.21 — uses Java interop to create
    a Mutable copy, remove the enchantment, then write it back.
*/

const BANNED_ENCHANT_ID = 'apothic_enchanting:life_mending';

let _DataComponents = null;
let _MutableEnchantments = null;
let _enchHolder = null;
let _ready = false;
let _initFailed = false;

function ensureInit(player) {
    if (_ready || _initFailed) return _ready;
    try {
        _DataComponents       = Java.loadClass('net.minecraft.core.component.DataComponents');
        _MutableEnchantments  = Java.loadClass('net.minecraft.world.item.enchantment.ItemEnchantments$Mutable');
        let RL  = Java.loadClass('net.minecraft.resources.ResourceLocation');
        let RK  = Java.loadClass('net.minecraft.resources.ResourceKey');
        let Reg = Java.loadClass('net.minecraft.core.registries.Registries');
        let reg = player.level.registryAccess().lookupOrThrow(Reg.ENCHANTMENT);
        _enchHolder = reg.getOrThrow(RK.create(Reg.ENCHANTMENT, RL.parse(BANNED_ENCHANT_ID)));
        _ready = true;
        console.info('[LifeMending] Initialized — will strip ' + BANNED_ENCHANT_ID + ' on detection');
    } catch (e) {
        console.error('[LifeMending] Init failed: ' + e);
        _initFailed = true;
    }
    return _ready;
}

function stripLifeMending(player) {
    if (!ensureInit(player)) return;
    let inv  = player.getInventory();
    let size = inv.getContainerSize();

    for (let i = 0; i < size; i++) {
        let stack = inv.getItem(i);
        if (!stack || stack.isEmpty()) continue;
        try {
            let enc = stack.get(_DataComponents.ENCHANTMENTS);
            if (!enc || enc.size() === 0) continue;
            if (enc.getLevel(_enchHolder) <= 0) continue;

            // Build a mutable copy without the banned enchant
            let mut = new _MutableEnchantments(enc);
            mut.set(_enchHolder, 0);
            stack.set(_DataComponents.ENCHANTMENTS, mut.toImmutable());
            console.info('[LifeMending] Removed ' + BANNED_ENCHANT_ID + ' from ' + player.name + ' slot ' + i + ' (' + stack.id + ')');
        } catch (e) {
            console.error('[LifeMending] Slot ' + i + ' error: ' + e);
        }
    }
}

PlayerEvents.loggedIn(event => {
    stripLifeMending(event.player);
});

PlayerEvents.tick(event => {
    if (event.player.tickCount % 6000 !== 0) return; // every 5 min
    stripLifeMending(event.player);
});
