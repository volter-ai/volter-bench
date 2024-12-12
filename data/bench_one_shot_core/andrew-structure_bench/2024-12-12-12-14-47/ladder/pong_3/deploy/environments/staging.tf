terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "pong-3-cdn-environment-staging"
      project = "Production"
    }
  }
}