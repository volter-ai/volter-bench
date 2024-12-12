terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "pong-1-cdn-environment-staging"
      project = "Production"
    }
  }
}