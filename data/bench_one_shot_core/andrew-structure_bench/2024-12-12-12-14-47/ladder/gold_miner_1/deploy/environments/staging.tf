terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "gold-miner-1-cdn-environment-staging"
      project = "Production"
    }
  }
}