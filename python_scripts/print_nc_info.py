def print_nc_info(top_dir, model, var, lat_name, lon_name):

    data_dir = os.path.join(top_dir, model)
    print('************************************************************')
    print('begin examining {} model'.format(model))

    print('begin examining {} nc files'.format(var))

    files = glob.glob(os.path.join(data_dir, var + '*.nc'))

    file = files[0] # print only the nc information of the first month of 1982 of every model
    print('file name: ', file)

    nc_file = xr.open_dataset(file)
    nc_data = nc_file[var].isel(time=0)
    unit = nc_file[var].attrs['units']

    print('unit: ', unit)

    print('data shape: ', nc_data.shape)

    nan_sum = np.where(np.isnan(nc_data))[0].size
    nan_per = nan_sum / nc_data.size * 100

    print('{} Nan values, accounting for {} %'.format(nan_sum, nan_per))

    nmax = np.nanmax(nc_data)
    nmin = np.nanmin(nc_data)
    nmean = np.nanmean(nc_data)

    print('maximum value with nan values: ',nmax)
    print('minimum value with nan values: ',nmin)
    print('mean value with nan values: ',nmean)

    print('------------------------------------------------------')

    print('grid info:')
    lat = nc_file.variables[lat_name][:]
    lon = nc_file.variables[lon_name][:]
    print('latitude: ', lat)
    print('longitude: ', lon)
    return nan_sum, nan_per, nmax, nmin, nmean, nc_data.shape, nc_data.size, unit

def main(experiment):
    log_dir = './log'

    make_print_to_file(log_dir, 'check_values_info_0627_{}.py'.format(experiment))

    model_list = ['CMCC-ESM2', 'IPSL-CM6A-LR', 'MIROC6', 'CESM2', 'CNRM-CM6-1', 'MPI-ESM1-2-LR', 'EC-Earth3']
    var_list = ['hfls', 'evspsbl', 'mrso', 'pr', 'tas']
    var_table = ['Amon', 'Amon', 'Lmon', 'Amon', 'Amon']

    top_dir = '../DATA_org/'
    lat_name = 'lat'
    lon_name = 'lon'


    if experiment == 'amip-lfmip-pdLC':
        dir_all = os.path.join(top_dir, 'LFMIP-pdLC')
        op_dir = '../outputs_info/'
        member_id = 'r1i1p1f2'
    else:
        dir_all = os.path.join(top_dir, 'historical')
        op_dir = top_dir
        member_id = 'r1i1p1f1'


    file_info = pd.DataFrame(
        columns=['model', 'var', 'nan_sum', 'nan_per', 'nmin', 'nmax', 'nmean', 'unit', 'shape', 'size'])
    row_idx = -1

    for idx, model in enumerate(model_list):
        for var in var_list:
            if experiment == 'amip-lfmip-pdLC' and model == 'MIROC6' and var == 'hfls':
                print('no such file !')
                continue
            row_idx += 1
            nan_sum, nan_per, nmax, nmin, nmean, shape, size, unit = \
                print_nc_info(var_dir, model, var, lat_name, lon_name)
            file_info.loc[row_idx, :] = model, var, nan_sum, nan_per, nmin, nmax, nmean, unit, shape, size

    file_info.to_csv(os.path.join(op_dir,'{}_file_info.csv'.format(experiment)))


if __name__ == '__main__':
    import os
    import glob
    import numpy as np
    import pandas as pd
    import xarray as xr
    from print_logging import *

    log_dir = './log'


  


    lfmip_file_info = pd.DataFrame(columns=['model','var','nan_sum','nan_per','nmax','nmin','nmean','unit','shape','size'])
    row_idx = -1

    
            # if model == 'MIROC6' and var == 'hfls':
            #     print('no such file !')
            #     continue
            row_idx += 1
            nan_sum, nan_per, nmax, nmin, nmean, shape, size, unit = print_nc_info(top_dir, model, var, lat_name, lon_name)
            lfmip_file_info.loc[row_idx,:] = model, var, nan_sum, nan_per, nmax, nmin, nmean, unit, shape, size

    # lfmip_file_info.to_csv('/mnt/hgfs/F/Data/Original/CMIP6/LFMIP-pdLC/scripts/lfmip_file_info.csv')
    lfmip_file_info.to_csv('cmip6hist_info.csv')