provider "aws" {
  region = local.region
}

# variables.tf
variable "environment" {
  description = "Environment name (e.g. staging, production)"
  type        = string
}

variable "account_id" {
  description = "AWS Account ID"
  type        = string
}

variable "domain_name" {
  description = "Domain name for the CDN"
  type        = string
}

variable "certificate_arn" {
  description = "ACM certificate ARN"
  type        = string
}

locals {
  region                 = "us-west-1"
  tf_environment         = var.environment
  cloudfront_price_class = "PriceClass_100"
  name                   = "infinite-runner-1"
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.65.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.10.1"
    }
  }
}


data "tfe_outputs" "environment" {
  organization = "volter"
  workspace    = "environment-${var.environment}"
}



# S3 backed CDN block

# S3 bucket for CDNs is initialized at the environment level.

module "cdn_s3_infinite-runner-1_game" {
  source  = "app.terraform.io/Volter/cdn/aws"
  version = "2.1.4"

  game_name              = local.name
  bucket_name            = data.tfe_outputs.environment.values.s3_games_content_bucket_name
  cloudfront_price_class = local.cloudfront_price_class
  website_content_path   = "dist"
  domain_name            = var.domain_name
  subdomain              = local.name
  route53_zone_id        = data.tfe_outputs.environment.values.route53_draw2_zone_id
  acm_certificate_arn    = data.tfe_outputs.environment.values.cdn_games_certificate_arn
  handle_404             = false
  handle_403             = false
  file_404               = ""
  file_403               = ""
}

output "cdn_info" {
  value       = module.cdn_s3_infinite-runner-1_game
  description = "The outputs of the cdn module"
}