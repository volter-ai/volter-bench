terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "pong-5-cdn-environment-development"
      project = "Development"
    }
  }
}