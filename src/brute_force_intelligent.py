from util import get_valid_coords, Point

"""
Finds the best placement for each station via brute force. This will iterate
over every possible X & Y placement of each station (where stations sharing the
same coordinates as a destination or another station is invalid). However, it
will avoid identical alignments (because order of stations does not matter).
The time-complexity of this is factorial.
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
    
    # these are used to splice the coordinate array so we don't have to check identical alignments
    min_index = 1
    max_index = len(valid_coords) - num_stations + 1
    # find best location for this station
    for coord in valid_coords[:max_index]:
        coord = Point(coord[0], coord[1])
        stations.append(coord)
        # find the best total LOS for the remaining stations if we put a station at this point
        sum_LOS, full_stations = _solve(
            num_stations - 1, max_distance, tightness, destinations, stations, valid_coords[min_index:])
        # remove the station from the list so we don't corrupt future recursions
        stations.pop(len(stations) - 1)
        if max_LOS < sum_LOS:
            max_LOS = sum_LOS
            best_station_alignment = full_stations
        min_index += 1
    return (max_LOS, best_station_alignment)