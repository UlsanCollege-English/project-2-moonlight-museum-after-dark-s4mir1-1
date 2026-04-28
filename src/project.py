"""Project 2: Moonlight Museum After Dark.

Complete implementation of all required features.
Use stdlib only.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque


# ---------------------------------------------------------------------------
# Data records
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Artifact:
    """A museum artifact stored in the archive BST."""

    artifact_id: int
    name: str
    category: str
    age: int
    room: str


@dataclass(frozen=True)
class RestorationRequest:
    """A request to inspect or repair an artifact."""

    artifact_id: int
    description: str


# ---------------------------------------------------------------------------
# BST
# ---------------------------------------------------------------------------

class TreeNode:
    """A node for the artifact BST."""

    def __init__(
        self,
        artifact: Artifact,
        left: TreeNode | None = None,
        right: TreeNode | None = None,
    ) -> None:
        self.artifact = artifact
        self.left = left
        self.right = right


class ArtifactBST:
    """Binary search tree keyed by artifact_id."""

    def __init__(self) -> None:
        self.root: TreeNode | None = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def insert(self, artifact: Artifact) -> bool:
        """Insert an artifact.

        Return True if inserted successfully.
        Return False if an artifact with the same ID already exists (ignored).
        """
        if self.root is None:
            self.root = TreeNode(artifact)
            return True
        return self._insert_recursive(self.root, artifact)

    def search_by_id(self, artifact_id: int) -> Artifact | None:
        """Return the matching artifact, or None if it does not exist."""
        node = self._search_recursive(self.root, artifact_id)
        return node.artifact if node is not None else None

    def inorder_ids(self) -> list[int]:
        """Return artifact IDs via inorder (left -> root -> right) traversal."""
        result: list[int] = []
        self._inorder(self.root, result)
        return result

    def preorder_ids(self) -> list[int]:
        """Return artifact IDs via preorder (root -> left -> right) traversal."""
        result: list[int] = []
        self._preorder(self.root, result)
        return result

    def postorder_ids(self) -> list[int]:
        """Return artifact IDs via postorder (left -> right -> root) traversal."""
        result: list[int] = []
        self._postorder(self.root, result)
        return result

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _insert_recursive(self, node: TreeNode, artifact: Artifact) -> bool:
        if artifact.artifact_id == node.artifact.artifact_id:
            return False  # duplicate: ignore
        if artifact.artifact_id < node.artifact.artifact_id:
            if node.left is None:
                node.left = TreeNode(artifact)
                return True
            return self._insert_recursive(node.left, artifact)
        else:
            if node.right is None:
                node.right = TreeNode(artifact)
                return True
            return self._insert_recursive(node.right, artifact)

    def _search_recursive(
        self, node: TreeNode | None, artifact_id: int
    ) -> TreeNode | None:
        if node is None:
            return None
        if artifact_id == node.artifact.artifact_id:
            return node
        if artifact_id < node.artifact.artifact_id:
            return self._search_recursive(node.left, artifact_id)
        return self._search_recursive(node.right, artifact_id)

    def _inorder(self, node: TreeNode | None, result: list[int]) -> None:
        if node is None:
            return
        self._inorder(node.left, result)
        result.append(node.artifact.artifact_id)
        self._inorder(node.right, result)

    def _preorder(self, node: TreeNode | None, result: list[int]) -> None:
        if node is None:
            return
        result.append(node.artifact.artifact_id)
        self._preorder(node.left, result)
        self._preorder(node.right, result)

    def _postorder(self, node: TreeNode | None, result: list[int]) -> None:
        if node is None:
            return
        self._postorder(node.left, result)
        self._postorder(node.right, result)
        result.append(node.artifact.artifact_id)


# ---------------------------------------------------------------------------
# Restoration queue
# ---------------------------------------------------------------------------

class RestorationQueue:
    """FIFO queue of restoration requests backed by collections.deque."""

    def __init__(self) -> None:
        self._items: Deque[RestorationRequest] = deque()

    def add_request(self, request: RestorationRequest) -> None:
        """Add a request to the back of the queue."""
        self._items.append(request)

    def process_next_request(self) -> RestorationRequest | None:
        """Remove and return the next request, or None if the queue is empty."""
        if self.is_empty():
            return None
        return self._items.popleft()

    def peek_next_request(self) -> RestorationRequest | None:
        """Return the next request without removing it, or None if empty."""
        if self.is_empty():
            return None
        return self._items[0]

    def is_empty(self) -> bool:
        """Return True if the queue has no requests."""
        return len(self._items) == 0

    def size(self) -> int:
        """Return the number of queued requests."""
        return len(self._items)


# ---------------------------------------------------------------------------
# Archive undo stack
# ---------------------------------------------------------------------------

class ArchiveUndoStack:
    """LIFO stack of recent archive actions backed by a Python list."""

    def __init__(self) -> None:
        self._items: list[str] = []

    def push_action(self, action: str) -> None:
        """Push an action onto the stack."""
        self._items.append(action)

    def undo_last_action(self) -> str | None:
        """Remove and return the most recent action, or None if empty."""
        if self.is_empty():
            return None
        return self._items.pop()

    def peek_last_action(self) -> str | None:
        """Return the most recent action without removing it, or None if empty."""
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self) -> bool:
        """Return True if the stack has no actions."""
        return len(self._items) == 0

    def size(self) -> int:
        """Return the number of stored actions."""
        return len(self._items)


# ---------------------------------------------------------------------------
# Exhibit route (singly linked list)
# ---------------------------------------------------------------------------

class ExhibitNode:
    """A node in the singly linked exhibit route."""

    def __init__(self, stop_name: str, next_node: ExhibitNode | None = None) -> None:
        self.stop_name = stop_name
        self.next = next_node


class ExhibitRoute:
    """Singly linked list of exhibit stops."""

    def __init__(self) -> None:
        self.head: ExhibitNode | None = None

    def add_stop(self, stop_name: str) -> None:
        """Add a stop to the end of the route."""
        new_node = ExhibitNode(stop_name)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node

    def remove_stop(self, stop_name: str) -> bool:
        """Remove the first matching stop.

        Return True if a stop was removed.
        Return False if the stop does not exist.
        """
        if self.head is None:
            return False

        # Removing the head node
        if self.head.stop_name == stop_name:
            self.head = self.head.next
            return True

        # Removing a non-head node
        current = self.head
        while current.next is not None:
            if current.next.stop_name == stop_name:
                current.next = current.next.next
                return True
            current = current.next

        return False

    def list_stops(self) -> list[str]:
        """Return the route as a list of stop names in order."""
        stops: list[str] = []
        current = self.head
        while current is not None:
            stops.append(current.stop_name)
            current = current.next
        return stops

    def count_stops(self) -> int:
        """Return the number of stops in the route."""
        count = 0
        current = self.head
        while current is not None:
            count += 1
            current = current.next
        return count


# ---------------------------------------------------------------------------
# Utility / report helpers
# ---------------------------------------------------------------------------

def count_artifacts_by_category(artifacts: list[Artifact]) -> dict[str, int]:
    """Return a dictionary counting artifacts in each category."""
    counts: dict[str, int] = {}
    for artifact in artifacts:
        counts[artifact.category] = counts.get(artifact.category, 0) + 1
    return counts


def unique_rooms(artifacts: list[Artifact]) -> set[str]:
    """Return a set of all rooms used by the given artifacts."""
    return {artifact.room for artifact in artifacts}


def sort_artifacts_by_age(
    artifacts: list[Artifact],
    descending: bool = False,
) -> list[Artifact]:
    """Return a new list of artifacts sorted by age.

    descending=False  ->  youngest to oldest (ascending)
    descending=True   ->  oldest to youngest (descending)

    Ties are broken by artifact_id to guarantee a stable, predictable order.
    """
    return sorted(artifacts, key=lambda a: a.age, reverse=descending)


def linear_search_by_name(
    artifacts: list[Artifact],
    name: str,
) -> Artifact | None:
    """Return the first artifact with an exact matching name, or None."""
    for artifact in artifacts:
        if artifact.name == name:
            return artifact
    return None


# ---------------------------------------------------------------------------
# Integration demo
# ---------------------------------------------------------------------------

def demo_museum_night() -> None:
    """Run a small integration demo showing the system working together."""

    print("=" * 60)
    print("  Moonlight Museum After Dark")
    print("=" * 60)

    # ------------------------------------------------------------------
    # 1. Create artifacts (same set as professor's make_artifacts)
    # ------------------------------------------------------------------
    artifacts = [
        Artifact(40, "Cursed Mirror",   "mirror",   220, "North Hall"),
        Artifact(20, "Clockwork Bird",  "machine",   80, "Workshop"),
        Artifact(60, "Whispering Map",  "paper",    140, "Archive"),
        Artifact(10, "Glowing Key",     "metal",     35, "Vault"),
        Artifact(30, "Moon Dial",       "device",   120, "North Hall"),
        Artifact(50, "Silver Mask",     "costume",  160, "Gallery"),
        Artifact(70, "Lantern Jar",     "glass",     60, "Gallery"),
        Artifact(25, "Ink Compass",     "device",   120, "Archive"),
    ]

    # ------------------------------------------------------------------
    # 2. Build BST
    # ------------------------------------------------------------------
    bst = ArtifactBST()
    for art in artifacts:
        bst.insert(art)

    # ------------------------------------------------------------------
    # 3. Traversals
    # ------------------------------------------------------------------
    print(f"\nInorder IDs:   {bst.inorder_ids()}")
    print(f"Preorder IDs:  {bst.preorder_ids()}")
    print(f"Postorder IDs: {bst.postorder_ids()}")

    # ------------------------------------------------------------------
    # 4. Search
    # ------------------------------------------------------------------
    found = bst.search_by_id(50)
    print(f"\nSearch ID 50 -> {found.name if found else 'Not found'}")
    missing = bst.search_by_id(999)
    print(f"Search ID 999 -> {'Not found' if missing is None else missing.name}")

    # ------------------------------------------------------------------
    # 5. Restoration queue
    # ------------------------------------------------------------------
    print("\n--- Restoration Queue ---")
    queue = RestorationQueue()
    queue.add_request(RestorationRequest(40, "Polish cracked frame"))
    queue.add_request(RestorationRequest(20, "Oil the wing gears"))
    queue.add_request(RestorationRequest(60, "Flatten folded corner"))

    print(f"Next restoration request: {queue.peek_next_request().description}")
    processed = queue.process_next_request()
    print(f"Processed: {processed.description}")
    print(f"Queue size after processing: {queue.size()}")

    # ------------------------------------------------------------------
    # 6. Archive undo stack
    # ------------------------------------------------------------------
    print("\n--- Archive Undo Stack ---")
    stack = ArchiveUndoStack()
    stack.push_action("Added Cursed Mirror to archive")
    stack.push_action("Queued Clockwork Bird repair")
    stack.push_action("Removed Secret Vault stop")

    print(f"Top of stack: {stack.peek_last_action()}")
    undone = stack.undo_last_action()
    print(f"Undo action: {undone}")
    print(f"Stack size after undo: {stack.size()}")

    # ------------------------------------------------------------------
    # 7. Exhibit route
    # ------------------------------------------------------------------
    print("\n--- Exhibit Route ---")
    route = ExhibitRoute()
    for stop in [
        "Entrance",
        "North Hall",
        "Workshop",
        "Archive",
        "Vault",
        "Gallery",
        "Exit",
    ]:
        route.add_stop(stop)

    print(f"Exhibit route: {route.list_stops()}")
    route.remove_stop("Vault")
    print(f"After removing 'Vault': {route.list_stops()}")

    # ------------------------------------------------------------------
    # 8. Reports
    # ------------------------------------------------------------------
    print("\n--- Museum Reports ---")
    category_counts = count_artifacts_by_category(artifacts)
    print(f"Category counts: {category_counts}")

    rooms = unique_rooms(artifacts)
    print(f"Unique rooms: {sorted(rooms)}")

    sorted_asc = sort_artifacts_by_age(artifacts)
    print(f"By age (asc):  {[a.name for a in sorted_asc]}")

    sorted_desc = sort_artifacts_by_age(artifacts, descending=True)
    print(f"By age (desc): {[a.name for a in sorted_desc]}")

    found_by_name = linear_search_by_name(artifacts, "Whispering Map")
    print(f"Search 'Whispering Map' -> {found_by_name.name if found_by_name else 'Not found'}")

    print("\n" + "=" * 60)
    print("  Demo complete. The museum is ready for the night.")
    print("=" * 60)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    demo_museum_night()