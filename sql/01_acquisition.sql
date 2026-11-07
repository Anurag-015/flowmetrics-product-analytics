USE FlowMetrics;


GO
SELECT   acquisition_channel,
         COUNT(user_id) AS total_users,
         SUM(CAST (is_activated AS INT)) AS activated_users,
         CAST (SUM(CAST (is_activated AS INT)) * 100.0 / COUNT(user_id) AS DECIMAL (5, 2)) AS activation_rate_pct,
         SUM(CAST (is_paid AS INT)) AS paid_users,
         CAST (SUM(CAST (is_paid AS INT)) * 100.0 / COUNT(user_id) AS DECIMAL (5, 2)) AS conversion_rate_pct
FROM     dbo.users
GROUP BY acquisition_channel
ORDER BY paid_users DESC;