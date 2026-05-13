cat > /etc/systemd/system/bandeo.service << 'EOF'
[Unit]
Description=Bandeo
After=network.target

[Service]
WorkingDirectory=/opt/bandeo
ExecStart=/opt/bandeo/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable bandeo
systemctl start bandeo
sleep 2
systemctl status bandeo --no-pager
