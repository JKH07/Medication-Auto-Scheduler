
from supabase import create_client, Client,PostgrestAPIError
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv()
import jwt as pyjwt

def update_medication_schedule(schedule, day: str, jwt: str):
    supabase_client = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )
    supabase_client.postgrest.headers.update({"Authorization": f"Bearer {jwt}"})

    # extract user_id from jwt
    decoded = pyjwt.decode(jwt, options={"verify_signature": False})
    user_id = decoded['sub']

    # group timings by med_id
    med_timings = {}
    for med_label, time_of_day in schedule.items():
        med_id = med_label.rsplit('_', 1)[0]
        if med_id not in med_timings:
            med_timings[med_id] = []
        med_timings[med_id].append(time_of_day)

    for med_id, timings in med_timings.items():
        try:
            # delete existing rows for this med and day
            supabase_client.table("Schedule")\
                .delete()\
                .eq("medication_id", med_id)\
                .eq("user_id", user_id)\
                .eq("day", day)\
                .execute()

            # insert one row per timing
            rows = [
                {
                    "medication_id": med_id,
                    "user_id": user_id,
                    "day": day,
                    "time_of_the_day": time
                }
                for time in timings
            ]
            supabase_client.table("Schedule")\
                .insert(rows)\
                .execute()

            print(f"Updated {med_id} with timings {timings} for {day}.")

        except PostgrestAPIError as e:
            print(f"Database error for {med_id}: {e.message}")
        except Exception as e:
            print(f"Unexpected error for {med_id}: {e}")