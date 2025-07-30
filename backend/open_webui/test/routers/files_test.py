import pytest
from unittest.mock import MagicMock, call

import uuid
import time
from fastapi import HTTPException

from open_webui.constants import ERROR_MESSAGES
from open_webui.models.users import (
    UserModel,
)
from open_webui.routers.files import delete_file_by_id

class TestFiles:
    @pytest.fixture
    def mock_user(self):
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = "email@example.com"
        mock_user.name = "John Doe"
        mock_user.role = "user"
        mock_user.created_at = "2022-01-01"
        mock_user.profile_image_url = "https://example.com/image.jpg"
        return mock_user

    def setup_mocks_for_delete_tests(self, monkeypatch, mock_user):
        self.mock_user = mock_user

        # open_webui.retrieval.vector.dbs.chroma.ChromaClient
        self.mock_chroma_db_http_client = MagicMock()
        monkeypatch.setattr("chromadb.HttpClient", self.mock_chroma_db_http_client)

        # Mock internal method to keep delete test complexity lower
        self.mock_has_access_to_file = MagicMock(return_value=True)
        monkeypatch.setattr("open_webui.routers.files.has_access_to_file", self.mock_has_access_to_file)

        self.mock_file = MagicMock()
        self.mock_file.id = id
        self.mock_file.user_id = 1
        self.mock_file.path = f"/mock/file/path/{self.mock_file.id}"

        self.mock_files_get_file_by_id = lambda id: self.mock_file
        monkeypatch.setattr("open_webui.models.files.Files.get_file_by_id", self.mock_files_get_file_by_id)

        self.mock_storage_delete_file = MagicMock()
        monkeypatch.setattr("open_webui.storage.provider.Storage.delete_file", self.mock_storage_delete_file)

        self.mock_vector_db_delete_collection = MagicMock()
        monkeypatch.setattr("open_webui.retrieval.vector.connector.VECTOR_DB_CLIENT.delete_collection", self.mock_vector_db_delete_collection)

        self.mock_db_delete_file_by_id = MagicMock(return_value=True)
        monkeypatch.setattr("open_webui.models.files.Files.delete_file_by_id", self.mock_db_delete_file_by_id)

    @pytest.mark.asyncio
    async def test_delete_file_by_id__should_fail_for_id_belongs_to_other_user_non_admin(self, monkeypatch, mock_user):
        self.mock_user = mock_user

        # User is normal user, file belongs to other user

        self.mock_file = MagicMock()
        self.mock_file.user_id = mock_user + 666

        self.mock_files_get_file_by_id = lambda id: self.mock_file
        monkeypatch.setattr("open_webui.models.files.Files.get_file_by_id", self.mock_files_get_file_by_id)

        self.mock_has_access_to_file = MagicMock(return_value=False)
        monkeypatch.setattr("open_webui.routers.files.has_access_to_file", self.mock_has_access_to_file)

        mock_file_id = "mock-file-id-of-other-user"

        with pytest.raises(Exception, match=ERROR_MESSAGES.NOT_FOUND):
            await delete_file_by_id(mock_file_id, self.mock_user)

    @pytest.mark.asyncio
    async def test_delete_file_by_id__should_fail_for_id_belongs_to_other_user_current_user_is_admin(self, monkeypatch, mock_user):
        self.mock_user = mock_user

        # User is admin, file belongs to other user

        self.mock_file = MagicMock()
        self.mock_user.role = "user"
        self.mock_file.user_id = mock_user + 666

        self.mock_files_get_file_by_id = lambda id: self.mock_file
        monkeypatch.setattr("open_webui.models.files.Files.get_file_by_id", self.mock_files_get_file_by_id)

        self.mock_has_access_to_file = MagicMock(return_value=False)
        monkeypatch.setattr("open_webui.routers.files.has_access_to_file", self.mock_has_access_to_file)

        mock_file_id = "mock-file-id-of-other-user"

        with pytest.raises(Exception, match=ERROR_MESSAGES.NOT_FOUND):
            await delete_file_by_id(mock_file_id, self.mock_user)

    @pytest.mark.asyncio
    async def test_delete_file_by_id__should_fail_for_not_accessible(self, monkeypatch, mock_user):
        self.mock_user = mock_user

        # File belongs to other user, user is not admin, does not have permissions

        self.mock_file = MagicMock()
        self.mock_user.role = "user"
        self.mock_file.user_id = mock_user + 666

        self.mock_files_get_file_by_id = lambda id: self.mock_file
        monkeypatch.setattr("open_webui.models.files.Files.get_file_by_id", self.mock_files_get_file_by_id)

        self.mock_has_access_to_file = MagicMock(return_value=False)
        monkeypatch.setattr("open_webui.routers.files.has_access_to_file", self.mock_has_access_to_file)

        mock_file_id = "mock-file-id-of-other-user"

        with pytest.raises(Exception, match=ERROR_MESSAGES.NOT_FOUND):
            await delete_file_by_id(mock_file_id, self.mock_user)

        self.mock_has_access_to_file.assert_has_calls([call(mock_file_id, "write", self.mock_user)])

    @pytest.mark.asyncio
    async def test_delete_file_by_id__delete_ok(self, monkeypatch, mock_user):
        self.setup_mocks_for_delete_tests(monkeypatch, mock_user)

        mock_file_id = "mock-file-id"

        await delete_file_by_id(mock_file_id, self.mock_user)

        self.mock_storage_delete_file.assert_has_calls([call(self.mock_file.path)])

        self.mock_vector_db_delete_collection.assert_has_calls([call(f"file-{self.mock_file.id}")])

        self.mock_db_delete_file_by_id.assert_has_calls([call(mock_file_id)])

    @pytest.mark.asyncio
    async def test_delete_file_by_id__delete_fails_in_storage(self, monkeypatch, mock_user):
        self.setup_mocks_for_delete_tests(monkeypatch, mock_user)

        mock_file_id = "mock-file-id"

        self.mock_storage_delete_file.side_effect = Exception('unknown error')

        with pytest.raises(Exception, match="Error deleting files"):
            await delete_file_by_id(mock_file_id, self.mock_user)

        self.mock_storage_delete_file.assert_has_calls([call(self.mock_file.path)])

        self.mock_vector_db_delete_collection.assert_not_called()

        self.mock_db_delete_file_by_id.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_file_by_id__delete_fails_in_vector_db(self, monkeypatch, mock_user):
        self.setup_mocks_for_delete_tests(monkeypatch, mock_user)

        mock_file_id = "mock-file-id"

        self.mock_vector_db_delete_collection.side_effect = Exception('unknown error')

        with pytest.raises(Exception, match="Error deleting files"):
            await delete_file_by_id(mock_file_id, self.mock_user)

        self.mock_storage_delete_file.assert_has_calls([call(self.mock_file.path)])

        self.mock_vector_db_delete_collection.assert_has_calls([call(f"file-{self.mock_file.id}")])

        self.mock_db_delete_file_by_id.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_file_by_id__fails_in_db(self, monkeypatch, mock_user):
        self.setup_mocks_for_delete_tests(monkeypatch, mock_user)

        mock_file_id = "mock-file-id"

        self.mock_db_delete_file_by_id.side_effect = Exception('unknown error')

        with pytest.raises(HTTPException, match="Error deleting files"):
            await delete_file_by_id(mock_file_id, self.mock_user)

        self.mock_storage_delete_file.assert_has_calls([call(self.mock_file.path)])

        self.mock_vector_db_delete_collection.assert_has_calls([call(f"file-{self.mock_file.id}")])

        self.mock_db_delete_file_by_id.assert_has_calls([call(mock_file_id)])
