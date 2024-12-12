terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "tank-attack-3-cdn-environment-development"
      project = "Development"
    }
  }
}