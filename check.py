
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
def fetch_try():
    response={}
    supabase_client = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )
    #supabase_client.postgrest.headers.update({"Authorization": f"Bearer {jwt}"})
    
    try:
        #get medication list from database
        # Perform a join to get the name from the related table
        # response = supabase_client.table("medication") \
        #     .select("active_ingredient_id") \
        #     .execute()
        # print(response.data)
        
        # for med in response.data:
        #     ingredient = med['active_ingredient_id']
        #     name = supabase_client.table("active_ingredients")\
        #     .select("name")\
        #     .eq("id",ingredient)\
        #     .execute()

        meds=["Spironolactone","Digoxin","Warfarin","Metolazone","Potassium Chloride","Metformin","Jardiance","Aspirin"]
        
        for med in meds:
            response = supabase_client.table("active_ingredients") \
            .select("id,name") \
            .eq("name",med)\
            .execute()
            
        
        for id in response.data:
             idd=id['id']
             name=id['name']
             supabase_client.table('medication')\
             .insert(
                     {'active_ingredient_id':idd,
                     'name':name})\
             .execute()
        
        print("Success!")
        
        return response
    except PostgrestAPIError as e:
        print(f"API Error: {e}")
        print(f"Status code: {e.code if hasattr(e, 'code') else 'N/A'}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    
fetch_try()