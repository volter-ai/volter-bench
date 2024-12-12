terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "coffee-tycoon-4-cdn-environment-development"
      project = "Development"
    }
  }
}