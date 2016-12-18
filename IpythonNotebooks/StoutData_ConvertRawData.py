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
StoutRawData = '/home/ehecht/BIGDATA/Stout_Homo_Faber/RAWDATA'
NiPypeOutputDir ='/EINSTEIN_BIGDATA/NIPYPE_WD/Stout_Haber/'
mem = Memory(base_dir=NiPypeOutputDir)  ## Create a memory cache I can use going forward

## Figure out which directories I want to run through the preprocessing pipeline
HomoFaberImageSessions = [ x for x in os.listdir(StoutRawData) if x.startswith('HOMO')]

print len(HomoFaberImageSessions),"Image Sets Found for HomoFaber"

### gnerate my list of directories to process

T1ImageInputDirectories =  glob( oj(StoutRawData,'*/*t1*'))
### So converting this back into a memcached version
dcmConverter = mem.cache(Dcm2nii)

for T1 in T1ImageInputDirectories:

    imageSessionName = T1.split('/')[-2]  ## Grab the subject Folder
    print T1, imageSessionName
    outputDir = oj(NiPypeOutputDir,"niiData",imageSessionName)

    #Make sure output directory exists
    if not os.path.isdir(outputDir):
        os.makedirs(outputDir)
    #### I may also just want to call it t1Mprage or whatever we use as the default
    dcmConverter(gzip_output=True,source_dir=T1ImageInputDirectories[0],reorient=False, 
             reorient_and_crop=False,
             output_dir=outputDir)


### Convert all of the images with the word diff in it now

diffImageInputDirectories =  glob( oj(StoutRawData,'*/*diff*'))





for diff in diffImageInputDirectories:

    imageSessionName = diff.split('/')[-2]  ## Grab the subject Folder
    print diff, imageSessionName
    outputDir = oj(NiPypeOutputDir,"niiData",imageSessionName)

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
