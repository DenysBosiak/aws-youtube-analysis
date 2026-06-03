# AWS YouTube Analysis

A serverless data pipeline on AWS that ingests YouTube trending data (CSV), transforms it, and sends notifications on completion.

## Pipeline

```
CSV file → S3 (raw/) → Lambda → Glue → EventBridge → SNS
```

| Step | Service | What it does |
|---|---|---|
| 1 | S3 | Receives raw CSV files in the `raw/` prefix |
| 2 | Lambda (`active-s3`) | Triggered on S3 `ObjectCreated:Put`, starts the Glue job |
| 3 | Glue (`s3_csv_change_schema`) | Reads CSV, applies schema mapping, writes Parquet to `bronze/` |
| 4 | EventBridge (`glue-finished`) | Listens for Glue job `SUCCEEDED` or `FAILED` state changes |
| 5 | SNS (`s3-notification`) | Sends notification when the pipeline finishes |

## Data transformation

The Glue job reads CSV from `s3://aws-developing-youtube-analysis/raw/` and applies the following schema changes:

- `category_id` string → int
- `publish_time` string → timestamp
- `views`, `likes`, `dislikes`, `comment_count` string → int

Output is written as Snappy-compressed Parquet to `s3://aws-developing-youtube-analysis/bronze/`.

## Infrastructure

All AWS resource configurations are stored in `infrastructure/`:

```
infrastructure/
├── config.json            # resource names and ARNs
├── s3/                    # S3 trigger config
├── lambda/                # Lambda code and IAM policies
├── glue/                  # Glue job script and IAM role
├── eventbridge/           # EventBridge rule and targets
└── sns/                   # SNS topic and subscriptions
```

## Exporting configs from AWS

To update local infrastructure configs after making changes in AWS Console, run the export script in AWS CloudShell:

```bash
chmod +x export-configs.sh
./export-configs.sh
```

Then copy the generated `infrastructure/` files to your local repo and commit.

## Region

`eu-north-1`
