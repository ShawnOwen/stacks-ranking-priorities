#!/usr/bin/env bash
set -euo pipefail

# Read-only public reconnaissance for equa.cc.
# Purpose: identify likely hosting surface (LB vs Cloud Run vs GCE/GKE) *without* GCP credentials.
# Output: writes a timestamped folder under ./tmp/equa-cc-public-recon/

ROOT_DOMAIN="${1:-equa.cc}"
API_DOMAIN="${2:-api.equa.cc}"
APP_DOMAIN="${3:-app.equa.cc}"

TS="$(date -u +%Y%m%dT%H%M%SZ)"
OUTDIR="tmp/equa-cc-public-recon/${TS}"
mkdir -p "${OUTDIR}"

log() { printf "%s\n" "$*" | tee -a "${OUTDIR}/_log.txt" >/dev/null; }
run() {
  log "$ $*"
  # shellcheck disable=SC2068
  ( $@ ) 2>&1 | tee -a "${OUTDIR}/_log.txt" >"${OUTDIR}/$(echo "$*" | tr ' /' '__' | tr -cd '[:alnum:]_\n\-').txt" || true
}

log "# equa.cc public recon"
log "timestamp_utc=${TS}"
log "root=${ROOT_DOMAIN} api=${API_DOMAIN} app=${APP_DOMAIN}"

# DNS
run dig +noall +answer "${ROOT_DOMAIN}" A AAAA CNAME
run dig +noall +answer "${API_DOMAIN}" A AAAA CNAME
run dig +noall +answer "${APP_DOMAIN}" A AAAA CNAME

# Nameservers for the zone
run dig +noall +answer "${ROOT_DOMAIN}" NS

# HTTP headers (follow redirects)
run curl -sS -D - -o /dev/null -L "https://${ROOT_DOMAIN}"
run curl -sS -D - -o /dev/null -L "https://${API_DOMAIN}"

# TLS certificate chain summary
# Note: will hang if SNI mismatch; we pass -servername.
run bash -lc "echo | openssl s_client -servername ${ROOT_DOMAIN} -connect ${ROOT_DOMAIN}:443 2>/dev/null | openssl x509 -noout -subject -issuer -dates -ext subjectAltName"

# IP + reverse DNS (best-effort)
IPV4_ROOT="$(dig +short "${ROOT_DOMAIN}" A | head -n1 || true)"
if [[ -n "${IPV4_ROOT}" ]]; then
  echo "${IPV4_ROOT}" > "${OUTDIR}/root_ipv4.txt"
  run dig +noall +answer -x "${IPV4_ROOT}"
fi

log "\nWrote: ${OUTDIR}"
log "Tip: compare 'server:' and other headers; 'Google Frontend' often implies a Google HTTPS LB/GFE edge."
