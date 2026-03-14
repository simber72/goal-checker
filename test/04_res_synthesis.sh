#/bin/zsh
#/bin/bash
#Date: 13/03/2026
#Generates the synthesis of the MC results for all the protocols in DLTL_PATH 
#Produces differences of .res_s files w.r.t. previous generation (files in DLTL_PATH subfolders)



GC_PATH=../goal_checker/
DLTL_PATH=../protocols/dltl_log/

#Previous generation: files in "cases" subfolders
#Subfolders
cases=(no_attack passive replay reflection mitm)
#Files in the subfolders
no_attack=(AndrewSecureRPC From_A_and_Back GSM ISOPK2PMAP ISOSK2PMAP Kerberos NSPK SSO )
passive=(From_A_and_Back_S GSM_S_1 NSPK_S_1)
replay=(AndrewSecureRPC_A ISOSK2PMAP_A1 ISOSK2PMAP_A2 SSO_A2)
reflection=(ISOPK2PMAP_A1 ISOPK2PMAP_A2)
mitm=(GSM_S_2 Kerberos_A NSPK_S_2 SSO_A1 SSO_S)


#: <<'COMMENT'
#Loop over the subfolders
for c in "${cases[@]}" 
do
	echo "----> Case: $c"
	prot_var="${c}[@]"
	prot_list=("${!prot_var}")
	#Loop over the protocols in the subfolder
	for prot in "${prot_list[@]}"
	do
    	echo "Protocol: $prot"
    	python3 ${GC_PATH}res_synthesis.py $prot > /dev/null    
		postfix=".res_s"
		#sf=$c	
		file_new="${DLTL_PATH}${prot}${postfix}"
		echo "New file: ${DLTL_PATH}${prot}${postfix}"
		file_old="${DLTL_PATH}$c/${prot}${postfix}"
		echo "Old file: ${DLTL_PATH}$c/${prot}${postfix}"
		echo $postfix 'diff starts ----------'
		diff $file_new $file_old
    	echo $postfix 'diff ends ----------'
	done
done

