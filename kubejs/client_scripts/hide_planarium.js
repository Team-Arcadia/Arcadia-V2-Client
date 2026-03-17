/**
 * @file hide_planarium.js
 * @description Masque le Planarium d'Ars Nouveau dans JEI pour éviter toute confusion suite à sa désactivation.
 * @author vyrriox
 * @version 1.0.0
 */

JEIEvents.hideItems(event => {
    event.hide('ars_nouveau:planarium');
});

// Compatibilité avec REI si présent
/*
REIEvents.hide('item', event => {
    event.hide('ars_nouveau:planarium');
});
*/

// Compatibilité avec EMI si présent
/*
EMIEvents.hideItems(event => {
    event.hide('ars_nouveau:planarium');
});
*/
