import math
import itertools

""" Basic class to support an immutable point."""
class Point(object):
    
    def __init__(self, x, y):
        
        self.X = x
        self.Y = y
        
    """ Returns the distance between this point and another. """
    def dist(self, other):
        dx = self.X - other.X
        dy = self.Y - other.Y
        return math.hypot(dx, dy)
    
    """ Returns the distance squared between this point and another. """
    def dsq(self, other):
        dx = self.X - other.X
        dy = self.Y - other.Y
        return (dx ** 2) + (dy ** 2)
    
    """ Returns the taxicab distance between this point and another. """
    def taxicab(self, other):
        return abs(self.X - other.X) + abs(self.Y - other.Y)
    
    def __eq__(self, other):
        return self.X == other.X and self.Y == other.Y
    
    def __str__(self):
        return "Point (%s, %s)"%(self.X, self.Y)

""" 
An extension of the Point class to include a name and population.
Includes a method for calculating how well this destination is served by nearby stations.
Only supports integer coordinates.
"""
class Destination(Point):
    
    def __init__(self, x, y, population, name="Destination"):
        if type(x) is not int or type(y) is not int:
            raise ValueError("Coordinates must be integers")
        Point.__init__(self, x, y)
        self.population = population
        self.name = name
    
    """
    Given a set of stations, calculates the total number of people originating 
    from this destination that will use the stations.
    """
    def get_LOS(self, stations, max_distance, tightness):
        ppl_served = 0
        
        for station in stations:
            # some other metrics I tried, before settling on the sigmoid function version:
            # ppl_served += (self.population / (self.dsq(station)))
            # ppl_served += (self.population / (self.taxicab(station)))
            ppl_served += (self.population * self._sigmoid(self.taxicab(station), max_distance, tightness))
            # cannot send more people to stations than the population of the destination
            if ppl_served >= self.population:
                return self.population

        return ppl_served
    
    # helper function, calculate LOS using modified sigmoid function
    def _sigmoid(self, x, point_of_inflection, slope):
        return (1.0 / (1.0 + (math.e ** ((slope / point_of_inflection) * (x - point_of_inflection))))) 
    
    def __str__(self):
        return "Destination \"%s\", (%s, %s), pop=%s"%(self.name, self.X, self.Y, self.population)
    
""" 
Given a set of destinations, returns the set of valid coordinates for a station.
This is any coordinate between the minimum and maximum coordinates for the set
of destinations excluding the coordinates already occupied by a destination.
"""
def get_valid_coords(destinations):
    min_X = None
    max_X = None
    min_Y = None
    max_Y = None
    
    # find rectangle that bounds set of destinations
    for dest in destinations:
        if not min_X or min_X > dest.X:
            min_X = dest.X
        if not max_X or max_X < dest.X:
            max_X = dest.X
        if not min_Y or min_Y > dest.Y:
            min_Y = dest.Y
        if not max_Y or max_Y < dest.Y:
            max_Y = dest.Y
    
    # get the cross product
    coords = list(itertools.product(range(min_X, max_X + 1), range(min_Y, max_Y + 1)))
    
    # re-iterate over list to remove already occupied coordinates
    for dest in destinations:
        coords.remove((dest.X, dest.Y))
    return coords