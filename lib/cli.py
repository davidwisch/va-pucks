import optparse


#Following two calsses are taken from: http://code.activestate.com/recipes/573441-extended-optparse-to-allow-definition-of-required-/
strREQUIRED = 'required'

class OptionWithDefault(optparse.Option):
	ATTRS = optparse.Option.ATTRS + [strREQUIRED]

	def __init__(self, *opts, **attrs):
		if attrs.get(strREQUIRED, False):
			attrs['help'] = '(Required) ' + attrs.get('help', "")
		optparse.Option.__init__(self, *opts, **attrs)

class OptionParser(optparse.OptionParser):
	def __init__(self, **kwargs):
		kwargs['option_class'] = OptionWithDefault
		optparse.OptionParser.__init__(self, **kwargs)

	def check_values(self, values, args):
		for option in self.option_list:
			if hasattr(option, strREQUIRED) and option.required:
				if not getattr(values, option.dest):
					self.error("option %s is required" % (str(option)))
		return optparse.OptionParser.check_values(self, values, args)	

#Back to my stuff
def parse():
	print "Loading Option Parser...."

	parser = OptionParser()
	parser.add_option("-f", "--frame-interval",
			dest="frame_interval",
			help="Set the frame interval while processing the video (defaults to 50)",
			metavar="INTERVAL",
			default=50,
			type="int"
			)
	parser.add_option("-d", "--driver-power",
			dest="driver_power",
			help="Set the power of the motor",
			metavar="POWER",
			required=True
			)
	parser.add_option("-a", "--table-angle",
			dest="table_angle",
			help="Set the table angle",
			metavar="ANGLE",
			required=True
			)
	parser.add_option("-m", "--puck-mass",
			dest="puck_mass",
			help="Sets the puck mass",
			metavar="MASS",
			required=True
			)
	parser.add_option("-v", "--video",
			dest="video",
			help="Location of video file",
			metavar="FILE",
			required=True
			)
	parser.add_option("-e", "--explicit",
			action="store_true",
			dest="explicit",
			help="Output a lot of information",
			default=False
			)
	parser.add_option("-c", "--cornerRGB",
			dest="cornerRGB",
			help="RGB values (separated by spaces) for corner points",
			metavar="RGB",
			type="int",
			nargs=3
			)
	parser.add_option("-p", "--puckRGB",
			dest="puckRGB",
			help="RGB values (separated by spaces) for pucks",
			metavar="RGB",
			type="int",
			nargs=3
			)
	parser.add_option("-g", "--cornerThresh",
			dest="cornerThresh",
			help="The threshold (in %) to accept corner point RGB deviations",
			metavar="PERCENT",
			type="int"
			)
	parser.add_option("-t", "--puckThresh",
			dest="puckThresh",
			help="The threshold (in %) to accept puck RGB deviations",
			metavar="PERCENT",
			type="int"
			)
	parser.add_option("-n", "--num-bins",
			dest="num_bins",
			help="The number of bins to use",
			metavar="BINS",
			type="int"
			)
	options, args = parser.parse_args()

	return options
