terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "coffee-tycoon-5-cdn-environment-staging"
      project = "Production"
    }
  }
}