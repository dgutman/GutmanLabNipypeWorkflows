### Convert RAW DICOM data to NIFTI Image Data set
import os, sys
from os.path import join as oj
from glob import glob

import nipype.pipeline.engine as pe
import nipype.interfaces.utility as util
import nipype.interfaces.io as nio
from nipype.interfaces.dcm2nii import Dcm2nii
from nipype.caching import Memory

## This is the location of the Raw DICOM Files from BITC
StoutRawData = '/home/ehecht/BIGDATA/Stout_Homo_Faber/RAWDATA/'
NiPypeOutputDir ='/EINSTEIN_BIGDATA/NIPYPE_WD/Stout_Haber/'
mem = Memory(base_dir=NiPypeOutputDir)  ## Create a memory cache I can use going forward

## Figure out which directories I want to run through the preprocessing pipeline
HomoFaberImageSessions = [ x for x in os.listdir(StoutRawData) if x.startswith('HOMO')]

print len(HomoFaberImageSessions),"Image Sets Found for HomoFaber"

### A complete image sesion should have the following directories

#$statement  = " dcm2nii -o $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/5B0_PA/ ";
#$statement .= " $RAWDATAPATH/" . $subjID[$i] . "/cmrr_mbep2d_diff_*5B0_PA*/ ";
#print "$statement \n";
#$statement  = " dcm2nii -o $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/ ";
#$statement .= " $RAWDATAPATH/" . $subjID[$i] . "/cmrr_mbep2d_diff_AP_[1-9]*/ ";
#print "$statement \n";
#$statement  = " dcm2nii -o $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_ADC/ ";
#$statement .= " $RAWDATAPATH/" . $subjID[$i] . "/cmrr_mbep2d_diff_AP_ADC_[1-9]*/ ";
#print "$statement \n";
#$statement  = " dcm2nii -o $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_FA/ ";
#$statement .= " $RAWDATAPATH/" . $subjID[$i] . "/cmrr_mbep2d_diff_AP_FA_[1-9]*/ ";
#print "$statement \n";
#$statement  = " dcm2nii -o $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_TRACEW/ ";
#$statement .= " $RAWDATAPATH/" . $subjID[$i] . "/cmrr_mbep2d_diff_AP_TRACEW_[1-9]*/ ";
#print "$statement \n";


DicomScanSet = { 'T1':         { 'dcmDir' : '/*t1*mprage*', 'outputDirName': 'T1'},
                 'diff5B0_PA': { 'dcmDir': '/cmrr_mbep2d_diff_AP_[1-9]*/', 'outputDirName': '/DTI/preprocess/diff5B0_PA'},
                 'diffAP':     { 'dcmDir': '/cmrr_mbep2d_diff_AP_[1-9]*/', 'outputDirName': '/DTI/preprocess/aP/'},
                 'AP_ADC':     { 'dcmDir': '/cmrr_mbep2d_diff_AP_ADC_[1-9]*/', 'outputDirName': '/DTI/preprocess/AP_ADC'},
                 'AP_FA':      { 'dcmDir': '/cmrr_mbep2d_diff_AP_FA_[1-9]*/', 'outputDirName': '/DTI/preprocess/AP_FA'},
                 'AP_TRACEW':  { 'dcmDir': '/cmrr_mbep2d_diff_AP_TRACEW_[1-9]*/', 'outputDirName': '/DTI/preprocess/AP_TRACEW'},
        }




def ScanDicomSet( ImageSessionDir, ScanInfoDict, DicomRoot ):
    """This will scan an image session directory and determine if all of the necessary files exist, if so it yields True
    and then I can run the DICOM Conversion """
    validSubjectDir = True ### If all dicom directories exist, I assume it's a valid scan

    for ScanType in ScanInfoDict:
        dcmDir  = os.listdir( oj( DicomRoot, ImageSessionDir)+(ScanInfoDict[ScanType]['dcmDir']) )
        print ScanType, dcmDir
	

ScanDicomSet( HomoFaberImageSessions[0], DicomScanSet, StoutRawData )

sys.exit()



T1ImageInputDirectories =  glob( oj(StoutRawData,'*/*t1*'))
### So converting this back into a memcached version
dcmConverter = mem.cache(Dcm2nii)


# convert dicoms
#$statement  = " dcm2nii -o $WORKINGDATAPATH/" . $subj[$i] . "/T1/ ";
#$statement .= " $RAWDATAPATH/" . $subjID[$i] . "/t1*/ ";
#print "$statement \n";

for T1 in T1ImageInputDirectories:

    imageSessionName = T1.split('/')[-2]  ## Grab the subject Folder
    print T1, imageSessionName
    outputDir = oj(NiPypeOutputDir,"niiData",imageSessionName,'T1')

    #Make sure output directory exists
    if not os.path.isdir(outputDir):
        os.makedirs(outputDir)
    #### I may also just want to call it t1Mprage or whatever we use as the default
    dcmConverter(gzip_output=True,source_dir=T1ImageInputDirectories[0],reorient=True, 
             reorient_and_crop=False,
             output_dir=outputDir)




#$statement  = " dcm2nii -o $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/5B0_PA/ ";
#$statement .= " $RAWDATAPATH/" . $subjID[$i] . "/cmrr_mbep2d_diff_*5B0_PA*/ ";
#print "$statement \n";
#$statement  = " dcm2nii -o $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/ ";
#$statement .= " $RAWDATAPATH/" . $subjID[$i] . "/cmrr_mbep2d_diff_AP_[1-9]*/ ";
#print "$statement \n";
#$statement  = " dcm2nii -o $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_ADC/ ";
#$statement .= " $RAWDATAPATH/" . $subjID[$i] . "/cmrr_mbep2d_diff_AP_ADC_[1-9]*/ ";
#print "$statement \n";
#$statement  = " dcm2nii -o $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_FA/ ";
#$statement .= " $RAWDATAPATH/" . $subjID[$i] . "/cmrr_mbep2d_diff_AP_FA_[1-9]*/ ";
#print "$statement \n";
#$statement  = " dcm2nii -o $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_TRACEW/ ";
#$statement .= " $RAWDATAPATH/" . $subjID[$i] . "/cmrr_mbep2d_diff_AP_TRACEW_[1-9]*/ ";
#print "$statement \n";

### Convert all of the images with the word diff in it now

diff5B0_PA_ImageInputDirectories =  glob( oj(StoutRawData,'*/*cmrr_mbep2d_diff_*5B0_PA*'))

for diff in diff5B0_PA_ImageInputDirectories:
    imageSessionName = diff.split('/')[-2]  ## Grab the subject Folder
    print diff, imageSessionName
    outputDir = oj(NiPypeOutputDir,"niiData",imageSessionName,)

    #Make sure output directory exists
    if not os.path.isdir(outputDir):
        os.makedirs(outputDir)
    #### I may also just want to call it t1Mprage or whatever we use as the default


    try:
        dcmConverter(gzip_output=True,source_dir=diff,reorient=False, 
             reorient_and_crop=False,
             output_dir=outputDir)
    except:
        print "Found error with",diff
