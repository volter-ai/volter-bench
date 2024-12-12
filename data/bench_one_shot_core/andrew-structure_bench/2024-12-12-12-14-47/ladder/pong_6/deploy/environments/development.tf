terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "pong-6-cdn-environment-development"
      project = "Development"
    }
  }
}