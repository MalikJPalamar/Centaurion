# GoHighLevel Playbook

## Overview

GoHighLevel (GHL) is BuilderBee's primary implementation platform. This playbook captures patterns, best practices, and templates for GHL deployments across clients.

## Core GHL Components

| Component | Use Case |
|-----------|----------|
| CRM & Contacts | Client contact management and segmentation |
| Workflows | Automated sequences triggered by events |
| Funnels | Landing pages and conversion flows |
| Calendars | Booking and scheduling |
| Reputation Management | Review solicitation and monitoring |
| Conversations | Unified inbox across channels |

## Implementation Patterns

### Standard Client Setup

1. **Sub-account creation** — One sub-account per client in GHL agency model
2. **Pipeline configuration** — Sales pipeline matching client's sales process
3. **Workflow templates** — Deploy proven automation workflows
4. **Integration setup** — Connect client's existing tools (Stripe, Calendly, etc.)
5. **Training session** — Walk client through their specific setup

### Common Workflows

- **Lead nurture:** New lead → email sequence → SMS follow-up → task for sales
- **Appointment reminder:** Booking → confirmation → 24h reminder → 1h reminder
- **Review request:** Service completed → delay → review request → follow-up if no response
- **Re-engagement:** No activity 30 days → re-engagement sequence

## Lessons Learned

- Always start with the client's existing process before optimizing
- Test workflows with dummy data before going live
- Document every workflow so clients can self-serve on modifications
- Use snapshots to deploy proven templates quickly across new clients

## Related

- [Service Offerings](service-offerings.md) — How GHL work fits into BuilderBee packages
- [Client Onboarding](client-onboarding.md) — When GHL setup happens in the client journey
