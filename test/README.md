# 🔍 Test
The ```test``` folder includes the following scripts:

### **01_log_extractor.sh**
generates the ```.csv``` and ```.goals``` of all the protocols in ```/protocols/dltl_log/``` and print the differences w.r.t. previous generation (files in ```/protocols/dltl_log/``` subfolders)
Usage:
```
> ./01_log_extractor.sh
```

### **02_dltl_generator.sh**
generates the ```.mod``` and updates ```.goals``` of all the protocols in ```/protocols/dltl_log/``` and write the differences w.r.t. previous generation (files in ```/protocols/dltl_log/``` subfolders)
Usage:
```
> ./02_dltl_generator.sh
```
### **03_dltl_mc.sh**
generates the result files of the model checking of all the protocols in ```/protocols/dltl_log/``` and write the differences of ```.res``` files  w.r.t. previous generation (files in ```/protocols/dltl_log/``` subfolders)
Usage:
```
> ./03_dltl_mc.sh
```

### **04_res_synthesis.sh**
generates the ```.res_s``` of all the protocols in ```/protocols/dltl_log/``` and print the differences w.r.t. previous generation (files in ```/protocols/dltl_log/``` subfolders)
Usage:
```
> ./04_res_synhtesis.sh
```
