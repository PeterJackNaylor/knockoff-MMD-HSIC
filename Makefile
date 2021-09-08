
DATA_FOLDER = data/
ENV=export PYTHONPATH=`pwd`:`pwd`/src:$${PYTHONPATH}; export NXF_OPTS='-Xms500M -Xmx2G'
SINGULARITY_IMG = env/container_img.sif
REQUIREMENTS = env/requirements.txt

$(SINGULARITY_IMG): $(REQUIREMENTS)
	bash env/create-singularity-container.sh

simulation-vanilla: $(SINGULARITY_IMG)
	$(ENV); nextflow src/knock-off_benchmark.nf --repeats 1 --full false -resume


simulation-cluster: $(SINGULARITY_IMG)
	$(ENV); nextflow src/knock-off_benchmark.nf --repeats 1000 -profile cluster -resume

test: $(SINGULARITY_IMG)
	singularity exec $(SINGULARITY_IMG) /bin/bash -c "cd ${PWD}; $(ENV); pytest test"

.PHONY: clean test

clean:
	nextflow clean
	rm $(SINGULARITY_IMG)
