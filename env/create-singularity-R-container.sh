#!/usr/bin/bash
# to set the directory to this one.
cd "$(dirname "$0")"

singularity build container_R_img.sif R_container.def