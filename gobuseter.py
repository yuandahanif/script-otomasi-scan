#!/usr/bin/python

import subprocess, sys, os
import re
import datetime
from urllib.parse import urlparse

def sanitize_target(url):
    # Remove protocol (http:// or https://)
    parsed = urlparse(url if '//' in url else f'http://{url}')
    domain = parsed.netloc if parsed.netloc else parsed.path
    
    # Remove port number if present
    domain = domain.split(':')[0]
    
    # Remove any remaining invalid filename characters
    sanitized = re.sub(r'[<>:"/\\|?*.]', '-', domain)
    return sanitized

class gobuster:
    target = ""
    output_dir =  ""
    target_output_file = ""
    worlsist = "SecLists/Discovery/Web-Content/directory-list-2.3-small.txt"
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    cwd = os.getcwd()


    def __init__(self, target):
        self.target = target
        target_path = sanitize_target(target)
        self.output_dir = os.path.join("outputs", target_path)
        self.target_output_file = os.path.join(self.output_dir, f"gobuster-{sanitize_target(target)}-{self.timestamp}.txt")

    def run(self):
        try:

            # Create output directory if it doesn't exist
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)

            command = [
                        "gobuster",
                        "dir",
                        "-u", self.target,
                        "--random-agent",
                        "-t", "50",
                        "-o", self.target_output_file,
                        "-w", self.worlsist
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