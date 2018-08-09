DTI=/HCP_Data/HCP_BedpostData/100610/T1w/Diffusion/data.nii.gz
DTI_B0=/HCP_Data/HCP_BedpostData/100610/T1w/Diffusion/nodif_brain.nii.gz
DTI_M=/HCP_Data/HCP_BedpostData/100610/T1w/Diffusion/nodif_brain_mask.nii.gz
T1_M=/HCP_Data/HCP_BedpostData/100610/T1w/brainmask_fs.nii.gz
T1=/HCP_Data/HCP_BedpostData/100610/T1w/T1w_acpc_dc.nii.gz
DTI_TO_T1=/HCP_Data/Scripts/GutmanLabNipypeWorkflows/HCP_Pipelines/sampleAntsRegData/nodif_to_T1_deformed.nii.gz
MNI_BRAIN=/usr/share/fsl/5.0/data/standard/MNI152_T1_1mm_brain.nii.gz 


T1_BRAIN=/HCP_Data/Scripts/GutmanLabNipypeWorkflows/HCP_Pipelines/sampleAntsRegData/T1w_acpc_dc_masked.nii.gz


ROI_ONE=/HCP_Data/EHECHT_ROIS/Human_Hypothalamus_Left.nii.gz  


echo $IN $T1_M $T1

## NOTES PROBABLY wouLD bE QUICKER IF WE USED THE T1 IMAGE WIHT THE MASK APPLIED... TO DO!!

export PATH=$PATH:/usr/lib/ants
export ANTSPATH=/usr/lib/ants

## Get the first B0 image from the DTI data set
#fslroi $DTI $DTI_B0 0 1 


## Register the B0/DTI image to the T1 --- we perhaps should have used the masked/brainonly T1??
#antsIntroduction.sh -d 3 -r $T1 i $DTI_B0 -o nodif_to_T1_ -t RI


## Need to apply the brain mask to the T1 image to speed things up
#fslmaths $T1 -mas $T1_M $T1_MASKED


### Thsi registers the T1 Brain image nonlinearly to MNI Space.. and also generated the inverse warp
#antsIntroduction.sh -d 3 -r $MNI_BRAIN  -i $T1_BRAIN -o T1_to_MNI_ -t GR

### note T1_To_MNI_Warp is the warp transform.. and we add two affine matrices which are also real files
WarpImageMultiTransform 3 $DTI_B0  nodif_to_MNI_test.nii.gz -R $MNI_BRAIN  T1_to_MNI_Warp.nii.gz T1_to_MNI_Affine.txt nodif_to_T1_Affine.txt


### THIS GOES IN REVERSE
WarpImageMultiTransform 3 $ROI_ONE ROI_ONE_test.nii.gz -R $MNI_BRAIN  T1_to_MNI_Warp.nii.gz T1_to_MNI_Affine.txt nodif_to_T1_Affine.txt


