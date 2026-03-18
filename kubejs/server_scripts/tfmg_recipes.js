// Priority: 99

/*
    TFMG Custom Recipes for Arcadia V2.
    Author: vyrriox
*/

ServerEvents.recipes((event) => {
    console.info("[Arcadia V2] Loading TFMG Custom Recipes...");

    // Steel Mechanism (Sequenced Assembly)
    event.recipes.create.sequenced_assembly(
        [
            "tfmg:steel_mechanism"
        ],
        "tfmg:heavy_plate",
        [
            event.recipes.createDeploying("tfmg:unfinished_steel_mechanism", [
                "tfmg:unfinished_steel_mechanism",
                "tfmg:steel_ingot",
            ]),
            event.recipes.createDeploying("tfmg:unfinished_steel_mechanism", [
                "tfmg:unfinished_steel_mechanism",
                "tfmg:aluminum_ingot",
            ]),
            event.recipes.createDeploying("tfmg:unfinished_steel_mechanism", [
                "tfmg:unfinished_steel_mechanism",
                "tfmg:screw",
            ]),
            event.recipes.createDeploying("tfmg:unfinished_steel_mechanism", [
                "tfmg:unfinished_steel_mechanism",
                "tfmg:screwdriver",
            ])
        ]
    ).transitionalItem("tfmg:unfinished_steel_mechanism").loops(1);

});
