import os
import numpy as np
import pandas as pd

def merge_nc(file_list, op_name):
    #1. merge nc files
    os.system('cdo mergetime {} {}'.format(file_list, op_name))

    
def selyear_day_mon_nc(sel_year,nc_infile,op_name):
    #2. select year and calculate monthly mean
    os.system('cdo -selyear,{} -monmean {} {}'.format(sel_year, nc_infile, op_name))

    
def regrid_nc(nc_infile,op_name):
    #3. regrid
    os.system('cdo remapbil,r180x90 {} {}'.format(nc_infile, op_name))

    
def rotate_nc(nc_infile,op_name):
    #4. rotate
    os.system('cdo sellonlatbox,-180,180,-90,90 {} {}'.format(nc_infile, op_name))

def main(top_dir, model, experiment,member_id,grid_label,op_dir,var,time_range,sel_year):

    data_dir = os.path.join(top_dir, model)
   
    op_datadir = os.path.join(op_dir, 'LFMIP-pdLC')

    op_name_a = os.path.join(op_datadir, var+'_Eday'+'_'+model+'_'+experiment+'_'+member_id+'_'+'198001-201912.nc')
    file_list = os.path.join(data_dir, var+'*.nc')
    merge_nc(file_list, op_name_a)
   
    nc_infile = op_name_a

    op_name_b = os.path.join(op_datadir, var+'_Amon'+'_'+model+'_'+experiment+'_'+member_id+'_'+'198201-201412.nc')

    selyear_day_mon_nc(sel_year,nc_infile, op_name_b)
    del nc_infile

    nc_infile = op_name_b

    op_name_c = os.path.join(op_datadir, var+'_Amon'+'_'+model+'_'+experiment+'_'+member_id+'_'+'198201-201412_regrid.nc')

    regrid_nc(nc_infile,op_name_c)
    del nc_infile

    nc_infile = op_name_c
    op_name_d = os.path.join(op_datadir, var+'_Amon'+'_'+model+'_'+experiment+'_'+member_id+'_'+'198201-201412_regrid_rotate.nc')

    rotate_nc(nc_infile,op_name_d)

################################################

top_dir = '../DATA_org/LFMIP-pdLC/'

model = 'MIROC6'

experiment = 'amip-lfmip-pdLC'

member_id = 'r1i1p1f2'

grid_label = 'gn'

op_dir = '../DATA_process/'

var = 'evspsbl'

# time_range = ['1980','1990','2000','2010']

sel_year = '1982/2014'

main(top_dir, model, experiment,member_id,grid_label,op_dir,var,time_range,sel_year)