from ortools.sat.python import cp_model
import random

def solve_complex_med_system():
    model = cp_model.CpModel()
    
    # data setup
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
            ("Metoprolol", "Amlodipine"): 1, 
            ("Furosemide", "Lisinopril"):1, 
            ("Warfarin", "Aspirin"): 1,       
    }

    same_med_lag = 2
    num_brackets = 6

    # Variables
    all_doses = {}
    for med_name, num_doses in med_requirements.items():
        for d in range(num_doses):
            all_doses[(med_name, d)] = model.NewIntVar(0, num_brackets - 1, f'{med_name}_d{d}')

    # constraints
    all_slacks = []

    # Same-Medication
    for med_name, num_doses in med_requirements.items():
        for d in range(num_doses - 1):
            model.Add(all_doses[(med_name, d+1)] >= all_doses[(med_name, d)] + same_med_lag)

    # Drug-Drug Conflicts 
    for (m1, m2), lag in drug_conflicts.items():
        if m1 in med_requirements and m2 in med_requirements:
            for d1 in range(med_requirements[m1]):
                for d2 in range(med_requirements[m2]):
                    diff = model.NewIntVar(0, num_brackets, f'diff_{m1}_{m2}_{d1}_{d2}')
                    model.AddAbsEquality(diff, all_doses[(m1, d1)] - all_doses[(m2, d2)])
                    
                    slack = model.NewIntVar(0, num_brackets, f'slack_{m1}_{m2}_{d1}_{d2}')
                    all_slacks.append(slack)
                    model.Add(diff + slack >= lag)

    # objective function
    is_daytime_vars = []
    for dose_var in all_doses.values():
        is_daytime = model.NewBoolVar('is_daytime')
        model.Add(dose_var <= 3).OnlyEnforceIf(is_daytime) 
        model.Add(dose_var > 3).OnlyEnforceIf(is_daytime.Not())
        is_daytime_vars.append(is_daytime)

    #  Minimize lag Maximize Daytime Drugs
    model.Maximize(sum(is_daytime_vars) * 10 - sum(all_slacks))

    # solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    #output
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        brackets = ["Morning", "Noon", "Afternoon", "Evening", "Midnight", "After-Midnight"]
        
        
        schedule = {i: [] for i in range(num_brackets)}
        for (m_name, d_idx), var in all_doses.items():
            schedule[solver.Value(var)].append(f"{m_name}(D{d_idx+1})")
        
        print(f"{'BRACKET':<20} | MEDICATIONS")
        print("-" * 50)
        for b_idx in range(num_brackets):
            meds_in_slot = ", ".join(schedule[b_idx]) if schedule[b_idx] else "--"
            print(f"{brackets[b_idx]:<20} | {meds_in_slot}")
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
        # Check for violations
        violations = [s for s in all_slacks if solver.Value(s) > 0]
        if violations:
            print(f"\n {len(violations)} conflicts were slightly compressed to fit the schedule.")
        else:
            print("\n Success: All 15 medications scheduled without conflict.")
    else:
        print("Model failed. Too many constraints for a 24h window.")

solve_complex_med_system()