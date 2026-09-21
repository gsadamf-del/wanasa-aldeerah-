# V26 Deployment

1. Push the repository to GitHub.
2. Configure the required GitHub Actions secrets.
3. Create a managed PostgreSQL database (Supabase is supported by the migration mirror).
4. Set `DATABASE_URL` and backend secrets in Render.
5. Deploy the Render Blueprint. Its pre-deploy command runs `alembic upgrade head`.
6. Verify `/api/v25/health` and `/api/v25/readiness`.
7. Push tag `v26.0.0` to build Android AAB, iOS IPA, Windows installer and Web.
8. Download the artifacts from the GitHub Actions run.

Do not commit certificates, provisioning profiles, keystores, `.env`, payment keys, Firebase private credentials or monitoring credentials.
