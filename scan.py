#!/usr/bin/python

import sys
import nuclei, gobuseter
import multiprocessing
import argparse

    
avaliable_tools = ["nuclei", "gobuster"]

if __name__ == "__main__":
    msg = "A simple tool to run nuclei and gobuster scans on a target URL"

    # Initialize parser
    parser = argparse.ArgumentParser(description = msg)

    # Adding optional argument
    parser.add_argument("url", help = "the URL to scan")
    parser.add_argument("-t", "--Tool", help = "Use -t to specify the tool to run eg. -t nuclei or -t gobuster")

    args = parser.parse_args()
    target = args.url
    tool = args.Tool

    if target == "":
        print("Usage: python scan.py <target>")
        sys.exit(1)
    if tool not in avaliable_tools:
        print(f"Invalid tool specified. Avaliable tools are: {avaliable_tools}")
        sys.exit(1)

    if tool == "nuclei":
        # Run nuclei scan
        n = nuclei.nuclei(target)
        n_p = multiprocessing.Process(target=n.run)
        n_p.start()
        n_p.join()

    if tool == "gobuster":
        # Run gobuster scan
        g = gobuseter.gobuster(target)
        g_p = multiprocessing.Process(target=g.run)
        g_p.start()
        g_p.join()