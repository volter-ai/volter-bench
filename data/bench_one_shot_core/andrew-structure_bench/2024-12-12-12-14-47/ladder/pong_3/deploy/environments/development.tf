terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "pong-3-cdn-environment-development"
      project = "Development"
    }
  }
}