#!/bin/bash

echo "🚀 RESISTANCE BLOCKCHAIN - ONE-CLICK DEPLOYMENT"
echo "=============================================="
echo

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run as root: sudo ./DEPLOY_EVERYTHING.sh"
    exit 1
fi

echo "📦 Installing dependencies..."
apt update && apt upgrade -y
apt install -y curl wget git nginx mysql-server nodejs npm python3 python3-pip build-essential

echo "🗄️ Setting up database..."
mysql -e "CREATE DATABASE rsdt_pool; CREATE DATABASE rsdt_explorer;"
mysql -e "CREATE USER 'rsdt'@'localhost' IDENTIFIED BY 'password123';"
mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'rsdt'@'localhost'; FLUSH PRIVILEGES;"

echo "🌐 Setting up Nginx..."
cat > /etc/nginx/sites-available/resistance << 'EOF'
server {
    listen 80;
    server_name _;
    
    location / {
        return 200 'Resistance Blockchain is LIVE! Privacy is Resistance!';
        add_header Content-Type text/plain;
    }
}
