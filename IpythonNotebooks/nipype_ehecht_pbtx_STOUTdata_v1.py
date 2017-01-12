#!/usr/bin/python

"""
This is the ehecht DATA Set
===============
dMRI [DTI, FSL]
===============
This pipeline example that uses several interfaces to perform analysis on
diffusion weighted images using FSL FDT tools.

I stripped out the bedpostX generation part and modified the dti_dti_datasource
to point directory to a bedpostX directory
"""
import nipype.interfaces.io as nio           # Data i/o
import nipype.interfaces.fsl as fsl          # fsl
import nipype.interfaces.utility as util     # utility
import nipype.pipeline.engine as pe          # pypeline engine
import os                                    # system functions
import glob
import sys

fsl.FSLCommand.set_default_output_type('NIFTI_GZ')

RAWDATAPATH='/GLOBAL_SCRATCH/ERIN_TEST_DATA/Stout_Human/'
WORKINGDATAPATH='/GLOBAL_SCRATCH/ERIN_TEST_DATA/STOUT_WD/'

### Could also simply autodetect this from the path...
subject_list = ['Subj01_Scan1','Subj01_Scan2','Subj01_Scan3', 'Subj02_Scan1', 'Subj02_Scan2a', \
'Subj02_Scan2b', 'Subj03_Scan1',  'Subj03_Scan2a', 'Subj03_Scan2b', 'Subj03_Scan3', 'Subj04_Scan1', \
'Subj05_Scan1', 'Subj05_Scan2', 'Subj05_Scan3', 'Subj06_Scan1', 'Subj06_Scan2a',  'Subj06_Scan2b' ]


subj_list = [ x for x in os.listdir(RAWDATAPATH) if 'Subj' in x ]
subject_list = subj_list  ### building a larger subject list

"""
Setting up workflows
--------------------
This is a generic workflow for DTI data analysis using the that I have adapted for  Ehecht Stout
"""
print len(subject_list),"entries to process"

"""
Map field names to individual subject runs
"""

infosource = pe.Node(interface=util.IdentityInterface(fields=['subject_id']),    name="infosource")
infosource.iterables = ('subject_id', subject_list)
### Above just converts the list of subjects into an iterable list I can connect to the next part of the pipeline

info = dict(
             bvecs = [['subject_id','bvecs']],
            bvals = [['subject_id','bvals']],
             thsamples = [['subject_id','th1samples']],
             phsamples =  [['subject_id','ph1samples']],
             fsamples =  [['subject_id','f1samples']]   ,
             nodif_brain_mask = [['subject_id','nodif_brain_mask']],
             nodif_to_struct_aff =   [['subject_id','nodif_12dof_struc.mat']],
	     struct_warpto_MNI = [['subject_id', 'struc_warp_MNI_warpfield.nii.gz']],
	     struct_to_nodif_aff = [['subject_id','struc_12dof_nodif.mat']],
             MNI_to_struct = [['subject_id','MNI_warp_struc_warpfield.nii.gz']]
                                 )

#             seed_region_base_dir = [['subject_id']],
##             xfm_base_dir = [['subject_id']],

### Generate the files/names for the DTI/bedpostX data
dti_datasource = pe.Node(interface=nio.DataGrabber(infields=['subject_id'], outfields=info.keys() ),   name='dti_datasource')
dti_datasource.inputs.base_directory = RAWDATAPATH
dti_datasource.inputs.template = "*"
dti_datasource.inputs.sort_filelist=True
dti_datasource.inputs.field_template = dict( nodif_brain_mask = '%s/DTI/data/%s.nii.gz',
        bvecs='%s/DTI/data/%s', bvals='%s/DTI/data/%s',  
  thsamples='%s/DTI/data.bedpostX/merged_%s.nii.gz', phsamples='%s/DTI/data.bedpostX/merged_%s.nii.gz',
  fsamples='%s/DTI/data.bedpostX/merged_%s.nii.gz', nodif_to_struct_aff = '%s/xfms/%s', 
		struct_warpto_MNI='%s/xfms/%s', struct_to_nodif_aff='%s/xfms/%s', MNI_to_struct='%s/xfms/%s'
     )
dti_datasource.inputs.template_args = info

# roi_datasource = pe.Node(interface=nio.DataGrabber(infields=['subject_id'],outfields = ['seed_rois'],  name='roi_datasource')
# roi_datasource.inputs.base_directory = RAWDATAPATH
# roi_datasource.inputs.template = "*"
# roi_datasource.inputs.field_template = {'seed_rois': '%s/ROIs/warped_ROIs_in_cropped_struct_space/Bar*.nii.gz'   }
# roi_datasource.inputs.template_args = {'seed_rois': [['subject_id']] }


"""
Setup for Tracktography
-----------------------
Here we will create a generic workflow for DTI computation, this workflow assumes the .bedpostX has already been run...
Here we will create a workflow to enable probabilistic tracktography and hard segmentation of the seed region
"""
stout_tractography = pe.Workflow(name='stout_tractography')
stout_tractography.base_dir = WORKINGDATAPATH

### First connect the subject list to the workflow to build up the patient lists
stout_tractography.connect( infosource,'subject_id',dti_datasource, 'subject_id' )

### GENERATE THE WARP FIELDS
cvtwarp_mni_to_dti = pe.Node(interface=fsl.ConvertWarp(),name='cvtwarp_mni_to_dti' )
cvtwarp_mni_to_dti.inputs.reference = os.path.join(RAWDATAPATH,"MNI152_T1_1mm_brain.nii.gz")

stout_tractography.connect( dti_datasource, 'nodif_to_struct_aff', cvtwarp_mni_to_dti, 'premat')
stout_tractography.connect( dti_datasource, 'struct_warpto_MNI', cvtwarp_mni_to_dti, 'warp1')

# $statement .= " --premat=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/nodif_12dof_struc.mat ";
# $statement .= " --warp1=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/struc_warp_MNI_warpfield.nii.gz ";
# $statement .= " --out=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/nodif_12dof_struc_warp_MNI_warpfield.nii.gz ";

cvtwarp_dti_to_mni = pe.Node(interface=fsl.ConvertWarp(),name='cvtwarp_dti_to_mni'  )
stout_tractography.connect( dti_datasource, 'nodif_brain_mask', cvtwarp_dti_to_mni, 'reference')
stout_tractography.connect( dti_datasource, 'MNI_to_struct', cvtwarp_dti_to_mni, 'warp1')
stout_tractography.connect( dti_datasource, 'struct_to_nodif_aff', cvtwarp_dti_to_mni, 'postmat')

# $statement .= " --ref=$WORKINGDATAPATH/" . $subj[$i] . "/DTI/data/nodif_brain_mask.nii.gz ";
# $statement .= " --warp1=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/MNI_warp_struc_warpfield.nii.gz ";
# $statement .= " --postmat=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/struc_12dof_nodif.mat ";
# $statement .= " --out=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/MNI_warp_struc_12dof_nodif_warpfield.nii.gz ";

#PERFORM PROBALISTIC TRACTOGRAPHY

pbx2 = pe.Node(interface=fsl.ProbTrackX2(),name='pbx2')
pbx2.inputs.c_thresh = 0.2
pbx2.inputs.n_steps=2000
pbx2.inputs.step_length=0.5
pbx2.inputs.n_samples= 5000 ### Make n_samples an iterable field...
pbx2.inputs.opd=True
pbx2.inputs.loop_check=True
pbx2.inputs.omatrix2=True  ##This requires I include target2
pbx2.inputs.correct_path_distribution=True ##corresponds to the --pd flag
pbx2.inputs.onewaycondition=True  
pbx2.inputs.target2= os.path.join(RAWDATAPATH,"MNI152_T1_1mm_brain_mask_downsample_2.nii.gz")
pbx2.inputs.rand_fib=0

### This will eventually become an iterable
pbx2.inputs.seed= [os.path.join(RAWDATAPATH,"ROIs/Human_IFG-vPrCG_L.nii.gz"),os.path.join(RAWDATAPATH,"ROIs/Human_IFG-vPrCG_R.nii.gz")]


# roi_list = [x for x in os.path.join(RAWDATAPATH,"ROIs/Human_*/*.nio.gz")]

# $statement  = " probtrackx2 --pd --onewaycondition --omatrix2 ";
# $statement .= " -s $WORKINGDATAPATH/" . $subj[$i] . "/DTI/data.bedpostX/merged "; 
# $statement .= " -m $WORKINGDATAPATH/" . $subj[$i] . "/DTI/data/nodif_brain_mask.nii.gz ";
# $statement .= " -x $WORKINGDATAPATH/ROIs/Human_" . $roi[$r] . "_" . $hemi[$h] . ".nii.gz ";
# $statement .= " --target2=$WORKINGDATAPATH/MNI152_T1_1mm_brain_mask_downsample_2.nii.gz ";
# $statement .= " -l -c 0.2 -S 2000 --steplength=0.5 -P 5000 --fibthresh=0.1 --randfib=0 ";  # check samples 
# $statement .= " --xfm=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/MNI_warp_struc_12dof_nodif_warpfield.nii.gz ";
# $statement .= " --invxfm=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/nodif_12dof_struc_warp_MNI_warpfield.nii.gz ";
# $statement .= " --forcedir --opd ";
# $statement .= " --dir=$OUTPUTDATAPATH/" . $subj[$i] . "_" . $roi[$r] . "_" . $hemi[$h] . "_Segmentation  ";

stout_tractography.connect( dti_datasource,'thsamples',pbx2,'thsamples')
stout_tractography.connect( dti_datasource,'phsamples',pbx2,'phsamples')
stout_tractography.connect( dti_datasource,'fsamples',pbx2,'fsamples')
stout_tractography.connect( dti_datasource,'nodif_brain_mask',pbx2,'mask')

### Now connect the warps generated from the previous steps

stout_tractography.connect( cvtwarp_dti_to_mni, 'out_file',pbx2,'xfm')
stout_tractography.connect( cvtwarp_mni_to_dti, 'out_file',pbx2,'inv_xfm')

# preuss_tractography.connect( roi_datasource, 'seed_rois',probtrackx,'seed')
#preuss_tractography.connect( seed_mask_ds,'out_files',probtrackx,'seed')
#preuss_tractography.connect( dti_dti_datasource, ('subject_id',mask_info),probtrackx,'seed')

"""
Setup data storage area for results
"""
datasink = pe.Node(interface=nio.DataSink(),name='datasink')

stout_tractography.connect( pbx2, 'fdt_paths', datasink, 'fdt_paths')
stout_tractography.connect( pbx2, 'matrix1_dot', datasink, 'matrix1.txt')
stout_tractography.connect( pbx2, 'matrix2_dot', datasink, 'matrix2.txt')
stout_tractography.connect( pbx2, 'matrix3_dot', datasink, 'matrix3.txt')
stout_tractography.connect( pbx2, 'lookup_tractspace', datasink, 'lookup_ts')
stout_tractography.connect( pbx2, 'way_total', datasink, 'waytotal.txt')


#datasink.inputs.base_directory = put_cleaned_up_results_here
#datasink.inputs.substitutions = [('_subject_id_', ''),
#                                 ('_seed_..bigdata2..NIPYPE_WD..SANCHEZ_WD..', '')]

if __name__ == '__main__':
    stout_tractography.write_graph(format='eps')
    #stout_tractography.export_graph()
    # stout_tractography.run(plugin='MultiProc', plugin_args={'n_procs': 28})
    #dwiproc.run(plugin='PBS', plugin_args = dict(qsub_args='-k oe -q batch ') )
    stout_tractography.run(plugin='PBS', plugin_args=dict(qsub_args='-e trq_logs -o trq_logs -q batch '))

"""


###WORKINGDATAPATH

# $statement  = " convertwarp ";
# $statement .= " --ref=$WORKINGDATAPATH/MNI152_T1_1mm_brain.nii.gz ";
# $statement .= " --premat=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/nodif_12dof_struc.mat ";
# $statement .= " --warp1=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/struc_warp_MNI_warpfield.nii.gz ";
# $statement .= " --out=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/nodif_12dof_struc_warp_MNI_warpfield.nii.gz ";
# print "$statement \n";

# $statement  = " convertwarp ";
# $statement .= " --ref=$WORKINGDATAPATH/" . $subj[$i] . "/DTI/data/nodif_brain_mask.nii.gz ";
# $statement .= " --warp1=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/MNI_warp_struc_warpfield.nii.gz ";
# $statement .= " --postmat=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/struc_12dof_nodif.mat ";
# $statement .= " --out=$WORKINGDATAPATH/" . $subj[$i] . "/xfms/MNI_warp_struc_12dof_nodif_warpfield.nii.gz ";
# print "$statement \n";

# print "$statement \n";
"""
