#!/bin/bash

BUCKET="aws-developing-youtube-analysis"
LAMBDA_NAME="active-s3"
LAMBDA_ROLE="active-s3-role-lif0542p"
GLUE_JOB="s3_csv_change_schema"
GLUE_ROLE="glue-s3-worker"
EB_RULE="glue-finished"
SNS_TOPIC_ARN="arn:aws:sns:eu-north-1:992382547485:s3-notification"

mkdir -p infrastructure/s3 infrastructure/lambda infrastructure/glue infrastructure/eventbridge infrastructure/sns

# S3 trigger
aws s3api get-bucket-notification-configuration --bucket $BUCKET > infrastructure/s3/trigger-config.json

# Lambda trust policy
aws iam get-role --role-name $LAMBDA_ROLE --query "Role.AssumeRolePolicyDocument" > infrastructure/lambda/trust-policy.json

# Lambda inline policies
for policy in $(aws iam list-role-policies --role-name $LAMBDA_ROLE --query "PolicyNames[]" --output text); do
    aws iam get-role-policy --role-name $LAMBDA_ROLE --policy-name $policy > "infrastructure/lambda/$policy.json"
done

# Glue job config
aws glue get-job --job-name $GLUE_JOB > infrastructure/glue/job-config.json

# Glue role config
aws iam list-attached-role-policies --role-name $GLUE_ROLE > infrastructure/glue/role-config.json

# Glue trust policy
aws iam get-role --role-name $GLUE_ROLE --query "Role.AssumeRolePolicyDocument" > infrastructure/glue/trust-policy.json

# EventBridge rule + targets
RULE=$(aws events describe-rule --name $EB_RULE)
TARGETS=$(aws events list-targets-by-rule --rule $EB_RULE)
echo "{\"rule\": $RULE, \"targets\": $TARGETS}" | python3 -m json.tool > infrastructure/eventbridge/rule.json

# SNS topic config + subscriptions
TOPIC_ATTRS=$(aws sns get-topic-attributes --topic-arn $SNS_TOPIC_ARN)
SUBSCRIPTIONS=$(aws sns list-subscriptions-by-topic --topic-arn $SNS_TOPIC_ARN)
echo "{\"attributes\": $TOPIC_ATTRS, \"subscriptions\": $SUBSCRIPTIONS}" | python3 -m json.tool > infrastructure/sns/topic-config.json

echo "Done. Copy the infrastructure/ folder to your local repo and commit."
