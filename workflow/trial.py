from supabase import create_client, Client, PostgrestAPIError
import os
from dotenv import load_dotenv
from initialization import send,fetch,get_supabase_client

load_dotenv()

supabase = get_supabase_client()

try: 
    data = supabase.auth.sign_in_with_password({
        "email": "test@mail.com", 
        "password": "123"
    })
    print("Auth successful!")
except Exception as e:
    print(f"Auth failed: {e}")
    exit(1)

jwt = data.session.access_token
user_id = supabase.auth.get_user().user.id

# data={
#     "user_id":user_id,
#     "medication_id":"afdd7099-c475-458e-8629-84862be9af4f"
# }
# #result1=send(jwt,data)

result = fetch(jwt,user_id)
