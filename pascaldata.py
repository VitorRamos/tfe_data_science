# -*- coding: utf-8 -*-
"""
    Module with Classes that generates xArray DataArray
    with processed data from applications execution.
"""

import json
import os
from collections import defaultdict
from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List, Callable

import numpy as np


class PascalData:
    """
    Class that store parsec run measures values

        Atrributes
            config - The metadata about execution informations
            measures - Resume dictionary with all measures times

        Methods
            loadata()
            save_data()
            times()
            speedups()
            plot2D()
            plot3D

    """

    def __init__(self, filename: str = None):
        """
        Create a empty object or initialized of data from a file saved
        with save_data method.

        :param filename: File name that store measures
        """
        self.config = {}
        self.data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        if filename:
            self.load_data(filename)
        return

    def __str__(self):
        """
        Default output string representation of class

        :return: specific formated string
        """

        if not self.config:
            return "No data"
        return (
            f"Package: {self.config['pkg']}\n"
            #f"Date: {self.config['execdate']}\n"
            #f"Command: {self.config['command']}"
        )

    def load_data(self, filename: str):
        """
        Read a file previously saved with method save_data() and initialize
        the object class dictionaries.

        :param filename: Filename with data dictionary of execution times.
        """

        # TODO should we raise on error ?
        if os.path.isfile(filename):
            with open(filename) as f:
                datadict = json.load(f)
            if "config" in datadict:
                self.config = datadict["config"]
            else:
                print("Warning: No config found")
            if "data" in datadict:
                self.data = datadict["data"]
            else:
                print("Warning: No data loaded")
        else:
            print("Error: File not found")
        return

    def save_data(self, filename: str = None):
        """
        Write to file the measures information stored on object class

        :param filename: Filename to save on.
        :return:
        """

        if filename is None:
            filedatename = self.config["execdate"]
            filename = os.path.basename(self.config["pkg"]).split(" ")[0]
            filename += "_datafile_" + filedatename + ".json"
        with open(filename, "w") as f:
            dictsave = {"config": self.config, "data": self.data}
            json.dump(dictsave, f, ensure_ascii=False)
        return dictsave

    def measures_build(self, keys: List[Any], subkey: str, data: List[Any],
                       subvalue: str = None):
        """
        Resume all tests, grouped by keys in a dictionary.

        Dictionary format
            {"keys_1":{"subkey":data,...},...}
            {"keys_1":{"subkey":{"subvale":[data,...]},...},...}

        :param keys: Current configuration
        :param subkey: Group of data
        :param [subvalue]: Subgroup of data
        :param data: data to store
        :return:
        """
        keys = filter(lambda x: x is not None, keys)
        keys = map(str, keys)
        if subvalue is not None:
            self.data[";".join(keys)][subkey][subvalue].append(data)
        else:
            self.data[";".join(keys)][subkey] = data

    def dataframe_generic(self, set_index: bool = False):
        """
        Create dataframe with all generic data (not in subgroups)

        format:
            key_1, key_2, ... generic_1, generic_2

        :param setindex: set dataframe index
        :return: dataframe
        """
        import pandas as pd
        df = []
        cols = self.config["data_descriptor"]["values"]
        for config, data in self.data.items():
            # if not "region" in data: break
            cfg = config.split(";")
            for c in cols:
                cfg += [data[c]]
            df.append(cfg)
        indx= self.config["data_descriptor"]["keys"]
        df = pd.DataFrame(df, columns=indx+list(cols))
        if set_index:
            df = df.set_index(indx)
        return df

    def dataframe_group(self, subkey: str, transform: Callable = None,
                        set_index: bool = False):
        """
        Create dataframe with all specific data (inside subgroup)

        format:
            key_1, key_2, ... subgroup, subgroup_key1, subgroup_key2, ...

        :param subkey: group name
        :param transform: applied to each sensor data to create the rows
        :param setindex: set dataframe index
        :return: dataframe
        """
        if not "extras" in self.config["data_descriptor"]:
            raise Exception("No extra data")
        if not subkey in self.config["data_descriptor"]["extras"]:
            raise Exception("Invalid subkey")
        import pandas as pd

        if transform is None:
            def transform(x): return list(map(list, zip(*x)))
        df = []
        for config, data in self.data.items():
            # if not "region" in data: break
            cfg = config.split(";")
            for key, val in data[subkey].items():
                aux = cfg+[key]+transform(val)
                df.append(aux)
        columns= self.config["data_descriptor"]["keys"].copy()
        columns+= [subkey]
        columns+= self.config["data_descriptor"]["extras"][subkey]["values"]
        df = pd.DataFrame(df, columns= columns)
        if set_index:
            df = df.set_index(self.config["keys"]+[subkey])
        return df

    def regions(self, method: str = "minmax", set_index: bool = False):
        """
            Calculates the average of region data and averages between
            runs

            :param method: minmax, maxthread
            :param setindex: set dataframe index
            :return: dataframe
        """
        df = self.data.dataframe_group("region")
        if method == "minmax":
            df["start_time"] = df["start_time"].apply(np.min)
            df["stop_time"] = df["stop_time"].apply(np.max)
            df["elaped_time"] = df["stop_time"]-df["start_time"]
        elif method == "maxthread":
            df["start_time"] = df["start_time"].apply(np.array)
            df["stop_time"] = df["stop_time"].apply(np.array)
            df["elaped_time"] = df["stop_time"]-df["start_time"]

        indx = self.config["keys"]+["region"]
        indx.remove("repetitions")

        df = df.groupby(indx).elaped_time.apply(np.mean).reset_index()

        if method == "maxthread":
            df["elaped_time"] = df["elaped_time"].apply(np.max)

        if set_index:
            df = df.set_index(indx)
        return df

    def energy(self, method: str = "mean", set_index: bool = False,
                     transform: Callable = None):
        """
            Calculates the average of sampled sensor data and averages between
            runs

            :param method: mean, timediff
            :param setindex: set dataframe index
            :param transform: applied to each sensor data to create the rows
            :return: dataframe
        """
        import pandas as pd
        if not "extras" in self.config["data_descriptor"] or \
            not "sensors" in self.config["data_descriptor"]["extras"]:
            indx = self.config["data_descriptor"]["keys"].copy()
            indx.remove("repetitions")
            df_general = self.dataframe_generic()
            df_general = df_general.groupby(indx).mean().reset_index()
            if not any(["rapl" in s or
                        "ipmi" in s for s in df_general.columns]):
                raise Exception("No energy sensor present (rapl, ipmi)")
            if set_index:
                df_general = df_general.set_index(indx)
            return df_general

        df_general = self.dataframe_generic()
        df_sensor = self.dataframe_group("sensors",transform=transform)
        df_sensor = df_sensor[df_sensor["sensors"].str.contains("rapl") |
                              df_sensor["sensors"].str.contains("ipmi")]
        if df_sensor.empty:
            raise Exception("No energy sensor present (rapl, ipmi)")
        indx = self.config["data_descriptor"]["keys"]+["sensors"]
        indx.remove("repetitions")
        if method == "mean":
            # compute the mean power in the execution
            df_sensor["info"] = df_sensor["info"].apply(np.mean)
        elif method == "timediff":
            from functools import partial
            # uses the time diff to calculate the energy
            df_sensor["time"] = df_sensor["time"].apply(partial(np.diff,
                                                                prepend=[0]))
            # df_sensor["info"]= df_sensor["info"].apply(lambda x: x[:-1])
            df_sensor["info"] = df_sensor["time"]*df_sensor["info"]
            df_sensor["info"] = df_sensor["info"].apply(np.sum)
            df_sensor = df_sensor.drop(columns=["time"])
        # compute the mean power between runs
        df_sensor = df_sensor.groupby(indx).mean().reset_index()
        # pivot sensor table
        indx.remove("sensors")
        sensors = df_sensor["sensors"].unique()
        df_sensor = pd.pivot_table(df_sensor, index=indx,
                                   columns="sensors", values="info",
                                   aggfunc=np.min).reset_index()

        # compute the mean time between runs
        df_general = df_general.groupby(indx).mean().reset_index()
        # merge with table with general data
        df_sensor = pd.merge(df_sensor, df_general)

        if method == "mean":
            # compute energy
            col_rename = {sen: f"{sen}_power" for sen in sensors}
            df_sensor = df_sensor.rename(columns=col_rename)
            for sen in sensors:
                df_sensor[f"{sen}_energy"] = df_sensor[f"{sen}_power"] * \
                    df_sensor["total_time"]

        if set_index:
            df_sensor = df_sensor.set_index(indx)

        return df_sensor

    def times(self, set_index: bool= False):
        """
        Return DataArray (xarray) with resume of all tests.

        DataArray format
            dims(frequency, size, cores)
            data=numpy array with median of measures times.

        :param setindex: set dataframe index
        :return: DataArray with median of measures times.
        """
        indx = self.config["data_descriptor"]["keys"].copy()
        indx.remove("repetitions")
        df_general = self.dataframe_generic()
        df_general = df_general.groupby(indx).mean().reset_index()
        if set_index:
            df_general = df_general.set_index(indx)
        return df_general

    def threads(self):
        """
        Return a xArray DataArray with resume of all threads,
        grouped by frequency, input size and number of cores.

        :return: dataframe with median of measures times.
        """
        import xarray as xr
        data = xr.DataArray([])
        return data

    def speedups(self):
        """
        Return DataArray (xarray) with resume of all speedups.

        DataArray format
            dims(frequency, size, cores)
            data=numpy array with calculated speedups.

        :return: DataArray with calculated speedups.
        """
        import xarray as xr
        data = xr.DataArray([])
        return data

    def efficiency(self):
        """
        Return DataArray (xarray) with resume of all efficiencies.

        DataArray format
            dims(frequency, size, cores)
            data=numpy array with calculated efficiencies.

        :return: DataArray with calculated efficiencies.
        """
        speedups = self.speedups()
        xefficency = speedups/speedups.coords["cores"]
        xefficency.attrs = speedups.attrs
        return xefficency

    @staticmethod
    def plot2D(data, title: str = "", 
                greycolor: bool = False, filename: str = ""):
        """
        Plot the 2D (Speedup x Cores) lines graph.

        :param data: DataArray to plot, generate by speedups(),
                     times() or efficiency().
        :param title: Plot Title.
        :param greycolor: If set color of graph to grey colormap.
        :param filename: File name to save figure (eps format).
        :return:
        """
        import matplotlib.pyplot as plt
        from matplotlib import cm
        from matplotlib import ticker

        if not data.size == 0:
            if len(data.dims) != 2:
                print("Error: Do not possible plot 3-dimensions data")
                return
            _, ax = plt.subplots()
            xs = data.coords["cores"].values
            if "size" in data.dims:
                datalines = data.coords["size"].values
                #xc_label = "Input Size"
            elif "frequency" in data.dims:
                datalines = data.coords["frequency"].values
                #xc_label = "Frequency"
            if greycolor:
                colors = plt.cm.Greys(
                    np.linspace(0, 1, len(datalines) + 10))
                colors = colors[::-1]
                colors = colors[:-5]
            else:
                colors = plt.cm.jet(np.linspace(0, 1, len(datalines)))
            for i, d in enumerate(datalines):
                if "size" in data.dims:
                    ys = data.sel(size=d)
                    legendtitle = "Sizes"
                    legendlabel = d
                elif "frequency" in data.dims:
                    ys = data.sel(frequency=d)
                    legendtitle = "Frequencies"
                    legendlabel = d
                ax.plot(xs, ys, "-", linewidth=2, color=colors[i],
                                label="Speedup for %s" % legendlabel)
            ax.legend(loc="lower right", title=legendtitle)
            ax.set_xlabel("Number of Cores")
            ax.set_xlim(0, xs.max())
            ax.xaxis.set_major_locator(ticker.MultipleLocator(2.0))
            ax.set_ylabel("Speedup")
            ax.set_ylim(0, data.max().max()+1)
            ax.yaxis.set_major_locator(ticker.MultipleLocator(1.0))
            plt.title(title)
            if filename:
                plt.savefig(filename, dpi=1000)
            plt.show()
        else:
            print("Error: Do not possible plot data without "
                  "speedups information")

    @staticmethod
    def plot3D(data, slidername: str = None, title: str = "Speedup Surface",
               zlabel: str = "speedup", greycolor: bool = False, filename: str = ""):
        """
        Plot the 3D (Speedup x cores x input size) surface.

        :param data: DataArray to plot, generate by speedups(),
                     times() or efficiency().
        :param slidername: name of dimension of DataArray to use on slider.
        :param title: Plot Title.
        :param zlabel: Z Axis Label.
        :param greycolor: If set color of graph to grey colormap.
        :param filename: File name to save figure (eps format).
        :return:
        """

        try:
            from mpl_toolkits.mplot3d import Axes3D
        except ImportError:
            print("Warning: No 3D plot support."
                  "Please install matplotlib with Axes3D toolkit")
            return
        import matplotlib.pyplot as plt
        from matplotlib.widgets import Slider, RadioButtons
        from matplotlib import cm
        from matplotlib import ticker

        def update_plot3D(idx):
            ax.clear()
            if idx is None:
                dataplot = data
                if "size" in data.dims:
                    xc = data.coords["size"].values
                    xc_label = "Input Size"
                elif "frequency" in data.dims:
                    xc = [i*1000 for i in data.coords["frequency"].values]
                    xc_label = "Frequency"
            else:
                if slidername is "size":
                    dataplot = data.sel(size=int(idx))
                    xc = [i*1000 for i in dataplot.coords["frequency"].values]
                    xc_label = "Frequency"
                elif slidername is "frequency":
                    dataplot = data.sel(frequency=float(idx))
                    xc = dataplot.coords["size"].values
                    xc_label = "Input Size"
            yc = dataplot.coords["cores"].values
            X, Y = np.meshgrid(yc, xc)
            Z = dataplot.values
            zmin = data.values.min()
            zmax = data.values.max()
            ax.plot_surface(Y, X, Z, cmap=colormap,
                            linewidth=0.5, edgecolor="k",
                            linestyle="-",
                            vmin=(zmin - (zmax - zmin) / 10),
                            vmax=(zmax + (zmax - zmin) / 10))
            ax.tick_params(labelsize="small")
            ax.set_xlabel(xc_label)
            if xc_label is "Frequency":
                ax.xaxis.set_major_formatter(ticker.EngFormatter(unit="Hz"))
            ax.set_ylabel("Number of Cores")
            ax.set_zlabel(zlabel)
            ax.set_zlim(0, 1.10 * zmax)
            fig.canvas.draw_idle()

        fig = plt.figure()
        ax = fig.gca(projection="3d")
        plt.title(title)
        if greycolor:
            colormap = cm.Greys
        else:
            colormap = cm.coolwarm

        if not data.size == 0:
            if len(data.dims) == 2:
                idx = None
            elif len(data.dims) == 3:
                if slidername in ("size", "frequency"):
                    rax = plt.axes([0.01, 0.01, 0.17,
                                    len(data.coords[slidername].values)*0.04],
                                   facecolor="lightgoldenrodyellow")
                    raxtxt = [str(i) for i in
                              data.coords[slidername].values]
                    idx = str(data.coords[slidername].values[0])
                    radio = RadioButtons(rax, tuple(raxtxt))
                    for circle in radio.circles:
                        circle.set_radius(0.03)
                    radio.on_clicked(update_plot3D)
                else:
                    print("Error: Not possible plot data with wrong "
                          "axis names")
                    return
            else:
                print("Error: Not possible plot data with wrong "
                      "number of axis")
                return
            update_plot3D(idx)
            if filename:
                plt.savefig(filename, dpi=1000)
            plt.show()
        else:
            print("Error: Not possible plot data without "
                  "speedups information")
