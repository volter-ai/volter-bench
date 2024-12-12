terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "infinite-runner-4-cdn-environment-development"
      project = "Development"
    }
  }
}