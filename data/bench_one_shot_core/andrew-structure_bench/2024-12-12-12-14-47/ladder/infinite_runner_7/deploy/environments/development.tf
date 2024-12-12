terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "infinite-runner-7-cdn-environment-development"
      project = "Development"
    }
  }
}