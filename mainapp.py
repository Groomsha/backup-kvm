#!/usr/bin/env python3

"""
Project Name: 'backup-kvm'
Version: 1.1

Description: 

Ihor Cheberiak (c) 2021
https://www.linkedin.com/in/ihor-cheberiak/
"""

import os
import json
import argparse

from sources.backup_dir_ssh import BackupDirSSH
from sources.backup_kvm_lvm import BackupKVMinLVM
from sources.backup_kvm_image import BackupKVMinIMG
from sources.restore_kvm_lvm import RestoreKVMinLVM
from sources.restore_kvm_image import RestoreKVMinIMG
from sources.delete_folder_backup import DeleteFolderBackup


help_parser = argparse.ArgumentParser(description="Backup and Restore Virtual Machines and Folders")
help_parser.add_argument("-setings_name_json", type=str, default="setings.json", help="Example: setings.json")

args_parser = help_parser.parse_args()
setings_json = args_parser.setings_name_json

if __name__ == '__main__':
    with open(f"{setings_json}", "r") as setings_json:
        setings = json.load(setings_json)

    seting_app = [parameter for _, parameter in setings.items()]

    if seting_app[0] == 1:
        delete_backup = DeleteFolderBackup(seting_app[1], seting_app[2], seting_app[4], seting_app[8])
        delete_backup.main_setup()

        backup_VM_LVM = BackupKVMinLVM(seting_app[1], seting_app[3], seting_app[4], seting_app[2], seting_app[7], seting_app[6])
        backup_VM_LVM.main_setup()
    elif seting_app[0] == 2:
        delete_backup = DeleteFolderBackup(seting_app[1], seting_app[2], seting_app[4], seting_app[8])
        delete_backup.main_setup()

        backup_VM_IMG = BackupKVMinIMG(seting_app[1], seting_app[3], seting_app[4], seting_app[2], seting_app[6])
        backup_VM_IMG.main_setup()
    elif seting_app[0] == 3:
        restore_VM_LVM = RestoreKVMinLVM(seting_app[1], seting_app[2], seting_app[5])
        restore_VM_LVM.main_setup()
    elif seting_app[0] == 4:
        restore_VM_IMG = RestoreKVMinIMG(seting_app[1], seting_app[2], seting_app[5])
        restore_VM_IMG.main_setup()
    elif seting_app[0] == 5:
        backup_dir_SSH = BackupDirSSH()
        backup_dir_SSH.main_setup()

    os._exit(0)
