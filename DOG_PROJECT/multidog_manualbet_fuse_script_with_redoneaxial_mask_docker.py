__author__ = 'dgutman' 
"""" This script will take a very disorganized set of axial that had a mask manually drawn in the axial plain, as well as sagittal dog images  
and register and reorient them so the data can be used for later averaging

The mask doesn't have to be perfect, but should be fairly close and not include excessive 
amounts of neck

Dropbox\DOG_PROJECT\RAW_UGA_DATA\DONE
each subject has a folder axial_mask with the brain mask in it.
and each base directory has the axial and sagittal mask...
 """

from glob import glob
import os, sys,re, optparse
import shutil
from nipype.interfaces.ants import N4BiasFieldCorrection
from nipype.interfaces.utility import Function

import nipype.pipeline.engine as pe
import nipype.interfaces.fsl as fsl
from nipype import config
from nipype.interfaces.utility import Function
import dg_nipype_lib
import nipype.interfaces.io as nio
import nipype.interfaces.utility as util
from nipype.interfaces.utility import Merge
config.stop_on_first_crash=True
import dog_nipye_functions as dnf

fsl.FSLCommand.set_default_output_type('NIFTI_GZ')

base_subject_directory = '/data/HCP_Data/DOG_BRAIN_AXL_SAG_DATA/RAW_UGA_DATA/DONE/'
"""all the input images are in there"""

working_dir = '/data/HCP_Data/NipypeScratch/DOG_PROJ_WORKING_DATA'

output_dir = '/data/HCP_Data/NipypeScratch/DOG_PROJECT/web_overview/'

SUBJECT_LIST = []
for dir in os.listdir(base_subject_directory):
	print(base_subject_directory,dir)
	if os.path.isdir( os.path.join(base_subject_directory,dir)) and 'UGA3T' in dir:
		SUBJECT_LIST.append(dir)
	else:
		print(dir,"is not a directory...")
print (len(SUBJECT_LIST),'subjects available to process')


### Define basic workflow here
dog_preproc_wf = pe.Workflow(name="dog_preproc_wf")
dog_preproc_wf.base_dir = working_dir

## DEFINE iterables for this workflow.. in this case I iterate through subjects
subject_infosource= pe.Node(interface=util.IdentityInterface(fields=["subject_id"]),
                        name="subject_infosource")
subject_infosource.iterables = ("subject_id",SUBJECT_LIST)


## Building input list which should have the axial and sagittal images
## and also pointing to the auto generated BET mask.... I am double checking to make sure
## we didn't cut off to much tissue

dogscan_datasource = pe.Node(nio.DataGrabber(infields=['subject_id'],outfields=['axl_t2','sag_t2','axial_bet_mask']),
        name="dog_axl_sag_datasource")

dogscan_datasource.inputs.base_directory = base_subject_directory 
dogscan_datasource.inputs.template ='*'
dogscan_datasource.inputs.field_template = { 'axl_t2': '%s/*/*axl-t2*.nii*', 'sag_t2': '%s/*/sag-t2*.nii*', 
		'axial_bet_mask' : '%s/*/axial_mask/*.hdr'	}

dogscan_datasource.inputs.template_args = { 'axl_t2' : [['subject_id']], 'sag_t2': [['subject_id']], 'axial_bet_mask': [['subject_id']]}
dog_preproc_wf.connect(subject_infosource,"subject_id",dogscan_datasource,"subject_id") 

## First do all the preprocessing on the axial image, basically crop it and also do N4 bias correction
## but I am only doing bias correction on the cropped image... will do a better job as I don't
## correct areas i am not going to use anyway..
### I am going to crop the BET'ed axial images  so I have a smaller working volume for registration
get_axial_crop_box = pe.Node(interface=fsl.ImageStats(),name='get_axial_crop_box')
get_axial_crop_box.inputs.op_string = '-w'
dog_preproc_wf.connect(dogscan_datasource,'axial_bet_mask',get_axial_crop_box,'in_file')
## ok now that I have the cropping box... I can use the fslroi command to acutlaly crop it...


#removed this step... seemed to better to apply the mask at the end.. trying to register the sagital to the cropped
## axial seemed messy
### nuts so to do this I need to mask the image first...
#apply_axial_bet_mask = pe.Node(interface=fsl.maths.ApplyMask(), name='apply_axial_bet_mask')
#dog_preproc_wf.connect(dogscan_datasource,'axl_t2',apply_axial_bet_mask,'in_file')
#dog_preproc_wf.connect(dogscan_datasource,'axial_bet_mask',apply_axial_bet_mask,'mask_file')


## Define the node to get the image dimensions...
image_dims = pe.Node( name="get_image_dims", interface=Function(input_names=['nifti_input_file'],
                output_names=['dim_x','dim_y','dim_z','vox_size_x','vox_size_x','vox_size_z','image_orientation'],
                function=dnf.get_nii_image_info ))
dog_preproc_wf.connect(dogscan_datasource,'axl_t2',image_dims,'nifti_input_file')

crop_axial_image    =pe.Node(interface=fsl.ExtractROI(),name='crop_axial_image')
list2str = lambda x: ' '.join([str(int(val)) for val in x])
dog_preproc_wf.connect(get_axial_crop_box,('out_stat',list2str),crop_axial_image,'args')
dog_preproc_wf.connect(dogscan_datasource,'axl_t2',crop_axial_image,'in_file')


crop_axial_mask_image    =pe.Node(interface=fsl.ExtractROI(),name='crop_axial_mask_image')
dog_preproc_wf.connect(get_axial_crop_box,('out_stat',list2str),crop_axial_mask_image,'args')
dog_preproc_wf.connect(dogscan_datasource,'axial_bet_mask',crop_axial_mask_image,'in_file')



resample_axial_mask_isotropic = pe.Node(interface=fsl.FLIRT(), name='resample_axial_mask_isotropic')

resample_axial_isotropic = pe.Node(interface=fsl.FLIRT(), name='resample_axial_isotropic')
## this is a trick from satra so I can pass the parameter
fmt_string = lambda x : '-applyisoxfm %.10f' % x
dog_preproc_wf.connect(image_dims,('vox_size_x',fmt_string),resample_axial_isotropic,'args')
#dog_preproc_wf.connect(dogscan_datasource,'axl_t2',resample_axial_isotropic,'in_file')
#dog_preproc_wf.connect(dogscan_datasource,'axl_t2',resample_axial_isotropic,'reference')
dog_preproc_wf.connect(crop_axial_image,'roi_file',resample_axial_isotropic,'in_file')
dog_preproc_wf.connect(crop_axial_image,'roi_file',resample_axial_isotropic,'reference')


dog_preproc_wf.connect(image_dims,('vox_size_x',fmt_string),resample_axial_mask_isotropic,'args')
dog_preproc_wf.connect(crop_axial_mask_image,'roi_file',resample_axial_mask_isotropic,'in_file')
dog_preproc_wf.connect(crop_axial_mask_image,'roi_file',resample_axial_mask_isotropic,'reference')

## so further complciationg things... I also have to crop out the non brian stuff..



## need to add the n4 bias node... at some point
#dog_preproc_wf.connect(axial_n4bias_node,'output_image',resample_axial_isotropic,'in_file')
#dog_preproc_wf.connect(axial_n4bias_node,'output_image',resample_axial_isotropic,'reference')





## first need to get it into the ~ orientation as the axial image..
swap_sagittal = pe.Node(interface=fsl.SwapDimensions(),name='swap_sagittal')
swap_sagittal.inputs.new_dims=('z','x','y')
swap_sagittal.inputs.output_type='NIFTI_GZ'
dog_preproc_wf.connect(dogscan_datasource,'sag_t2', swap_sagittal,'in_file')

### next step is to use the axial mask i generated and transform it to the sagittal image
## so I can crop the images and work with a smaller FOV.. also get better reg


## wILL DEBATE IF I REGISTER THE ORIGINAL IMAGE OR WORK WITH A CROPPED IMAGE... MAY NOT MATTER

reg_input_sagittal_to_axial = pe.Node(interface=fsl.FLIRT(), name='reg_input_sagittal_to_axial')
reg_input_sagittal_to_axial.inputs.dof = 6
reg_input_sagittal_to_axial.inputs.searchr_x = [-10,10]
reg_input_sagittal_to_axial.inputs.searchr_x = [-10,10]
reg_input_sagittal_to_axial.inputs.searchr_x = [-10,10]


dog_preproc_wf.connect(swap_sagittal,'out_file', reg_input_sagittal_to_axial,'in_file')
dog_preproc_wf.connect(dogscan_datasource,'axl_t2', reg_input_sagittal_to_axial,'reference')


### HERE i ACTUALLY INVERT THe transformation....
gen_axial_to_sag_xfm = pe.Node(interface=fsl.ConvertXFM(),name='gen_axial_to_sag_xfm')
gen_axial_to_sag_xfm.inputs.invert_xfm=True
dog_preproc_wf.connect(reg_input_sagittal_to_axial,'out_matrix_file',gen_axial_to_sag_xfm,'in_file')


""" So that I can deal with smaller volumes... I want to take the original axial mask Erin draw and back transform it to the sagital image... and then crop that image to a smaller box..."""

applyxfm_axlmask_to_sag = pe.Node(interface=fsl.preprocess.ApplyXFM(),name='applyxfm_axlmask_to_sag')
## so want to do the same steps... find the crude mask, crop the image and then register the smaller image area to the axial
dog_preproc_wf.connect(gen_axial_to_sag_xfm,'out_file',applyxfm_axlmask_to_sag,'in_matrix_file')
dog_preproc_wf.connect(dogscan_datasource,'axial_bet_mask',applyxfm_axlmask_to_sag,'in_file')
dog_preproc_wf.connect(swap_sagittal,'out_file',applyxfm_axlmask_to_sag,'reference')
applyxfm_axlmask_to_sag.inputs.apply_xfm=True
applyxfm_axlmask_to_sag.inputs.interp='nearestneighbour'
## I need to add nearesy neighbor interlpolation as well... otherwise I get wonky mask values


## so that erin only has to draw a single mask... I am applying the axial mask to the sagittal image...

get_sagittal_crop_box = pe.Node(interface=fsl.ImageStats(),name='get_sagittal_crop_box')
get_sagittal_crop_box.inputs.op_string = '-w'
dog_preproc_wf.connect(applyxfm_axlmask_to_sag,'out_file',get_sagittal_crop_box,'in_file')
## ok now that I have the cropping box... I can use the fslroi command to acutlaly crop it...

crop_sagittal_image    =pe.Node(interface=fsl.ExtractROI(),name='crop_sagittal_image')      

dog_preproc_wf.connect(get_sagittal_crop_box,('out_stat',list2str),crop_sagittal_image,'args')
dog_preproc_wf.connect(swap_sagittal,'out_file',crop_sagittal_image,'in_file')







## so now I need to try again to register the sagittal image to the axial... this time the image should be much smaller anyway..
reg_cropped_sagittal_to_axial = pe.Node(interface=fsl.FLIRT(), name='reg_cropped_sagittal_to_axial')
reg_cropped_sagittal_to_axial.inputs.dof = 6
reg_cropped_sagittal_to_axial.inputs.searchr_x = [-10,10]
reg_cropped_sagittal_to_axial.inputs.searchr_x = [-10,10]
reg_cropped_sagittal_to_axial.inputs.searchr_x = [-10,10]

dog_preproc_wf.connect(crop_sagittal_image,'roi_file', reg_cropped_sagittal_to_axial,'in_file')

dog_preproc_wf.connect(resample_axial_isotropic,'out_file', reg_cropped_sagittal_to_axial,'reference')
## Above will eventually change




normalize_axial_image_node = pe.Node( name="normalize_axial_image", interface=Function(input_names=['nifti_input_file'],
                output_names=['out_file'],                  
                function=dnf.normalize_image ))

normalize_sagittal_image_node = pe.Node( name="normalize_sagittal_image", interface=Function(input_names=['nifti_input_file'],
                output_names=['out_file'],
                function=dnf.normalize_image ))

dog_preproc_wf.connect(resample_axial_isotropic,'out_file', normalize_axial_image_node,'nifti_input_file')


dog_preproc_wf.connect(reg_cropped_sagittal_to_axial,'out_file', normalize_sagittal_image_node,'nifti_input_file')


average_images = pe.Node(interface=fsl.ImageMaths(), name="average_images")
average_images.inputs.op_string = '-add'

dog_preproc_wf.connect(normalize_axial_image_node,'out_file',average_images,'in_file')
dog_preproc_wf.connect(normalize_sagittal_image_node,'out_file' ,average_images,'in_file2')


apply_final_mask = pe.Node(interface=fsl.maths.ApplyMask(), name='apply_final_mask')


### nuts so to do this I need to mask the image first...

dog_preproc_wf.connect(average_images,'out_file',apply_final_mask,'in_file')
dog_preproc_wf.connect(resample_axial_mask_isotropic,'out_file',apply_final_mask,'mask_file')


#threshold_template_mask = pe.Node(interface=fsl.ImageMaths(op_string=' -thr 1.0'), name="threshold_template_mask")



slicer_midslice = pe.MapNode(interface=fsl.Slicer(), name="slicer_midslice",iterfield=['in_file'])
slicer_midslice.inputs.middle_slices = True

slicer_all_axial = pe.MapNode(interface=fsl.Slicer(), name="slicer_all_axial",iterfield=['in_file'])
slicer_all_axial.inputs.image_width = 1000
slicer_all_axial.inputs.sample_axial = 3

	

datasink = pe.Node(nio.DataSink(),name='datasink')
datasink.inputs.base_directory = output_dir


merge_node = pe.Node(interface=Merge(4), name='merge_node')
dog_preproc_wf.connect( normalize_axial_image_node,'out_file',merge_node,"in1")
dog_preproc_wf.connect( normalize_sagittal_image_node,'out_file',merge_node,"in2")
dog_preproc_wf.connect( average_images,'out_file',merge_node,"in3")
dog_preproc_wf.connect( apply_final_mask,'out_file',merge_node,"in4")

dog_preproc_wf.connect(merge_node,'out',slicer_midslice,'in_file')
#dog_preproc_wf.connect(merge_node,'out',slicer_all_axial,'in_file')
dog_preproc_wf.connect(slicer_midslice,'out_file',datasink,'png_files')
#dog_preproc_wf.connect(slicer_all_axial,'out_file',datasink,'axial_png_files')






dog_preproc_wf.write_graph()
#shutil.copy( os.path.join(working_dir,'dog_preproc_wf/graph.dot.png'),output_dir)

dog_preproc_wf.run(plugin='MultiProc', plugin_args={'n_procs' : 24 })

sys.exit()


## need to invert the rerference and the in_file... 
#register_template_to_cropped_axial = pe.Node(interface=fsl.FLIRT(), name = 'register_template_to_cropped_axial')
#register_template_to_cropped_axial.inputs.in_file = '/data/dgutman/Dropbox/DOG_PROJECT/Erin_9dogtemplate.nii.gz'
#dog_preproc_wf.connect(crop_axial_image,'roi_file', register_template_to_cropped_axial,'reference')


### before I apply the registered high dof mask... I actually need to threshold it...
### FSL will include ANY value that is > 0 in the mask and so there are so 1e-15 values so the mask is includnig extra stuff

#threshold_template_mask = pe.Node(interface=fsl.ImageMaths(op_string=' -thr 1.0'), name="threshold_template_mask")
#dog_preproc_wf.connect(highdof_register_template_to_cropped_axial,'out_file',threshold_template_mask,'in_file')

## I am debating if I should dilate the mask one value first... thoughts???...


#dog_preproc_wf.connect(crop_axial_image,'roi_file',apply_template_mask,'in_file')
#dog_preproc_wf.connect(threshold_template_mask,'out_file',apply_template_mask,'mask_file')


axial_n4bias_node = pe.Node(interface=N4BiasFieldCorrection(), name='n4bias_node')
axial_n4bias_node.inputs.dimension = 3
axial_n4bias_node.inputs.bspline_fitting_distance = 300
axial_n4bias_node.inputs.shrink_factor = 3
axial_n4bias_node.inputs.n_iterations = [50,50,30,20]
axial_n4bias_node.inputs.convergence_threshold = 1e-6
#dog_preproc_wf.connect(apply_template_mask,'out_file',axial_n4bias_node,'input_image')


## now I am going to apply the template masked image...which in this case is the 12 DOF warped image..




### so this workflow is quite botched... the mask I am trying to apply isn't registered to the axial image

### I am going to crop the BET'ed axial images  so I have a smaller working volume for registration







#dog_preproc_wf.connect(threshold_template_mask,'out_file',apply_final_mask,'mask_file')
## this won't work.. image would have to be sliced isotorpically.. oops


### I am now going to invert this XFM to I have the axial--> SAGITTAL transformation for the original image...

#dog_preproc_wf.write_graph(graph2use='flat',simple_form=True)

sys.exit()


shutil.copy('/data/dgutman/DOG_PROJECT_working_dir/dog_preproc_wf/graph.dot.png',output_dir)



