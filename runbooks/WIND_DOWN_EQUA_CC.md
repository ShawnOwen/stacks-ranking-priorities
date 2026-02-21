# Wind Down Public `equa.cc` (Issue #358)

> Non-destructive, rollback-friendly plan to reduce GCP spend.

## What we can confirm from outside (no GCP auth)
As of **2026-02-21**:
- `equa.cc` **A** → `136.110.187.76`
- `api.equa.cc` **A** → `136.110.187.76`
- Reverse DNS for `136.110.187.76` → `*.bc.googleusercontent.com` (Google Cloud customer IP)
- `app.equa.cc` **CNAME** → `ghs.googlehosted.com` (Google hosted)
- Nameservers → `ns-cloud-c*.googledomains.com` (Google Cloud DNS)
- `curl -I https://equa.cc` returns `server: Google Frontend` (often indicates HTTPS Load Balancer and/or serverless)
- `curl -I https://api.equa.cc` returns `x-powered-by: Express` + `server: Google Frontend`

**Implication:** there is very likely a **Google Cloud HTTPS Load Balancer** (or similar Google front-door) serving both the static site and the API.

## Immediate goal
Reduce monthly run-rate to near-idle by:
1) backing up data + capturing config
2) cutting public traffic at DNS/edge
3) scaling compute to zero / stopping VMs
4) sweeping for lingering billable resources (LB/NAT/static IP/Artifact Registry/SQL)

## Inputs needed from Shawn (to make the checklist exact)
Please provide one of:
- the **GCP Project ID** that owns the `equa.cc` infra (and any staging project), or
- paste the output of `gcloud projects list` and confirm which project is prod.

Also helpful:
- whether the API is Cloud Run vs GCE VM vs GKE
- what DB is used (Cloud SQL Postgres/MySQL? Firestore?)

## Inventory commands (copy/paste)
> These are safe read-only commands.

```bash
gcloud config get-value project

gcloud run services list --platform=managed --regions=all

gcloud compute instances list

gcloud compute forwarding-rules list --global

gcloud compute url-maps list

gcloud compute target-https-proxies list

gcloud compute backend-services list --global

gcloud compute addresses list --global

gcloud dns managed-zones list
# If zone is known:
# gcloud dns record-sets list --zone <zone>

gcloud sql instances list

gcloud scheduler jobs list --locations=all

gcloud pubsub topics list

gcloud pubsub subscriptions list

gcloud storage buckets list

gcloud artifacts repositories list --locations=all

gcloud compute routers list --regions=all

gcloud compute networks subnets list --regions=all
```

## Backup / capture state (do BEFORE stopping)
1) **Cloud SQL**: create on-demand backup + export to GCS (portable)
2) **Firestore** (if used): export to GCS
3) **GCS buckets**: at least list buckets; optionally rsync critical buckets to a dedicated backup bucket
4) **Cloud Run**: export service config YAML/JSON (env var names only; do not commit secret values)
5) **Cloud DNS**: export zone file

## Shutdown sequence (recommended)
### Step 1 — Cut public traffic (fast rollback)
Option A (preferred): **DNS cutover**
- Lower TTL to 60s (temporary)
- Point `equa.cc` and `api.equa.cc` to a maintenance target (cheap static host)
- Keep old records for rollback

Option B: **Lock down API**
- For Cloud Run: remove `allUsers` invoker IAM binding

### Step 2 — Stop/scale compute
- Cloud Run: set `min-instances=0` (and verify CPU is request-only)
- Compute Engine: stop VMs
- GKE: scale node pools to 0 or minimum
- Pause Cloud Scheduler jobs / disable Pub/Sub push endpoints

### Step 3 — Billing sweep
Within 24–72 hours, check Billing → Reports SKUs.
Common lingering costs:
- Cloud SQL instance tier/storage
- HTTPS Load Balancer (base hourly + rule)
- Cloud NAT
- Reserved static external IPs
- Artifact Registry storage

## Rollback (keep this trivial)
- Revert DNS records to previous values
- Re-enable Cloud Run invoker / restart VMs / restore scheduler jobs

## Cost levers (rule-of-thumb)
Without the project’s Billing → SKU breakdown, exact numbers aren’t possible, but typical major spend drivers are:
- **Cloud SQL** (often $100–$400/mo depending tier/HA/storage)
- **GKE node pools / VMs** (varies widely)
- **HTTPS Load Balancer** (commonly ~$18+/mo base, plus usage)
- **Cloud NAT** (can be ~$30+/mo base + data)

Next step is to run the inventory commands above and identify the top 3 SKUs in Billing.
