# NetCDF to GeoJSON Vectors

Convert CF-compliant NetCDF files with vector attributes (u, v, magnitude, direction) to GeoJSON.

## Usage

Install Python requirements:

`pip install -r requirements.txt`

### Arguments

```
netcdf_to_geojson_vectors.py [-h] [-c CONFIG_FILE] [-d INPUT_DIR] [-i INPUT_FILE] [-m MAX_RECORDS] [-o OUTPUT_DIR]
```

```
  -h, --help            Show this help message and exit
  -c CONFIG_FILE, --config_file CONFIG_FILE
                        Configuration file
  -d INPUT_DIR, --input_dir INPUT_DIR
                        Directory containing input files
  -i INPUT_FILE, --input_file INPUT_FILE
                        Input file
  -m MAX_RECORDS, --max_records MAX_RECORDS
                        Maximum number of records to process
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Output directory
```

## Example

```shell
./netcdf_to_geojson_vectors.py -c sample_oscar.cfg -i ./data/oscar_currents_final_20200101.nc -o output/
```

## Configuration Options

* latVar: Name of the `latitude` variable in the source data file
* lonVar: Name of the `longitude` variable in the source data file
* magnitudeVar: Name of the `magnitude` variable in the source data file
* directionVar: Name of the `direction` variable in the source data file
* uVar: Name of the `u` variable in the source data file
* vVar: Name of the `v` variable in the source data file
* convertUV: Convert `u` and `v` components to `magnitude` and `direction`
* convertMagDir: Convert `magnitude` and `direction` components to `u` and `v`
* is360: Convert extents from `0 - 360` to `-180 - 180`
* extraVars: An array of extra variables to include with the GeoJSON output
