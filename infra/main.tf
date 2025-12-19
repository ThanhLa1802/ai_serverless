terraform {
  backend "s3" {
    bucket = "my-data-quality-bucket-thanh"
    key    = "state/terraform.tfstate"
    region = "ap-southeast-1"
  }
}