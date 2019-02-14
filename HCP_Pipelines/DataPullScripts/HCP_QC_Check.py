import os,sys,glob
import shutil
### Make this resilient for me being in or NOT in docker... so have it check if /HCP_Data exists and change the path
### accordingly

if os.path.isdir("/HCP_Data/"):
    root = "/HCP_Data/"
else:
    root = "/data/"

subjRootDir = root+ "HCP_BedpostData/"

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




xfmFiles = ['dtiToStruct0GenericAffine.mat','dtiToStruct1InverseWarp.nii.gz','dtiToStruct1Warp.nii.gz',
            'structToMni1Warp.nii.gz','structToMni1InverseWarp.nii.gz','structToMni0GenericAffine.mat']


#print(len(FULL_SUBJECT_LIST),"Subjects have a masked T1 image")
missingData = []
missingXFMs = []
missingROIsInDTISpace = []
missingPBXData = []
subjList = [x for x in os.listdir(subjRootDir) if os.path.isdir(subjRootDir+x)]


roiCount = 8

for s in subjList:

    try:
        XFM_Files = os.listdir(subjRootDir+'addlInfoV2/subject/'+s)
    except:
        print("No XFMs found for",s)
        missingXFMs.append(s)
        continue

    xfmsFound = 0
    for xfm in xfmFiles:
        if xfm in XFM_Files:
            xfmsFound+=1

    if(xfmsFound!=6):
        missingXFMs.append(s)

    DTI_ROIs = glob.glob(subjRootDir+'addlInfoV2/subject/'+s+'/DTI_ROIs/Human*.nii.gz')
    if (len(DTI_ROIs)!= roiCount):
        #print(len(DTI_ROIs),"DTI ROIS found..",s)
        missingData.append(x)
    pbxResults = glob.glob(subjRootDir+'addlInfoV2/subject/'+s+'/pbxResults/DTI/Human*.nii.gz')
#    if (len(pbxResults)!= roiCount):
#        print(len(pbxResults),"pbxResults were ROIS found..")
        #missingData.append(x)


print(missingData)
print(len(set(missingData)))
print(xfmsFound)
print(missingXFMs)

#for m in missingXFMs:
#    shutil.move(subjRootDir+m,"/HCP_Data/HCP_StructOnly/")

sys.exit()
## Look for dirs that don't have DTI and I'll move them somewhere else for now..

