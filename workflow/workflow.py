from workflow.schedule2 import solve_med_schedule

from workflow.initialization import fetch_conflicts, get_supabase_client, fetch_med_details, fetch_med_list, fetch_active_ingredients

def fetch(day,jwt) -> dict:
    try:
        medication_list = fetch_med_list(day, jwt)
        medication_details = fetch_med_details(jwt, medication_list)
        active_ingredients = fetch_active_ingredients(medication_list)
        conflicts = fetch_conflicts(active_ingredients)
        return {
            "medication_details": medication_details,
            "conflicts": conflicts
        }
    except Exception as err:
        print(f"fetch() failed: {err}")
        raise

def formalize_meds(medication) -> dict:
    meds = {}
    for med in medication:
        meds[med['medication_id']] = int(med['total_dosage'] / med['dosage_per_time'])
    return meds

def formalize_conflicts(conflicts) -> dict:
    cons = {}
    for con in conflicts:
        cons[(con['medA'], con['medB'])]=2
    return cons

def create_schedule(meds, conflicts) -> dict | None:
    try:
        schedule = solve_med_schedule(meds, conflicts)
        print("Success")
        return schedule
    except Exception as e:
        print(e)
        return None



def pipeline(day, jwt):
    res = fetch(day,jwt)
    formalized_meds = formalize_meds(res['medication_details'])
    formalized_conflicts = {}
    if res['conflicts']:
        formalized_conflicts = formalize_conflicts(res['conflicts'])
    print(formalized_meds)
    print(formalized_conflicts)
    schedule = create_schedule(formalized_meds, formalized_conflicts)
    print(schedule)
    return schedule