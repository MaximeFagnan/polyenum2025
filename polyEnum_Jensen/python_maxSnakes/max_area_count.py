class MaxAreaCount:
    def __init__(self, max_area = None, nb_configs = None):
        self.max_area = 0 if max_area is None else max_area
        self.nb_configs = 0 if nb_configs is None else nb_configs
        
    def __add__(self, other):
        assert isinstance(other,MaxAreaCount)

        if self.max_area > other.max_area:
            return MaxAreaCount(self.max_area, self.nb_configs)
        elif self.max_area < other.max_area:
            return MaxAreaCount(other.max_area, other.nb_configs)
        else:
            return MaxAreaCount(self.max_area, self.nb_configs + other.nb_configs)

    def increase_max_area(self):
        self.max_area += 1

    def decrease_max_area(self):
        self.max_area -= 1

    def __repr__(self):
        return f"Max area: {self.max_area} \nNumber of configurations: {self.nb_configs}"

    def clone(self):
        return MaxAreaCount(self.max_area,self.nb_configs)
    
    # # No need to verify if empty?
    # def is_empty(self):
    #     if len(self.terms) == 0: 
    #         return True
    #     else:
    #         return False