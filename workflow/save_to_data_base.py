
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

def insert_medication(data: dict):
    supabase = get_supabase_client()
    
    try:
        response = supabase.table("medication").insert(data).execute()
        
        print("Data sent successfully.")
        return response

    except PostgrestAPIError as e:
        print(f"Database API error: {e.message}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")