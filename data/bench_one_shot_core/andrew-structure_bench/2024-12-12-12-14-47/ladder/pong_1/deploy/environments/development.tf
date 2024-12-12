terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "pong-1-cdn-environment-development"
      project = "Development"
    }
  }
}