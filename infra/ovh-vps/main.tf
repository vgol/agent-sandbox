terraform {
  required_version = ">= 1.5.0, < 2.0.0"

  required_providers {
    ovh = {
      source  = "ovh/ovh"
      version = "2.23.0"
    }
  }
}

provider "ovh" {
  endpoint = "ovh-eu"
}

variable "datacenter" {
  description = "Explicit location; recheck stock before ordering. BHS is the Canadian fallback."
  type        = string
  default     = "BHS"

  validation {
    condition = contains([
      "DE", "EU-SOUTH-MIL", "EU-WEST-RBX", "GRA", "SBG", "UK", "WAW", "BHS"
    ], var.datacenter)
    error_message = "Choose a European location or BHS (Beauharnois, Canada)."
  }
}

variable "purchase_approved" {
  description = "Keep false until the account-specific checkout total, stock and terms have been reviewed."
  type        = bool
  default     = false
}

resource "ovh_vps" "server" {
  display_name   = "vps-1"
  ovh_subsidiary = "DE"

  plan = [{
    plan_code    = "vps-2027-model1"
    duration     = "P1M"
    pricing_mode = "default"

    configuration = [
      {
        label = "vps_datacenter"
        value = var.datacenter
      },
      {
        label = "vps_os"
        value = "Ubuntu 24.04"
      }
    ]
  }]

  plan_option = [
    for code in [
      "option-linux",
      "option-storage-local-2027-model1",
      "option-auto-backup-2027-1-model1"
      ] : {
      plan_code    = code
      duration     = "P1M"
      pricing_mode = "default"
      quantity     = 1
    }
  ]

  lifecycle {
    prevent_destroy = true

    precondition {
      condition     = var.purchase_approved
      error_message = "Ordering is blocked. Review the account-specific checkout price, stock and monthly terms before explicitly setting purchase_approved=true."
    }
  }
}

output "service_name" {
  description = "OVHcloud service identifier; find its public IP in the OVHcloud Control Panel."
  value       = ovh_vps.server.name
}

output "datacenter" {
  value = var.datacenter
}
