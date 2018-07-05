
import os
import json
import tempfile
import shutil

import pytest

from dtoolcore import generate_admin_metadata

from dtool_azure.storagebroker import (
    AzureStorageBroker,
)

_HERE = os.path.dirname(__file__)
TEST_SAMPLE_DATA = os.path.join(_HERE, "data")


def _key_exists_in_storage_broker(storage_broker, key):

    return storage_broker._blobservice.exists(storage_broker.uuid, key)


def _get_data_structure_from_key(storage_broker, key):

    text_blob = storage_broker._blobservice.get_blob_to_text(
        storage_broker.uuid,
        key
    )

    return json.loads(text_blob.content)


def _get_unicode_from_key(storage_broker, key):

    text_blob = storage_broker._blobservice.get_blob_to_text(
        storage_broker.uuid,
        key
    )

    return text_blob.content


def _remove_dataset(uri):

    storage_broker = AzureStorageBroker(uri)

    storage_broker._blobservice.delete_container(storage_broker.uuid)


@pytest.fixture
def tmp_uuid_and_uri(request):
    admin_metadata = generate_admin_metadata("test_dataset")
    uuid = admin_metadata["uuid"]

    uri = AzureStorageBroker.generate_uri(
        "test_dataset",
        uuid,
        "azure://test-dtool-azure-collection"
    )

    @request.addfinalizer
    def teardown():
        _remove_dataset(uri)

    return (uuid, uri)


@pytest.fixture
def tmp_dir_fixture(request):
    d = tempfile.mkdtemp()

    @request.addfinalizer
    def teardown():
        shutil.rmtree(d)
    return d
