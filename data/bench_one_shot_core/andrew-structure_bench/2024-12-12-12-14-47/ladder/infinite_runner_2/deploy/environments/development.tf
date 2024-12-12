terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "infinite-runner-2-cdn-environment-development"
      project = "Development"
    }
  }
}