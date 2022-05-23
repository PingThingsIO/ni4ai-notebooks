from matplotlib import pyplot as plt

import os
import pandas as pd
import numpy as np

def plot_event_timeseries(df, streams):
    stream_names = [[], []]
    legend_names = [[], []]
    for s in streams:
        if s.unit == 'amps':
            stream_names[0].append(os.path.join(s.collection, s.name))
            legend_names[0].append(s.name)
        elif s.unit == 'volts':
            stream_names[1].append(os.path.join(s.collection, s.name))
            legend_names[1].append(s.name)

    fig, ax = plt.subplots(figsize=(15,3), ncols=2)

    _df = df[stream_names[0]].rename(columns=dict(zip(stream_names[0], legend_names[0])))
    _df.plot(ax=ax[0])

    _df = df[stream_names[1]].rename(columns=dict(zip(stream_names[1], legend_names[1])))
    _df.plot(ax=ax[1])

    ax[0].set_title('%s\nCurrent Streams'%(s.collection))
    ax[1].set_title('%s\nVoltage Streams'%(s.collection))
    ax[0].set_ylabel('Amps')
    ax[1].set_ylabel('Volts')
    plt.show()  