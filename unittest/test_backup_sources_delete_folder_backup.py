"""
Project Name: 'backup-kvm'
Version: 1.0

Description: Unit Test: restore_kvm_vm_in_lvm.py

Ihor Cheberiak (c) 2021
https://www.linkedin.com/in/ihor-cheberiak/
"""

import unittest
import unittest.mock

from backup.sources.delete_folder_backup import DeleteFolderBackup


class Test_DeleteFolderBackup(unittest.TestCase):
    def setUp(self) -> None:
        seting_app = ["/var/log/", "/var/backup/prod-vm/", 2]
        self.delete_folder = DeleteFolderBackup(seting_app[0], seting_app[1], seting_app[2])

    def test_logs_creation(self):
        pass
    
    def test_performance_shell(self):
        pass

if __name__ == '__main__':
    unittest.main()
