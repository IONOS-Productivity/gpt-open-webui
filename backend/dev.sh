PORT="${PORT:-8080}"

if [ -z "$RUN_MIGRATIONS" ] || [ "$RUN_MIGRATIONS" = "true" ]; then
  # if custom_resource_loader script exists, run it
  if [ -f "custom_resource_loader.py" ]; then
    echo "Running maintenance script"
    python custom_resource_loader.py
  else
    echo "custom_resource_loader not found"
  fi
else
  echo "RUN_MIGRATIONS is either not set or set to false, skipping migrations."
fi

uvicorn open_webui.main:app --port $PORT --host 0.0.0.0 --forwarded-allow-ips '*' --reload