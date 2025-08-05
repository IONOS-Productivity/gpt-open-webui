import os
import shutil
import json
import logging
from abc import ABC, abstractmethod
from typing import BinaryIO, Tuple

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from open_webui.config import (
    S3_ACCESS_KEY_ID,
    S3_BUCKET_NAME,
    S3_ENDPOINT_URL,
    S3_KEY_PREFIX,
    S3_REGION_NAME,
    S3_SECRET_ACCESS_KEY,
    S3_USE_ACCELERATE_ENDPOINT,
    S3_ADDRESSING_STYLE,
    GCS_BUCKET_NAME,
    GOOGLE_APPLICATION_CREDENTIALS_JSON,
    AZURE_STORAGE_ENDPOINT,
    AZURE_STORAGE_CONTAINER_NAME,
    AZURE_STORAGE_KEY,
    STORAGE_PROVIDER,
    UPLOAD_DIR,
)
from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError, NotFound
from open_webui.constants import ERROR_MESSAGES
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError
from open_webui.env import SRC_LOG_LEVELS


log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MAIN"])

# --- Custom Exception Classes ---

class StorageError(Exception):
    """Base class for storage-related errors."""
    pass

class FileNotFoundError(StorageError):
    """Raised when a file is not found in the storage."""
    pass

class FileUploadError(StorageError):
    """Raised when a file upload fails."""
    pass

class FileDeletionError(StorageError):
    """Raised when a file deletion fails."""
    pass

class ConfigurationError(StorageError):
    """Raised for configuration-related issues."""
    pass

class StorageProvider(ABC):
    @abstractmethod
    def get_file(self, file_path: str) -> BinaryIO:
        pass

    @abstractmethod
    def upload_file(self, file: BinaryIO, filename: str) -> Tuple[int, str]:
        pass

    @abstractmethod
    def delete_all_files(self) -> None:
        pass

    @abstractmethod
    def delete_file(self, file_path: str) -> None:
        pass


class LocalStorageProvider(StorageProvider):

    def upload_file(self, file: BinaryIO, filename: str) -> Tuple[int, str]:
        """
        Saves a binary stream to the local filesystem.

        Args:
            file: The binary file stream to save.
            filename: The name of the file to save.

        Returns:
            A tuple containing the file size in bytes and the full file path.
        """
        try:
            file.seek(0, os.SEEK_END)
            size = file.tell()
            file.seek(0)
            if size == 0:
                raise FileUploadError("Cannot upload an empty file.")
            if ".." in filename or filename.startswith("/"):
                raise ValueError("Invalid filename.")
            file_path = os.path.join(UPLOAD_DIR, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as f:
                shutil.copyfileobj(file, f)
            return size, file_path

        except (IOError, OSError) as e:
            raise FileUploadError(f"Error saving file to local storage: {e}") from e

    def get_file(self, file_path: str) -> BinaryIO:
        """
        Retrieves a file from local storage as a binary stream.

        Args:
            file_path: The absolute path to the file.

        Returns:
            A binary stream (BinaryIO) of the file.
        """
        try:
            if not os.path.abspath(file_path).startswith(os.path.abspath(UPLOAD_DIR)):
                 raise FileNotFoundError(f"Access denied to file path: {file_path}")
            return open(file_path, "rb")
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found at path: {file_path}")
        except (IOError, OSError) as e:
            raise StorageError(f"Error reading file from local storage: {e}") from e


    def delete_file(self, file_path: str) -> None:
        """Handles deletion of the file from local storage."""
        filename = file_path.split("/")[-1]
        file_path = f"{UPLOAD_DIR}/{filename}"
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            log.warning(f"File {file_path} not found in local storage.")

    def delete_all_files(self) -> None:
        """Handles deletion of all files from local storage."""
        if os.path.exists(UPLOAD_DIR):
            for filename in os.listdir(UPLOAD_DIR):
                file_path = os.path.join(UPLOAD_DIR, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  # Remove the file or link
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # Remove the directory
                except Exception as e:
                    log.exception(f"Failed to delete {file_path}. Reason: {e}")
        else:
            log.warning(f"Directory {UPLOAD_DIR} not found in local storage.")


class S3StorageProvider(StorageProvider):
    def __init__(self):
        config = Config(
            s3={
                "use_accelerate_endpoint": S3_USE_ACCELERATE_ENDPOINT,
                "addressing_style": S3_ADDRESSING_STYLE,
            },
        )

        # If access key and secret are provided, use them for authentication
        if S3_ACCESS_KEY_ID and S3_SECRET_ACCESS_KEY:
            self.s3_client = boto3.client(
                "s3",
                region_name=S3_REGION_NAME,
                endpoint_url=S3_ENDPOINT_URL,
                aws_access_key_id=S3_ACCESS_KEY_ID,
                aws_secret_access_key=S3_SECRET_ACCESS_KEY,
                config=config,
            )
        else:
            # If no explicit credentials are provided, fall back to default AWS credentials
            # This supports workload identity (IAM roles for EC2, EKS, etc.)
            self.s3_client = boto3.client(
                "s3",
                region_name=S3_REGION_NAME,
                endpoint_url=S3_ENDPOINT_URL,
                config=config,
            )

        self.bucket_name = S3_BUCKET_NAME
        self.key_prefix = S3_KEY_PREFIX if S3_KEY_PREFIX else ""

    def upload_file(self, file: BinaryIO, filename: str) -> Tuple[int, str]:
        try:
            file.seek(0, os.SEEK_END)
            size = file.tell()
            file.seek(0)
            if size == 0:
                raise FileUploadError(ERROR_MESSAGES.EMPTY_CONTENT)

            s3_key = os.path.join(self.key_prefix, filename)
            self.s3_client.upload_fileobj(file, self.bucket_name, s3_key)
            return (size, f"s3://{self.bucket_name}/{filename}")
        except ClientError as e:
            raise FileUploadError(f"Error uploading file to S3: {e}") from e

    def get_file(self, file_path: str) -> BinaryIO:
        """Handles downloading of the file from S3 storage."""
        try:
            s3_key = self._extract_s3_key(file_path)
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=s3_key)
            return response['Body']
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                raise FileNotFoundError(f"File not found in S3: {file_path}") from e
            raise StorageError(f"Error downloading file from S3: {e}") from e
        except (IndexError, ValueError):
            raise ValueError(f"Invalid S3 path format: {file_path}")

    def delete_file(self, file_path: str) -> None:
        """Handles deletion of the file from S3 storage."""
        s3_key = self._extract_s3_key(file_path)
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
        except ClientError as e:
            raise FileDeletionError(f"Error deleting file from S3: {e}") from e


    def delete_all_files(self) -> None:
        """
        Deletes all files from the S3 bucket efficiently using batch operations.

        Raises:
            FileDeletionError: If the deletion process fails.
        """
        try:
            paginator = self.s3_client.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=self.bucket_name)

            objects_to_delete = []
            for page in pages:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        objects_to_delete.append({'Key': obj['Key']})

                        # S3 delete_objects has a limit of 1000 keys per request
                        if len(objects_to_delete) == 1000:
                            self.s3_client.delete_objects(
                                Bucket=self.bucket_name,
                                Delete={'Objects': objects_to_delete}
                            )
                            objects_to_delete = []

            # Delete any remaining objects
            if objects_to_delete:
                self.s3_client.delete_objects(
                    Bucket=self.bucket_name,
                    Delete={'Objects': objects_to_delete}
                )

        except ClientError as e:
            raise FileDeletionError(f"Error deleting all files from S3: {e}") from e


    # The s3 key is the name assigned to an object. It excludes the bucket name, but includes the internal path and the file name.
    def _extract_s3_key(self, full_file_path: str) -> str:
        return "/".join(full_file_path.split("//")[1].split("/")[1:])


class GCSStorageProvider(StorageProvider):
    def __init__(self):
        self.bucket_name = GCS_BUCKET_NAME

        if GOOGLE_APPLICATION_CREDENTIALS_JSON:
            self.gcs_client = storage.Client.from_service_account_info(
                info=json.loads(GOOGLE_APPLICATION_CREDENTIALS_JSON)
            )
        else:
            # if no credentials json is provided, credentials will be picked up from the environment
            # if running on local environment, credentials would be user credentials
            # if running on a Compute Engine instance, credentials would be from Google Metadata server
            self.gcs_client = storage.Client()
        self.bucket = self.gcs_client.bucket(GCS_BUCKET_NAME)

    def upload_file(self, file: BinaryIO, filename: str) -> Tuple[int, str]:
        """Handles uploading of a file stream to GCS storage.

        Args:
            file: The binary file stream to upload.
            filename: The destination object name in the GCS bucket.

        Returns:
            A tuple containing the file size in bytes and the GCS URI.

        Raises:
            FileUploadError: If the file stream is empty or a cloud error occurs.
        """
        try:
            # Get the size of the stream by seeking to the end, and then rewind
            file.seek(0, os.SEEK_END)
            size = file.tell()
            file.seek(0)
            if size == 0:
                raise FileUploadError(ERROR_MESSAGES.EMPTY_CONTENT)
            blob = self.bucket.blob(filename)
            # Use upload_from_file to upload the stream directly
            blob.upload_from_file(file)
            # Return the size and the GCS URI
            return size, f"gs://{self.bucket_name}/{filename}"
        except GoogleCloudError as e:
            raise FileUploadError(f"Error uploading file to GCS: {e}") from e

    def get_file(self, file_path: str) -> BinaryIO:
        """
        Downloads a file from GCS storage as an in-memory binary stream.

        Args:
            file_path: The full GCS URI of the file (e.g., 'gs://bucket/file.txt').

        Returns:
            An in-memory binary stream (io.BytesIO) of the file's content.

        Raises:
            FileNotFoundError: If the file does not exist in GCS.
            StorageError: For other download-related failures.
        """
        try:
            # Robustly parse the blob name from the full GCS URI
            prefix = f"gs://{self.bucket_name}/"
            if not file_path.startswith(prefix):
                raise ValueError(f"Invalid GCS URI format. Must start with '{prefix}'.")
            blob_name = file_path.removeprefix(prefix)
            blob = self.bucket.blob(blob_name)
            file_bytes = blob.download_as_bytes()
            return io.BytesIO(file_bytes)
        except NotFound:
            raise FileNotFoundError(f"File not found at GCS path: {file_path}")
        except Exception as e:
            raise StorageError(f"Failed to get file from GCS: {e}") from e

    def delete_file(self, file_path: str) -> None:
        """Handles deletion of the file from GCS storage."""
        try:
            filename = file_path.removeprefix("gs://").split("/")[1]
            blob = self.bucket.get_blob(filename)
            blob.delete()
        except NotFound as e:
            raise RuntimeError(f"Error deleting file from GCS: {e}")

    def delete_all_files(self) -> None:
        """Handles deletion of all files from GCS storage."""
        try:
            blobs = self.bucket.list_blobs()

            for blob in blobs:
                blob.delete()

        except NotFound as e:
            raise RuntimeError(f"Error deleting all files from GCS: {e}")


class AzureStorageProvider(StorageProvider):
    def __init__(self):
        self.endpoint = AZURE_STORAGE_ENDPOINT
        self.container_name = AZURE_STORAGE_CONTAINER_NAME
        storage_key = AZURE_STORAGE_KEY

        if storage_key:
            # Configure using the Azure Storage Account Endpoint and Key
            self.blob_service_client = BlobServiceClient(
                account_url=self.endpoint, credential=storage_key
            )
        else:
            # Configure using the Azure Storage Account Endpoint and DefaultAzureCredential
            # If the key is not configured, then the DefaultAzureCredential will be used to support Managed Identity authentication
            self.blob_service_client = BlobServiceClient(
                account_url=self.endpoint, credential=DefaultAzureCredential()
            )
        self.container_client = self.blob_service_client.get_container_client(
            self.container_name
        )

    def upload_file(self, file: BinaryIO, filename: str) -> Tuple[int, str]:
        """
        Handles uploading of a file stream to Azure Blob Storage.

        Args:
            file: The binary file stream to upload.
            filename: The destination blob name in the container.

        Returns:
            A tuple containing the file size in bytes and the blob URL.
        """
        try:
            # Get the size of the stream and then rewind it
            file.seek(0, os.SEEK_END)
            size = file.tell()
            file.seek(0)
            if size == 0:
                raise FileUploadError("Cannot upload an empty file.")
            blob_client = self.container_client.get_blob_client(filename)
            # Upload the stream directly, overwriting if the blob exists
            blob_client.upload_blob(file, overwrite=True)
            return size, f"{self.endpoint}/{self.container_name}/{filename}"
        except AzureError as e:
            raise FileUploadError(f"Error uploading file to Azure: {e}") from e

    def get_file(self, file_path: str) -> BinaryIO:
        """
        Downloads a file from Azure Blob Storage as an in-memory binary stream.

        Args:
            file_path: The full URL of the blob.

        Returns:
            An in-memory binary stream (io.BytesIO) of the file's content.
        """
        try:
            filename = file_path.split("/")[-1]
            blob_client = self.container_client.get_blob_client(filename)
            downloader = blob_client.download_blob()
            file_bytes = downloader.readall()
            return io.BytesIO(file_bytes)
        except ResourceNotFoundError:
            raise FileNotFoundError(f"File not found at Azure path: {filename}")
        except AzureError as e:
            raise StorageError(f"Failed to get file from Azure: {e}") from e

    def delete_file(self, file_path: str) -> None:
        """Handles deletion of the file from Azure Blob Storage."""
        try:
            filename = file_path.split("/")[-1]
            blob_client = self.container_client.get_blob_client(filename)
            blob_client.delete_blob()
        except ResourceNotFoundError as e:
            raise RuntimeError(f"Error deleting file from Azure Blob Storage: {e}")

    def delete_all_files(self) -> None:
        """Handles deletion of all files from Azure Blob Storage."""
        try:
            blobs = self.container_client.list_blobs()
            for blob in blobs:
                self.container_client.delete_blob(blob.name)
        except Exception as e:
            raise RuntimeError(f"Error deleting all files from Azure Blob Storage: {e}")


def get_storage_provider(storage_provider: str):
    if storage_provider == "local":
        Storage = LocalStorageProvider()
    elif storage_provider == "s3":
        Storage = S3StorageProvider()
    elif storage_provider == "gcs":
        Storage = GCSStorageProvider()
    elif storage_provider == "azure":
        Storage = AzureStorageProvider()
    else:
        raise RuntimeError(f"Unsupported storage provider: {storage_provider}")
    return Storage


Storage = get_storage_provider(STORAGE_PROVIDER)
