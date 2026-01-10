PORT="${PORT:-8080}"

if [ "${DEBUGGER_LISTEN}" == "true" ]; then
	echo "Install debugging libs ..."
	pip install pydevd pydevd-pycharm~=243.23654.177
fi

uvicorn open_webui.main:app --port $PORT --host 0.0.0.0 --forwarded-allow-ips '*' --reload
