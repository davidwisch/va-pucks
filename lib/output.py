import os
import time

from lib import helpers

def output_dir_info(options, base_dir, num_bins):
	file = open(os.path.join(base_dir, "DIR_INFO.txt"), "w")
	file.write("Date & Time: %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S")))
	file.write("Avg. Puck Mass: %s\n" % (options.puck_mass))
	file.write("Table Angle: %s\n" % (options.table_angle))
	file.write("Motor Power: %s\n" % (options.driver_power))
	file.write("Frame Interval: %s\n" % (options.frame_interval))
	file.write("Num Bins: %s\n" % (num_bins))
	file.write("\nDistribution Information stored in ./bincounts.txt\n")
	file.close()

def output_bin_points(upper_bins, lower_bins, filename):
	bin_file = open(filename, "w")
	for i in range(len(upper_bins)):
		bin_file.write("%s %s\n" % (upper_bins[i][0], upper_bins[i][1]))
	for i in range(len(lower_bins)):
		bin_file.write("%s %s\n" % (lower_bins[i][0], lower_bins[i][1]))
	bin_file.close()

def output_bin_lines(upper_bins, lower_bins, filename):
	bin_file = open(filename, "w")
	for binno in range(len(upper_bins)):
		divisions = 10
		up_bin = upper_bins[binno]
		low_bin = lower_bins[binno]
		slope = helpers.find_slope(up_bin, low_bin)
		x_dist = abs(up_bin[0] - low_bin[0])
		y_dist = abs(up_bin[1] - low_bin[1])
		dx = x_dist / divisions
		for i in range(divisions):
			x =low_bin[0] + (dx * i)
			y = low_bin[1] + (slope * (dx * i))
			bin_file.write("%s %s\n" % (x, y))
	bin_file.close()

def output_2d_array(arr, filename):
	arr_file = open(filename, "w")
	for val in arr:
		arr_file.write("%s %s\n" % (val[0], val[1]))
	arr_file.close()

def output_bin_data(bins, filename):
	bin_file = open(filename, "w")
	for bin in bins:
		print "%s => %s" % (bin, bins[bin])
		if bin == None: continue
		bin_file.write("%s %s\n" % (bin, bins[bin]))
	bin_file.close()

def dump_video(cmd):
	os.system(cmd)

def output_gnuplot(filename, *plot_files):
	dat_file = open(filename, "w")
	out_str = "plot '%s' " % (plot_files[0])
	for f in plot_files[1:]:
		out_str += ", '%s'" % (f)
	dat_file.write(out_str)
	dat_file.close()

def output_heatmap(gnuplot_cmd, grid, base_dir):
	#output data file
	dat_file = open(os.path.join(base_dir, "datfile.txt"), "w")
	for x in range(grid.shape[0]):
		for y in range(grid.shape[1]):
			dat_file.write("%s %s %s\n" % (x, y, grid[x, y]))
		dat_file.write("\n")
	dat_file.close()

	#output gnuplot config file
	config = open(os.path.join(base_dir, "gnuplot.config"), "w")
	config.write("set view map\n")
	config.write("set contour base\n")
	config.write("set output '%s'\n" % (os.path.join(base_dir, "heatmap.png")))
	config.write("set term png\n")
	config.write("splot '%s' w pm3d t \"\"\n" % (os.path.join(base_dir, "datfile.txt")))
	config.write("set terminal windows\n")
	config.close()
	os.system("%s \"%s\"" % (gnuplot_cmd, os.path.join(base_dir, "gnuplot.config")))

def output_distribution(gnuplot_cmd, distribution, base_dir):
	filename_title = "distribution.png"
	filename = os.path.join(base_dir, filename_title)
	#output data file
	dat_filename = os.path.join(base_dir, filename_title) + ".txt"
	dat_file = open(dat_filename, "w")
	for binno in range(len(distribution)):
		try:
			dat_file.write("%s %s\n" % (binno, distribution[binno]))
		except(KeyError):
			dat_file.write("%s %s\n" % (binno, 0))
	dat_file.close()

	#output gnuplot config file
	config = open(os.path.join(base_dir, "gnuplot_dist.config"), "w")
	config.write("set output '%s'\n" % (filename))
	config.write("set term png\n")
	config.write("plot '%s' t \"\"\n" % (dat_filename))
	config.write("set terminal windows\n")
	config.close()
	os.system("%s \"%s\"" % (gnuplot_cmd, os.path.join(base_dir, "gnuplot_dist.config")))

	return filename
