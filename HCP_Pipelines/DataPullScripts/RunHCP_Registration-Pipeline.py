import nipype
import os,glob,sys,shutil
sys.path.append("/usr/lib/ants/")
import nipype.interfaces.fsl as fsl
import nipype.pipeline.engine as pe
import nipype.interfaces.utility as util
import nipype.interfaces.io as nio
import nipype.interfaces.ants.legacy as antsL
import nipype.interfaces.ants as ants
from nipype.interfaces.ants import Registration
from nipype.interfaces.ants import RegistrationSynQuick
from IPython.display import Image
from nipype.interfaces.fsl import Info
from nipype.interfaces.ants import ApplyTransforms
from nipype import config

from os.path import join as opj
MNI_template = Info.standard_image('MNI152_T1_1mm_brain.nii.gz')
from nipype import config

#cfg = dict(execution={'remove_unnecessary_outputs': False,
#                     'keep_inputs': True})
#config.update_config(cfg)

mountPoint = "/data/" ### I am sometimes running this in a docker container

subjRootDir = opj(mountPoint,"HCP_BedpostData/")


if not os.path.isdir(mountPoint):
    print("Double check mount points...")
    sys.exit()

## add back in npype scratch at some point
regScratchDir = opj(mountPoint,"NipypeScratch/hcpRegPipeline_addDtiWarp/")
print("Registration data will be stored in",regScratchDir)
# """
# Setup for DataGrabber inputs needed for the registration pipeline; This is using the freesurfer nodif and t1 masks
# """
ds = nio.DataGrabber(infields=['subject_id'],
    outfields=['nodif_brain','nodif_brain_mask','struct','struct_mask','struct_brain'])

datasource = pe.Node(interface=ds,name="datasource")
# create a node to obtain the functional images
datasource.inputs.base_directory = subjRootDir
datasource.inputs.template ='*'
datasource.inputs.sort_filelist = True
datasource.inputs.field_template = dict(
    nodif_brain='%s/T1w/Diffusion/nodif_brain.nii*',
    nodif_brain_mask='%s/T1w/Diffusion/nodif_brain_mask.nii*',
    struct='%s/T1w/T1w_acpc_dc.nii*',
    struct_mask='%s/T1w/brainmask_fs.nii*', 
    struct_brain='%s/T1w/T1w_acpc_dc_masked.nii*'
)

datasource.inputs.template_args = dict(
             nodif_brain = [['subject_id']],
             nodif_brain_mask =  [['subject_id']],
             struct =  [['subject_id']],
             struct_mask = [['subject_id']],
             struct_brain = [['subject_id']] )

FULL_SUBJECT_LIST = [x for x in os.listdir(subjRootDir) if os.path.isdir( subjRootDir+x+'/T1w/Diffusion.bedpostX')]
print(len(FULL_SUBJECT_LIST),"Subjects are potentially available to be processed!")

#FULL_SUBJECT_LIST = ["107220","569965","123723","130518","188145","385046","176845","139435","728454","694362"]

#FULL_SUBJECT_LIST = ['107220', '109123', '111716', '113821', '116120', '120212', '123117', '124826', '562446', '567961', '613235', '733548', '745555', 'addlInfo', '113417', '111312', '112819', '113619', '128127', '129028', '145531', '159845', '203721', '486759', '567052', '571548', '953764', '108828', '111514', '114924', '115320', '120111', '126931', '128329', '129432', '131621', '143527', '165234', '169141', '221218', '552544', '782157', '186949', '822244', '107321', '108121', '114419', '126325', '126628', '127630', '128632', '168038', '317332', '611231', '662551', '171128', '623137', '122620', '142424', '201717', '121315', '190132', '521331', '355542', '109325', '734247', '129533', '123420', '113215', '118528', '116524', '120515', '127933', '355845', 'addlInfoV2', '117728', '239136', '108323', '119833', '580751', '106319', '485757', '570243', '197449', '650746', '121618', '689470', '584355', '124220', '171734', '579665', '107422', '150423', '108525', '565452', '111413', '492754', '568963', '579867', '122317', '121820', '207628', '113922', '559053', '209531', '121719', '106521', '110411']


"""
Setup for Registration  Pipeline InfoSource i.e. subjects
"""
subj_infosource = pe.Node(interface=util.IdentityInterface(fields=['subject_id']),  name="subj_infosource")
#infosource.iterables = ('subject_id', SampleSubjList)
subj_infosource.iterables = ('subject_id', FULL_SUBJECT_LIST[:10])
### Above just converts the list of subjects into an iterable list I can connect to the next part of the pipeline

#roi = "/data/HCP_Data/EHECHT_ROIS/Human_Hypothalamus_Left.nii.gz"
roiList = glob.glob( mountPoint+"/EHECHT_ROIS/Human_*nii.gz")

#### RIGID BODY REGISTRATION OF DTI -- >  Struct Brain    using RegSynQuick
regDtiToStruct = pe.Node( RegistrationSynQuick(
                             num_threads=4,
                             output_prefix="dtiToStruct"),
                             name='regDtiToStruct')

regStructToMni = pe.Node( RegistrationSynQuick(
                             num_threads=5, fixed_image=MNI_template,output_prefix="structToMni"),
                             name='regStructToMNI')

warpROIsMniToDti = pe.Node( nipype.interfaces.ants.ApplyTransforms(invert_transform_flags = [True,False,True,False],
                                    interpolation='NearestNeighbor',
                                    ), iterfield=['input_image'], name="warpROIsMniToDti")
warpROIsMniToDti.iterables = ('input_image', roiList)

## CREATE A DATASINK TO COPY OVER THE ROIS IN STANDARD SPACE-- ALSO COPY OVER THE XFMS IN FUTURE VERSION

datasink = pe.Node(nio.DataSink(), name='datasink')
datasink.inputs.base_directory = mountPoint+"HCP_BedpostData/addlInfo/"

datasink.inputs.substitutions = [ ('_subject_id_', ''), ('_input_image_..data..HCP_Data....EHECHT_ROIS..', 'DTI_ROIs/')]

### need to remove the filenames from the path as well as it makes this very messy
for roi in roiList:
   datasink.inputs.substitutions.append( (os.path.basename(roi),'')   )

#                                 ('Human_BasalForebrain_Bilat.nii.gz/',''),
#                                ('Human_BasalForebrain_Left.nii.gz/',''),
#                                 ('Human_BasalForebrain_Right.nii.gz/',''),
#                                 ('Human_Hypothalamus_Right.nii.gz/',''),
#                                 ('Human_Hypothalamus_Left.nii.gz/',''),
#                                 ('Human_Hypothalamus_Bilat.nii.gz/',''),
#                                ]

mergeDtiToMniXfms = pe.Node(util.Merge(4), name='mergeDtiToMniXfms')

run_hcp_reg  = pe.Workflow(name="HcpRegPipelineWarps")
run_hcp_reg.base_dir = regScratchDir

### Conneccts list ofls -al subjects to the data source generator
run_hcp_reg.connect(subj_infosource,'subject_id',datasource,'subject_id')

## Connect inputs for registering the DTI to Structural Image (Rigid Registration)
run_hcp_reg.connect( datasource,'struct_brain',regDtiToStruct,'fixed_image')
run_hcp_reg.connect( datasource,'nodif_brain',regDtiToStruct,'moving_image')

## Connect the inputs for registering Structural to MNI 1mm template-- template is specified in fxn
run_hcp_reg.connect( datasource,'struct_brain',regStructToMni,'moving_image')

run_hcp_reg.connect( regStructToMni, "out_matrix",mergeDtiToMniXfms, "in1"   )
run_hcp_reg.connect( regStructToMni, "inverse_warp_field", mergeDtiToMniXfms, "in2"    )

run_hcp_reg.connect( regDtiToStruct, "out_matrix",mergeDtiToMniXfms, "in3"   )
run_hcp_reg.connect( regDtiToStruct, "inverse_warp_field",mergeDtiToMniXfms, "in4"   )

## So order of matrices being applied is inverse warp field(S->M), affine (S-M) Inverted, then Affine(DTI->S) Inverted

run_hcp_reg.connect( mergeDtiToMniXfms,  'out', warpROIsMniToDti, 'transforms')
run_hcp_reg.connect( datasource, 'nodif_brain', warpROIsMniToDti, 'reference_image')

### Copy the files to a datasink
run_hcp_reg.connect(subj_infosource,'subject_id',datasink,'subject')
run_hcp_reg.connect(warpROIsMniToDti,'output_image',datasink,'subject.@ROIs')

run_hcp_reg.connect(regStructToMni,'forward_warp_field',datasink,'subject.@fwd_warp')
run_hcp_reg.connect(regStructToMni,'inverse_warp_field',datasink,'subject.@inv_warp')
run_hcp_reg.connect(regStructToMni,'out_matrix',datasink,'subject.@affine_mtx')

run_hcp_reg.connect( regDtiToStruct, "out_matrix",datasink, "subject.@dtiToStructMat"   )

run_hcp_reg.connect( regDtiToStruct, "forward_warp_field",datasink, "subject.@dtiToStruct_fdwwarp"   )
run_hcp_reg.connect( regDtiToStruct, "inverse_warp_field",datasink, "subject.@dtiToStruct_invwarp"   )
run_hcp_reg.connect( warpROIsMniToDti,"output_image",datasink,"subject.@roisInDTISpace")

run_hcp_reg.run(plugin='MultiProc', plugin_args={'n_procs' : 40})

run_hcp_reg.write_graph()

