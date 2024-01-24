# File: vectrandr_resolve_assignment.py
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

import phantom.app as phantom

import vectrandr_consts as consts
from actions import BaseAction


class ResolveAssignmentAction(BaseAction):
    """Class to handle resolve assignment action."""

    def execute(self):
        """Execute the resolve assignment action."""
        ret_val, assignment_id = self._connector.util._validate_integer(
            self._action_result, self._param['assignment_id'], "assignment_id", True)
        if phantom.is_fail(ret_val):
            return self._action_result.get_status()

        ret_val, outcome = self._connector.util._get_outcome(self._action_result, self._param['outcome'])
        if phantom.is_fail(ret_val):
            return self._action_result.get_status()

        note = self._param.get("note", "Updated by Splunk SOAR")
        triage_as = self._param.get("triage_as")

        ret_val, detection_ids = self._connector.util._extract_ids_from_params(
            self._action_result, 'detection_ids', self._param.get('detection_ids', ""), False, True)
        if phantom.is_fail(ret_val):
            return self._action_result.get_status()

        url = f'{consts.VECTRA_API_VERSION}{consts.VECTRA_RESOLVE_ASSIGNMENT_ENDPOINT.format(assignment_id=assignment_id)}'
        payload = {
            "outcome": outcome,
            "note": note,
            "triage_as": triage_as,
            "detection_ids": detection_ids
        }

        ret_val, response = self._connector.util._make_rest_call_helper(url, self._action_result, method='put', json=payload)

        if phantom.is_fail(ret_val):
            return self._action_result.get_status()

        self._action_result.add_data(response.get("assignment", {}))

        return self._action_result.set_status(phantom.APP_SUCCESS, "Successfully resolved assignment")
