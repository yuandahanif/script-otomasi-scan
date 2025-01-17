#!/usr/bin/python

import sys
import nuclei, gobuseter
import multiprocessing


def main():
    target = sys.argv[1]

    if target == "":
        print("Usage: python scan.py <target>")
        sys.exit(1)
    # Run nuclei scan
    n = nuclei.nuclei(target)

    n_p = multiprocessing.Process(target=n.run)

    # Run gobuster scan
    g = gobuseter.gobuster(target)
    g_p = multiprocessing.Process(target=g.run)

    n_p.start()
    g_p.start()

    n_p.join()
    g_p.join()


if __name__ == "__main__":
    main()