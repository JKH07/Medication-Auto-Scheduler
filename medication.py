import datetime

class medication:
    def __init__(self, name, dosage,id,min_gap_min,conflicts=None,constraints=None):
        self.name=name
        self.dosage=dosage
        self.id=id
        self.conflicts=conflicts or []
        self.constraints=constraints or []
        
        self.min_gap_min=min_gap_min

        #fill later
        self.interval_vars = []
        self.timing=datetime
