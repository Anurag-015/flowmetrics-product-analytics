USE FlowMetrics;


GO
WITH   user_funnel_flags
AS     (SELECT   u.user_id,
                 MAX(CASE WHEN e.event_name = 'signup_completed' THEN 1 ELSE 0 END) AS step_1_signup,
                 MAX(CASE WHEN e.event_name = 'workspace_created' THEN 1 ELSE 0 END) AS step_2_workspace,
                 MAX(CASE WHEN e.event_name = 'project_created' THEN 1 ELSE 0 END) AS step_3_project,
                 MAX(CASE WHEN e.event_name = 'task_created' THEN 1 ELSE 0 END) AS step_4_task,
                 MAX(CASE WHEN e.event_name = 'teammate_invited' THEN 1 ELSE 0 END) AS step_5_invite,
                 MAX(CASE WHEN u.is_paid = 1 THEN 1 ELSE 0 END) AS step_6_paid
        FROM     dbo.users AS u
                 LEFT OUTER JOIN
                 dbo.events AS e
                 ON u.user_id = e.user_id
        GROUP BY u.user_id),
       stage_aggregates
AS     (SELECT COUNT(*) AS total_signups,
               SUM(CASE WHEN step_1_signup = 1
                             AND step_2_workspace = 1 THEN 1 ELSE 0 END) AS s2_workspace,
               SUM(CASE WHEN step_1_signup = 1
                             AND step_2_workspace = 1
                             AND step_3_project = 1 THEN 1 ELSE 0 END) AS s3_project,
               SUM(CASE WHEN step_1_signup = 1
                             AND step_2_workspace = 1
                             AND step_3_project = 1
                             AND step_4_task = 1 THEN 1 ELSE 0 END) AS s4_task,
               SUM(CASE WHEN step_1_signup = 1
                             AND step_2_workspace = 1
                             AND step_3_project = 1
                             AND step_4_task = 1
                             AND step_5_invite = 1 THEN 1 ELSE 0 END) AS s5_invite,
               SUM(CASE WHEN step_1_signup = 1
                             AND step_2_workspace = 1
                             AND step_3_project = 1
                             AND step_4_task = 1
                             AND step_5_invite = 1
                             AND step_6_paid = 1 THEN 1 ELSE 0 END) AS s6_paid
        FROM   user_funnel_flags)
SELECT '1. Signup Completed' AS funnel_stage,
       total_signups AS user_count,
       100.0 AS stage_conversion_pct,
       0.0 AS stage_dropoff_pct
FROM   stage_aggregates
UNION ALL
SELECT '2. Workspace Created',
       s2_workspace,
       CAST (s2_workspace * 100.0 / total_signups AS DECIMAL (5, 2)),
       CAST ((total_signups - s2_workspace) * 100.0 / total_signups AS DECIMAL (5, 2))
FROM   stage_aggregates
UNION ALL
SELECT '3. Project Created',
       s3_project,
       CAST (s3_project * 100.0 / s2_workspace AS DECIMAL (5, 2)),
       CAST ((s2_workspace - s3_project) * 100.0 / s2_workspace AS DECIMAL (5, 2))
FROM   stage_aggregates
UNION ALL
SELECT '4. Task Created',
       s4_task,
       CAST (s4_task * 100.0 / s3_project AS DECIMAL (5, 2)),
       CAST ((s3_project - s4_task) * 100.0 / s3_project AS DECIMAL (5, 2))
FROM   stage_aggregates
UNION ALL
SELECT '5. Teammate Invited',
       s5_invite,
       CAST (s5_invite * 100.0 / s4_task AS DECIMAL (5, 2)),
       CAST ((s4_task - s5_invite) * 100.0 / s4_task AS DECIMAL (5, 2))
FROM   stage_aggregates
UNION ALL
SELECT '6. Paid Subscribed',
       s6_paid,
       CAST (s6_paid * 100.0 / s5_invite AS DECIMAL (5, 2)),
       CAST ((s5_invite - s6_paid) * 100.0 / s5_invite AS DECIMAL (5, 2))
FROM   stage_aggregates;