# Supabase V26

`supabase/migrations/202609220001_v25_baseline.sql` mirrors the PostgreSQL baseline used by the backend Alembic migration.

For a fresh Supabase project:

```bash
supabase login
supabase link --project-ref <PROJECT_REF>
supabase db push
```

For an existing database, compare the live schema first. Do not blindly replay a baseline migration against an already populated V25 database.
