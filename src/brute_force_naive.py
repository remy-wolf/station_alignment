from util import get_valid_coords, Point

"""
Finds the best placement for each station via brute force. This will iterate
over every possible X & Y placement of each station (where stations sharing the
same coordinates as a destination or another station is invalid).
The time-complexity of this is exponential.
"""
def solve(num_stations, max_distance, tightness, destinations):
    valid_coords = get_valid_coords(destinations)
    if num_stations > len(valid_coords):
        raise ValueError("not enough room for all stations")
    return _solve(num_stations, max_distance, tightness, destinations, [], valid_coords)

def _solve(num_stations, max_distance, tightness, destinations, stations, valid_coords):
    if num_stations <= 0:
        # base case, calculate the score for this alignment
        sum_LOS = 0
        for destination in destinations:
            sum_LOS += destination.get_LOS(stations, max_distance, tightness)
        return (sum_LOS, stations.copy())
    
    # the maximum LOS we can achieve given where we know previous stations are already located
    max_LOS = 0
    # the best alignment of stations given where we know previous stations are already located
    best_station_alignment = None
    
    # find best location for this station
    for coord in valid_coords:
        # ensure that further stations cannot share the same location as this one
        updated_valid_coords = valid_coords.copy()
        updated_valid_coords.remove(coord)
        
        coord = Point(coord[0], coord[1])
        stations.append(coord)
        # find the best total LOS for the remaining stations if we put a station at this point
        sum_LOS, full_stations = _solve(
            num_stations - 1, max_distance, tightness, destinations, stations, updated_valid_coords)
        # remove the station from the list so we don't corrupt future recursions
        stations.pop(len(stations) - 1)
        if max_LOS < sum_LOS:
            max_LOS = sum_LOS
            best_station_alignment = full_stations
    return (max_LOS, best_station_alignment)