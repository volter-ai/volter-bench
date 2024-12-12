terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "gold-miner-5-cdn-environment-staging"
      project = "Production"
    }
  }
}