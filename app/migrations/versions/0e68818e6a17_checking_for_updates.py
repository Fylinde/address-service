"""checking for updates

Revision ID: 0e68818e6a17
Revises: ed33bee8e8c0
Create Date: 2024-10-17 08:51:13.438100

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "0e68818e6a17"
down_revision: Union[str, None] = "ed33bee8e8c0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the foreign key constraints
    op.drop_constraint("addresses_user_id_fkey", "addresses", type_="foreignkey")
    op.drop_constraint(
        "address_history_user_id_fkey", "address_history", type_="foreignkey"
    )

    # Drop indexes on the users table before dropping the table
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_id", table_name="users")

    # Drop the users table
    op.drop_table("users")

    # Alterations to the addresses table
    op.add_column(
        "addresses", sa.Column("first_name", sa.String(length=256), nullable=True)
    )
    op.add_column(
        "addresses", sa.Column("last_name", sa.String(length=256), nullable=True)
    )
    op.add_column(
        "addresses", sa.Column("company_name", sa.String(length=256), nullable=True)
    )
    op.add_column(
        "addresses", sa.Column("street_address_1", sa.String(length=256), nullable=True)
    )
    op.add_column(
        "addresses", sa.Column("street_address_2", sa.String(length=256), nullable=True)
    )
    op.add_column(
        "addresses", sa.Column("city_area", sa.String(length=128), nullable=True)
    )
    op.add_column(
        "addresses", sa.Column("country_area", sa.String(length=128), nullable=True)
    )
    op.add_column(
        "addresses", sa.Column("validation_skipped", sa.Boolean(), nullable=True)
    )
    op.add_column("addresses", sa.Column("vendor_id", sa.Integer(), nullable=True))
    op.add_column("addresses", sa.Column("geolocation", sa.String(), nullable=True))
    op.alter_column("addresses", "city", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column(
        "addresses", "postal_code", existing_type=sa.VARCHAR(), nullable=True
    )
    op.drop_column("addresses", "street")
    # Other column modifications as needed...


def downgrade() -> None:
    # Add back the users table
    op.create_table(
        "users",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("hashed_password", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            "first_name", sa.VARCHAR(length=128), autoincrement=False, nullable=True
        ),
        sa.Column(
            "last_name", sa.VARCHAR(length=128), autoincrement=False, nullable=True
        ),
        sa.Column(
            "phone_number", sa.VARCHAR(length=20), autoincrement=False, nullable=True
        ),
        sa.Column("profile_picture", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("date_of_birth", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("gender", sa.VARCHAR(length=10), autoincrement=False, nullable=True),
        sa.Column(
            "preferences",
            postgresql.JSON(astext_type=sa.Text()),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "notification_preferences", sa.VARCHAR(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "language_code",
            sa.VARCHAR(length=35),
            server_default=sa.text("'en'::character varying"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "is_active",
            sa.BOOLEAN(),
            server_default=sa.text("true"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "is_admin",
            sa.BOOLEAN(),
            server_default=sa.text("false"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "is_email_verified",
            sa.BOOLEAN(),
            server_default=sa.text("false"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "is_phone_verified",
            sa.BOOLEAN(),
            server_default=sa.text("false"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "two_factor_enabled",
            sa.BOOLEAN(),
            server_default=sa.text("false"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "two_factor_secret", sa.VARCHAR(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "subscription_status", sa.VARCHAR(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "full_name", sa.VARCHAR(length=255), autoincrement=False, nullable=False
        ),
        sa.Column(
            "middle_name", sa.VARCHAR(length=128), autoincrement=False, nullable=True
        ),
        sa.PrimaryKeyConstraint("id", name="users_pkey"),
        sa.UniqueConstraint("phone_number", name="users_phone_number_key"),
    )
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    # Recreate the foreign key constraints
    op.create_foreign_key(
        "addresses_user_id_fkey", "addresses", "users", ["user_id"], ["id"]
    )
    op.create_foreign_key(
        "address_history_user_id_fkey", "address_history", "users", ["user_id"], ["id"]
    )
