terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "pong-2-cdn-environment-staging"
      project = "Production"
    }
  }
}