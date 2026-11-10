---
title: AI-assisted campaign targets Linux infrastructure
source: https://unit42.paloaltonetworks.com/ai-campaign-targets-linux-infrastructure/
published: 2026-10
domain: SECURITY
---

## Summary

The attackers focused on Linux environments to run extensive reconnaissance and keep persistent network access for intelligence gathering. They tried to dump sensitive databases and exfiltrate government mailboxes to reach social media accounts. Entry and persistence relied on editing `.bashrc`, inserting malicious code into PHP scripts and scanning for cleartext passwords. A fake password prompt mimicking the system's sudo prompt captured credentials and passed them on to the real `sudo`, logging them to a file named `Solarwinds.StatusLog.txt` to blend in; the article states there is no evidence SolarWinds systems were compromised. Tooling included a multi-platform remote access trojan (SysGoRAT), reverse shells, web shells, NetCat, LinPEAS and a PwnKit exploit attempt (CVE-2021-4034).

## Case studies

- attack_linux_via_campaigns

## Key takeaways

- Enforce strict outbound firewall rules and use endpoint detection to spot standard utilities spawning interactive shells.
- Monitor shell start-up files (`.bashrc`) and web application scripts for unexpected changes.
- Keep passwords out of configuration files and command history; search for them before attackers do.
- Patch local privilege-escalation bugs such as PwnKit (CVE-2021-4034).
