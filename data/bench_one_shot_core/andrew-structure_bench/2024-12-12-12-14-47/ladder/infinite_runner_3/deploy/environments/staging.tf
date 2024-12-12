terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "infinite-runner-3-cdn-environment-staging"
      project = "Production"
    }
  }
}