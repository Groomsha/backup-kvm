"""
Project Name: 'backup-kvm'
Version: 1.1

Description: 

Ihor Cheberiak (c) 2021
https://www.linkedin.com/in/ihor-cheberiak/
"""

import time as time_os
import os as terminal_os
import subprocess as shell


class RestoreKVMinIMG():
    def __init__(self, name_obj, dir_logs, backup_folder) -> None:
        self.name_obj = name_obj
        self.dir_logs = dir_logs
        self.backup_folder = backup_folder
        self.dev_pool = ""
        self.dev_img = ""

    def main_setup(self):
        with open(f"{self.backup_folder}{self.name_obj}-img_info") as backup:
            temp_str = ""
            for line in backup:
                temp_str += line

        *rest, self.dev_pool, self.dev_img = temp_str.split()
    
        self.logs_creation([f"Start Process Restoring Virtual Machine: {self.name_obj} {self.backup_folder}"])

        self.virsh_command("destroy")
        self.virsh_command("delete", [self.dev_pool, self.dev_img])
        self.virsh_command("define")
        self.archive_creation()

        print("Restore Сompleted!")
    
    def logs_creation(self, messages):
        if terminal_os.path.isfile(f"{self.dir_logs}{self.name_obj}.log"):
            access_type = "a"
        else:
            access_type = "w"
        
        time_message = time_os.ctime()
        with open(f"{self.dir_logs}{self.name_obj}.log", access_type) as log:
            for message in messages:
                print(f"{time_message} {message}")
                log.write(f"\n{time_message} {message}")
    
    def performance_shell(self, command, wait_shell = True):
        shell_os = shell.Popen(command, stdout=shell.PIPE, stderr=shell.PIPE, shell=True, executable="/bin/bash", universal_newlines=True)

        if wait_shell: shell_os.wait()
        
        output, errors = shell_os.communicate()
        if len(str(output)) != 0:
            self.logs_creation(str(output.strip()).splitlines())
        if len(str(errors)) != 0:
            self.logs_creation(str(errors.strip()).splitlines())

    def virsh_command(self, command, sources = None):
        """ Уничтажает виртуальную машину (VM), восстановление 
            из Backup и запускает виртуальную машину (VM)
        """
        if command == "destroy":
            self.performance_shell(f"virsh destroy {self.name_obj}")
        elif command == "delete":
            self.performance_shell(f"virsh vol-delete {sources[1]} --pool {sources[0]}")
        elif command == "define":
            self.performance_shell(f"virsh define {self.backup_folder}{self.name_obj}.xml")
        elif command == "restore":
            self.performance_shell(f"virsh start {self.name_obj}")

    def archive_creation(self):
        dev_img_temp = self.dev_img[self.dev_img.find("."):]
        self.logs_creation([f"Process GUNZIP Disk Image: For disk recovery VM: {self.name_obj}"])
        self.performance_shell(f"gunzip -ck {self.backup_folder}{self.name_obj}{dev_img_temp}.gz > {self.dev_img}")
        self.virsh_command("restore")
