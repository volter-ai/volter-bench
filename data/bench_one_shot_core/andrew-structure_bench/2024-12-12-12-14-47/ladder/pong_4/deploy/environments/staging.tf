terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "pong-4-cdn-environment-staging"
      project = "Production"
    }
  }
}