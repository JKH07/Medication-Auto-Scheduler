
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
def fetch_med_list(jwt:str,day:str):
    
    supabase_client = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )
    supabase_client.postgrest.headers.update({"Authorization": f"Bearer {jwt}"})
    
    try:
        #get medication list from database
        med_ids = supabase_client.table("users_medication")\
            .select("medication_id,dosage")\
            .eq("day",day)\
            .execute()
        
        print("Success!")
        print(f"Retrieved data:{med_ids}")
        return med_ids
    except PostgrestAPIError as e:
        print(f"API Error: {e}")
        print(f"Status code: {e.code if hasattr(e, 'code') else 'N/A'}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def fetch_med_details(med_ids:dict,jwt:str):
    #using the medication table get the active ingredients 
    meds=med_ids[0]['id']
    supabase_client = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )
    supabase_client.postgrest.headers.update({"Authorization": f"Bearer {jwt}"})
    
    try:
        #get
        active = supabase_client.table("medication")\
            .select("active_ingredient,id")\
            .eq("id",meds)\
            .execute()
        
        print("Success!")
        print(f"Retrieved data:{med_ids}")
        return active
    except PostgrestAPIError as e:
        print(f"API Error: {e}")
        print(f"Status code: {e.code if hasattr(e, 'code') else 'N/A'}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    

    return


def fetch_conflicts(active: list, jwt: str):
    supabase_client = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )
    supabase_client.postgrest.headers.update({"Authorization": f"Bearer {jwt}"})

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


