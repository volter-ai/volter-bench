terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "infinite-runner-3-cdn-environment-development"
      project = "Development"
    }
  }
}