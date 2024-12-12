terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "tank-attack-2-cdn-environment-staging"
      project = "Production"
    }
  }
}