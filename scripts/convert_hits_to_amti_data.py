""" Usage:
    <file-name> --in=INPUT_FILE --out=OUTPUT_FILE [--debug]

Convert AMT csv format to amti jsonl.

"""
# External imports
import logging
import pdb
from pprint import pprint
from pprint import pformat
from docopt import docopt
from pathlib import Path
from tqdm import tqdm
import pandas as pd
import json

# Local imports


#----

if __name__ == "__main__":

    # Parse command line arguments
    args = docopt(__doc__)
    csv_fn = Path(args["--in"])
    out_fn = Path(args["--out"])

    # Determine logging level
    debug = args["--debug"]
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    # Start computation
    df = pd.read_csv(csv_fn, sep = ",", header = 0, na_filter = False)
    jsons = [dict(row) for _, row in df.iterrows()]

    with open(out_fn, "w", encoding = "utf8") as fout:
        fout.write("\n".join(map(json.dumps, jsons)))

    num_of_jsons = len(jsons)
    logging.info(f"Wrote {num_of_jsons} lines to {out_fn}")

    # End
    logging.info("DONE")
