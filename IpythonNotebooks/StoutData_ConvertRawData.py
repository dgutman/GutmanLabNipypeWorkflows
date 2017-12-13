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

dcmConverter = mem.cache(Dcm2nii)

DicomScanSet = { 'T1':         { 'dcmDir' : '*t1*', 'outputDirName': 'T1'}, 
     'diff5B0_PA': { 'dcmDir': 'cmrr_mbep2_diff_*5B0_PA*', 'outputDirName':'DTI/preprocess/diff5B0_PA'},
                 'diffAP':     { 'dcmDir': 'cmrr_mbep2d_diff_AP_[1-9]*', 'outputDirName': 'DTI/preprocess/AP'},
                 'AP_ADC':     { 'dcmDir': 'cmrr_mbep2d_diff_AP_ADC_[1-9]*', 'outputDirName': 'DTI/preprocess/AP_ADC'},
                 'AP_FA':      { 'dcmDir': 'cmrr_mbep2d_diff_AP_FA_[1-9]*', 'outputDirName': 'DTI/preprocess/AP_FA'},
                 'AP_TRACEW':  { 'dcmDir': 'cmrr_mbep2d_diff_AP_TRACEW_[1-9]*', 'outputDirName': 'DTI/preprocess/AP_TRACEW'},
        }

#QFE   *t1* for *t1*mprage*??? 

#     # convert dicoms
#     $statement  = " dcm2nii -o $WORKINGDATAPATH/" . $subj[$i] . "/T1/ ";
#     $statement .= " $RAWDATAPATH/" . $subjID[$i] . "/t1*/ ";
#     #print "$statement \n";
#     $statement  = " dcm2nii -o $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/5B0_PA/ ";
#     $statement .= " $RAWDATAPATH/" . $subjID[$i] . "/cmrr_mbep2d_diff_*5B0_PA*/ ";
#     #print "$statement \n";
#     $statement  = " dcm2nii -o $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP/ ";
#     $statement .= " $RAWDATAPATH/" . $subjID[$i] . "/cmrr_mbep2d_diff_AP_[1-9]*/ ";
#     #print "$statement \n";
#     $statement  = " dcm2nii -o $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_ADC/ ";
#     $statement .= " $RAWDATAPATH/" . $subjID[$i] . "/cmrr_mbep2d_diff_AP_ADC_[1-9]*/ ";
#     #print "$statement \n";
#     $statement  = " dcm2nii -o $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_FA/ ";
#     $statement .= " $RAWDATAPATH/" . $subjID[$i] . "/cmrr_mbep2d_diff_AP_FA_[1-9]*/ ";
#     #print "$statement \n";
#     $statement  = " dcm2nii -o $WORKINGDATAPATH/" . $subj[$i] . "/DTI/preprocess/AP_TRACEW/ ";
#     $statement .= " $RAWDATAPATH/" . $subjID[$i] . "/cmrr_mbep2d_diff_AP_TRACEW_[1-9]*/ ";
#     #print "$statement \n";


def generateNIIData( inputDcmDir, imageType, outputDir, debug=False):
    if debug:
        print "Received %s" % outputDir
        print "Dumping data to %s" % outputDir
    #Make sure output directory exists
    if not os.path.isdir(outputDir):
        os.makedirs(outputDir)
    #### I may also just want to call it t1Mprage or whatever we use as the default

    ##Only generate files if the output directory doesn't have anything in it..
    
    
    if (len( os.listdir(outputDir))  == 0 ):
    
        dcmConverter(gzip_output=True,source_dir=inputDcmDir,
             output_dir=outputDir)
    

