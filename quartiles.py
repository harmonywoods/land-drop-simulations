import statistics
def quartiles(data):
    '''seemed easiest to roll my own quartile function, uses this algorithm from wikipedia
    Use the median to divide the ordered data set into two-halves.
        If there are an odd number of data points in the original ordered data set, do not include the median (the central value in the ordered list) in either half.
        If there are an even number of data points in the original ordered data set, split this data set exactly in half.
    The lower quartile value is the median of the lower half of the data. The upper quartile value is the median of the upper half of the data.
'''
    #returns upper quartile, median quartile, lower quartile
    median = statistics.median(data)
    data.sort()
    middle=int(len(data)/2.0)
    lowerhalf = data[0:middle+1]
    upperhalf = data[middle+1:]
    return [statistics.median(lowerhalf),median,statistics.median(upperhalf)]