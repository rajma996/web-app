class ConstraintError(object):
    str=None

    def __init__(self, str):
        self.str=str

    def __str__(self):
        return repr(self.str)



class TempData(object):
    min =None
    max =None

    def __init__(self, min, max):
        if self.invariant(min,max):
            self.min=min
            self.max=max
        else:
            raise ConstraintError("Min is greater than max");

    def get_min(self):
        return self.min

    def get_max(self):
        return self.max

    def invariant(self,a,b):
        return a<=b

    def set_min(self,min):
        if min<=self.max:
            self.min=min

        else:
            raise ConstraintError("Min is greater than max")

    def set_max(self,max):
        if max>=self.min:
            self.max=max
        else:
            raise ConstraintError("Max is less than min")
