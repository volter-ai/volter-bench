terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "infinite-runner-7-cdn-environment-staging"
      project = "Production"
    }
  }
}