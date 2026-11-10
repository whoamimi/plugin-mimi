---
title: Securing AWS AgentCore harness credentials
source: https://unit42.paloaltonetworks.com/securing-aws-agentcore-harness-credentials/
published: 2026-10
domain: AI
---

## Summary

An agent harness that processes incoming support tickets can be steered by instructions hidden in the ticket's HTML. In the case described, a POST request carrying a crafted support ticket caused the harness to run a hidden function that returned its JWT credentials and the URL of its MCP server. With those, an attacker can call the agent's downstream integrations with the harness's own permissions. The exposure comes from defaults: built-in shell and file tools enabled for every session, and service accounts scoped more widely than each integration needs.

## Case studies

- attack_agentcore_via_prompt_injection

## Key takeaways

- Scope allowed tools when the harness is invoked, per session, not when it is created; turn off built-in shell and file tools for sessions that do not need them.
- Give every identity-vault service account least privilege for its one downstream integration; a leaked credential is worth only what its scope allows.
- Watch outbound traffic from harness containers; any endpoint outside the integration list is evidence of an active injection, not configuration drift.
- After a suspected leak, rotate JWT signing keys and reset server session state.
