terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "pong-7-cdn-environment-staging"
      project = "Production"
    }
  }
}