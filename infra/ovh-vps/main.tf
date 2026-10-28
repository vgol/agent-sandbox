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

variable "service_name" {
  description = "Service name of the manually ordered VPS, shown in the OVHcloud Control Panel."
  type        = string
  default     = "vps-9ce61658.vps.ovh.ca"

  validation {
    condition     = can(regex("\\.vps\\.ovh\\.(net|ca)$", var.service_name))
    error_message = "Expected a VPS service name such as vps-9ce61658.vps.ovh.ca."
  }
}

import {
  to = ovh_vps.server
  id = var.service_name
}

# The VPS was ordered manually, so the order-only attributes (ovh_subsidiary,
# plan, plan_option) are required by the schema but must never trigger a new
# order or a replacement. They are ignored after import.
resource "ovh_vps" "server" {
  display_name   = "marusya-agent"
  ovh_subsidiary = "DE"

  plan = [{
    plan_code    = "vps-2027-model1"
    duration     = "P1M"
    pricing_mode = "default"
  }]

  lifecycle {
    prevent_destroy = true
    ignore_changes  = [ovh_subsidiary, plan, plan_option]
  }
}

output "service_name" {
  description = "OVHcloud service identifier; find the public IP in the OVHcloud Control Panel."
  value       = ovh_vps.server.service_name
}
