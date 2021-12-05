#!/usr/bin/python3


### AUTHOR DOCUMENTATION ###

# HISTORY:
# Created by Matthew Delfino on 2019.09.02
# 
# LICENSE:
# Copyright (c) 2019, Matthew Delfino.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 	* Redistributions of source code must retain the above copyright notice,
# 	  this list of conditions and the following disclaimer.
# 	* Redistributions in binary form must reproduce the above copyright
# 	  notice, this list of conditions and the following disclaimer in the
# 	  documentation and/or other materials provided with the distribution.
# 	* The name of "KNOCK, inc." may not be used to endorse or promote
#	  products derived from this software without specific prior written
#	  permission.
# 
# THIS SOFTWARE IS PROVIDED BY KNOCK, INC. `AS IS' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL KNOCK, INC. BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


### IMPORT ###

import os, sys, getopt


### VARIABLES ###

script_name 	= os.path.basename(__file__)
script_version	= 1.0
list_of_source	= False
excludes_file	= False


#### FUNCTIONS ###

def main(argv):
	# By matthew.delfino, 2019.09.02: For parsing arguments, options.

	if len(sys.argv) <= 1:
		print_help_page ( "no arguments", "You must specify at least one option" )
		exit( 1 )
	else:
		try:
			opts, args = getopt.getopt( argv, "hvt:e:", ["help", "version", "text-file=", "excludes-file="] )
		except getopt.GetoptError as err:
			print_help_page ( str(err), None )
			exit( 1 )
		for opt, arg in opts:
			if opt in ("-h", "--help"):
				print_help_page ( None, None )
				exit( 0 ) 
			elif opt in ("-v", "--version"):
				print script_version
				exit( 0 )
			# START STUMP !!
			elif opt in ("-t", "--text-file"):
				text_file = arg
				if os.path.isfile( text_file ):
					list_of_source = open( text_file ).read().split()
				else:
					print_help_page ( "specified file, '" + text_file + "' does not exist", None )
					exit( 1 )
			# END STUMP !!
			elif opt in ("-e", "--excludes-file"):
				excludes_file = arg
				if not os.path.isfile( excludes_file ):
					print_help_page ( "specified file, '" + excludes_file + "' does not exist", None )
					exit( 1 )
			# START STUMP !!
			else:
				print_help_page ( "argument '" + opt + "' not recognized", None )
				exit( 1 )
			# END STUMP !!

def print_help_page( illegal_option, tip_to_print ):
	# By matthew.delfino, 2019.09.02: A helpful help page.

	if illegal_option:
		print "ILLEGAL:", illegal_option
	if tip_to_print:
		print tip_to_print

	print script_name, "forces lowercase on all words except those listed in an excludes file, which it will capitalize."
	print script_name, "--text-file file_of_words --excludes-file file_of_excludes"
	print script_name, "--version"

def transform_string ( string_to_transform, type_of_transformation ):
	# By matthew.delfino, 2019.09.02: Uses Python to transform text so that
	# the string is 1) capitalized, 2) all lower case or 3) all upper case.
	# Variable "type_of_transformation" accepts values of 1) 'capitalize',
	# 2) 'lower', and 3) 'upper'.

	if type_of_transformation == capitalize:
		return string_to_transform.capitalize()
	elif type_of_transformation == lower:
		return string_to_transform.lower()
	elif type_of_transformation == upper:
		return string_to_transform.upper()
	else:
		print string_to_transform, "is an invalid value for the 'type_of_transformation' variable. Valide options include 'capitalize', 'lower' and 'upper'."
		exit( 2 )


### SEQUENCE ###

if __name__ == "__main__":
	main(sys.argv[1:])

if not list_of_source or not excludes_file:
	print_help_page ( None, "You must specify both a text and an excludes file." )
	exit( 1 )

# We will need a loop counter.
loop_counter	= 0

print ( list_of_source )

#for i in list_of_source
#do
#	# After each echo, except the last one, there needs to be a space. So,
#	# we add it here at the beginning. But we don't want to add one if this
#	# is the first loop, hence this small test:
#	if [[ $loop_counter != 0 ]]; then /bin/echo -n " "; fi
#
#	# Every loop counter needs to increment. I like this particular option:
#	(( loop_counter++ ))
#
#	# We test the iteration against the excludes list in the excludes file.
#	grep -iqw ${i} "$excludes_file"
#	if [[ $? == 0 ]]
#	then
#		# If it matches, we will capitalize.
#		transform_string "$i" c
#	else
#		# Otherwise, we make sure every letter is lowercase.
#		transform_string "$i" l
#	fi
#
#	/bin/echo -n "$returnedObject"
#done

# To apply one carriage return to the end.
print
