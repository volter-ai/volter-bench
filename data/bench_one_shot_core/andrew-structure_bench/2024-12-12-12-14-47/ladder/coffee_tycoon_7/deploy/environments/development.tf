terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "coffee-tycoon-7-cdn-environment-development"
      project = "Development"
    }
  }
}