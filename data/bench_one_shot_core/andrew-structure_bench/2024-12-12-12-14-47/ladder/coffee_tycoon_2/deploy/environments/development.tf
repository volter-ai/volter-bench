terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "coffee-tycoon-2-cdn-environment-development"
      project = "Development"
    }
  }
}