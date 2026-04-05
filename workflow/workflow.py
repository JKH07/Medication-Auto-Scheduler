from initialization import fetch,get_supabase_client
def workflow():
    return 


#fetching data based on user id
def fetch_data(jwt,user_id):
    try:
        response=fetch(jwt,user_id)
        return response
    except Exception as err:
        print(err)

#update format to suit google or tools
def formalize():
    return
#set and check rules
def set_rules():
    return
#start cearting the schedule
#schedule will be processed day by day
def create_schedule():
    return
#finalize schedule format , place the outputted days as a week
def finalize():
    return
#edit database medication timings
def set_timings():
    return
#end: frontend will get these timings from the database and display the schedule