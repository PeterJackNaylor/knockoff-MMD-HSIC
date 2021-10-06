

CWD = System.getProperty("user.dir")

params.full = 'true'

params.repeats = 1

if (params.full == 'true'){
    DATASETS = [
        "model_0",
        "model_2a",
        "model_2b",
        "model_4a",
        "model_4b",
        "model_5a",
        "model_5b",
        "model_5c"
    ] //"model_2c", "model_2d"

    ASSOCIATION_MEASURES = [
        "DC",
        "TR",
        "pearson_correlation",
        "HSIC",
        "MMD",
        "PC"
    ]
    KERNELS = ['linear', 'distance', 'gaussian']
    sample_size = [100, 500, 1000]
    // d depends mostly on n
    associated_d = ['100': 50, '500': 300, '1000': 100]
    feature_size = [100, 5e2, 5e3]
    NORMALIZE = [0]
}
else {
    DATASETS = ["model_6a"]
    ASSOCIATION_MEASURES = [
        "MMD" // "PC"
    ]
    KERNELS = ['linear', 'distance', 'gaussian']
    sample_size = [500]
    // d depends mostly on n
    associated_d = ['100': 50, '500': 300, '200': 90]
    feature_size = [5e2]
    NORMALIZE = [0]
}

KERNELLESS_AM = [
    "DC", "PC", "TR", "pearson_correlation"
]

BINARY_AM = [
    "MMD"
]

BINARY_MODELS = [
    "model_5b",
    "model_5c",
    "model_6a"
]


process data {
    tag "DATASET=${data_name};n=${n};p=${p}"

    input:
        val data_name from DATASETS
        each n from sample_size
        each p from feature_size
        each rep from 0..(params.repeats - 1)
    output:
        set val("DATASET=${data_name};n=${n};p=${p};rep=${rep}"), file("Xy.npz") into XY
    when:
        (n < p + 1) || ((n == 500) && (p == 100))
    script:
        py_file = file("${CWD}/src/data/${data_name}.py")
        """
        python $py_file --n $n --p $p
        """
}


process knock_off {
    errorStrategy 'ignore'

    input:
        set PARAMS, file(Xy) from XY
        each T from ASSOCIATION_MEASURES
        each k from KERNELS
        each normalise from NORMALIZE
    output:
        file("fdr.csv") into FDR
    when:
        MMD_and_BINARY = (PARAMS.split(';')[0].split('=')[1] in BINARY_MODELS) || (!(T in BINARY_AM))
        AM_NO_KERNEL = ((k == "linear") && (normalise == 0)) || (!(T in KERNELLESS_AM))
        MMD_and_BINARY && AM_NO_KERNEL
        // MMD needs binary data
        // only the kernel AM need normalise and kernel looping
    script:
        feature_size = PARAMS.split(';')[1].split('=')[1]
        py_file = file("${CWD}/src/model/knock-off.py")
        """

        python $py_file --t $T --n_1 0.3 \\
                        --d ${associated_d[feature_size]} \\
                        --param "$PARAMS" \\
                        --kernel $k \\
                        --normalise $normalise
        """
}


FDR.collectFile(skip: 1, keepHeader: true)
   .set { ALL_FDR }


process plots_and_simulation_results {
    publishDir "./outputs/vanilla/simulations_results", mode: 'copy', overwrite: 'true'
    input:
        file concatenated_exp from ALL_FDR
    output:
        set file("*.html"), file("$concatenated_exp")
    script:
        py_box_plots = file("${CWD}/src/results/box_plots.py")
        py_fdr_control = file("${CWD}/src/results/benchmark_plot_like_python.py")
        py_empty_set = file("${CWD}/src/results/empty_set.py")
        """
        python $py_box_plots --csv_file $concatenated_exp 
        python $py_fdr_control --csv_file $concatenated_exp --kernels 0 --name normal
        python $py_fdr_control --csv_file $concatenated_exp --kernels 1 --name kernel
        python $py_empty_set --csv_file $concatenated_exp --kernels 0 --name normal
        python $py_empty_set --csv_file $concatenated_exp --kernels 1 --name kernel
        """
}
