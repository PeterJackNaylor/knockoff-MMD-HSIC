
import argparse
import pandas as pd

def options():
    # options
    parser = argparse.ArgumentParser(description="Knock off run")
    parser.add_argument("--csv_file", type=str)
    args = parser.parse_args()

    return args

def main():
    ## Load data
    opt = options()
    table = pd.read_csv(opt.csv_file)
    import pdb; pdb.set_trace()
if __name__ == "__main__":
    main()
