# Data Engineering - Lambda Volume Calculator

A Terraform project that deploys an AWS Lambda function to calculate rectangular volume.

## What it does

Lambda function accepts `length`, `width`, and `height` parameters and returns the calculated volume.

## Usage

### Deploy
```bash
terraform init
terraform apply
```

### Invoke from CLI
```bash
aws lambda invoke \
  --function-name example_lambda_function \
  --payload '{"length": 10, "width": 6, "height": 1}' \
  response.json

cat response.json
# Output: {"volume": 60}
```

### Cleanup
```bash
terraform destroy
```

## Environment

- Runtime: Python 3.12
- IAM Role: `lambda_execution_role` (auto-created)
- Region: Default AWS region in your credentials
