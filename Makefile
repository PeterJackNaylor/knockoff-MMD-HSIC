
DATA_FOLDER = data/
ENV=export PYTHONPATH=`pwd`:`pwd`/src:$${PYTHONPATH}; export NXF_OPTS='-Xms500M -Xmx2G'
SINGULARITY_IMG = env/container_img.sif
SINGULARITY_R_IMG = env/container_R_img.sif
REQUIREMENTS = env/requirements.txt

$(SINGULARITY_IMG): $(REQUIREMENTS)
	bash env/create-singularity-container.sh

$(SINGULARITY_R_IMG): $(REQUIREMENTS)
	bash env/create-singularity-R-container.sh

simulation-vanilla: $(SINGULARITY_IMG)
	$(ENV); nextflow src/knock-off_benchmark.nf --repeats 5 --full false -profile knockoff -resume


simulation-cluster:
	$(ENV); nextflow src/knock-off_benchmark.nf --repeats 200 -profile knockoff -resume

test: $(SINGULARITY_IMG)
	singularity exec $(SINGULARITY_IMG) /bin/bash -c "cd ${PWD}; $(ENV); pytest test"

real_data:
	$(ENV); nextflow src/knock-off_real_data.nf -profile knockoff -resume

.PHONY: clean test

clean:
	nextflow clean
	rm $(SINGULARITY_IMG)
