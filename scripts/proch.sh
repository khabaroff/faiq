#!/usr/bin/env bash
# /прочь — генератор сводки сессии для проекта guides
# Запускается в панелях JUNIOR/SENIOR через cmux dispatch
set -euo pipefail

PROJECT_ROOT="/Users/khabaroff/GOO_LIBARCH/guides"
cd "$PROJECT_ROOT"

echo "========================================"
echo "   📋 СВОДКА СЕССИИ"
echo "   $(date '+%Y-%m-%d %H:%M:%S')"
echo "   $(whoami)@$(hostname)"
echo "========================================"
echo ""

# Git summary
echo "### 🔄 Последние коммиты"
git log --oneline --graph -10 2>/dev/null || echo "(git недоступен)"

echo ""
echo "### 📁 Текущий статус"
git status --short 2>/dev/null || echo "(git статус недоступен)"

echo ""
echo "### 🎯 Задачи beads"
if command -v bd >/dev/null 2>&1; then
    echo "**Готовые к работе:**"
    bd ready 2>/dev/null | head -20 || true
    echo ""
    echo "**В процессе:**"
    bd show --status=in_progress 2>/dev/null | head -20 || true
else
    echo "(beads CLI не найден)"
fi

echo ""
echo "### 📝 Ключевые файлы (изменения за последние коммиты)"
RECENT_FILES=$(git diff --name-only HEAD~3..HEAD 2>/dev/null | head -10)
if [ -n "$RECENT_FILES" ]; then
    for f in $RECENT_FILES; do
        if [ -f "$f" ]; then
            echo ""
            echo "--- $f ---"
            git diff HEAD~1 -- "$f" 2>/dev/null | head -30 || git show HEAD:"$f" 2>/dev/null | head -30 || echo "(файл новый)"
        fi
    done
else
    echo "(нет изменений за последние коммиты)"
fi

echo ""
echo "### 💾 События .beads (последние 5)"
if [ -f .beads/interactions.jsonl ]; then
    tail -5 .beads/interactions.jsonl 2>/dev/null | python3 -c "
import sys, json
for line in sys.stdin:
    try:
        d = json.loads(line)
        ts = d.get('timestamp', '?')
        ev = d.get('event', '?')
        data = str(d.get('data', ''))[:120]
        print(f'  [{ts}] {ev}: {data}')
    except Exception as e:
        print(f'  RAW: {line.strip()[:100]}')
" 2>/dev/null || tail -5 .beads/interactions.jsonl
else
    echo "(.beads/interactions.jsonl не найден)"
fi

echo ""
echo "### 🏁 Завершено: $(date '+%H:%M:%S')"
