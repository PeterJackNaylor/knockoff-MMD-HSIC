

CWD = System.getProperty("user.dir")

params.full = 'true'

params.repeats = 1

if (params.full == 'true'){
    DATASETS = ["model_0", "model_2a", "model_2b", "model_2c", "model_2d", "model_4a", "model_4b"]
    ASSOCIATION_MEASURES = ["PC", "DC", "TR", "HSIC", "pearson_correlation", "MMD"]
    sample_size = [100, 500, 1000]
    // d depends mostly on n
    associated_d = ['100': 50, '500': 300, '1000': 100]
    feature_size = [5e2, 5e3]
    ALPHA_MIN = 1
    ALPHA_MAX = 9
}
else {
    DATASETS = ["model_0"]
    ASSOCIATION_MEASURES = ["PC", "DC", "TR", "HSIC", "MMD"]
    sample_size = [200]
    // d depends mostly on n
    associated_d = ['100': 50, '500': 300, '200': 90]
    feature_size = [5e2]
    ALPHA_MIN = 4
    ALPHA_MAX = 4

}



process data {
    tag "DATASET=${data_name};n=${n};p=${p}"

    input:
        val data_name from DATASETS
        each n from sample_size
        each p from feature_size
        each rep from 0..(params.repeats - 1)
    output:
        set val("DATASET=${data_name};n=${n};p=${p};rep=${rep}"), file("Xy.npz") into XY
    script:
        py_file = file("${CWD}/src/data/${data_name}.py")
        """
        python $py_file --n $n --p $p
        """
}


process knock_off {
    publishDir "./outputs/vanilla/simulations_results/fdp", pattern: "fdp_*.csv", mode: 'copy', overwrite: 'true'

    input:
        set PARAMS, file(Xy) from XY
        each T from ASSOCIATION_MEASURES
        each alpha from ALPHA_MIN..ALPHA_MAX
    output:
        file("fdr.csv") into FDR
        file("fdp_*.csv")
    script:
        feature_size = PARAMS.split(';')[1].split('=')[1]
        py_file = file("${CWD}/src/model/knock-off.py")
        """
        python $py_file --alpha ${alpha / 10} \\
                        --t $T --n_1 0.3 \\
                        --d ${associated_d[feature_size]} \\
                        --param "$PARAMS"
        """
}


FDR.collectFile(skip: 1, keepHeader: true)
   .set { ALL_FDR }


process plots_and_simulation_results {
    publishDir "./outputs/vanilla/simulations_results", mode: 'copy', overwrite: 'true'
    input:
        file concatenated_exp from ALL_FDR
    output:
        set file("simulation_plot.html"), file("$concatenated_exp")
    script:
        py_file = file("${CWD}/src/results/simulation.py")
        """
        python $py_file --csv_file $concatenated_exp
        """
}
