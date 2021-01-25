from pathlib import Path
from unittest import mock
import responses
import json
import gzip
from tests.cli_test_case import CliTestCase
from launchable.utils.http_client import get_base_url


class MinitestTest(CliTestCase):
    test_files_dir = Path(__file__).parent.joinpath('../data/minitest/').resolve()
    result_file_path = test_files_dir.joinpath('record_test_result.json')

    @responses.activate
    def test_record_test_minitest(self):
        responses.add(responses.POST, "{}/intake/organizations/launchableinc/workspaces/mothership/builds/{}/test_sessions/{}/events".format(get_base_url(), self.build_name, self.session_id),
                      json={}, status=200)
        result = self.cli('record', 'tests',  '--session', self.session, 'minitest', str(self.test_files_dir) + "/")
        self.assertEqual(result.exit_code, 0)

        payload = json.loads(gzip.decompress(
            b''.join(responses.calls[0].request.body)).decode())

        expected = self.load_json_from_file(self.result_file_path)
        self.assert_json_orderless_equal(expected, payload)
