#!/bin/sh


### AUTHOR DOCUMENTATION ###

# HISTORY:
# Created by Matthew Delfino on 2019.08.09
# 
# LICENSE:
# Copyright (c) 2019, KNOCK, inc.
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


### VARIABLES ###

SNAME="${0##*/}"
VERSION=1.0


### FUNCTIONS ###

PrintHelpPage()
{
	# Author matthew.delfino on 2016.10.26:
	#
	# A helpful help page.

	# Parsed Argument Variables
	local illegalOption=$1		# An illegal option passed to the
					# function (e.g., "--makemerich").
	local tipToPrint=$2		# A tip (e.g., "Try again.")

	# Sequence
	if [ "$illegalOption" != "" ]
	then
		echo "ILLEGAL OPTION: $illegalOption"
	fi
	if [ "$tipToPrint" != "" ]; then echo "$tipToPrint"; fi
	echo "A script that forces lowercase on all words except those listed"\
	     "in an excludes file, which it will capitalize."
	echo "$SNAME --text-file file_of_words --excludes-file file_of_excludes"
	echo "$SNAME --version"
}

PrintVersion()
{
	# Author matthew.delfino on 2016.10.26:
	#
	# Just prints the current version. Takes no arguments.

	# Sequence
	echo $VERSION
}

TransformString()
{
	# Author matthew.delfino on 2019.08.09: 
	#
	# Uses Python to transform text so that the string is 1) capitalized, 2)
	# all lower case or 3) all upper case.

	# Parsed Argument Variables
	local theString=$1		# The string whose case we wish to
					# transform (e.g., "red grape Seed").
	local transForm=$2		# Type of case transformation. Accept-
					# able values are 1) 'capitalize', 'C'
					# or 'c', 2) 'lower', 'L' or 'l', and 3)
					# 'upper', 'U' or 'u'.

	# Sequence
	case $transForm in
		capitalize | [Cc] )
			returnedObject=$(python -c "name = '$theString'; print \
				       (name.capitalize())")
			;;
		lower | [Ll] )
			returnedObject=$(python -c "name = '$theString'; print \
				       (name.lower())")
			;;
		upper | [Uu] )
			returnedObject=$(python -c "name = '$theString'; print \
				       (name.upper())")
			;;
	esac
}


### SEQUENCE ###

listOfSource="null"
excludesFile="null"

while (( "$#" ))
do
	case $1 in
		--text-file | -[Tt] )
			shift
			if [[ ! -f $1 ]]
			then
				PrintHelpPage "$1" "No such file."
				exit 1
			else
				listOfSource=$(cat "$1" | sed -e 's/#.*$//' -e \
					     '/^$/d')
				shift
			fi
			;;
		--excludes-file | -[Ee] )
			shift
			if [[ ! -f $1 ]]
			then
				PrintHelpPage "$1" "No such file."
				exit 1
			else
				excludesFile="$1"
				shift
			fi
			;;
		--version | -[Vv] | [Vv] )
			PrintVersion
			exit 0
			;;
		--help | -[Hh] | [Hh] )
			PrintHelpPage "" ""
			exit 0
			;;
		*)
			PrintHelpPage "$1"
			exit 1
			;;
	esac
done

if [[ $listOfSource == "null" ]] || [[ $excludesFile == "null" ]]
then
	PrintHelpPage "" "You must specify both a text and an excludes file."
	exit 1
fi

# We will need a loop counter.
loopCounter=0

for i in $listOfSource
do
	# After each echo, except the last one, there needs to be a space. So,
	# we add it here at the beginning. But we don't want to add one if this
	# is the first loop, hence this small test:
	if [[ $loopCounter != 0 ]]; then /bin/echo -n " "; fi

	# Every loop counter needs to increment. I like this particular option:
	(( loopCounter++ ))

	# We test the iteration against the excludes list in the excludes file.
	grep -iqw ${i} "$excludesFile"
	if [[ $? == 0 ]]
	then
		# If it matches, we will capitalize.
		TransformString "$i" c
	else
		# Otherwise, we make sure every letter is lowercase.
		TransformString "$i" l
	fi

	/bin/echo -n "$returnedObject"
done

# To apply one carriage return to the end.
echo

exit 0
