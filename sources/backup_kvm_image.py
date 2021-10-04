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


class BackupKVMinIMG():
    def __init__(self, name_obj, dir_obj, dir_backup, dir_logs, compression):
        self.name_obj = name_obj
        self.dir_obj = dir_obj
        self.dir_backup = dir_backup
        self.dir_logs = dir_logs
        self.compression = str(compression)

    def main_setup(self):
        self.concatenation_folder()

        self.virsh_command()
        self.archive_creation()

        self.logs_creation(["#"*120])

    def concatenation_folder(self):
        time_backup = time_os.strftime("%d.%m.%Y")

        self.folder_backup = f"{self.name_obj}_{time_backup}"
        self.touch_folder = f"{self.dir_backup}{self.folder_backup}/{self.name_obj}"

    def logs_creation(self, messages):
        if terminal_os.path.isfile(f"{self.dir_logs}{self.name_obj}.log"):
            access_type = "a"
        else:
            access_type = "w"
        
        time_message = time_os.ctime()
        with open(f"{self.dir_logs}{self.name_obj}.log", access_type) as log:
            for message in messages:
                log.write(f"\n{time_message} {message}")

    def performance_shell(self, command, wait_shell = True):
        shell_os = shell.Popen(command, stdout=shell.PIPE, stderr=shell.PIPE, shell=True, executable="/bin/bash", universal_newlines=True)

        if wait_shell: shell_os.wait()
        
        output, errors = shell_os.communicate()
        if len(str(output)) != 0:
            self.logs_creation(str(output.strip()).splitlines())
        if len(str(errors)) != 0:
            self.logs_creation(str(errors.strip()).splitlines())


    def virsh_command(self, command = None):
        """ Остонавливает виртуальную машину (VM) и собирает информацию
            для ее восстановления из Backup по надобности в будущем.
        """
        if terminal_os.popen(f"virsh domstate {self.name_obj}").read().split() == ["running"]:
            self.performance_shell(f"virsh shutdown {self.name_obj}")
        if terminal_os.popen(f"virsh domstate {self.name_obj}").read().split() != ["running"]:
            dir_img_temp = self.dir_obj[self.dir_obj.find(".")-1:]
            self.performance_shell(f"virsh dumpxml {self.name_obj} > {self.touch_folder}.xml")
            self.performance_shell(f"virsh domblkinfo {self.name_obj} {self.dir_obj} > {self.touch_folder}-{3}_info && virsh vol-pool {self.dir_obj} >> {self.touch_folder}-{dir_img_temp}_info && echo {self.dir_obj} >> {self.touch_folder}-{dir_img_temp}_info") 
        
        self.logs_creation([f"Process Virsh: Shutdown VM and creation of auxiliary files {self.name_obj} VM!"])

        if command == "start":
            self.performance_shell(f"virsh start {self.name_obj}")
            self.logs_creation([f"Process Virsh: Start VM {self.name_obj} - Running"])

    def archive_creation(self):
        """ compression: Степень сжатия .gz файла от 1 до 9. Чем выше степень,
            тем больше нужно мощностей процессора и времени на создание архива.
        """
        dir_img_temp = self.dir_obj[self.dir_obj.find("."):]
        self.logs_creation([f"Process GZIP Disk Image: For disk recovery Virtual Machine {self.name_obj}"])
        self.performance_shell(f"dd if={self.dir_obj} | gzip -kc -{self.compression} > {self.touch_folder}{dir_img_temp}.gz")
        self.virsh_command("start")
