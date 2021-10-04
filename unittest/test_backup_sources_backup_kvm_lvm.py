"""
Project Name: 'backup-kvm'
Version: 1.0

Description: Unit Test: backup_kvm_lvm.py

Ihor Cheberiak (c) 2021
https://www.linkedin.com/in/ihor-cheberiak/
"""

import unittest
import time

from backup.sources.backup_kvm_lvm import BackupKVMinLVM


class Test_BackupKVMinLVM(unittest.TestCase):
    def setUp(self) -> None:
        seting_app = ["srv4prod-vm", "/dev/vg0/prod-vm", "/var/backup/prod-vm/", "/var/log/", 2, 3]
        self.backup_lvm = BackupKVMinLVM(seting_app[0], seting_app[1], seting_app[2], seting_app[3], seting_app[4], seting_app[5])

        self.test_time = time.strftime("%d.%m.%Y")
        self.backup_lvm.concatenation_folder()

    def test_concatenation_folder_backup(self):
        self.assertEqual(f"srv4prod-vm_{self.test_time}", self.backup_lvm.folder_backup)
    
    def test_concatenation_touch_folder(self):
        self.assertEqual(f"/var/backup/prod-vm/srv4prod-vm_{self.test_time}/srv4prod-vm", self.backup_lvm.touch_folder)


if __name__ == '__main__':
    unittest.main()
    