terraform {
  cloud {
    organization = "volter"
    workspaces {
      name    = "coffee-tycoon-5-cdn-environment-development"
      project = "Development"
    }
  }
}