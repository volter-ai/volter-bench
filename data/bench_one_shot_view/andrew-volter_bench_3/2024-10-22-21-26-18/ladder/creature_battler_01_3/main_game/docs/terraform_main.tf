provider "aws" {
  region = local.region
}

locals {
  region                 = "us-west-1"
  domain_name            = "voltername.com"
  account_id             = "340752828662"
  tf_environment         = "creature_battler_01_1-staging"
  environment            = "staging"
  cloudfront_price_class = "PriceClass_100"
  name                   = "creature_battler_01_1"
  certificate_arn        = "arn:aws:acm:us-east-1:340752828662:certificate/523feeb7-f41b-49bb-b268-6f486a1d3305" # Your existing ACM certificate ARN
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

  cloud {
    organization = "volter"

    workspaces {
      name    = "creature_battler_01_1-staging"
      project = "Staging"
    }
  }
}


data "tfe_outputs" "environment" {
  organization = "volter"
  workspace    = "environment-${local.environment}"
}


# S3 backed CDN block

# S3 bucket for CDNs is initialized at the environment level.

module "cdn_s3_creature_battler_01_1_game" {
  source  = "app.terraform.io/Volter/cdn/aws"
  version = "1.1.3"

  bucket_name            = data.tfe_outputs.environment.values.s3_static_content_bucket_name
  cloudfront_price_class = local.cloudfront_price_class
  website_content_path   = "dist"
  domain_name            = local.domain_name
  subdomain              = local.name
  route53_zone_id        = data.tfe_outputs.environment.values.route53_zone_id
  acm_certificate_arn    = local.certificate_arn
  handle_404 = true
  handle_403 = true
  file_404 = "index.html"
  file_403 = "index.html"
}

output "cdn_info" {
  value       = module.cdn_s3_creature_battler_01_1_game
  description = "The outputs of the cdn module"
}