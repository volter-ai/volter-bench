terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "gold-miner-7-cdn-environment-development"
      project = "Development"
    }
  }
}