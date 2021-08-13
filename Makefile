
DATA_FOLDER = data/
ENV=export PYTHONPATH=`pwd`:`pwd`/src:$${PYTHONPATH}
SINGULARITY_IMG = env/container_img.sif
REQUIREMENTS = env/requirements.txt

$(SINGULARITY_IMG): $(REQUIREMENTS)
	bash env/create-singularity-container.sh

simulation-vanilla: $(SINGULARITY_IMG)
	$(ENV); nextflow src/knock-off_benchmark.nf --data $(DATA_FOLDER) -resume

test: $(SINGULARITY_IMG)
	singularity exec $(SINGULARITY_IMG) /bin/bash -c "cd ${PWD}; $(ENV); pytest test"

.PHONY: clean test

clean:
	nextflow clean
	rm $(SINGULARITY_IMG)
