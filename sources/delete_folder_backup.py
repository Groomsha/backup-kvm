"""
Project Name: 'backup-kvm'
Version: 1.0

Description: 

Ihor Cheberiak (c) 2021
https://www.linkedin.com/in/ihor-cheberiak/
"""

import os
import time
import subprocess

from datetime import datetime


class DeleteFolderBackup:
    def __init__(self, name_obj, dir_logs, dir_backup, number_archives) -> None:
        self.name_obj = name_obj
        self.dir_logs = dir_logs
        self.dir_backup = dir_backup
        self.number_archives = number_archives
        self.shell_output = []
    
    def main_setup(self):
        self.performance_shell(f"ls {self.dir_backup}")

        for rm in self.shell_output[self.number_archives:]:
            self.performance_shell(f"rm -r {self.dir_backup}{rm}")
            self.logs_creation([f"rm -r {self.dir_backup}{rm}"])

    def logs_creation(self, messages):
        if os.path.isfile(f"{self.dir_logs}delete_backup.log"):
            access_type = "a"
        else:
            access_type = "w"
        
        time_message = time.ctime()
        with open(f"{self.dir_logs}delete_backup.log", access_type) as log:
            for message in messages:
                log.write(f"\n{time_message} {message}")
    
    def performance_shell(self, command, wait_shell=True):
        shell_os = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, executable="/bin/bash", universal_newlines=True)

        if wait_shell:
            shell_os.wait()

        output, errors = shell_os.communicate()

        if shell_os.returncode != 0:
            self.logs_creation(str(errors.strip()).splitlines())
        else:
            if command[:2] == "ls":
                for data in str(output.strip()).splitlines():
                    if data[:-11] == self.name_obj:
                        self.shell_output.append(data)

                self.shell_output.sort(key=lambda date: datetime.strptime(date[-10:], "%d.%m.%Y"), reverse=True)
        