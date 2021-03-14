from util import get_valid_coords, Point

"""
Finds the best station alignment by sequentially finding the best placement for
each individual statement. This makes the assumption that small changes in the
placement of one station will not affect the optimal placement of other stations.
The time-complexity of this is polynomial.
"""
def solve(num_stations, max_distance, tightness, destinations):
    valid_coords = get_valid_coords(destinations)
    if num_stations > len(valid_coords):
        raise ValueError("not enough room for all stations")
    return _solve(num_stations, max_distance, tightness, destinations, valid_coords)

def _solve(num_stations, max_distance, tightness, destinations, valid_coords):
    
    total_LOS = 0
    best_station_alignment = []
    
    for i in range(num_stations):
        station_coord = None
        max_LOS = 0
        stations = best_station_alignment.copy()
        for coord in valid_coords:
            stations.append(Point(coord[0], coord[1]))
            
            sum_LOS = 0
            # calculate LOS with this current alignment
            for destination in destinations:
                sum_LOS += destination.get_LOS(stations, max_distance, tightness)
            if sum_LOS > max_LOS:
                max_LOS = sum_LOS
                best_station_alignment = stations.copy()
                station_coord = coord
                
            # remove the station from the list so we don't corrupt future recursions
            stations.pop(len(stations) - 1)
        
        total_LOS = max_LOS
        # remove the coordinate of this station so it can't be used again
        valid_coords.remove(station_coord)
    
    return total_LOS, best_station_alignment
    