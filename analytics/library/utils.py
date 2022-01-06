import numpy as np
import pandas as pd
from tabulate import tabulate
from tqdm.auto import tqdm 

#Retrieving Stream Data
def describe_streams(streams):
    table = [["Index", "Collection", "Name", "Units", "UUID"]]
    for idx, stream in enumerate(streams):
        tags = stream.tags()
        table.append([idx, stream.collection, stream.name, tags["unit"], stream.uuid])
    return tabulate(table, headers="firstrow")


# def stream_to_df(stream, start, end, pw=None, width=None, depth=None, agg=None, 
#                   to_datetime=False):  
#     if agg != None:
#         agg = agg = list(set(agg))
#         if agg == 'all':
#             agg = ['min','mean','max', 'count', 'stddev']
#     else:
#         # if the user doesn't pass in a list of args 
#         agg = ['value']
        
#     if 'time' not in agg : 
#         agg.append('time')
        
        
#     if pw is not None:
#         points, _ = zip(*stream.aligned_windows(start=start, end=end, pointwidth=pw))
#     elif (width is not None) and (depth is not None):
#         points, _ = zip(*stream.windows(start=start, end=end, width=width, depth=depth))
#     else:
#         points, _ = zip(*stream.values(start=start,end=end))


#     data = [tuple(getattr(point,a) for a in agg) for point in points] 
#     streams_df = pd.DataFrame(data, columns = agg)
#     streams_df = streams_df.set_index('time', drop=True)
    
#     if to_datetime:
#         streams_df.index = pd.to_datetime(streams_df.index)
        
#     return streams_df


def streams_to_df(streams, start, end, pw=None, width=None, depth=None, agg=None, 
                  to_datetime=False, disable_progress_bar=False):  
    if agg != None:
        agg = agg = list(set(agg))
        if agg == 'all':
            agg = ['min','mean','max', 'count', 'stddev']
    else:
        # if the user doesn't pass in a list of args 
        agg = ['value']
        
    if 'time' not in agg : 
        agg.append('time')
    
    if not isinstance(streams, list):
        streams = [streams]
    
    df_dict = {}
    
    prog_bar = tqdm(enumerate(streams), total=len(streams), disable=disable_progress_bar,
                    desc='Getting streams', dynamic_ncols=True)
    for ith_stream, stream in prog_bar:
        if pw is not None:
            points, _ = zip(*stream.aligned_windows(start=start, end=end, pointwidth=pw))
        elif (width is not None) and (depth is not None):
            points, _ = zip(*stream.windows(start=start, end=end, width=width, depth=depth))
        else:
            points, _ = zip(*stream.values(start=start,end=end))

        data = [tuple(getattr(point,a) for a in agg) for point in points]
        streams_df = pd.DataFrame(data, columns = agg)
        streams_df = streams_df.set_index('time', drop=True)
        df_dict[(stream.collection, stream.unit, stream.name)] = streams_df

    df = pd.concat(df_dict, axis=1)
    df.columns.names =  ['collection', 'unit', 'name', 'agg']
    
    if to_datetime:
        df.index = pd.to_datetime(df.index)
        
    return df

# Converts pointwidths to seconds
def seconds2pointwidth(seconds):
    return np.log(1e9*seconds) / np.log(2) 


# Returns the mean value of a stream. Useful for automatically getting the 
# nominal voltage
def get_global_mean_value(stream, pw=55, version=0):
    earliest_time = stream.earliest()[0][0]
    latest_time = stream.latest()[0][0]
    # Get all of the stat points at the highest level of the tree as possible
    statpoints, _ = zip(*stream.aligned_windows(
        start=earliest_time, end=latest_time, pointwidth=pw, version=version
    ))

    # Unless you have decades of data, this will likely only be one stat point
    # use np.mean() to ensure only 1 overall mean of all statspoints being returned
    sps_mean = np.mean([sp.mean for sp in statpoints])
    return sps_mean

# Gets window of data around point
def get_event(stream, event_time, window_in_sec = 0.5, version=0):
    window_in_nanosec = 1e9 * window_in_sec 
    raw_points, _ = zip(*stream.values(event_time-window_in_nanosec, 
                                       event_time+window_in_nanosec, 
                                       version)) 
    values = [raw_point[1] for raw_point in raw_points]
    return values

def freq_vs_size(size_min, size_max):
    x = np.arange(size_min, size_max, 0.001)
    y = x / (1-x)
    area = integral(size_max) - integral(size_min)
    return x, y / area
    
def integral(x):
    return -x-np.log(1-x)

def window_avg(timeseries, sampling_period, num_seconds=60):
    print(sampling_period)
    num_avg = int(num_seconds/sampling_period)
    print(num_avg)
    num_points = len(timeseries)
    avg_timeseries = np.zeros(num_points-num_avg)
    
    for i in range(num_points-num_avg):
        avg_timeseries[i] = np.mean(timeseries[i:i+num_avg])
    return avg_timeseries, num_avg
  
def window_std(timeseries, sampling_period, num_seconds=60):
    print(sampling_period)
    num_avg = int(num_seconds/sampling_period)
    print(num_avg)
    num_points = len(timeseries)
    std_timeseries = np.zeros(num_points-num_avg)
    for i in range(num_points-num_avg):
        std_timeseries[i] = np.std(timeseries[i:i+num_avg])
    return std_timeseries, num_avg