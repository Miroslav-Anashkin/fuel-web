# -*- coding: utf-8 -*-

#    Copyright 2013 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json

from nailgun.db.sqlalchemy.models import Release
from nailgun.test.base import BaseIntegrationTest
from nailgun.test.base import reverse


class TestHandlers(BaseIntegrationTest):
    def test_release_put_change_name_and_version(self):
        release = self.env.create_release(api=False)
        resp = self.app.put(
            reverse('ReleaseHandler', kwargs={'obj_id': release.id}),
            params=json.dumps({
                'name': 'modified release',
                'version': '5.1'
            }),
            headers=self.default_headers,
            expect_errors=True)
        self.assertEquals(200, resp.status_code)
        response = json.loads(resp.body)
        release_from_db = self.db.query(Release).one()
        self.db.refresh(release_from_db)
        self.assertEquals('5.1', release_from_db.version)
        self.assertEquals('5.1', response['version'])
        self.assertEquals('modified release', response['name'])

    def test_release_put_returns_400_if_no_body(self):
        release = self.env.create_release(api=False)
        resp = self.app.put(
            reverse('ReleaseHandler', kwargs={'obj_id': release.id}),
            "",
            headers=self.default_headers,
            expect_errors=True)
        self.assertEquals(resp.status_code, 400)

    def test_release_delete_returns_400_if_clusters(self):
        cluster = self.env.create_cluster(api=False)
        resp = self.app.delete(
            reverse('ReleaseHandler',
                    kwargs={'obj_id': cluster.release.id}),
            headers=self.default_headers,
            expect_errors=True
        )
        self.assertEquals(resp.status_code, 400)
        self.assertEquals(
            resp.body,
            "Can't delete release with "
            "clusters assigned"
        )
