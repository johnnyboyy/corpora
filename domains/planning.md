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
                                 # role starts with the interaction surface visible, not just the
                                 # task's own scope. Populated by the planner so the executing role
                                 # does not re-derive it.
    status: pending              # pending | in-progress | complete | blocked
    blocked-by: []               # list of task ids this task cannot start without
    parallel-ok: false           # true if this task can run alongside its non-blocking peers
    concern: ""                  # what kind of work this task involves — open-ended, named from
                                 # what orientation found (e.g. visual, interaction, implementation).
                                 # The orchestrator routes from this; the planner does not name roles.
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
  rule: "A task must be specific enough that the orchestrator can route it and a role can act on it without doing planning work of its own. If a task description requires the role to first decide what the task actually is, it is not yet a task."
  condition: "When decomposing a capability into tasks."
  reason: "The planner's job is to consume the ambiguity so roles do not have to. A task that delegates planning back to the role negates the benefit of the queue and makes loop-mode orchestration unreliable."

- id: sequence-by-output-dependency
  rule: "Sequence tasks by what each task's output is required by, not by assumed role order. Two tasks that don't depend on each other's output are parallelizable regardless of which roles would handle them."
  condition: "When ordering tasks in the queue."
  reason: "Role order (UX before UI before coder) is a heuristic, not a law. It breaks when tasks within a capability don't align with that order. Output dependency is the correct sequencing signal — it holds regardless of who does the work."

- id: open-questions-are-explicit
  rule: "A question the planner cannot resolve from available information must appear as an explicit open question in the queue, with the tasks it blocks listed. Do not make an assumption and proceed silently."
  condition: "When a decomposition decision hinges on information the planner does not have."
  reason: "Silent assumptions compound. An unresolved question that travels silently into a task produces a deliverable built on an unknown foundation. Making the question explicit lets the orchestrator surface it to the operator before work begins."

- id: task-describes-output-not-implementation
  rule: "A task description states the observable output and its acceptance condition. It does not name files, functions, types, or data paths the role should touch."
  condition: "When writing or reviewing any task description in the queue."
  reason: "Naming implementation details couples the plan to a specific approach before the coder has seen the code. It narrows the solution space unnecessarily and makes the queue wrong the moment the code diverges from the assumption — without any signal that it has. The coder's job is to decide how; the planner's job is to decide what."

- id: surface-shared-concept-before-implementation
  rule: "When orientation reveals that two or more tasks in the decomposition will operate on the same runtime concept — a current position, a selection, a history, a running count — add an open question naming that concept, stating the conflict or ambiguity, and blocking all affected tasks. Do not decompose into tasks that will independently decide how a shared concept behaves."
  condition: "When a capability description mentions multiple features (e.g. undo + filter, pagination + sort, bookmark + search) that imply a shared underlying concept the tasks will each need to read or mutate."
  reason: "Tasks that independently decide how a shared runtime concept behaves produce implementations that are locally correct but globally inconsistent. The conflict only appears at runtime, where it is expensive to fix. Surfacing it as a blocked open question moves the cost to planning time, where it is cheap — one operator answer becomes context for every affected task."

killed:
```
