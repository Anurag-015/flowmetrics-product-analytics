USE FlowMetrics;


GO
-- Feature Adoption Ranking & Plan Penetration
WITH     eligible_users
AS       (SELECT COUNT(DISTINCT user_id) AS active_user_pool
          FROM   dbo.events
          WHERE  event_name <> 'signup_completed'),
         feature_counts
AS       (SELECT   f.feature_name,
                   f.feature_category,
                   COUNT(e.event_id) AS total_interactions,
                   COUNT(DISTINCT e.user_id) AS unique_adopters
          FROM     dbo.features AS f
                   LEFT OUTER JOIN
                   dbo.events AS e
                   ON ((f.feature_name = 'Task Management'
                        AND e.event_name = 'task_created')
                       OR (f.feature_name = 'Team Collaboration'
                           AND e.event_name = 'teammate_invited')
                       OR (f.feature_name = 'Calendar'
                           AND e.event_name = 'calendar_viewed')
                       OR (f.feature_name = 'Automation'
                           AND e.event_name = 'automation_created')
                       OR (f.feature_name = 'Analytics Reports'
                           AND e.event_name = 'report_exported')
                       OR (f.feature_name = 'File Sharing'
                           AND e.event_name = 'file_shared'))
          GROUP BY f.feature_name, f.feature_category)
SELECT   fc.feature_name,
         fc.feature_category,
         fc.total_interactions,
         fc.unique_adopters,
         CAST (fc.unique_adopters * 100.0 / eu.active_user_pool AS DECIMAL (5, 2)) AS adoption_rate_pct,
         DENSE_RANK() OVER (ORDER BY fc.unique_adopters DESC) AS adoption_rank
FROM     feature_counts AS fc
         CROSS JOIN eligible_users AS eu
ORDER BY adoption_rank;