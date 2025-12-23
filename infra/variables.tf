variable "aws_region" {
  default = "ap-southeast-1"
}

variable "project_name" {
  default = "serverless-rag"
}

variable "openai_api_key" {
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

variable "image_tag" {
  description = "Docker image tag"
  type        = string
}