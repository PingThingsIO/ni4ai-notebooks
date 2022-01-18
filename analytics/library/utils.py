import btrdb
import numpy as np
import pandas as pd
from tabulate import tabulate
from tqdm.auto import tqdm 

#Retrieving Stream Data
def describe_streams(streams):
    """
    This function prints streams info("Collection", "Name", "Units", "UUID") in tabular format.
    
    Parameters
    ----------
    streams : list of Stream objects or Streamset.
    
    Examples
    ----------
    >>> streams = db.streams_in_collection('sunshine/PMU3')
    >>> print(describe_streams(streams))
    """   
    table = [["Index", "Collection", "Name", "Units", "UUID"]]
    for idx, stream in enumerate(streams):
        tags = stream.tags()
        table.append([idx, stream.collection, stream.name, tags["unit"], stream.uuid])
    return tabulate(table, headers="firstrow")


def get_streamset(conn, collection_name, return_metadata=False, return_uuid=False, **kwargs):
    """
    This function creates dynamic sql queries depending on the input kwargs being passed in for tags and annotations.
    
    Parameters
    ----------
    conn : BTrDB connection object
    collection_name : str or list of str
        str of collection name. The format is collection_name='str' or collection_name=[str1, str2]
    return_metadata : bool, default=False 
        Return the json metadata of each stream if set to True.
    return_uuid : bool, default=False 
        Return the uuid of each stream if set to True.
    kwargs : List of column names in PostgreSQL database that are used to identify the streams. 
                     For non-annotations keys besides collection, the format is key='str' or key=[str1, str2]
                     For annotations keys, the format is annotations={'key':str1} or annotations={'key':[str1,str2]}
    
    Returns
    ----------
    streams : list of uuids, list of metadata json or a streamset object. Default is a streamset object of desired streams.
    
    Notes
    ----------
    For non-annotations keys in kwargs, they are distiller, ingress, name, unit, uuid and property_version. 
    The first 4 are tags for the stream.
    
    Examples
    ----------
    # get streamset of streams in multiple collections
    >>> my_streamset =  get_streamset(conn, collection_name = ['agave/IC_B/B5', 'agave/IC_A/A1'], 
                                        name='VPM', annotations={'sample_rate':'30'})
    # get streamset of streams with multiple sample_rate in annotations
    >>> my_streamset =  get_streamset(conn, collection_name = ['agave/IC_B/B5', 'agave/IC_A/A1'], 
                                        name='VPM', annotations={'sample_rate':['30','60']})
    # get uuids of streams for streams in multiple collections
    >>> my_streamset =  get_streamset(conn, collection_name = ['agave/IC_B/B5', 'agave/IC_A/A1'], 
                                        name='VPM', annotations={'sample_rate':['30','60']}, return_uuid=True)
    # get json metadata of streams for streams in multiple collections
    >>> my_streamset =  get_streamset(conn, collection_name = ['agave/IC_B/B5', 'agave/IC_A/A1'], 
                                        name='VPM', annotations={'sample_rate':['30','60']}, return_metadata=True)                                        
    """    
    annotations = kwargs.get('annotations')
    
    query_params = []

#     sql = f""" Select * from streams where """
    
    param_count=1
    # force collection_name to be a list so we go through them one by one to create sql statement
    if type(collection_name) is not list:
        collection_name = [collection_name]
            
#     sql = sql +  """collection similar to $1 """
    sql = "select * from streams where collection similar to $1"
    query_params=[] # empty place holder to store all the kwargs
    
    # placeholder that will store a list of sql statements that will be combined in the end later
    query_params.append('|'.join([f"%{c}%" for c in collection_name])) 
    param_count = param_count + 1 # since collection will use one param
    
    sql_list = []  # placeholder that will store a list of sql statements that will be combined in the end later
    for k, v in kwargs.items():
        # skip annotations as annotations is stored as hstore and have a different sql syntax than tags
        if k == 'annotations':
            continue
        if type(v) is not list:
            v = [v]
        # go through the list of values to create sql queries for tags 
        temp_param_store = []
        for item in v :                
            query_params.append(f"{item}")
            temp_param_store.append(f"${param_count}")
            param_count += 1                                
        sql_list.append(f" {k} in ({','.join(temp_param_store)})")
        
    if annotations is not None:
        
        ########## Check to see if user-passed-in-annotations are actually in annotations ##########
        not_found_annotations= {}
        
        # go through each collection to make sure the annotations keys being passed in actually exist in metadata
        not_found_in_collections=[]
        for collection in collection_name:
            
            collection_annotations = set(conn.collection_metadata(collection)[1].keys())
            check_annotations = set(annotations.keys()).difference(collection_annotations)
                        
            if len(check_annotations) > 0: 
                not_found_annotations[collection]  = check_annotations
        
        # if one or more annotation not found in metadata table, 
        # an error will be thrown to tell you which annotation(s) is not found and in which collection(s)
        if len(not_found_annotations) > 0:
            unknown_annotation_count=1
            error_message = ''
            for not_found_k, not_found_v in not_found_annotations.items():
                and_str=''
                if unknown_annotation_count > 1:
                    and_str = ", AND "
                
                error_message = error_message + and_str+ f'{not_found_v} not found in collection "{not_found_k}"' 
                unknown_annotation_count += 1
            raise Exception(f'{error_message}')
               
        # if annotations exist in metadata, then proceed to create sql queries
        for k, v in annotations.items():
            if type(v) is not list:
                v = [v]                
            temp_param_store = []    
            # go through the list of values to create sql queries for annotations            
            for item in v :                 
                query_params.append(f"{item}")
                temp_param_store.append(f"${param_count}")
                param_count += 1
            sql_list.append(f" annotations -> '{k}' in ({','.join(temp_param_store)})")
                               
    # combine all sql statements    
    for sql_statement in sql_list:
        sql = sql + " and" + sql_statement
        
    streams_metadata = conn.query(sql, query_params)
    
    if return_metadata:
        return streams_metadata 

    if return_uuid:
        streams_metadata = [s['uuid'] for s in streams_metadata]
        return streams_metadata
        
    streams_metadata = conn.streams(*[s['uuid'] for s in streams_metadata])
    
    return streams_metadata



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
    """
    This function query the data of the input streams and return their values in panda dataframe format.
    
    Parameters
    ----------
    streams : btrdb.Stream, [btrdb.Stream], or btrdb.Stream.Streamset
        Desired streams to query the data for.
    start : int or float
        Start time to query data in nanoseconds.
    end : int or float
        End time to query data in nanoseconds.  
    pw : int, default=None
        Pointwidth used to query data using aligned_windows().
    width : int, default=None
        Width used to query data using windows().
    depth : int, default=None
        Depth used to query data using windows(). 
    agg : str,[str] default=None
        Aggregates to use when using aligned_windows() or windows(). 
        The aggreates that can be used are : ['min','mean','max', 'count', 'stddev'].
        If agg='all', all the aggregates in the list above will ne returned.
   to_datetime : bool, default=False
        Return the timestamps as datetime instead of nanoseconds.
   disable_progress_bar : bool, default=False
        Disable progress bar when querying data.
    
    Returns 
    ----------
    df : pandas.DataFrame
        Pandas multi-index Dataframe containing streams values with index being the timestamps.
        The levels of multi-index columns are in the order of ['collection', 'unit', 'name', 'agg'].
        
    Examples
    ----------
    >>> data = streams_to_df(streamset, start_time, end_time, pw=26, agg=['mean'], to_datetime=True)
    """     
    if agg != None:
        agg = agg = list(set(agg))
        if agg == 'all':
            agg = ['min','mean','max', 'count', 'stddev']
    else:
        # if the user doesn't pass in a list of args 
        agg = ['value']
        
    if 'time' not in agg : 
        agg.append('time')
    
    # if only one stream being passed in, put it in a list
    if isinstance(streams, btrdb.stream.Stream):
        streams = [streams]
    
    df_dict = {}
    prog_bar = tqdm(enumerate(streams), total=len(streams), disable=disable_progress_bar,
                    desc='Getting streams', dynamic_ncols=True)
    for ith_stream, stream in prog_bar:        
        if pw is not None:
            data = stream.aligned_windows(start, end, pw)
        elif width is not None:
            data = stream.windows(start, end, width, depth=depth)
        else:
            data = stream.values(start, end)

        if len(data) > 0:
            points, _ = zip(*data)
        else:
            continue

        data = [tuple(getattr(point,a) for a in agg) for point in points]
        streams_df = pd.DataFrame(data, columns = agg)
        streams_df = streams_df.set_index('time', drop=True)
        df_dict[(stream.collection, stream.unit, stream.name)] = streams_df

    df = pd.concat(df_dict, axis=1)
    df.columns.names =  ['collection', 'unit', 'name', 'agg']
    
    if to_datetime:
        df.index = pd.to_datetime(df.index)
        
    return df


def to_nearest_pointwidth(days=0, hours=0, minutes=0, seconds=0, milliseconds=0, 
                          microseconds=0, nanoseconds=0, hertz=0):
    """
    Convert time delta of days, hours, minutes, seconds, milliseconds, microseconds, nanoseconds or hertz to nearest pointwidth. This function will return the nearest pointwidth and the margin of error in nanoseconds.
    
    Parameters
    ----------
    days : int or float
        Number of days.
    hours : int or float
        Number of hours.
    minutes : int or float
        Number of minutes.
    seconds : int or float
        Number of seconds.
    milliseconds : int or float
        Number of milliseconds.        
    microseconds : int or float
        Number of mimicrosecondsnutes.
    nanoseconds : int or float
        Number of nanoseconds.
    hertz : int or float
        Frequency in hertz.
        
    Returns
    ----------
    prevpw : int
        Closest pointwidth of the input time/frequency.
    preverr : float
        Margin of errors to the closest pointwidth of the input time/frequency.
    nextpw : int
        Closest pointwidth of the input time/frequency.
    nexterr : float
        Margin of errors to the closest pointwidth of the input time/frequency.
    
    Examples
    ----------
    >>> pw, err = to_nearest_pointwidth(days=1)
    """  
    if hertz != 0:
        seconds = 1/hertz
    
    dt_ns = ns_delta(days=days, hours=hours, minutes=minutes, seconds=seconds, 
                           milliseconds=milliseconds, microseconds=microseconds, nanoseconds=nanoseconds)
    prevpw = int(np.floor(np.log2(dt_ns)))
    nextpw = int(np.ceil(np.log2(dt_ns)))
    
    preverr = dt_ns - pointwidth(prevpw).nanoseconds 
    nexterr = pointwidth(nextpw).nanoseconds - dt_ns
    
    if preverr <= nexterr:
        return prevpw, preverr
    else:
        return nextpw, nexterr


def seconds2pointwidth(seconds):
    """
    Converts pointwidths to seconds.
    
    Parameters
    ----------
    seconds : int or float
        Number of seconds.
        
    Returns
    ----------
    int
      Closest pointwidth to the input seconds  
    """      
    return np.log(1e9*seconds) / np.log(2) 


def get_global_mean_value(stream, pw=55, version=0):
    """
    Returns the global mean value of a stream. Useful for programmatically estimating the nominal value.
    
    Parameters
    ----------
    stream : btrdb.Stream
        Stream object.
    pw : int, default=55
        Pointwidth.
    version : int, default=0
        Stream version.
        
    Returns
    ----------
    sps_mean : float
      Global mean across the entire stream. 
    """  
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

# # Gets window of data around point
# def get_event(stream, event_time, window_in_sec = 0.5, version=0):
#     window_in_nanosec = 1e9 * window_in_sec 
#     raw_points, _ = zip(*stream.values(event_time-window_in_nanosec, 
#                                        event_time+window_in_nanosec, 
#                                        version)) 
#     values = [raw_point[1] for raw_point in raw_points]
#     return values


def get_event_data(stream, event_time, window_in_sec_left = 0.5, window_in_sec_right=0.5, version=0,
                  return_timestamp=False):
    """
    Returns the raw values of a stream around a specified event time. The duration of the data returned is adjustable, defaulting to one second centering the event time.
    
    Parameters
    ----------
    stream : btrdb.Stream
        Stream object.
    event_time : int or float
        Event time.
    window_in_sec_left : int or float, default=0.5
        Duration of queried data (in seconds) preceding the event time.
    window_in_sec_right : int or float, default=0.5
        Duration of queried data (in seconds) following the event time.  
    version : int, default=0
        Stream version.
    return_timestamp : bool, default=False
        Whether to return the timestamps or only the stream values.
        
    Returns
    ----------
    timestamps : list of int
      Timestamps of the stream in the queried windows in nanoseconds.
    values : numpy.array
      Values of the stream.      
    """     
    window_in_nanosec_left = 1e9 * window_in_sec_left 
    window_in_nanosec_right = 1e9 * window_in_sec_right 
    
    raw_points, _ = zip(*stream.values(event_time-window_in_nanosec_left, 
                                       event_time+window_in_nanosec_right, 
                                       version)) 
    timestamps, values = zip(*raw_points)

    if return_timestamp:
        return timestamps, np.array(values)
    else:
        return np.array(values)
    
    
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