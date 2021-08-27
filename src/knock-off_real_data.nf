
// This script has not been checked, but it should be
// very similar to benchmark but with real data, therefor/
// It may need train/test split if we need to check the prediciton.
params.repeats = 1
params.splits = 1
ASSOCIATION_MEASURES = ["PC", "DistanceCorrelation", "TR"]
CWD = System.getProperty("user.dir")


process data {
    tag "DATASET=${data_name}"

    input:
        val data_name from DATASETS
    output:
        set val("DATASET=${data_name}"), file("Xy.npz") into XY
    script:
        """
        python ${CWD}/src/data/${data_name}.py
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
    
    input:
        set PARAMS, file(Xy_train), file(Xy_test) from splits
        each T from ASSOCIATION_MEASURES
        each alpha from 1..5
    output:
        file("fdr.csv") into FDR
    script:
        feature_size = PARAMS.split(';')[1].split('=')[1]
        """
        echo ${feature_size}
        python ${CWD}/src/model/knock-off.py --alpha ${alpha / 10} --t $T --n_1 0.3 --d ${associated_d[feature_size]} --param "$PARAMS"
        """
}


FDR.collectFile(skip: 1, keepHeader: true)
   .set { ALL_FDR }


process plots_and_real_data_results {
    publishDir "./outputs/real_data_results", mode: 'copy', overwrite: 'true'
    input:
        file concatenated_exp from ALL_FDR
    output:
        set file("real_data_plot.html"), file("$concatenated_exp")
    script:
        """
        python ${CWD}/src/results/ --csv_file $concatenated_exp
        """
}