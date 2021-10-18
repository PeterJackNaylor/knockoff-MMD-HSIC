color_dictionnary = {
    "cMMD": "rgb(239,59,44)",
    "HSIC": "rgb(107,174,214)",
    "HSIC_norm": "rgb(0,109,44)",
    "TR": "rgb(253,191,111)",
    "pearson_correlation": "rgb(106,61,154)",
    "PC": "rgb(116,196,118)",
    "DC": "rgb(177,89,40)",
}

hector_color = {
    "cMMD(linear)": "rgb(165,15,21)",
    "cMMD(distance)": "rgb(252,187,161)",
    "cMMD(gaussian)": "rgb(239,59,44)",
    "HSIC(distance)": "rgb(198,219,239)",
    "HSIC(linear)": "rgb(8,81,156)",
    "HSIC(gaussian)": "rgb(107,174,214)",
    "HSIC_norm": "rgb(116,196,118)",
    "TR": "rgb(253,191,111)",
    "Pearson": "rgb(106,61,154)",
    "PC": "rgb(116,196,118)",
    "DC": "rgb(177,89,40)",
}

kernel_colours = {
    "cMMD": {
        "linear": "rgb(165,15,21)",
        "gaussian": "rgb(251,106,74)",
        "distance": "rgb(252,187,161)",
    },
    "HSIC": {
        "linear": "rgb(8,81,156)",
        "gaussian": "rgb(107,174,214)",
        "distance": "rgb(198,219,239)",
    },
    "HSIC_norm": {
        "linear": "rgb(0,109,44)",
        "gaussian": "rgb(116,196,118)",
        "distance": "rgb(199,233,192)",
    },
}

mapping_data_name = {
    "model_1a": "1.a",
    "model_1b": "1.b",
    "model_1c": "1.c",
    "model_2a": "2.a",
    "model_2b": "2.b",
    "model_2c": "2.c",
    "model_2d": "2.d",
    "model_2e": "2.e",
    "model_3a": "3.a",
    "model_3b": "3.b",
    "model_3c": "3.c",
}


def color_dictionnary_fdr(name, kernel, normalised, only_kernel=True):
    if only_kernel:
        s = "_norm" if normalised else ""
        return kernel_colours[name + s][kernel]
    else:
        if normalised:
            name += "_norm"
        return color_dictionnary[name]


inside_colors = {
    "linear": "rgb(37,37,37)",
    "gaussian": "rgb(150,150,150)",
    "distance": "rgb(217,217,217)",
}


def name_mapping(name, kernel, normed):
    if name in ["HSIC", "cMMD"]:
        s = "n" if normed else ""
        return name + s
    elif name == "pearson_correlation":
        return "Pearson"
    else:
        return name


def name_mapping_fdr(name, kernel, normed):
    if name in ["HSIC", "cMMD"]:
        s = "n" if normed else ""
        return name + s + f" ({kernel})"
    elif name == "pearson_correlation":
        return "Pearson"
    else:
        return name


def helper(name, kernel):
    if "_norm" in name:
        return name_mapping_fdr(name.split("_")[0], kernel, True)
    else:
        return name_mapping_fdr(name, kernel, False)


color_dictionnary_fdr_keys = [
    helper(am, kernel)
    for am in color_dictionnary.keys()
    for kernel in inside_colors.keys()
]
