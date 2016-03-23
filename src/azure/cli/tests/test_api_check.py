import unittest
import unittest
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

from azure.cli.commands.resource import _resolve_api_version as resolve_api_version

class TestApiCheck(unittest.TestCase):   

    @classmethod
    def setUpClass(cls):
        pass
        
    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test_resolve_api_max_priority_option(self):
        """ Verifies the --api-version parameter has maximum priority. """
        args = {'api-version': '2015-01-01', 'resource-type': 'Mock/test'}
        self.assertEqual(resolve_api_version(args, self._get_mock_client()), "2015-01-01")

    def test_resolve_api_provider_backup(self):
        """ Verifies provider is used as backup if api-version not specified. """
        args = {'resource-type': 'Mock/test'}
        self.assertEqual(resolve_api_version(args, self._get_mock_client()), "2016-01-01")

    def test_resolve_api_provider_with_parent_backup(self):
        """ Verifies provider (with parent) is used as backup if api-version not specified. """
        args = {'resource-type': 'Mock/bar', 'parent': 'foo/testfoo123'}
        self.assertEqual(resolve_api_version(args, self._get_mock_client()), "1999-01-01")

    def test_resolve_api_all_previews(self):
        """ Verifies most recent preview version returned only if there are no non-preview versions. """
        args = {'resource-type': 'Mock/preview'}
        self.assertEqual(resolve_api_version(args, self._get_mock_client()), "2005-01-01-preview")    

    def _get_mock_client(self):
        client = MagicMock()
        provider = MagicMock()
        provider.resource_types = [
            self._get_mock_resource_type('skip', ['2000-01-01-preview', '2000-01-01']),
            self._get_mock_resource_type('test', ['2016-01-01-preview', '2016-01-01']),
            self._get_mock_resource_type('foo/bar', ['1999-01-01-preview', '1999-01-01']),
            self._get_mock_resource_type('preview', ['2005-01-01-preview', '2004-01-01-preview'])
        ]
        client.providers.get.return_value = provider
        return client

    def _get_mock_resource_type(self, name, api_versions):
        rt = MagicMock()
        rt.resource_type = name
        rt.api_versions = api_versions
        return rt

if __name__ == '__main__':
    unittest.main()
