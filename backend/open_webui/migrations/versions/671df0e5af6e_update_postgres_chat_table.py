"""Update postgres chat table

Revision ID: 671df0e5af6e
Revises: 3781e22d8b01
Create Date: 2025-08-29 10:01:31.009079

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, select, update
import json

revision = "671df0e5af6e"
down_revision = "3781e22d8b01"
branch_labels = None
depends_on = None


def upgrade():
    """
    Upgrades the 'chat' column from JSON to JSONB if the database is PostgreSQL.
    """
    # Get the underlying connection to check the dialect
    conn = op.get_bind()

    # This migration is only for PostgreSQL
    if conn.dialect.name != "postgresql":
        print("Skipping migration: Not a PostgreSQL database.")
        return

    from sqlalchemy.dialects.postgresql import JSONB
    # Inspect the database to check the current column type
    inspector = sa.inspect(conn)
    columns = inspector.get_columns("chat")
    column_info = next((c for c in columns if c["name"] == "chat"), None)

    if not column_info:
        print("Skipping migration: Column 'chat' not found in table 'chat'.")
        return

    # Check if the column type is JSON before altering.
    # The type from the inspector for 'json' is JSON, not a specific dialect class.
    # We can check the string representation to be sure.
    if str(column_info["type"]).upper() == "JSON":
        print("Altering 'chat.chat' column from JSON to JSONB.")
        op.alter_column(
            "chat",
            "chat",
            existing_type=sa.JSON(),
            type_=JSONB,
            postgresql_using="chat::jsonb",  # Required for casting data
        )
    else:
        print(
            f"Skipping migration: 'chat.chat' column is not of type JSON. "
            f"(Current type: {column_info['type']})"
        )

def downgrade():
    """
    Downgrades the 'chat' column from JSONB back to JSON if the database is PostgreSQL.
    """
    # Get the underlying connection to check the dialect
    conn = op.get_bind()

    # This migration is only for PostgreSQL
    if conn.dialect.name != "postgresql":
        print("Skipping downgrade: Not a PostgreSQL database.")
        return

    from sqlalchemy.dialects.postgresql import JSONB
    # Inspect the database to check the current column type
    inspector = sa.inspect(conn)
    columns = inspector.get_columns("chat")
    column_info = next((c for c in columns if c["name"] == "chat"), None)

    if not column_info:
        print("Skipping downgrade: Column 'chat' not found in table 'chat'.")
        return

    # Check if the column type is JSONB before altering it back.
    if isinstance(column_info["type"], JSONB):
        print("Altering 'chat.chat' column from JSONB to JSON.")
        op.alter_column(
            "chat",
            "chat",
            existing_type=postgresql.JSONB,
            type_=sa.JSON(),
            postgresql_using="chat::json",  # Required for casting data
        )
    else:
        print(
            f"Skipping downgrade: 'chat.chat' column is not of type JSONB. "
            f"(Current type: {column_info['type']})"
        )