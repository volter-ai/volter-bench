terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "coffee-tycoon-1-cdn-environment-staging"
      project = "Production"
    }
  }
}