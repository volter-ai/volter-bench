terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "infinite-runner-5-cdn-environment-staging"
      project = "Production"
    }
  }
}