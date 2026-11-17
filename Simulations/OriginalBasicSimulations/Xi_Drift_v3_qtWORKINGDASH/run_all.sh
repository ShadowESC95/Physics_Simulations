#!/bin/bash
set -e

# -------- CONFIG --------
NUM_RANKS=4
PORT=8050
TB_PORT=6006
LATEX_FILE="report.tex"
LATEX_CMD="pdflatex"  # fallback to xelatex if Unicode fails
EMAIL_TO="you@example.com"
WS_LOG="logs/telemetry_ws.log"
DASH_LOG="logs/dash_gui.log"
TB_LOG="logs/tensorboard.log"
# ------------------------

mkdir -p logs output

echo "🔁 Starting Ξχ dual-field simulation (parallel MPI)..."
mpirun -n $NUM_RANKS python3 sim/parallel_launcher.py

echo "📦 Merging simulation logs..."
python3 tools/merge_logs.py || echo "⚠️ Merge skipped or already done."

echo "📈 Generating spiral phase portrait..."
python3 tools/plot_phase_spiral.py || echo "⚠️ Plot skipped or already exists."

echo "📤 Exporting for OpenFOAM + YT..."
python3 data/convert_to_yt.py || echo "⚠️ Export skipped or failed."

# -------- Handle GUI Port Conflict --------
echo "🌐 Checking port $PORT availability..."
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
  PID=$(lsof -t -i:$PORT)
  echo "🛑 Port $PORT is in use by PID $PID, killing it..."
  kill -9 $PID
fi

# -------- Start Dash GUI --------
HOST_IP=$(hostname -I | awk '{print $1}')
echo "🌍 Starting Dash GUI at: http://$HOST_IP:$PORT"
gunicorn app:server --bind 0.0.0.0:$PORT --workers 2 > $DASH_LOG 2>&1 &

# -------- Start WebSocket Telemetry --------
echo "📡 Starting telemetry WebSocket (logs: $WS_LOG)..."
python3 telemetry_ws.py > $WS_LOG 2>&1 &

# -------- Compile LaTeX Report --------
echo "📓 Attempting LaTeX report compilation..."
if ! $LATEX_CMD $LATEX_FILE > /dev/null 2>&1; then
  echo "❌ LaTeX failed — retrying with Unicode-safe fallback (xelatex)..."
  if command -v xelatex > /dev/null; then
    xelatex $LATEX_FILE || echo "❌ xelatex also failed. Check Unicode chars!"
  else
    echo "🚫 xelatex not installed. Try: sudo dnf install texlive-xetex"
  fi
else
  echo "✅ PDF report compiled: ${LATEX_FILE%.tex}.pdf"
fi

# -------- Launch TensorBoard --------
echo "📊 Launching TensorBoard at http://$HOST_IP:$TB_PORT"
tensorboard --logdir logs/ --bind_all --port $TB_PORT > $TB_LOG 2>&1 &

# -------- Email Output (if mutt/mail configured) --------
if command -v mail >/dev/null; then
  echo "Ξχ Simulation Complete — see attached spiral phase plot." \
  | mail -A output/phase_spiral.png -s "Ξχ Sim Report 📬" $EMAIL_TO && echo "📧 Email sent to $EMAIL_TO"
else
  echo "⚠️ 'mail' not found. Install with: sudo dnf install mailx (or mutt)"
fi

# -------- Final Output --------
echo ""
echo "✅ All systems launched successfully!"
echo "🌐 Interfaces:"
echo "   • Dash GUI       → http://$HOST_IP:$PORT"
echo "   • WebSocket WS   → ws://$HOST_IP:8765"
echo "   • TensorBoard    → http://$HOST_IP:$TB_PORT"
echo ""
echo "📁 Output Folder: ./output/"
echo "🧪 Logs Folder:   ./logs/"
