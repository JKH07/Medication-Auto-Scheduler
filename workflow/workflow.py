from initialization import fetch,get_supabase_client
from schedule2 import solve_med_schedule
from save_to_data_base import update_medication_schedule

def workflow(day,jwt):
    data=fetch_data(jwt,day)
    formalized=formalize(data)
    meds=formalized['meds']
    conflicts=formalized['conflicts']
    schedule=create_schedule(meds,conflicts)
    set_timings(schedule,day,jwt)
    return 


#fetching data based on user id
def fetch_data(jwt,user_id):
    try:
        response=fetch(jwt,user_id)
        return response
    except Exception as err:
        print(err)

#update format to suit google or tools
def formalize(data)->dict:
    formalized={
        'meds':[],
        'conflicts':[]
    }
    return formalized
#start cearting the schedule
#schedule will be processed day by day
def create_schedule(meds,conflicts)-> dict | None:
    schedule=solve_med_schedule(meds,conflicts)
    return schedule

#edit database medication timings
def set_timings(data:dict,day:str,jwt):
    try:
        update_medication_schedule(data,day,jwt)
    except e:
        print(e)
    return None
#end: frontend will get these timings from the database and display the schedule