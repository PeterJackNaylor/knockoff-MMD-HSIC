# knockoff-MMD-HSIC
Implementation of knockoff with MMD and HSIC. Paper submitted in AISTATS 2021: *Kernel knockoff for post selection screening* by Benjamin Poignard, Peter Naylor, Hector Climente-Gonzales and Makoto Yamada.
If you use our code, please cite the above paper.

## Reproducible results
### Prerequisite: 
Follow the official documentation to install [Nextflow](https://www.nextflow.io/).

### Set up `nextflow.config` file
Nextflow's power is that it allows one to run a scientific pipeline with one single script, this script can optimize your available resources.
If you are on your local computer, there isn't much to change expect to define the number of allowed process in parallel such as `executor.queueSize`.
If you have access to a cluster, you can define a scheduler, such as SGE or Slurm.
Here is an example of such a script for our SGE cluster with Singularity:
```
profiles {
    knockoff {
        process.executor = 'sge' \\scheduler
        process.queue = 'c1normal' \\ cluster queue
        process.memory = '10GB'
        process.container = 'file://./env/container_img.sif' 
        process.containerOptions = '-B /data:/data' \\for mounting our external HD
        executor {
            queueSize = 500
            submitRateLimit = '10 sec'
        }
        singularity {
            enabled = true
            envWhitelist = 'PYTHONPATH'
        }
    }
}
```

### Possible environnement 
To offer a couple of possibilities we have set up a Singularity or conda environnement. 
Nextflow can use either, or the Singularity containers or it will create the conda environnement on the fly.
#### Singularity
Install [Singularity](https://sylabs.io/guides/3.0/user-guide/quick_start.html) following the official installation guide.
The nextflow.config file in master and the one above have Singularity enabled. 
As Singularity uses containers you will have to build the images:
There are two containers, one for Python and the other one for R.
To create the images you will have to run with sudo:
``` bash
sudo make env/container_img.sif
sudo make env/container_R_img.sif
```
#### Conda
To use the Conda environnement on the fly, you will have to remove the Singularity option and add the Conda ones; for example:

```
profiles {
    knockoff {
        process.executor = 'sge' \\scheduler
        process.queue = 'c1normal' \\ cluster queue
        process.memory = '10GB'
        process.conda = '/path/to/main/folder/.../env/knockoff.yaml'
        executor {
            queueSize = 500
            submitRateLimit = '10 sec'
        }
    }
}
```

## Final commands
Finally, to launch the pipeline on the simulated dataset:
```
make simulation-cluster
```
and to launch the pipeline on real data:
```
make real_data
```

