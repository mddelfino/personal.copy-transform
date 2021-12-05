#!/usr/bin/python

import os, sys, getopt

script_name 	= os.path.basename(__file__)
script_version	= 1.0

def print_help_page( illegal_option, tip_to_print ):
	# By matthew.delfino, 2019.09.02: A helpful help page.

	if illegal_option:
		print "ILLEGAL:", illegal_option
	if tip_to_print:
		print tip_to_print

	print script_name, "forces lowercase on all words except those listed "\
	     "in an excludes file, which it will capitalize."
	print script_name, "--text-file file_of_words --excludes-file file_of_excludes"
	print script_name, "--version"

	return

def main(argv):

	if len(sys.argv) <= 1:
		print_help_page ( "no arguments", "You must specify at least one option" )
		exit( 1 )
	else:
		try:
			opts, args = getopt.getopt( argv, "t:", ["text-file="] )
		except getopt.GetoptError as err:
			print_help_page ( str(err), None )
			exit( 1 )
		for opt, arg in opts:
			if opt in ("-t", "--text-file"):
				text_file = arg
				if not os.path.isfile(text_file):
					print_help_page ( "specified file, '" + text_file + "' does not exist", None )
					exit( 1 )
				else:
					list_of_source = open( text_file ).read().split()
		return list_of_source


### SEQUENCE ###

if __name__ == "__main__":
	main(sys.argv[1:])

