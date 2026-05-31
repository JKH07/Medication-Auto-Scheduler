
from supabase import create_client, Client,PostgrestAPIError
import os
from dotenv import load_dotenv
from datetime import date
from itertools import combinations

load_dotenv()

def get_supabase_client() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("Supabase credentials not found in environment variables.")
    return create_client(url, key)


#fetch medication from database
def fetch_med_details(jwt: str, med_list):
    supabase_client = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )
    supabase_client.postgrest.headers.update({"Authorization": f"Bearer {jwt}"})

    try:
        med_ids = [
            med['medication_id'] if isinstance(med, dict) else med
            for med in med_list
        ]

        med_details = supabase_client.table("users_medication")\
            .select("medication_id,total_dosage,dosage_per_time")\
            .in_("medication_id", med_ids)\
            .execute()

        print("Success!")
        print(f"Retrieved data: {med_details.data}")
        return med_details.data

    except PostgrestAPIError as e:
        print(f"API Error: {e}")
        print(f"Status code: {e.code if hasattr(e, 'code') else 'N/A'}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def fetch_med_list(day: str, jwt: str):
    supabase_client = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )
    supabase_client.postgrest.headers.update({"Authorization": f"Bearer {jwt}"})

    try:
        meds = supabase_client.table("Schedule")\
            .select("medication_id")\
            .eq("day", day)\
            .eq("status","pending")\
            .eq("time_of_the_day","none")\
            .execute()

        print("Success!")
        print(f"Retrieved data: {meds.data}")
        return meds.data

    except PostgrestAPIError as e:
        print(f"API Error: {e}")
        print(f"Status code: {e.code if hasattr(e, 'code') else 'N/A'}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def fetch_conflicts(active: list):
    supabase_client = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )
   
    try:
        results = []

        for med_a, med_b in combinations(active, 2):
            # Check both (A,B) and (B,A) since storage order is unknown
            response = (
                supabase_client.table("med_interactions")
                .select("medA, medB, severity")
                .or_(
                    f"and(medA.eq.{med_a},medB.eq.{med_b}),"
                    f"and(medA.eq.{med_b},medB.eq.{med_a})"
                )
                .execute()
            )

            if response.data:
                results.extend(response.data)

        print(f"Success! Found {len(results)} interaction(s).")
        return results

    except PostgrestAPIError as e:
        print(f"API Error: {e} | Code: {getattr(e, 'code', 'N/A')}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def fetch_active_ingredients( med_list):
    supabase_client = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )
    
    try:
        med_ids = [
            med['medication_id'] if isinstance(med, dict) else med
            for med in med_list
        ]

        active_ingredients = supabase_client.table("medication_active")\
            .select("active_ingredient,med_id")\
            .in_("med_id", med_ids)\
            .execute()

        print("Success!")
        print(f"Retrieved data: {active_ingredients.data}")
        return active_ingredients.data

    except PostgrestAPIError as e:
        print(f"API Error: {e}")
        print(f"Status code: {e.code if hasattr(e, 'code') else 'N/A'}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None