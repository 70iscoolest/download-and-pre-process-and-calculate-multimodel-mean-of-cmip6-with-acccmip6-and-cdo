
def create_nc_file(op_ncfilename, ref_nc, arr, latname, lonname):
    ref_lat = ref_nc.variables[latname][:].data
    ref_lon = ref_nc.variables[lonname][:].data

    ref_time = ref_nc.variables['time'][:].data
    # date = num2date(ref_time[0,], units=ref_nc.variables['time'].units, calendar=ref_nc.variables['time'].calendar)
    # time = np.array(date,dtype='datetime64[s]')
    # time =
    # print(date)
    # print(time)

    mean_nc = nc.Dataset(op_ncfilename, "w", format="NETCDF4")
    mean_nc.createDimension("latitude", len(ref_lat))
    mean_nc.createDimension("longitude", len(ref_lon))
    mean_nc.createDimension("time", 1)

    mean_nc.createVariable("latitude", "f", ("latitude"))
    mean_nc.createVariable("longitude", "f", ("longitude"))
    settime = mean_nc.createVariable("time", ref_nc.variables['time'].datatype,
                                  ref_nc.variables['time'].dimensions)
    settime.units = ref_nc.variables['time'].units
    settime.longname = 'time'


    mean_nc.createVariable(varname=var, datatype="f", dimensions = ("time", "latitude", "longitude"), fill_value=1.e20)

    mean_nc.variables["latitude"][:] = ref_lat
    mean_nc.variables["longitude"][:] = ref_lon

    mean_nc.variables["time"][:] = ref_time

    mean_nc.variables[var][:] = arr


    mean_nc.close()


def multi_model_mean(data_topdir, experiment, experiment_dir ,var, model_list, year, mon, latname, lonname):


    data_dir = os.path.join(data_topdir ,experiment_dir)
    data_vardir = os.path.join(data_dir, var)
    data_splitdir = os.path.join(data_vardir, 'split')

    temp = ma.empty(shape=(len(model_list), 90, 180), dtype=np.float32)

    idx = -1
    for model in model_list:
        if model == 'MIROC6' and experiment == 'lfmip' and var == 'hfls':
            continue

        idx += 1

        model_dir = os.path.join(data_splitdir, model)
        filename = os.path.join(model_dir, '{}_{}_{}_{}.nc'.format(var, model, experiment, str(year) +mon))
        nc_file = nc.Dataset(filename)
        print(filename)

        MA = nc_file.variables[var].missing_value
        print(MA)

        data = nc_file.variables[var][0,] #masked array
        print(np.min(data))
        print(np.max(data))
        print(np.mean(data))

        temp[idx,] = data

        nc_file.close()
    concat_arr = ma.masked_values(temp, 1.e20)
    mean_arr = np.mean(concat_arr, axis=0, dtype=np.float32)

    arr = np.array(mean_arr)
    arr[arr == 1.e20] = np.nan

    ref_filename = os.path.join(model_dir, '{}_{}_{}_{}.nc'.format(var, model, experiment,str(year)+mon))
    ref_file = nc.Dataset(ref_filename)

    data_opdir = os.path.join(data_vardir, 'multimodel_mean')
    if not os.path.exists(data_opdir):
        os.mkdir(data_opdir)

    data_ncopdir = os.path.join(data_opdir,'nc')
    data_npopdir = os.path.join(data_opdir, 'numpy')

    if not os.path.exists(data_ncopdir):
        os.mkdir(data_ncopdir)

    if not os.path.exists(data_npopdir):
        os.mkdir(data_npopdir)

    op_ncfilename = os.path.join(data_ncopdir, '{}_{}_{}_{}.nc'.format(var, 'mean', experiment, str(year) + mon))
    op_npfilename = os.path.join(data_npopdir, '{}_{}_{}_{}.npy'.format(var, 'mean', experiment, str(year) + mon))
    create_nc_file(op_ncfilename, ref_file, mean_arr, latname, lonname)

    np.save(op_npfilename, arr)
    print('******************************************************************************************************')
    #CESM2 CMCC-ESM2 CNRM-CM6-1 IPSL-CM6A-LR MIROC6 MPI-ESM1-2-LR EC-Earth3




if __name__ == '__main__':
    import os
    import glob
    import numpy as np
    import numpy.ma as ma
    import netCDF4 as nc
    from cftime import num2date
    from print_logging import *
    # import pandas as pd
    # import xarray as xr
    # import itertools


    make_print_to_file('./log' ,'multimodel_mean_0628.py')
    data_topdir = '../DATA_process/'
    # data_opdir = '../DATA_analysis/'
    experiment = 'hist'
    experiment_dir = 'historical'
    # experiment = 'lfmip'
    # experiment_dir = 'LFMIP-pdLC'

    model_list = ['CMCC-ESM2', 'IPSL-CM6A-LR', 'MIROC6', 'CESM2', 'CNRM-CM6-1', 'MPI-ESM1-2-LR', 'EC-Earth3']
    var_list = ['hfls', 'evspsbl', 'mrso', 'pr', 'tas']
    # var_table = ['Amon', 'Amon', 'Lmon', 'Amon', 'Amon']
    # var_list = ['mrso', 'evspsbl']
    # var_list = ['hfls', 'pr', 'tas']

    # var_table = ['Lmon','Amon', ]

    year_range = [x for x in range(1982,2014+1)]
    mon_list = ['01','02','03','04','05','06','07','08','09','10','11','12']
    mon_range = [y for y in range(1,12+1)]
    latname = 'lat'
    lonname = 'lon'

    for var in var_list:
        for year in year_range:
            for mon in mon_list:
                # CMCC-ESM2 IPSL-CM6A-LR MIROC6 CESM2 CNRM-CM6-1 MPI-ESM1-2-LR EC-Earth3
                multi_model_mean(data_topdir, experiment, experiment_dir, var, model_list, year, mon, latname, lonname)
