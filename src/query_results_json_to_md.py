#!/usr/bin/env python3

# Portions of this file contributed by NIST are governed by the
# following statement:
#
# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties. Pursuant to Title 17 Section 105 of the
# United States Code, this software is not subject to copyright
# protection within the United States. NIST assumes no responsibility
# whatsoever for its use by other parties, and makes no guarantees,
# expressed or implied, about its quality, reliability, or any other
# characteristic.
#
# We would appreciate acknowledgement if the software is used.

"""
This script converts a subset of SPARQL Query Results JSON objects to a Markdown table.

SECURITY NOTE: At this time, this script has no control in place for malicious Markdown syntax.  It SHOULD NOT be used on unreviewed results from untrusted graphs.
"""

__version__ = "0.0.1"

import argparse
import json
from typing import TypedDict

SolutionObject = TypedDict("SolutionObject", {"type": str, "value": str})

HeadObject = TypedDict("HeadObject", {"vars": list[str]})


class ResultsObject(TypedDict):
    bindings: list[dict[str, SolutionObject]]


class QueryResultsObject(TypedDict):
    """
    https://www.w3.org/TR/sparql11-results-json/
    """

    head: HeadObject
    results: ResultsObject


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("in_json")
    parser.add_argument("out_md")
    args = parser.parse_args()

    with open(args.out_md, "w") as out_fh:
        with open(args.in_json, "r") as in_fh:
            qrobj: QueryResultsObject = json.load(in_fh)
            out_fh.write("| ")
            out_fh.write(" | ".join(["?" + var for var in qrobj["head"]["vars"]]))
            out_fh.write(" |\n")

            out_fh.write("| ")
            out_fh.write(" | ".join(["---" for var in qrobj["head"]["vars"]]))
            out_fh.write(" |\n")

            for binding in qrobj["results"]["bindings"]:
                out_fh.write("| ")
                out_fh.write(
                    " | ".join([binding[var]["value"] for var in qrobj["head"]["vars"]])
                )
                out_fh.write(" |\n")


if __name__ == "__main__":
    main()
