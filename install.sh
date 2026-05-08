#!/usr/bin/env bash
# ============================================================
# WSZ Marketing & SEO Skills — One-command installer
# https://github.com/Dangluu1010/WSZ-MKT-and-SEO-skills
#
# Usage:
#   git clone https://github.com/Dangluu1010/WSZ-MKT-and-SEO-skills.git
#   cd WSZ-MKT-and-SEO-skills && ./install.sh
# ============================================================

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

info()    { echo -e "${CYAN}[INFO]${NC}  $*"; }
success() { echo -e "${GREEN}[ OK ]${NC}  $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error()   { echo -e "${RED}[FAIL]${NC}  $*"; exit 1; }
header()  { echo -e "\n${BOLD}$*${NC}"; }

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_SRC="${SCRIPT_DIR}/skills"
SKILLS_DEST="${HOME}/.claude/skills"

echo ""
echo -e "${BOLD}============================================================${NC}"
echo -e "${BOLD}  WSZ Marketing & SEO Skills Installer${NC}"
echo -e "${BOLD}============================================================${NC}"
echo ""

# Verify source skills exist
[ -d "${SKILLS_SRC}" ] || error "skills/ directory not found. Make sure you cloned the full repo."

# ── 1. Node.js ───────────────────────────────────────────────
header "Step 1 — Node.js"

export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
[ -s "$NVM_DIR/nvm.sh" ] && source "$NVM_DIR/nvm.sh"

if command -v node &>/dev/null; then
  success "Node.js $(node --version) already installed"
else
  warn "Node.js not found — installing via nvm..."
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
  export NVM_DIR="$HOME/.nvm"
  source "$NVM_DIR/nvm.sh"
  nvm install --lts
  nvm use --lts
  success "Node.js $(node --version) installed"
fi

# ── 2. Claude Code ───────────────────────────────────────────
header "Step 2 — Claude Code"

if command -v claude &>/dev/null; then
  success "Claude Code already installed"
else
  info "Installing Claude Code..."
  npm install -g @anthropic-ai/claude-code
  export PATH="$(npm config get prefix)/bin:$PATH"
  command -v claude &>/dev/null || error "claude not found after install. Add npm global bin to PATH."
  success "Claude Code installed"
fi

# ── 3. Install Skills (direct file copy) ────────────────────
header "Step 3 — Installing Skills"

mkdir -p "${SKILLS_DEST}"

INSTALLED=0
FAILED=()

for skill_dir in "${SKILLS_SRC}"/*/; do
  skill_name=$(basename "$skill_dir")
  target="${SKILLS_DEST}/${skill_name}"

  if mkdir -p "${target}" && cp -r "${skill_dir}"* "${target}/" 2>/dev/null; then
    success "${skill_name}"
    (( INSTALLED++ )) || true
  else
    warn "Failed to copy: ${skill_name}"
    FAILED+=("${skill_name}")
  fi
done

# ── 4. Python dependencies (for skills that need them) ──────
header "Step 4 — Python Dependencies (optional)"

if command -v python3 &>/dev/null; then
  PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
  success "Python ${PYTHON_VERSION} detected"

  # SEO skill has the main requirements.txt
  SEO_REQ="${SKILLS_DEST}/seo/requirements.txt"
  if [ -f "${SEO_REQ}" ]; then
    info "Installing SEO Python dependencies..."
    VENV_DIR="${SKILLS_DEST}/seo/.venv"
    if python3 -m venv "${VENV_DIR}" 2>/dev/null; then
      "${VENV_DIR}/bin/pip" install --quiet -r "${SEO_REQ}" 2>/dev/null && \
        success "SEO dependencies installed in ${VENV_DIR}" || \
        warn "SEO pip install failed. Run manually: ${VENV_DIR}/bin/pip install -r ${SEO_REQ}"
    else
      warn "Could not create venv. Run: pip install --user -r ${SEO_REQ}"
    fi

    # Playwright browsers (optional, for visual analysis)
    info "Installing Playwright browsers (optional)..."
    if [ -f "${VENV_DIR}/bin/playwright" ]; then
      "${VENV_DIR}/bin/python" -m playwright install chromium 2>/dev/null && \
        success "Playwright chromium installed" || \
        warn "Playwright install failed. Visual analysis will use WebFetch fallback."
    fi
  fi

  # Blog-google skill dependencies
  BLOG_GOOGLE_REQ="${SKILLS_DEST}/blog-google/scripts/requirements.txt"
  if [ -f "${BLOG_GOOGLE_REQ}" ]; then
    info "Installing blog-google Python dependencies..."
    BG_VENV="${SKILLS_DEST}/blog-google/.venv"
    if python3 -m venv "${BG_VENV}" 2>/dev/null; then
      "${BG_VENV}/bin/pip" install --quiet -r "${BLOG_GOOGLE_REQ}" 2>/dev/null && \
        success "blog-google dependencies installed" || \
        warn "blog-google pip install failed."
    fi
  fi

  # Blog-audio skill dependencies
  BLOG_AUDIO_REQ="${SKILLS_DEST}/blog-audio/scripts/requirements.txt"
  if [ -f "${BLOG_AUDIO_REQ}" ]; then
    info "Installing blog-audio Python dependencies..."
    BA_VENV="${SKILLS_DEST}/blog-audio/.venv"
    if python3 -m venv "${BA_VENV}" 2>/dev/null; then
      "${BA_VENV}/bin/pip" install --quiet -r "${BLOG_AUDIO_REQ}" 2>/dev/null && \
        success "blog-audio dependencies installed" || \
        warn "blog-audio pip install failed."
    fi
  fi

  # Blog-notebooklm skill dependencies
  BLOG_NLM_REQ="${SKILLS_DEST}/blog-notebooklm/scripts/requirements.txt"
  if [ -f "${BLOG_NLM_REQ}" ]; then
    info "Installing blog-notebooklm Python dependencies..."
    BN_VENV="${SKILLS_DEST}/blog-notebooklm/.venv"
    if python3 -m venv "${BN_VENV}" 2>/dev/null; then
      "${BN_VENV}/bin/pip" install --quiet -r "${BLOG_NLM_REQ}" 2>/dev/null && \
        success "blog-notebooklm dependencies installed" || \
        warn "blog-notebooklm pip install failed."
    fi
  fi
else
  warn "Python 3 not found. Some skills (seo, blog-google, blog-audio) need Python."
  warn "Install Python 3 and re-run, or install deps manually later."
fi

# ── 5. Summary ───────────────────────────────────────────────
TOTAL=$(find "${SKILLS_SRC}" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')

echo ""
echo -e "${BOLD}============================================================${NC}"
echo -e "${BOLD}  Summary${NC}"
echo -e "${BOLD}============================================================${NC}"
success "Installed: ${INSTALLED} / ${TOTAL} skills"

if [ ${#FAILED[@]} -gt 0 ]; then
  echo ""
  warn "Failed skills:"
  for s in "${FAILED[@]}"; do
    echo "      - $s"
  done
fi

echo ""
echo -e "${BOLD}Next steps:${NC}"
echo "  1. Run:  claude"
echo "  2. Log in with your Anthropic account when prompted"
echo "  3. Use skills as slash commands: /blog, /seo, /market, /ui-ux-pro-max"
echo "  4. Type / in Claude Code to browse all available skills"
echo ""
success "Done!"
