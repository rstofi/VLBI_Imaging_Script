from VLBI_imaging_functions import *;

difmap_imaging_script(visibility_file='J0017+8135_S_1998_10_01_pus_vis.fits',object_name='J0017+8135_S_1998_10_01',clean_sigma=6,map_size=512,pixel_size=0.3,observation_length=900,script_name='test_run');

run_difmap_imaging_script(script_name='test_run');
