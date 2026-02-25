-- sql/migrations/001_initial_schema.sql
-- SQL Server migration script
-- Run order is determined by the numeric prefix (001, 002, ...)
-- These are applied manually or via a migration tool (e.g. Flyway, Liquibase)

-- ── Create staging schema ──────────────────────────────────────────────────
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'staging')
BEGIN
    EXEC('CREATE SCHEMA staging')
END
GO

-- ── Create raw landing table ───────────────────────────────────────────────
IF NOT EXISTS (
    SELECT 1 FROM sys.tables t
    JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE s.name = 'staging' AND t.name = 'example_raw'
)
BEGIN
    CREATE TABLE staging.example_raw (
        id              BIGINT IDENTITY(1,1) PRIMARY KEY,
        source_system   NVARCHAR(100)   NOT NULL,
        raw_payload     NVARCHAR(MAX),
        ingested_at     DATETIME2       DEFAULT GETUTCDATE(),
        environment     NVARCHAR(20)    NOT NULL
    )
END
GO
