""" Usage:
    <file-name> --in=INPUT_FILE --out=OUTPUT_FILE [--debug]

Group all annotations by hit. Fields stay the same but become lists corresponding to the
original annotations by order.
"""
# External imports
import logging
import pdb
import json
from pprint import pprint
from pprint import pformat
from docopt import docopt
from pathlib import Path
from tqdm import tqdm

# Local imports


#----


HIT_ID_KEY = "HITId"

def create_new_group(dic):
    """
    create a new hit group from a single assignment.
    """
    grp = {}
    grp[HIT_ID_KEY] = dic[HIT_ID_KEY]
    for k, v in dic.items():
        if k == HIT_ID_KEY:
            continue
        grp[k] = [v]
    return grp

if __name__ == "__main__":

    # Parse command line arguments
    args = docopt(__doc__)
    inp_fn = Path(args["--in"])
    out_fn = Path(args["--out"])

    # Determine logging level
    debug = args["--debug"]
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    # Start computation
    inp_jsons = [json.loads(line.strip())
             for line in open(inp_fn, encoding = "utf8")]

    out_jsons = {}

    for dic in tqdm(inp_jsons):
        hit_id = dic[HIT_ID_KEY]
        if hit_id not in out_jsons:
            out_jsons[hit_id] = create_new_group(dic)
        else:
            cur_json = out_jsons[hit_id]
            for k, v in dic.items():
                if k == HIT_ID_KEY:
                    # don't add the hit id
                    continue
                else:
                    # all other values are concatenated
                    cur_json[k].append(v)
    # Output
    with open(out_fn, "w", encoding = "utf8") as fout:
        for dic in out_jsons.values():
            fout.write(json.dumps(dic) + "\n")

    # End
    logging.info("DONE")
