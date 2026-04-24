#tests

#  MEDICATION REQUIREMENTS

med_requirements = {
    "Metformin": 3,        
    "Glipizide": 2,        
    "Losartan": 1,         
    "Hydrochlorothiazide": 1,
    "Jardiance": 1,        
    "Atorvastatin": 1,     
    "Aspirin_Low": 1,      
    "Omega3": 2,           
    "B12_Complex": 1,     
    "Magnesium": 1,       
    "Lantus": 1           
}

# DRUG-DRUG CONFLICTS
drug_conflicts = {
    ("Metformin", "Glipizide"): 1,      
    ("Losartan", "Hydrochlorothiazide"): 2, 
    ("Metformin", "Atorvastatin"): 1,   
    ("Lantus", "Glipizide"): 3          
}

# 1. MEDICATION REQUIREMENTS
med_requirements = {
    "Gabapentin": 3,     
    "Ibuprofen_800": 3,    
    "Acetaminophen": 3,  
    "Amoxicillin": 3,      
    "Pantoprazole": 1,    
    "Stool_Softener": 2,  
    "Vitamin_C": 1,        
    "Zinc": 1             
}

# 2. DRUG-DRUG CONFLICTS

drug_conflicts = {
    ("Gabapentin", "Acetaminophen"): 2, 
    ("Amoxicillin", "Ibuprofen_800"): 1,
    ("Ibuprofen_800", "Acetaminophen"): 1 
}


