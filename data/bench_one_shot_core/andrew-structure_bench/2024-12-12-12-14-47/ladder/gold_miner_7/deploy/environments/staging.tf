terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "gold-miner-7-cdn-environment-staging"
      project = "Production"
    }
  }
}