#!/usr/bin/python
import os
import glob
import shutil
import subprocess
import sys
import nipype.interfaces.fsl as fsl
import nipype.pipeline.engine as pe
import nipype.interfaces.utility as util
import nipype.interfaces.io as nio
## basic python script to move and copy over files to help me do bedpost and basic scripts on goodman data...
from nipype.workflows.dmri.fsl.dti import create_eddy_correct_pipeline, create_bedpostx_pipeline



original_source_data_dir = '/data/dgutman/NIPYPE_WD/wf_dcm2nii/_subject_id_'
working_data_dir = '/bigdata2/NIPYPE_WD/GOODMAN_DATA/'

SUBJECT_LIST = ['HOMADAMSubjectP320_20100331', 'HOMADAMSubjectP337_20110120', 'CIDAR3SubjectP311_Scan1_20090709',
	'HOMADAMSubjectP321_20100405', 'HOMADAMSubjectP338_20110228', 'CIDARProject3HOMADAMSubjectP307_20080905',
	'HOMADAMSubjectP322_20100428', 'HOMADAMSubjectP339_20110714', 'CIDARPROJECT3SubjectP312_20090731',
	'HOMADAMSubjectP326_20100528', 'HOMADAMSubjectP342_20110829', 'HOMADAM_P341_20110812', 'HOMADAMSubjectP327_20100624', 
	'HOMADAMSubjectP344_20110919', 'HOMADAMSubjectP305_20080806', 'HOMADAMSubjectP330_20100727', 'HOMADAMSubjectP346_20111102',
	'HOMADAMSubjectP315_20091112', 'HOMADAMSubjectP331_20100817', 'HOMADAMSubjectP347_20111025', 'HOMADAMSubjectP316_20091123',
	'HOMADAMSubjectP334_20101203', 'HOMADAMSubjectP348_20111027', 'HOMADAMSubjectP318_20091207', 'HOMADAMSubjectP335_20101213',
	'HOMADAMSubjectP350_20111103', 'HOMADAMSubjectP319_20091130', 'HOMADAMSubjectP336_20101217', 'HOMADAMSubjP302_20080710']
print len(SUBJECT_LIST),"entries to process"


SUBJECTS_NEEDING_EC = []  ### I am using both explcit scriping and nipype to perform some of the preprocessing...
			  ## largely depending what is/was easier for me to read...


def move_dti_files_from_nipype(source_dir,target_dir,subject_name):
	target_dir= target_dir+subject_name+'/dti/'
	###first file to move is *bitcdiffnEchoesAP*.nii or it's equivalent---
	## need to see if the dti data exists in the source directory

	dti_source_file = glob.glob(source_dir+subject_name+'/dti_dcm2nii/2*bitcdiffnEchoesAP*.nii')
	print dti_source_file
	if len(dti_source_file) > 1:
		print "More than one dti  file located...."
	 	sys.exit()	
	bvec_file = glob.glob(source_dir+subject_name+'/dti_dcm2nii/2*bitcdiffnEchoesAP*.bvec')
	print bvec_file
	if len(bvec_file) > 1:
		print "More than one bvec file located...."
	 	sys.exit()	
	bval_file = glob.glob(source_dir+subject_name+'/dti_dcm2nii/2*bitcdiffnEchoesAP*.bval')
	print bval_file
	if len(bval_file) > 1:
		print "More than one bval file located...."
	 	sys.exit()	



	if os.path.isfile(dti_source_file[0]):
		print "Subject",subject_name,"has DTI data..."
		if not os.path.isfile(target_dir+'raw_data.nii'): 
			if not os.path.isdir(target_dir): os.makedirs(target_dir)  ### need to make output directory if it's not there
			shutil.copyfile(dti_source_file[0],target_dir+'raw_data.nii')
		if not os.path.isfile(target_dir+'bvecs'): 
			shutil.copyfile(bvec_file[0],target_dir+'bvecs')
		if not os.path.isfile(target_dir+'bvals'): 
			shutil.copyfile(bval_file[0],target_dir+'bvals')
	else:
		print "Subject",subject_name,"did not have a DTI file...."



for subj in SUBJECT_LIST:
	print "Processing subject",subj
	move_dti_files_from_nipype(original_source_data_dir,working_data_dir,subj)



### first set up basic preprocessing for DTI work..

computeTensor = pe.Workflow(name='computeTensor')

fslroi = pe.Node(interface=fsl.ExtractROI(),name='fslroi')
fslroi.inputs.t_min=0
fslroi.inputs.t_size=1


bet = pe.Node(interface=fsl.BET(),name='bet')
bet.inputs.mask=True
bet.inputs.frac=0.34  ## may need to adjust...

eddycorrect = create_eddy_correct_pipeline('eddycorrect')
eddycorrect.inputs.inputnode.ref_num=0

dtifit = pe.Node(interface=fsl.DTIFit(),name='dtifit')


computeTensor.connect([
                        (fslroi,bet,[('roi_file','in_file')]),
                        (eddycorrect, dtifit,[('outputnode.eddy_corrected','dwi')]),
                        (infosource, dtifit,[['subject_id','base_name']]),
                        (bet,dtifit,[('mask_file','mask')])
                      ])
sys.exit()


gen_fa = pe.Workflow(name="gen_fa")
gen_fa.base_dir = working_data_dir

eddy_correct  = create_eddy_correct_pipeline()
eddy_correct.inputs.inputnode.ref_num = 0
subject_id_infosource = pe.Node(util.IdentityInterface(fields=['subject_id']),
                                name='subject_id_infosource')
subject_id_infosource.iterables = ('subject_id', SUBJECT_LIST)

datasource = pe.Node(interface=nio.DataGrabber(infields=['subject_id'],
                                               outfields=['dwi', 'bvec',
                                                          'bval']),
                     name='datasource')
datasource.inputs.base_directory = working_data_dir 
datasource.inputs.template = '%s/dti/%s'
datasource.inputs.template_args = dict(dwi=[['subject_id', 'raw_data.nii']],
                                       bvec=[['subject_id', 'bvecs']],
                                       bval=[['subject_id', 'bvals']])
gen_fa.connect(subject_id_infosource, 'subject_id', datasource, 'subject_id')

eddy_correct = create_eddy_correct_pipeline()
eddy_correct.inputs.inputnode.ref_num = 0
gen_fa.connect(datasource, 'dwi', eddy_correct, 'inputnode.in_file')

bet = pe.Node(interface=fsl.BET(), name='bet')
bet.inputs.mask = True
bet.inputs.frac = 0.2
gen_fa.connect(eddy_correct, 'pick_ref.out', bet, 'in_file')

dtifit = pe.Node(interface=fsl.DTIFit(), name='dtifit')
gen_fa.connect(eddy_correct, 'outputnode.eddy_corrected', dtifit, 'dwi')
gen_fa.connect(subject_id_infosource, 'subject_id', dtifit, 'base_name')
gen_fa.connect(bet, 'mask_file', dtifit, 'mask')
gen_fa.connect(datasource, 'bvec', dtifit, 'bvecs')
gen_fa.connect(datasource, 'bval', dtifit, 'bvals')

datasink = pe.Node(interface=nio.DataSink(), name="datasink")
datasink.inputs.base_directory = os.path.join(os.path.abspath(working_data_dir),
                                              'sri_results')
datasink.inputs.parameterization = False
gen_fa.connect(dtifit, 'FA', datasink, 'FA')
gen_fa.connect(dtifit, 'MD', datasink, 'MD')

### FA map and MD maps are generated--- also want to actually run tractography...




tractography = pe.Workflow(name='tractography')

#bedpostx.connect("
#bedpostx.	

flirt = pe.Node(interface=fsl.FLIRT(), name='flirt')
flirt.inputs.in_file = fsl.Info.standard_image('MNI152_T1_2mm_brain.nii.gz')
flirt.inputs.dof = 12

bedpostx = create_bedpostx_pipeline()
bedpostx.get_node("xfibres").iterables = ("n_fibres",[1,2])


tractography.add_nodes(['bedpostx','flirt'])


#tractography.connect('datasource','bvecs', 'bedpostx', 'bvecs')
#tractography.connect('datasource','bvals', 'bedpostx', 'bvals')
#tractography.connect('eddy_correct','eddy_corrected', 'bedpostx', 'dwi')
#tractography.connect('bet','mask_filed', 'bedpostx', 'mask')




if __name__ == '__main__':
    gen_fa.write_graph()
    gen_fa.run(plugin='MultiProc', plugin_args={'n_procs': 24})
