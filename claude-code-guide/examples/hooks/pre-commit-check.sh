#!/bin/bash

# Hook: Pre-Commit Quality Check
# Ejecuta antes de crear commits para validar calidad del código

set -e

echo "🔍 Running pre-commit checks..."

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're actually committing
if [[ ! $CLAUDE_USER_MESSAGE == *"commit"* ]]; then
    exit 0
fi

echo -e "${YELLOW}Detected commit request. Running checks...${NC}"

# 1. Linter
echo "📝 Running linter..."
if command -v eslint &> /dev/null; then
    if ! eslint . --max-warnings 0; then
        echo -e "${RED}❌ Linter failed. Fix errors before committing.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Linter passed${NC}"
fi

# 2. Type check
echo "🔎 Running type check..."
if [ -f "tsconfig.json" ]; then
    if ! npx tsc --noEmit; then
        echo -e "${RED}❌ Type check failed.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Type check passed${NC}"
fi

# 3. Tests
echo "🧪 Running tests..."
if [ -f "package.json" ]; then
    if npm test 2>/dev/null; then
        echo -e "${GREEN}✅ Tests passed${NC}"
    else
        echo -e "${YELLOW}⚠️  Some tests failed. Review before committing.${NC}"
    fi
fi

# 4. Check for console.log
echo "🔍 Checking for console.log..."
if git diff --cached | grep -E "console\.(log|debug|info)" > /dev/null; then
    echo -e "${YELLOW}⚠️  Found console.log statements. Consider removing them.${NC}"
fi

# 5. Check for TODO/FIXME
echo "📌 Checking for TODO/FIXME..."
TODO_COUNT=$(git diff --cached | grep -c -E "(TODO|FIXME)" || true)
if [ $TODO_COUNT -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Found $TODO_COUNT TODO/FIXME comments${NC}"
fi

# 6. Security check
echo "🔒 Running security check..."
if command -v npm &> /dev/null; then
    npm audit --audit-level=high 2>/dev/null || echo -e "${YELLOW}⚠️  Security vulnerabilities found${NC}"
fi

echo -e "${GREEN}✅ All pre-commit checks passed!${NC}"
