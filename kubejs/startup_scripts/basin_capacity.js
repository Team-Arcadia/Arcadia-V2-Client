// Priority: 0
/*
    Modify TFMG Casting Basin Capacity using PowerfulJS.
    Author: vyrriox
*/

PowerfulEvents.registerCapabilities(event => {
    // Modify Fluid Capacity of the Casting Basin to 250mB
    event.addBlockEntity('tfmg:casting_basin', 'fluid', (blockEntity) => {
        return PowerfulFluidHandler.fixed(250)
    })
})
