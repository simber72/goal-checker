'''
Author: S. Bernardi
Date: 31-Oct-2025

This module launches the modules of the goal_checker:
0- sim_launcher.py 		--> optional: not to be launched in case of replications of experiments
1- log_extractor.py 	--> pre-processing of execution traces
2- dltl_generator.py 	--> trace model and DLTL formulas generation
3- mc/MC.py 			--> trace checking
4- res_synthesis.py 	--> post-processing of model checker results


Usage:
> python3 sim_launcher.py <protocol> -o [OPTIONS] 
where <protocol> is the name of the protocol.

'''

import sys
import os
import re
import subprocess
import click #CLI

DLTL_PATH 	= "../protocols/dltl_log/"
ST_PATH 	= "../protocols/sim_traces/tmp/"
#---------------------------------------------------------------------------
def run(module,protocol):
	
	if module == "rm":
		#$DLTL_PATH/protocol.norm $DLTL_PATH/protocol_longs_trazas.txt
		prot = DLTL_PATH + protocol
		command = [module, prot+".norm", prot+"_longs_trazas.txt"]
	elif module == "mc/MC.py":
		#log-file=$DLTL_PATH/protocol formula-file=$DLTL_PATH/protocol.goals
		prot = DLTL_PATH + protocol
		logfile = "log-file=" + prot
		formulafile = "formula-file=" + prot + ".goals"
		command = ["python3", module, logfile, formulafile]
	else:
		#protocol
		command = ["python3", module, protocol]

	try:
		# Run the command
		result = subprocess.run(command, capture_output=True, text=True, check=True)

		# Print the output (verbose)
		#print(f"{result.stdout}")
		if result.stderr:
			print(f"{result.stderr}")

	except subprocess.CalledProcessError as e:
		print(f"Error running {command} command:")
		print(e.output)
		print(e.stderr)

#---------------------------------------------------------------------------
@click.command()
@click.argument('protocol')
@click.option('-s','--simul', is_flag=True, show_default=True, default=False, help="Protocol simulation and trace generation")
def main_cli(protocol,simul):
	
	print("--------------------------------------------------------------------------------")
	print(f"Protocol: {protocol}")
	print(f"Intermediate and final results will be saved in {DLTL_PATH}")
	print("--------------------------------------------------------------------------------")

	#optional: not to be launched in case of replications of experiments
	if simul:
		print("Start protocol execution ...")
		run("sim_launcher.py",protocol)
		print(f"Execution traces saved in {ST_PATH}: {protocol}_role*.txt\n")

	#Pre-processing of execution traces
	print("Start preprocessing of logs...")
	run("log_extractor.py",protocol)
	print(f"Formatted log: {protocol}.csv\n")

	#Trace model and DLTL formulas generation
	print("Generation of trace model and DLTL formulas...")
	run("dltl_generator.py",protocol)
	print(f"Trace model: {protocol}.mod")
	print(f"DLTL parametric formulas: {protocol}.goals\n")
	
	#Trace checking
	print("Start trace checking logs...")
	run("mc/MC.py",protocol)
	print(f"Instantiated formulas: {protocol}.forms")
	print(f"Model checker results: {protocol}.res")

	#Clean not relevant results files  
	run("rm",protocol)
	print(f"Removing other file results: .norm .txt\n")

	#Post-processing of model checker results
	print("Start results synthesis...")
	run("res_synthesis.py",protocol)
	print(f"Final results: {protocol}.res_s")
	print("--------------------------------------------------------------------------------")
#---------------------------------------------------------------------------
if __name__ == "__main__":
	main_cli()