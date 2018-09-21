import nipype
import os,glob,sys,shutil
import nipype.interfaces.fsl as fsl
import nipype.pipeline.engine as pe
import nipype.interfaces.utility as util
import nipype.interfaces.io as nio
from IPython.display import Image

subjRootDir = "/data/HCP_BedpostData/"
FULL_SUBJECT_LIST = [x for x in os.listdir(subjRootDir) if os.path.isdir( subjRootDir+x+'/T1w/Diffusion')]
print(len(FULL_SUBJECT_LIST),"Subjects are potentially available to be processed!")


subject_id_infosource = pe.Node(util.IdentityInterface(fields=['subject_id']),
                                name='subject_id_infosource')
subject_id_infosource.iterables = ('subject_id', FULL_SUBJECT_LIST)

datasource = pe.Node(interface=nio.DataGrabber(infields=['subject_id'],
                                               outfields=['dwi', 'bvec', 'bval']),
                                                 name='datasource')
datasource.inputs.base_directory = subjRootDir 
datasource.inputs.sort_filelist = True
datasource.inputs.template = '%s/T1w/Diffusion/%s'
datasource.inputs.template_args = dict(dwi=[['subject_id', 'data.nii.gz']],
                                       bvecs=[['subject_id', 'bvecs']],
                                       bvals=[['subject_id', 'bvals']],
                                       nodif_brain_mask=[['subject_id','nodif_brain_mask.nii.gz']])
## Just mapped each subject to the corresponding bvec,bvals, brain mask and preprocessed DWI data
### Create the Node for DTIFIT
dtifit = pe.Node(interface=fsl.DTIFit(), name='dtifit')


gen_fa = pe.Workflow(name="gen_fa")
gen_fa.base_dir = '/data/NipypeScratch/'
gen_fa.connect(subject_id_infosource, 'subject_id', datasource, 'subject_id')

gen_fa.connect(subject_id_infosource, 'subject_id', dtifit, 'base_name')
gen_fa.connect(datasource, 'bvecs', dtifit, 'bvecs')
gen_fa.connect(datasource, 'bvals', dtifit, 'bvals')
gen_fa.connect(datasource, 'nodif_brain_mask', dtifit, 'mask')
gen_fa.connect(datasource, 'dwi', dtifit, 'dwi')

datasink = pe.Node(interface=nio.DataSink(), name="datasink")
datasink.inputs.base_directory = os.path.join('/data/NipypeScratch/',
                                              'dtifit_results')
datasink.inputs.parameterization = False
gen_fa.connect(dtifit, 'FA', datasink, 'FA')
gen_fa.connect(dtifit, 'MD', datasink, 'MD')
gen_fa.connect(dtifit, 'V1', datasink, 'V1')
gen_fa.connect(dtifit, 'V2', datasink, 'V2')
gen_fa.connect(dtifit, 'V3', datasink, 'V3')
gen_fa.connect(dtifit, 'L1', datasink, 'L1')
gen_fa.connect(dtifit, 'L2', datasink, 'L2')
gen_fa.connect(dtifit, 'L3', datasink, 'L3')


print(gen_fa.write_graph(graph2use='colored',simple_form=False))
#Image('/data/NipypeScratch/gen_fa/graph.png')
#Image('/data/HCP_Data/NipypeScratch/gen_fa/graph.png')


gen_fa.run(plugin='MultiProc', plugin_args={'n_procs' : 40})

