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
from __future__ import annotations

import unittest

import boto3

from airflow.providers.amazon.aws.hooks.emr import EmrHook

try:
    from moto import mock_emr
except ImportError:
    mock_emr = None


@unittest.skipIf(mock_emr is None, 'moto package not present')
class TestEmrHook(unittest.TestCase):
    @mock_emr
    def test_get_conn_returns_a_boto3_connection(self):
        hook = EmrHook(aws_conn_id='aws_default', region_name='ap-southeast-2')
        assert hook.get_conn().list_clusters() is not None

    @mock_emr
    def test_create_job_flow_uses_the_emr_config_to_create_a_cluster(self):
        client = boto3.client('emr', region_name='us-east-1')

        hook = EmrHook(aws_conn_id='aws_default', emr_conn_id='emr_default')
        cluster = hook.create_job_flow({'Name': 'test_cluster'})

        assert client.list_clusters()['Clusters'][0]['Id'] == cluster['JobFlowId']

    @mock_emr
    def test_create_job_flow_extra_args(self):
        """
        Test that we can add extra arguments to the launch call.

        This is useful for when AWS add new options, such as
        "SecurityConfiguration" so that we don't have to change our code
        """
        client = boto3.client('emr', region_name='us-east-1')

        hook = EmrHook(aws_conn_id='aws_default', emr_conn_id='emr_default')
        # AmiVersion is really old and almost no one will use it anymore, but
        # it's one of the "optional" request params that moto supports - it's
        # coverage of EMR isn't 100% it turns out.
        cluster = hook.create_job_flow({'Name': 'test_cluster', 'ReleaseLabel': '', 'AmiVersion': '3.2'})

        cluster = client.describe_cluster(ClusterId=cluster['JobFlowId'])['Cluster']

        # The AmiVersion comes back as {Requested,Running}AmiVersion fields.
        assert cluster['RequestedAmiVersion'] == '3.2'

    @mock_emr
    def test_get_cluster_id_by_name(self):
        """
        Test that we can resolve cluster id by cluster name.
        """
        hook = EmrHook(aws_conn_id='aws_default', emr_conn_id='emr_default')

        job_flow = hook.create_job_flow(
            {'Name': 'test_cluster', 'Instances': {'KeepJobFlowAliveWhenNoSteps': True}}
        )

        job_flow_id = job_flow['JobFlowId']

        matching_cluster = hook.get_cluster_id_by_name('test_cluster', ['RUNNING', 'WAITING'])

        assert matching_cluster == job_flow_id

        no_match = hook.get_cluster_id_by_name('foo', ['RUNNING', 'WAITING', 'BOOTSTRAPPING'])

        assert no_match is None
