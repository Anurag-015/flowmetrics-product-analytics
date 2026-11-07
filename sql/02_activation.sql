USE FlowMetrics;


GO
-- 7-Day Activation Rate by Channel & Company Size
SELECT   acquisition_channel,
         company_size,
         COUNT(user_id) AS total_users,
         SUM(CAST (is_activated AS INT)) AS activated_users,
         CAST (SUM(CAST (is_activated AS INT)) * 100.0 / COUNT(user_id) AS DECIMAL (5, 2)) AS activation_rate_pct,
         AVG(DATEDIFF(day, signup_date, activation_date)) AS avg_days_to_activate
FROM     dbo.users
GROUP BY acquisition_channel, company_size
ORDER BY activation_rate_pct DESC;