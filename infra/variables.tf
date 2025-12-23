variable "aws_region" {
  default = "ap-southeast-1" # Singapore - gần Việt Nam nhất
}

variable "project_name" {
  default = "serverless-rag"
}

variable "groq_api_key" {
  type      = string
  sensitive = true
}

variable "pinecone_api_key" {
  type      = string
  sensitive = true
}

variable "pinecone_index" {
  type    = string
  default = "document-index"
}