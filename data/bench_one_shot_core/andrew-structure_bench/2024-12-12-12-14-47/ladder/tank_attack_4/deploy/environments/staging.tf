terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "tank-attack-4-cdn-environment-staging"
      project = "Production"
    }
  }
}