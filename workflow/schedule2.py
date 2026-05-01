from ortools.sat.python import cp_model


BRACKETS = ["Morning", "Noon", "Afternoon", "Evening", "Night", "AfterMidnight"]
NUM_BRACKETS = len(BRACKETS)
DAYTIME_CUTOFF = 3   # brackets 0-3 are daytime (up to and including 6PM-10PM)
SAME_MED_LAG = 2     # minimum bracket gap between doses of the same medication


def solve_med_schedule(med_requirements: dict, drug_conflicts: dict) -> dict | None:
   
    model = cp_model.CpModel()

    # -- Decision variables ---------------------------------------------------
    all_doses: dict = {}
    for med_name, num_doses in med_requirements.items():
        for d in range(num_doses):
            all_doses[(med_name, d)] = model.NewIntVar(
                0, NUM_BRACKETS - 1, f"{med_name}_d{d}"
            )

    # -- Constraints ----------------------------------------------------------

    # 1. Same-medication spacing: doses of the same drug must be spread out
    for med_name, num_doses in med_requirements.items():
        for d in range(num_doses - 1):
            model.Add(
                all_doses[(med_name, d + 1)] >= all_doses[(med_name, d)] + SAME_MED_LAG
            )

    # 2. Drug-drug conflict spacing (hard constraint - gap must be met or infeasible)
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

    # -- Objective ------------------------------------------------------------
    # Maximise daytime doses - all conflict gaps are hard constraints.
    is_daytime_vars: list = []
    for idx, dose_var in enumerate(all_doses.values()):
        is_daytime = model.NewBoolVar(f"is_daytime_{idx}")
        model.Add(dose_var <= DAYTIME_CUTOFF).OnlyEnforceIf(is_daytime)
        model.Add(dose_var > DAYTIME_CUTOFF).OnlyEnforceIf(is_daytime.Not())
        is_daytime_vars.append(is_daytime)

    model.Maximize(sum(is_daytime_vars))

    # -- Solve ----------------------------------------------------------------
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # -- Output ---------------------------------------------------------------
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        schedule: dict = {}
        for (med_name, dose_idx), var in all_doses.items():
            bracket_name = BRACKETS[solver.Value(var)]
            label = (
                f"{med_name}({dose_idx + 1})"
                if med_requirements[med_name] > 1
                else med_name
            )
            schedule.setdefault(bracket_name, []).append(label)
            
        return schedule
    else:
        print("MODEL FAILED TO FIND A SOLUTION")
        print(f"  Status: {solver.StatusName(status)}")
        print("  Possible reasons:")
        print("  - same_med_lag too large relative to NUM_BRACKETS")
        print("  - too many multi-dose medications")
        print("  - conflicting hard constraints")
        return None


# -- Example run --------------------------------------------------------------
if __name__ == "__main__":
    med_requirements = {
        "Aspirin":        1,
        "Metoprolol":     2,
        "Lisinopril":     1,
        "Atorvastatin":   1,
        "Furosemide":     2,
        "Clopidogrel":    1,
        "Amlodipine":     1,
        "Isosorbide":     2,
        "Warfarin":       1,
        "Digoxin":        1,
        "Spironolactone": 1,
        "Potassium_Sup":  1,
    }

    drug_conflicts = {
        ("Metoprolol",  "Amlodipine"):    2,
        ("Furosemide",  "Lisinopril"):    2,
        ("Warfarin",    "Aspirin"):       3,
      
    }

    result = solve_med_schedule(med_requirements, drug_conflicts)
    print(result)