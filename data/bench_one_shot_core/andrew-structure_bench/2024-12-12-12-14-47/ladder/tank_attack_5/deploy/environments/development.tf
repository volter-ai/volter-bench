terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "tank-attack-5-cdn-environment-development"
      project = "Development"
    }
  }
}