from ortools.sat.python import cp_model


BRACKETS = ["Morning", "Noon", "Afternoon", "Evening", "Night", "AfterMidnight"]
NUM_BRACKETS = len(BRACKETS)
DAYTIME_CUTOFF = 3   
SAME_MED_LAG = 1   


def solve_med_schedule(med_requirements: dict, drug_conflicts: dict) -> dict | None:
   
    model = cp_model.CpModel()

    #variables
    all_doses: dict = {}
    for med_name, num_doses in med_requirements.items():
        for d in range(num_doses):
            all_doses[(med_name, d)] = model.NewIntVar(
                0, NUM_BRACKETS - 1, f"{med_name}_d{d}"
            )

    # constraints

    # Same-medication spacing
    for med_name, num_doses in med_requirements.items():
        for d in range(num_doses - 1):
            model.Add(
                all_doses[(med_name, d + 1)] >= all_doses[(med_name, d)] + SAME_MED_LAG
            )

    # Drug-drug conflict spacing
    for (m1, m2), lag in drug_conflicts.items():
        if lag == 0:
            continue  # zero-lag adds no constraint
        if m1 not in med_requirements or m2 not in med_requirements:
            continue
        for d1 in range(med_requirements[m1]):
            for d2 in range(med_requirements[m2]):
                diff = model.NewIntVar(0, NUM_BRACKETS, f"diff_{m1}_{d1}_{m2}_{d2}")
                model.AddAbsEquality(diff, all_doses[(m1, d1)] - all_doses[(m2, d2)])
                model.Add(diff >= lag)

    #Objective
    # Maximise daytime doses
    is_daytime_vars: list = []
    for idx, dose_var in enumerate(all_doses.values()):
        is_daytime = model.NewBoolVar(f"is_daytime_{idx}")
        model.Add(dose_var <= DAYTIME_CUTOFF).OnlyEnforceIf(is_daytime)
        model.Add(dose_var > DAYTIME_CUTOFF).OnlyEnforceIf(is_daytime.Not())
        is_daytime_vars.append(is_daytime)

    model.Maximize(sum(is_daytime_vars))

    # solver
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # output
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        schedule = {}
        for (med_name, dose_idx), var in all_doses.items():
            bracket_name = BRACKETS[solver.Value(var)]
            label = (
                f"{med_name}_{dose_idx + 1}"
                if med_requirements[med_name] > 1
                else med_name
            )
            schedule[label] = bracket_name
        return schedule
    else:
        print("MODEL FAILED TO FIND A SOLUTION")
        print(f"  Status: {solver.StatusName(status)}")
        print("  Possible reasons:")
        print("  - same_med_lag too large relative to NUM_BRACKETS")
        print("  - too many multi-dose medications")
        print("  - conflicting hard constraints")
        return None


