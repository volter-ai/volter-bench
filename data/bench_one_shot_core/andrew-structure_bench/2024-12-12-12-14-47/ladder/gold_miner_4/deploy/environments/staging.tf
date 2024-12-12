terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "gold-miner-4-cdn-environment-staging"
      project = "Production"
    }
  }
}