# ===========================
# run_reaction_simulation.sh
# Wrapper for running reaction simulation inside its venv
# ===========================

PROJECT_DIR="/home/josh/projects/reaction-etl/src/generator"
VENV_DIR="$PROJECT_DIR/.venv"
PYTHON="$VENV_DIR/bin/python"
SCRIPT="$PROJECT_DIR/main.py"
LOG_DIR="/home/josh/projects/reaction-etl/logs"
LOG="$LOG_DIR/sim.log"
ERR="$LOG_DIR/sim.err"

mkdir -p "$LOG_DIR"
cd "$PROJECT_DIR" || exit 1

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S.%3N')
echo "Simulation started at: [$TIMESTAMP]" >> "$LOG"

source "$VENV_DIR/bin/activate"

$PYTHON "$SCRIPT" >> "$LOG" 2>> "$ERR"
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "Simulation completed at [$(date '+%Y-%m-%d %H:%M:%S.%3N')]" >> $LOG
else
    echo "Simulation started at [$TIMESTAMP] FAILED with exit code $EXIT_CODE" >> "$ERR"
fi

exit $EXIT_CODE
