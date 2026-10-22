---
name: backup-project
description: Briefs the user on CLI steps to back up a local project to GitHub, together with a checklist of their current local system setup (Git, GitHub CLI, identity, credentials, SSH) and their access to GitHub. Run from the VS Code integrated terminal at the project root. Use this whenever the user invokes /backup-project or says things like "back up my project", "push this to GitHub", "put my code on GitHub", "save my project to GitHub", "check my GitHub setup", "is Git set up", "can I push to GitHub", or "why can't I push", even if they don't mention Git or the CLI explicitly.
---

# Backup Project

Help the user back up the project in their open VS Code workspace to GitHub using only terminal commands. The skill has two jobs: first confirm the local machine and GitHub access are ready, then give the shortest reliable set of CLI steps to create the backup and to repeat it later.

A backup only counts if it can be restored, and most failed pushes come from a missing identity, an expired login, or secrets nearly committed by accident. That is why the readiness checklist comes before the steps, and why the steps include a safety review of what is about to be uploaded.

## Arguments (both optional)

| Argument | Meaning | Default |
|----------|---------|---------|
| `repo` | Name for the GitHub repository | The workspace folder's name |
| `visibility` | `private` or `public` | `private` |

Invocation example: `/backup-project repo="habit-tracker" visibility="private"`

Accept `key="value"` form or plain natural language. Never default to public. Only use `--public` when the user explicitly asks for it.

## Assumptions

- The project is open in VS Code and commands are run in the integrated terminal (Ctrl+` on Windows/Linux, Cmd+` on macOS) from the project root.
- On Windows the terminal is PowerShell unless the user says otherwise.
- `<name>` is the repository name (the `repo` argument, otherwise the folder name, kebab-case).
- Replies stay in chat as steps and commands. Do not produce zip files or pre-built project files.

## Workflow

1. **Ask the questionnaire** (below), then stop and wait.
2. **Reply with the output template**: the readiness checklist first, then the backup steps that match the user's answers.
3. **Offer troubleshooting**: end by inviting the user to paste any failing command's output so you can give the exact fix.

## Questionnaire rules

- All questions are multiple choice. Use the `ask_user_input_v0` tool when it is available (1 to 3 questions per call, 2 to 4 options each); otherwise present lettered options in chat.
- Ask exactly these three together in one turn, skipping any the user has already answered:
  1. **Operating system:** macOS / Windows / Linux
  2. **How do you prefer to sign in to GitHub?** GitHub CLI login (recommended) / SSH key / HTTPS with a personal access token / Not sure, recommend one
  3. **Project state:** Not a Git repository yet / Already a Git repository with no remote / Already has a GitHub remote
- If the user picks "Not sure", choose GitHub CLI login and say so in one line.

## Readiness checklist

Present this as a checkbox list. Each item shows the command, what a pass looks like, and, in an "If not" line, the fix. Include only the items that apply to the user's answers (for example, skip the SSH item for GitHub CLI login, and skip the project-state items that are irrelevant).

Also give one combined diagnostic block the user can paste in a single go, in the right shell syntax for their OS, so they can tick everything quickly.

| # | Check | Command | Pass looks like | If not |
|---|-------|---------|-----------------|--------|
| 1 | Git installed | `git --version` | A version number prints | macOS `xcode-select --install` or `brew install git`; Windows `winget install --id Git.Git -e`; Ubuntu/Debian `sudo apt install git` |
| 2 | Git identity set | `git config --global user.name` and `git config --global user.email` | Both print a value | `git config --global user.name "<Your Name>"` and `git config --global user.email "<you@example.com>"` |
| 3 | Default branch is `main` | `git config --global init.defaultBranch` | Prints `main` | `git config --global init.defaultBranch main` |
| 4 | GitHub CLI installed | `gh --version` | A version number prints | macOS `brew install gh`; Windows `winget install --id GitHub.cli -e`; Linux see cli.github.com for the package repository |
| 5 | Signed in to GitHub | `gh auth status` | Shows "Logged in to github.com" with a token that includes the `repo` scope | `gh auth login` (choose GitHub.com, your preferred protocol, and the browser flow). To add scope: `gh auth refresh -s repo` |
| 6 | Git uses your GitHub login (HTTPS only) | `gh auth setup-git` | Completes with no error | Re-run after `gh auth login` |
| 7 | SSH access works (SSH only) | `ssh -T git@github.com` | Message says you have successfully authenticated | Create a key with `ssh-keygen -t ed25519 -C "<you@example.com>"`, then upload it with `gh ssh-key add ~/.ssh/id_ed25519.pub` (PowerShell: `$HOME\.ssh\id_ed25519.pub`) |
| 8 | GitHub API reachable with your account | `gh api user --jq .login` | Prints your GitHub username | Re-run check 5; if it still fails, check network or proxy settings |
| 9 | Project is a Git repository | `git rev-parse --is-inside-work-tree` | Prints `true` | Handled by backup step 1 |
| 10 | Remote configured | `git remote -v` | Shows `origin` pointing at the intended repository, or nothing yet if not set up | Handled by backup step 4 |
| 11 | Working tree status | `git status --short` | Shows what is uncommitted, so you know what the next backup will include | Not a failure; review before committing |

For the HTTPS with personal access token preference, recommend GitHub CLI login instead (it stores the credential in the system credential manager). Never suggest putting a token in a remote URL, a script, or a file in the project.

## Backup steps

Tailor to the user's project state and sign-in choice. Keep each step to one line of instruction plus a copy-paste block.

**Step 1: Initialise the repository** (skip if already a repository)
```
git init -b main
```

**Step 2: Add a `.gitignore`** (skip if one exists). Pull GitHub's official template for the project's language (for example `Python`, `Node`, `Go`, `C`, `C++`):
```
gh api /gitignore/templates/<Template> --jq .source > .gitignore
```
PowerShell form (avoids a UTF-16 file that Git would misread):
```
gh api /gitignore/templates/<Template> --jq .source | Set-Content -Encoding ascii .gitignore
```

**Step 3: Review, then make the first commit**

Preview what will be uploaded and check that no secrets (`.env` files, keys, credentials) appear in the list:
```
git add --dry-run .
```
If anything sensitive is listed, add it to `.gitignore` first. Then commit:
```
git add .
git commit -m "Initial commit"
```

**Step 4: Create the GitHub repository and push**

Not yet on GitHub (private is the default; use `--public` only when asked):
```
gh repo create <name> --private --source=. --remote=origin --push
```
Repository already exists on GitHub:
```
git remote add origin <repository-url>
git push -u origin main
```
Use the HTTPS URL for GitHub CLI or token logins, and the `git@github.com:<owner>/<name>.git` form for SSH.

**Step 5: Verify the backup**
```
git status -sb
gh repo view <name>
```
`git status -sb` should show `main` with no "ahead" or "behind" marker. For a stronger check, confirm the backup restores cleanly into a throwaway folder (then delete it):
```
gh repo clone <name> ../<name>-restore-check
```

**Repeating the backup later**
```
git add -A
git commit -m "<what changed>"
git push
```

Notes to add only when relevant:
- Files over 100 MB are rejected by GitHub. If the project has large assets, suggest Git LFS (`git lfs install`, then `git lfs track "<pattern>"`).
- If a push is rejected because the remote has changes, run `git pull --rebase` and then `git push`. Do not suggest force-pushing for a backup.
- If a secret was already committed, tell the user to rotate that secret immediately, since removing it from history does not make it safe.

## Output template

Use this structure.

````
## Backup plan: <name> (<OS>, <sign-in method>)
**Your choices:** <one-line recap, including visibility>
**Where:** VS Code integrated terminal, project root

### Part 1: Readiness checklist
Run this block and tick each item:
```<bash | powershell>
<combined diagnostic commands>
```
- [ ] <check 1: pass looks like ...>
  If not: <fix command>
- [ ] <check 2> ...

### Part 2: Backup steps
#### Step 1: <short title>
<one-line instruction>
```<bash | powershell>
<commands>
```
...

### Next backups
```<bash | powershell>
git add -A
git commit -m "<what changed>"
git push
```
````

End with one line: "Paste the output of any check that failed and I'll give you the exact fix."

Formatting rules:
- Use `bash` fences for macOS and Linux, `powershell` fences for Windows. In PowerShell blocks, put each command on its own line instead of chaining with `&&`.
- Commands are plain and copy-ready, with no `$` prompts.
- Keep every instruction to one line. One short clause of why is enough when a step is not obvious.
- Do not echo, request, or store tokens, passwords, or private keys. If the user pastes one by mistake, tell them to revoke it and create a new one.
- Skip checks and steps the user's answers make unnecessary.
