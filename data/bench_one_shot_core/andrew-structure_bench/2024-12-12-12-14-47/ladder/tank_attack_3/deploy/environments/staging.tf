terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "tank-attack-3-cdn-environment-staging"
      project = "Production"
    }
  }
}