# FlowMetrics product insights and experiment proposals

**Audience:** Product and growth teams  
**Prepared:** November 2026  
**Data scope:** Synthetic demonstration dataset; 10,000 users with signup dates in 2025

## Executive summary

FlowMetrics uses generated data to demonstrate product analytics workflows. The dataset is not production telemetry and does not establish real customer behavior, business performance, or causal effects.

In the current CSV snapshot, 2,897 of 10,000 users are marked activated (28.97%), 605 are marked paid (6.05%), and active subscriptions total $27,275 in monthly revenue. Workspace, project, and task events are useful for illustrating onboarding analysis, but event counts alone do not prove why users stop or that a particular product change would improve outcomes.

The generator samples teammate invitations and paid conversion independently among users who complete a task. An observed relationship between invitations and paid status should therefore not be interpreted as evidence that inviting a teammate causes conversion.

## Current generated snapshot

| Measure | Current value |
|---|---:|
| Users | 10,000 |
| Sessions | 25,812 |
| Events | 53,635 |
| Active subscriptions | 605 |
| Activated users | 2,897 (28.97%) |
| Paid users | 605 (6.05%) |
| Active monthly recurring revenue | $27,275 |
| Users with a workspace-created event | 7,008 |
| Users with a project-created event | 3,858 |
| Users with a task-created event | 3,286 |
| Users with a teammate-invited event | 1,147 |

These are descriptive counts from the current generated files and may change when the data is regenerated. Event counts are distinct users per event name; they are not necessarily mutually exclusive or a sequential funnel. For example, `task_created` can also be generated in a later engagement session.

In the current snapshot, activation is highest in the `201-500` employee-size segment at 30.85%. Paid conversion is highest for Organic Search at 6.72%, followed by Direct at 6.59%. These subgroup differences are descriptive only and do not show that company size or acquisition channel caused the outcomes.

## What the generator models

The generator creates users with signup dates from January 1 through December 31, 2025. It samples onboarding actions with these conditional probabilities:

- Workspace creation: 70% of users.
- Project creation: 55% of users who created a workspace.
- Initial task creation: 75% of users who created a project.
- Activation: completion of workspace, project, and task creation within seven days of signup.
- Teammate invitation: sampled with 40% probability among users who completed a task, subject to the generated invitation date falling within the data window.
- Paid conversion: sampled independently with 22% probability among users who completed a task, subject to the conversion date falling within the data window.

These are simulation rules, not estimates of real-world rates. Because later engagement can also generate task events, the number of users with any `task_created` event is not the same as the number who completed the initial onboarding task.

## Experiment proposal 1: Guided project setup

**Question:** Does offering a guided project template help new users create their first project?

- **Hypothesis:** A relevant starter template and a clear next step may make it easier for new users to move from workspace creation to project creation.
- **Population:** Newly registered users who create a workspace and are eligible for the onboarding experience.
- **Control:** Current project-creation experience.
- **Variant:** Optional guided setup with a relevant template and a clear next action.
- **Randomization:** Assign at the user or workspace level, consistently across sessions.
- **Primary metric:** Share of eligible users who create their first project within a pre-defined period after workspace creation.
- **Guardrails:** Time to first project, onboarding abandonment, and support contacts, where instrumented.
- **Evaluation:** Establish the production baseline, observation window, minimum detectable effect, and sample size before launch. Do not use synthetic rates as the production baseline.

## Experiment proposal 2: Contextual teammate invitation

**Question:** Does a contextual invitation prompt increase valid invitations without disrupting task setup?

- **Hypothesis:** An optional prompt after a user's first task may make the invitation action easier to discover.
- **Population:** Users who create their first task and have not already sent a valid invitation.
- **Control:** Existing invitation entry point.
- **Variant:** Optional contextual invitation prompt after task creation.
- **Randomization:** Assign consistently at the workspace level if multiple users share a workspace; otherwise use the product's appropriate account unit.
- **Primary metric:** Share of eligible users who send at least one valid invitation within a pre-defined period.
- **Guardrails:** Task completion, invitation cancellation or rejection, user reports, and support contacts, where instrumented.
- **Evaluation:** Treat paid conversion and retention as secondary outcomes. The generator does not model invitations as causing either outcome; assess them with a properly designed production experiment.

## Measurement guidance

Before using these analyses to make product decisions:

1. Label generated results as synthetic in dashboards and reports.
2. Define each metric's event, numerator, denominator, eligibility rules, and observation window.
3. Distinguish the initial onboarding task from later `task_created` events.
4. Treat invitation and paid conversion as separate outcomes unless production event definitions and analysis support a specific sequence.
5. Account for incomplete follow-up: users signing up near the end of 2025 do not have a full 30- or 60-day observation window.
6. Pre-register experiment hypotheses, primary metrics, sample-size requirements, and guardrails before examining outcomes.
7. Report counts and uncertainty alongside rates; do not make causal claims from descriptive subgroup comparisons.
