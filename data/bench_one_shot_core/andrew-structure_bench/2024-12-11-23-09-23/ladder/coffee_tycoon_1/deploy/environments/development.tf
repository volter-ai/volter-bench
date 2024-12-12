terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "coffee-tycoon-1-cdn-environment-development"
      project = "Development"
    }
  }
}