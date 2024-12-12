terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "coffee-tycoon-6-cdn-environment-staging"
      project = "Production"
    }
  }
}