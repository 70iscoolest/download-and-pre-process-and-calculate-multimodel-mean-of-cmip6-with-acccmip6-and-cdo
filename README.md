
# <center> <font color=#FF9797 face="Segoe UI Black" size=5> **Uniformly aggregate and regrid monthly CMIP6 historical/LFMIP nc files using CDO** </font> </center>

> <font color=#20B2AA face="Javanese Text" size=4>**AIM: generate monthly $2\degree \times 2\degree$ nc files merged in time series (198201-201412) for each model**</font>

## <font color=#20B2AA face="Javanese Text" size=4> **0. Environment** </font>

- Linux (#44~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon May 22 13:39:36 UTC 2 x86_64 x86_64 x86_64 GNU/Linux)
- Anaconda (23.1.0)
- Python (3.10)
- cdo

## <font color=#20B2AA face="Javanese Text" size=4> **1. Models** </font>

|model|grid|resolution|time format (historical)|
|---|---|---|---|
|CESM2|gn|192 $\times$ 288(0.94 $\times$ 1.25)|1850-2014|
|CMCC-ESM2|gn|192 $\times$ 288(0.94 $\times$ 1.25)|1850-2014|
|CNRM-CM6-1|gr|128 $\times$ 256(1.39 $\times$ 1.406)|1850-2014|
|EC-Earth3|gr|256 $\times$ 512(0.69 $\times$ 0.7031)|yearly|
|IPSL-CM6A-LR|gr|143 $\times$ 144(1.26761 $\times$ 2.5)|1850-2014|
|MIROC6|gn|128 $\times$ 256(1.39 $\times$ 1.406)|1850-2014|
|MPI-ESM1-2-LR|gn|96 $\times$ 192(1.85 $\times$ 1.875)|20-year-ly|
||||||

## <font color=#20B2AA face="Javanese Text" size=4> **2. Search and download data [acccmip6]**</font>

1.search

```
acccmip6 -o S -v evspsbl,mrso,tas,pr,hfls -f mon -e amip-lfmip-pdLC -m CESM2,CMCC-ESM2,CNRM-CM6-1,IPSL-CM6A-LR,MIROC6,MPI-ESM1-2-LR -skip 1f1
acccmip6 -o S -v evspsbl,mrso,tas,pr,hfls -e historical -m CESM2,CMCC-ESM2,CNRM-CM6-1,IPSL-CM6A-LR,MIROC6,MPI-ESM1-2-LR -rlzn 1
```
2.download

(1) for monthly nc files containing the whole time range:
- run a bash

    ```
    for i in CESM2 CMCC-ESM2 CNRM-CM6-1 IPSL-CM6A-LR MPI-ESM1-2-LR
    do
        acccmip6 -o D -v evspsbl -f mon -e historical -m $i -rlzn 1 -dir $i
    done

    for i in CESM2 CMCC-ESM2 CNRM-CM6-1 IPSL-CM6A-LR MPI-ESM1-2-LR
    do
        acccmip6 -o D -v evspsbl -f mon -e amip-lfmip-pdLC -m $i -rlzn 1 -dir $i -skip 1f1
    done
    ```

- actually not all 5 model above contain the whole range as 1850-2014 or 1850-2100, some models generate nc files for each time range of 20 years or so, you can download files according to each model respectively, but running a bash can be a little more efficient, after which you can simply delete unnecessary files

(2) for MICRO6 model which only provides daily nc files
- run in the terminal
    ```
    acccmip6 -o D -v evspsbl -e  historical -m MIROC6 -rlzn 1 -dir MIROC6

    acccmip6 -o D -v evspsbl -e amip-lfmip-pdLC -m MIROC6 -rlzn 1 -dir MIROC6 -skip 1f1
    ```

(3) for EC-Earth3 which provides monthly nc files but are seperate by yearly time step
- run in the terminal
    ```
    acccmip6 -o D -v evspsbl -e  historical -m EC-Earth3 -rlzn 1 -dir EC-Earth3 -yr -32 # select the time range I want: 1982-2014

    acccmip6 -o D -v evspsbl -e amip-lfmip-pdLC -m EC-Earth3 -f mon -rlzn 1 -dir EC-Earth3 -yr 35 -skip 1f1
    ```

- the available time range is 1980-2100, I only need historical time range which is the first 35 years of the time range, it seems impossible to choose the middle time range in the acccmip6


## <font color=#20B2AA face="Javanese Text" size=4> **3. data pre-process [CDO]** </font>

### <font size=4> 3.1. *[CDO] installation* </font>
- CDO
```
conda install -c conda-forge cdo
```
- python CDO: To install this package run one of the following:
```
conda install -c conda-forge python-cdo
conda install -c "conda-forge/label/cf201901" python-cdo
conda install -c "conda-forge/label/cf202003" python-cdo
conda install -c "conda-forge/label/gcc7" python-cdo
```
### <font size=4> 3.2. *basic info* </font>

#### 1. **CMIP6 historical**

    [cmip6hist_file_info.csv](../CMIP6PROJECT/outputs_info/cmip6hist_file_info.csv)

#### 2. **LFMIP**

    [cmip6hist_file_info.csv](../CMIP6PROJECT/outputs_info/amip-lfmip-pdLC_file_info.csv)

- mrso nc files contain null values except for `CMCC-ESM2` model, in which the missing values are assigned with zero
- other variables have no null values across the globe, as they are atmospheric variables
- things are different in `CESM2` model, as all variables including atmospheric ones contain null values, suggesting the modelling group have assigned non-terrestrial grids with null values
> however, I don't feel like it's a problem, as the cdo deals well with null values, and only terrestrial grids would be used in my analysis, there is minor interpolation difference between nc files with null values and those with no null values

- it's necessary to first assign zero values in mrso nc files of `CMCC-ESM2` model with null values, or there can be errors when interpolation is performing across multiple grids. 
- This means the data processing procedure of mrso nc files of `CMCC-ESM2` model needs to be performed again, which can be referred to [3.3 Example 1](#u2)

#### <div id='u3'>3 batch coding in python</div>
    [print_nc_info.py](../CMIP6PROJECT/python_scripts/print_nc_info.py)

### <font size=4> 3.3. *processing* </font>

> <div id='u1'>Example 1. mrso_Lmon_CMCC-ESM2_amip-lfmip-pdLC_r1i1p1f2_gn_198001-210012.nc<div></p>
> run a bash on terminal

- 1. select year I wanted: 198201-201412, meanwhile assign 0 values with null values
- 2. regrid
- 3. rotate

- see `bash_scripts/cdo_mrso_example.sh`

> Example 2. evspsbl </p>

#### <div id='u2'> 1. MIROC6: (only for amip-lfmip-pdLC)<div>

 - 1. merge seperate nc files for a large time range
 - 2. select year I wanted
 - 3. calculate monthly average according to the original daily files
 - 4. regrid
 - 5. rotate

- see `python_scripts/evspsbl_MIRCO6_example.py`

#### 2. MPI-ESM1-2-LR (files are seperate in 20-year time range)
 - 1. merge seperate nc files for a large time range
 - 2. select year I wanted
 - ~~calculate monthly average according to the original daily files~~
 - 3. regrid
 - 4. rotate

 - files are not indentical in two simulations, in historical, the time range is 1970-2014 

    ```
    run a bash to copy files containing the time range I want

    cp ../Data_org/MPI-ESM1-2-LR/evspsbl*2000*.nc ./
    cp ../Data_org/MPI-ESM1-2-LR/evspsbl*1980*.nc ./
    ```

    - the following python codes is similar to [MIROC6: (only for amip-lfmip-pdLC)](#u2), except for calculating monmean

#### 3. models containing the whole time range

>['CMCC-ESM2', 'IPSL-CM6A-LR', 'CESM2', 'CNRM-CM6-1', 'MIRCO6'(only for historical)]
  - ~~merge seperate nc files for a large time range~~
  - 1. select year wanted
  - ~~calculate monthly average according to the original daily files~~
  - 2. regrid
  - 3. rotate
  > some steps can be combined as cdo supports chained operations
  - see `python_scripts/evspsbl_5models_example.py`

#### 4. yearly nc files: EC-Earth3

> only files in wanted time range in the root directory
  - 1. merge time
  - 2. select wanted time range and regrid
  - 3. rotate

    ```
    #run a bash where you download the original nc files

    for i in `seq 1982 2014`
    do
        cp ./evspsbl*$i*.nc ../DATA_process/EC-Earth3/temp1982_2014/
    done

    for i in `seq 1982 2014`
    do
        cp ./evspsbl*$i*.nc ../DATA_process/EC-Earth3/temp1982_2014/
    done
    ```
    - see `python_scripts/evspsbl_EC-Earth3_example.py`


### <font size=4> 3.4 *Check processed files* </font>

python coding same as [batch coding in python](#u3)

[process_historical_file_info.csv](../CMIP6PROJECT/outputs_info/process_historical_file_info.csv)

[process_amip-lfmip-pdLC_file_info.csv](../CMIP6PROJECT/outputs_info/process_amip-lfmip-pdLC_file_info.csv)


## <font color=#20B2AA face="Javanese Text" size=4> **4. about missing values in cdo** </font>

> how does cdo cooperate with missing values?

Missing values are data points that are missing or invalid. Such data points are treated in a different way
than valid data. Most CDO operators can handle missing values in a smart way. But if the missing value
is within the range of valid data, it can lead to incorrect results. This applies to all arithmetic operations,
but especially to logical operations when the missing value is 0 or 1.

- so there is a need to assign 0 in mrso nc files with nan


