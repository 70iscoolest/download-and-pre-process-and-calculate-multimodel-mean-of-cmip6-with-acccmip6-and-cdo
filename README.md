# download-and-pre-process-and-calculate-multimodel-mean-of-cmip6-with-acccmip6-and-cdo


# <center> <font color=#FF9797 face="Segoe UI Black" size=5> **Calculate multimodel mean across 7 models of CMIP6 historical/LFMIP and visualization** </font> </center>

## <font color=#20B2AA face="Javanese Text" size=4> **0. Environment** </font>

- Linux (#44~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon May 22 13:39:36 UTC 2 x86_64 x86_64 x86_64 GNU/Linux)
- Anaconda (23.1.0)
- Python (3.10)
- cdo

## <font color=#20B2AA face="Javanese Text" size=4> **1. Models ([aggregated and regridded](https://github.com/70iscoolest/download-and-process-cmip6-historical-and-lfmip-with-acccmip6-and-cdo))** </font>

|model|grid|resolution|time format|
|---|---|---|---|
|CESM2|bilinear interpolation|90 $\times$ 180 ($2 \degree \times 2 \degree$)|198201-201412|
|CMCC-ESM2|bilinear interpolation|90 $\times$ 180 ($2 \degree \times 2 \degree$)|198201-201412|
|CNRM-CM6-1|bilinear interpolation|90 $\times$ 180 ($2 \degree \times 2 \degree$)|198201-201412|
|EC-Earth3|bilinear interpolation|90 $\times$ 180 ($2 \degree \times 2 \degree$)|198201-201412|
|IPSL-CM6A-LR|bilinear interpolation|90 $\times$ 180 ($2 \degree \times 2 \degree$)|198201-201412|
|MIROC6|bilinear interpolation|90 $\times$ 180 ($2 \degree \times 2 \degree$)|198201-201412|
|MPI-ESM1-2-LR|bilinear interpolation|90 $\times$ 180 ($2 \degree \times 2 \degree$)|198201-201412|


## <font color=#20B2AA face="Javanese Text" size=4> **2. variables**</font>

|variables|description|unit|
|---|---|---|
|mrso|total soil water content|kg m-2|
|evspsbl|Evaporation Including Sublimation and Transpiration|kg m-2 s-1|
|hfls|surface upward latent heat flux|W m-2|
|pr|precipitation|kg m-2 s-1|
|tas|near surface temperature|K|


## <font color=#20B2AA face="Javanese Text" size=4> **3. Split contact single nc files (198201-201412) into singles file containing one month**</font>

the processed nc files are stored according to each variable and each model
- `../CMIP6PROJECT/DATA_process/LFMIP-pdLC/`

![](./pics/file%20structure1.png)

- `../CMIP6PROJECT/DATA_process/LFMIP-pdLC/evspsbl/`

![](./pics/file%20structure2.png)

run a bash

```
for i in CMCC-ESM2 IPSL-CM6A-LR MIROC6 CESM2 CNRM-CM6-1 MPI-ESM1-2-LR EC-Earth3
do
	for j in pr tas hfls evspsbl mrso
	do
		cdo splityearmon /mnt/hgfs/F/Data/Original/CMIP6/CMIP6PROJECT/DATA_process/LFMIP-pdLC/$j/*$i*.nc /mnt/hgfs/F/Data/Original/CMIP6/CMIP6PROJECT/DATA_process/LFMIP-pdLC/$j/split/$i/"$j"_"$i"_lfmip_
	done
done
```
> before that, use `mkdir` to make directories of 7 models in each variables

- `../CMIP6PROJECT/DATA_process/LFMIP-pdLC/evspsbl/split/`

![](./pics/file%20structure3.png)

- `../CMIP6PROJECT/DATA_process/LFMIP-pdLC/evspsbl/split/CESM2/`

![](./pics/file%20structure4.png)

## <font color=#20B2AA face="Javanese Text" size=4> **4. Calculate multiple model mean for each variable**</font>

- see `../scipts/multimodel_mean.py`
- generate mean nc files of each month for each variable 

![](./pics/file%20structure5.png)

## <font color=#20B2AA face="Javanese Text" size=4> **5. Merge these mean files into one single nc files with time series**</font>

run a bash
```
for i in hfls pr tas mrso evspsbl
do
	cdo mergetime /mnt/hgfs/F/Data/Original/CMIP6/CMIP6PROJECT/DATA_process/LFMIP-pdLC/$i/multimodel_mean/nc/*.nc /mnt/hgfs/F/Data/Original/CMIP6/CMIP6PROJECT/DATA_process/LFMIP-pdLC/$i/multimodel_mean/nc/"$i"_lfmip_198201-201412.nc
	cp /mnt/hgfs/F/Data/Original/CMIP6/CMIP6PROJECT/DATA_process/LFMIP-pdLC/$i/multimodel_mean/nc/"$i"_lfmip_198201-201412.nc /mnt/hgfs/F/Data/Original/CMIP6/CMIP6PROJECT/DATA_analysis/"$i"_lfmip_198201-201412.nc
done
```
- finally generate multimodel mean nc files for each variable

![](./pics/file%20structure6.png)

