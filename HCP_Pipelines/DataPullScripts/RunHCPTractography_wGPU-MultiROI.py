import nipype
import os,glob,sys,shutil
import nipype.interfaces.fsl as fsl
import nipype.pipeline.engine as pe
import nipype.interfaces.utility as util
import nipype.interfaces.io as nio
from IPython.display import Image

from nipype import config
# cfg = dict(execution={'remove_unnecessary_outputs': False,
#                      'keep_inputs': True},
#           monitoring={'enabled': True,
#                       'sample_frequency': 5})


#get_ipython().system(u'probtrackx2')

subjRootDir = "/data/HCP_BedpostData/"
FULL_SUBJECT_LIST = [x for x in os.listdir(subjRootDir) if os.path.isdir( subjRootDir+'/addlInfo/subject/'+x)]
print(len(FULL_SUBJECT_LIST),"Subjects are potentially available to be processed!")

"""
Setup for Probtrackx2 Computational Pipeline
"""
subj_infosource = pe.Node(interface=util.IdentityInterface(fields=['subject_id']),  name="subj_infosource")
#infosource.iterables = ('subject_id', SampleSubjList)
subj_infosource.iterables = ('subject_id', FULL_SUBJECT_LIST)
### Above just converts the list of subjects into an iterable list I can connect to the next part of the pipeline


# """
# Setup for DataGrabber inputs needed for probtrackx2
# """
datasource = pe.Node(interface=nio.DataGrabber(infields=['subject_id'],
        outfields=['nodif_brain_mask','thsamples','phsamples','fsamples','mniROIs']),
        name='datasource')
# create a node to obtain the functional images
datasource.inputs.base_directory = "/data/HCP_BedpostData/"
datasource.inputs.template ='*'
datasource.inputs.sort_filelist = True
datasource.inputs.field_template = dict(
    thsamples='%s/T1w/Diffusion.bedpostX/merged_%s.nii*',
    fsamples='%s/T1w/Diffusion.bedpostX/merged_%s.nii*',
    phsamples='%s/T1w/Diffusion.bedpostX/merged_%s.nii*',
    nodif_brain_mask='%s/T1w/Diffusion.bedpostX/%s.nii*', 
    mniROIs='addlInfoV2/subject/%s/DTI_ROIs/Human_*_trans.nii.gz'
    )

datasource.inputs.template_args = dict(
             thsamples = [['subject_id','th1samples']],
             phsamples =  [['subject_id','ph1samples']],
             fsamples =  [['subject_id','f1samples']],
             nodif_brain_mask = [['subject_id','nodif_brain_mask']],
            mniROIs=[['subject_id']]
        )

pbx2 = pe.MapNode(interface=fsl.ProbTrackX2(), name='pbx2', iterfield=['seed'])
pbx2.inputs.c_thresh = 0.2   # -c 0.2   F cutoff
pbx2.inputs.n_steps = 2000   # -S 2000
pbx2.inputs.step_length = 0.5 # --steplength=0.5
pbx2.inputs.n_samples = 25000  # -P 5000
pbx2.inputs.opd = True
pbx2.inputs.loop_check = True
pbx2.inputs.correct_path_distribution = True # -pd  i.e. distance correction


#runpbx.connect(subj_infosource,'subject_id',datasource,'subject_id')
runpbx2  = pe.Workflow(name="runpbx2_gpu_dtispace_fixedwarps")
runpbx2.base_dir = "/data/NipypeScratch/"

samples_base_name_fxn = lambda x : x.replace('_th1samples.nii.gz','')

runpbx2.connect(subj_infosource,'subject_id',datasource,'subject_id')

# ### Connect the dti_datasource to the pbx2 command
runpbx2.connect( datasource,'thsamples',pbx2,'thsamples')
runpbx2.connect( datasource,'phsamples',pbx2,'phsamples')
runpbx2.connect( datasource,'fsamples',pbx2,'fsamples')
runpbx2.connect( datasource,'nodif_brain_mask',pbx2,'mask')
runpbx2.connect( datasource, ('thsamples', samples_base_name_fxn ), pbx2,'samples_base_name') ###  NOTE THIS IS A WEIRD TUPLE IS


runpbx2.connect( datasource,'mniROIs', pbx2,'seed')  #pbx2 is a mapnode, so it will run each ROI separately
#runpbx2.run(plugin='MultiProc', plugin_args={'n_procs' : 1})
runpbx2.run()

graphFile = runpbx2.write_graph(graph2use='orig',simple_form=False)


#print(gen_fa.write_graph(graph2use='colored',simple_form=False))
#Image('/data/HCP_Data/NipypeScratch/gen_fa/graph.png')
#Image('/data/HCP_Data/NipypeScratch/gen_fa/graph.png')

