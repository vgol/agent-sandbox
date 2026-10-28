# OVHcloud VPS-1

Configuration only: no server has been ordered or paid for.

## Provider and selection

- Official repository: <https://github.com/ovh/terraform-provider-ovh>
- Resource documentation: <https://registry.terraform.io/providers/ovh/ovh/2.23.0/docs/resources/vps>
- Provider pinned to `ovh/ovh` version `2.23.0`.
- German billing subsidiary, using the European account API (`ovh-eu`).
  The API endpoint follows the account, not the server location.
- VPS-1 2027 (`vps-2027-model1`), Ubuntu 24.04 LTS.
- Monthly subscription (`P1M`, `default`), with no long-term commitment.
- Mandatory options: Linux, local storage and standard one-day automatic backup.
  No premium backup, snapshot, control panel or additional disk.

On 2026-10-28, the public stock API reported all listed European locations
out of stock for this plan and Ubuntu. Beauharnois, Canada (`BHS`) was available,
so it is the explicit fallback. The older VPS-1 2026 plan was also out of stock
in Europe. Stock is not reserved.

## Catalogue price, not an account-specific quote

The German public catalogue returned these monthly prices on 2026-10-28:

| Item | Excluding VAT |
| --- | ---: |
| VPS-1 2027 | EUR 4.49 |
| Required standard automatic backup | EUR 0.35 |
| Required Linux and local storage | EUR 0.00 |
| Total | EUR 4.84 |
| Total including German 19% VAT, rounded | EUR 5.76 |

The selected default installation fees were zero. Account tax treatment,
discounts, location-specific charges and catalogue changes can affect checkout.
**Review the authenticated checkout total and renewal terms before approving
any order.** A Terraform plan is not a binding price quotation.

Public sources:

- [German VPS catalogue](https://eu.api.ovh.com/1.0/order/catalog/public/vps?ovhSubsidiary=DE)
- [Stock for VPS-1 and Ubuntu 24.04](https://eu.api.ovh.com/1.0/vps/order/rule/datacenter?ovhSubsidiary=DE&planCode=vps-2027-model1&os=Ubuntu%2024.04)

To recheck stock without account credentials:

```sh
curl -fsSL --get 'https://eu.api.ovh.com/1.0/vps/order/rule/datacenter' \
  --data-urlencode ovhSubsidiary=DE \
  --data-urlencode planCode=vps-2027-model1 \
  --data-urlencode 'os=Ubuntu 24.04' |
  jq '.datacenters[] | {datacenter, status, linuxStatus}'
```

Prefer an available European location before falling back to `BHS`:
`DE` (Germany), `GRA`/`SBG`/`EU-WEST-RBX` (France), `WAW` (Poland),
`UK` (United Kingdom), or `EU-SOUTH-MIL` (Italy). Set the chosen code with
`-var='datacenter=DE'`, for example. There is deliberately no automatic retry
or region change during ordering.

## Validate safely

The repository's devcontainer includes Terraform and the HashiCorp Terraform
VS Code extension. Rebuild and reopen the devcontainer to use them, or
install [Terraform](https://developer.hashicorp.com/terraform/install) locally.
Then run from this directory:

```sh
terraform init
terraform fmt -check
terraform validate
```

These commands do not order anything and do not require account credentials.
Keep the generated `.terraform.lock.hcl` in version control.

`purchase_approved` defaults to `false`: a lifecycle precondition blocks an
order plan/apply. `prevent_destroy` also guards against accidental termination
and replacements while this resource block remains in the configuration.
Neither mechanism is an account-level spending restriction.

## Credentials and checkout review

Do not paste API secrets or private SSH keys into chat, Terraform source,
variable files or Git. Use a short-lived, restricted API token and environment
variables, or a protected configuration file outside the repository.

For application-key authentication, set these locally:

```sh
export OVH_ENDPOINT=ovh-eu
read -rsp 'OVH application key: ' OVH_APPLICATION_KEY; echo
export OVH_APPLICATION_KEY
read -rsp 'OVH application secret: ' OVH_APPLICATION_SECRET; echo
export OVH_APPLICATION_SECRET
read -rsp 'OVH consumer key: ' OVH_CONSUMER_KEY; echo
export OVH_CONSUMER_KEY
```

The commands above use Bash. Do not enable shell tracing while handling secrets.
[Provider authentication options](https://registry.terraform.io/providers/ovh/ovh/2.23.0/docs).

Before granting payment rights, sign into the OVHcloud Control Panel and build
the same VPS configuration in the order funnel. Review its final total,
monthly/no-commitment terms and stock, but **do not complete that order** if
Terraform will create it. The account needs a default payment method for a
later Terraform order.

For a future order-capable token, follow the provider's
[order workflow access rules](https://github.com/ovh/terraform-provider-ovh/blob/v2.23.0/docs/guides/order_consumer_key_access_rules.md)
for `ovh_vps`. VPS-only API permissions are insufficient: ordering also needs
cart, checkout, payment and order-status routes. Avoid unrestricted `/*`
permissions. Configuration validation needs no token at all.

## Future provisioning, only after explicit approval

Do not run this section as part of configuration-only preparation. These are
manual instructions for a later, approved purchase, not an authorization.

1. Recheck stock, account-specific price and terms.
2. Select the location explicitly; do not change it after creating the VPS.
3. Generate and review an order plan:

   ```sh
   terraform plan \
     -var='purchase_approved=true' \
     -var='datacenter=BHS' \
     -out=order.tfplan
   ```

4. Only after approving the purchase, `terraform apply order.tfplan` places
   and pays for the order. Treat the saved plan and state as sensitive.
5. After provisioning, keep `purchase_approved=true` in a local ignored
   variable file for subsequent plans. Changing plan/options/datacenter can
   require replacement and another purchase; `prevent_destroy` blocks this
   rather than silently migrating the VPS.

If you instead buy in the Control Panel, do not apply this configuration to
create a second VPS. Import the existing service and reconcile its
configuration first.

## First login after a future purchase

This configuration deliberately does not set `public_ssh_key`: this provider
requires an image UUID with that argument, and a guessed image UUID is unsafe.
The initial OS is selected via `vps_os`. OVHcloud's default initial-password
delivery remains enabled; follow the delivery email and Control Panel
instructions, using the actual public IP.

For an Ubuntu installation, the initial SSH user is normally `ubuntu`.
Verify the host fingerprint through a trusted channel, change the initial
password, install your public SSH key and verify key login in a second session.
Only then disable SSH password authentication. Enable a firewall that allows
SSH before activating it, apply OS updates, and open only application ports
you actually need. Never upload your private SSH key to the VPS.

Moving to Europe later requires a new VPS, data migration and explicit
cancellation of the Canadian subscription; it is not an in-place location
change. Deleting Terraform files/state does not cancel OVHcloud billing.
