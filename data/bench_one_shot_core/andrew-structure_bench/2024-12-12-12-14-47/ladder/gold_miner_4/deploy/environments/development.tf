terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "gold-miner-4-cdn-environment-development"
      project = "Development"
    }
  }
}