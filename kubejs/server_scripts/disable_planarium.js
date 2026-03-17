/**
 * @file disable_planarium.js
 * @description Désactive le craft du Planarium d'Ars Nouveau pour éviter les problèmes de duplication et de lag.
 * @author vyrriox
 * @version 1.0.0
 */

ServerEvents.recipes(event => {
    // Suppression de l'item Planarium d'Ars Nouveau
    event.remove({ output: 'ars_nouveau:planarium' });
});
