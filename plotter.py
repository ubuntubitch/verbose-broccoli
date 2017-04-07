# -*- coding: utf-8 -*-
import json
import sys

import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'serif'


def _has_empty_sets(*args):
    for arg in args:
        arg_set = set(arg)
        if len(arg_set) == 1 and arg_set.pop() is None:
            return True
    return False


def plot_velocity_profiles(loc):
    tag = '%s_velocityProfile' % loc['name']
    print tag

    velocity_profile = loc['children']['velocityProfile'][0]
    vp = velocity_profile['vp']['values']
    vs = velocity_profile['vs']['values']
    depth = velocity_profile['depth']['values']

    if _has_empty_sets(vp, vs, depth):
        return

    fig, (ax1, ax2) = plt.subplots(ncols=2)

    ax1.set_ylabel('Depth (%s)' % velocity_profile['depth']['units'], fontsize='large')
    ax1.set_xlabel('S-Wave V. (%s)' % velocity_profile['vs']['units'], fontsize='large')
    ax1.step(vs, depth, 'bo')
    ax1.xaxis.set_tick_params(labelsize=7)
    ax1.yaxis.set_tick_params(labelsize=7)

    ax2.set_xlabel('P-Wave V. (%s)' % velocity_profile['vp']['units'], fontsize='large')
    ax2.step(vp, depth, 'ro')
    ax2.xaxis.set_tick_params(labelsize=7)
    ax2.yaxis.set_tick_params(labelsize=7)

    fig.savefig('%s.png' % tag)


def plot_dispersion_data(loc):
    tag = '%s_dispersionData' % loc['name']
    print tag

    dispersion_data = loc['children']['dispersionData'][0]
    tdv = dispersion_data['theoreticalDispersionVelocity']['values']
    sdv = dispersion_data['siteDispersionVelocity']['values']
    freq = dispersion_data['frequency']['values']

    if _has_empty_sets(tdv, sdv, freq):
        return

    fig = plt.figure()
    ax = fig.gca()
    ax.plot(freq, tdv, label='Field Ave. Velocity (m/s)')
    ax.plot(freq, sdv, 'm-', label='Inverted Phase Velocity (m/s)')
    ax.plot(freq, sdv, 'k_')
    ax.legend(loc='upper right')
    ax.set_xlabel('Frequency (Hz)', fontsize='large')
    ax.set_ylabel('Phase Velocity (m/s)', fontsize='large')
    ax.xaxis.set_tick_params(labelsize=7)
    ax.yaxis.set_tick_params(labelsize=7)
    fig.savefig('%s.png' % tag)


def plot_lab_test(loc):
    tag = '%s_labTest' % loc['name']
    print tag

    lab_test = loc['children']['geotechnicalData'][0]['children']['labTest'][0]
    # grainSizeDistribution
    grain_size_dist = lab_test['children']['grainSizeDistribution'][0]['grainSize']['values']
    portion_finer = lab_test['children']['grainSizeDistribution'][0]['portionFiner']['values']

    if _has_empty_sets(grain_size_dist, portion_finer):
        return

    fig = plt.figure()
    ax = fig.add_subplot(121)
    ax.plot(grain_size_dist, portion_finer)
    ax.set_xlabel('Grain Size (mm)', fontsize='large')
    ax.set_ylabel('Portion Finer (%)', fontsize='large')
    ax.xaxis.set_tick_params(labelsize=7)
    ax.yaxis.set_tick_params(labelsize=7)

    # nonlinearTest
    ax2 = fig.add_subplot(222)
    ax2.xaxis.set_tick_params(labelsize=7)
    ax2.yaxis.set_tick_params(labelsize=7)
    ax2.set_xlabel('Cyclic Shear Strain')
    ax2.set_ylabel('G/Gmax')
    ax2.grid(True)

    ax3 = fig.add_subplot(224)
    ax3.xaxis.set_tick_params(labelsize=7)
    ax3.yaxis.set_tick_params(labelsize=7)
    ax2.set_xlabel('Cyclic Shear Strain')
    ax2.set_ylabel('Damping Ratio, %')
    ax3.grid(True)

    for prop in lab_test['children']['nonlinearTest']:
        if prop['propertyType'] not in ['G/Gmax', 'Damping']:
            continue
        ax = ax2 if prop['propertyType'] == 'G/Gmax' else ax3
        strain = prop['strain']['values']
        property_ = prop['property']['values']

        if _has_empty_sets(strain, property_):
            continue

        ax.plot(strain, property_)

    fig.savefig('%s.png' % tag)


def plot_field_test(loc):
    tag = '%s_fieldTest' % loc['name']
    print tag

    lab_test = loc['children']['geotechnicalData'][0]['children']['fieldTest'][0]
    # standardPenetrationTest
    blow_count = lab_test['children']['standardPenetrationTest'][0]['Blow count (N)']['values']
    depth_1 = lab_test['children']['standardPenetrationTest'][0]['depth']['values']

    # conePenetrationTest
    sleeve_friction = lab_test['children']['conePenetrationTest'][0]['Sleeve Friction']['values']
    tip_resistance = lab_test['children']['conePenetrationTest'][0]['Tip Resistance']['values']
    pore_pressure = lab_test['children']['conePenetrationTest'][0]['Pore Pressure']['values']
    depth_2 = lab_test['children']['conePenetrationTest'][0]['depth']['values']

    if _has_empty_sets(blow_count, depth_1, sleeve_friction, tip_resistance, pore_pressure, depth_2):
        return

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(ncols=4)
    fig.set_size_inches(8, 5, forward=True)

    ax1.plot(blow_count, depth_1)
    ax1.set_xlabel('SPT', fontsize='10')
    ax1.xaxis.set_label_position('top')
    ax1.xaxis.set_tick_params(labelsize=7)

    ax2.plot(tip_resistance, depth_2, 'r-')
    ax2.set_xlabel('Tip Resistance (kPa)', fontsize='10')
    ax2.xaxis.set_label_position('top')
    ax2.xaxis.set_tick_params(labelsize=7)
    ax2.grid(True)

    ax3.plot(sleeve_friction, depth_2, 'r-')
    ax3.set_xlabel('Sleeve Friction (kPa)', fontsize='10')
    ax3.xaxis.set_label_position('top')
    ax3.xaxis.set_tick_params(labelsize=7)
    ax3.grid(True)

    ax4.plot(pore_pressure, depth_2, 'r-')
    ax4.set_xlabel('Pore Pressure (kPa)', fontsize='10')
    ax4.xaxis.set_label_position('top')
    ax4.xaxis.set_tick_params(labelsize=7)
    ax4.grid(True)

    fig.savefig('%s.png' % tag)


if __name__ == '__main__':
    filename = sys.argv[1] if len(sys.argv) > 1 else 'Robert_Kayen_2013_2.json'
    data = json.load(open(filename))

    for loc in data['location']:
        print 'Plotting %s...' % loc['name']
        plot_velocity_profiles(loc)
        plot_dispersion_data(loc)
        plot_lab_test(loc)
        plot_field_test(loc)
