from exceptions import Exception

class DistsDiffer(Exception):
    def __init__(self, message):
        print "The two distributions under measure are not over the same set of variables."
        print message
