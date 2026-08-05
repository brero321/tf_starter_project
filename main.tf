# IAM role for Lambda execution

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "example" {
  name               = "lambda_execution_role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

# S3 bucket the Lambda will read/write
resource "aws_s3_bucket" "example" {
  bucket = "example-lambda-data-bucket" # must be globally unique; change as needed
}

# IAM policy scoped to just this bucket
data "aws_iam_policy_document" "lambda_s3_access" {
  statement {
    effect = "Allow"

    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject",
    ]

    resources = ["${aws_s3_bucket.example.arn}/*"]
  }

  statement {
    effect = "Allow"

    actions = [
      "s3:ListBucket",
    ]

    resources = [aws_s3_bucket.example.arn]
  }
}

resource "aws_iam_role_policy" "lambda_s3_access" {
  name   = "lambda_s3_access"
  role   = aws_iam_role.example.id
  policy = data.aws_iam_policy_document.lambda_s3_access.json
}

# Basic CloudWatch Logs permissions (commonly needed, not present before)
data "aws_iam_policy_document" "lambda_logging" {
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = ["arn:aws:logs:*:*:*"]
  }
}

resource "aws_iam_role_policy" "lambda_logging" {
  name   = "lambda_logging"
  role   = aws_iam_role.example.id
  policy = data.aws_iam_policy_document.lambda_logging.json
}

# Package the Lambda function code
data "archive_file" "example" {
  type        = "zip"
  source_file = "${path.module}/lambda/example.py"
  output_path = "${path.module}/lambda/function.zip"
}

# Lambda function
resource "aws_lambda_function" "example" {
  filename      = data.archive_file.example.output_path
  function_name = "example_lambda_function"
  role          = aws_iam_role.example.arn
  handler       = "example.lambda_handler"
  code_sha256   = data.archive_file.example.output_base64sha256

  runtime = "python3.12"

  environment {
    variables = {
      ENVIRONMENT = "production"
      LOG_LEVEL   = "info"
      BUCKET_NAME = aws_s3_bucket.example.bucket
    }
  }

  tags = {
    Environment = "production"
    Application = "example"
  }
}