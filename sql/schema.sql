IF OBJECT_ID('dbo.subscriptions', 'U') IS NOT NULL DROP TABLE dbo.subscriptions;
IF OBJECT_ID('dbo.events', 'U') IS NOT NULL DROP TABLE dbo.events;
IF OBJECT_ID('dbo.sessions', 'U') IS NOT NULL DROP TABLE dbo.sessions;
IF OBJECT_ID('dbo.features', 'U') IS NOT NULL DROP TABLE dbo.features;
IF OBJECT_ID('dbo.users', 'U') IS NOT NULL DROP TABLE dbo.users;

CREATE TABLE dbo.users (
    user_id BIGINT PRIMARY KEY,
    signup_date DATE NOT NULL,
    acquisition_channel VARCHAR(50) NOT NULL,
    country VARCHAR(100) NOT NULL,
    company_size VARCHAR(50) NOT NULL,
    plan_type VARCHAR(50) NOT NULL DEFAULT 'Free',
    device_type VARCHAR(50) NOT NULL,
    is_activated BIT NOT NULL DEFAULT 0,
    activation_date DATE NULL,
    is_paid BIT NOT NULL DEFAULT 0,
    paid_conversion_date DATE NULL
);

CREATE TABLE dbo.sessions (
    session_id VARCHAR(64) PRIMARY KEY,
    user_id BIGINT NOT NULL FOREIGN KEY REFERENCES dbo.users(user_id) ON DELETE CASCADE,
    session_start DATETIME2 NOT NULL,
    session_end DATETIME2 NOT NULL,
    session_duration_seconds INT NOT NULL CHECK (session_duration_seconds >= 0),
    device_type VARCHAR(50) NOT NULL,
    pages_viewed INT NOT NULL CHECK (pages_viewed >= 1)
);

CREATE TABLE dbo.features (
    feature_id INT PRIMARY KEY,
    feature_name VARCHAR(100) NOT NULL UNIQUE,
    feature_category VARCHAR(100) NOT NULL,
    launch_date DATE NOT NULL,
    is_core_feature BIT NOT NULL
);

-- Note: session_id FK uses default NO ACTION to eliminate multiple cascade paths
CREATE TABLE dbo.events (
    event_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL FOREIGN KEY REFERENCES dbo.users(user_id) ON DELETE CASCADE,
    event_timestamp DATETIME2 NOT NULL,
    event_name VARCHAR(100) NOT NULL,
    session_id VARCHAR(64) NOT NULL FOREIGN KEY REFERENCES dbo.sessions(session_id),
    device_type VARCHAR(50) NOT NULL,
    page_name VARCHAR(100) NOT NULL
);

CREATE TABLE dbo.subscriptions (
    subscription_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL FOREIGN KEY REFERENCES dbo.users(user_id) ON DELETE CASCADE,
    plan_name VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NULL,
    monthly_revenue DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    subscription_status VARCHAR(50) NOT NULL
);

CREATE NONCLUSTERED INDEX idx_users_signup ON dbo.users(signup_date);
CREATE NONCLUSTERED INDEX idx_users_channel ON dbo.users(acquisition_channel);
CREATE NONCLUSTERED INDEX idx_events_user_time ON dbo.events(user_id, event_timestamp);
CREATE NONCLUSTERED INDEX idx_events_name ON dbo.events(event_name);
CREATE NONCLUSTERED INDEX idx_sessions_user_start ON dbo.sessions(user_id, session_start);
CREATE NONCLUSTERED INDEX idx_subscriptions_user ON dbo.subscriptions(user_id);
