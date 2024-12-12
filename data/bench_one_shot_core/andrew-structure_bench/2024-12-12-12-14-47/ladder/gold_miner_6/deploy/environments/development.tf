terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "gold-miner-6-cdn-environment-development"
      project = "Development"
    }
  }
}