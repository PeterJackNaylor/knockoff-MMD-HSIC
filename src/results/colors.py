
kernel_fdr = {

}

color_dictionnary = {
        "MMD": "rgb(239,59,44)",
        "HSIC": "rgb(107,174,214)",
        "HSIC_norm":  "rgb(0,109,44)",
        "TR": "rgb(253,191,111)",
        "pearson_correlation": "rgb(106,61,154)",
        "PC": "rgb(116,196,118)",
        "DC": "rgb(177,89,40)",
        # "MMD_norm": "rgb(178, 223, 138)",
        # "MMD_linear": "rgb(178, 223, 138)",
        # "MMD_linear_norm": "rgb(51,160,44)",
        # "MMD_distance": "rgb(166,206,227)",
        # "MMD_distance_norm": "rgb(31,120,180)",
        # "MMD_gaussian": "rgb(253,191,111)",
        # "MMD_gaussian_norm": "rgb(255,127,0)",
        # "TR": "rgb(255,255,153)",
        # "HSIC_linear": "rgb(251,154,153)",
        # "HSIC_linear_norm":"rgb(227,26,28)",
        # "HSIC_distance": "rgb(202,178,214)",
        # "HSIC_distance_norm":"rgb(106,61,154)",
        # "HSIC_gaussian": "rgb(128,205,193)",
        # "HSIC_gaussian_norm":"rgb(53,151,143)",
        # "pearson_correlation": "rgb(30,30,30)",
        # "PC": "rgb(177,89,40)",
        # "DC": "rgb(200,200,200)"
        }

hector_color = {
        "MMD(linear)": "rgb(165,15,21)",
        "MMD(distance)": "rgb(252,187,161)",
        "MMD(gaussian)": "rgb(239,59,44)",
        "cMMD(linear)": "rgb(165,15,21)",
        "cMMD(distance)": "rgb(252,187,161)",
        "cMMD(gaussian)": "rgb(239,59,44)",
        "HSIC(distance)": "rgb(198,219,239)",
        "HSIC(linear)": "rgb(8,81,156)",
        "HSIC(gaussian)": "rgb(107,174,214)",
        # "MMD_norm": "rgb(178, 223, 138)",
        # "HSIC": "rgb(31,120,180)",
        "HSIC_norm":  "rgb(116,196,118)",
        "TR": "rgb(253,191,111)",
        "Pearson": "rgb(106,61,154)",
        "PC": "rgb(116,196,118)",
        "DC": "rgb(177,89,40)", 
}

kernel_colours = {
        "MMD": {"linear": "rgb(165,15,21)",
                "gaussian": "rgb(251,106,74)",
                "distance": "rgb(252,187,161)"},
        # "MMD_norm": {"linear": "rgb(198,219,239)",
        #         "gaussian": "rgb(66,146,198)",
        #         "distance": "rgb(8,69,148)"}, 
        "HSIC": {"linear": "rgb(8,81,156)",
                "gaussian": "rgb(107,174,214)",
                "distance": "rgb(198,219,239)"},
        "HSIC_norm": {"linear": "rgb(0,109,44)",
                "gaussian": "rgb(116,196,118)",
                "distance": "rgb(199,233,192)"},
}

mapping_data_name = {
        "model_0": "1.a",
        "model_4a": "1.b",
        "model_4b": "1.c",
        "model_2a": "2.a",
        "model_2b": "2.b",
        "model_5a": "2.c",
        "model_5b": "3.a",
        "model_5c": "3.b",
        "model_6a": "3.c",
}

def color_dictionnary_fdr(name, kernel, normalised, only_kernel=True):
        if only_kernel:
                s = "_norm" if normalised else ""
                return kernel_colours[name+s][kernel]
        else:
                if normalised:
                        name += "_norm"
                return color_dictionnary[name]

inside_colors = {
        "linear": "rgb(37,37,37)", #"rgba(240,240,240,0.8)",
        "gaussian":  "rgb(150,150,150)", #"rgba(178, 223, 138,0.8)",
        "distance": "rgb(217,217,217)"#"rgba(202,178,214,0.8)"
}

def name_mapping(name, kernel, normed):
        if name in ["HSIC", "MMD"]:
                s = "n" if normed else ""
                if name == 'MMD':
                        name = "cMMD"
                return name + s
        elif name == "pearson_correlation":
                return "Pearson"
        else:
                return name

def name_mapping_fdr(name, kernel, normed):
        if name in ["HSIC", "MMD"]:
                s = "n" if normed else ""
                if name == 'MMD':
                        name = "cMMD"
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
        helper(am, kernel) for am in color_dictionnary.keys() for kernel in inside_colors.keys() 
]
positions = {
        "PC": 0,
        "DC": 1,
        "TR": 2,
        "pearson_correlation": 3,
        "MMD_linear": 4,
        "MMD_linear_norm": 5,
        "MMD_distance": 6,
        "MMD_distance_norm": 7,
        "MMD_rbf": 8,
        "MMD_rbf_norm": 9,
        "HSIC_linear": 10,
        "HSIC_linear_norm": 11,
        "HSIC_distance": 12,
        "HSIC_distance_norm": 13,
        "HSIC_rbf": 14,
        "HSIC_rbf_norm": 15,
        }
