#!/usr/bin/env python3

"""
Project Name: 'backup-kvm'
Version: 1.1

Description: 

Ihor Cheberiak (c) 2021
https://www.linkedin.com/in/ihor-cheberiak/
"""

import sys
import json
import argparse

from sources.backup_dir_ssh import BackupDirSSH
from sources.backup_kvm_lvm import BackupKVMinLVM
from sources.backup_kvm_image import BackupKVMinIMG
from sources.restore_kvm_lvm import RestoreKVMinLVM
from sources.restore_kvm_image import RestoreKVMinIMG
from sources.delete_folder_backup import DeleteFolderBackup


help_parser = argparse.ArgumentParser(description="Backup and Restore Virtual Machines and Folders")
help_parser.add_argument("-settings_name_json", type=str, default="settings.json", help="Example: settings.json")

args_parser = help_parser.parse_args()
settings_json = args_parser.setings_name_json


def init_backup(args):
    if args[0] == 1:
        delete_backup = DeleteFolderBackup(args[1], args[2], args[4], args[8])
        delete_backup.main_setup()

        backup_vm_lvm = BackupKVMinLVM(args[1], args[3], args[4], args[2], args[7], args[6])
        backup_vm_lvm.main_setup()
    elif args[0] == 2:
        delete_backup = DeleteFolderBackup(args[1], args[2], args[4], args[8])
        delete_backup.main_setup()

        backup_vm_img = BackupKVMinIMG(args[1], args[3], args[4], args[2], args[6])
        backup_vm_img.main_setup()
    elif args[0] == 3:
        backup_vm_lvm = RestoreKVMinLVM(args[1], args[2], args[5])
        backup_vm_lvm.main_setup()
    elif args[0] == 4:
        backup_vm_img = RestoreKVMinIMG(args[1], args[2], args[5])
        backup_vm_img.main_setup()
    elif args[0] == 5:
        backup_dir_ssh = BackupDirSSH()
        backup_dir_ssh.main_setup()


def close_backup():
    sys.exit()


if __name__ == '__main__':
    with open(f"{settings_json}", "r") as j:
        settings_json = json.load(j)

    settings = [parameter for _, parameter in settings_json.items()]

    init_backup(settings)
    close_backup()
