terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "infinite-runner-6-cdn-environment-staging"
      project = "Production"
    }
  }
}