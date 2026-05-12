// Priority: 0
/*
    Iron Sheet hand-craft fallback.

    recipe_overhaul gates iron tools/armor behind create:iron_sheet, but
    iron_sheet is normally only obtainable via Mechanical Press (which itself
    needs 1 iron_block + shaft + andesite_casing — heavy upfront cost). Solo
    players hit a wall before they can craft their first iron pickaxe.

    Fallback: 3 iron_ingot stacked vertically -> 1 iron_sheet in vanilla
    crafting table. 3x the cost of pressing (1 ingot -> 1 sheet) so the
    Mechanical Press remains the efficient long-term path.

    Author: vyrriox
*/

ServerEvents.recipes(event => {
    event.shaped('create:iron_sheet', [
        'I',
        'I',
        'I'
    ], {
        I: 'minecraft:iron_ingot'
    }).id('arcadia:iron_sheet_handcraft_fallback');

    console.info('[Arcadia V2] Iron sheet hand-craft fallback recipe loaded (3 iron_ingot -> 1 iron_sheet).');
});
