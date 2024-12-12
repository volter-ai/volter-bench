terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "gold-miner-1-cdn-environment-development"
      project = "Development"
    }
  }
}