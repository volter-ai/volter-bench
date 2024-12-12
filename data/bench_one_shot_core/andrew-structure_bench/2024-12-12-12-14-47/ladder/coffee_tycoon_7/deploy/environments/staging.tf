terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "coffee-tycoon-7-cdn-environment-staging"
      project = "Production"
    }
  }
}