terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "tank-attack-1-cdn-environment-staging"
      project = "Production"
    }
  }
}