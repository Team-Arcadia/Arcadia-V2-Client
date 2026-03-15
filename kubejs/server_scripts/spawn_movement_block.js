// Priority: 1000
/*
    Spawn Movement Block Script
    Blocks spells and items that allow moving entities/players in arcadia:spawn.
    Covers: Ars Nouveau, Iron's Spells 'n Spellbooks, Simply Swords.
    Author: vyrriox
*/

// --- CONFIGURATION ---

const PROTECTED_DIMENSION = "arcadia:spawn";

// Iron's Spells 'n Spellbooks: Spells to block
const IRONS_MOVEMENT_SPELLS = [
    "teleport",
    "blink",
    "blood_step",
    "portal",
    "recall",
    "gust",
    "shadow_step",
    "charge",
    "abyssal_shroud"
];

// Ars Nouveau: Glyphs that involve movement or displacement
const ARS_MOVEMENT_GLYPHS = [
    "ars_nouveau:glyph_blink",
    "ars_nouveau:glyph_exchange",
    "ars_nouveau:glyph_leap",
    "ars_nouveau:glyph_launch",
    "ars_nouveau:glyph_gravity",
    "ars_nouveau:glyph_pull",
    "ars_nouveau:glyph_push",
    "ars_nouveau:glyph_teleport"
];

// Simply Swords: Weapons with movement/teleport abilities
const SIMPLY_SWORDS_MOVEMENT_ITEMS = [
    "simplyswords:whisperwind",
    "simplyswords:emberlash",
    "simplyswords:stars_edge",
    "simplyswords:storm_edge",
    "simplyswords:thunderbrand",
    "simplyswords:soul_pyre",
    "simplyswords:soul_stealer",
    "simplyswords:molten_edge",
    "simplyswords:hearthflame",
    "simplyswords:stormbringer",
    "simplyswords:arcaneist"
];

// --- HELPERS ---

function isInSpawn(entity) {
    if (!entity || !entity.level) return false;
    return String(entity.level.dimension) === PROTECTED_DIMENSION;
}

function notifyBlocked(player, message) {
    if (player && player.tell) {
        player.tell(Text.red(`[Arcadia] ${message}`));
    }
}

// --- IRON'S SPELLS 'N SPELLBOOKS ---

if (typeof ISSEvents !== 'undefined') {
    ISSEvents.spellPreCast(event => {
        if (!isInSpawn(event.entity)) return;

        let spellId = String(event.spellId);
        let idOnly = spellId.split(':')[1] || spellId;

        if (IRONS_MOVEMENT_SPELLS.includes(idOnly)) {
            event.cancel();
            notifyBlocked(event.entity, "Ce sort de déplacement est bloqué au spawn ! | This movement spell is blocked at spawn!");
        }
    });
}

// --- ARS NOUVEAU ---

// Blocking the entity displacement via spawned entity checks (Leap, Gravity, etc. often spawn entities or use arrows)
EntityEvents.spawned('ars_nouveau:spell_arrow', event => {
    if (!isInSpawn(event.entity)) return;
    
    // We can't cancel the arrow easily without knowing the spell, but we can block it if in spawn for safety
    // or just let it stay for now until we find the glyph event.
});

// --- SIMPLY SWORDS & GENERAL ITEM PROTECTION ---

ItemEvents.rightClicked(event => {
    if (!isInSpawn(event.player)) return;

    let itemId = String(event.item.id);
    if (SIMPLY_SWORDS_MOVEMENT_ITEMS.includes(itemId)) {
        if (!event.player.isCreative()) {
            event.cancel();
            notifyBlocked(event.player, "L'aptitude spéciale de cette arme est bloquée au spawn ! | This weapon's special ability is blocked at spawn!");
        }
    }
});

ItemEvents.entityInteracted(event => {
    if (!isInSpawn(event.player)) return;

    let itemId = String(event.item.id);
    if (SIMPLY_SWORDS_MOVEMENT_ITEMS.includes(itemId)) {
        if (!event.player.isCreative()) {
            event.cancel();
            notifyBlocked(event.player, "L'aptitude spéciale de cette arme est bloquée au spawn ! | This weapon's special ability is blocked at spawn!");
        }
    }
});

console.info("[Arcadia V2] Spawn Movement Protection Loaded: Iron's Spells and Simply Swords blocked. Ars Nouveau discovery pending.");
