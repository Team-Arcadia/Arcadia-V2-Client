// Priority: 900

/*
    Anti Duplication Script (Yawp)
    Prevents players from duplicating books by placing them as decoration
    in the arcadia:spawn dimension where Yawp block interactions are cancelled.
    Author: vyrriox
*/

const BANNED_SPAWN_BOOKS = [
  "minecraft:book",
  "minecraft:enchanted_book",
  "minecraft:written_book",
  "minecraft:writable_book"
];

BlockEvents.rightClicked(event => {
  // Check if we are in the spawn dimension
  if (event.level.dimension.toString() !== "arcadia:spawn") return;

  // Check if item is a book
  if (BANNED_SPAWN_BOOKS.includes(event.item.id)) {
    // If player is not creative, we block the interaction to prevent Yawp desync duplication
    if (!event.player.isCreative()) {
      event.cancel();
      event.player.tell(Text.red(" Vous ne pouvez pas placer de livres en zone spawn ! | You cannot place books in the spawn area!"));
    }
  }
});

// Also block right clicking the air with books (which bypasses block events in some cases, causing desyncs)
ItemEvents.rightClicked(event => {
  // Check if we are in the spawn dimension
  if (event.level.dimension.toString() !== "arcadia:spawn") return;

  // Check if item is a book
  if (BANNED_SPAWN_BOOKS.includes(event.item.id)) {
    if (!event.player.isCreative()) {
      // Force cancel the item usage completely
      event.cancel();
    }
  }
});

console.info("[Arcadia V2] Anti-Dupe Books Loaded: Enabled for arcadia:spawn dimension.");
