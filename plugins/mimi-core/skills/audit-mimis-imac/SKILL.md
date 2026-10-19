---
name: "audit-mimis-imac"
description: Installs or verifies and runs a macOS security audit toolchain (Lynis, rkhunter, chkrootkit, osquery and nmap) on the user's iMac, then summarises the logs into one status table with a plain-language verdict. Use when the user wants to check their Mac for security issues, hacking indicators, rootkits, suspicious startup items or open ports. Examples include "audit my Mac", "has my iMac been hacked?", "scan for rootkits", "what ports are open on my machine?" and "run my monthly security check".
---

# MacOS Security Audit (Imac M1)

A repeatable workflow for auditing a macOS machine using five open-source tools installed via Homebrew. Each tool checks a different layer: configuration hygiene, rootkit signatures, persistence mechanisms, and network exposure.

## Step 1 — Check for existing installs, then install what's missing

Never blind-install. Check first, so re-runs are fast and idempotent.

```bash
for pkg in lynis rkhunter chkrootkit osquery nmap; do
  if brew list "$pkg" &>/dev/null; then
    echo "[OK] $pkg already installed ($(brew list --versions "$pkg"))"
  else
    echo "[MISSING] Installing $pkg..."
    brew install "$pkg"
  fi
done
```

If any install fails, run `brew doctor` before retrying — most failures trace back to a stale Homebrew cache or a permissions conflict in `/opt/homebrew`.

## Step 2 — Run each tool and capture its output to a log

Create a working directory for this run, timestamped so past audits aren't overwritten.

```bash
AUDIT_DIR=~/security-audits/$(date +%Y-%m-%d_%H%M)
mkdir -p "$AUDIT_DIR"
```

### Lynis — full system configuration audit
```bash
sudo lynis audit system --no-colors | tee "$AUDIT_DIR/lynis.log"
```
Note: Lynis may prompt about file ownership on Homebrew-installed files. Pressing ENTER to continue is safe when the tool was installed by the user via `brew install` moments earlier.

### rkhunter — rootkit signature scan
```bash
sudo rkhunter --update
sudo rkhunter --check --sk | tee "$AUDIT_DIR/rkhunter.log"
```
`--sk` ("skip keypress") lets the scan run unattended through each section.

### chkrootkit — secondary rootkit cross-check
```bash
sudo chkrootkit | tee "$AUDIT_DIR/chkrootkit.log"
```

### osquery — persistence mechanism inspection
```bash
{
  echo "== LaunchAgents/Daemons referencing curl or wget =="
  osqueryi --json "SELECT name, program_arguments, path FROM launchd WHERE program_arguments LIKE '%curl%' OR program_arguments LIKE '%wget%';"
  echo "== All startup items =="
  osqueryi --json "SELECT name, path, status FROM startup_items;"
} | tee "$AUDIT_DIR/osquery.log"
```

### nmap — local exposed-port scan
```bash
sudo nmap -sT -O localhost -oN "$AUDIT_DIR/nmap.log"
```

## Step 3 — Parse each log and build the summary table

Read each log file in `$AUDIT_DIR` and extract:

| Tool | What to extract |
|---|---|
| `lynis.log` | The final "Hardening index" score, and count of lines starting with `Warning` / `Suggestion` |
| `rkhunter.log` | Count of lines containing `Warning`, and whether the final summary reports any infections |
| `chkrootkit.log` | Any line NOT containing `not found` or `nothing found` — those indicate a positive hit worth reviewing |
| `osquery.log` | Row count returned by each query — a nonzero `startup_items` count is expected and normal; flag only unrecognized entries |
| `nmap.log` | List of ports reported as `open`, plus the detected OS guess |

Present findings in this exact table format:

```
| Tool        | Status  | Key Finding                                    | Action Needed |
|-------------|---------|-------------------------------------------------|---------------|
| Lynis       | OK      | Hardening index: NN/100, N warnings              | ...           |
| rkhunter    | REVIEW  | N warnings, 0 infections found                   | ...           |
| chkrootkit  | OK      | N/A or list of positive hits                     | ...           |
| osquery     | ALERT   | N startup items, N unrecognized                  | ...           |
| nmap        | OK      | N open ports: [list]                             | ...           |
```

Status legend: `OK` clean, `REVIEW` needs review (non-critical warnings), `ALERT` positive finding requiring immediate investigation.

## Step 4 — Close with a plain-language summary

After the table, write 2–3 sentences in plain language: overall posture (clean / minor hygiene issues / needs attention), and the single highest-priority item to address, if any. Do not alarm the user over routine Lynis suggestions (these are nearly always present on any machine) — reserve `ALERT` status for actual rkhunter/chkrootkit positive hits or unexpected open ports.

## Notes

- All five tools are read-only auditors; none of them modify the system. Running them repeatedly is safe.
- Re-run this skill periodically (monthly is reasonable for a personal machine) and diff the summary tables across runs to spot new findings quickly.
- If `chkrootkit` or `rkhunter` report a positive finding, do not treat it as confirmed compromise on its own — cross-reference the specific file or process named against a fresh web search before taking remedial action, since both tools are known for occasional false positives on legitimate development tools.