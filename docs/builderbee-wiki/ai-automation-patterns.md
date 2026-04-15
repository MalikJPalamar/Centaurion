# AI Automation Patterns

## Overview

Reusable automation patterns that BuilderBee deploys across clients. Each pattern is a proven template that can be adapted to specific business contexts.

## Pattern Library

### Lead Response Automation
- **Trigger:** New lead from any source (form, ad, referral)
- **Action:** Immediate acknowledgment, qualify via AI chatbot, route to appropriate pipeline stage
- **Value:** Sub-60-second response time, 24/7 availability
- **Tools:** GHL workflows, AI chatbot, SMS/email

### Appointment Scheduling
- **Trigger:** Qualified lead ready for consultation
- **Action:** Offer calendar link, send reminders, handle reschedules, follow up on no-shows
- **Value:** Eliminates scheduling back-and-forth, reduces no-show rate
- **Tools:** GHL calendar, automated reminders, SMS

### Review Generation
- **Trigger:** Service completion or positive interaction
- **Action:** Timed review request, platform-specific link, follow-up sequence
- **Value:** Consistent review volume, improved online reputation
- **Tools:** GHL reputation management, email/SMS workflows

### Client Re-engagement
- **Trigger:** No activity for configurable period (default 30 days)
- **Action:** Personalized re-engagement sequence, offer or check-in, escalate if no response
- **Value:** Recover dormant clients, identify churn risk early
- **Tools:** GHL workflows, segmentation, email/SMS

### AI-Powered Intake
- **Trigger:** New inquiry or form submission
- **Action:** AI chatbot gathers requirements, qualifies opportunity, creates structured summary
- **Value:** Consistent intake quality, immediate response, reduced manual data entry
- **Tools:** AI chatbot, GHL custom fields, workflow automation

## Pattern Development Process

1. Build for one client's specific need
2. Abstract into reusable template
3. Document triggers, actions, and configuration points
4. Add to snapshot library for rapid deployment
5. Track performance across deployments to refine

## Centaurion Integration

Centaurion tracks which patterns are deployed where, monitors their performance, and surfaces optimization opportunities. Cross-client pattern performance feeds back into the library.

## Related

- [GHL Playbook](ghl-playbook.md) — Platform-specific implementation details
- [Service Offerings](service-offerings.md) — Which packages include which patterns
