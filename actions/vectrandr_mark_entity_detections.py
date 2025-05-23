# File: vectrandr_mark_entity_detection.py
#
# Copyright (c) 2024-2025 Vectra
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

import phantom.app as phantom

import vectrandr_consts as consts
from actions import BaseAction


class MarkEntityDetectionsAction(BaseAction):
    """Class to handle mark entity detections action."""

    def execute(self):
        """Execute the mark entity detections action."""
        entity_type = self._param["entity_type"].lower()

        ret_val, entity_id = self._connector.util._validate_integer(self._action_result, self._param["entity_id"], "entity_id", True)
        if phantom.is_fail(ret_val):
            return self._action_result.get_status()

        if entity_type not in consts.VECTRA_VALID_ENTITIES:
            return self._action_result.set_status(phantom.APP_ERROR, consts.VECTRA_ERROR_INVALID_ENTITY)

        url = f"""{consts.VECTRA_API_VERSION}{
            consts.VECTRA_ENTITY_ENDPOINT.format(entity_type=consts.ENTITY_TYPE_MAPPING[entity_type], entity_id=entity_id)
        }"""
        ret_val, entity_repsonse = self._connector.util._make_rest_call_helper(url, self._action_result)
        if phantom.is_fail(ret_val):
            return self._action_result.get_status()

        detection_set = entity_repsonse.get("detection_set")
        if not detection_set:
            return self._action_result.set_status(phantom.APP_SUCCESS, "No detections found for given entity")

        ret_val, detection_ids = self._connector.util._extract_detection_id_from_entity_response(self._action_result, detection_set)
        if phantom.is_fail(ret_val):
            return self._action_result.get_status()

        ret_val, response = self._connector.util._mark_detection(self._action_result, detection_ids, "True")
        if phantom.is_fail(ret_val):
            return self._action_result.get_status()

        self._action_result.add_data(response)

        return self._action_result.set_status(phantom.APP_SUCCESS, "Successfully marked detections")
