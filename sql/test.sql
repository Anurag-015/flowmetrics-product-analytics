USE FlowMetrics;


GO
-- 1. Table Counts Check
SELECT 'users' AS table_name,
       COUNT(*) AS row_count
FROM   dbo.users
UNION ALL
SELECT 'sessions',
       COUNT(*)
FROM   dbo.sessions
UNION ALL
SELECT 'events',
       COUNT(*)
FROM   dbo.events
UNION ALL
SELECT 'features',
       COUNT(*)
FROM   dbo.features
UNION ALL
SELECT 'subscriptions',
       COUNT(*)
FROM   dbo.subscriptions;

-- 2. Core KPIs Reconciliation Check
SELECT COUNT(*) AS total_signups,
       SUM(CAST (is_activated AS INT)) AS activated_users,
       CAST (SUM(CAST (is_activated AS INT)) * 100.0 / COUNT(*) AS DECIMAL (5, 2)) AS activation_rate_pct,
       SUM(CAST (is_paid AS INT)) AS paid_users,
       CAST (SUM(CAST (is_paid AS INT)) * 100.0 / COUNT(*) AS DECIMAL (5, 2)) AS paid_conversion_rate_pct
FROM   dbo.users;