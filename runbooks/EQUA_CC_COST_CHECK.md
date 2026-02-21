# equa.cc — Cost check (GCP)

This is a lightweight checklist to identify **what is still charging** after you cut traffic and/or stop services.

> Goal: drive run-rate to **<$50/mo** while keeping rollback possible.

## 1) Quick billing snapshot (UI)

1. Open **GCP Console → Billing → Reports**
2. Set:
   - **Project** = the equa.cc prod project
   - **Time range** = last **7 days** (and also last **24 hours** after changes)
   - **Group by** = **SKU** (and optionally by **Service**)
3. Export or copy the top 10 SKUs.

### Common “lingering charge” culprits
- **Cloud SQL** (often the #1 cost driver)
- **Cloud Load Balancing** (forwarding rules, URL maps, proxies)
- **Cloud NAT** (if used)
- **Compute Engine**: instance core hours, persistent disks, snapshots
- **Artifact Registry** storage
- **Cloud Logging** ingestion/retention
- **BigQuery** storage/query

## 2) Programmatic run-rate check (requires gcloud auth)

If you have permission, you can use the Billing export APIs, but the UI is usually faster.

A practical approach is:
- use `scripts/gcp_inventory_dump.sh <PROJECT_ID>` to list what exists
- use Billing Reports (UI) to map charges → specific resources

## 3) Fast mapping: resource → cost lever

| Resource | Cost lever | Rollback friendliness |
|---|---|---|
| Cloud Run | set min instances = 0; remove unauth invoker; disable schedulers calling it | very high |
| Cloud SQL | stop instance (if supported) or downsize tier | medium-high (depending on restore) |
| HTTPS Load Balancer | delete LB components and release static IP **after DNS cutover** | medium |
| Reserved external IP | release if unused | high |
| Cloud NAT | delete NAT router if no egress needs remain | medium |
| Logging | reduce retention / exclusions | high |

## 4) After changes: verify

- Re-check Billing Reports after **24–72h**.
- Confirm:
  - No Cloud SQL compute charges (or reduced)
  - LB / static IP charges reduced
  - No unexpected VM/GKE charges

## 5) Attach findings back to the issue

When reporting back, paste:
- project id
- top SKUs (7d) and (24h)
- inventory dump folder path created by `gcp_inventory_dump.sh`
