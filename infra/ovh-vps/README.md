# OVHcloud VPS-1

The VPS-1 (VPS-1 2027, Ubuntu 24.04 LTS, monthly, hosted in Canada) was
**ordered manually** in the OVHcloud order funnel. This configuration does not
order anything: it adopts the existing server into Terraform state by import.

- Provider: <https://github.com/ovh/terraform-provider-ovh>, pinned to `ovh/ovh` `2.23.0`.
- Resource: <https://registry.terraform.io/providers/ovh/ovh/2.23.0/docs/resources/vps>
- API endpoint `ovh-eu` (follows the account, not the server location).
- Display name: `marusya-agent`.
- Service name: `vps-9ce61658.vps.ovh.ca` (the default Terraform import target).
- [VPS dashboard](https://manager.eu.ovhcloud.com/#/dedicated/vps/vps-9ce61658.vps.ovh.ca/dashboard)
  (requires an OVHcloud login).

## How it works

- `import` block binds `ovh_vps.server` to `var.service_name`.
- The provider does not read `ovh_subsidiary`, `plan` or `plan_option` back
  from the API; they only matter for ordering. They are required by the schema,
  so placeholders are kept and listed in `ignore_changes`. A plan therefore
  cannot trigger a new order or a replacement.
- `ovh_subsidiary = "DE"` is an ignored ordering placeholder for the billing
  subsidiary, not the datacenter. It does not place or move the server in
  Germany. The existing Canadian location is preserved by import; the API
  endpoint also follows the account rather than the physical location.
- `prevent_destroy = true` blocks accidental termination. It is not an
  account-level spending restriction, and deleting Terraform files or state does
  not cancel OVHcloud billing.

## Find the service name

OVHcloud Control Panel, Bare Metal Cloud, VPS: this server's service name is
`vps-9ce61658.vps.ovh.ca`. It is an identifier, not a secret, and is configured
as the default for `var.service_name`. Its IP address, specifications and exact
datacenter must be checked in the authenticated dashboard or API.

## Credentials

Never put API secrets or private keys in chat, Terraform source, variable
files or Git. Use environment variables:

```sh
export OVH_ENDPOINT=ovh-eu
read -rsp 'OVH application key: ' OVH_APPLICATION_KEY; echo
export OVH_APPLICATION_KEY
read -rsp 'OVH application secret: ' OVH_APPLICATION_SECRET; echo
export OVH_APPLICATION_SECRET
read -rsp 'OVH consumer key: ' OVH_CONSUMER_KEY; echo
export OVH_CONSUMER_KEY
```

Import and read need only read access to the VPS, for example `GET` on
`/vps/*`, not any order or payment rights. Create the token at
<https://eu.api.ovh.com/createToken/> with that restriction.
Applying the display-name change additionally requires `PUT` on
`/vps/<service_name>` for this VPS. Do not grant order, payment, rebuild or
termination rights.
[Other authentication options](https://registry.terraform.io/providers/ovh/ovh/2.23.0/docs).

## Query the VPS and IP addresses

The devcontainer includes the [official OVHcloud CLI](https://github.com/ovh/ovhcloud-cli).
Run `ovhcloud version` to check the installation. It uses the same credentials
as Terraform from the environment variables above, or a local `ovh.conf`
configuration file. Keep credentials outside Git and chat. Grant only `GET`
on `/vps/*` for these read-only queries:

```sh
ovhcloud vps get vps-9ce61658.vps.ovh.ca -o json
ovhcloud vps ip list vps-9ce61658.vps.ovh.ca -o json
```

The second command queries the assigned IP addresses rather than guessing
them from DNS. If the CLI reports that authentication is missing, configure
the credentials above in the environment where it runs. Alternatively,
`ovhcloud login` creates credentials interactively; review the requested
permissions and restrict them to read access before authorizing.

## Import and verify

The devcontainer configuration includes Terraform. If VS Code reports it
missing in an older Codespace, run **Codespaces: Rebuild Container** (or
**Dev Containers: Rebuild and Reopen in Container** locally) to install the
configured feature. Check `terraform version` in a new terminal.
From this directory:

```sh
terraform init
terraform fmt -check
terraform validate
terraform plan
```

The first plan should report `1 to import` and no create, replace or destroy.
An in-place `display_name` update to `marusya-agent` is
expected if the current name differs. If it proposes any other changes, stop
and reconcile the configuration with the real server before applying. Then:

```sh
terraform apply
```

To target a different existing VPS, override `service_name` with `-var` or a
local `*.tfvars` file; these files are ignored by Git. Review the plan carefully
before switching targets. State contains server details, so keep it out of
Git too.

## First login

The initial SSH user is normally `ubuntu`; the initial password is delivered
by OVHcloud email unless disabled. Verify the host fingerprint through a
trusted channel, change the password, install your public SSH key and verify
key login in a second session. Only then disable SSH password authentication.
Enable a firewall that allows SSH first, apply OS updates and open only the
ports you need. Never upload your private SSH key to the VPS.

Moving to another location later requires a new VPS and data migration; it is
not an in-place change.
