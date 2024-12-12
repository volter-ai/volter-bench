terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "tank-attack-7-cdn-environment-development"
      project = "Development"
    }
  }
}