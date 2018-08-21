DTI=/HCP_Data/HCP_BedpostData/100610/T1w/Diffusion/data.nii.gz
DTI_B0=/HCP_Data/HCP_BedpostData/100610/T1w/Diffusion/nodif.nii.gz
DTI_B0_BRAIN=/HCP_Data/HCP_BedpostData/100610/T1w/Diffusion/nodif_brain.nii.gz
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
antsIntroduction.sh -d 3 -r $MNI_BRAIN  -i $T1_BRAIN -o T1_to_MNI_ -t GR

### note T1_To_MNI_Warp is the warp transform.. and we add two affine matrices which are also real files
#WarpImageMultiTransform 3 $DTI_B0  nodif_to_MNI_test.nii.gz -R $MNI_BRAIN  T1_to_MNI_Warp.nii.gz T1_to_MNI_Affine.txt nodif_to_T1_Affine.txt


### THIS GOES IN REVERSE
#WarpImageMultiTransform 3 $ROI_ONE ROI_ONE_to_subjDTI.nii.gz -R $DTI_B0 -i nodif_to_T1_Affine.txt -i T1_to_MNI_Affine.txt  T1_to_MNI_InverseWarp.nii.gz
#WarpImageMultiTransform 3 $ROI_ONE ROI_ONE_to_subjDTI_NN.nii.gz -R $DTI_B0 --use-NN -i nodif_to_T1_Affine.txt -i T1_to_MNI_Affine.txt  T1_to_MNI_InverseWarp.nii.gz

## --use-NN: Use Nearest Neighbor Interpolation. 
 

#
#Then check that nodif-to-MNI mappings look good: slicesdir –p MNI_template.nii.gz Subj_*_nodif_to_MNI.nii.gz
#Apply INVERSE transformation from MNI-space ROIs to individual subjects’ diffusion space
#WarpImageMultiTransform 3 template_ROI.nii.gz SubjX_ROI.nii.gz –R nodif.nii.gz –i DTI_to_T1_Affine.txt –i T1_to_MNI_Affine.txt T1_to_MNI_InverseWarp.nii.gz

 

#Run probtrackx using native-space ROIs… this will produce a native-space fdt_paths.nii.gz file.  Threshold and normalize in native space.

 

#Apply transformations to get thresholded, normalized tracts into MNI space

#WarpImageMultiTransform 3 fdt_paths_thresh_norm.nii.gz SubjX_fdt_paths_thresh_norm_in_MNIspace.nii.gz -R MNI.nii.gz T1_to_MNI_Warp.nii.gz T1_to_MNI_Affine.txt DTI_to_T1_Affine.txt

 

#Fslmerge –t Subj*_fdt_paths_thresh_norm_in_MNIspace.nii.gz à this becomes the input for randomi

thisfolder=${PWD}/sampleOutput
sub=11111 

antsRegistration --dimensionality 3 --float 0 \
--output [$thisfolder/NN_DTI_to_Struct_${sub}_,$thisfolder/NN_DTI_to_Struct_${sub}_Warped.nii.gz] \
--interpolation NearestNeighbor \
--winsorize-image-intensities [0.005,0.995] \
--use-histogram-matching 0 \
--transform Rigid[0.1] \
--metric MI[$T1_BRAIN,$DTI_B0,1,32,Regular,0.25] \
--convergence [1000x500x250x100,1e-6,10] \
--shrink-factors 8x4x2x1 \
--smoothing-sigmas 3x2x1x0vox 
