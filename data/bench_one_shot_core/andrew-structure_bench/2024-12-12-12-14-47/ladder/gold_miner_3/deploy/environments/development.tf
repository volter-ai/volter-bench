terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "gold-miner-3-cdn-environment-development"
      project = "Development"
    }
  }
}