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
from nipype.interfaces.ants import WarpImageMultiTransform
from nipype import config

from os.path import join as opj
MNI_template = Info.standard_image('MNI152_T1_1mm_brain.nii.gz')
from nipype import config

cfg = dict(execution={'remove_unnecessary_outputs': False,
                     'keep_inputs': True})
config.update_config(cfg) 

regScratchDir = "/data/HCP_Data/run_hcp_reg_pipeline_addDtiWarp/"

# """
# Setup for DataGrabber inputs needed for the registration pipeline; This is using the freesurfer nodif and t1 masks
# """
ds = nio.DataGrabber(infields=['subject_id'],
    outfields=['nodif_brain','nodif_brain_mask','struct','struct_mask','struct_brain'])

datasource = pe.Node(interface=ds,name="datasource")
# create a node to obtain the functional images
datasource.inputs.base_directory = "/data/HCP_Data/HCP_BedpostData/"
datasource.inputs.template ='*'
datasource.inputs.sort_filelist = True
datasource.inputs.field_template = dict(
    nodif_brain='%s/T1w/Diffusion/nodif_brain.nii*',
    nodif_brain_mask='%s/T1w/Diffusion/nodif_brain_mask.nii*',
    struct='%s/T1w/T1w_acpc_dc.nii*',
    struct_mask='%s/T1w/brainmask_fs.nii*', 
    struct_brain='%s/T1w/T1w_acpc_dc_masked.nii*'
)

# datasource.base_dir="/data/HCP_Data/NipypeScratch/datasource_cache_v2"
datasource.inputs.template_args = dict(
             nodif_brain = [['subject_id']],
             nodif_brain_mask =  [['subject_id']],
             struct =  [['subject_id']],
             struct_mask = [['subject_id']],
             struct_brain = [['subject_id']] )

subjRootDir = "/data/HCP_Data/HCP_BedpostData/"
FULL_SUBJECT_LIST = [x for x in os.listdir(subjRootDir) if os.path.isdir( subjRootDir+x+'/T1w/Diffusion.bedpostX')]
print(len(FULL_SUBJECT_LIST),"Subjects are potentially available to be processed!")

#FULL_SUBJECT_LIST = ["569965","123723","130518","188145","385046","176845","139435","728454","694362"]


"""
Setup for Registration  Pipeline InfoSource i.e. subjects
"""
subj_infosource = pe.Node(interface=util.IdentityInterface(fields=['subject_id']),  name="subj_infosource")
#infosource.iterables = ('subject_id', SampleSubjList)
subj_infosource.iterables = ('subject_id', FULL_SUBJECT_LIST)
### Above just converts the list of subjects into an iterable list I can connect to the next part of the pipeline

#roi = "/data/HCP_Data/EHECHT_ROIS/Human_Hypothalamus_Left.nii.gz"
roiList = glob.glob("/data/HCP_Data/EHECHT_ROIS/Human_*nii.gz")

#### RIGID BODY REGISTRATION OF DTI -- >  Struct Brain    using RegSynQuick
reg_DTI_to_Struct = pe.Node( RegistrationSynQuick(
                             num_threads=3,
                             transform_type='sr',output_prefix="dtiToStruct"),
                             name='reg_DTI_to_Struct')

reg_Struct_to_MNI = pe.Node( RegistrationSynQuick(
                             num_threads=6, fixed_image=MNI_template,output_prefix="structToMNI"),
                             name='reg_Struct_to_MNI')

warp_ROIs_MNI_to_DTI = pe.Node( WarpImageMultiTransform(invert_affine = [1,2],
                                    use_nearest=True,
                                    ), iterfield=['input_image'], name="warp_ROIs_MNI_to_DTI")

warp_ROIs_MNI_to_DTI.iterables = ('input_image', roiList)
## CREATE A DATASINK TO COPY OVER THE ROIS IN STANDARD SPACE-- ALSO COPY OVER THE XFMS IN FUTURE VERSION

datasink = pe.Node(nio.DataSink(), name='datasink')
datasink.inputs.base_directory = '/data/HCP_Data/HCP_BedpostData/addlInfo/'

datasink.inputs.substitutions = [ ('_subject_id_', ''), ('_input_image_..data..EHECHT_ROIS..', 'DTI_ROIs/'),
                                 ('Human_BasalForebrain_Bilat.nii.gz/',''),
                                 ('Human_BasalForebrain_Left.nii.gz/',''),
                                 ('Human_BasalForebrain_Right.nii.gz/',''),
                                 ('Human_Hypothalamus_Right.nii.gz/',''),
                                 ('Human_Hypothalamus_Left.nii.gz/',''),
                                 ('Human_Hypothalamus_Bilat.nii.gz/','')
                                ]

merge_xfms = pe.Node(util.Merge(3), name='merge_xfms')


run_hcp_reg  = pe.Workflow(name="run_hcp_reg_pipeline_redo")
run_hcp_reg.base_dir = regScratchDir

### Conneccts list ofls -al subjects to the data source generator
run_hcp_reg.connect(subj_infosource,'subject_id',datasource,'subject_id')

## Connect inputs for registering the DTI to Structural Image (Rigid Registration)
run_hcp_reg.connect( datasource,'struct_brain',reg_DTI_to_Struct,'fixed_image')
run_hcp_reg.connect( datasource,'nodif_brain',reg_DTI_to_Struct,'moving_image')

## Connect the inputs for registering Structural to MNI 1mm template-- template is specified in fxn
run_hcp_reg.connect( datasource,'struct_brain',reg_Struct_to_MNI,'moving_image')

run_hcp_reg.connect( reg_Struct_to_MNI, "inverse_warp_field", merge_xfms, "in1"    )
run_hcp_reg.connect( reg_Struct_to_MNI, "out_matrix",merge_xfms, "in2"   )

run_hcp_reg.connect( reg_DTI_to_Struct, "out_matrix",merge_xfms, "in3"   )
## So order of matrices being applied is inverse warp field(S->M), affine (S-M) Inverted, then Affine(DTI->S) Inverted

run_hcp_reg.connect( merge_xfms,  'out', warp_ROIs_MNI_to_DTI, 'transformation_series')
run_hcp_reg.connect( datasource, 'nodif_brain', warp_ROIs_MNI_to_DTI, 'reference_image')

### Copy the files to a datasink
run_hcp_reg.connect(subj_infosource,'subject_id',datasink,'subject')
    
run_hcp_reg.connect(warp_ROIs_MNI_to_DTI,'output_image',datasink,'subject.@ROIs')

run_hcp_reg.connect(reg_Struct_to_MNI,'forward_warp_field',datasink,'subject.@fwd_warp')
run_hcp_reg.connect(reg_Struct_to_MNI,'inverse_warp_field',datasink,'subject.@inv_warp')
run_hcp_reg.connect(reg_Struct_to_MNI,'out_matrix',datasink,'subject.@affine_mtx')

run_hcp_reg.connect( reg_DTI_to_Struct, "out_matrix",datasink, "subject.@dtiToStructMat"   )
run_hcp_reg.connect( reg_DTI_to_Struct, "out_matrix",merge_xfms, "subject.@dtiToStruct_fdwwarp"   )
run_hcp_reg.connect( reg_DTI_to_Struct, "out_matrix",merge_xfms, "subject.@dtiToStruct_invwarp"   )

run_hcp_reg.connect( warp_ROIs_MNI_to_DTI,"output_image",datasink,"subject.@roisInDTISpace")

#run_hcp_reg.write_graph()
run_hcp_reg.run(plugin='MultiProc', plugin_args={'n_procs' : 30})


Image('/data/HCP_Data/NipypeScratch/run_hcp_reg_pipeline/run_hcp_reg_pipeline/graph.png')                    

