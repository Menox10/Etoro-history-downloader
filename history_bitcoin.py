#!/usr/bin/python
########### Python 2.7 #############
import httplib, urllib, base64, re
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import time
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

# major and minor plot seetings
majorLocator = MultipleLocator(200)
majorFormatter = FormatStrFormatter('%d')
minorLocator = MultipleLocator(50)

majoryLocator = MultipleLocator(10)
majoryFormatter = FormatStrFormatter('%d')
minoryLocator = MultipleLocator(2)

majorXLocator = MultipleLocator(24)
majorXFormatter = FormatStrFormatter('%d')
minorXLocator = MultipleLocator(6)

def history(a):
    
    body = a[2:-4]
    closeprice = []

    for key in body:
       if "Close" in key:
           c = key.split(':')
           close = float(re.findall('\d+\.\d+', c[1] )[0])
           closeprice.append(close) 

    return closeprice

def moving_average(x, n, type='simple'):
    """
    compute an n period moving average.

    type is 'simple' | 'exponential'

    """
    x = np.asarray(x)
    if type == 'simple':
        weights = np.ones(n)
    else:
        weights = np.exp(np.linspace(-1., 0., n))

    weights /= weights.sum()

    a = np.convolve(x, weights, mode='full')[:len(x)]
    a[:n] = a[n]
    return a

def plotcoin(closeprice):

    # create Bitcoin plot
    ema50 = moving_average(closeprice, 50, type='exponential')
    fig, ax1 = plt.subplots()
    ax1.plot(closeprice[-480:] , 'g-')
    ax1.plot(ema50[-480:] , 'r-') 
    ax1.set_title('Bitcoin Price Etoro') 
    ax1.set_xlabel('Time (1 Hour)', color='k')
    ax1.set_ylabel('Close price (USD)', color='k')
    ax1.tick_params(colors='k')
    ax1.grid(color='k', linestyle='-', linewidth=0.5)
    ax1.yaxis.set_major_locator(majorLocator)
    ax1.yaxis.set_major_formatter(majorFormatter)
    ax1.yaxis.set_minor_locator(minorLocator)
    ax1.xaxis.set_major_locator(majorXLocator)
    ax1.xaxis.set_major_formatter(majorXFormatter)
    ax1.xaxis.set_minor_locator(minorXLocator)
    plt.savefig('bitcoin.png')   # save the figure to file
    plt.close(fig)    # close the figure


conn = httplib.HTTPSConnection('candle.etoro.com')
# 480 is 480 periods of 1 hour, 100000 is Bitcoin
conn.request("GET", "/candles/asc.json/OneHour/480/100000")
response = conn.getresponse()
data = response.read()
a = data.split(',')
closeprice = history(a)
print(closeprice)
conn.close()
plotcoin(closeprice)
