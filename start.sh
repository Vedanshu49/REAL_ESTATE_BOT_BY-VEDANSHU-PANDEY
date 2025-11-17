#!/bin/bash
# Real Estate AI Bot - Quick Start Guide

echo "🚀 Starting Real Estate AI Bot..."
echo ""

# Backend
cd backend
python manage.py runserver 0.0.0.0:8000 &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"
sleep 2

# Frontend
cd ../frontend
npm run dev &
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID)"

echo ""
echo "🌐 Open: http://localhost:5173"
echo "📊 Backend: http://localhost:8000/api/"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

wait
