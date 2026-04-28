# Project 2: Moonlight Museum After Dark

## Team information
- Team name: Moonlight Coders
- Members: (add your names here)
- Repository name: project-2-moonlight-museum

---

## Project summary

Our project builds a complete management system for the Moonlight Museum's secret late-night exhibition of strange artifacts. The system uses multiple data structures to organize artifacts, process restoration requests, undo archive actions, manage a guided exhibit route, and generate useful reports. A Binary Search Tree stores and retrieves artifacts efficiently by ID, while a queue, stack, and singly linked list handle requests, undo history, and the exhibit route respectively. Together these structures form an integrated system demonstrated through the `demo_museum_night()` function.

---

## Feature checklist

### Core structures
- [x] `Artifact` class/record
- [x] `ArtifactBST`
- [x] `RestorationQueue`
- [x] `ArchiveUndoStack`
- [x] `ExhibitRoute` singly linked list

### BST features
- [x] insert artifact
- [x] search by ID
- [x] preorder traversal
- [x] inorder traversal
- [x] postorder traversal
- [x] duplicate IDs ignored

### Queue features
- [x] add request
- [x] process next request
- [x] peek next request
- [x] empty check
- [x] size

### Stack features
- [x] push action
- [x] undo last action
- [x] peek last action
- [x] empty check
- [x] size

### Linked list features
- [x] add stop to end
- [x] remove first matching stop
- [x] list stops in order
- [x] count stops

### Utility/report features
- [x] category counts
- [x] unique rooms
- [x] sort by age
- [x] linear search by name

### Integration
- [x] `demo_museum_night()`
- [x] at least 8 artifacts in demo
- [x] demo shows system parts working together

---

## Design note (150-250 words)

We chose a Binary Search Tree for the artifact archive because artifact IDs are unique integers that define a natural ordering. The BST allows efficient insert and search in O(h) time — where h is the tree height — without requiring all IDs to be known in advance. Inserting artifacts one by one and searching by ID maps directly to BST insert and lookup operations. Duplicate IDs are silently rejected and return `False`, which protects the archive from accidental overwriting.

A queue fits restoration requests naturally because the museum staff should process the oldest outstanding request first — classic first-in, first-out behavior. We backed it with `collections.deque` for O(1) front removal, which a plain Python list cannot guarantee.

A stack fits undo actions because the most recently performed action is always the first one a staff member would want to reverse — last-in, first-out order. A Python list with `append` and `pop` gives O(1) push and undo.

A singly linked list fits the exhibit route because the route is inherently sequential and changes often as stops are added or removed. Insertion at the tail and removal by name are natural linked-list operations, and there is no need for random index access that would justify an array.

The system is split into clearly separated classes for each data structure, with standalone utility functions for reporting, keeping responsibilities narrow and testable.

---

## Complexity reasoning

- `ArtifactBST.insert`: O(h) where h is the tree height, because we follow one root-to-leaf path comparing IDs at each node. In the average case with a balanced tree this is O(log n); in the worst case (sorted insertion) it is O(n).
- `ArtifactBST.search_by_id`: O(h) for the same reason — one path from root to the matching node or a leaf, comparing once per level.
- `ArtifactBST.inorder_ids`: O(n) where n is the number of nodes, because every node is visited exactly once during the recursive traversal.
- `RestorationQueue.process_next_request`: O(1) because `collections.deque.popleft()` removes from the front in constant time regardless of queue size.
- `ArchiveUndoStack.undo_last_action`: O(1) because Python list `pop()` removes from the end in constant time.
- `ExhibitRoute.remove_stop`: O(n) in the worst case because we may need to traverse the entire linked list to find the target stop before unlinking it.
- `sort_artifacts_by_age`: O(n log n) because it uses Python's built-in `sorted()`, which implements Timsort.
- `linear_search_by_name`: O(n) because in the worst case we scan every artifact in the list before finding a match or confirming it is absent.

---

## Edge-case checklist

### BST
- [x] insert into empty tree — the new node becomes the root and `insert` returns `True`.
- [x] search for missing ID — `_search_recursive` reaches `None` and returns `None`; `search_by_id` returns `None`.
- [x] empty traversals — all three traversal methods return `[]` when `self.root is None`.
- [x] duplicate ID — `_insert_recursive` detects equality and returns `False` without modifying the tree.

### Queue
- [x] process empty queue — `process_next_request` checks `is_empty()` first and returns `None`.
- [x] peek empty queue — `peek_next_request` checks `is_empty()` first and returns `None`.

### Stack
- [x] undo empty stack — `undo_last_action` checks `is_empty()` first and returns `None`.
- [x] peek empty stack — `peek_last_action` checks `is_empty()` first and returns `None`.

### Exhibit route linked list
- [x] empty route — `list_stops` returns `[]`; `count_stops` returns `0`; `remove_stop` returns `False`.
- [x] remove missing stop — traversal reaches the end without a match; returns `False`.
- [x] remove first stop — handled as a special case: `self.head` is advanced to `self.head.next`.
- [x] remove middle stop — the predecessor node's `next` pointer is redirected around the target node.
- [x] remove last stop — the predecessor node's `next` is set to `None`.
- [x] one-stop route — treated as a remove-head case; after removal `self.head` is `None`.

### Reports
- [x] empty artifact list — `count_artifacts_by_category` returns `{}`; `unique_rooms` returns `set()`; `sort_artifacts_by_age` returns `[]`; `linear_search_by_name` returns `None`.
- [x] repeated categories — the category count dictionary increments the existing key rather than creating a new one.
- [x] repeated rooms — the set comprehension in `unique_rooms` deduplicates automatically.
- [x] missing artifact name — `linear_search_by_name` reaches the end of the list without a match and returns `None`.
- [x] same-age artifacts — `sort_artifacts_by_age` uses Python's stable `sorted()`, so artifacts with equal ages preserve their original relative order.

---

## Demo plan / how to run

### Requirements
- Python 3.11 or later
- `pytest` (stdlib only for the main code; pytest is only needed for tests)

### Run the tests
```bash
pytest -q
```

### Run the integration demo
```bash
python -c "from src.project import demo_museum_night; demo_museum_night()"
```

### Expected demo output (summary)
The demo will print:
- All 8 artifacts inserted into the BST with duplicate rejection shown
- Inorder, preorder, and postorder traversal ID lists
- A successful artifact search and a failed search
- Restoration queue peek, process, and remaining size
- Undo stack peek, undo action, and remaining size
- Full exhibit route, then route after a stop is removed
- Category counts, unique rooms, age-sorted lists, and name search results

---

## Assistance & sources

- AI used? Y
- What it helped with: Scaffolding the starter code structure, checking edge-case logic for the linked list remove operation, and reviewing that demo output strings matched the required test assertions.
- Non-course sources used: Python 3 official documentation for `collections.deque` and `dataclasses`.
- Links:
  - https://docs.python.org/3/library/collections.html#collections.deque
  - https://docs.python.org/3/library/dataclasses.html