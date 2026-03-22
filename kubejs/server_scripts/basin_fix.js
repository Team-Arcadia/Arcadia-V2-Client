// Priority: 10
/*
    Global workaround for TFMG Casting Basin limitation.
    Capper all casting recipes fluid cost to 140mB to fit in the 144mB basin.
    Author: vyrriox
*/

ServerEvents.recipes(event => {
    let count = 0
    
    // Process all TFMG casting recipes
    event.forEachRecipe({ type: 'tfmg:casting' }, recipe => {
        let json = recipe.json
        
        // TFMG recipes usually have an "ingredients" array
        if (json.has('ingredients')) {
            let ingredients = json.get('ingredients')
            
            // Check each ingredient for fluid amount
            ingredients.forEach(ing => {
                if (ing.has('fluid') && ing.has('amount')) {
                    let amount = ing.get('amount').asInt()
                    if (amount > 140) {
                        ing.addProperty('amount', 140)
                        count++
                    }
                }
            })
        }
    })
    
    if (count > 0) {
        console.info(`[Arcadia V2] Basin Fix: Capped ${count} casting recipes to 140mB.`);
    }
})
