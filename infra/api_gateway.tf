resource "aws_apigatewayv2_api" "http_api" {
  name          = "${var.project_name}-gateway"
  protocol_type = "HTTP"

  cors_configuration {
    allow_headers = ["*"]
    allow_methods = ["GET", "POST", "OPTIONS"]
    allow_origins = ["*"]
    max_age       = 300
  }
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http_api.id
  name        = "$default"
  auto_deploy = true
}

# Kết nối API Gateway tới Lambda
resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id           = aws_apigatewayv2_api.http_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.query_handler.arn
}

# Định nghĩa Route (Ví dụ: POST /ask)
resource "aws_apigatewayv2_route" "query_route" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "POST /ask"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_stage" "dev_stage" {
  api_id = aws_apigatewayv2_api.http_api.id
  name   = "dev"

  auto_deploy = true
}

# Cấp quyền cho API Gateway gọi Lambda
resource "aws_lambda_permission" "api_gw_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.query_handler.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http_api.execution_arn}/*/*"
}