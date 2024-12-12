terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "gold-miner-2-cdn-environment-staging"
      project = "Production"
    }
  }
}