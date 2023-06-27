def sel_year_regrid(selyear, nc_file, opname):
    '''
    for contact time range
    e.g. 1850-2014 or 1950-2014

    nc_file: a single nc file containing the whole time range
    '''
    #os.system('cdo -selyear,{} -remapbil,r180x90 -sellonlatbox,-180,180,-90,90 {} {}'.format(selyear, nc_file, opname))
    #the rotation of longitude won't work, a second step is needed
    os.system('cdo -selyear,{} -remapbil,r180x90 {} {}'.format(selyear, nc_file, opname))


def rotate_nc(nc_file, opname):
    os.system('cdo sellonlatbox,-180,180,-90,90 {} {}'.format(nc_file, opname))


def main_contact_evspsbl():
    log_dir = './log/'
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    make_print_to_file(log_dir,'cdo_selyear_regrid_0625_evspsbl_0627.py')

    # experiment = 'amip-lfmip-pdLC'
    experiment = 'historical'


    if experiment == 'amip-lfmip-pdLC':
        dir_all = '../Data_org/'
        op_dir = '../DATA_process/'
        contact_models = ['CMCC-ESM2', 'IPSL-CM6A-LR', 'CESM2', 'CNRM-CM6-1']
        contact_model_grid = ['gn', 'gr', 'gn', 'gr']

        time_list = ['198001-210012','198001-210012','197001-210012','198001-201412',]
        member_id = 'r1i1p1f2'
    else:
        dir_all = '/mnt/hgfs/F/Data/Original/CMIP6/CMIP6/DATA_org/'
        op_dir = '/mnt/hgfs/F/Data/Original/CMIP6/CMIP6/DATA_process/'
        contact_models = ['CMCC-ESM2', 'IPSL-CM6A-LR', 'CESM2', 'CNRM-CM6-1','MIROC6']
        contact_model_grid = ['gn', 'gr', 'gn', 'gr', 'gn']

        time_list = ['185001-201412', '185001-201412', '185001-201412', '185001-201412','195001-201412']


    var_list = ['evspsbl']
    var_table = ['Amon']

    selyearm = '198201-201412'
    selyear = '1982/2014'

    for i in range(len(contact_models)):
        model = contact_models[i]
        print(model)

        if model == 'CNRM-CM6-1':
            member_id = 'r1i1p1f2'
        else:
            member_id = 'r1i1p1f1'

        data_dir = os.path.join(dir_all, model)


        data_opdir = os.path.join(op_dir, model)
        if not os.path.exists(data_opdir):
            os.mkdir(data_opdir)

        for idx, var in enumerate(var_list):


            nc_file = os.path.join(data_dir,
                                    '{}_{}_{}_{}_{}_{}_{}.nc'.format(var, var_table[idx],
                                                                    model,experiment,member_id,contact_model_grid[i],
                                                                    time_list[i]))


            opname = os.path.join(data_opdir,
                                    '{}_{}_{}_{}_{}_{}.nc'.format(var, var_table[idx], model,
                                                                        experiment,member_id, selyearm))


            sel_year_regrid(selyear, nc_file, opname)
            del nc_file

            nc_file = opname
            opname_b = os.path.join(data_opdir,
                                    '{}_{}_{}_{}_{}_{}_rotate.nc'.format(var, var_table[idx], model,
                                                                        experiment,member_id, selyearm))
            rotate_nc(nc_file, opname_b)

            print('finish processing {} file in {} model'.format(var, model))

if __name__ == '__main__':
    import os
    import glob
    from print_logging import *
    #################################################################################################################

    main_contact_evspsbl()