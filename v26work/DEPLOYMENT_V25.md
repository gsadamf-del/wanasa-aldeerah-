# وناسة الديرة V25 — نشر GitHub + Cloud + Build

## Architecture
- GitHub: source + CI/CD + build artifacts.
- Render Free: FastAPI API demo endpoint.
- Supabase Free (recommended for demo): PostgreSQL database.
- Flutter: Android APK/AAB, iOS Runner/IPA (signed only with Apple credentials), Windows EXE, Web.
- Secrets: GitHub Actions Secrets and Render Environment Variables only.

## Important V25 release audit
The supplied V25 archive contains the production gate and PostgreSQL driver, but it does **not** contain a complete Alembic migration history. Do not claim the production database is migrated until an initial migration has been generated and executed successfully against the target PostgreSQL database.

The included Render blueprint intentionally does not create a free Render Postgres database because Render documents that its free Postgres databases expire after 30 days and have no backups. Use Supabase Free for a longer-lived demo database, or use paid managed Postgres for production.

## GitHub repository
1. Create a repository named `wanasa-aldeerah`.
2. For zero-cost public CI, a public repository gets standard GitHub-hosted runners without charge.
3. Upload/extract this release and push the contents.
4. Never commit real payment, Firebase, APNs, JWT, or database credentials.

## Required GitHub Actions secrets
`API_BASE_URL` — public HTTPS URL of the API.

Optional release/signing secrets can be added later:
- Android keystore/signing variables.
- Apple App Store Connect API key and signing certificate/provisioning profile.
- `WINDOWS_SIGNING_CERT` and `WINDOWS_SIGNING_PASSWORD` if Windows code signing is later enabled.

## Build outputs
- Android: `wanasa-v25-android-apk` artifact.
- Android bundle: add a signed AAB step after Play signing is configured.
- iOS: `wanasa-v25-ios-runner` is an unsigned device build; a distributable IPA requires Apple signing.
- Windows: `wanasa-v25-windows` contains the Flutter Windows release directory including the executable.
- Web: `wanasa-v25-web` contains the static Flutter web site.

## Cloud API
Render creates a public `onrender.com` URL. Set:
- `DATABASE_URL` to the Supabase/Postgres connection string.
- `CORS_ORIGINS` to the exact web/app origins.
- payment/push/monitoring secrets only after the corresponding provider accounts are configured.

## Database
Before setting `ENVIRONMENT=production`, create and test the V25 PostgreSQL migration. The application deliberately refuses an unvalidated production configuration and does not call `Base.metadata.create_all()` in production.

## Restore testing
Keep a scheduled backup/restore drill outside the production instance. Render Free Postgres has no backups, so it is unsuitable as the only production datastore.

## Release sequence
1. Push code to GitHub.
2. Run `Backend Tests`.
3. Create/validate PostgreSQL migration.
4. Create Supabase project and database.
5. Deploy API to Render.
6. Set `API_BASE_URL` in GitHub.
7. Run `Build All Platforms`.
8. Download artifacts and test.
9. Add real payment/push credentials.
10. Configure signed Android/iOS releases.
11. Add monitoring and backup/restore verification.
