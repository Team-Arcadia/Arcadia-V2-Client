/*
    Liquid Blaze Burner schematic cost fix for Arcadia V2 (ticket #240).
    Optimized for KubeJS 1.21.1 (NeoForge).
    Created by vyrriox.

    Why:
      Create Crafts & Additions converts a Blaze Burner into a Liquid Blaze
      Burner when a Straw is used on it, consuming the straw. The block has no
      item of its own: LiquidBlazeBurnerBlock.asItem() returns
      create:blaze_burner, and the block implements neither
      SpecialBlockItemRequirement nor registers anything in Create's
      SchematicRequirementRegistries. Create therefore falls back to asItem(),
      so a schematicannon prints a Liquid Blaze Burner for the price of a plain
      Blaze Burner and never takes the straw out of the chest. Its loot table
      drops the burner AND a straw, so print, break, repeat yields a free straw
      per cycle.

    Fix:
      Register the missing block requirement, so a printed Liquid Blaze Burner
      costs a Blaze Burner plus a Straw, matching both the manual conversion and
      the block's loot table. The material checklist lists the straw as well.
      Heat level is not branched on the way Create does for its own burner: the
      liquid variant can only be made from a burner that already holds a blaze,
      so the empty burner item never applies here.
*/

const LIQUID_BURNER_BLOCK_ID = 'createaddition:liquid_blaze_burner';
const BURNER_ITEM_ID = 'create:blaze_burner';
const STRAW_ITEM_ID = 'createaddition:straw';

function registerLiquidBurnerRequirement() {
    const BuiltInRegistries = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries');
    const ResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation');
    const Blocks = Java.loadClass('net.minecraft.world.level.block.Blocks');
    const ItemStack = Java.loadClass('net.minecraft.world.item.ItemStack');

    const block = BuiltInRegistries.BLOCK.get(ResourceLocation.parse(LIQUID_BURNER_BLOCK_ID));
    if (block === null || block === Blocks.AIR) {
        console.info('[Arcadia] Liquid Blaze Burner absent, schematic cost fix skipped.');
        return;
    }

    const burnerItem = BuiltInRegistries.ITEM.get(ResourceLocation.parse(BURNER_ITEM_ID));
    const strawItem = BuiltInRegistries.ITEM.get(ResourceLocation.parse(STRAW_ITEM_ID));

    const ItemRequirement = Java.loadClass('com.simibubi.create.content.schematics.requirement.ItemRequirement');
    const ItemUseType = Java.loadClass('com.simibubi.create.content.schematics.requirement.ItemRequirement$ItemUseType');
    const SchematicRequirementRegistries = Java.loadClass('com.simibubi.create.api.schematic.requirement.SchematicRequirementRegistries');
    const BlockRequirement = Java.loadClass('com.simibubi.create.api.schematic.requirement.SchematicRequirementRegistries$BlockRequirement');

    // Fresh stacks on every call: the requirement keeps them and Create walks
    // that list while filling the cannon.
    //
    // The delegate has to be an object keyed by the interface method name.
    // Rhino builds the adapter class from the function properties it finds on
    // the delegate, so a bare function contributes no method: the adapter still
    // implements BlockRequirement, but getRequiredItems returns null on every
    // call and Create resolves the block to nothing.
    const requirement = new BlockRequirement({
        getRequiredItems: (state, blockEntity) =>
            new ItemRequirement(ItemUseType.CONSUME, new ItemStack(burnerItem))
                .union(new ItemRequirement(ItemUseType.CONSUME, new ItemStack(strawItem)))
    });

    // Probe the adapter before handing it over: SimpleRegistry refuses a second
    // registration for the same block, so there is no second attempt once the
    // first one is in.
    const probe = requirement.getRequiredItems(block.defaultBlockState(), null);
    if (probe === null || probe.getRequiredItems().size() < 2) {
        console.error('[Arcadia] Liquid Blaze Burner requirement adapter resolves to nothing, schematic cost left untouched.');
        return;
    }

    SchematicRequirementRegistries.BLOCKS.register(block, requirement);

    // Self test through Create's own resolution path, interface cast included.
    const resolved = ItemRequirement.of(block.defaultBlockState(), null);
    const stacks = resolved === null ? 0 : resolved.getRequiredItems().size();
    if (stacks < 2) {
        console.error('[Arcadia] Liquid Blaze Burner requirement registered but resolves to ' + stacks + ' stack(s): the straw is still free.');
        return;
    }

    console.info('[Arcadia] Liquid Blaze Burner schematic cost fixed: blaze burner + straw (' + stacks + ' stacks).');
}

StartupEvents.postInit(() => {
    try {
        registerLiquidBurnerRequirement();
    } catch (err) {
        console.error('[Arcadia] Failed to register the Liquid Blaze Burner schematic cost: ' + err);
    }
});
