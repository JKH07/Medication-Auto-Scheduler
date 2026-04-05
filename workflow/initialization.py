
from supabase import create_client, Client,PostgrestAPIError
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv()

def get_supabase_client() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("Supabase credentials not found in environment variables.")
    return create_client(url, key)


#fetch medication from database
def fetch(jwt,user_id):
    
    supabase_client = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )
    supabase_client.postgrest.headers.update({"Authorization": f"Bearer {jwt}"})
    
    try:
        response = supabase_client.table("users_medication")\
            .select("*")\
            .eq("user_id", user_id)\
            .execute()
        
        print("Success!")
        print(f"Retrieved data")
        return response
    except PostgrestAPIError as e:
        print(f"API Error: {e}")
        print(f"Status code: {e.code if hasattr(e, 'code') else 'N/A'}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def send(jwt, data):
    
    supabase_client = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )
    supabase_client.postgrest.headers.update({"Authorization": f"Bearer {jwt}"})
    
    try:
        response = supabase_client.table("users_medication").insert(data).execute()
        print("Success!")
        print(f"Inserted data: {response.data}")
        return response
    except PostgrestAPIError as e:
        print(f"API Error: {e}")
        print(f"Status code: {e.code if hasattr(e, 'code') else 'N/A'}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def fetch_conflicts(med_id):
    supabase_client = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )
    supabase_client.postgrest.headers.update({"Authorization": f"Bearer {jwt}"})
    
    try:
        response = supabase_client.table("users_medication")\
            .select("*")\
            .eq("med_A", med_id)\
            .execute()
        
        print("Success!")
        print(f"Retrieved data")
        return response
    except PostgrestAPIError as e:
        print(f"API Error: {e}")
        print(f"Status code: {e.code if hasattr(e, 'code') else 'N/A'}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

#dont forget to make sure that not the same info is inputted twice
#A-B and B-A for ex
