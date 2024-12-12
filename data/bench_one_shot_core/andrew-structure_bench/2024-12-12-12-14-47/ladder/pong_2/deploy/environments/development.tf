terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "pong-2-cdn-environment-development"
      project = "Development"
    }
  }
}