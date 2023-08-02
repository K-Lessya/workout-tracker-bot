terraform {
  required_version = ">= 1.0.0"
    backend "s3" {
      bucket = "workout-bot-iac"
      key    = "/workout-bot/terraform.tfstate"
      region = "eu-north-1"
    }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0.0"
    }
  }

}