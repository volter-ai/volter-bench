terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "infinite-runner-1-cdn-environment-development"
      project = "Development"
    }
  }
}