import pytest
from unittest.mock import MagicMock, call

import uuid
import time
from fastapi import HTTPException

from open_webui.models.knowledge import (
    Knowledge,
    Knowledges,
)
from open_webui.models.users import (
    UserModel,
)
from open_webui.routers.knowledge import (
    delete_knowledge_by_id,
)

class GetFileByIdMock(MagicMock):
    """
    Mock of Files.get_file_by_id()
    """
    def __call__(self, id):
        mock_file = MagicMock()
        mock_file.path = f"/mock/file/path/{id}"
        return mock_file

class KnowledgeDataGetterMock(MagicMock):
    """
    Mock of Knowledge.data's get() method
    """
    def __call__(self, property_name, default):
        if property_name == "file_ids":
            return self.file_ids

class TestIntegrationKnowledge:
    @pytest.fixture
    def mock_user(self):
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = "email@example.com"
        mock_user.name = "John Doe"
        mock_user.role = "admin"
        mock_user.created_at = "2022-01-01"
        mock_user.profile_image_url = "https://example.com/image.jpg"
        return mock_user

    @pytest.fixture
    def mock_knowledge(self):
        mock_knowledge = MagicMock()
        mock_knowledge.id = str(uuid.uuid4())
        mock_knowledge.user_id = str(uuid.uuid4())
        mock_knowledge.updated_at = int(time.time())
        mock_knowledge.created_at = int(time.time())
        mock_knowledge.name = "some name"
        mock_knowledge.description = "some description"
        return mock_knowledge

    def setup_mocks_for_delete_tests(self, monkeypatch, mock_user, mock_knowledge, file_ids):
        self.mock_user = mock_user
        self.mock_knowledge = mock_knowledge

        # Mocked to reduce test complexity
        self.mock_has_access = MagicMock(return_value=None)
        monkeypatch.setattr("open_webui.utils.access_control.has_access", self.mock_has_access)

        self.mock_knowledge.user_id = mock_user.id
        self.mock_get_knowledge_by_id = MagicMock(return_value=mock_knowledge)
        monkeypatch.setattr("open_webui.models.knowledge.Knowledges.get_knowledge_by_id", self.mock_get_knowledge_by_id)

        self.mock_knowledge.data = MagicMock()
        self.mock_knowledge.data.get = KnowledgeDataGetterMock(file_ids=file_ids)

        self.mock_files_get_file_by_id = GetFileByIdMock()
        monkeypatch.setattr("open_webui.models.files.Files.get_file_by_id", self.mock_files_get_file_by_id)

        self.mock_delete_file = MagicMock()
        monkeypatch.setattr("open_webui.storage.provider.Storage.delete_file", self.mock_delete_file)

        self.mock_has_collection = MagicMock()
        monkeypatch.setattr("open_webui.retrieval.vector.connector.VECTOR_DB_CLIENT.has_collection", self.mock_has_collection)

        self.mock_delete_collection = MagicMock()
        monkeypatch.setattr("open_webui.retrieval.vector.connector.VECTOR_DB_CLIENT.delete_collection", self.mock_delete_collection)

        self.mock_delete_file_by_id = MagicMock(return_value=True)
        monkeypatch.setattr("open_webui.models.files.Files.delete_file_by_id", self.mock_delete_file_by_id)

        # No models for this test to reduce test complexity
        self.mock_delete_get_all_models = MagicMock(return_value=[])
        monkeypatch.setattr("open_webui.models.models.Models.get_all_models", self.mock_delete_get_all_models)

        self.mock_delete_knowledge_by_id = MagicMock(return_value=True)
        monkeypatch.setattr("open_webui.models.knowledge.Knowledges.delete_knowledge_by_id", self.mock_delete_knowledge_by_id)


    @pytest.mark.asyncio
    async def test_delete_knowledge_by_id__delete_ok(self, monkeypatch, mock_user, mock_knowledge):
        file_ids = [
            str(uuid.uuid4()),
            str(uuid.uuid4()),
        ]

        self.setup_mocks_for_delete_tests(monkeypatch, mock_user, mock_knowledge, file_ids)

        mock_collection_id = "foo-knowledge-id"

        await delete_knowledge_by_id(mock_collection_id, self.mock_user)

        self.mock_delete_collection.assert_has_calls([
            call(collection_name=f"file-{file_ids[0]}"),
            call(collection_name=f"file-{file_ids[1]}"),
            call(collection_name=mock_collection_id),
        ])

        self.mock_delete_file_by_id.assert_has_calls([
            call(file_ids[0]),
            call(file_ids[1]),
        ])

        self.mock_delete_knowledge_by_id.assert_has_calls([
            call(id=mock_collection_id)
        ])

        self.mock_delete_file.assert_has_calls([
            call(f"/mock/file/path/{file_ids[0]}"),
            call(f"/mock/file/path/{file_ids[1]}"),
        ])


    @pytest.mark.asyncio
    async def test_delete_knowledge_by_id__delete_vector_failed(self, monkeypatch, mock_user, mock_knowledge):
        file_ids = [
            str(uuid.uuid4()),
            str(uuid.uuid4()),
        ]

        self.setup_mocks_for_delete_tests(monkeypatch, mock_user, mock_knowledge, file_ids)

        mock_collection_id = "foo-knowledge-id"

        def delete_collection_side_effect(id):
            if id == file_ids[0]:
                raise Exception('can not delete collection')

        self.mock_delete_collection.side_effect = delete_collection_side_effect

        with pytest.raises(Exception, match="Error deleting files"):
            await delete_knowledge_by_id(mock_collection_id, self.mock_user)

        # First file's collection delete will fail
        self.mock_delete_collection.assert_has_calls([
            call(collection_name=f"file-{file_ids[0]}"),
        ])

        self.mock_delete_file_by_id.assert_not_called()

        self.mock_delete_knowledge_by_id.assert_not_called()

        self.mock_delete_file.assert_not_called()


    @pytest.mark.asyncio
    async def test_delete_knowledge_by_id__delete_collection_vector_failed(self, monkeypatch, mock_user, mock_knowledge):
        file_ids = [
            str(uuid.uuid4()),
            str(uuid.uuid4()),
        ]

        self.setup_mocks_for_delete_tests(monkeypatch, mock_user, mock_knowledge, file_ids)

        mock_collection_id = "foo-knowledge-id"

        def delete_collection_side_effect(collection_name = None):
            if collection_name == mock_collection_id:
                raise Exception('can not delete collection')

        self.mock_delete_collection.side_effect = delete_collection_side_effect

        await delete_knowledge_by_id(mock_collection_id, self.mock_user)

        self.mock_delete_collection.assert_has_calls([
            call(collection_name=f"file-{file_ids[0]}"),
            call(collection_name=f"file-{file_ids[1]}"),
            call(collection_name=mock_collection_id),
        ])

        self.mock_delete_file_by_id.assert_has_calls([
            call(file_ids[0]),
            call(file_ids[1]),
        ])

        self.mock_delete_knowledge_by_id.assert_has_calls([
            call(id=mock_collection_id)
        ])

        self.mock_delete_file.assert_has_calls([
            call(f"/mock/file/path/{file_ids[0]}"),
            call(f"/mock/file/path/{file_ids[1]}"),
        ])



    @pytest.mark.asyncio
    async def test_delete_knowledge_by_id__file_deletion_failed(self, monkeypatch, mock_user, mock_knowledge):
        file_ids = [
            str(uuid.uuid4()),
            str(uuid.uuid4()),
        ]

        self.setup_mocks_for_delete_tests(monkeypatch, mock_user, mock_knowledge, file_ids)

        mock_collection_id = "foo-knowledge-id"

        def delete_file_side_effect(path):
            if path == f"/mock/file/path/{file_ids[0]}":
                raise Exception("can not delete file")

        self.mock_delete_file.side_effect = delete_file_side_effect

        with pytest.raises(Exception, match="Error deleting files"):
            await delete_knowledge_by_id(mock_collection_id, self.mock_user)

        # First file's storage delete failed, second can not happen
        self.mock_delete_collection.assert_has_calls([
            call(collection_name=f"file-{file_ids[0]}"),
        ])

        # First file's collection delete will fail
        self.mock_delete_file.assert_has_calls([
            call(f"/mock/file/path/{file_ids[0]}"),
        ])

        self.mock_delete_knowledge_by_id.assert_not_called()


    @pytest.mark.asyncio
    async def test_delete_knowledge_by_id__file_deletion_failed(self, monkeypatch, mock_user, mock_knowledge):
        file_ids = [
            str(uuid.uuid4()),
            str(uuid.uuid4()),
        ]

        self.setup_mocks_for_delete_tests(monkeypatch, mock_user, mock_knowledge, file_ids)

        mock_collection_id = "foo-knowledge-id"

        self.mock_delete_knowledge_by_id.side_effect = lambda id: False

        assert await delete_knowledge_by_id(mock_collection_id, self.mock_user) == False

        # First file's storage delete failed, second can not happen
        self.mock_delete_collection.assert_has_calls([
            call(collection_name=f"file-{file_ids[0]}"),
        ])

        # First file's collection delete will fail
        self.mock_delete_file.assert_has_calls([
            call(f"/mock/file/path/{file_ids[0]}"),
        ])
