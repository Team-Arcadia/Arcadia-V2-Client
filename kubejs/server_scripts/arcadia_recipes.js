// Priority: 0

/*
    Arcadia V2 Custom Recipes.
    Author: vyrriox
*/

ServerEvents.recipes(event => {
    console.info("[Arcadia V2] Loading Arcadia Custom Recipes...");

    // Recipe for ATM (Arcadia)
    // Uses Create components for a premium feel.
    event.shaped('arcadia:atm', [
        'PPP',
        'SMS',
        'PPP'
    ], {
        P: 'create:iron_sheet',
        S: 'minecraft:glass_pane',
        M: 'create:precision_mechanism'
    }).id('arcadia:atm_recipe');
});
