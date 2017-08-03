from VLBI_imaging_functions import *;

###
#The most simple usage of the library:
#working with one file within the same directory
#fit model components to the (imaged) visibility data
#the script create no output (remove them)
#and print the fitted model component parameters
###

### Modelling script ###
difmap_modeling_script(visibility_file='J0017+8135_S_1998_10_01_pus_vis.fits',
					output_name='J0017+8135_S_1998_10_01',
					clean_sigma=6,
					map_size=512,
					pixel_size=0.3,
					observation_length=900,
					model_sigma=6,
					phi=0,
					major_axis=0.02,
					minor_axis=1,
					model_type=1,
					model_iter=10,
					max_jet_component_number=2,
					script_name='model_test_run');

run_difmap_imaging_script(script_name='model_test_run');

### Get image and modelfit parameters from difmap output ###
image_parameters = get_image_parameters_from_log();
#print(image_parameters);

modelcomps = get_model_parameters_from_mod(modfile_name='J0017+8135_S_1998_10_01');
print(modelcomps);

### clear output and logfiles ###
clear_output_files(input_script_name='model_test_run',output_file_name='J0017+8135_S_1998_10_01');
