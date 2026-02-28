# Task Threads - Priority Stack Ranking: Auto-Add Issue Flows

> **Last Updated:** February 28, 2026
>
> This document maps how issues from all connected repositories automatically flow into the
> [Task Threads - Priority Stack Ranking](https://github.com/orgs/Balancing-Rock/projects/4) project.

## Architecture Overview

```mermaid
flowchart TD
    subgraph PROJECT["Task Threads - Priority Stack Ranking\n(GitHub Project V2)"]
        BOARD["Unified Project Board\nPrioritize | Track | Manage"]
    end

    subgraph WORKFLOW_A["Built-in Auto-Add Workflows\n(GitHub Project Settings)"]
        W1["Auto-add to project\nRepo: stacks-ranking-priorities\nFilter: is:issue"]
        W2["Auto-add: command-center-so\nRepo: command-center-so\nFilter: is:issue"]
        W3["Auto-add: stack-ranked-priorities\nRepo: stack-ranked-priorities\nFilter: is:issue"]
        W4["Auto-add: Food-Tracking_App\nRepo: Food-Tracking_App\nFilter: is:issue"]
        W5["Auto-add: sscs-qbo-sync\nRepo: sscs-qbo-sync\nFilter: is:issue"]
    end

    subgraph WORKFLOW_B["GitHub Actions Workflows\n(.github/workflows/auto-add-to-project.yml)"]
        A1["actions/add-to-project@v1.0.2\nTrigger: issues.opened\nSecret: ADD_TO_PROJECT_PAT"]
    end

    subgraph REPOS_BUILTIN["Repos via Built-in Workflows"]
        R1[(stacks-ranking-priorities)]
        R2[(command-center-so)]
        R3[(stack-ranked-priorities)]
        R4[(Food-Tracking_App)]
        R5[(sscs-qbo-sync)]
    end

    subgraph REPOS_ACTIONS["Repos via GitHub Actions"]
        R6[(task-threads)]
        R7[(demo-repository)]
        R8[(Speed-Reader-App)]
    end

    R1 -->|"new/updated issue"| W1
    R2 -->|"new/updated issue"| W2
    R3 -->|"new/updated issue"| W3
    R4 -->|"new/updated issue"| W4
    R5 -->|"new/updated issue"| W5

    R6 -->|"issue opened"| A1
    R7 -->|"issue opened"| A1
    R8 -->|"issue opened"| A1

    W1 --> BOARD
    W2 --> BOARD
    W3 --> BOARD
    W4 --> BOARD
    W5 --> BOARD
    A1 --> BOARD

    style PROJECT fill:#238636,stroke:#2ea043,color:#fff
    style WORKFLOW_A fill:#1f6feb,stroke:#388bfd,color:#fff
    style WORKFLOW_B fill:#8957e5,stroke:#a371f7,color:#fff
    style REPOS_BUILTIN fill:#21262d,stroke:#30363d,color:#c9d1d9
    style REPOS_ACTIONS fill:#21262d,stroke:#30363d,color:#c9d1d9
```

## How It Works

### Method 1: Built-in Project Workflows (5 repos)

| Workflow Name | Repository | Filter | Trigger |
|---|---|---|---|
| Auto-add to project | `stacks-ranking-priorities` | `is:issue` | New or updated issue |
| Auto-add: command-center-so | `command-center-so` | `is:issue` | New or updated issue |
| Auto-add: stack-ranked-priorities | `stack-ranked-priorities` | `is:issue` | New or updated issue |
| Auto-add: Food-Tracking_App | `Food-Tracking_App` | `is:issue` | New or updated issue |
| Auto-add: sscs-qbo-sync | `sscs-qbo-sync` | `is:issue` | New or updated issue |

**Limit:** GitHub Team plan supports max 5 auto-add workflows per project.

### Method 2: GitHub Actions (3 repos)

| Repository | Workflow File | Trigger | Auth |
|---|---|---|---|
| `task-threads` | `.github/workflows/auto-add-to-project.yml` | `issues: [opened]` | `ADD_TO_PROJECT_PAT` org secret |
| `demo-repository` | `.github/workflows/auto-add-to-project.yml` | `issues: [opened]` | `ADD_TO_PROJECT_PAT` org secret |
| `Speed-Reader-App` | `.github/workflows/auto-add-to-project.yml` | `issues: [opened]` | `ADD_TO_PROJECT_PAT` org secret |

**Action used:** `actions/add-to-project@v1.0.2`

## Key Principle: Separation of Concerns

- **Issues live in their repos.** Each issue retains its repo-level context: labels, milestones, branches, PRs, and CI/CD.
- **The project is an organizational layer.** It provides a unified cross-repo view for centralized prioritization and tracking.
- **Work happens in the repo.** Branching, code review, and merging all stay scoped to the originating repository.

## Authentication

- **Org Secret:** `ADD_TO_PROJECT_PAT` (classic PAT with `repo` + `project` scopes)
- **Visibility:** All private repositories in the Balancing-Rock org
- **Expiration:** No expiration (monitor and rotate as needed)
