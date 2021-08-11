
DATA_FOLDER = data/

singularity_image:
	bash env/create-singularity-container.sh

simulation-vanilla:
	nextflow src/knock-off_benchmark.nf --data $(DATA_FOLDER) -resume

test: $(SINGULARITY_ENV)
	$(SINGULARITY_ENV); pytest test
