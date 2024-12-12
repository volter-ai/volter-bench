terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "coffee-tycoon-6-cdn-environment-development"
      project = "Development"
    }
  }
}