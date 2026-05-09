
from supabase import create_client, Client,PostgrestAPIError
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv()

def update_medication_schedule(medication_dict: dict, day: str, jwt: str):
    supabase_client = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )
    supabase_client.postgrest.headers.update({"Authorization": f"Bearer {jwt}"})

   
    for time_of_day, medications in medication_dict.items():
        
        for med_id in medications:
            try:
                response = (
                    supabase_client.table("users_medication")
                    .update({"time_of_day": time_of_day})\
                    .eq("medication_id", med_id)\
                    .eq("day", day)\
                    .execute()
                )
                print(f"Updated {med_id} to {time_of_day} for {day}.")
            
            except PostgrestAPIError as e:
                print(f"Database error for {med_id}: {e.message}")
            except Exception as e:
                print(f"Unexpected error for {med_id}: {e}")



