USE FlowMetrics;


GO
SELECT   plan_name,
         COUNT(subscription_id) AS active_subscriptions,
         SUM(monthly_revenue) AS total_mrr,
         CAST (AVG(monthly_revenue) AS DECIMAL (10, 2)) AS arpu
FROM     dbo.subscriptions
WHERE    subscription_status = 'Active'
GROUP BY plan_name
ORDER BY total_mrr DESC;