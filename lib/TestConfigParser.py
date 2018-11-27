import unittest
from lib import ConfigParser
import platform


class MyTestCase(unittest.TestCase):

    file = 'test_datadog.json'

    def test_get_hostname(self):
        conf = ConfigParser(self.file)
        self.assertEqual(conf.get_host_name(), platform.node())

    def test_get_config_valid(self):
        conf = ConfigParser(self.file)
        self.assertIsNot(conf.schema, None)
        self.assertIsNot(conf.config, None)
        self.assertIsNot(conf.get_config, False)
        conf.config = ["wrong config"]
        self.assertEquals(conf.get_config, "['wrong config'] is not of type 'object'")


if __name__ == '__main__':
    unittest.main()
