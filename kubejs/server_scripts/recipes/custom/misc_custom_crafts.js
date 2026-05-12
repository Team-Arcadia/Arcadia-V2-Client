// Priority: 0

/*
    Arcadia V2 — Miscellaneous custom crafts.

    Single home for one-off Arcadia-specific recipes that don't fit a
    larger themed file (armor, fusion core chain, recipe overhaul, etc.).

    Currently bundled:
      - Arcadia ATM (cosmetic / utility block, uses Create premium parts)
      - Iron sheet hand-craft fallback (early-game unblock for recipe_overhaul gating)

    Author: vyrriox
*/

ServerEvents.recipes(event => {
    console.info('[Arcadia V2] Loading misc custom crafts...');

    // --- Arcadia ATM ---
    // Premium feel: iron sheets frame + glass viewing pane + precision mechanism core.
    event.shaped('arcadia:atm', [
        'PPP',
        'SMS',
        'PPP'
    ], {
        P: 'create:iron_sheet',
        S: 'minecraft:glass_pane',
        M: 'create:precision_mechanism'
    }).id('arcadia:atm_recipe');

    // --- Iron sheet hand-craft fallback ---
    // recipe_overhaul gates iron tools/armor behind create:iron_sheet, but
    // iron_sheet is normally only obtainable via Mechanical Press (which itself
    // needs 1 iron_block + shaft + andesite_casing — heavy upfront cost).
    // 3 iron_ingot stacked vertically -> 1 iron_sheet unblocks fresh starts.
    // 3x the cost of pressing, so the press remains the efficient long-term path.
    event.shaped('create:iron_sheet', [
        'I',
        'I',
        'I'
    ], {
        I: 'minecraft:iron_ingot'
    }).id('arcadia:iron_sheet_handcraft_fallback');
});
