# Wanasa V25 PostgreSQL migration

The file `0001_v25_baseline.sql` is the V25 baseline generated from the SQLAlchemy models loaded by the application (34 tables). Alembic revision `202609220001` executes this baseline.

## Fresh database

Use:

```bash
alembic upgrade head
```

## Existing V25 database

If the database already contains the same V25 schema created outside Alembic, **do not run the baseline blindly**. First compare the schema with `0001_v25_baseline.sql`, take a backup, and then use:

```bash
alembic stamp 202609220001
```

only after the schema has been verified equivalent. If the existing schema differs, create a data-preserving upgrade migration instead.
