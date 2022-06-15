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
netcdf-geojson-vectors.py
================

Convert CF-compliant NetCDF files with vector attributes to GeoJSON
"""
import argparse
import os
import geopandas
import xarray as xr
from pathlib import Path


def netcdf2geojson(config_file, input_file, output_dir):

    if os.path.exists(output_dir) is False:
        os.makedirs(output_dir)

    output_file = output_dir + '/' + Path(input_file).stem + '.json'
    print(f'Reading {input_file}')
    local_dataset = xr.open_dataset(input_file)
    df = local_dataset.to_dataframe()
    df = df.dropna(how='any', axis=0).reset_index()
    df['lon'] = (df['lon'] + 180) % 360 - 180
    print(df)

    data = {'u': df.u,
            'v': df.v}

    print('Converting to GeoJSON')
    gdf = geopandas.GeoDataFrame(data, geometry=geopandas.points_from_xy(df.lon, df.lat))
    print(gdf)

    print(f'Writing {output_file}')
    gdf.to_file(f'{output_file}', driver="GeoJSON")
    print(f'Created {output_file}')


parser = argparse.ArgumentParser(description='Convert CF-compliant NetCDF files with vector attributes to GeoJSON.')
parser.add_argument(
    '-c',
    '--config_file',
    dest='config_file',
    action='store',
    help='Configuration file')
parser.add_argument(
    '-i',
    '--input_file',
    dest='input_file',
    help='Input file',
    action='store')
parser.add_argument(
    '-o',
    '--output_dir',
    default='./output',
    dest='output_dir',
    help='Output directory',
    action='store')


args = parser.parse_args()

netcdf2geojson(args.config_file,
               args.input_file,
               args.output_dir)
