from supabase import create_client, Client, PostgrestAPIError
import os
from dotenv import load_dotenv

from save_to_data_base import update_medication_schedule
from initialization import fetch_conflicts,get_supabase_client,fetch_med_details

load_dotenv()

supabase = get_supabase_client()

try: 
    data = supabase.auth.sign_in_with_password({
        "email": "test2@gmail.com", 
        "password": "123"
    })
    print("Auth successful!")
except Exception as e:
    print(f"Auth failed: {e}")
    exit(1)

jwt = data.session.access_token
user_id = supabase.auth.get_user().user.id

schedule= {'Morning': ['Aspirin', 'Metoprolol(1)', 'Furosemide(1)', 'Isosorbide(1)'], 
           'Night': ['Metoprolol(2)', 'Lisinopril'], 
           'Evening': ['Atorvastatin', 'Clopidogrel', 'Isosorbide(2)', 'Warfarin', 'Digoxin', 'Spironolactone', 'Potassium_Sup'], 
           'Afternoon': ['Furosemide(2)', 'Amlodipine']}

#result = fetch(jwt,user_id)

#result2=update_medication_schedule(schedule,"Monday",jwt)

meds={"DDInter1","DDInter1348"}

#res=fetch_conflicts(meds,jwt)
res=fetch_med_details(meds,jwt)
print(res)