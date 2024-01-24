# File: test_vectrandr_remove_tags.py
#
# Copyright (c) 2024 Vectra
#
# This unpublished material is proprietary to Vectra.
# All rights reserved. The methods and
# techniques described herein are considered trade secrets
# and/or confidential. Reproduction or distribution, in whole
# or in part, is forbidden except by express written permission
# of Vectra.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.


import json
import unittest
from unittest.mock import patch

from vectrandr_connector import VectraNDRConnector

from . import vectrandr_config, vectrandr_responses


class RemoveTagsAction(unittest.TestCase):
    """Class to test the remove tags action."""

    def setUp(self):
        """Set up method for the tests."""
        self.connector = VectraNDRConnector()
        self.test_json = dict()
        self.test_json = dict(vectrandr_config.TEST_JSON)
        self.test_json.update({"action": "remove tags", "identifier": "remove_tags"})

        return super().setUp()

    @patch("vectrandr_utils.requests.get")
    @patch("vectrandr_utils.requests.patch")
    def test_remove_detection_pass(self, mock_get, mock_patch):
        """Test the valid case for the remove tags action.

        Token is available in the state file.
        Patch the get() to return the valid response.
        """
        self.test_json['parameters'] = [{'entity_id': 2584, "entity_type": "host", "tags_list": "tag2,tag3"}]

        mock_get.return_value.status_code = 200
        mock_get.return_value.headers = vectrandr_config.DEFAULT_HEADERS
        mock_get.return_value.json.return_value = vectrandr_responses.PATCH_TAGS_RESP

        mock_patch.return_value.status_code = 200
        mock_patch.return_value.headers = vectrandr_config.DEFAULT_HEADERS
        mock_patch.return_value.json.return_value = vectrandr_responses.GET_TAGS_RESP

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        ret_val = json.loads(ret_val)

        self.assertEqual(ret_val["result_summary"]["total_objects"], 1)
        self.assertEqual(ret_val["result_summary"]["total_objects_successful"], 1)
        self.assertEqual(ret_val["status"], "success")

    @patch("vectrandr_utils.requests.get")
    def test_remove_tags_notexist_entity_id(self, mock_get):
        """Test the valid case for the remove tags action.

        Token is available in the state file.
        Patch the get() to return the valid response.
        """
        self.test_json['parameters'] = [{'entity_id': 21123445552, "entity_type": "host", "tags_list": "tag2,tag3"}]

        mock_get.return_value.status_code = 404
        mock_get.return_value.headers = vectrandr_config.DEFAULT_HEADERS
        mock_get.return_value.json.return_value = vectrandr_responses.OBJECT_NOT_FOUND_RESP

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        ret_val = json.loads(ret_val)

        self.assertEqual(ret_val["result_summary"]["total_objects"], 1)
        self.assertEqual(ret_val["result_summary"]["total_objects_successful"], 0)
        self.assertEqual(ret_val["status"], "failed")

    def test_remove_tags_invalid_entity_type(self):
        """Test the invalid case for the remove tags action.

        Token is available in the state file.
        Patch the get() to return the valid response.
        """
        self.test_json['parameters'] = [{'entity_type': "account_not_present", 'entity_id': 1, "tags_list": "tag2,tag3"}]

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        ret_val = json.loads(ret_val)

        self.assertEqual(ret_val["result_summary"]["total_objects"], 1)
        self.assertEqual(ret_val["result_summary"]["total_objects_successful"], 0)
        self.assertEqual(ret_val["status"], "failed")

    def test_remove_tags_invalid_tags_list(self):
        """Test the invalid case for the remove tags action.

        Token is available in the state file.
        Patch the get() to return the valid response.
        """
        self.test_json['parameters'] = [{'entity_type': "account", 'entity_id': 10, "tags_list": ",,,,"}]

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        ret_val = json.loads(ret_val)

        self.assertEqual(ret_val["result_summary"]["total_objects"], 1)
        self.assertEqual(ret_val["result_summary"]["total_objects_successful"], 0)
        self.assertEqual(ret_val["status"], "failed")
