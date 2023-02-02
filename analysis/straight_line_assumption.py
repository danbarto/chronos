#!/usr/bin/env python3

import math

def rel_error(l, p):
    '''
    calculate the relative error we make by assuming a straight line instead of the curved track

    '''
    r = 3*p/3.8
    b = 2*r*math.asin(l/(2*r))
    return abs((b-l)/b)


if __name__ == "__main__":

    pt = 5
    print (f"Assuming particles with pt>{pt} GeV")
    print ("Shortest distance from IP to MTD: 1.15m.")
    print (f"- Relative Error: {rel_error(1.15, 5)}")

    longest_distance = round(math.sqrt(3**2 + 1.2**2),2)  # outer edge of ETL
    print (f"Shortest distance from IP to MTD: {longest_distance}m.")
    print (f"- Relative Error: {rel_error(longest_distance, 5)}")

    pt = 10
    print (f"Assuming particles with pt>{pt} GeV")
    print ("Shortest distance from IP to MTD: 1.15m.")
    print (f"- Relative Error: {rel_error(1.15, pt)}")

    longest_distance = round(math.sqrt(3**2 + 1.2**2),2)  # outer edge of ETL
    print (f"Shortest distance from IP to MTD: {longest_distance}m.")
    print (f"- Relative Error: {rel_error(longest_distance, pt)}")
