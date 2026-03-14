'''
Author: S. Bernardi, J. Ezpeleta
Date: 1-January-2026
Comments: revised version of "csv2mod.py"

This module processes the synthetized execution traces (.csv) and the goal parameters instantiation (.goals)
and produces the model and formulas in DLTL MC format.

Input files: 

- <protocol>.csv    <--- synthetized execution traces

Example:
#session,step,active_part,passive_part,action,msg_content,msg_type
1,0,alice,-,generateNumber,X0,anbxj.Crypto_ByteArray
1,0,alice,-,AnBx_Params,X1;X0,anbxj.AnBx_Params

- <protocol>.goals  <--- instantiated goal parameters 

Output file:

- <protocol>.mod   <--- DLTL model
- <protocol>.goals  <--- DLTL formula (.goals updated with DLTL formula)

Usage:
> python3 dltl_generator <protocol>

'''

import os
import sys
import re
import string
import csv
from datetime import datetime

DLTL_PATH = "../protocols/dltl_log/"

def read_last_line(filename):
	with open(filename, 'rb') as f:  # open in binary mode
		f.seek(-2, 2)  # jump to second last byte
		while f.read(1) != b'\n':  # move backward until a newline
			f.seek(-2, 1)
		return f.readline().decode()  # decode bytes to string
		#closes filename before the return
# ---------------------------------------------------------------------------
def at_t_active(t,role):
	#"(t)t[active]==role" 
	return '\"({0}){0}[active]=={1}\"'.format(t,role)

def at_t_in_mess(t,asset):
	#("(t)asset in t[mess]")
	return '(\"({0}){1} in {0}[mess]\")'.format(t,asset)

def at_t_not_active(t,role):
	#("(t)t[active]!=role") 
	return '(\"({0}){0}[active]!={1}\")'.format(t,role)

def at_t_not_sealed(t):
	#("(t)t[type] != 'javax.crypto.SealedObject.toString'")
	return '(\"({0}){0}[type]!=\'javax.crypto.SealedObject.toString\'\")'.format(t)

def equal_asset(t1,t2,asset):
	#("(t1,t2)t1[mess]==t2[mess]")
	return '(\"({0},{1}){0}[mess]=={1}[mess]\")'.format(t1,t2)

def recovery(t,who,asset):
	return '{0} & ?can_recover & {1}'.format(at_t_active(t,who),at_t_in_mess(t,asset))

def agree(t,who,asset):
	return '{0} & ?agrees{1} & {2}'.format(at_t_active(t,who),asset[1:],at_t_in_mess(t,asset))

def recoveryfwd(t1,t2,who,asset):
	return '{0} & ?can_recover & {1}'.format(at_t_active(t2,who),equal_asset(t1,t2,asset))

def agreefwd(t,who,asset):
	return '{0} & ?agrees{1}'.format(at_t_active(t,who),asset[1:])

# ---------------------------------------------------------------------------
def set_auth_form(assets,who):

	letter = string.ascii_lowercase[::-1] # z-a
	content = ''
	count = 0
	'''
	#AUTH_VIOLATION_BCK (LTL)
	for i in range(len(assets)):
		z_i = letter[count]
		# G z_i.( !(("(z_i)w[active]==who[0]") & ?can_recover & ("(z_i)?asset[i] in z_i[mess]")) ) |
		content += 'G {0}.( !({1} ) | '.format(z_i,recovery(z_i,who[0],assets[i]))		
		y_i = letter[count+1]
		#F y_i.(("(y_i)y_i[active]==who[0]") & ?can_recover & ("(y_i)assets[i] in y_i[mess]") & 
		content += 'F {0}.( {1} & '.format(y_i,recovery(y_i,who[0],assets[i]))
		x_i = letter[count+2]
		count += 3
		#Y H x_i.( !( ("(x_i)x_i[active]==who[1]") & ?agrees & ("(x_i)assets[i] in x_i[mess]")))
		content += 'Y H {0}.( !( {1} ) )) )'.format(x_i,agree(x_i,who[1],assets[i]))
		if i < len(assets)-1:
			content += ' | '
	#The formula should be negated in case who[1] is the intruder
	if who[1] == '?I':
		content = '!( ' + content + ')\n'
	else:
		content += '\n'
	'''
	#AUTH_VIOLATION_FWD (DLTL)
	#
	count = 0
	for i in range(len(assets)):
		x_i = letter[count]
		#x_i.( !("(x_i)x_i[active]==?B" & ?agreesNB2) ) | 
		content += 'G {0}.( !({1}) |'.format(x_i,agreefwd(x_i,who[1],assets[i]))
		y_i = letter[count+1]
		count += 2
		#! X F y.( "(y)y[active]==?A" & ?can_recover ) ) & "(z,y)z[mess]==y[mess]"))
		content += '! X F {0}.({1}))'.format(y_i,recoveryfwd(x_i,y_i,who[0],assets[i]))
		if i < len(assets)-1:
			content += ' & '	
	#The formula should be negated in case who[1] is the intruder
	if who[1] == '?I':
		content = '!( ' + content + ')\n'
	else:
		content += '\n'

	return content

# ---------------------------------------------------------------------------
def set_secret_form(assets,who):
	
	instants = string.ascii_lowercase[::-1] # z-a
	content = ''
	for i in range(len(assets)):
		x_i = instants[i]
		#F x_i.((
		content += 'F {0}.(('.format(x_i)
		#"(x_i)x_i[active]==who[0]") | ("(x_i)x_i[active]==who[1]" ...
		for j in range(len(who)):
			content += '{0}'.format(at_t_active(x_i,who[j]))
			if j < len(who)-1:
				content += ' | '
		#) & ?generates  &
		content += ') & ?generates{0} & '.format(assets[i][1:])
		y_i = instants[i+1]
		#X F y_i.(
		content += 'X F {0}.('.format(y_i)
		#("(y_i)y_i[active]!=who[0]") & ("(y_i)y_i[active]!=who[1]") ... 
		for j in range(len(who)):
			content += '{0}'.format(at_t_not_active(y_i,who[j]))
			if j < len(who)-1:
				content += ' & '
		#& ?can_read &  ("(z,y)z[mess]==y[mess]") & ("(y_i)y_i[type] != 'javax.crypto.SealedObject.toString'")))
		content += '& ?can_read & {0} & {1}))'.format(equal_asset(x_i,y_i,assets[i]),at_t_not_sealed(y_i))
		if i < len(assets)-1:
			content += ' | '
		else:
			content += '\n'

	return content

# ---------------------------------------------------------------------------
def generate_formula(prefixname):
#Pre: prefixname.goals file
	filename = DLTL_PATH + prefixname
	params = dict()
	content = ''
	#read .goals to parse the goals
	with open(filename + '.goals', 'r') as fgoals:
		for line in fgoals:
			#parse SET
			set_pattern = re.compile(r'^_SET\s(\?\w+)\s(.+)')
			matched = set_pattern.match(line)
			if matched:
				p, v = matched.groups()
				params.update({p:v.split(",")})
				print(params)
			#parse GOAL
			goal_pattern = re.compile(r'^;GOAL\s(\w+):\[(.+)\],\[(.+)\]')
			matched = goal_pattern.match(line)
			if matched:
				goal_type,assets,who = matched.groups()
				assets = assets.split(',')
				who = who.split(',')
				#generate param. formulas from GOALS and store line
				if goal_type == 'auth':
					content += '\n;AUTH_VIOLATION\n'
					content += set_auth_form(assets,who)		
				else:
					content += '\n;SECRET_VIOLATION\n'
					content += set_secret_form(assets,who)

	#update .goals with the param. and instantiated formula
	with open(filename + '.goals', 'a') as fgoals:
		fgoals.write(f"{content}\n\n")
		fgoals.write("_WRITE\n")
		fgoals.write("_BYE\n")


# ---------------------------------------------------------------------------
def generate_model(prefixname):
#Pre: prefixname.csv file
	filename = DLTL_PATH + prefixname + '.csv'
	
	headingMod = "aaction,nsession,nstep,sactive,spassive,@mess,stype"

	#Retrieve the last line to read the last session number (max)
	last_line = read_last_line(filename)
	last_line = last_line.split(',')
	last_sess = str(last_line[0])

	#Open the .mod file to write
	with open(DLTL_PATH + prefixname + '.mod', 'w') as fmod:
	
		fmod.write(headingMod + '\n')

		#Open the .csv file to read line by line 
		with open(filename, 'r', newline='') as fcsv:
			reader = csv.DictReader(fcsv)
			for row in reader:
				
				# Trace identifier
				id = prefixname + '_' + str(row["#session"]).zfill(len(last_sess))
				attribsOrder =  ["action","#session","step","active_part", 
								 "passive_part","msg_content","msg_type"
								]
				rowList = [row[attrib] for attrib in attribsOrder]
				rowList = id + ',' + '&'.join(rowList)
				fmod.write(rowList + '\n')
	#---------------------------------------------------------------------------
def generate_dltl_spec(filename):

	print("Save model in ", filename + ".............................")
	generate_model(filename)
	print("Update goals in ", filename + ".............................")
	generate_formula(filename)

#---------------------------------------------------------------------------
if __name__ == "__main__":

	if len(sys.argv) == 2:
		generate_dltl_spec(sys.argv[1]) #name of the protocol name (filename without extensions)
	else:
		print("Usage: python3 dltl_generator <protocol_name>")
		exit(1)

	

