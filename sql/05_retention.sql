;WITH cohort_items AS (
    SELECT
        u.user_id,
        DATEADD(
            DAY,
            -(DATEDIFF(DAY, '19000101', u.signup_date) % 7),
            u.signup_date
        ) AS cohort_week
    FROM dbo.users AS u
),
user_activities AS (
    SELECT DISTINCT
        e.user_id,
        DATEDIFF(
            DAY,
            ci.cohort_week,
            CONVERT(DATE, e.event_timestamp)
        ) / 7 AS period_weeks
    FROM dbo.events AS e
    INNER JOIN cohort_items AS ci
        ON e.user_id = ci.user_id
    WHERE e.event_name <> 'signup_completed'
),
cohort_sizes AS (
    SELECT
        cohort_week,
        COUNT(user_id) AS total_users
    FROM cohort_items
    GROUP BY cohort_week
)
SELECT
    cs.cohort_week,
    cs.total_users,
    ROUND(
        COUNT(DISTINCT CASE WHEN ua.period_weeks = 0 THEN ua.user_id END)
            * 100.0 / cs.total_users,
        1
    ) AS week_0_pct,
    ROUND(
        COUNT(DISTINCT CASE WHEN ua.period_weeks = 1 THEN ua.user_id END)
            * 100.0 / cs.total_users,
        1
    ) AS week_1_pct,
    ROUND(
        COUNT(DISTINCT CASE WHEN ua.period_weeks = 2 THEN ua.user_id END)
            * 100.0 / cs.total_users,
        1
    ) AS week_2_pct,
    ROUND(
        COUNT(DISTINCT CASE WHEN ua.period_weeks = 3 THEN ua.user_id END)
            * 100.0 / cs.total_users,
        1
    ) AS week_3_pct,
    ROUND(
        COUNT(DISTINCT CASE WHEN ua.period_weeks = 4 THEN ua.user_id END)
            * 100.0 / cs.total_users,
        1
    ) AS week_4_pct
FROM cohort_sizes AS cs
LEFT JOIN cohort_items AS ci
    ON cs.cohort_week = ci.cohort_week
LEFT JOIN user_activities AS ua
    ON ci.user_id = ua.user_id
GROUP BY
    cs.cohort_week,
    cs.total_users
ORDER BY
    cs.cohort_week;
