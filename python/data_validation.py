import pandas as pd
import sys

def run_validations():
    print("Running FlowMetrics data validation pipeline...")
    
    users = pd.read_csv("data/raw/users.csv")
    sessions = pd.read_csv("data/raw/sessions.csv")
    events = pd.read_csv("data/raw/events.csv")
    subs = pd.read_csv("data/raw/subscriptions.csv")
    
    # 1. Uniqueness Checks
    assert users["user_id"].is_unique, "Validation Failure: user_id contains duplicates!"
    assert sessions["session_id"].is_unique, "Validation Failure: session_id contains duplicates!"
    assert events["event_id"].is_unique, "Validation Failure: event_id contains duplicates!"
    assert subs["subscription_id"].is_unique, "Validation Failure: subscription_id contains duplicates!"
    
    # 2. Referential Integrity
    assert sessions["user_id"].isin(users["user_id"]).all(), "FK Error: Orphaned user_id in sessions!"
    assert events["user_id"].isin(users["user_id"]).all(), "FK Error: Orphaned user_id in events!"
    assert events["session_id"].isin(sessions["session_id"]).all(), "FK Error: Orphaned session_id in events!"
    assert subs["user_id"].isin(users["user_id"]).all(), "FK Error: Orphaned user_id in subscriptions!"
    
    # 3. Temporal & Logic Consistency
    assert (sessions["session_duration_seconds"] >= 0).all(), "Logic Error: Negative session durations detected!"

    sessions["session_start"] = pd.to_datetime(sessions["session_start"], errors="raise")
    sessions["session_end"] = pd.to_datetime(sessions["session_end"], errors="raise")
    events["event_timestamp"] = pd.to_datetime(events["event_timestamp"], errors="raise")

    calculated_duration = (
        sessions["session_end"] - sessions["session_start"]
    ).dt.total_seconds()
    assert calculated_duration.equals(
        sessions["session_duration_seconds"].astype(float)
    ), "Logic Error: Session duration does not match session timestamps!"

    event_sessions = events.merge(
        sessions[["session_id", "session_start", "session_end"]],
        on="session_id",
        how="left",
        validate="many_to_one",
    )
    assert (
        event_sessions["event_timestamp"].ge(event_sessions["session_start"])
        & event_sessions["event_timestamp"].le(event_sessions["session_end"])
    ).all(), "Temporal Error: Event timestamp falls outside its session!"

    # Validate activation date >= signup date
    activated_users = users[users["is_activated"] == True].dropna(subset=["activation_date"])
    signup_dates = pd.to_datetime(activated_users["signup_date"])
    activation_dates = pd.to_datetime(activated_users["activation_date"])
    assert (activation_dates >= signup_dates).all(), "Temporal Error: Activation occurs prior to signup!"
    
    # Validate paid conversion date >= signup date
    paid_users = users[users["is_paid"] == True].dropna(subset=["paid_conversion_date"])
    assert (pd.to_datetime(paid_users["paid_conversion_date"]) >= pd.to_datetime(paid_users["signup_date"])).all(), "Temporal Error: Paid conversion occurs prior to signup!"
    
    print("All 11 data quality assertions passed successfully.")

if __name__ == "__main__":
    run_validations()