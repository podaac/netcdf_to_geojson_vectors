#!/usr/bin/env python3

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
================
netcdf_to_geojson_vectors.py
================

Convert CF-compliant NetCDF files with vector attributes to GeoJSON
"""
import argparse
import os
import json
import geopandas
import numpy as np
import xarray as xr
from pathlib import Path


def netcdf2geojson(config_file, input_file, output_dir, max_records=None):
    """Converts NetCDF file to GeoJSON based on config"""
    conf = read_config(config_file)

    # Make sure output path exists
    if os.path.exists(output_dir) is False:
        os.makedirs(output_dir)
    output_file = Path(output_dir).joinpath(Path(input_file).stem + '.json')
    print(f'Reading {input_file}')

    # Read dataset and remove nan values
    local_dataset = xr.open_dataset(input_file)
    df = local_dataset.to_dataframe()
    df = df.dropna(how='any', axis=0).reset_index()

    # Limit records (generally for testing)
    if max_records is not None:
        df = df[0: int(max_records)]

    # Convert extents from 0 - 360 to -180 - 180
    if conf['is360'] is True:
        df[conf['lonVar']] = (df[conf['lonVar']] + 180) % 360 - 180

    print(df)
    data = {}

    # Set output values for speed dire
    if conf.get('speedVar') and conf.get('dirVar'):
        print('Using speedVar and dirVar')
        data['speed'] = df[conf['speedVar']]
        data['dir'] = df[conf['dirVar']]

    # Convert u and v components to speed and dir if desired
    if conf.get('uVar') and conf.get('vVar'):
        if conf['convertUV'] is True:
            print('Calculating speed and direction from uVar and vVar')
            data['speed'] = df.apply(lambda x: uv2speed(x[conf['uVar']], x[conf['vVar']]), axis=1)
            data['dir'] = df.apply(lambda x: uv2dir(x[conf['uVar']], x[conf['vVar']]), axis=1)
        else:
            print('Using uVar and vVar')
            data['u'] = df[conf['uVar']]
            data['v'] = df[conf['vVar']]

    # Convert to geopandas dataframe
    print('Converting to GeoJSON')
    gdf = geopandas.GeoDataFrame(data, geometry=geopandas.points_from_xy(df[conf['lonVar']], df[conf['latVar']]))
    print(gdf)

    # Use geopandas to write out dataframe as GeoJSON
    print(f'Writing {output_file}')
    gdf.to_file(f'{output_file}', driver="GeoJSON")
    print(f'Created {output_file}')


def read_config(config_file):
    """
    Parses a JSON dataset config file
    Parameters
    ----------
    config_file = path to configuration file
    """
    config = None
    with open(config_file) as config_f:
        config = json.load(config_f)
    return config


def uv2dir(u, v):
    """
    Calculates direction from u and v components
    Parameters
    ----------
    u = west/east direction
    v = south/north direction
    """
    dir = (270 - np.rad2deg(np.arctan2(v, u))) % 360
    return dir


def uv2speed(u, v):
    """
    Calculates speed from u and v components
    Parameters
    ----------
    u = west/east direction
    v = south/north direction
    """
    speed = np.sqrt(np.square(u) + np.square(v))
    return speed


parser = argparse.ArgumentParser(description='Convert CF-compliant NetCDF files with vector attributes to GeoJSON.')
parser.add_argument(
    '-c',
    '--config_file',
    dest='config_file',
    action='store',
    help='Configuration file')
parser.add_argument(
    '-d',
    '--input_dir',
    dest='input_dir',
    help='Directory containing input files',
    action='store')
parser.add_argument(
    '-i',
    '--input_file',
    dest='input_file',
    help='Input file',
    action='store')
parser.add_argument(
    '-m',
    '--max_records',
    dest='max_records',
    help='Maximum number of records to process',
    action='store')
parser.add_argument(
    '-o',
    '--output_dir',
    default='./output',
    dest='output_dir',
    help='Output directory',
    action='store')

args = parser.parse_args()
if args.input_dir:
    input_files = Path(args.input_dir).glob('*.nc')
    for input_file in input_files:
        netcdf2geojson(args.config_file,
                       input_file,
                       args.output_dir,
                       args.max_records)
else:
    netcdf2geojson(args.config_file,
                   args.input_file,
                   args.output_dir,
                   args.max_records)
