# Tạo ECR Repository để đẩy Docker Image lên
resource "aws_ecr_repository" "app_repo" {
  name = var.project_name
}

resource "aws_lambda_function" "query_handler" {
  function_name = "query-handler"
  role          = aws_iam_role.lambda_exec.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.my_repo.repository_url}:latest"

  environment {
    variables = {
      GEMINI_API_KEY      = var.gemini_api_key
      PINECONE_API_KEY    = var.pinecone_api_key
      PINECONE_INDEX_NAME = "my-docs-index"
    }
  }
}


resource "aws_lambda_function" "rag_lambda" {
  function_name = "${var.project_name}-handler"
  role          = aws_iam_role.lambda_exec_role.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.app_repo.repository_url}:latest"
  
  timeout       = 30 # Tăng timeout vì xử lý LLM tốn thời gian
  memory_size   = 1024 # LangChain cần RAM tương đối

  environment {
    variables = {
      GEMINI_API_KEY      = var.gemini_api_key
      PINECONE_API_KEY    = var.pinecone_api_key
      PINECONE_INDEX_NAME = var.pinecone_index
    }
  }
}

# 1. Log Group cho hàm Ingestion
resource "aws_cloudwatch_log_group" "ingest_logs" {
  name              = "/aws/lambda/${aws_lambda_function.ingest_handler.function_name}"
  retention_in_days = 7 # Tự động xóa sau 7 ngày
}

# 2. Log Group cho hàm Query
resource "aws_cloudwatch_log_group" "query_logs" {
  name              = "/aws/lambda/${aws_lambda_function.query_handler.function_name}"
  retention_in_days = 7
}

# 3. IAM Policy cho phép ghi Log (Dùng chung cho cả 2 Role Lambda)
resource "aws_iam_policy" "lambda_logging_policy" {
  name        = "${var.project_name}-logging-policy"
  description = "Cho phép Lambda ghi log vào CloudWatch"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = [
          "${aws_cloudwatch_log_group.ingest_logs.arn}:*",
          "${aws_cloudwatch_log_group.query_logs.arn}:*"
        ],
        Effect = "Allow"
      }
    ]
  })
}

# Gắn Policy vào Role của Lambda
resource "aws_iam_role_policy_attachment" "ingest_logs_attach" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.lambda_logging_policy.arn
}