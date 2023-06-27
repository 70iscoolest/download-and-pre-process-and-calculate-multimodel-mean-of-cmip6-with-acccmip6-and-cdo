def rotate_nc(nc_file, opname):
    os.system('cdo sellonlatbox,-180,180,-90,90 {} {}'.format(nc_file, opname))


def merge_year(var, data_dir, opname):
    '''
    for yearly time range
    i.e. 'EC-Earth3'
    '''

    # os.system('rm {} '.format(os.path.join(data_dir, var+'*1981*.nc')))
    # os.system('rm {} '.format(os.path.join(data_dir, var+'*1980*.nc')))

    infiles = os.path.join(data_dir, var + '*.nc')

    os.system('cdo -mergetime {} {}'.format(infiles, opname))# only one command at one step!!!


def main_multiple_ecearth_evspsbl():
    log_dir = './log/'
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    make_print_to_file(log_dir, 'cdo_mergetime_regrid_0625_0627.py')


    model = 'EC-Earth3'
    selyearm = '198201-201412'

    # experiment = 'amip-lfmip-pdLC'
    experiment = 'historical'


    if experiment == 'amip-lfmip-pdLC':
        dir_all = '../DATA_process/LFMIP-pdLC/EC-Earth3/temp1982_2014/'
        op_dir = '../DATA_process/LFMIP-pdLC/EC-Earth3/process/'
        member_id = 'r1i1p1f2'
    else:
        dir_all = '../DATA_process/historical/EC-Earth3/temp1982_2014/'
        op_dir = '../DATA_process/historical/EC-Earth3/process/'
        member_id = 'r1i1p1f1'

    data_dir = dir_all
    data_opdir = op_dir
    var_list = ['evspsbl']
    var_table = ['Amon']


    for idx, var in enumerate(var_list):
        # print(var)
        ########################################################################################
        opname_a = os.path.join(data_opdir,
                              '{}_{}_{}_{}_{}_{}.nc'.format(var, var_table[idx], model,
                                                            experiment, member_id, selyearm))
        merge_year(var, data_dir, opname_a)
        ##########################################################################################
        nc_file = opname_a

        opname_b = os.path.join(data_opdir,
                                '{}_{}_{}_{}_{}_{}_regrid.nc'.format(var, var_table[idx], model,
                                                              experiment, member_id, selyearm))

        only_regrid(nc_file, opname_b)
        del nc_file
        #########################################################################################
        nc_file = opname_b
        opname_c = opname_b = os.path.join(data_opdir,
                                '{}_{}_{}_{}_{}_{}_regrid_rotate.nc'.format(var, var_table[idx], model,
                                                              experiment, member_id, selyearm))

        rotate_nc(nc_file,opname_c)


        print('finish processing {} file in {} model'.format(var, model))

        
if __name__ == '__main__'
    main_multiple_ecearth_evspsbl()