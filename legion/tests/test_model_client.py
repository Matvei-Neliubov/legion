#
#    Copyright 2017 EPAM Systems
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
from __future__ import print_function

import unittest2
import os

try:
    from .legion_test_utils import patch_environ
except ImportError:
    from legion_test_utils import patch_environ
import legion.config
import legion.model.client
import legion.serving.pyserve as pyserve


class TestModelClient(unittest2.TestCase):
    MODEL_ID = 'temp'
    MODEL_VERSION = '1.8'

    def test_image_loading(self):
        image = self.data_directory = os.path.join(os.path.dirname(__file__), 'data', 'nine.png')
        result = legion.model.client.load_image(image)
        self.assertIsInstance(result, bytes)

    def test_image_loading_wrong(self):
        image = self.data_directory = os.path.join(os.path.dirname(__file__), 'data', 'nine-text.yaml')
        with self.assertRaises(Exception):
            result = legion.model.client.load_image(image)

    def test_client_building(self):
        client = legion.model.client.ModelClient(self.MODEL_ID, 'localhost')
        root_url = 'localhost/api/model/{}'.format(self.MODEL_ID)
        self.assertEqual(client.api_url, root_url)
        self.assertEqual(client.info_url, root_url + '/info')
        self.assertEqual(client.invoke_url, root_url + '/invoke')

    def test_client_building_relative(self):
        client = legion.model.client.ModelClient(self.MODEL_ID, use_relative_url=True)
        root_url = '/api/model/{}'.format(self.MODEL_ID)
        self.assertEqual(client.api_url, root_url)
        self.assertEqual(client.info_url, root_url + '/info')
        self.assertEqual(client.invoke_url, root_url + '/invoke')

    def test_client_building_from_env(self):
        with patch_environ({legion.config.MODEL_SERVER_URL[0]: 'test:10'}):
            client = legion.model.client.ModelClient(self.MODEL_ID)
            root_url = 'test:10/api/model/{}'.format(self.MODEL_ID)
            self.assertEqual(client.api_url, root_url)
            self.assertEqual(client.info_url, root_url + '/info')
            self.assertEqual(client.invoke_url, root_url + '/invoke')


if __name__ == '__main__':
    unittest2.main()
