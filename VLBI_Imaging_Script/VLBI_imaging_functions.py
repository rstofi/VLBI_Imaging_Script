import os; #for Linux terminal commands
import numpy as np; #numeric python library
import math; #for negative power function
import subprocess; #for running difmap on Linux
import pylab; #for data reading
from astropy.io import fits; #for reading .fits file header

def data_setup(path_to_original_data,visibility_file):
	"""
	Moves the datafile to the working folder
	"""

	os.system('mv %s/%s .' %(path_to_original_data,visibility_file));
	
def header(visibility_file,show_header=False):
	"""
	Read .fits file header and return key informations.
	"""
	if not show_header:
		fits_header = fits.open(visibility_file);
		print(fits_header[0].header.keys);
		fits_header.close();
		
	source = fits.getval(visibility_file,'OBJECT');
	observation_date = fits.getval(visibility_file,'DATE-OBS');
	telescop = fits.getval(visibility_file,'TELESCOP');
	obs_freq = fits.getval(visibility_file,'CRVAL4');
		
	observation_parameters = np.asarray([source,telescop,observation_date,obs_freq]);
	
	return observation_parameters;

def difmap_imaging_script(visibility_file,
						output_name,
						clean_sigma,
						map_size,
						pixel_size,
						observation_length,
						**kwargs):
	"""
	This function creates the difmap imaging .log script
	"""
	
	
	if 'script_name' in kwargs:
		fn = open('%s.log' %kwargs['script_name'], 'a');
	else:	
		fn = open("difmap_imaging_script.log", "a");

	fn.write('''	!set imaging pypeline parameters
	!declare variables for imaging

	float clean_sigma; clean_sigma  = {clean_sigma}
	float map_size; map_size = {map_size}
	float pixel_size; pixel_size = {pixel_size}
	float observation_length; observation_length = {observation_length}

	float signal_to_noise_p;
	float signal_to_noise_a;
		
	!Imaging

	observe {obj_file}
	select i
	mapsize map_size,pixel_size

	startmod "",1
	uvw 2,0
	peakwin 1.5
	clean 100,0.05
	selfcal false,false,0

	!if snr > clean_sigma more calibration steps will be done

	!clean-selfcal calibration:
	if(peak(flux,max)/imstat(rms) > clean_sigma)
		repeat;\
			peakwin 1.5; clean; selfcal
		until(peak(flux,max)/imstat(rms) < clean_sigma)
	end if

	uvw 2,-1

	!clean-selfcal calibration:
	if(peak(flux,max)/imstat(rms) > clean_sigma)
		repeat;\
			peakwin 1.5; clean; selfcal
		until(peak(flux,max)/imstat(rms) < clean_sigma)
	end if

	uvw 0,-1

	!clean-selfcal calibration:
	if(peak(flux,max)/imstat(rms) > clean_sigma)
		repeat;\
			peakwin 1.5; clean; selfcal
		until(peak(flux,max)/imstat(rms) < clean_sigma)
	end if

	gscale

	!here one should use tlpot to determine the true value of actual_time

	!observation time domain calibration:
	signal_to_noise_p = peak(flux,max)/imstat(rms)
	repeat;\
		selfcal true,true,observation_length
		signal_to_noise_a = peak(flux,max)/imstat(rms)
		if(peak(flux,max)/imstat(rms) > clean_sigma)
			if(signal_to_noise_a <= signal_to_noise_p)
				peakwin 1.5; clean; selfcal
			observation_length=observation_length/2
				signal_to_noise_a = signal_to_noise_p
			end if
			if(signal_to_noise_a > signal_to_noise_p)
				clrmod false,true
			observation_length=observation_length/2
				signal_to_noise_a = signal_to_noise_p
			end if
		else
			observation_length=observation_length/2
		end if
	until(observation_length < 2)

	selfcal true,true,0

	delwin
	clean 1000,0.01
	device /NULL
	mapl
	cmul=3*imstat(rms)

	!Save image
	!device {obj}.ps/vcps
	device {obj}.ps/vps
	mapl clean, false 

	!get clean image and beam statistics
	print "MARKING_STRING"
	print peak(flux)
	print imstat(rms)
	print cmul
	print imstat(bmin)
	print imstat(bmaj)
	print imstat(bpa)
	print "END_MARKING"

	!save clean map into a fits file
	save {obj}

	!quit from difmap
	quit'''.format(obj_file=visibility_file,
				obj=output_name,
				clean_sigma=clean_sigma,
				map_size=map_size,
				pixel_size=pixel_size,
				observation_length=observation_length));

	fn.close();

def difmap_modeling_script(visibility_file,
						output_name,
						clean_sigma,
						map_size,
						pixel_size,
						observation_length,
						model_sigma,
						phi,
						major_axis,
						minor_axis,
						model_type,
						model_iter,
						max_jet_component_number,
						**kwargs):
	"""
	This function creates the difmap modeling .log script
	"""
	
	
	if 'script_name' in kwargs:
		fn = open('%s.log' %kwargs['script_name'], 'a');
	else:	
		fn = open("difmap_modeling_script.log", "a");

	fn.write('''	!set imaging pypeline parameters
	!declare variables for imaging

	float clean_sigma; clean_sigma  = {clean_sigma}
	float map_size; map_size = {map_size}
	float pixel_size; pixel_size = {pixel_size}
	float observation_length; observation_length = {observation_length}

	float signal_to_noise_p;
	float signal_to_noise_a;

	!declare variables for model fitting

	float model_sigma; model_sigma = {model_sigma};

	float phi; phi = {phi};
	float major_axis; major_axis = {major_axis};
	float minor_axis; minor_axis = {minor_axis};
	float m_type; m_type = {m_type};
	float model_iter; model_iter = {model_iter};
		
	!Imaging

	observe {obj_file}
	select i
	mapsize map_size,pixel_size

	startmod "",1
	uvw 2,0
	peakwin 1.5
	clean 100,0.05
	selfcal false,false,0

	!if snr > clean_sigma more calibration steps will be done

	!clean-selfcal calibration:
	if(peak(flux,max)/imstat(rms) > clean_sigma)
		repeat;\
			peakwin 1.5; clean; selfcal
		until(peak(flux,max)/imstat(rms) < clean_sigma)
	end if

	uvw 2,-1

	!clean-selfcal calibration:
	if(peak(flux,max)/imstat(rms) > clean_sigma)
		repeat;\
			peakwin 1.5; clean; selfcal
		until(peak(flux,max)/imstat(rms) < clean_sigma)
	end if

	uvw 0,-1

	!clean-selfcal calibration:
	if(peak(flux,max)/imstat(rms) > clean_sigma)
		repeat;\
			peakwin 1.5; clean; selfcal
		until(peak(flux,max)/imstat(rms) < clean_sigma)
	end if

	gscale

	!here one should use tlpot to determine the true value of actual_time

	!observation time domain calibration:
	signal_to_noise_p = peak(flux,max)/imstat(rms)
	repeat;\
		selfcal true,true,observation_length
		signal_to_noise_a = peak(flux,max)/imstat(rms)
		if(peak(flux,max)/imstat(rms) > clean_sigma)
			if(signal_to_noise_a <= signal_to_noise_p)
				peakwin 1.5; clean; selfcal
			observation_length=observation_length/2
				signal_to_noise_a = signal_to_noise_p
			end if
			if(signal_to_noise_a > signal_to_noise_p)
				clrmod false,true
			observation_length=observation_length/2
				signal_to_noise_a = signal_to_noise_p
			end if
		else
			observation_length=observation_length/2
		end if
	until(observation_length < 2)

	selfcal true,true,0

	delwin
	clean 1000,0.01
	device /NULL
	mapl
	cmul=3*imstat(rms)

	!Save image
	!device {obj}.ps/vcps
	!device {obj}.ps/vps
	!mapl clean, false 

	!Modeling

	clrmod true

	!Fit first (elliptical-gaussian) component

	addcmp peak(flux),true,peak(x),peak(y),true,{major_axis},true,{minor_axis},true,{phi},true,{m_type}
	modelfit model_iter

	!Fit other (cirle-gaussian) components
	i = 0
	repeat;\
		i = i + 1
		if(peak(flux)/imstat(rms) > model_sigma)
			addcmp peak(flux),true,peak(x),peak(y),true,1,false,1,false,{phi},true,1
			modelfit model_iter
		end if
	until(i >= {max_loop})

	!Image with model components
	!device {obj}.ps/vcps
	device {obj}.ps/vps
	mapl clean, true 

	!get clean image and beam statistics
	print "MARKING_STRING"
	print peak(flux)
	print imstat(rms)
	print cmul
	print imstat(bmin)
	print imstat(bmaj)
	print imstat(bpa)
	print "END_MARKING"

	!Write model components parameters to a .mod file
	wmod {obj}.mod

	!save modelfit map
	save {obj}

	!quit from difmap
	quit'''.format(obj_file=visibility_file,
				obj=output_name,
				clean_sigma=clean_sigma,
				map_size=map_size,
				pixel_size=pixel_size,
				observation_length=observation_length,
				model_sigma=model_sigma,
				phi=phi,
				major_axis=major_axis,
				minor_axis=minor_axis,
				m_type=model_type,
				model_iter=model_iter,
				max_loop=max_jet_component_number));

	fn.close();

def run_difmap_imaging_script(script_name,show_difmap_output=False):
	"""
	This function run the difmap imaging script using Linux terminal.
	"""
	
	shell_run_command = 'echo @%s.log | difmap' %script_name;
	
	if not show_difmap_output:
		shell_run_command += " >/dev/null"
	
	os.system(shell_run_command);

def get_image_parameters_from_log(difmap_output='difmap.log',beam_err=0.1):
	"""
	Get image parameters from difmap output logfile
	"""
	
	### use difmap.log for image parameters ###
	logfile = open(difmap_output, "r");

	### create a string from logfile between marking strings using the ! comment lines ###
	logf = "";
	
	marking = False;
	while True:
		line = logfile.readline();
		if line.find('! MARKING_STRING') != -1:
			marking = True;		
		elif marking == True:	
			if line.find('! END_MARKING') != -1:
				break;
			elif '!' in line:
				logf += line;
		if not line:break;
	
	### remove ! characters ###
	for char in logf:
            if char is '!':
                logf = logf.replace(char, '');
	
	### create a list with the image values ###
	logf = logf.split(' ');#create list from string
	logf = filter(str.strip, logf);#remove whitespace
	logf = list(map(float, logf));#set values to float
	
	### map parameters ###
	flux_peak = logf[0];#in Jy/beam
	map_rms = logf[1];#in Jy/beam
	cmul = logf[2]; #in Jy/beam -> Difmap use this value to create clean maps
	beam_min = logf[3]; 
	beam_max = logf[4];
	beam_angle = logf[5];
	
	bpa = np.radians(beam_angle) #convert degrees to radians

	### compute the axis intersections of the beam -> NEED CITATION! ###
	beamx = np.sqrt(np.power(beam_max,2)*np.power(beam_min,2)*(np.power(beam_max,2)*np.power(np.cos(bpa),2)+
					np.power(beam_min,2)*np.power(np.sin(bpa),2)))/(np.power(beam_max,2)*np.power(np.cos(bpa),2)+
					np.power(beam_min,2)*np.power(np.sin(bpa),2));
	beamy = np.sqrt(np.power(beam_max,2)*np.power(beam_min,2)*(np.power(beam_max,2)*np.power(np.sin(bpa),2)+
					np.power(beam_min,2)*np.power(np.cos(bpa),2)))/(np.power(beam_max,2)*np.power(np.sin(bpa),2)+
					np.power(beam_min,2)*np.power(np.cos(bpa),2));

	### compute the position error ###
	beamx = beamx*beam_err;
	beamy = beamy*beam_err;
	
	logfile.close();
	
	image_paramters = np.asarray([flux_peak,map_rms,cmul,beam_min,beam_max,beam_angle,beamx,beamy]);
	
	return image_paramters;

def get_model_parameters_from_mod(modfile_name):
	"""
	modelcomps is a matrix containing the propertyes of the fitted model components.
	Each row corresponds to a model component.
	The first colum is the flux below the component.
	The second column is the relative RA of the component.
	The third column is the relative DEC of the component.
	The fourt column is the major axis size (radius size if the component is circe).
	The fifth column is the axial ratio.
	The sixth column is the position angle (in radians from North -> East).
	The seventh column is the spec index.
	"""
	
	fmodelcomp = open('%s.mod' %modfile_name, 'r');

	modelcomps = '';
	while 1:
		line = fmodelcomp.readline();
		if '!' not in line:
			modelcomps += line;
		if not line:break;

	### remove v and \n characters ###
	for char in modelcomps:
		if char is 'v':
			modelcomps = modelcomps.replace(char, "");
		elif char is '\n':
			modelcomps = modelcomps.replace(char, " ");
	
	### create a list with the image values ###
	modelcomps = modelcomps.split(' ');#create list from string
	modelcomps = filter(str.strip, modelcomps);#remove whitespace
	modelcomps = list(map(float, modelcomps));#set values to float

	### compute model components RA and Dec coordinates ###
	j = len(modelcomps);
	i = 0;
	while i <= (j-(j/7)):
		r = modelcomps[i+1];
		theta = np.radians(modelcomps[i+2]);

		modelcomps[i+1] = r*np.sin(theta); #RA or x direction
		modelcomps[i+2] = r*np.cos(theta); #Dec or y direction

		x0 = modelcomps[1];
		y0 = modelcomps[2];

		modelcomps[i+1] = modelcomps[i+1]-x0;
		modelcomps[i+2] = modelcomps[i+2]-y0;

		i += 7;
	
	### create numpy matrix of model components parameters ###
	modelcomps = np.asarray(modelcomps);
	modelcomps = np.reshape(modelcomps,(int(modelcomps.size/7),7));
	
	fmodelcomp.close();
	
	return modelcomps;

def clear_output_files(input_script_name,
					output_file_name,
					keep_output_log=False,
					keep_fits=False,
					keep_par=False,
					keep_uvf=False,
					keep_mod=False,
					keep_ps=False,
					keep_python_build=False):
	"""
	Clear the used trash output files
	"""

	### remove difmap input logfile ###
	os.system('rm %s.log'%input_script_name);
		
	### remove output files ###
	if not keep_output_log:
		os.system('rm difmap.log');#remove difmap logfile
	if not keep_fits:
		os.system('rm %s/%s.fits' %(os.getcwd(),output_file_name));#remove clean .fits file
	if not keep_par:
		os.system('rm %s/%s.par' %(os.getcwd(),output_file_name));#remove .par file
	if not keep_uvf:
		os.system('rm %s/%s.uvf' %(os.getcwd(),output_file_name));#remove .uvf file
	if not keep_mod:
		os.system('rm %s/%s.mod' %(os.getcwd(),output_file_name));#remove .uvf file
	if not keep_ps:
		os.system('rm %s/%s.ps' %(os.getcwd(),output_file_name));#remove .uvf file	
	if not keep_python_build:
		os.system('rm -r __pycache__');#remove tha python build folder __pycache__

def data_organizer(path_to_original_data,
				visibility_file,
				output_file_name=False,
				copy_output_log=False,
				copy_fits=False,
				copy_par=False,
				copy_uvf=False,
				copy_mod=False,
				copy_ps=False,
				**kwargs):
	"""
	Organize the output data
	"""
	
	### move the datafile back to it's original folder ###
	os.system('mv %s %s' %(visibility_file,path_to_original_data));
	
	### move other output files ###
	if output_file_name:
		if copy_output_log:
			if 'path_output_log' in kwargs and 'output_log_newname' in kwargs:
				os.system('mv difmap.log %s/%s' %(kwargs['path_output_log'],kwargs['output_log_newname']));
		if copy_fits:
			if 'path_fits' in kwargs:
				os.system('mv %s.fits %s' %(output_file_name,kwargs['path_fits']));
		if copy_par:
			if 'path_par' in kwargs:
				os.system('mv %s.par %s' %(output_file_name,kwargs['path_par']));
		if copy_par:
			if 'path_uvf' in kwargs:
				os.system('mv %s.uvf %s' %(output_file_name,kwargs['path_uvf']));
		if copy_par:
			if 'path_mod' in kwargs:
				os.system('mv %s.mod %s' %(output_file_name,kwargs['path_mod']));
		if copy_par:
			if 'path_ps' in kwargs:
				os.system('mv %s.ps %s' %(output_file_name,kwargs['path_ps']));
