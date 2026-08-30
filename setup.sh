#!/bin/bash

echo "========================================="
echo "  OSINT Tool - Automated Setup"
echo "========================================="

# Create requirements file
cat > requirements.txt << 'EOF'
requests==2.31.0
dnspython==2.4.2
python-whois==0.8.0
phonenumbers==8.13.25
EOF

# Install Python packages
echo "[+] Installing dependencies..."
pip3 install -r requirements.txt

# Make script executable
chmod +x osint_tool.py

echo "[+] Setup complete!"
echo ""
echo "Usage examples:"
echo "  python3 osint_tool.py -t google.com"
echo "  python3 osint_tool.py -t +233593332092"
echo "  python3 osint_tool.py -t user@email.com"
echo "  python3 osint_tool.py -t 8.8.8.8"
