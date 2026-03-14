# CryptoSimulator
Checking security goals on execution traces of the Java-based implementation of cryptographic protocols produced by the AnBx framework (https://paolo.science/anbx/).


## 🗂️ Project Structure

The project is organized as follows:

```
project/
├── AnBxJ            <----------------- AnBxJ and Bouncy Castle Crypto libraries
├── goal_checker     <----------------- .py modules         
├── protocols/
    ├── anbx/        <----------------- AnBx files of protocol specification
    ├── dltl_log/    <----------------- formatted traces, DLTL model and formula, results
    ├── keystore     <----------------- store of public/private keys of participants 
    ├── ofmc_traces/ <----------------- counterexamples produced by OFMC model checker
    ├── sim_traces/  <----------------- execution traces produced by protocol simulators
    └── src/         <----------------- Java code of protocol simulators
├── test             <----------------- .sh scripts to generate all the goal_checker artifacts of the protocol set 
├── LICENSE 
└── README.md 
```

## 🚀 Usage notes

- [Use of the goal_checker](https://github.com/simber72/goal-checker/tree/main/goal_checker) 
- [Set of protocols used in the experiments](https://github.com/simber72/goal-checker/tree/main/protocols)
- [Test the steps with the protocol set](https://github.com/simber72/goal-checker/tree/main/test)
- [The AnBxJ and BCC libraries](https://github.com/simber72/goal-checker/tree/main/AnBxJ)

## 🔗 Dependencies
The ```goal_checker``` is based on the AnBx framework (https://paolo.science/anbx/). 
The following artifacts either come from or have been generated with the AnBx framework:
1. The AnBxJ library (```AnBxJ```)
2. The AnBx specification of the set of protocols considered in the experiments (```protocols/anbx```)
3. The set of public/private keys of aliases (```protocols/keystore```), 
4. The counterexamples of security goals (```protocols/ofmc_traces```), and 
5. The Java code and configuration files of the protocols (```protocols/src```) **The Java code has been manually changed after generation** 

The DLTL model checker used in this repository is an ad-hoc version for this project. 
The official repo of the MC prototype is available [here](https://github.com/ezpeleta/py_MC)
