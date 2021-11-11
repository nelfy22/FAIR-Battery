#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

input_filepath = r"test.csv"
output_filepath = r"overpotential_result.jpg"
show_plot = True

data = np.genfromtxt(input_filepath, delimiter=',', skip_header=1)
data = data[~(~np.isfinite(data)).any(axis=1)]  # Discard a few NaNs


def soc(time, voltage, current):
    charge = np.empty_like(voltage)
    charge[0] = 0
    charge[1:] = (np.diff(time) * (current[:-1] + current[1:]) / 2).cumsum()
    soc = charge / abs(charge[-1])
    return soc if soc[-1] > 0 else soc + 1


def fit_voltage_over_soc(time, voltage, current, mode, mode_target, bins=200):
    mode_mask = mode == mode_target
    if mode_mask.sum() == 0:
        raise ValueError(f"mode {mode_target} not found in mode list")

    time = time[mode_mask]
    voltage = voltage[mode_mask]
    current = -current[mode_mask]

    the_soc = soc(time, voltage, current)
    # We resample the data linearly over SoC by averaging over bins
    if mode_target in [2, 4]:  # Charging
        bin_edges = the_soc.searchsorted(np.linspace(0, 1, num=bins + 1))
    else:  # Discharging: make soc ascending for searchsorted
        bin_edges = -1 - np.flip(the_soc).searchsorted(np.linspace(0, 1, num=bins + 1))
    mean_voltages = np.empty(bins)
    for i in range(bins):
        if mode_target in [2, 4]:
            bin_slice = slice(bin_edges[i], bin_edges[i + 1])
        else:
            bin_slice = slice(bin_edges[i + 1], bin_edges[i])

        bin_voltages = voltage[bin_slice]
        bin_socs = the_soc[bin_slice]
        if bin_voltages.size > 0:
            # The mean voltage is obtained by integrating and dividing by the domain
            voltage_int = np.trapz(bin_voltages, bin_socs)
            mean_voltages[i] = voltage_int / (bin_socs[-1] - bin_socs[0])
        else:
            # The voltage is assumed equal to the closest value
            # TODO: Interpolate between nearest available values
            mean_voltages[i] = voltage[bin_edges[i]]
    return mean_voltages


def get_soc_bins(bins=200):
    return np.linspace(0, 1, num=bins, endpoint=False) + 0.5 / bins


soc_bins = get_soc_bins()
voltage_mode2 = fit_voltage_over_soc(*data.T, 2)
voltage_mode3 = fit_voltage_over_soc(*data.T, 3)
emf = (voltage_mode2 + voltage_mode3) / 2

voltage_mode4 = fit_voltage_over_soc(*data.T, 4)
voltage_mode5 = fit_voltage_over_soc(*data.T, 5)
overpotential_charging = voltage_mode4 - emf
overpotential_discharging = voltage_mode5 - emf

plt.axhline(0, c='k')
plt.plot(soc_bins * 100, overpotential_charging, 'k', label="Charging 0.5 C")
plt.plot(soc_bins * 100, overpotential_discharging, '--k', label="Discharging 0.5 C")
plt.xlim(100, 0)
plt.xlabel("State of Charge (%)")
plt.ylabel("Overpotential (V)")
plt.legend()
if output_filepath:
    plt.savefig(output_filepath, dpi=100)
if show_plot:
    plt.show()
