# 1. Tạo S3 Bucket để chứa tài liệu PDF
resource "aws_s3_bucket" "document_bucket" {
  bucket = "${var.project_name}-documents-${var.aws_region}"
}

# 2. Cấp quyền cho S3 để có thể trigger Lambda Ingestion
resource "aws_lambda_permission" "allow_s3_ingest" {
  statement_id  = "AllowS3InvokeIngestLambda"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ingest_handler.function_name # Đảm bảo tên resource trùng với lambda.tf
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.document_bucket.arn
}

# 3. Cấu hình Event Notification: Trigger khi có file .pdf được tạo
resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.document_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.ingest_handler.arn
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = ".pdf"
  }

  depends_on = [aws_lambda_permission.allow_s3_ingest]
}