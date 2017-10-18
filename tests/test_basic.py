# -*- coding: utf-8 -*-


from .context import FetchPublicBlacklists  # noqa
from FetchPublicBlacklists import FetchPublicBlacklists  # noqa
from FetchPublicBlacklists import helpers  # noqa
import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_absolute_truth_and_meaning(self):
        assert True

    def test_IP_to_IPv4(self):
        """Test IP binary string to IPv4 Dot notation"""
        self.assertEqual(helpers.IP_to_IPv4('00000000000000000000000000000000'), '0.0.0.0')
        self.assertEqual(
            helpers.IPs_to_IPv4s(
                [
                    '00000000000000000000000000000000',
                    '10001000100110100011111010101001'
                ]
            ),
            ['0.0.0.0', '136.154.62.169']
        )


    def test_IPv4_to_IP(self):
        """Test IPv4 Dot notation to IP binary string"""
        self.assertEqual(helpers.IPv4_to_IP('0.0.0.0'), '00000000000000000000000000000000')
        self.assertEqual(
            helpers.IPv4s_to_IPs(['0.0.0.0', '136.154.62.169']),
            [
                '00000000000000000000000000000000',
                '10001000100110100011111010101001'
            ]
        )

    def test_IP_to_Int(self):
        """Test IP binary string to int"""
        self.assertEqual(helpers.IP_to_int('00000000000000000000000000000000'), 0)
        self.assertEqual(helpers.IP_to_int('10001000100110100011111010101001'), 2291809961)

    def test_Int_to_IP(self):
        """Test int to IP binary string"""
        self.assertEqual(helpers.int_to_IP(0), '00000000000000000000000000000000')
        self.assertEqual(helpers.int_to_IP(2291809961), '10001000100110100011111010101001')

    def test_Int_to_IPv4(self):
        """Test Int to IPv4 Dot notation"""
        self.assertEqual(helpers.int_to_IPv4(0), '0.0.0.0')
        self.assertEqual(helpers.int_to_IPv4(2291809961), '136.154.62.169')
        someInts = helpers.ints_to_IPv4s([
            111239847,
            167239847,
            2291809961,
            67306243,
            0
        ])
        someIPv4s = [
            '6.161.98.167',
            '9.247.224.167',
            '136.154.62.169',
            '4.3.3.3',
            '0.0.0.0'
        ]
        self.assertEqual(len(someIPv4s), len(someInts))
        for someIndex in range(len(someInts)):
            self.assertEqual(someInts[someIndex], someIPv4s[someIndex])

    def test_IPv4_to_int(self):
        """Test IPv4 Dot notation to int"""
        self.assertEqual(helpers.int_to_IPv4(0), '0.0.0.0')
        self.assertEqual(helpers.int_to_IPv4(2291809961), '136.154.62.169')
        someInts = [
            111239847,
            167239847,
            2291809961,
            67306243,
            0,
            None
        ]
        someIPv4s = helpers.IPv4s_to_ints([
            '6.161.98.167',
            '9.247.224.167',
            '136.154.62.169',
            '4.3.3.3',
            '0.0.0.0',
            None
        ])
        self.assertEqual(len(someIPv4s), len(someInts))
        for someIndex in range(len(someInts)):
            self.assertEqual(someIPv4s[someIndex], someInts[someIndex])

    def test_IP_to_int(self):
        """Test IP to int"""
        self.assertEqual(helpers.int_to_IPv4(0), '0.0.0.0')
        self.assertEqual(helpers.int_to_IPv4(2291809961), '136.154.62.169')
        someInts = [
            111239847,
            167239847,
            2291809961,
            67306243,
            0
        ]
        someIPs = helpers.IPs_to_ints([
            '00000110101000010110001010100111',
            '00001001111101111110000010100111',
            '10001000100110100011111010101001',
            '00000100000000110000001100000011',
            '00000000000000000000000000000000'
        ])
        self.assertEqual(len(someIPs), len(someInts))
        for someIndex in range(len(someInts)):
            self.assertEqual(someIPs[someIndex], someInts[someIndex])

    def test_IPv4s_to_CIDRs(self):
        """Test of generating IPv4 CIDR suffix string from IPv4 Dot notations"""
        test_list = [
            '1.2.3.1', '1.2.3.2', '1.2.3.3',
            '1.2.3.4', '1.2.3.5', '1.2.3.6',
            '5.6.7.8', '8.7.6.5', '1.2.2.250',
            '41.2.2.251', '1.2.2.252', '1.2.2.253',
            '1.2.2.254', '1.2.2.255'
        ]
        match_list = [
            '1.2.3.0/29', '1.2.3.4/30',
            '5.6.7.8', '8.7.6.5',
            '1.2.2.250', '41.2.2.251',
            '1.2.2.252/30'
        ]
        self.assertEqual(helpers.compress_ip_list_to_cidr(test_list), match_list)

    def test_IPv4_to_CIDR(self):
        """Test of generating IPv4 CIDR string from IPv4 Dot notation"""
        match_list = '1.2.3.0/29'
        self.assertEqual(helpers.IPRange_to_CIDR('1.2.3.1', '1.2.3.6'), match_list)

    def test_noop(self):
        """Test of junk for coverage"""
        self.assertFalse(helpers.getBcastAddrforIPv4())
        self.assertIsNone(helpers.no_op())


if __name__ == '__main__':
    unittest.main()
