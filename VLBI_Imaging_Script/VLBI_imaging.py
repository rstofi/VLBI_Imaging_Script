from VLBI_imaging_functions import *;

### Test header ###
#header(visibility_file='J0017+8135_S_1998_10_01_pus_vis.fits');

### Imaging script ###
'''
difmap_imaging_script(visibility_file='J0017+8135_S_1998_10_01_pus_vis.fits',
					output_name='J0017+8135_S_1998_10_01',
					clean_sigma=6,
					map_size=512,
					pixel_size=0.3,
					observation_length=900,
					script_name='test_run');

run_difmap_imaging_script(script_name='test_run');
#'''

### Modelling script ###
#'''
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
#'''

### Get image parameters from difmap output ###
image_parameters = get_image_parameters_from_log();

print(image_parameters);

modelcomps = get_model_parameters_from_mod(modfile_name='J0017+8135_S_1998_10_01');

print(modelcomps);
