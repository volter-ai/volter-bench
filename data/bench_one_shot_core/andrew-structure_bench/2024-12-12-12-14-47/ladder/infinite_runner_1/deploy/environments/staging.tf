terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "infinite-runner-1-cdn-environment-staging"
      project = "Production"
    }
  }
}