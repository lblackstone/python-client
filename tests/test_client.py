"""Tests for the objectrocket.client module."""
from objectrocket import auth
from objectrocket import constants
from objectrocket import instances
from objectrocket.client import Client


#################################
# Tests for Client constructor. #
#################################
def test_client_binds_correct_default_url(patched_requests_map):
    username, password = 'tester', 'testpass'
    client = Client(username, password)
    assert client._url == constants.DEFAULT_API_URL


def test_client_binds_alternative_url_properly(patched_requests_map):
    username, password = 'tester', 'testpass'
    client = Client(username, password, alternative_url='testing')
    assert client._url == 'testing'


def test_client_binds_proper_username_and_password_properties(patched_requests_map):
    username, password = 'tester', 'testpass'
    client = Client(username, password)
    assert client._username == username
    assert client._password == password


def test_client_makes_auth_request_upon_instantiation(patched_requests_map):
    username, password = 'tester', 'testpass'
    client = Client(username, password, alternative_url='testing/')
    patched_requests_map['auth'].get.assert_called_once_with(
        client.auth._url,
        auth=(username, password),
        **client.auth._default_request_kwargs
    )


def test_client_binds_auth_token_properly(patched_requests_map, obj):
    username, password = 'tester', 'testpass'
    obj.json = lambda: {'data': {'token': 'testing_token'}}
    patched_requests_map['auth'].get.return_value = obj

    client = Client(username, password)

    assert client._token == 'testing_token'


######################################
# Tests for Client public interface. #
######################################
def test_client_has_embedded_auth_class(patched_requests_map):
    username, password = 'tester', 'testpass'
    client = Client(username, password)
    assert isinstance(client.auth, auth.Auth)


def test_client_has_embedded_instances_class(patched_requests_map):
    username, password = 'tester', 'testpass'
    client = Client(username, password)
    assert isinstance(client.instances, instances.Instances)


#######################################
# Tests for Client private interface. #
#######################################
def test_client_token_setter_binds_new_token(patched_requests_map):
    username, password = 'tester', 'testpass'
    client = Client(username, password)
    new_token = 'new_test_token'

    client._token = new_token

    assert client._token == new_token
