// Priority: 10
/*
    Occult Engineering — Mechanical Pulverizer duplication fix

    The custom recipe `occultengineering:upgrade_tier` allows N pulverizers in a
    crafting grid (any number of slots), but only consumes 1 while producing N
    upgraded outputs in shift-craft mode. This is a critical duplication bug.

    Stack trace explanation (decompiled from UpgradeTierRecipe.class):
      - matches() iterates items, returns true if 1 PulverizerBlockItem + 1 MechanicalUpgradeItem are found
      - assemble() copies the first found PulverizerBlockItem and writes the new tier on it
      - getRemainingItems() (vanilla default) only marks ONE pulverizer slot as consumed
      - On shift-craft, vanilla multiplies the output by min(grid stacks) -> 30 outputs from 30 inputs but only 1 consumed

    Fix: remove the broken custom recipe and replace it with 3 explicit shapeless recipes
    that consume EXACTLY 1 pulverizer + 1 upgrade and output 1 upgraded pulverizer.

    Tiers (Occult Engineering progression):
      - Tier 1 (base):       occultengineering:mechanical_pulverizer
      - Tier 2 (Djinni):     base + upgrade_djinni
      - Tier 3 (Afrit):      tier2 + upgrade_afrit
      - Tier 4 (Marid):      tier3 + upgrade_marid

    The tier is stored via the data component `occultengineering:crushing_item_tier` (int).
    Base pulverizer has no component (tier=1 by default in the mod's code).

    Author: vyrriox
*/

ServerEvents.recipes(event => {
    // Remove the broken upgrade_tier custom recipe entirely.
    event.remove({ type: 'occultengineering:upgrade_tier' });

    const pulverizer    = 'occultengineering:mechanical_pulverizer';
    const upgradeDjinni = 'occultengineering:mechanical_upgrade_djinni';
    const upgradeAfrit  = 'occultengineering:mechanical_upgrade_afrit';
    const upgradeMarid  = 'occultengineering:mechanical_upgrade_marid';

    // Helper: pulverizer with a specific crushing tier data component.
    // Minecraft 1.21+ uses data components (not legacy NBT) — KubeJS parses inline
    // component syntax: `item_id[component_id=value]` directly in Item.of().
    const pulverizerOfTier = (tier) => Item.of(`${pulverizer}[occultengineering:crushing_item_tier=${tier}]`);

    // Tier 1 -> Tier 2 (Djinni)
    event.shapeless(
        pulverizerOfTier(2),
        [pulverizer, upgradeDjinni]
    ).id('arcadia:pulverizer_upgrade_t1_to_t2');

    // Tier 2 -> Tier 3 (Afrit)
    event.shapeless(
        pulverizerOfTier(3),
        [pulverizerOfTier(2), upgradeAfrit]
    ).id('arcadia:pulverizer_upgrade_t2_to_t3');

    // Tier 3 -> Tier 4 (Marid)
    event.shapeless(
        pulverizerOfTier(4),
        [pulverizerOfTier(3), upgradeMarid]
    ).id('arcadia:pulverizer_upgrade_t3_to_t4');

    // Also allow skipping tiers (T1 + afrit -> T3, T1 + marid -> T4, T2 + marid -> T4)
    // to match the original mod's behavior (a higher-tier upgrade can be applied directly)
    event.shapeless(
        pulverizerOfTier(3),
        [pulverizer, upgradeAfrit]
    ).id('arcadia:pulverizer_upgrade_t1_to_t3');

    event.shapeless(
        pulverizerOfTier(4),
        [pulverizer, upgradeMarid]
    ).id('arcadia:pulverizer_upgrade_t1_to_t4');

    event.shapeless(
        pulverizerOfTier(4),
        [pulverizerOfTier(2), upgradeMarid]
    ).id('arcadia:pulverizer_upgrade_t2_to_t4');
});

console.info("[Arcadia V2] Occult Engineering Pulverizer dupe fix loaded: replaced custom upgrade_tier recipe with 6 shapeless recipes.");
