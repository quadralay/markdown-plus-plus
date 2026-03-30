#!/bin/bash
# Bump version in plugin.json and marketplace.json
# Usage: ./scripts/bump-version.sh [patch|minor|major]

set -e

BUMP_TYPE="${1:-patch}"
PLUGIN_JSON="plugins/markdown-plus-plus/.claude-plugin/plugin.json"
MARKETPLACE_JSON=".claude-plugin/marketplace.json"

# Validate bump type
if [[ ! "$BUMP_TYPE" =~ ^(patch|minor|major)$ ]]; then
    echo "Usage: $0 [patch|minor|major]"
    echo "  patch: 1.0.0 -> 1.0.1 (default)"
    echo "  minor: 1.0.0 -> 1.1.0"
    echo "  major: 1.0.0 -> 2.0.0"
    exit 1
fi

# Check dependencies
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed."
    echo "  Install with: apt-get install jq (Debian/Ubuntu) or brew install jq (macOS)"
    exit 1
fi

# Check if files exist
if [[ ! -f "$PLUGIN_JSON" ]]; then
    echo "Error: $PLUGIN_JSON not found"
    exit 1
fi

if [[ ! -f "$MARKETPLACE_JSON" ]]; then
    echo "Error: $MARKETPLACE_JSON not found"
    exit 1
fi

# Get current version
CURRENT=$(jq -r '.version' "$PLUGIN_JSON")
echo "Current version: $CURRENT"

# Validate semver format
if [[ ! "$CURRENT" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Invalid version format: $CURRENT (must be X.Y.Z)"
    exit 1
fi

# Parse version components
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"

# Calculate new version
case $BUMP_TYPE in
    major)
        MAJOR=$((MAJOR + 1))
        MINOR=0
        PATCH=0
        ;;
    minor)
        MINOR=$((MINOR + 1))
        PATCH=0
        ;;
    patch)
        PATCH=$((PATCH + 1))
        ;;
esac

NEW_VERSION="${MAJOR}.${MINOR}.${PATCH}"
echo "New version: $NEW_VERSION ($BUMP_TYPE)"

# Update plugin.json (using unique temp files to avoid race conditions)
tmp_plugin=$(mktemp)
jq --arg v "$NEW_VERSION" '.version = $v' "$PLUGIN_JSON" > "$tmp_plugin" && mv "$tmp_plugin" "$PLUGIN_JSON"

# Update marketplace.json
tmp_marketplace=$(mktemp)
jq --arg v "$NEW_VERSION" '.version = $v' "$MARKETPLACE_JSON" > "$tmp_marketplace" && mv "$tmp_marketplace" "$MARKETPLACE_JSON"

echo "Updated $PLUGIN_JSON"
echo "Updated $MARKETPLACE_JSON"
echo ""
echo "Next steps:"
echo "  git add $PLUGIN_JSON $MARKETPLACE_JSON"
echo "  git commit -m \"chore: bump version to $NEW_VERSION\""
