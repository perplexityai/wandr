#!/usr/bin/env bash
set -uo pipefail

tests_dir="${TESTS_DIR:-/tests}"
logs_dir="${LOGS_DIR:-/logs/verifier}"
workspace_dir="${WORKSPACE_DIR:-/workspace}"
task_dir="${WANDR_TASK_DIR:-${tests_dir}/wandr_task}"
instruction_path="${WANDR_INSTRUCTION_PATH:-${tests_dir}/../instruction.md}"
output_dir="${WANDR_OUTPUT_DIR:-${logs_dir}/wandr}"
setup_log="${logs_dir}/setup.log"
uv_bootstrap_log="${logs_dir}/uv-bootstrap.log"
verifier_python="${WANDR_VERIFIER_PYTHON:-}"

artifact() {
  python "${tests_dir}/artifacts.py" "$@" 2>> "${setup_log}"
}

finish_error() {
  artifact fail "${logs_dir}" "$1" || exit 1
  exit 1
}

with_log_tail() {
  local message="$1"
  local path="$2"
  if [[ ! -s "${path}" ]]; then
    printf "%s" "${message}"
    return
  fi
  printf "%s\n\nLast log lines from %s:\n" "${message}" "${path}"
  tail -n 20 "${path}"
}

mkdir -p "${logs_dir}" 2>/dev/null || exit 1
: > "${setup_log}" || exit 1
rm -f "${uv_bootstrap_log}" 2>> "${setup_log}" \
  || finish_error "uv bootstrap log cleanup failed; see setup.log"
artifact clear "${logs_dir}" || finish_error "artifact cleanup failed; see setup.log"
rm -f "${logs_dir}/.complete" 2>> "${setup_log}" \
  || finish_error "completion marker cleanup failed; see setup.log"
mkdir -p "${workspace_dir}" "${output_dir}" 2>> "${setup_log}" \
  || finish_error "setup directory creation failed; see setup.log"
export WANDR_LOG_DIR="${WANDR_LOG_DIR:-${output_dir}}"
export WANDR_STDIO_LOG_PATH="${WANDR_STDIO_LOG_PATH:-${WANDR_LOG_DIR}/stdio.log}"
mkdir -p "$(dirname "${WANDR_STDIO_LOG_PATH}")" 2>> "${setup_log}" \
  || finish_error "stdio log directory creation failed; see setup.log"
exec 3>&1 || finish_error "public stdout fd preservation failed; see setup.log"
exec 4>&2 || finish_error "public stderr fd preservation failed; see setup.log"
export WANDR_PUBLIC_STDOUT_FD=3
export WANDR_PUBLIC_STDERR_FD=4

if [[ -n "${verifier_python}" ]]; then
  if [[ ! -x "${verifier_python}" ]]; then
    finish_error "verifier python is not executable at ${verifier_python}; unset WANDR_VERIFIER_PYTHON to use locked uv sync"
  fi
elif ! command -v uv >/dev/null 2>&1; then
  if ! python -m pip install --quiet --no-cache-dir uv > "${uv_bootstrap_log}" 2>&1; then
    finish_error "uv bootstrap failed; see uv-bootstrap.log"
  fi
fi

export WANDR_TASK_DIR="${task_dir}"
export UV_PROJECT_ENVIRONMENT="${UV_PROJECT_ENVIRONMENT:-/tmp/.venv-wandr-core}"
export UV_LINK_MODE="${UV_LINK_MODE:-copy}"
export UV_HTTP_TIMEOUT="${UV_HTTP_TIMEOUT:-120}"
export UV_HTTP_RETRIES="${UV_HTTP_RETRIES:-8}"
export UV_CONCURRENT_DOWNLOADS="${UV_CONCURRENT_DOWNLOADS:-4}"
if [[ -d /uv-cache && -z "${UV_CACHE_DIR:-}" ]]; then
  export UV_CACHE_DIR=/uv-cache
fi
cd "${tests_dir}/wandr_core" 2>> "${setup_log}" \
  || finish_error "wandr_core directory missing; see setup.log"
export PYTHONPATH="${tests_dir}/wandr_core${PYTHONPATH:+:${PYTHONPATH}}"
verify_args=(
  --workspace-dir "${workspace_dir}"
  --task-dir "${task_dir}"
  --output-dir "${output_dir}"
)
if [[ -f "${instruction_path}" ]]; then
  verify_args+=(--instruction-path "${instruction_path}")
fi
if [[ -n "${verifier_python}" ]]; then
  verifier_status=0
  "${verifier_python}" "${tests_dir}/verify.py" \
    "${verify_args[@]}" \
    > "${WANDR_STDIO_LOG_PATH}" 2>&1 || verifier_status=$?
else
  unset UV_EXCLUDE_NEWER
  verifier_status=0
  uv --no-config run --locked --project "${tests_dir}/wandr_core" python "${tests_dir}/verify.py" \
    "${verify_args[@]}" \
    > "${WANDR_STDIO_LOG_PATH}" 2>&1 || verifier_status=$?
fi
if [[ "${verifier_status}" -ne 0 ]]; then
  if artifact has-error "${logs_dir}"; then
    with_log_tail "verification failed; see ${logs_dir}/error.json" "${WANDR_STDIO_LOG_PATH}" >&4
    exit 1
  fi
  finish_error "$(with_log_tail "verification failed before verifier wrote error.json" "${WANDR_STDIO_LOG_PATH}")"
fi

{
  printf "\nWANDR report paths:\n"
  printf "  HTML: %s\n" "${logs_dir}/report.html"
  printf "  Text: %s\n" "${logs_dir}/report.txt"
  printf "  Metrics: %s\n" "${logs_dir}/wandr_metrics.json"
  printf "  Diagnostics: %s\n" "${logs_dir}/wandr-details.json"
  printf "  Debug: %s\n" "${output_dir}/debug"
} >&3
: > "${logs_dir}/.complete" || finish_error "completion marker write failed; see setup.log"

exit 0
