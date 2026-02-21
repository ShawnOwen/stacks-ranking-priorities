#!/usr/bin/env bash
set -euo pipefail

# Read-only inventory dump for equa.cc wind-down.
# Usage:
#   ./scripts/gcp_inventory_dump.sh <project-id> [output-dir]

PROJECT_ID="${1:-}"
OUT_DIR="${2:-}"

if [[ -z "$PROJECT_ID" ]]; then
  echo "Usage: $0 <project-id> [output-dir]" >&2
  exit 1
fi

TS="$(date +%Y%m%d-%H%M%S)"
if [[ -z "$OUT_DIR" ]]; then
  OUT_DIR="$HOME/equa-winddown-inventory/$PROJECT_ID/$TS"
fi

mkdir -p "$OUT_DIR/state"

echo "Writing inventory to: $OUT_DIR" >&2

gcloud config set project "$PROJECT_ID" >/dev/null

echo "project" >&2
(gcloud projects describe "$PROJECT_ID" --format=json || true) > "$OUT_DIR/state/project.json"

echo "enabled apis" >&2
(gcloud services list --enabled --format=json || true) > "$OUT_DIR/state/enabled-apis.json"

echo "cloud run" >&2
(gcloud run services list --platform=managed --regions=all --format=json || true) > "$OUT_DIR/state/cloudrun-services.json"

echo "compute" >&2
(gcloud compute instances list --format=json || true) > "$OUT_DIR/state/compute-instances.json"

echo "load balancer bits" >&2
(gcloud compute forwarding-rules list --global --format=json || true) > "$OUT_DIR/state/lb-forwarding-rules.json"
(gcloud compute url-maps list --format=json || true) > "$OUT_DIR/state/lb-url-maps.json"
(gcloud compute target-https-proxies list --format=json || true) > "$OUT_DIR/state/lb-https-proxies.json"
(gcloud compute backend-services list --global --format=json || true) > "$OUT_DIR/state/lb-backend-services.json"
(gcloud compute addresses list --global --format=json || true) > "$OUT_DIR/state/compute-addresses-global.json"

(gcloud compute routers list --regions=all --format=json || true) > "$OUT_DIR/state/compute-routers.json"
(gcloud compute networks list --format=json || true) > "$OUT_DIR/state/networks.json"
(gcloud compute networks subnets list --regions=all --format=json || true) > "$OUT_DIR/state/subnets.json"


echo "dns" >&2
(gcloud dns managed-zones list --format=json || true) > "$OUT_DIR/state/dns-zones.json"

# If you know the zone, export record sets:
# ZONE="equa-cc"
# gcloud dns record-sets export "$OUT_DIR/state/dns-$ZONE.zone" --zone "$ZONE" || true


echo "sql" >&2
(gcloud sql instances list --format=json || true) > "$OUT_DIR/state/cloudsql-instances.json"


echo "scheduler" >&2
(gcloud scheduler jobs list --locations=all --format=json || true) > "$OUT_DIR/state/scheduler-jobs.json"


echo "pubsub" >&2
(gcloud pubsub topics list --format=json || true) > "$OUT_DIR/state/pubsub-topics.json"
(gcloud pubsub subscriptions list --format=json || true) > "$OUT_DIR/state/pubsub-subscriptions.json"


echo "storage" >&2
(gcloud storage buckets list --format=json || true) > "$OUT_DIR/state/gcs-buckets.json"


echo "artifact registry" >&2
(gcloud artifacts repositories list --locations=all --format=json || true) > "$OUT_DIR/state/artifact-repos.json"


echo "done" >&2
printf "%s\n" "$OUT_DIR" > "$OUT_DIR/OUT_DIR.txt"
