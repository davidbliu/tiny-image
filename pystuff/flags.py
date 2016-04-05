from optparse import OptionParser
parser = OptionParser()
parser.add_option("-n","--name", dest="name",
	help="upload files as NAME", metavar="NAME")
parser.add_option("-s", "--skip", dest = "skip",
	help = "SKIP option (see README)", metavar = "SKIP")
(options, args) = parser.parse_args()
print options
print 'args are'
print args