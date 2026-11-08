#!/usr/bin/env bash

# SDCU Universal Skill Installer
# Installs SDCU skills into your favorite AI coding assistant

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$REPO_DIR/skills"

echo "=================================================="
echo "          SDCU Skills Universal Installer         "
echo "  (System Design · Context Graph · UI Craft)      "
echo "=================================================="

install_antigravity() {
    local target="$HOME/.gemini/config/skills"
    echo "Installing SDCU skills for Antigravity in $target..."
    mkdir -p "$target"
    cp -r "$SKILLS_DIR"/* "$target/"
    echo "✅ Antigravity skills installed successfully!"
}

install_claude() {
    local target="$HOME/.claude/skills"
    echo "Installing SDCU skills for Claude Code in $target..."
    mkdir -p "$target"
    cp -r "$SKILLS_DIR"/* "$target/"
    echo "✅ Claude Code skills installed successfully!"
}

install_cursor() {
    local target="$PWD/.cursor/rules"
    echo "Installing SDCU rules for Cursor in $target..."
    mkdir -p "$target"
    cp "$SKILLS_DIR/sdcu/SKILL.md" "$target/sdcu.mdc"
    cp "$SKILLS_DIR/sdcu-sd/SKILL.md" "$target/sdcu-sd.mdc"
    cp "$SKILLS_DIR/sdcu-c/SKILL.md" "$target/sdcu-c.mdc"
    cp "$SKILLS_DIR/sdcu-u/SKILL.md" "$target/sdcu-u.mdc"
    echo "✅ Cursor rules installed in current workspace!"
}

case "$1" in
    --claude)
        install_claude
        ;;
    --antigravity)
        install_antigravity
        ;;
    --cursor)
        install_cursor
        ;;
    --all|"")
        install_antigravity
        install_claude
        install_cursor
        ;;
    *)
        echo "Usage: $0 [--antigravity | --claude | --cursor | --all]"
        exit 1
        ;;
esac

echo "=================================================="
echo "Installation complete! Try running /sdcu in chat."
echo "=================================================="
