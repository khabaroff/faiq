#!/usr/bin/env bash
# dispatch-proch.sh — отправляет /прочь в JUNIOR и SENIOR одновременно
set -euo pipefail

PROJECT_ROOT="/Users/khabaroff/GOO_LIBARCH/guides"
COMMAND="cd $PROJECT_ROOT && bash scripts/proch.sh"

SENIOR_SURFACE="surface:11"
JUNIOR_SURFACE="surface:12"
WORKSPACE="workspace:5"

echo "========================================"
echo "   📤 ОТПРАВКА /прочь В ПАНЕЛИ"
echo "========================================"
echo ""
echo "SENIOR:  $SENIOR_SURFACE (FW-GLM-5)"
echo "JUNIOR:  $JUNIOR_SURFACE (Kimi K2.6)"
echo ""

# Прервать возможные зависшие процессы
echo "[1/4] Прерывание текущих процессов..."
cmux send-key --workspace $WORKSPACE --surface $SENIOR_SURFACE ctrl+c 2>/dev/null || true
sleep 0.5
cmux send-key --workspace $WORKSPACE --surface $SENIOR_SURFACE ctrl+c 2>/dev/null || true
cmux send-key --workspace $WORKSPACE --surface $JUNIOR_SURFACE ctrl+c 2>/dev/null || true
sleep 0.5
cmux send-key --workspace $WORKSPACE --surface $JUNIOR_SURFACE ctrl+c 2>/dev/null || true
sleep 1

# Отправить команду
echo "[2/4] Отправка команды в SENIOR..."
cmux send --workspace $WORKSPACE --surface $SENIOR_SURFACE "$COMMAND"
cmux send-key --workspace $WORKSPACE --surface $SENIOR_SURFACE Enter

echo "[3/4] Отправка команды в JUNIOR..."
cmux send --workspace $WORKSPACE --surface $JUNIOR_SURFACE "$COMMAND"
cmux send-key --workspace $WORKSPACE --surface $JUNIOR_SURFACE Enter

echo "[4/4] Ожидание выполнения (5 сек)..."
sleep 5

echo ""
echo "========================================"
echo "   📥 РЕЗУЛЬТАТ SENIOR"
echo "========================================"
cmux read-screen --workspace $WORKSPACE --surface $SENIOR_SURFACE --lines 60

echo ""
echo "========================================"
echo "   📥 РЕЗУЛЬТАТ JUNIOR"
echo "========================================"
cmux read-screen --workspace $WORKSPACE --surface $JUNIOR_SURFACE --lines 60

echo ""
echo "========================================"
echo "   ✅ /прочь ЗАВЕРШЁН"
echo "========================================"
