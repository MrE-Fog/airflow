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
"""This module is deprecated. Please use :mod:`airflow.providers.opsgenie.operators.opsgenie`."""
from __future__ import annotations

import warnings

from airflow.providers.opsgenie.operators.opsgenie import OpsgenieCreateAlertOperator

warnings.warn(
    "This module is deprecated. Please use `airflow.providers.opsgenie.operators.opsgenie`.",
    DeprecationWarning,
    stacklevel=2,
)


class OpsgenieAlertOperator(OpsgenieCreateAlertOperator):
    """
    This operator is deprecated.
    Please use :class:`airflow.providers.opsgenie.operators.opsgenie.OpsgenieCreateAlertOperator`.
    """

    def __init__(self, *args, **kwargs):
        warnings.warn(
            "This operator is deprecated. "
            "Please use :class:`airflow.providers.opsgenie.operators.opsgenie.OpsgenieCreateAlertOperator`.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)
