terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "coffee-tycoon-2-cdn-environment-staging"
      project = "Production"
    }
  }
}