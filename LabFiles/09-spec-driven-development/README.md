# Lab 09: Spec-Driven Development

## Overview
This lab demonstrates spec-driven development with GitHub Spec Kit. Use the stakeholder documents to generate the project constitution, specification, and implementation plan before writing code.

## MVP Scope
The project is a simple RSS/Atom feed reader focused on the smallest useful feature set:

- Add a feed subscription by URL
- Display the list of subscriptions in the UI

For the MVP:

- Subscriptions can be stored in memory only
- Feed validation is not required
- Feed fetching and item display are deferred to the next phase

## Stakeholder Documents

Use these documents as the source of truth for generating project artifacts:

- `StakeholderDocuments/ProjectGoals.md` - overall scope and MVP definition
- `StakeholderDocuments/AppFeatures.md` - feature priorities and phase breakdown
- `StakeholderDocuments/TechStack.md` - architecture and technology choices

## Spec Kit Workflow

GitHub Spec Kit uses the stakeholder documents to generate:

1. `constitution.md`
2. `spec.md`
3. `plan.md`

Start with the stakeholder docs, then generate the spec and plan before implementation.

## What "Done" Means

The MVP is complete when:

1. A user can add a feed URL
2. The UI shows the updated subscription list

No feed parsing, item loading, or persistence is required for the MVP.

## Next Phase
After the MVP works, the Extended-MVP can add:

- Manual feed refresh
- Feed item display
- Basic error handling

## Related Files

- `StakeholderDocuments/ProjectGoals.md`
- `StakeholderDocuments/AppFeatures.md`
- `StakeholderDocuments/TechStack.md`
