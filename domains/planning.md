# Domain: planning

Judgment about decomposing roadmap capabilities into sequenced task lists and managing the work
queue. Declared by the **planner** lens. Provenance and per-kill detail in `domains/audit.md`.

Also defines the **queue file schema** (`corpora/queue.md`) — the planner writes it, the
orchestrator reads it in loop mode.

---

## Queue file schema

The queue lives at `corpora/queue.md` in the project root. One active capability at a time.

```yaml
capability: "Exact capability statement from ROADMAP.md"
area: "Area name from ROADMAP.md"
status: active       # active | complete | on-hold
created: YYYY-MM-DD
updated: YYYY-MM-DD

tasks:
  - id: <area-abbrev>-<nn>      # e.g. disc-01, song-03
    title: "Short, actionable title"
    description: "What this task requires and what its output is."
    context: ""                  # what the planner found during orientation: current state, relevant
                                 # files, what exists vs. what is missing. Also: any concepts this
                                 # task shares with other tasks in this capability — state, data, or
                                 # behavior that multiple tasks will read or mutate — so the executing
                                 # spawn starts with the interaction surface visible, not just the
                                 # task's own scope. Populated by the planner so the executing spawn
                                 # does not re-derive it.
    status: pending              # pending | in-progress | complete | blocked
    blocked-by: []               # list of task ids this task cannot start without
    parallel-ok: false           # true if this task can run alongside its non-blocking peers
    concern: ""                  # what kind of work this task involves — open-ended, named from
                                 # what orientation found (e.g. visual, interaction, implementation).
                                 # The orchestrator routes from this; the planner does not name lenses.
    judgment: ""                 # settled | uncertain — whether orientation found established project
                                 # patterns that cover this work, or genuine novel territory where
                                 # judgment under uncertainty is required.
    notes: ""                    # planner or orchestrator notes; resolution of open questions

open-questions:
  - id: q-<nn>
    question: "The unanswered question that must be resolved before the task(s) that depend on it."
    blocks: []                   # list of task ids this question blocks
    resolved: false
    answer: ""
```

Rules:
- `id` must be stable once written — the orchestrator uses it to mark status.
- A task whose `blocked-by` list is non-empty and contains any `pending` or `in-progress` ids
  cannot be started.
- A question that is `resolved: false` blocks all tasks in its `blocks` list.
- The orchestrator updates `status` on tasks and `resolved`/`answer` on questions in-place.
- When all tasks are `complete` and all questions are `resolved`, set the top-level `status` to
  `complete`.

---

```yaml
last-retrospective: none

principles:

- id: task-is-actionable-without-planning
  rule: "A task must be specific enough that the orchestrator can route it and a spawn can act on it without doing planning work of its own. If a task description requires the spawn to first decide what the task actually is, it is not yet a task."
  condition: "When decomposing a capability into tasks."
  reason: "The planner's job is to consume the ambiguity so executing spawns do not have to. A task that delegates planning back to the spawn negates the benefit of the queue and makes loop-mode orchestration unreliable."

- id: sequence-by-output-dependency
  rule: "Sequence tasks by what each task's output is required by, not by assumed lens order. Two tasks that don't depend on each other's output are parallelizable regardless of which lens would handle them."
  condition: "When ordering tasks in the queue."
  reason: "Lens order (ux-design before ui-design before coder) is a heuristic, not a law. It breaks when tasks within a capability don't align with that order. Output dependency is the correct sequencing signal — it holds regardless of who does the work."

- id: open-questions-are-explicit
  rule: "A question the planner cannot resolve from available information must appear as an explicit open question in the queue, with the tasks it blocks listed — never a silent assumption. This includes a shared runtime concept (a current position, a selection, a history, a running count) that two or more decomposed tasks would each need to read or mutate: name the concept, state the conflict, and block every affected task rather than letting them independently decide how it behaves."
  condition: "When a decomposition decision hinges on information the planner does not have — including when a capability description implies multiple tasks will operate on the same underlying runtime concept (e.g. undo + filter, pagination + sort, bookmark + search)."
  reason: "Silent assumptions compound: an unresolved question that travels silently into a task produces a deliverable built on an unknown foundation. This is especially costly for a shared concept — tasks that independently decide how it behaves are locally correct but globally inconsistent, and the conflict only surfaces at runtime, where it's expensive to fix. Making it explicit at planning time moves that cost to where it's cheap — one operator answer becomes context for every affected task."

- id: task-describes-output-not-implementation
  rule: "A task description states the observable output and its acceptance condition. It does not name files, functions, types, or data paths the executing spawn should touch."
  condition: "When writing or reviewing any task description in the queue."
  reason: "Naming implementation details couples the plan to a specific approach before the coder has seen the code. It narrows the solution space unnecessarily and makes the queue wrong the moment the code diverges from the assumption — without any signal that it has. The coder's job is to decide how; the planner's job is to decide what."

- id: concern-names-work-not-role
  rule: "When setting a task's `concern` field, name the character of the work (e.g. visual, interaction, implementation) as orientation revealed it — never a lens that should perform it."
  condition: "When decomposing a capability into tasks and populating each task's `concern` field."
  reason: "Naming a lens there pre-empts a routing decision the planner doesn't own, and removes the orchestrator's flexibility — e.g. it blocks the lighter surface-to-operator path for settled work, which routes off `concern`/`judgment` signals rather than a lens assignment."

killed:

- id: surface-shared-concept-before-implementation
  rule: "When orientation reveals that two or more tasks in the decomposition will operate on the same runtime concept — a current position, a selection, a history, a running count — add an open question naming that concept, stating the conflict or ambiguity, and blocking all affected tasks. Do not decompose into tasks that will independently decide how a shared concept behaves."
  kill_type: quality
  reason_killed: "Merged into open-questions-are-explicit as a named instance — a shared concept two tasks would each touch is exactly 'information the planner doesn't have.' The lens itself already states the general test in prose (step 3, 'Settle open questions')."
```
