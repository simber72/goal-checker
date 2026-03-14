# 🤝 Set of protocols used in the experiments
The folder ```protocols``` includes the artifacts produced for a set protocols. They are organized in several subfolders:
```
├── protocols/
    ├── anbx/        <----------------- AnBx files of protocol specification
    ├── dltl_log/    <----------------- formatted traces, DLTL model and formulas
    ├── keystore/    <----------------- store of public/private keys of participants
    ├── ofmc_traces/ <----------------- counterexamples produced by OFMC model checker
    ├── sim_traces/  <----------------- execution traces produced by protocol simulators
    └── src/         <----------------- Java code of protocol simulators
```

## Protocols and security goals (anbx)
Procols and security goals are specified using the [AnBx notation](https://paolo.science/anbxtutorial/tools/OFMC-tutorial.pdf)
and the examples are taken from the [AnBx tool](https://www.dais.unive.it/~modesti/anbx/).

The following table summarizes the protocols and the security goals:

| Protocol  |  Security goal 
| -------- |  ---------------------
| AndrewSecureRPC |  ```A``` authenticates ```B``` on ```NB2```
| From_A_and_Back      | ```Msg secret``` between ```a```,```B```
| GSM                  |  ```Msg``` secret between ```B```,```M``` 
| NSPK                 | ```NxNA``` secret between ```A```,```B```
| ISOPK2PMAP           |  ```A```  authenticates ```B``` on ```Text3``` 
|                      |  ```B```  authenticates ```A``` on ```Text1``` 
| ISOSK2PMAP           |  ```A```  authenticates ```B``` on ```Text3``` 
|                      |  ```B```  authenticates ```A``` on ```Text1``` 
| Kerberos             |  ```C```  authenticates ```s``` on ```Payload``` 
| SSO                 |  ```SP```  authenticates ```C``` on ```URI``` 
|                  |  ```C```  authenticates ```SP``` on ```Data``` 
|                  |  ```Data```  secret between ```SP```, ```C``` 


All the protocols violate the corresponding security goals.

Security goals to be verified fall in these categories:
- secrecy
- weak authentication
- strong authentication

### Secrecy
```
NA secret between A,B
```
Specifies *what* (```NA```) must to be kept secret and *who* (```A``` and ```B```) is cleared to know it. 

### Weak authentication
```
B weakly authenticates A on NA
```
The weaker notion of authentication (agreement), it has a direction: the protocol authentically transmits *a value* (```NA```)
form *a participant* (```A```) to *another participant* (```B```).

### Strong authentication
```
B authenticates A on NA
```
The stronger notion of authentication implies:
- weak authentication, and
- the *value* (```NA```) is *fresh*, that is it has been generated in the protocol session


## Traces, formulas and results (dltl_log)
There are different folders, one for each type of test case: 
```
├── no_attack/  <----------------- no attack
├── replay/     <----------------- replay attacks
├── reflection/ <----------------- reflection attacks
├── mitm/       <----------------- mitm attacks 
└── passive/    <----------------- passive attacks
```

Each folder includes:
1. The formatted traces (```.cvs```) 
2. The trace model (```.mod```) and formulas (```.goals```) to be fed to the DLTL model-checker
3. The instantiated formulas (```.forms```) and the results (```.res```) from the ```mc/MC``` model-checker
4. The syntesized results (```.res_s```) produced by the ```res_synthesis``` module.

### Formatted traces
The formatted traces are obtained by pre-processing the execution logs with the ```log_extractor``` module
and they are saved as ```csv ``` files with the following data format:

| Column | Field | Description
| --- | ------------- | ---------------------
| 1 | timestamp | HH:mm:ss:SSS (it is empty if the original AnBx library ```AnBxJ/AnBx.jar``` is used)
| 2 | session | session number
| 3 | step | step in the protocol execution
| 4 | active participant | it is the participant that carries out the action (column 6)
| 5 | passive participant | it is the receiver in case of ```sent``` action, the sender in case of ```received``` action, ```-``` otherwise
| 6 | action | it is the action carried out by the active participant
| 7 | message content | it is the content of the message
| 8 | message type content | the type of message content 


#### Type of actions
The type of actions in an execution log (column 6) are the following:

| Action | Description
| -------- | -------------
| sent | a message is sent by the active participant (column 4) to the passive participant (column 5)
| received | a message is received by the active participant (column 4) from the passive participant (column 5)
| generateNumber | the active participant generates a fresh value (nonce)
| AnBx_Params | the active participant prepares the message content to be sent (sets the content as a tuple, encrypt, etc.)
| eq_check | the active participant verifies the message content (column 7) with an equality check
| inv_check | the active participant verifies the  message content (column 7) with a crypto operation (decrypt a value) or a projection operation followed by another check (e.g., extracts a component of the tuple and performs an equality check)

#### Message content and type

| Content |       Type         | Example
| -------- | --------------------------- | ---------------
| nonce    | anbj.Crypto_ByteArray | **X0**  an array of 256 integers
| hash     | anbj.Crypto_ByteArray | **X1**  an array of 32 integers
| tuple    | anbj.Crypto_AnBx_Params | **X0**;**X1** a tuple with two Crypto_ByteArray 
| ciphertext (symmetric scheme) | javax.crypto.SealedObject | **@1e730495** the object identifier
| ciphertext (asymmetric scheme)| anbxj.Crypto_SealedPair | **@2928854b** the object identifier
| secret key | javax.crypto.spec.SecretKeySpec | **@8e761151** the object identifier
| participant name | string | **alice**


| Checking |       Type         | Example of content
| -------- | --------------------------- | ---------------
| eq_check  | anbxj.Crypto_ByteArray.toString | **X1**, where **X1** is checked if equal to a value known by the actor who carries out the checking
| inv_check | anbxj.Crypto_SealedPair.toString | **X1**, where **X1** is extracted and checked if equal to a value known by the actor who carries out the checking

### Trace model and formulas
The trace model and formulas are generated by the ```dltl_generator``` module and they are saved, respectively,
in ```.mod``` and ```.goals``` textual files. 
The DLTL formulas are parametric with respect to the roles and the assets in the AnB protocol specification.
Each formula expresses the violation of a security goal.

### Model-checker output and synthesized results
The ```mc/MC``` model-checker produces results in form of matrix (row: trace, column: instantiated formula), that are saved in
```.res``` file. 
The ```res_synthesis``` module summarizes the results as true/false outcome, that are saved in ```.res_s``` file. When the formula is satisfied, i.e., the corresponding goal is violated, the list of traces that breach the goal is indicated.

## Keystore
The ```keystore``` folder includes the public/private keys of a set of aliases (copied from AnBx framework https://paolo.science/anbx/).
It is used by the ```sim_launcher``` module to generate the execution traces of the protocols.

## OFMC traces
The ```ofmc_traces``` folder includes the counter-examples of security goals of the protocols in the set that have been generated by the OFMC model checker from the AnB specifications.

## Simulation traces
The ```sim_traces``` folder includes the execution traces produced by running the Java-based implementation of the protocol.
The ```sim_launcher``` module has been used to compile the Java-code of the protocol, run the simulation for a number of sessions and generate the execution traces.

## Java-based implementations
The ```src``` folder includes the Java source code of the protocols. The Java code has been generated from the AnBx specification by using the ```anbxc``` compiler from the AnBx framework (framework https://paolo.science/anbx/)
and, in case,  manually changed (the changed/newly added lines include comments prefixed by *SB*).
Each Java-based implementation includes a ```.property``` and a ```.build.xml``` configuration file.
The path of the AnBJ library has been set to the path ```./AnBxJ/``` of this repository.

