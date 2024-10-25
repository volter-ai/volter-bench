module "s3_static_content_bucket" {
  source        = "app.terraform.io/Volter/s3-bucket/aws"
  version       = "1.0.4"
  bucket_name   = "volter-sites-static-content-${local.name}"
  force_destroy = true
  tags = {
    Environment = "${local.name}-development"
    Project     = "Development"
  }
}

# S3 backed CDN block
# S3 bucket for CDNs is initialized at the environment level.
module "cdn_s3_one_shot_game" {
  source  = "app.terraform.io/Volter/cdn/aws"
  version = "1.1.8"
  bucket_name            = module.s3_static_content_bucket.bucket_name
  cloudfront_price_class = local.cloudfront_price_class
  # Must be a directory.
  website_content_path   = "dist"
  domain_name            = local.domain_name
  subdomain              = local.name
  route53_zone_id        = "Z1045067G5OQQNGM5F08"
  acm_certificate_arn    = local.certificate_arn # Your existing ACM certificate ARN
  handle_404 = false
  handle_403 = false
  file_404 = "404.html"
  file_403 = "index.html"
}

output "cdn_info" {
  value       = module.cdn_s3_one_shot_game
  description = "The outputs of the cdn module"
}
