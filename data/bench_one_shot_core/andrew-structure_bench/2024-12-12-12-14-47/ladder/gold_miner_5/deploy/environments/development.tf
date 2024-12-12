terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "gold-miner-5-cdn-environment-development"
      project = "Development"
    }
  }
}