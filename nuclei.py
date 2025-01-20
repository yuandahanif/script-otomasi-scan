#!/usr/bin/python

import subprocess, os
import datetime
import utils.sanitize as sanitize

class nuclei:
    target = ""
    output_dir =  ""
    target_output_file = ""
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    cwd = os.getcwd()


    def __init__(self, target, output_dir = ""):
        self.target = target
        target_path = sanitize.sanitize_target(target)
        self.output_dir = os.path.join("outputs", output_dir, target_path)
        self.target_output_file = os.path.join(self.output_dir, f"nuclei-{sanitize.sanitize_target(target)}-{self.timestamp}.txt")

    def run(self):
        try:

            # Create output directory if it doesn't exist
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)

            command = [
                        "nuclei",
                        "-target", self.target,
                        # "-severity", "low,medium,high,critical",
                        "-o", self.target_output_file,
                    ]

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
                    error_msg = f"Error scanning {self.target}: {str(e)}\n"
                    print(error_msg)
                    # log.write(error_msg)
