import pandas as pd
import numpy as np

import btrdb
from btrdb.utils.timez import *

import os
from matplotlib import pyplot as plt

def seconds2pointwidth(seconds):
    return np.log(1e9*seconds) / np.log(2) 

def write_to_stream(stream, times, values):
    if hasattr(times, '__len__'):
        stream.insert(list(zip(times, values)), merge='replace')
    else:
        stream.insert([(times, values),], merge='replace')


def get_stream_duration(stream, unit='hours'):
    start, _ = stream.earliest()
    end, _ = stream.latest()
    
    nanosec = end.time - start.time
    seconds = nanosec / 1e9
    
    if unit == 'hours':
        return seconds / 3600
    
    elif unit == 'days':
        return seconds / 3600 / 24
    
def print_stream_summary(stream):
    print(f"""
        Collection: {stream.collection}
        Measurement: {stream.name}
        Duration: {np.round(get_stream_duration(stream), 1)} hours
        Size: {np.round(stream.count()/1e6, 2)} million points
        """)
    
def print_metadata_summary(db, collection):
    streams = db.streams_in_collection(collection)
    metadata, _ = streams[0].annotations()
    
    print('\n', collection)
    for key in metadata.keys():
        print('   %s: %s'%(key, metadata[key]))
        

def convert_timestamp(time, t0=None, tf=None, convert_to=None):
    if convert_to == 'datetime':
        if type(time) == int:
            return ns_to_datetime(time)
        else:
            return [ns_to_datetime(t) for t in time]

    elif convert_to == 'relative':
        if type(time) == int:
            return (time - t0)/1e9
        
        elif hasattr(time, '__len__'):
            return (time - min(time))/1e9
        
    elif 'normalized':
        if type(time) == int:
            return (time - t0) / (tf - t0)
        
        elif hasattr(time, '__len__'):
            return [(t - t0) / (tf - t0) for t in time]

    elif time_conversion == None:
        return time

    
def points_to_dataframe(points, 
                        resolution=None, # accepts: 'full' or integer pointwidth
                        aggregates=['time','mean','min','max','count','stddev'], # accepts: 
                        convert_time_to=None, # accepts: None, datetime, relative, normalized
                        use_time_as_index=True,
                        t0=None
                       ):
    
    time_kwargs = {'t0': points[0][0].time if t0 == None else t0, 
                   'tf': points[-1][0].time, 
                   'convert_to': convert_time_to}
    

    if resolution == 'full':
        # create dataframe from raw point values
        df = pd.DataFrame(columns=['time','value'], index=range(len(points)))
        
        for i, (point, _) in enumerate(points):
            time = convert_timestamp(point.time, **time_kwargs)
            df.loc[i] = [time, point.value]
        
    else:
        # create dataframe from statpoint attributes
        df = pd.DataFrame(columns=aggregates, index=range(len(points)))
        for i, (point, _) in enumerate(points):
            df.loc[i] = [getattr(point, attr) for att in aggregates]
            
            if convert_time_to != None:
                df['time'].loc[i] = convert_timestamp(point.time, **time_kwargs)
                                
    if use_time_as_index:                
        # resets index to use time instead of range
        df = df.set_index('time')
        
    return df


def get_points_from_collection(db, collection,
                               resolution='full',
                               filter_kwargs={}, 
                               rename_cols=False,
                               convert_time_to=None,
                               ):
    
    streams = db.streams_in_collection(collection, **filter_kwargs)
    streamset = btrdb.stream.StreamSet(streams)
    
    start, _ = streams[0].earliest()
    end, _ = streams[0].latest()
    
    if resolution == 'full':
        df = streamset.filter(start.time, end.time).to_dataframe()
        
    elif type(resolution) == int:
        # to do
        pass
    
    if convert_time_to != None:
        df['time'] = convert_timestamp(df['time'], 
                                       t0=df['time'].min(), tf=df['time'].max(), 
                                       convert_to=convert_time_to)
        
    if rename_cols == True:
        df = df.rename(columns=dict(zip(df.keys().tolist(), [s.name for s in streams])))
        
    return df
    
        
