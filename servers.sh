#!/bin/bash

# Simple dev runner for backend (FastAPI) and frontend (Next.js)
# Usage: chmod +x servers.sh && ./servers.sh

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Dev Application...${NC}"

# Kill any existing processes on ports 8000 and 3000
echo -e "${YELLOW}Cleaning up existing processes...${NC}"
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

# Helper: choose python
choose_python() {
  if command -v python3 >/dev/null 2>&1; then
    echo python3
  elif command -v python >/dev/null 2>&1; then
    echo python
  else
    echo -e "${RED}Python is not installed. Please install Python 3.11+${NC}"
    exit 1
  fi
}

# Start backend server
echo -e "${GREEN}Starting backend server on port 8000...${NC}"
pushd backend >/dev/null

PY_BIN=$(choose_python)

if [ ! -d "venv" ]; then
  echo -e "${YELLOW}Creating virtual environment...${NC}"
  "$PY_BIN" -m venv venv
fi

# shellcheck disable=SC1091
source venv/bin/activate
pip install -q -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
popd >/dev/null

# Wait a bit for backend to start
sleep 3

# Start frontend server
echo -e "${GREEN}Starting frontend server on port 3000...${NC}"
pushd frontend >/dev/null

# Default API URL for dev if not provided
export NEXT_PUBLIC_API_URL="${NEXT_PUBLIC_API_URL:-http://localhost:8000}"

if command -v npm >/dev/null 2>&1; then
  npm install --silent
  npm run dev -- --port 3000 &
  FRONTEND_PID=$!
else
  echo -e "${RED}npm is not installed. Please install Node.js 20+.${NC}"
  kill "$BACKEND_PID" 2>/dev/null || true
  exit 1
fi

popd >/dev/null

echo -e "${GREEN}Both servers are starting...${NC}"
echo -e "${YELLOW}Backend PID: $BACKEND_PID${NC}"
echo -e "${YELLOW}Frontend PID: $FRONTEND_PID${NC}"
echo ""
echo -e "${GREEN}Access the application at:${NC}"
echo -e "  Frontend: http://localhost:3000"
echo -e "  Backend API: http://localhost:8000"
echo -e "  API Docs: http://localhost:8000/docs"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop both servers${NC}"

# Cleanup on exit
cleanup() {
  echo -e "\n${YELLOW}Stopping servers...${NC}"
  kill "$BACKEND_PID" 2>/dev/null || true
  kill "$FRONTEND_PID" 2>/dev/null || true
  lsof -ti:8000 | xargs kill -9 2>/dev/null || true
  lsof -ti:3000 | xargs kill -9 2>/dev/null || true
  echo -e "${GREEN}Servers stopped.${NC}"
  exit 0
}

trap cleanup INT TERM

wait

