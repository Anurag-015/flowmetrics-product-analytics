---

### `reports/data_dictionary.md`

```markdown
# FlowMetrics Data Dictionary

## Overview

This document details the FlowMetrics entity-relationship model and schema specifications implemented in [`sql/schema.sql`](../sql/schema.sql)[cite: 26]. The database runs on Microsoft SQL Server using the `dbo` schema[cite: 26]. Source datasets are generated via `python/generate_data.py` into `data/raw/` and validated through `python/data_validation.py`[cite: 26].

### Current Dataset Snapshot

| Metric Entity | Count / Value |
| :--- | :--- |
| **Total Users** | 10,000[cite: 26] |
| **Total Recorded Sessions** | 25,812[cite: 26] |
| **Total Telemetry Events** | 53,635[cite: 26] |
| **Product Features Catalog** | 6[cite: 26] |
| **Active Subscriptions** | 605[cite: 26] |
| **Activation Rate** | 28.97%[cite: 26] |
| **Paid Conversion Rate** | 6.05%[cite: 26] |
| **Active Monthly Recurring Revenue** | $27,275.00 ($27.28K rounded)[cite: 26] |
| **Plan Revenue Concentration** | Enterprise: 50.45% \| Pro: 49.55%[cite: 26] |

---

## Tables Specification

### 1. `dbo.users`
Stores user profile information, acquisition metadata, and account conversion flags[cite: 26].

| Column | SQL Server Type | Nullable | Key / Constraint | Description |
|---|---|:---:|---|---|
| `user_id` | `BIGINT` | No | Primary Key | Unique identifier assigned to each user[cite: 26]. |
| `signup_date` | `DATE` | No | — | Date of user account creation[cite: 26]. |
| `acquisition_channel` | `VARCHAR(50)` | No | — | Inbound source: `Organic Search`, `Direct`, `Paid Search`, `Social Media`, `Referral`, or `Email Campaign`[cite: 26]. |
| `country` | `VARCHAR(100)` | No | — | ISO country code[cite: 26]. |
| `company_size` | `VARCHAR(50)` | No | — | Organizational tier: `1-10`, `11-50`, `51-200`, `201-500`, `500+`[cite: 26]. |
| `plan_type` | `VARCHAR(50)` | No | Default: `'Free'` | Subscription tier: `Free`, `Pro`, or `Enterprise`[cite: 26]. |
| `device_type` | `VARCHAR(50)` | No | — | Primary signup device: `Desktop`, `Mobile`, or `Tablet`[cite: 26]. |
| `is_activated` | `BIT` | No | Default: `0` | Flag (`1`/`0`) indicating user created Workspace, Project, and Task within 7 days[cite: 26]. |
| `activation_date` | `DATE` | Yes | — | Timestamp of completing qualifying activation sequence (`NULL` if unactivated)[cite: 26]. |
| `is_paid` | `BIT` | No | Default: `0` | Flag (`1`/`0`) indicating conversion to a paid subscription tier[cite: 26]. |
| `paid_conversion_date` | `DATE` | Yes | — | Date of conversion to Pro or Enterprise (`NULL` if Free)[cite: 26]. |

---

### 2. `dbo.sessions`
Logs user sessions including duration, device attribution, and pageview depth[cite: 26].

| Column | SQL Server Type | Nullable | Key / Constraint | Description |
|---|---|:---:|---|---|
| `session_id` | `VARCHAR(64)` | No | Primary Key | UUID identifying the unique user browsing session[cite: 26]. |
| `user_id` | `BIGINT` | No | FK to `dbo.users(user_id)` ON DELETE CASCADE | Associated user account[cite: 26]. |
| `session_start` | `DATETIME2(7)` | No | — | Session start timestamp[cite: 26]. |
| `session_end` | `DATETIME2(7)` | No | — | Session conclusion timestamp[cite: 26]. |
| `session_duration_seconds` | `INTEGER` | No | CHECK: `>= 0` | Total session duration in seconds[cite: 26]. |
| `device_type` | `VARCHAR(50)` | No | — | Client device used during the session[cite: 26]. |
| `pages_viewed` | `INTEGER` | No | CHECK: `>= 1` | Count of unique page requests during the session[cite: 26]. |

---

### 3. `dbo.events`
Atomic event stream capturing product usage, onboarding steps, and feature actions[cite: 26].

| Column | SQL Server Type | Nullable | Key / Constraint | Description |
|---|---|:---:|---|---|
| `event_id` | `BIGINT` | No | Primary Key | Sequential unique event log identifier[cite: 26]. |
| `user_id` | `BIGINT` | No | FK to `dbo.users(user_id)` | User who executed the action[cite: 26]. |
| `event_timestamp` | `DATETIME2(7)` | No | — | Precise timestamp of the event[cite: 26]. |
| `event_name` | `VARCHAR(100)` | No | — | Action name: `signup_completed`, `workspace_created`, `project_created`, `task_created`, `login`, `teammate_invited`, `calendar_viewed`, `file_shared`, `report_exported`, `automation_created`, `subscription_started`[cite: 26]. |
| `session_id` | `VARCHAR(64)` | No | FK to `dbo.sessions(session_id)` ON DELETE CASCADE | Session context during which event was fired[cite: 26]. |
| `device_type` | `VARCHAR(50)` | No | — | Device category logged with event[cite: 26]. |
| `page_name` | `VARCHAR(100)` | No | — | Application URL route where event occurred[cite: 26]. |

---

### 4. `dbo.features`
Catalog mapping of platform capabilities and strategic core feature designations[cite: 26].

| Column | SQL Server Type | Nullable | Key / Constraint | Description |
|---|---|:---:|---|---|
| `feature_id` | `INTEGER` | No | Primary Key | Integer identifier[cite: 26]. |
| `feature_name` | `VARCHAR(100)` | No | Unique | Feature label (e.g., Task Management, Calendar, Automation)[cite: 26]. |
| `feature_category` | `VARCHAR(100)` | No | — | Feature module: `Core Workflow`, `Communication`, `Productivity`, `Advanced`, `Reporting`, `Collaboration`[cite: 26]. |
| `launch_date` | `DATE` | No | — | Date module was made available in production[cite: 26]. |
| `is_core_feature` | `BIT` | No | — | Indicator whether feature is considered vital for baseline activation[cite: 26]. |

---

### 5. `dbo.subscriptions`
Records active customer billing contracts and recurring revenue[cite: 26].

| Column | SQL Server Type | Nullable | Key / Constraint | Description |
|---|---|:---:|---|---|
| `subscription_id` | `BIGINT` | No | Primary Key | Unique subscription contract identifier[cite: 26]. |
| `user_id` | `BIGINT` | No | FK to `dbo.users(user_id)` ON DELETE CASCADE | Subscribing user account[cite: 26]. |
| `plan_name` | `VARCHAR(50)` | No | — | Tier: `Pro` ($29.00/mo) or `Enterprise` ($99.00/mo)[cite: 26]. |
| `start_date` | `DATE` | No | — | Billing start date[cite: 26]. |
| `end_date` | `DATE` | Yes | — | Termination date (`NULL` for active subscriptions)[cite: 26]. |
| `monthly_revenue` | `DECIMAL(10, 2)` | No | Default: `0.00` | Normalized Monthly Recurring Revenue (MRR)[cite: 26]. |
| `subscription_status` | `VARCHAR(50)` | No | — | Status flag (`Active`)[cite: 26]. |