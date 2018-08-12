def get_nii_image_info(nifti_input_file):
	import nibabel as nib
	img = nib.load(nifti_input_file)
	img_shape =  img.get_shape()
	img_header = img.get_header()['pixdim'][1:4]
	dim_x = img_shape[0]
	dim_y = img_shape[1]
	dim_z = img_shape[2]
	vox_size_x = img_header[0]
	vox_size_y = img_header[1]
	vox_size_z = img_header[2]
	""" May be a better way to do this, but I also compute the plane with the highest resolution
	which in theory should represent the image acquisition plane, but of course you can always
	resample the image and break these assumptions"""
	image_orientation = ""    ## I guess in theory this will fail to yield a value in the event
				  ## someone cut/resized/did something weird to the acquistion window
				  ## it of course doesn't HAVE to be a square matrix for the inplane
				  ## probably could just figure out the smallest axis which should
				  ## refer to the Sliced dimension
	if(    dim_x  == dim_y ): image_orientation = 'axial'
	elif(  dim_y  == dim_z ): image_orientation = 'sagittal'
	elif(  dim_x  == dim_z ): image_orientation = 'coronal'
	return dim_x, dim_y, dim_z, vox_size_x, vox_size_y, vox_size_z, image_orientation



def normalize_image(nifti_input_file):
	#from nipype.interfaces.fsl import ImageStats
	from nipype.interfaces import fsl
	""" This will take an image and scale it so the mean intensity is 100 ...."""
	
	stats=fsl.ImageStats(in_file=nifti_input_file, op_string= '-R')
	stats_results = stats.run()
	### so the -R flag outputs the min and max robust intensity value
#	print stats_results.outputs[1]
	# So this gets messy quickly...
	normalize_image = fsl.ImageMaths(in_file=nifti_input_file, op_string= ' -div '+
		str(stats_results.outputs.out_stat[1])	+' -mul 1000')
	run_image_norm = normalize_image.run()
	return run_image_norm.outputs.out_file
