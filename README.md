# station_alignment
A set of algorithms for determining the optimal placement of transit stations given a model of a city (or cities).

Full documentation of the project, including explanation of design choices, can be found in [the report](https://github.com/remy-wolf/station_alignment/blob/main/Transit%20Station%20Alignment%20Algorithm%20Report.pdf). 

Run the program with `python main.py <input file> <algorithm>` from the src/ directory.

Input files should be located in the samples folder.
They should be structured as such:  

\<number of stations>  
<max_distance>  
\<tightness>  
<x-coordinate 1>, <y-coordinate 1>, <population 1>  
<x-coordinate 2>, <y-coordinate 2>, <population 2>  
.
.
.

Information how the `max_distance` and `tightness` hyperparameters are used can be found in [the report](https://github.com/remy-wolf/station_alignment/blob/main/Transit%20Station%20Alignment%20Algorithm%20Report.pdf). `max_distance` should represent the estimated maximum distance one will travel to a transit station from a destination, and `tightness` allows control over how quickly LOS of a station drops off near max_distance. From experimentation, 5 seems to be a good value for `tightness`.

Valid choices for `<algorithm>` are `-bfn|-bfi|-ga`, for the brute-force-naive, brute-force-intelligent, and greedy-approximation algorithms, respectively.
