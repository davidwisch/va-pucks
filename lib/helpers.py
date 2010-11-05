import os
import sys
import time
import math

import helpers

def percent_diff(num1, num2):
	return (abs(num1-num2)/((num1+num2) * 0.5)) * 100.0
	
def find_slope(point1, point2):
	#try/cactch is pretty much a hack in this instance
	#the exception should never be thrown if program is calibrated
	#correctly.
	try:
		return (float(point2[1]) - float(point1[1])) / (float(point2[0]) - float(point1[0]))
	except(ZeroDivisionError):
		return 1000000

def find_distance(point1, point2):
	return math.sqrt((float(point1[0])-float(point2[0]))**2.0 + (float(point1[1])-float(point2[1]))**2.0)
	
def unique(good_points, point, width):
	for p in good_points:
		if helpers.find_distance(point, p) < width:
			return False
	return True

def find_bin(point, upper_bins, lower_bins):
	for binno in range(len(upper_bins)):
		if binno+1 == len(upper_bins):
			break
		slope_left = find_slope(lower_bins[binno], upper_bins[binno])
		slope_right = find_slope(lower_bins[binno+1], upper_bins[binno+1])

		left_x = ((point[1] - lower_bins[binno][1]) / slope_left) + lower_bins[binno][0]
		right_x = ((point[1] - lower_bins[binno+1][1]) / slope_right) + lower_bins[binno+1][0]

		if left_x < point[0] and right_x > point[0]:
			return binno
		elif binno == 0 and point[0] < left_x:
			return binno
	return None

def get_upper_bins(upper_left, upper_right, NUM_BINS):
	upper_bins = []
	dist = helpers.find_distance(upper_left, upper_right)
	bin_width = dist / NUM_BINS
	slope = helpers.find_slope(upper_left, upper_right)
	x = upper_left[0]
	for binno in range(NUM_BINS):
		bin_y = upper_left[1] + (slope * x)
		upper_bins.append( (x, bin_y) )
		x += bin_width
	return upper_bins

def get_lower_bins(lower_left, lower_right, NUM_BINS):
	lower_bins = []
	dist = helpers.find_distance(lower_left, lower_right)
	bin_width = dist / NUM_BINS
	slope = helpers.find_slope(lower_left, lower_right)
	x = lower_left[0]
	for binno in range(NUM_BINS):
		bin_y = lower_left[1] + (slope * x)
		lower_bins.append( (x, bin_y) )
		x += bin_width
	return lower_bins

def cleanup(directory):
	print "Deleting files in: ", directory
	files = os.listdir(directory)
	for f in files:
		f = os.path.join(directory, f)
		os.unlink(f)
	print "Done"
