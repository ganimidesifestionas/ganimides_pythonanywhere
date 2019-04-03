import datetime
import base64
import io
import plotly.tools as tls
import plotly.plotly as py
import numpy as np
import matplotlib.pyplot as plt
plt.rcdefaults()

"""
========
Barchart
========

A bar plot with errorbars and height labels on individual bars.
"""


def build_graph(x_coordinates, y_coordinates, title='', xlabel='', ylabel=''):
    img = io.BytesIO()
    #plt.figure(figsize=(3.7, 4))
    plt.plot(x_coordinates, y_coordinates, label='visits')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.savefig(img, format='png')

    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    #print(plt.figure)
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)


def build_barchart_vertical(labels, values, title='', xlabel='', ylabel=''):
    img = io.BytesIO()

    objects = labels  # ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
    y_pos = np.arange(len(objects))
    performance = values  # [10,8,6,4,2,1]
    #plt.figure(figsize=(3.7, 4))

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel(ylabel)
    plt.title(title)

    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)


def xbuild_barchart_horiz(labels, values):
    img = io.BytesIO()

    # Fixing random state for reproducibility
    np.random.seed(19680801)
    plt.rcdefaults()
    fig, ax = plt.subplots()

    # Example data
    people = ('Tom', 'Dick', 'Harry', 'Slim', 'Jim')
    y_pos = np.arange(len(people))
    values = 3 + 10 * np.random.rand(len(people))
    error = np.random.rand(len(people))

    N = len(labels)
    menMeans = (20, 35, 30, 35, 27)
    womenMeans = (25, 32, 34, 20, 25)
    menStd = (2, 3, 4, 1, 2)
    womenStd = (3, 5, 2, 3, 3)
    ind = np.arange(N)  # the x locations for the groups
    vStd = (1, 2)
    print('@@@@', N, ind, values)
    width = 0.35       # the width of the bars: can also be len(x) sequence

    p1 = plt.bar(ind, values, width, yerr=vStd)
    #p2 = plt.bar(ind, womenMeans, width,bottom=menMeans, yerr=womenStd)

    plt.ylabel('Visits')
    plt.title('Visits by Month')
    plt.xticks(ind, labels)
    plt.yticks(np.arange(0, 81, 10))
    #plt.legend((p1[0], p2[0]), ('Men', 'Women'))

    # plt.show()

    # ax.barh(y_pos, values, xerr=error, align='center', color='green', ecolor='black')
    # ax.set_yticks(y_pos)
    # ax.set_yticklabels(people)
    # ax.invert_yaxis()  # labels read top-to-bottom
    # ax.set_xlabel('Performance')
    # ax.set_title('How fast do you want to go today?')
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    # plt.show()
    return 'data:image/png;base64,{}'.format(graph_url)


def build_barchart_horizz(people, values):
    img = io.BytesIO()

    # Fixing random state for reproducibility
    np.random.seed(19680801)
    plt.rcdefaults()
    fig, ax = plt.subplots()

    # Example data
    people = ('Tom', 'Dick', 'Harry', 'Slim', 'Jim')
    y_pos = np.arange(len(people))
    values = 3 + 10 * np.random.rand(len(people))
    error = np.random.rand(len(people))

    N = 5
    menMeans = (20, 35, 30, 35, 27)
    womenMeans = (25, 32, 34, 20, 25)
    menStd = (2, 3, 4, 1, 2)
    womenStd = (3, 5, 2, 3, 3)
    ind = np.arange(N)    # the x locations for the groups
    width = 0.35       # the width of the bars: can also be len(x) sequence

    p1 = plt.bar(ind, menMeans, width, yerr=menStd)
    p2 = plt.bar(ind, womenMeans, width, bottom=menMeans, yerr=womenStd)

    plt.ylabel('Scores')
    plt.title('Scores by group and gender')
    plt.xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5'))
    plt.yticks(np.arange(0, 81, 10))
    plt.legend((p1[0], p2[0]), ('Men', 'Women'))

    # plt.show()

    # ax.barh(y_pos, values, xerr=error, align='center', color='green', ecolor='black')
    # ax.set_yticks(y_pos)
    # ax.set_yticklabels(people)
    # ax.invert_yaxis()  # labels read top-to-bottom
    # ax.set_xlabel('Performance')
    # ax.set_title('How fast do you want to go today?')
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    # plt.show()
    return 'data:image/png;base64,{}'.format(graph_url)


def xbuild_barchart_vert(people, values):
    img = io.BytesIO()
    men_means, men_std = (20, 35, 30, 35, 27), (2, 3, 4, 1, 2)
    women_means, women_std = (25, 32, 34, 20, 25), (3, 5, 2, 3, 3)

    ind = np.arange(len(men_means))  # the x locations for the groups
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - width/2, men_means, width, yerr=men_std, color='SkyBlue', label='Men')
    rects2 = ax.bar(ind + width/2, women_means, width, yerr=women_std, color='IndianRed', label='Women')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.set_xticks(ind)
    ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))
    ax.legend()
    autolabel(ax, rects1, "left")
    autolabel(ax, rects2, "right")
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    # plt.show()
    return 'data:image/png;base64,{}'.format(graph_url)


def autolabel(ax, rects, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height, '{}'.format(height), ha=ha[xpos], va='bottom')
    return ax


def build_graph0(x_coordinates, y_coordinates):
    img = io.BytesIO()
    plt.plot(x_coordinates, y_coordinates, label='visits')
    plt.xlabel('date')
    plt.ylabel('visits')
    plt.title("visits per day")
    plt.legend()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    #x = np.linspace(0, 2, 100)
    ##plt.plot(x, x, label='linear')
    #plt.plot(x, x**2, label='quadratic')
    #plt.plot(x, x**3, label='cubic')


# Minimal code:

# import asyncio
# import matplotlib
# matplotlib.use('TkAgg')
# import tkinter as tk
# from tkinter import ttk
# from skimage._shared._tempfile import temporary_file
# import numpy as np


# @asyncio.coroutine
# def _async(func, *args):
#     loop = asyncio.get_event_loop()
#     return (yield from loop.run_in_executor(None, func, *args))


# STANDARD_MARGIN = (3, 3, 12, 12)


# def long_computation():
#     import time
#     time.sleep(4)
#     import matplotlib.pyplot as plt
#     fig, ax = plt.subplots()
#     ax.imshow(np.random.rand(500, 500))
#     with temporary_file(suffix='.png') as fname:
#         fig.savefig(fname)


# class MainWindow(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title('I gonna die')
#         main = ttk.Frame(master=self, padding=STANDARD_MARGIN)
#         main.grid(row=0, column=0, sticky='nsew')
#         fsync = long_computation
#         fasync = lambda: asyncio.ensure_future(_async(long_computation))
#         button = ttk.Button(master=main, padding=STANDARD_MARGIN,
#                             text='Run stuff',
#                             command=fasync)
#         button.grid(row=0, column=0)
#         main.pack()


# def tk_update(loop, app):
#     try:
#         app.update()
#     except tk.TclError as e:
#         loop.stop()
#         return
#     loop.call_later(.01, tk_update, loop, app)


# def main():
#     loop = asyncio.get_event_loop()
#     app = MainWindow()
#     #app.mainloop()
#     tk_update(loop, app)
#     loop.run_forever()


# if __name__ == '__main__':
#     main()
