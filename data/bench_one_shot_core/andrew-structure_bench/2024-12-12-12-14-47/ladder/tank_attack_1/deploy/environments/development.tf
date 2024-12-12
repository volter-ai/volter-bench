terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "tank-attack-1-cdn-environment-development"
      project = "Development"
    }
  }
}