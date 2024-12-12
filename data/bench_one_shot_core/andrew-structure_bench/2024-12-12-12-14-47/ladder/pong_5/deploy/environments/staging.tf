terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "pong-5-cdn-environment-staging"
      project = "Production"
    }
  }
}