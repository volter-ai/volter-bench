terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "coffee-tycoon-3-cdn-environment-staging"
      project = "Production"
    }
  }
}