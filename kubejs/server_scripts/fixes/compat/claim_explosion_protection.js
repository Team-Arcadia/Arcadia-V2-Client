// Priority: 10
/*
    Claim Explosion Protection
    Hardens FTB Chunks block protection against custom mod explosions that bypass
    the built-in handler (notably Mutant Monsters' MutatedExplosionHelper — a Mutant
    Creeper spawned via Chemical X explodes with a custom ExplosionDamageCalculator
    and was destroying blocks inside claimed chunks).

    On every explosion, any affected block sitting in an FTB Chunks claimed chunk is
    removed from the blow list, so the explosion still damages entities / plays its
    effect but never breaks protected terrain. Wilderness (unclaimed) explosions are
    untouched, preserving normal gameplay.

    Author: vyrriox
    KubeJS 7.x / MC 1.21.1 NeoForge.
*/

(function () {
const FTBChunksAPI = Java.loadClass('dev.ftb.mods.ftbchunks.api.FTBChunksAPI');
const ChunkDimPos = Java.loadClass('dev.ftb.mods.ftblibrary.math.ChunkDimPos');

LevelEvents.afterExplosion(event => {
    const level = event.level;
    // Server-side only; claims do not exist client-side.
    if (level.isClientSide()) return;

    const blocks = event.getAffectedBlocks();
    if (!blocks || blocks.isEmpty()) return;

    // FTB Chunks data may not be loaded yet during very early world load.
    const api = FTBChunksAPI.api();
    if (!api.isManagerLoaded()) return;
    const manager = api.getManager();

    // Cache claim lookups per chunk: an explosion touches many blocks in the same
    // few chunks, so we avoid re-querying the manager for every single block.
    const claimCache = {};
    const toRemove = [];

    blocks.forEach(levelBlock => {
        const pos = levelBlock.getPos();
        // ChunkDimPos(Level, BlockPos) maps the block to its owning chunk.
        const cdp = new ChunkDimPos(level, pos);
        const key = cdp.toString();

        let claimed = claimCache[key];
        if (claimed === undefined) {
            // getChunk returns null when the chunk is not claimed.
            claimed = manager.getChunk(cdp) !== null;
            claimCache[key] = claimed;
        }

        if (claimed) {
            toRemove.push(levelBlock);
        }
    });

    if (toRemove.length > 0) {
        toRemove.forEach(b => event.removeAffectedBlock(b));
    }
});

console.info("[Arcadia V2] Claim Explosion Protection Loaded: explosions can no longer break blocks inside FTB Chunks claims.");
})();
