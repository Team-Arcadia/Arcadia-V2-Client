// Author: vyrriox
// Renders Arcadia gears outside the vanilla hotbar so item slots stay unobstructed.

const RenderGuiEventPost = Java.loadClass(
    'net.neoforged.neoforge.client.event.RenderGuiEvent$Post'
)
const Minecraft = Java.loadClass('net.minecraft.client.Minecraft')
const ResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')

const hotbarGearTexture = ResourceLocation.fromNamespaceAndPath(
    'minecraft',
    'textures/gui/sprites/hud/hotbar_gear.png'
)

const hotbarWidth = 182
const hotbarHeight = 22
const gearSize = 13

NativeEvents.onEvent(RenderGuiEventPost, event => {
    const minecraft = Minecraft.getInstance()
    if (minecraft.player == null || minecraft.options.hideGui) {
        return
    }

    const graphics = event.guiGraphics
    const hotbarLeft = Math.floor((graphics.guiWidth() - hotbarWidth) / 2)
    const gearY = graphics.guiHeight() - hotbarHeight + Math.floor((hotbarHeight - gearSize) / 2)
    const leftGearX = hotbarLeft - gearSize + 1
    const rightGearX = hotbarLeft + hotbarWidth - 1

    graphics.blit(
        hotbarGearTexture,
        leftGearX,
        gearY,
        0,
        0,
        gearSize,
        gearSize,
        gearSize,
        gearSize
    )
    graphics.blit(
        hotbarGearTexture,
        rightGearX,
        gearY,
        0,
        0,
        gearSize,
        gearSize,
        gearSize,
        gearSize
    )
})
