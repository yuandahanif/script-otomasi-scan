#!/usr/bin/python

import subprocess, sys, os
import re
import datetime
from urllib.parse import urlparse
import pty
import tty
import termios
import sys
import select

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


    def __init__(self, target, output_dir = ""):
        self.target = target
        target_path = sanitize_target(target)
        self.output_dir = os.path.join("outputs", output_dir, target_path)
        self.target_output_file = os.path.join(self.output_dir, f"gobuster-{sanitize_target(target)}-{self.timestamp}.txt")

    def run(self):
        try:
            # Create pseudo-terminal for proper progress bar handling
            master_fd, slave_fd = pty.openpty()

            # Store original terminal settings
            old_settings = termios.tcgetattr(sys.stdin)

            # Create output directory if it doesn't exist
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)

            try:
                # Set raw mode for terminal
                tty.setraw(master_fd)

                command = [
                        "gobuster",
                        "dir",
                        "-u", self.target,
                        "--random-agent",
                        "-t", "50",
                        "-o", self.target_output_file,
                        "-w", self.worlsist
                    ]
                # Execute gobuster with PTY
                process = subprocess.Popen(
                    command,
                    stdout=slave_fd,
                    stderr=slave_fd,
                    universal_newlines=True,
                    start_new_session=True
                )

                # Read and display output while preserving progress bar
                while True:
                    try:
                        r, w, e = select.select([master_fd], [], [], 0.1)
                        
                        if master_fd in r:
                            output = os.read(master_fd, 1024).decode('utf-8', errors='ignore')
                            if output:
                                # Write to screen
                                sys.stdout.write(output)
                                sys.stdout.flush()
                        
                        # Check if process has finished
                        if process.poll() is not None:
                            break
                            
                    except (IOError, OSError):
                        break

            finally:
                # Restore terminal settings
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                os.close(master_fd)
                os.close(slave_fd)

        except Exception as e:
                    error_msg = f"Error scanning {self.target}: {str(e)}\n"
                    print(error_msg)
                    # log.write(error_msg)