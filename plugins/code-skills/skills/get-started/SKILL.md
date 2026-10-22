---
name: "get-started"
description: Interactive, strictly local project-setup guide that scaffolds a new project inside the user's already-open, empty VS Code workspace folder, step by step in chat, using official generators and templates rather than hand-built files. Supports Python, React (TypeScript or JavaScript), React Native, C/C++, Go, and Bash/sh scripting. Requires two arguments, `task` (short project brief) and `stack` (tech stack). Use this whenever the user invokes /get-started or says things like "get started", "set up a new project", "scaffold", "bootstrap", "init a project", "new app", or "help me start a Python/React/Go/C++/Bash project", even if they don't name a tool or language explicitly.
---

# Get Started

Guide the user through setting up a brand-new coding project on their own machine. Everything runs in the **VS Code integrated terminal**, in the workspace folder that is **already open and empty**. The goal is a project scaffolded in place by a real generator, with dependencies installed and a starter that runs. Application logic comes later, as a separate request.

Setup commands differ by operating system, version manager, and project type, so ask a few targeted multiple-choice questions first, then give a short, copy-paste-ready plan that fits those answers.

## Scope: strictly local

- The project lives only on this machine. Do not mention, suggest, or configure Git, GitHub, remotes, CI, deployment, hosting, or any collaboration workflow.
- Generators often run `git init` by default. Switch that off with the flag listed in the stack reference so no repository is created.
- Do not create new project folders or ask the user to `cd` into one. Scaffold into the current directory (`.`), because the open folder is the project root.

## Arguments

The user must supply both arguments. Accept either `key="value"` form or plain natural language.

| Argument | Meaning | Example |
|----------|---------|---------|
| `task` | One-line brief of what the project is for | `task="REST API for a todo list"` |
| `stack` | Tech stack to use | `stack="python"` |

Invocation example: `/get-started task="habit tracker mobile app" stack="react-native"`

Normalise `stack` to one of these identifiers (match loosely, e.g. "TS React" → `react-ts`):

`python` · `react-ts` · `react-js` · `react-native` · `c` · `cpp` · `go` · `bash`

If an argument is missing or ambiguous:
- `task` missing: ask for it in one short line (the one place a free-text answer is unavoidable).
- `stack` missing: show the supported stacks as a lettered list and wait.
- "React" with no language: ask TypeScript or JavaScript. "C/C++" with no preference: infer from the task, otherwise ask.
- A stack outside this list: say it is not covered by this skill and stop.

## Assumptions

- VS Code is open on an empty folder, and the user will run commands in its integrated terminal (Ctrl+` on Windows/Linux, Cmd+` on macOS) from the workspace root.
- On Windows the integrated terminal is PowerShell unless the user says otherwise.
- `<name>` is the project name. Use the workspace folder's name when it is a valid identifier; otherwise derive a kebab-case name from `task` (for example "habit tracker" → `habit-tracker`). Define it once and use it consistently.
- Replies stay in chat. Do not produce zip files, pre-built project files, or artifacts containing project code.

## Workflow

1. **Parse** `task` and `stack` (above).
2. **Ask the questionnaire** (below). Stop and wait for answers. Do not give any setup steps beforehand.
3. **Pick the scaffold route** from the answers using the stack reference below.
4. **Reply with the setup plan** using the output template.
5. **Close** with one line offering to help build the actual features once the starter runs.

If the user later reports an error, ask them to paste the message, then give the fix as a command block. A common cause is the folder not being empty, since most generators refuse to scaffold into a non-empty directory.

## Questionnaire rules

- Every question is multiple choice. Use the `ask_user_input_v0` tool when it is available (1 to 3 questions per call, 2 to 4 options each); otherwise present lettered options in chat.
- Tailor questions to the given `task` and `stack`. Skip anything the user has already stated or that the task makes obvious.
- Ask at most 3 questions in total, and ask them together in a single turn.
- Question 1 is always the operating system: **macOS / Windows / Linux**.
- Question 2 is the stack's environment or toolchain question.
- Question 3 is the stack's project-shape question, informed by `task`.
- Where it helps, include a "Not sure, recommend one" option and then choose the sensible default.

### Question bank (adapt wording to the task)

| Stack | Q2: environment | Q3: project shape |
|-------|-----------------|-------------------|
| `python` | Environment manager already installed or preferred: uv / Poetry / conda / venv + pip | Script or CLI / Web API (FastAPI, Flask) / Django web app / Data or ML notebook |
| `react-ts`, `react-js` | Node setup: nvm / fnm / Volta / Not installed. Plus package manager if unclear: npm / pnpm / yarn / bun | Single-page app (Vite) / Full-stack or SEO site (Next.js) |
| `react-native` | Approach: Expo (recommended) / Bare React Native CLI / Not sure | Test target: iOS simulator (macOS only) / Android emulator / Physical phone |
| `c`, `cpp` | Compiler toolchain: GCC / Clang / MSVC / Not installed | Build system: CMake + Conan / Meson / Not sure |
| `go` | Go status: Not installed / Installed already / Using a version manager | Executable (simple) / CLI with subcommands / HTTP server / Library |
| `bash` | Tooling: ShellCheck + shfmt + bats installed / Partly / None | Target shell: Bash / Bash that must work on macOS default 3.2 / POSIX sh only |

If the user is on Windows and the stack is `bash`, recommend WSL and treat the environment as Linux inside it. VS Code can attach its terminal to WSL with `code .` run from the WSL shell.

## Stack reference

Use these routes. Every route uses an official or widely adopted generator, run **in place** in the empty workspace folder. Never tell the user to create project files or folder layouts by hand, or to paste in file contents. If a route does not exist for a case, say so plainly and pick the closest generator instead.

Generators change flags between releases, especially the in-place and no-git options. When web search is available, quickly confirm the current command for the chosen generator before replying.

### python
- **uv:** `uv init --vcs none` (add `--package` for an installable `src/` layout), then `uv add <deps>` and `uv run main.py`. For `--package`, run the entry point with `uv run <name>`.
- **Poetry:** `poetry new --name <name> .`, then `poetry add <deps>` and `poetry run pytest`.
- **conda or venv + pip:** create and activate the environment first (`conda create -n <name> python=3.12 -y` then `conda activate <name>`, or `python -m venv .venv` then activate it), then `pip install uv`, `uv init --package --vcs none`, `pip install -e .`, and run the entry point `<name>`.
- **Django:** add Django, then `django-admin startproject <name_underscored> .` and `python manage.py runserver` (prefix with `uv run` under uv).
- **Web API:** add `fastapi[standard]` or `flask` as the dependency and verify with the starter's run command; no hand-written layout.
- **Data or ML:** add `pandas jupyterlab`, then launch with `jupyter lab`.
- **Install uv:** macOS/Linux `curl -LsSf https://astral.sh/uv/install.sh | sh` (or `brew install uv`); Windows `winget install --id=astral-sh.uv -e`.
- **VS Code:** `code --install-extension ms-python.python`

### react-ts / react-js
- **Vite SPA:** `npm create vite@latest . -- --template react-ts` (use `--template react` for JavaScript). pnpm: `pnpm create vite . --template react-ts`. yarn: `yarn create vite . --template react-ts`. bun: `bun create vite . --template react-ts`.
- Then install (`npm install`) and run (`npm run dev`).
- **Next.js:** `npx create-next-app@latest . --typescript --disable-git` (use `--javascript` for JS), then `npm run dev`.
- **Node install:** fnm `fnm install --lts` then `fnm use`; nvm `nvm install --lts`; Volta `volta install node`; none installed: macOS `brew install node`, Windows `winget install OpenJS.NodeJS.LTS`.
- **VS Code:** `code --install-extension dbaeumer.vscode-eslint` and `esbenp.prettier-vscode`

### react-native
- **Expo:** `npx create-expo-app@latest .` (add `--template blank-typescript` or `--template blank` for a minimal start), then `npx expo start`. Verify with `npx expo-doctor`.
- **Bare CLI:** `npx @react-native-community/cli@latest init <PascalCaseName> --directory . --skip-git-init`, then `npx react-native doctor` and `npx react-native run-android` or `run-ios`.
- iOS simulators need macOS with Xcode (`xcode-select --install`). On Windows and Linux, target Android (Android Studio: macOS `brew install --cask android-studio`, Windows `winget install Google.AndroidStudio`) or a physical phone running Expo Go.
- JavaScript-only requests: use Expo's `blank` template.

### c / cpp
- **C++ with CMake + Conan:** install Conan (`pip install conan`), run `conan profile detect --force`, then `conan new cmake_exe -d name=<name> -d version=0.1` (writes into the current folder), `conan install . --build=missing`, `conan build .`. Run the binary from `build/Release/` (`.exe` on Windows).
- **C, or Meson preference:** `pip install meson ninja`, then `meson init --name <name> --language c` (use `cpp` for C++), `meson setup builddir`, `meson compile -C builddir`, `./builddir/<name>`. The Conan template is C++ only, so C always goes through Meson.
- **Compilers:** macOS `xcode-select --install`; Ubuntu/Debian `sudo apt install build-essential cmake`; Windows MSVC `winget install Microsoft.VisualStudio.2022.BuildTools` (select the C++ workload and open a Developer PowerShell inside VS Code's terminal profiles) and CMake `winget install Kitware.CMake`.
- **VS Code:** `code --install-extension ms-vscode.cpptools`, `ms-vscode.cmake-tools` (CMake) or `mesonbuild.mesonbuild` (Meson)

### go
- **Install Go:** macOS `brew install go`; Windows `winget install GoLang.Go`; Linux from go.dev/dl. Verify with `go version`.
- **CLI with subcommands (scaffolds in place):** `go install github.com/spf13/cobra-cli@latest`, `go mod init <name>`, `cobra-cli init`, `go run .`.
- **Executable, library, or HTTP server:** `gonew` always writes into a new subfolder, so scaffold and flatten into the workspace root.
  - Install: `go install golang.org/x/tools/cmd/gonew@latest`
  - Template: `golang.org/x/example/hello` (executable or library) or `golang.org/x/example/helloserver` (HTTP server)
  - macOS/Linux: `gonew <template> <name> && cp -R <name>/. . && rm -rf <name>`
  - PowerShell: `gonew <template> <name>`, then `Move-Item <name>\* .`, then `Remove-Item <name>`
  - Then `go run .`
- If `gonew` or `cobra-cli` is not found, add Go's bin folder to PATH: `export PATH="$PATH:$(go env GOPATH)/bin"` (PowerShell: `$env:Path += ";$(go env GOPATH)\bin"`).
- **VS Code:** `code --install-extension golang.go`

### bash
- **Tooling:** macOS `brew install shellcheck shfmt bats-core`; Ubuntu/Debian/WSL `sudo apt install shellcheck shfmt bats`.
- **Scaffold with Bashly (in place):** `gem install bashly` (needs Ruby) or the Docker form `docker run --rm -it --user $(id -u):$(id -g) --volume "$PWD:/app" dannyben/bashly init`. Then `bashly init`, `bashly generate`, and verify with `./download --help`.
- Bashly generates Bash scripts. If the user needs strictly POSIX sh, say that clearly: no mainstream generator targets it, so set up only the tooling (ShellCheck with `--shell=sh`, shfmt with `-ln posix`) and offer to author the script together in a follow-up rather than leaving them to assemble it by hand.
- **VS Code:** `code --install-extension timonwong.shellcheck` and `foxundermoon.shell-format`

## Output template

Use this structure for the setup plan. Keep each instruction to one line.

````
## Setup plan: <name> (<stack>, <OS>)
**Your choices:** <one-line recap of the answers>
**Where:** VS Code integrated terminal, workspace root (empty folder)

### Step 1: <short title>
<one-line instruction>
```<bash | powershell>
<copy-paste commands>
```

### Step 2: <short title>
...

### Final check
<one line saying what success looks like, for example "the dev server prints a local URL">
````

Formatting rules:
- 4 to 7 steps, in this order: confirm the folder is empty, prerequisites, scaffold in place, install dependencies, run or verify, VS Code extensions.
- The empty-folder check is `ls -A` (macOS/Linux) or `Get-ChildItem -Force` (PowerShell); it should print nothing.
- Commands are plain and copy-ready: no `$` prompts, and only add comments where a flag would otherwise confuse.
- Use `bash` fences for macOS and Linux, `powershell` fences for Windows. In PowerShell blocks, put each command on its own line instead of chaining with `&&`.
- Skip steps the user's answers make unnecessary (for example, skip installing Node if they already have it).
- Never include `cd` into a new folder, `git` commands, repository setup, file contents, hand-written project structures, or instructions to create source files manually.
- Do not explain the commands at length. One short clause of why is enough when a choice is not obvious.
