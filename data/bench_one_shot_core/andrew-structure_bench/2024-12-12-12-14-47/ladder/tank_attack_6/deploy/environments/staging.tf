terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "tank-attack-6-cdn-environment-staging"
      project = "Production"
    }
  }
}