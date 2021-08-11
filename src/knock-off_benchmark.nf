
params.splits = 5
params.data = "/data/"
data_folder = file(params.data)

DATASETS = ["model_2a", "model_2b", "model_2c", "model_2d"]

CWD = System.getProperty("user.dir")
sample_size = [100, 500]
feature_size = [5e2, 5e3]

process data {
    tag "DATASET=${data_name};n=${n};p=${p}"

    input:
        val data_name from DATASETS
        each n from sample_size
        each p from feature_size
    output:
        set val("DATASET=${data_name};n=${n};p=${p}"), file("Xy.npz") into XY
    script:
        """
        python ${CWD}/src/data/${data_name}.py --n $n --p $p
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
    output:
        file("out")
    script:
        """
        python ${CWD}/src/model/knock-off.py
        """

}