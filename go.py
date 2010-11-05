import os
import sys
import time
import datetime

from lib import helpers
from lib import analyze
from lib import output
from lib import cli

BINARIES = "bin"
MPLAYER = os.path.join(BINARIES, "mencoder", "mplayer.exe")
PIL_INSTALLER = os.path.join(BINARIES, "installers", "PIL-1.1.7.win32-py2.6.exe")	
NUMPY_INSTALLER = os.path.join(BINARIES, "installers","numpy-1.3.0-win32-superpack-python2.6.exe")
GNUPLOT = os.path.join(BINARIES, "gnuplot", "bin", "wgnuplot.exe")
USER_OUTPUT_DIR = os.path.join(os.getenv('USERPROFILE'), 'Desktop')
OUTPUT_DIR = "output"

def check_deps():
	print "Checking Dependencies..."
	#check that mplayer.exe is around
	sys.stdout.write("Checking for mplayer...")
	if os.path.exists(MPLAYER):
		sys.stdout.write("FOUND\n")
	else:
		sys.stdout.write("MISSING\n")
		exit("ERROR: mplayer.exe was not found")
	
	sys.stdout.write("Checking for PIL...")
	try:
		import Image
		sys.stdout.write("FOUND\n")
	except:
		sys.stdout.write("MISSING\n")
		print 'Launching PIL installer in 3 seconds...'
		time.sleep(3)
		os.system(PIL_INSTALLER)
		exit("Exiting...relaunch when ready")
		
	sys.stdout.write("Checking for numpy...")
	try:
		import numpy
		sys.stdout.write("FOUND\n")
	except:
		sys.stdout.write("MISSING\n")
		print "Launching NumPy installer in 3 seconds..."
		time.sleep(3)
		os.system(NUMPY_INSTALLER)
		exit('Exiting...relaunch when ready')

	return True

def init_dirs():
	if not os.path.exists(OUTPUT_DIR):
		os.mkdir(OUTPUT_DIR)
	if not os.path.exists(USER_OUTPUT_DIR):
		os.mkdir(USER_OUTPUT_DIR)

if __name__ == "__main__":
	#Check dependencies
	check_deps()

	#parse the command line arguments
	options = cli.parse()

	#set number of bins
	if options.num_bins:
		NUM_BINS = options.num_bins
	else:
		NUM_BINS = 15

	#finish constructing USER_OUTPUT_DIR var
	folder_name = "%s.%s.%s.%s.%s.%s" % (
		str(datetime.date.today()),
		options.frame_interval,
		options.driver_power,
		options.table_angle,
		options.puck_mass,
		NUM_BINS
	)
	USER_OUTPUT_DIR = os.path.join(USER_OUTPUT_DIR, folder_name)

	init_dirs()
	output.output_dir_info(options, USER_OUTPUT_DIR, NUM_BINS)

	if not os.path.exists(options.video):
		exit("ERROR: Cannot find video file")

	#dump video to images
	CMD = "%s %s -nosound -speed 10.0 -vf framestep=%s -vo jpeg:outdir=%s:quality=80" % (MPLAYER, options.video, options.frame_interval, OUTPUT_DIR)
	if len(os.listdir(OUTPUT_DIR)) == 0:
		print "Dumping video to images... ( BE PATIENT )"
		time.sleep(2)
		output.dump_video(CMD)
		print "Dump complete"	
	else:
		print "Output Directory not empty"
		delete = raw_input("Empty? [n/Y] ")
		if delete == "Y":
			helpers.cleanup(OUTPUT_DIR)
			output.dump_video(CMD)

	files = os.listdir(OUTPUT_DIR)
	print "Num Files:", len(files)

	bins = {}
	timesteps = []
	framesize = None
	failed_reads = 0
	total_pucks = 0

	for i in range(len(files)):

		filename = os.path.join(OUTPUT_DIR, files[i])
		puck_points, corner_points, frame_size = analyze.analyze_frame(filename, options)
		if not framesize:
			framesize = frame_size

		if len(corner_points) < 4:
			failed_reads += 1

			print "Unable to process frame %s/%s" % (i, len(files))
			continue

		upper_right, lower_right, lower_left, upper_left = analyze.find_corners(corner_points)

		if (upper_right is None or
			lower_right is None or
			lower_left is None or
			upper_left is None):
			failed_reads += 1

			print "Unable to process frame %s/%s" % (i, len(files))
			continue

		total_pucks += len(puck_points)

		#line between upper points
		upper_bins = helpers.get_upper_bins(upper_left, upper_right, NUM_BINS)

		#line between lower points
		lower_bins = helpers.get_lower_bins(lower_left, lower_right, NUM_BINS)

		#bin our data
		bins = analyze.bin_data(bins, puck_points, upper_bins, lower_bins)

		#save timestep
		timesteps.append(puck_points)

		if options.explicit:
			#write out bin points
			filename_bins = os.path.join(USER_OUTPUT_DIR, files[i]+'.bp.txt')
			output.output_bin_points(upper_bins, lower_bins, filename_bins)

			#writeout bin lines
			filename_lines = os.path.join(USER_OUTPUT_DIR, files[i]+'.bl.txt')
			output.output_bin_lines(upper_bins, lower_bins, filename_lines)

			#writeout puck points
			filename_points  = os.path.join(USER_OUTPUT_DIR, files[i]+".pt.txt")
			output.output_2d_array(puck_points, filename_points)

			#writeout corner points
			filename_corners = os.path.join(USER_OUTPUT_DIR, files[i]+".cp.txt")
			output.output_2d_array(corner_points, filename_corners)

			#Create gnuplot file for plotting everything
			filename_gnuplot = os.path.join(USER_OUTPUT_DIR, files[i]+'.gnuplot')
			output.output_gnuplot(
					filename_gnuplot,
					filename_bins,
					filename_lines,
					filename_points,
					filename_corners
					)

	filename = os.path.join(USER_OUTPUT_DIR, "bincounts.txt")
	output.output_bin_data(bins, filename)

	#output heatmap
	heatmap = analyze.generate_heatmap(timesteps, framesize)
	output.output_heatmap(GNUPLOT, heatmap, USER_OUTPUT_DIR)

	#Output distribution plot
	distribution = analyze.generate_distribution(bins)
	dist_filename = output.output_distribution(GNUPLOT, distribution, USER_OUTPUT_DIR)

	print "Processed %s / %s" % (len(files) - failed_reads, len(files))
	try:
		print "Avg pucks detected/image: %s" % (total_pucks / (len(files)-failed_reads))
	except(ZeroDivisionError):
		pass
	print "Avg Puck Mass: %s" % (options.puck_mass)
	print "Table Angle: %s" % (options.table_angle)
	print "Driver Motor Power: %s" % (options.driver_power)
	print "Frame Interval: %s" % (options.frame_interval)
	print "Number of Bins: %s" % (NUM_BINS)
	print "Output Directory: %s" % (USER_OUTPUT_DIR)
	print "Raw Output is: %s" % (os.path.join(os.getcwd(), OUTPUT_DIR))
