from ortools.sat.python import cp_model

def solve_complex_med_system():
    model = cp_model.CpModel()
    
    med_requirements = {
        "Aspirin": 1,          
        "Metoprolol": 2,      
        "Lisinopril": 1,      
        "Atorvastatin": 1,    
        "Furosemide": 2,       
        "Clopidogrel": 1,     
        "Amlodipine": 1,      
        "Isosorbide": 2,      
        "Warfarin": 1,         
        "Digoxin": 1,        
        "Spironolactone": 1,  
        "Potassium_Sup": 1     
    }
  
    
    drug_conflicts = {
            ("Metoprolol", "Amlodipine"): 2, 
            ("Furosemide", "Lisinopril"): 2, 
            ("Warfarin", "Aspirin"): 3,       
            ("Isosorbide", "Amlodipine"): 2,  
            ("Digoxin", "Spironolactone"): 2, 
            ("Metoprolol", "Isosorbide"): 2,  
            ("Furosemide", "Potassium_Sup"): 0,
    }
    # parameters
    same_med_lag = 2        # 2 brackets = 8hours
    num_brackets = 6        # 6 brackets = 4 hours
    brackets = ["6AM-10AM", "10AM-2PM", "2PM-6PM", "6PM-10PM", "10PM-2AM", "2AM-6AM"]
    
    # Daytime brackets 
    daytime_limit = 3       #  0-3 =daytime
    
    # variables
    all_doses = {}
    for med_name, num_doses in med_requirements.items():
        for d in range(num_doses):
            all_doses[(med_name, d)] = model.NewIntVar(0, num_brackets - 1, f'{med_name}_d{d}')
    
    # constraints
    all_slacks = []
    
    # spacing Same-Medication 
    for med_name, num_doses in med_requirements.items():
        for d in range(num_doses - 1):
            model.Add(all_doses[(med_name, d+1)] >= all_doses[(med_name, d)] + same_med_lag)
    
    #  Drug-Drug Conflict 
    for (m1, m2), lag in drug_conflicts.items():
        if m1 in med_requirements and m2 in med_requirements:
            for d1 in range(med_requirements[m1]):
                for d2 in range(med_requirements[m2]):
                   
                    diff = model.NewIntVar(0, num_brackets, f'diff_{m1}_{m2}_{d1}_{d2}')
                    
                    # Absolute value
                    model.Add(diff >= all_doses[(m1, d1)] - all_doses[(m2, d2)])
                    model.Add(diff >= all_doses[(m2, d2)] - all_doses[(m1, d1)])
                    
                    
                    slack = model.NewIntVar(0, num_brackets, f'slack_{m1}_{m2}_{d1}_{d2}')
                    all_slacks.append(slack)
                    model.Add(diff + slack >= lag)
    
    # objective function
    
    is_daytime_vars = []
    for dose_var in all_doses.values():
        is_daytime = model.NewBoolVar('is_daytime')
        model.Add(dose_var <= daytime_limit).OnlyEnforceIf(is_daytime)
        model.Add(dose_var > daytime_limit).OnlyEnforceIf(is_daytime.Not())
        is_daytime_vars.append(is_daytime)
    

    model.Maximize(sum(is_daytime_vars) * 10 - sum(all_slacks))
    
    #solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    # output
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    
        schedule = {i: [] for i in range(num_brackets)}
        for (med_name, dose_idx), var in all_doses.items():
            bracket_value = solver.Value(var)
            dose_label = f"{med_name}"
            if med_requirements[med_name] > 1:
                dose_label = f"{med_name}({dose_idx+1})"
            schedule[bracket_value].append(dose_label)
        
        # Print formatted schedule
      
        print("MEDICATION SCHEDULE")
        print("=" * 60)
        print(f"{'TIME BRACKET':<20} | MEDICATIONS")
        print("-" * 60)
        
        for bracket_idx in range(num_brackets):
            meds_in_slot = ", ".join(schedule[bracket_idx]) if schedule[bracket_idx] else "--"
            
            if bracket_idx > daytime_limit:
                meds_in_slot = f"[NIGHT] {meds_in_slot}"
            print(f"{brackets[bracket_idx]:<20} | {meds_in_slot}")
        
        # Print statistics
        print("-" * 60)
        
        # Daytime dose count
        daytime_doses = 0
        for var in is_daytime_vars:
            if solver.Value(var) == 1:
                daytime_doses += 1
        total_doses = len(all_doses)
        
        print(f"\n STATISTICS:")
        print(f"   Total doses: {total_doses}")
        print(f"   Daytime doses (before 10PM): {daytime_doses}")
        print(f"   Nighttime doses (after 10PM): {total_doses - daytime_doses}")
        
        # Conflict report
        violations = [slack for slack in all_slacks if solver.Value(slack) > 0]
        if violations:
            print(f" Conflicts: {len(violations)} drug pairs had spacing violations (slack > 0)")
        else:
            print(f" Conflicts: None - all spacing requirements satisfied")
        
        # Objective value
        print(f"   Objective value: {solver.ObjectiveValue():.2f}")
        
    else:
        print("\n MODEL FAILED TO FIND A SOLUTION")
        print(f"   Status: {solver.StatusName(status)}")
        print("\n   Possible reasons:")
        print("   - Constraints are too tight (try increasing same_med_lag or num_brackets)")
        print("   - Too many medications requiring specific spacing")
        print("   - Conflicting requirements between drugs")
    
    return solver, status, all_doses, schedule if status in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None


# --- 8. RUN THE SOLVER ---
if __name__ == "__main__":
    solve_complex_med_system()