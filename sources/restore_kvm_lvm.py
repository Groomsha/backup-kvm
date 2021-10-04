"""
Project Name: 'backup-kvm'
Version: 1.1

Description: Скрипт позволяет востоновить бекапы виртуальных 
машин для гипервизора KVM размещенных на блочном устройстве LVM.

Ihor Cheberiak (c) 2021
https://www.linkedin.com/in/ihor-cheberiak/
"""

import time as time_os
import os as terminal_os
import subprocess as shell


class RestoreKVMinLVM():
    def __init__(self, name_obj, dir_logs, backup_folder) -> None:
        self.name_obj = name_obj
        self.dir_logs = dir_logs
        self.backup_folder = backup_folder
        self.size_lvm_block = ""
        self.dev_lvm_block = ""
    
    def main_setup(self):
        with open(f"{self.backup_folder}{self.name_obj}-raw_info") as backup:
            temp_str = ""
            for line in backup:
                temp_str += line

        *rest, self.size_lvm_block, _, self.dev_lvm_block = temp_str.split()

        self.logs_creation([f"Start Process Restoring Virtual Machine: {self.name_obj} {self.backup_folder}"])

        self.virsh_command("destroy")
        self.lvm_command("remove")
        self.virsh_command("define")
        self.lvm_command("create")

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
    
    def virsh_command(self, command):
        """ Уничтажает виртуальную машину (VM), восстановление 
            из Backup и запускает виртуальную машину (VM)
        """
        if command == "destroy":
            self.performance_shell(f"virsh destroy {self.name_obj}")
        elif command == "define":
            self.performance_shell(f"virsh define {self.backup_folder}{self.name_obj}.xml")
        elif command == "restore":
            self.performance_shell(f"virsh restore {self.backup_folder}{self.name_obj}.vmstate")
    
    def lvm_command(self, command):
        """ command: (create) Создать блочное устройство LVM. (remove) Удалить блочное устройство LVM.
            size: Размер блочного устройства для Virtual Machine в 'Байтах'. Из файла -raw_info. 
        """

        lvm_size_str = str(self.size_lvm_block)
        lvm_split_str = self.dev_lvm_block.split('/')[-2] 

        if command == "create":
            self.performance_shell(f"sudo lvcreate -y -n {self.name_obj} -L{lvm_size_str}B {lvm_split_str}")
            self.logs_creation([f"LVM Block Device Create: {self.name_obj} Size: {lvm_size_str} Byte Target: {self.dev_lvm_block}"])
            self.archive_creation()
        elif command == "remove":
            self.performance_shell(f"sudo lvremove -f {self.dev_lvm_block}")
            self.logs_creation([f"LVM Block Device Remove {self.dev_lvm_block}"])
    
    def archive_creation(self):
        self.logs_creation([f"Process GUNZIP LVM Block Device: For disk recovery VM: {self.name_obj}"])
        self.performance_shell(f"gunzip -ck {self.backup_folder}{self.name_obj}.gz > {self.dev_lvm_block}")
        self.virsh_command("restore")
