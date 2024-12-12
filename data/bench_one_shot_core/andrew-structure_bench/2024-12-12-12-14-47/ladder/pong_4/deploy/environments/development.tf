terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "pong-4-cdn-environment-development"
      project = "Development"
    }
  }
}