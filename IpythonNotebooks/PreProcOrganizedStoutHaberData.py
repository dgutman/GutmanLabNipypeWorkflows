## Nipype Workflow for Erin's DTI Data
### Convert RAW DICOM data to NIFTI Image Data set
import os, sys
from os.path import join as oj
from glob import glob

import nipype.pipeline.engine as pe
import nipype.interfaces.utility as util
import nipype.interfaces.io as nio
import nipype.interfaces.fsl as fsl


### This is where Erin has put all of the renamed/reorganized files
RenamedNIIDir = '/home/ehecht/BIGDATA/Stout_Homo_Faber/WORKINGDATA'
NiPypeOutputDir = '/EINSTEIN_BIGDATA/NIPYPE_WD/Stout_Haber/niPypePreProc/'

HomoFaberImageSessions = [] ### Null Array

## LETS BE SMART..
for ss in os.listdir(RenamedNIIDir):
    fullSubjDirPath =  oj(RenamedNIIDir,ss)
    if ss.startswith('Subj'):
        HomoFaberImageSessions.append(ss)
        
print len(HomoFaberImageSessions),"Subjects to process"

stoutPreProc_wf = pe.Workflow('stoutPreProc_wf') ## Initialize the workflow
stoutPreProc_wf.base_dir = NiPypeOutputDir  ## Tell it where to dump the results of the workflow

imageSession_InfoSrc  = pe.Node(util.IdentityInterface(fields=['imageSessionName']),name='imageSession_InfoSrc')
imageSession_InfoSrc.iterables = ('imageSessionName', HomoFaberImageSessions)

"""
Map field names to individual subject runs
"""
wfInfo = dict( 
        T1Brain = [['imageSessionName','struc_brain']],
        nodiffBrain = [['imageSessionName', 'nodif_brain']],
        nodiffBrainMask = [['imageSessionName','nodif_brain_mask']],
        dtidata = [['imageSessionName','data']],
        bvecs = [['imageSessionName']],
        bvals = [['imageSessionName']],
        imageSessionName = [['imageSessionName']]
        )



wfFieldTemplate = dict( T1Brain='%s/T1/%s.nii.gz', nodiffBrain = '%s/DTI/data/%s.nii.gz',
        nodiffBrainMask = '%s/DTI/data/%s.nii.gz', dtidata = "%s/DTI/data/%s.nii.gz",
	bvecs = "%s/DTI/data/bvecs", bvals = "%s/DTI/data/bvals", imageSessionName = "%s")

# ## Create a datasource.. this basically helps me find the individual image files and data sets for an image session
# ## a single image directory likely consists of DTI data, T2 images, T1 images, etc, etc
datasource = pe.Node(interface=nio.DataGrabber(infields=['imageSessionName'],outfields=wfInfo.keys()), name='datasource')
datasource.inputs.base_directory = RenamedNIIDir
datasource.inputs.template = '*'
datasource.inputs.sort_filelist = True
datasource.inputs.field_template = wfFieldTemplate
datasource.inputs.template_args = wfInfo

## Let's create our first actual workflow step... register the nodiffBrain to the T1 Image Space
nodiffToT1 = pe.Node(interface=fsl.FLIRT(), name='nodiffToT1')
nodiffToT1.inputs.dof = 6

### Also register the T1 image to standard space!!
flirtToStd = pe.Node(interface=fsl.FLIRT(), name='flirtToStd')
flirtToStd.inputs.reference = fsl.Info.standard_image('MNI152_T1_2mm_brain.nii.gz')
flirtToStd.inputs.dof = 12


### Now start connecting up the nodes/graph


###bet = pe.Node(interface=fsl.BET(), name='bet')
##bet.inputs.mask = True
###bet.inputs.frac = 0.2

#gen_fa.connect(datasource, 'dwi', eddy_correct, 'inputnode.in_file')

#bet = pe.Node(interface=fsl.BET(), name='bet')
#bet.inputs.mask = True
#bet.inputs.frac = 0.2
#gen_fa.connect(eddy_correct, 'pick_ref.out', bet, 'in_file')

dtifit = pe.Node(interface=fsl.DTIFit(), name='dtifit')


#### Generate all the connections needed for the DTIFIT module


stoutPreProc_wf.connect(datasource,'bvecs',dtifit,'bvecs')
stoutPreProc_wf.connect(datasource,'bvals',dtifit,'bvals')
stoutPreProc_wf.connect(datasource,'dtidata',dtifit,'dwi')

stoutPreProc_wf.connect(datasource, 'nodiffBrainMask', dtifit, 'mask')

stoutPreProc_wf.connect(datasource, 'imageSessionName', dtifit, 'base_name')

datasink = pe.Node(interface=nio.DataSink(), name="datasink")
datasink.inputs.base_directory = os.path.join(os.path.abspath(NiPypeOutputDir),
                                              'dgDevTesting_results')


datasink.inputs.parameterization = False
stoutPreProc_wf.connect(dtifit, 'FA', datasink, 'FA')
stoutPreProc_wf.connect(dtifit, 'MD', datasink, 'MD')



### Infosource is already connected to the list of subject directories
## Connect InfoSource --> DataSource
stoutPreProc_wf.connect(imageSession_InfoSrc,'imageSessionName',datasource,'imageSessionName')

### Connect the datasource to flirtToStd
stoutPreProc_wf.connect(datasource,'T1Brain',flirtToStd,'in_file')


stoutPreProc_wf.connect(datasource,'nodiffBrain',nodiffToT1,'in_file')
stoutPreProc_wf.connect(datasource,'T1Brain' , nodiffToT1,'reference')
#stoutPreProc_wf.connect(datasource,'nodiffBrain',nodiffToT1,'in_file')

stoutPreProc_wf.run(plugin='MultiProc', plugin_args={'n_procs' : 8})



