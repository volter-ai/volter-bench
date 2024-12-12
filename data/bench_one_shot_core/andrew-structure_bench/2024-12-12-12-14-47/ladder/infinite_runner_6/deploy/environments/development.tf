terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "infinite-runner-6-cdn-environment-development"
      project = "Development"
    }
  }
}