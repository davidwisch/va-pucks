import math

import Image
import numpy

from lib import helpers

def bin_data(bins, points, upper_bins, lower_bins):
	for p in points:
			bin = helpers.find_bin(p, upper_bins, lower_bins)
			if bin in bins:
				bins[bin] += 1
			else:
				bins[bin] = 1
	return bins

def analyze_frame(filename, options):
	puck_points = []
	corner_points = []

	image = Image.open(filename)
	width, height = image.size
	data = image.load()

	#puck_width = 26.0 #in pixels
	puck_width = 18.0
	bin_width = puck_width * 2.5

	#set corner RGB values
	if options.cornerRGB:
		CORNERS = (
			options.cornerRGB[0],
			options.cornerRGB[1],
			options.cornerRGB[2]
		)
	else:
		CORNERS = (210, 117, 84)

	#set puck RGB values
	if options.puckRGB:
		PUCKS = (
			options.puckRGB[0],
			options.puckRGB[1],
			options.puckRGB[2]
		)
	else:
		PUCKS = (28, 101, 74)

	#set the corner threshold
	if options.cornerThresh:
		CORNER_THRESH = options.cornerThresh
	else:
		CORNER_THRESH = 15

	#set the puck threshold
	if options.puckThresh:
		PUCK_THRESH = options.puckThresh
	else:
		PUCK_THRESH = 23

	for y in range(height):
		for x in range(width):
			pixel = data[x, y]
			if (helpers.percent_diff(pixel[0], CORNERS[0]) < CORNER_THRESH and
				helpers.percent_diff(pixel[1], CORNERS[1]) < CORNER_THRESH and
				helpers.percent_diff(pixel[2], CORNERS[2]) < CORNER_THRESH):
				if helpers.unique(corner_points, (x, y), bin_width) and x > 150:
					corner_points.append( (x, y) )
			if (helpers.percent_diff(pixel[0], PUCKS[0]) < PUCK_THRESH and
				helpers.percent_diff(pixel[1], PUCKS[1]) < PUCK_THRESH and
				helpers.percent_diff(pixel[2], PUCKS[2]) < PUCK_THRESH):
				if helpers.unique(puck_points, (x, y), puck_width):
					puck_points.append( (x, y) )
	return puck_points, corner_points, image.size

def generate_distribution(bin_counts):
	for binno in range(len(bin_counts)):
		try:
			bin_counts[binno] = math.log(bin_counts[binno])
		except(KeyError):
			bin_counts[binno] = 0
	return bin_counts

def find_corners(corner_points):
	upper_right = None
	lower_right = None
	lower_left = None
	upper_left = None
	
	for p in corner_points:
		if p[0] > 400 and p[1] < 300:
			upper_right = p
		elif p[0] > 400 and p[1] > 300:
			lower_right = p
		elif p[0] < 400 and p[1] < 300:
			upper_left = p
		else:
			lower_left = p
			
	return upper_right, lower_right, lower_left, upper_left

def generate_heatmap(timesteps, framesize):
	DIMX = 75
	DIMY = 50
	dx = framesize[0] / DIMX
	dy = framesize[1] / DIMY
	grid = numpy.zeros((DIMX, DIMY), "float32")
	for points in timesteps:
		for point in points:
			x,y = point[0], point[1]
			bin_x = int(x / dx)
			bin_y = int(y / dy)

			#try/cactch is pretty much a hack in this instance
			#the exception should never be thrown if program is calibrated
			#correctly.
			try:
				grid[bin_x, bin_y] += 1
			except(IndexError):
				continue
	return grid
