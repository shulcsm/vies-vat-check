from datetime import datetime
import pytest

from viesvatcheck.client import Client, TEST_WSDL
from viesvatcheck.exceptions import EXCEPTION_MAP

client = Client(TEST_WSDL)


def test_valid_request_valid_number():
    success, response = client.check('LV', '100')
    assert success is True
    assert response == {
        'countryCode': 'LV',
        'vatNumber': '100',
        'requestDate': datetime.now().date(),
        'valid': True,
        'name': 'John Doe',
        'address': '123 Main St, Anytown, UK'
    }


def test_valid_request_invalid_number():
    success, response = client.check('LV', '200')
    assert success is False
    assert response == {
        'countryCode': 'LV',
        'vatNumber': '200',
        'requestDate': datetime.now().date(),
        'valid': False,
        'name': '---',
        'address': '---'
    }


def test_error():
    for number, error in (
            ('201', 'INVALID_INPUT'),
            ('202', 'INVALID_REQUESTER_INFO'),
            ('300', 'SERVICE_UNAVAILABLE'),
            ('301', 'MS_UNAVAILABLE'),
            ('302', 'TIMEOUT'),
            ('400', 'VAT_BLOCKED'),
            ('401', 'IP_BLOCKED'),
            ('500', 'GLOBAL_MAX_CONCURRENT_REQ'),
            ('501', 'GLOBAL_MAX_CONCURRENT_REQ_TIME'),
            ('600', 'MS_MAX_CONCURRENT_REQ'),
            ('601', 'MS_MAX_CONCURRENT_REQ_TIME'),
    ):
        with pytest.raises(EXCEPTION_MAP[error]):
            client.check('LV', number)
