#!/usr/bin/python

import subprocess, sys
import re
import datetime

def sanitize_target(target):
        # Remove http:// or https:// from the target
        target = re.sub(r'^https?://', '', target)
        # Remove invalid filename characters for Unix systems
        target = re.sub(r'[<>:"/\\|?*]', '', target)
        return target

class gobuster:
    target = ""
    target_output_file = ""
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")


    def __init__(self, target):
        self.target = target
        self.target_output_file = f"./outputs/{sanitize_target(target)}-{self.timestamp}.txt"

    def run(self):
        try:
            command = f"""
            gobuster dir -o {self.target_output_file} -t 50 -w ./SecLists/Discovery/Web-Content/directory-list-2.3-small.txt -b 404,302 -u {self.target} --random-agent
            """

            process =  subprocess.Popen(
                            command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            universal_newlines=True,
                            bufsize=1
                        )
            # Read and display output in real-time
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
                    # log.write(output)

        except Exception as e:
                    error_msg = f"Error scanning {target}: {str(e)}\n"
                    print(error_msg)
                    # log.write(error_msg)


if __name__ == "__main__":
    target = sys.argv[1]

    if target == "":
        print("Usage: python gobuster.py <target>")
        sys.exit(1)

    g = gobuster(target)
    g.run()