
// This script has not been checked, but it should be
// very similar to benchmark but with real data, therefor/
// It may need train/test split if we need to check the prediciton.
params.repeats = 1
params.splits = 3
ASSOCIATION_MEASURES = ["DC", "HSIC", "MMD", "PC", "TR"]
CWD = System.getProperty("user.dir")
DATASETS = ['MNIST.py']


process data {
    tag "DATASET=${data_name}"

    input:
        val data_name from DATASETS
    output:
        set val("DATASET=${data_name}"), file("Xy.npz") into XY
    script:
        dl_file = file("${CWD}/src/data/${data_name}")
        """
        $dl_file 
        """
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
        template 'train_test_split.py'
}

process knock_off {

    errorStrategy 'ignore'
    
    input:
        set PARAMS, file(Xy_train), file(Xy_test) from splits
        each T from ASSOCIATION_MEASURES
    output:
        set PARAMS, file(Xy_train), file(Xy_test), file("fdr.csv") into selected_features
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

    input:
        file concatenated_exp from ALL_ACCURACIES
    output:
        file "scores.csv"
    script:
        """
        cp $concatenated_exp scores.csv
        """
}
