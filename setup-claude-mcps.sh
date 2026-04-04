#!/bin/bash
# setup-claude-mcps.sh
# Configures Claude Desktop MCPs on macOS
# Run this script on your Mac terminal: bash setup-claude-mcps.sh

set -e

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BOLD}=== Claude Desktop MCP Setup ===${NC}"
echo ""

# --- Step 1: Check Node.js and npx ---
echo -e "${BOLD}[1/7] Checking Node.js and npx...${NC}"

if ! command -v node &>/dev/null; then
  echo -e "${YELLOW}Node.js not found. Installing via Homebrew...${NC}"
  if ! command -v brew &>/dev/null; then
    echo -e "${RED}Homebrew not found. Installing Homebrew first...${NC}"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  fi
  brew install node
else
  echo -e "${GREEN}Node.js found: $(node --version)${NC}"
fi

if ! command -v npx &>/dev/null; then
  echo -e "${RED}npx not found even after Node install. Please check your PATH.${NC}"
  exit 1
else
  echo -e "${GREEN}npx found: $(npx --version)${NC}"
fi

# --- Step 2: Detect real home directory ---
echo ""
echo -e "${BOLD}[2/7] Detecting home directory...${NC}"
USER_HOME="$HOME"
echo -e "${GREEN}Home: $USER_HOME${NC}"

# --- Step 3: Ensure Claude Desktop config directory exists ---
echo ""
echo -e "${BOLD}[3/7] Ensuring Claude Desktop config directory exists...${NC}"
CLAUDE_CONFIG_DIR="$USER_HOME/Library/Application Support/Claude"
CLAUDE_CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"

mkdir -p "$CLAUDE_CONFIG_DIR"
echo -e "${GREEN}Directory ready: $CLAUDE_CONFIG_DIR${NC}"

# --- Step 4: Read existing config or start fresh ---
echo ""
echo -e "${BOLD}[4/7] Reading existing config...${NC}"

if [ -f "$CLAUDE_CONFIG_FILE" ]; then
  echo -e "${GREEN}Existing config found. Merging MCPs...${NC}"
  # Backup existing config
  cp "$CLAUDE_CONFIG_FILE" "$CLAUDE_CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
  echo -e "${YELLOW}Backup created at: $CLAUDE_CONFIG_FILE.backup.*${NC}"
else
  echo -e "${YELLOW}No existing config. Creating new one.${NC}"
fi

# --- Step 5: Write config with all MCPs ---
echo ""
echo -e "${BOLD}[5/7] Writing MCP configuration...${NC}"

cat > "$CLAUDE_CONFIG_FILE" << JSONEOF
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "$USER_HOME/Desktop",
        "$USER_HOME/Documents",
        "$USER_HOME/Downloads",
        "$USER_HOME"
      ]
    },
    "fetch": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-fetch"
      ]
    },
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    },
    "playwright": {
      "command": "npx",
      "args": [
        "-y",
        "@playwright/mcp@latest"
      ]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sequential-thinking"
      ]
    },
    "github": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "SUBSTITUIR_PELO_SEU_TOKEN"
      }
    }
  }
}
JSONEOF

echo -e "${GREEN}Config written successfully.${NC}"

# --- Step 6: Validate JSON ---
echo ""
echo -e "${BOLD}[6/7] Validating JSON...${NC}"

if python3 -m json.tool "$CLAUDE_CONFIG_FILE" > /dev/null 2>&1; then
  echo -e "${GREEN}JSON is valid!${NC}"
else
  echo -e "${RED}JSON validation failed! Check the file manually:${NC}"
  echo "  $CLAUDE_CONFIG_FILE"
  exit 1
fi

# --- Step 7: Show final file ---
echo ""
echo -e "${BOLD}[7/7] Final config file contents:${NC}"
echo -e "${YELLOW}File: $CLAUDE_CONFIG_FILE${NC}"
echo "---"
cat "$CLAUDE_CONFIG_FILE"
echo "---"

# --- Summary ---
echo ""
echo -e "${BOLD}=== Setup Complete! ===${NC}"
echo ""
echo -e "${BOLD}MCPs configured:${NC}"
echo -e "  ${GREEN}filesystem${NC}         - Read/write files in Desktop, Documents, Downloads, Home"
echo -e "  ${GREEN}fetch${NC}              - Real-time web access"
echo -e "  ${GREEN}memory${NC}             - Persistent memory between sessions"
echo -e "  ${GREEN}playwright${NC}         - Browser automation"
echo -e "  ${GREEN}sequential-thinking${NC} - Structured step-by-step reasoning"
echo -e "  ${YELLOW}github${NC}             - GitHub integration (NEEDS TOKEN - see below)"
echo ""
echo -e "${BOLD}${RED}ACTION REQUIRED - Manual configuration needed:${NC}"
echo ""
echo -e "  ${YELLOW}GitHub MCP:${NC}"
echo "    1. Go to: https://github.com/settings/tokens"
echo "    2. Click 'Generate new token (classic)'"
echo "    3. Select scopes: repo, read:org, read:user"
echo "    4. Copy the token"
echo "    5. Open: $CLAUDE_CONFIG_FILE"
echo "    6. Replace  SUBSTITUIR_PELO_SEU_TOKEN  with your token"
echo ""
echo -e "${BOLD}${GREEN}Restart Claude Desktop for changes to take effect!${NC}"
echo ""
echo "  Mac: Cmd+Q to quit Claude Desktop, then reopen it."
