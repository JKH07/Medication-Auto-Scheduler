from supabase import create_client, Client, PostgrestAPIError
import os
from dotenv import load_dotenv

from save_to_data_base import update_medication_schedule
from initialization import fetch_conflicts,get_supabase_client,fetch_med_details,fetch_med_list,fetch_active_ingredients
from workflow import pipeline

load_dotenv()

supabase = get_supabase_client()

try: 
    data = supabase.auth.sign_in_with_password({
        "email": "yosrnajjar@gmail.com", 
        "password": "Teest_12345678"
    })
    print("Auth successful!")
except Exception as e:
    print(f"Auth failed: {e}")
    exit(1)

jwt = data.session.access_token
user_id = supabase.auth.get_user().user.id


pipeline("Monday",jwt)