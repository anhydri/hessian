# Viewing vibration from Hessian calculations

### Requirements:
  - Python pip
  - Jupyter Notebook
  
To install python pip, go to https://pip.pypa.io/en/stable/installing/

To install Jupyter Notebook, go to https://jupyter.readthedocs.io/en/latest/install.html

### Download and run:
In the linux terminal, go to the directory you want to download this Jupyter Notebook to. <br/>
To download the jupyter notebook and the script for installing python packages, copy and run this command line:

```bash
$ git clone https://github.com/anhydri/hessian.git
```

Go to the downloaded folder hessian/, run this command to install the required packages:

```bash
$ bash install_pypack.sh
```

These packages need to be installed only once for each computer.

It might take some minutes to install, please be patient.

To view the vibrations from the output of the Hessian calculation: <br/>
- Requiring: an output file (e.g. hessian.log) and an input file (e.g. hessian.inp). <br/>
  These files must have the same name, except for the file ending ("hessian")
- Call jupyter notebook:

```bash
$ jupyter notebook
```

In the first cell of the notebook, change the name of the "input_file" variable to the name of your output file:
```python
input_file = "hessian.log"
```



