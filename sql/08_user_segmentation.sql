;WITH user_activity_summary AS (
    SELECT
        u.user_id,
        u.plan_type,
        COUNT(DISTINCT s.session_id) AS total_sessions,
        COUNT(e.event_id) AS total_events,
        COALESCE(
            MAX(e.event_timestamp),
            CONVERT(DATETIME2(7), '20250101', 112)
        ) AS last_active_time
    FROM dbo.users AS u
    LEFT JOIN dbo.sessions AS s
        ON u.user_id = s.user_id
    LEFT JOIN dbo.events AS e
        ON u.user_id = e.user_id
        AND e.event_name <> 'signup_completed'
    GROUP BY
        u.user_id,
        u.plan_type
)
SELECT
    user_id,
    plan_type,
    total_sessions,
    total_events,
    CASE
        WHEN total_events >= 30 AND total_sessions >= 10 THEN 'Highly Engaged'
        WHEN total_events BETWEEN 10 AND 29 THEN 'Moderately Engaged'
        WHEN total_events BETWEEN 1 AND 9 THEN 'Low Engagement'
        ELSE 'Dormant'
    END AS engagement_segment
FROM user_activity_summary;
