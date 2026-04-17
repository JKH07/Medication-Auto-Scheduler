

medication_data=[
    [("user/time_bracket","lag time"),(),()], #dosage 1
    [], #dosage 2
    [] #number of dosages= number of sets
]

time_bracket_count=6; 
all_time-brackets=["morning 6-11"," noon 11-3"," afternoon 3-7",
"evening 7-11","midnight 12-3","aftermidnight 3-6"]

#worst ossible solution is decreasing comfort levels to 0 or below
# comfort levels are determined by prefernces like 
# stratetgy:
#minimize pill windows while adhering to safety constraints