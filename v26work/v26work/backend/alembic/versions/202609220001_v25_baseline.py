"""V25 PostgreSQL baseline schema"""
from pathlib import Path
from alembic import op
revision="202609220001"
down_revision=None
branch_labels=None
depends_on=None
def upgrade():
 sql=(Path(__file__).resolve().parents[2]/"migrations"/"0001_v25_baseline.sql").read_text(encoding="utf-8")
 for statement in sql.split(";"):
  if statement.strip(): op.execute(statement)
def downgrade():
 raise RuntimeError("V25 baseline downgrade is disabled; restore a known-good backup.")
