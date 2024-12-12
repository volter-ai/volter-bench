terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "infinite-runner-4-cdn-environment-staging"
      project = "Production"
    }
  }
}