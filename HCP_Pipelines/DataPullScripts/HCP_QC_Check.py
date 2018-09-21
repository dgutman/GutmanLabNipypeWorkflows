import os,sys

### Make this resilient for me being in or NOT in docker... so have it check if /HCP_Data exists and change the path
### accordingly


if os.path.isdir("/HCP_Data/"):
    root = "/HCP_Data/"
else:
    root = "/data/"

subjRootDir = root+ "/HCP_BedpostData/"

FULL_SUBJECT_LIST = [x for x in os.listdir(subjRootDir) if os.path.isdir( subjRootDir+x+'/T1w/Diffusion')]
print(len(FULL_SUBJECT_LIST),"Subjects have Diffusion data available to be processed!")

FULL_SUBJECT_LIST = [x for x in os.listdir(subjRootDir) if os.path.isdir( subjRootDir+x+'/T1w/Diffusion.bedpostX')]
print(len(FULL_SUBJECT_LIST),"Subjects have processed Diffusion data")


FULL_SUBJECT_LIST = [x for x in os.listdir(subjRootDir) if os.path.isfile( subjRootDir+x+'/T1w/Diffusion/data_FA.nii.gz')]
print(len(FULL_SUBJECT_LIST),"Subjects have processed FA map data")


FULL_SUBJECT_LIST = [x for x in os.listdir(subjRootDir) if os.path.isfile( subjRootDir+x+'/T1w/Diffusion/nodif_brain_mask.nii.gz')]
print(len(FULL_SUBJECT_LIST),"Subjects have Nodiff brain masks")


FULL_SUBJECT_LIST = [x for x in os.listdir(subjRootDir) if os.path.isfile( subjRootDir+x+'/T1w/T1w_acpc_dc_masked.nii.gz')]
print(len(FULL_SUBJECT_LIST),"Subjects have a masked T1 image")



