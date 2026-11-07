import uuid
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
np.random.seed(42)
random.seed(42)

NUM_USERS = 10000
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 12, 31)
DATE_SPAN_DAYS = (END_DATE - START_DATE).days

CHANNELS = ["Organic Search", "Direct", "Paid Search", "Social Media", "Referral", "Email Campaign"]
CHANNEL_WEIGHTS = [0.30, 0.20, 0.20, 0.15, 0.10, 0.05]
COMPANY_SIZES = ["1-10", "11-50", "51-200", "201-500", "500+"]
COMPANY_WEIGHTS = [0.45, 0.25, 0.15, 0.10, 0.05]
DEVICES = ["Desktop", "Mobile", "Tablet"]
DEVICE_WEIGHTS = [0.70, 0.25, 0.05]

# 1. Feature Metadata
features_data = [
    {"feature_id": 1, "feature_name": "Task Management", "feature_category": "Core Workflow", "launch_date": "2024-01-01", "is_core_feature": True},
    {"feature_id": 2, "feature_name": "Team Collaboration", "feature_category": "Communication", "launch_date": "2024-01-01", "is_core_feature": True},
    {"feature_id": 3, "feature_name": "Calendar", "feature_category": "Productivity", "launch_date": "2024-03-01", "is_core_feature": False},
    {"feature_id": 4, "feature_name": "Automation", "feature_category": "Advanced", "launch_date": "2024-06-01", "is_core_feature": False},
    {"feature_id": 5, "feature_name": "Analytics Reports", "feature_category": "Reporting", "launch_date": "2024-01-01", "is_core_feature": False},
    {"feature_id": 6, "feature_name": "File Sharing", "feature_category": "Collaboration", "launch_date": "2024-01-01", "is_core_feature": True}
]
df_features = pd.DataFrame(features_data)

# 2. Users, Sessions, Events, Subscriptions Generation
users = []
sessions = []
events = []
subscriptions = []

event_id_counter = 1
subscription_id_counter = 1

for u_id in range(1, NUM_USERS + 1):
    signup_offset = random.randint(0, DATE_SPAN_DAYS)
    signup_dt = START_DATE + timedelta(days=signup_offset, seconds=random.randint(0, 86399))
    signup_date = signup_dt.date()
    
    channel = np.random.choice(CHANNELS, p=CHANNEL_WEIGHTS)
    country = fake.country_code()
    comp_size = np.random.choice(COMPANY_SIZES, p=COMPANY_WEIGHTS)
    device = np.random.choice(DEVICES, p=DEVICE_WEIGHTS)
    
    # Onboarding Probabilities
    completed_workspace = random.random() < 0.70
    completed_project = completed_workspace and (random.random() < 0.55)
    completed_task = completed_project and (random.random() < 0.75)
    
    # Activation Rule: Workspace + Project + Task within 7 days
    is_activated = False
    activation_date = None
    
    # Session 1: Onboarding Session
    session_id_1 = str(uuid.uuid4())
    s1_duration = random.randint(300, 1800)
    s1_start = signup_dt
    s1_end = s1_start + timedelta(seconds=s1_duration)
    
    sessions.append({
        "session_id": session_id_1,
        "user_id": u_id,
        "session_start": s1_start,
        "session_end": s1_end,
        "session_duration_seconds": s1_duration,
        "device_type": device,
        "pages_viewed": random.randint(3, 8)
    })
    
    # Event: Signup Completed
    events.append({
        "event_id": event_id_counter,
        "user_id": u_id,
        "event_timestamp": s1_start,
        "event_name": "signup_completed",
        "session_id": session_id_1,
        "device_type": device,
        "page_name": "/signup"
    })
    event_id_counter += 1
    
    current_time = s1_start + timedelta(seconds=random.randint(30, 90))
    if completed_workspace:
        events.append({
            "event_id": event_id_counter,
            "user_id": u_id,
            "event_timestamp": current_time,
            "event_name": "workspace_created",
            "session_id": session_id_1,
            "device_type": device,
            "page_name": "/onboarding/workspace"
        })
        event_id_counter += 1
        
        if completed_project:
            current_time += timedelta(seconds=random.randint(60, 180))
            events.append({
                "event_id": event_id_counter,
                "user_id": u_id,
                "event_timestamp": current_time,
                "event_name": "project_created",
                "session_id": session_id_1,
                "device_type": device,
                "page_name": "/projects/new"
            })
            event_id_counter += 1
            
            if completed_task:
                current_time += timedelta(seconds=random.randint(60, 180))
                events.append({
                    "event_id": event_id_counter,
                    "user_id": u_id,
                    "event_timestamp": current_time,
                    "event_name": "task_created",
                    "session_id": session_id_1,
                    "device_type": device,
                    "page_name": "/tasks/board"
                })
                event_id_counter += 1
                
                if (current_time.date() - signup_date).days <= 7:
                    is_activated = True
                    activation_date = current_time.date()

    onboarding_duration = int((current_time - s1_start).total_seconds())
    if onboarding_duration > s1_duration:
        sessions[-1]["session_end"] = current_time
        sessions[-1]["session_duration_seconds"] = onboarding_duration

    # Downstream Feature Engagement & Retention Sessions
    invited_teammate = completed_task and (random.random() < 0.40)
    will_convert_paid = completed_task and (random.random() < 0.22) # Yields ~5% overall conversion
    
    # Determine retention profile
    max_days_forward = min(60, (END_DATE.date() - signup_date).days)
    if is_activated:
        retention_days = [d for d in [1, 2, 7, 14, 21, 30, 45, 60] if d <= max_days_forward and random.random() < 0.55]
    else:
        retention_days = [d for d in [1, 7] if d <= max_days_forward and random.random() < 0.15]
        
    for day in retention_days:
        s_date = signup_dt + timedelta(days=day, hours=random.randint(1, 10))
        dur = random.randint(120, 2400)
        s_id = str(uuid.uuid4())
        
        sessions.append({
            "session_id": s_id,
            "user_id": u_id,
            "session_start": s_date,
            "session_end": s_date + timedelta(seconds=dur),
            "session_duration_seconds": dur,
            "device_type": device,
            "pages_viewed": random.randint(2, 12)
        })
        
        # Core active event
        events.append({
            "event_id": event_id_counter,
            "user_id": u_id,
            "event_timestamp": s_date + timedelta(seconds=10),
            "event_name": "login",
            "session_id": s_id,
            "device_type": device,
            "page_name": "/dashboard"
        })
        event_id_counter += 1
        
        # Feature interactions
        possible_events = ["task_created", "calendar_viewed", "file_shared", "report_exported", "automation_created"]
        event_pick = random.choice(possible_events)
        events.append({
            "event_id": event_id_counter,
            "user_id": u_id,
            "event_timestamp": s_date + timedelta(seconds=random.randint(30, dur - 10)),
            "event_name": event_pick,
            "session_id": s_id,
            "device_type": device,
            "page_name": f"/{event_pick.split('_')[0]}"
        })
        event_id_counter += 1

    # Team invite event
    if invited_teammate:
        invite_time = signup_dt + timedelta(days=random.randint(1, 4), hours=3)
        if invite_time <= END_DATE:
            s_invite = str(uuid.uuid4())
            sessions.append({
                "session_id": s_invite,
                "user_id": u_id,
                "session_start": invite_time,
                "session_end": invite_time + timedelta(seconds=300),
                "session_duration_seconds": 300,
                "device_type": device,
                "pages_viewed": 3
            })
            events.append({
                "event_id": event_id_counter,
                "user_id": u_id,
                "event_timestamp": invite_time + timedelta(seconds=60),
                "event_name": "teammate_invited",
                "session_id": s_invite,
                "device_type": device,
                "page_name": "/settings/team"
            })
            event_id_counter += 1

    # Monetization
    is_paid = False
    paid_conversion_date = None
    plan_type = "Free"
    
    if will_convert_paid:
        conversion_day_offset = random.randint(3, 20)
        conv_date = signup_date + timedelta(days=conversion_day_offset)
        if conv_date <= END_DATE.date():
            is_paid = True
            paid_conversion_date = conv_date
            plan_type = np.random.choice(["Pro", "Enterprise"], p=[0.75, 0.25])
            monthly_mrr = 29.00 if plan_type == "Pro" else 99.00
            
            s_conv = str(uuid.uuid4())
            conv_timestamp = datetime.combine(conv_date, datetime.min.time()) + timedelta(hours=14)
            sessions.append({
                "session_id": s_conv,
                "user_id": u_id,
                "session_start": conv_timestamp,
                "session_end": conv_timestamp + timedelta(seconds=450),
                "session_duration_seconds": 450,
                "device_type": device,
                "pages_viewed": 4
            })
            events.append({
                "event_id": event_id_counter,
                "user_id": u_id,
                "event_timestamp": conv_timestamp + timedelta(seconds=120),
                "event_name": "subscription_started",
                "session_id": s_conv,
                "device_type": device,
                "page_name": "/billing/plans"
            })
            event_id_counter += 1
            
            subscriptions.append({
                "subscription_id": subscription_id_counter,
                "user_id": u_id,
                "plan_name": plan_type,
                "start_date": conv_date,
                "end_date": None,
                "monthly_revenue": monthly_mrr,
                "subscription_status": "Active"
            })
            subscription_id_counter += 1

    users.append({
        "user_id": u_id,
        "signup_date": signup_date,
        "acquisition_channel": channel,
        "country": country,
        "company_size": comp_size,
        "plan_type": plan_type,
        "device_type": device,
        "is_activated": is_activated,
        "activation_date": activation_date,
        "is_paid": is_paid,
        "paid_conversion_date": paid_conversion_date
    })

# Convert to DataFrames and Export
df_users = pd.DataFrame(users)
df_sessions = pd.DataFrame(sessions)
df_events = pd.DataFrame(events)
df_subscriptions = pd.DataFrame(subscriptions)

df_users.to_csv("data/raw/users.csv", index=False)
df_sessions.to_csv("data/raw/sessions.csv", index=False)
df_events.to_csv("data/raw/events.csv", index=False)
df_subscriptions.to_csv("data/raw/subscriptions.csv", index=False)
df_features.to_csv("data/raw/features.csv", index=False)

print(f"Data generation complete: {len(df_users)} users, {len(df_sessions)} sessions, {len(df_events)} events, {len(df_subscriptions)} subscriptions.")
