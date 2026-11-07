USE FlowMetrics;


GO
-- Daily Active Users (DAU) & Rolling 30-Day MAU Stickiness
WITH     daily_active
AS       (SELECT   CAST (event_timestamp AS DATE) AS activity_date,
                   COUNT(DISTINCT user_id) AS dau
          FROM     dbo.events
          WHERE    event_name <> 'signup_completed'
          GROUP BY CAST (event_timestamp AS DATE))
SELECT   activity_date,
         dau,
         (SELECT COUNT(DISTINCT user_id)
          FROM   dbo.events AS e
          WHERE  e.event_name <> 'signup_completed'
                 AND CAST (e.event_timestamp AS DATE) BETWEEN DATEADD(day, -29, da.activity_date) AND da.activity_date) AS mau_rolling_30d,
         CAST (dau * 100.0 / NULLIF ((SELECT COUNT(DISTINCT user_id)
                                      FROM   dbo.events AS e
                                      WHERE  e.event_name <> 'signup_completed'
                                             AND CAST (e.event_timestamp AS DATE) BETWEEN DATEADD(day, -29, da.activity_date) AND da.activity_date), 0) AS DECIMAL (5, 2)) AS stickiness_ratio_pct
FROM     daily_active AS da
ORDER BY activity_date;