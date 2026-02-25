# de1-code-migration

Holds all ETL scripts, Lambda functions, and SQL migrations for the DE1 data engineering project.

## Branch Flow

```
feature/* → dev → qa → prod
```

Always branch off `dev`. Never commit directly to `dev`, `qa`, or `prod`.

## Folder Structure

```
de1-code-migration/
├── glue/jobs/              # AWS Glue PySpark ETL scripts
├── lambda/functions/       # Lambda functions (one folder per function)
├── sql/migrations/         # SQL Server migration scripts (numbered in order)
├── tests/                  # Unit tests (pytest)
└── .github/workflows/
    ├── validate.yml        # Runs on PRs → lint + tests
    └── deploy.yml          # Runs on merge to prod → S3 sync (with approval)
```

## Adding a New Glue Job

1. Create `glue/jobs/your_job_name.py`
2. Add the matching Glue Job resource in `de1-infrastructure/terraform/modules/glue/main.tf`
3. Feature branch → PR to dev → qa → prod

On prod merge, the script is automatically synced to:
```
s3://de1-prod-glue-scripts/jobs/your_job_name.py
```

## Adding a New Lambda Function

1. Create `lambda/functions/your_function_name/handler.py`
2. Add the matching Lambda resource in `de1-infrastructure/terraform/modules/lambda/main.tf`
3. Feature branch → PR to dev → qa → prod

On prod merge, the function is zipped and synced to:
```
s3://de1-prod-lambda-packages/functions/your_function_name.zip
```

## Running Tests Locally

```bash
pip install pytest boto3 flake8
pytest tests/ -v
flake8 glue/ lambda/ --max-line-length=120
```

## Deployment Order (Important)

**Code must deploy before infrastructure.**

1. Merge to prod in `de1-code-migration` → scripts land in S3
2. Then merge to prod in `de1-infrastructure` → Glue/Lambda resources created pointing to those scripts
