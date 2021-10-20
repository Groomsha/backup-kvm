#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

"""
Project Name: 'backup-kvm'
Version: 1.0

Description: Unit Test: test_delete_folder_backup.py

Ihor Cheberiak (c) 2021
https://www.linkedin.com/in/ihor-cheberiak/
"""

import unittest
import sources as service


class TestDeleteFolderBackup(unittest.TestCase):
    def setUp(self) -> None:
        self.delete_folder = service.DeleteFolderBackup("srv4prod-vm", "/unittest/.test_folder_cash/", "/unittest/.test_folder_cash/", 3)


if __name__ == '__main__':
    unittest.main()
    