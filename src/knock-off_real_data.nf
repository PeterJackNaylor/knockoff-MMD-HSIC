
params.repeats = 1
params.splits = 8

ASSOCIATION_MEASURES = [
    "DC",
    "HSIC",
    "cMMD",
    "PC",
    "TR",
    "pearson_correlation"
]

CWD = System.getProperty("user.dir")

DATASETS = [
    'MNIST.py',
    "tcga.R"
]

PHENOTYPES = [
    'BRCA'
]

process data {

    tag "DATASET=${tag}"
    container 'file://./env/container_R_img.sif'

    input:
        val data_name from DATASETS
        each phenotype from PHENOTYPES

    output:
        set val("DATASET=${tag}"), file("Xy.npz") into XY

    when:
        (phenotype == 'BRCA') || (data_name == "tcga.R")

    script:
        dl_file = file("${CWD}/src/data/${data_name}")
        if (data_name == "tcga.R"){
            tag = "${data_name}-${phenotype}"
            """
            $dl_file $phenotype
            """
        } else {
            tag = "${data_name}}"
            """
            python3 $dl_file 
            """
        }
}

process split_data {

    tag "${PARAMS};fold=${I}"

    input:
        set PARAMS, file(DATA) from XY
        each I from 0..(params.splits - 1)
        val SPLITS from params.splits

    output:
        set val("${PARAMS};fold=${I}"), file("Xy_train.npz"), file("Xy_test.npz") into splits
    
    script:
        template 'stratified_train_test_split.py'
}

process knock_off {

    tag "AM=${T};${PARAMS}"
    errorStrategy 'ignore'
    
    input:
        set PARAMS, file(Xy_train), file(Xy_test) from splits
        each T from ASSOCIATION_MEASURES
    output:
        set val("AM=${T};${PARAMS}"), file(Xy_train), file(Xy_test), file("fdr.csv") into selected_features
    script:
        feature_size = PARAMS.split(';')[1].split('=')[1]
        py_file = file("${CWD}/src/model/knock-off.py")
        """
        python $py_file --t $T --n_1 0.3 \\
                        --d 100 \\
                        --param "$PARAMS" \\
                        --xy $Xy_train
        """
}

process classify {

    input:
        set PARAMS, file(Xy_train), file(Xy_test), file(FEATURES) from selected_features
    output:
        file 'accuracy.csv' into ACCURACIES
    script:
        template 'rf.py'

}

ACCURACIES.collectFile(skip: 1, keepHeader: true)
   .set { ALL_ACCURACIES }
   
process output {
    
    publishDir "./outputs/real_world/", mode: 'copy', overwrite: 'true'

    input:
        file concatenated_exp from ALL_ACCURACIES
    output:
        file "scores.csv"
    script:
        """
        cp $concatenated_exp scores.csv
        """
}
