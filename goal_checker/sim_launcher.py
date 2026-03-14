'''
Author: S. Bernardi
Date: 31-Oct-2025

This module compile and launches the  protocol simulator (Java code obtained from anbxc) 
and stores the execution (unformatted) traces in .txt files
There are as many .txt files as number of roles in the protocol

Input artifacts: 

- ../protocols/src/<protocol> 	<---- Java sources and build.xml file configuration
- ../protocols/keystore			<---- keystore folder which includes pub/priv keys of role instances
- ../AnBxJ/original/AnBxJ.jar	<---- AnBxJ library the Java sources depend on

Output artifacts:

- ../protocols/bin/<protocol>						  	<--- simulator binaries
- ../protocols/sim_traces/tmp/<protocol>_role<ROLE>.txt <--- execution traces

Usage:
> python3 sim_launcher.py <protocol>

'''

import sys
import re
import subprocess

SOURCE_PATH = "../protocols/src/"
ST_TMP_PATH = "../protocols/sim_traces/tmp/"
#---------------------------------------------------------------------------
def run_init(build_file):

    # ant -buildfile $BUILD runinit
    command = ["ant"]
    if build_file:
        command += ["-buildfile", build_file]
        command += ["runinit"]

    try:
        # Run the command
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # Print the output
        print(f"{result.stdout}")
        if result.stderr:
            print(f"{result.stderr}")
    
    except subprocess.CalledProcessError as e:
        print("Error running ant runinit command:")
        print(e.output)
        print(e.stderr)
#---------------------------------------------------------------------------

def run_role(build_file,target,log_file):
    command = ["ant"]
    if build_file:
        command += ["-buildfile", build_file]
        command.append(target)

    # Open the log file for writing
    with open(log_file, "w") as lf:
        # Start the command in the background, redirecting output to log_file
        process = subprocess.Popen(
            command,
            stdout=lf,
            stderr=subprocess.STDOUT  # Redirect stderr to stdout (same log_file)
        )

    print(f"{target} launched with PID {process.pid}, logging to {log_file}")

#---------------------------------------------------------------------------
def retrieve_roles(build_file):

	roles = []
	with open(build_file, 'r') as fb:
		for line in fb:
			#<target name="ROLE_B"  >
			line = line.strip('\t')
			role_pattern = re.compile(r'<target\sname=\"ROLE_(\w+)\".+')
			matched = role_pattern.match(line)
			if matched:
				goal = matched.groups()[0]
				roles.append(goal)

	return roles

#---------------------------------------------------------------------------
def launch_simulation(protocol_name):

	#Java code and built.xml exist in protocol_name (lowercase) folder 
	build_file = SOURCE_PATH + protocol_name.lower() + '/build.xml'

	roles = retrieve_roles(build_file)
	run_init(build_file)
	for r in roles:
		#run_role in background and log
		role_name = 'ROLE_' + r
		log_file = ST_TMP_PATH + protocol_name + '_role' + r + '.txt'
		#ISOPK2PMAP_I1_roleA
		run_role(build_file,role_name,log_file)


#---------------------------------------------------------------------------
if __name__ == "__main__":

	if len(sys.argv) == 2:
		launch_simulation(sys.argv[1]) #name of the protocol name (filename without extensions)
	else:
		print("Usage: python3 sim_launcher <protocol_name>")
		exit(1)

	

