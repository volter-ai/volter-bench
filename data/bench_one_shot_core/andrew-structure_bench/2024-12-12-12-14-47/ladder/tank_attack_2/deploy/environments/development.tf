terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "tank-attack-2-cdn-environment-development"
      project = "Development"
    }
  }
}