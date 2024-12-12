terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "pong-7-cdn-environment-development"
      project = "Development"
    }
  }
}