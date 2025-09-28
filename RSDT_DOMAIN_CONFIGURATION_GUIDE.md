# RSDT DOMAIN CONFIGURATION GUIDE
## Complete Guide for Setting Up Your Domain with RSDT Blockchain

---

## 🌐 **DOMAIN SETUP OVERVIEW**

This guide will help you configure your domain to work with the RSDT blockchain services running on your Ubuntu 24 VM.

### Services to Configure:
- **Blockchain Explorer**: `explorer.yourdomain.com`
- **Mining Pool**: `pool.yourdomain.com`
- **RPC API**: `api.yourdomain.com`
- **Main Website**: `yourdomain.com`

---

## 🔧 **DNS CONFIGURATION**

### 1.1 DNS Records Setup

**A Records (IPv4):**
```
yourdomain.com          A    YOUR_VM_IP
www.yourdomain.com      A    YOUR_VM_IP
explorer.yourdomain.com A    YOUR_VM_IP
pool.yourdomain.com     A    YOUR_VM_IP
api.yourdomain.com      A    YOUR_VM_IP
```

**CNAME Records (if using subdomains):**
```
www     CNAME   yourdomain.com
explorer CNAME  yourdomain.com
pool    CNAME   yourdomain.com
api     CNAME   yourdomain.com
```

### 1.2 DNS Propagation

**Check DNS propagation:**
```bash
# Check A record
dig yourdomain.com A
dig explorer.yourdomain.com A
dig pool.yourdomain.com A
dig api.yourdomain.com A

# Check from different locations
nslookup yourdomain.com 8.8.8.8
nslookup yourdomain.com 1.1.1.1
```

**Wait for propagation (usually 5-30 minutes)**

---

## 🔒 **SSL CERTIFICATE SETUP**

### 2.1 Install Certbot

```bash
# Install Certbot
sudo apt update
sudo apt install -y certbot python3-certbot-nginx

# Or install snap version
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

### 2.2 Install Nginx

```bash
# Install Nginx
sudo apt install -y nginx

# Start and enable Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Check status
sudo systemctl status nginx
```

### 2.3 Configure Nginx

#### 2.3.1 Main Website Configuration

```bash
# Create main website config
sudo tee /etc/nginx/sites-available/yourdomain.com <<EOF
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    location / {
        return 301 https://\$server_name\$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    root /var/www/yourdomain.com;
    index index.html;
    
    location / {
        try_files \$uri \$uri/ =404;
    }
}
EOF
```

#### 2.3.2 Blockchain Explorer Configuration

```bash
# Create explorer config
sudo tee /etc/nginx/sites-available/explorer.yourdomain.com <<EOF
server {
    listen 80;
    server_name explorer.yourdomain.com;
    
    location / {
        return 301 https://\$server_name\$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name explorer.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/explorer.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/explorer.yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
```

#### 2.3.3 Mining Pool Configuration

```bash
# Create pool config
sudo tee /etc/nginx/sites-available/pool.yourdomain.com <<EOF
server {
    listen 80;
    server_name pool.yourdomain.com;
    
    location / {
        return 301 https://\$server_name\$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name pool.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/pool.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/pool.yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://127.0.0.1:3333;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
```

#### 2.3.4 RPC API Configuration

```bash
# Create API config
sudo tee /etc/nginx/sites-available/api.yourdomain.com <<EOF
server {
    listen 80;
    server_name api.yourdomain.com;
    
    location / {
        return 301 https://\$server_name\$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://127.0.0.1:18081;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
```

### 2.4 Enable Sites

```bash
# Enable all sites
sudo ln -s /etc/nginx/sites-available/yourdomain.com /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/explorer.yourdomain.com /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/pool.yourdomain.com /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/api.yourdomain.com /etc/nginx/sites-enabled/

# Test Nginx configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

---

## 🔐 **SSL CERTIFICATE GENERATION**

### 3.1 Generate Certificates

```bash
# Generate certificate for main domain
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Generate certificate for explorer
sudo certbot --nginx -d explorer.yourdomain.com

# Generate certificate for pool
sudo certbot --nginx -d pool.yourdomain.com

# Generate certificate for API
sudo certbot --nginx -d api.yourdomain.com
```

### 3.2 Auto-renewal Setup

```bash
# Test auto-renewal
sudo certbot renew --dry-run

# Add to crontab for automatic renewal
(crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -
```

---

## 🌐 **WEBSITE SETUP**

### 4.1 Create Main Website

```bash
# Create website directory
sudo mkdir -p /var/www/yourdomain.com
sudo chown -R $USER:$USER /var/www/yourdomain.com

# Create main page
cat > /var/www/yourdomain.com/index.html <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RSDT - Resistance Blockchain</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .logo { text-align: center; font-family: monospace; font-size: 24px; margin-bottom: 30px; }
        .services { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 30px; }
        .service { padding: 20px; border: 1px solid #ddd; border-radius: 5px; text-align: center; }
        .service h3 { color: #3498db; margin-top: 0; }
        .service a { color: #2c3e50; text-decoration: none; font-weight: bold; }
        .service a:hover { color: #3498db; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            ██████╗ ███████╗██████╗ ████████╗<br>
            ██╔══██╗██╔════╝██╔══██╗╚══██╔══╝<br>
            ██████╔╝███████╗██║  ██║   ██║<br>
            ██╔══██╗╚════██║██║  ██║   ██║<br>
            ██║  ██║███████║██████╔╝   ██║<br>
            ╚═╝  ╚═╝╚══════╝╚═════╝    ╚═╝
        </div>
        
        <h1 style="text-align: center; color: #2c3e50;">Resistance Blockchain (RSDT)</h1>
        <p style="text-align: center; font-size: 18px; color: #7f8c8d;">Privacy • Freedom • Resistance</p>
        
        <div class="services">
            <div class="service">
                <h3>Blockchain Explorer</h3>
                <p>Explore blocks, transactions, and addresses</p>
                <a href="https://explorer.yourdomain.com">explorer.yourdomain.com</a>
            </div>
            
            <div class="service">
                <h3>Mining Pool</h3>
                <p>Join our mining pool and earn RSDT</p>
                <a href="https://pool.yourdomain.com">pool.yourdomain.com</a>
            </div>
            
            <div class="service">
                <h3>RPC API</h3>
                <p>Access blockchain data via API</p>
                <a href="https://api.yourdomain.com">api.yourdomain.com</a>
            </div>
        </div>
        
        <div style="margin-top: 40px; text-align: center; color: #7f8c8d;">
            <p><strong>Genesis Message:</strong> "Censorship is control; privacy is resistance"</p>
            <p><strong>Network ID:</strong> 0x1230F171610441611731008216A1A110</p>
            <p><strong>Total Supply:</strong> 200M RSDT | <strong>Premine:</strong> 20M RSDT (10%)</p>
        </div>
    </div>
</body>
</html>
EOF
```

---

## 🔧 **SERVICE CONFIGURATION UPDATES**

### 5.1 Update RSDT Services

#### 5.1.1 Update Blockchain Explorer

```bash
# Update explorer to bind to localhost only
sudo systemctl edit rsdt-explorer

# Add override configuration
[Service]
ExecStart=
ExecStart=/usr/bin/python3 /opt/rsdt/explorer/rsdt_blockchain_explorer.py --host=127.0.0.1 --port=8080

# Restart service
sudo systemctl restart rsdt-explorer
```

#### 5.1.2 Update Mining Pool

```bash
# Update pool configuration
sudo tee -a /opt/rsdt/config/pool_config.json <<EOF
{
    "daemon_url": "http://127.0.0.1:18081",
    "pool_fee": 1.0,
    "min_payout": 0.1,
    "database": "/opt/rsdt/data/rsdt_pool.db",
    "pool_address": "4A64wDfoaR6Lf1CGww4KanRZXbwrzXFFfE7wjtwvtZu8gVWEyYHzgbpAPiBra5UR5HCjcEFufBMZLRcHj3BCXLfuNf9Sn4N",
    "pool_port": 3333,
    "api_port": 8080,
    "bind_host": "127.0.0.1"
}
EOF

# Restart pool service
sudo systemctl restart rsdt-pool
```

---

## 🧪 **TESTING AND VERIFICATION**

### 6.1 Test Domain Access

```bash
# Test main website
curl -I https://yourdomain.com
curl -I https://www.yourdomain.com

# Test explorer
curl -I https://explorer.yourdomain.com

# Test pool
curl -I https://pool.yourdomain.com

# Test API
curl -s https://api.yourdomain.com/json_rpc -d '{"jsonrpc":"2.0","id":"0","method":"get_info"}' | head -5
```

### 6.2 SSL Certificate Verification

```bash
# Check certificate details
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com < /dev/null 2>/dev/null | openssl x509 -noout -dates

# Test SSL Labs (external)
echo "Visit: https://www.ssllabs.com/ssltest/analyze.html?d=yourdomain.com"
```

### 6.3 Service Integration Test

```bash
# Test explorer through domain
curl -s https://explorer.yourdomain.com/api/stats

# Test pool through domain
curl -s https://pool.yourdomain.com/api/stats

# Test API through domain
curl -s https://api.yourdomain.com/json_rpc -d '{"jsonrpc":"2.0","id":"0","method":"get_info"}'
```

---

## 🔍 **MONITORING AND LOGS**

### 7.1 Nginx Logs

```bash
# Access logs
sudo tail -f /var/log/nginx/access.log

# Error logs
sudo tail -f /var/log/nginx/error.log

# Site-specific logs
sudo tail -f /var/log/nginx/yourdomain.com.access.log
sudo tail -f /var/log/nginx/explorer.yourdomain.com.access.log
```

### 7.2 SSL Certificate Monitoring

```bash
# Check certificate expiration
sudo certbot certificates

# Monitor renewal
sudo journalctl -u certbot.timer -f
```

---

## 🚨 **TROUBLESHOOTING**

### 8.1 Common Issues

#### 8.1.1 DNS Not Resolving

```bash
# Check DNS resolution
dig yourdomain.com A
nslookup yourdomain.com

# Check from different DNS servers
nslookup yourdomain.com 8.8.8.8
nslookup yourdomain.com 1.1.1.1
```

#### 8.1.2 SSL Certificate Issues

```bash
# Check certificate status
sudo certbot certificates

# Renew certificate manually
sudo certbot renew --force-renewal -d yourdomain.com

# Check Nginx SSL configuration
sudo nginx -t
```

#### 8.1.3 Service Not Accessible

```bash
# Check service status
sudo systemctl status rsdtd rsdt-pool rsdt-explorer

# Check port binding
sudo netstat -tlnp | grep -E "(8080|3333|18081)"

# Check firewall
sudo ufw status
```

#### 8.1.4 Nginx Configuration Issues

```bash
# Test Nginx configuration
sudo nginx -t

# Check Nginx status
sudo systemctl status nginx

# View Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

---

## 📋 **DEPLOYMENT CHECKLIST**

- [ ] Domain DNS records configured
- [ ] DNS propagation verified
- [ ] Nginx installed and configured
- [ ] SSL certificates generated
- [ ] All subdomains configured
- [ ] Main website created
- [ ] Services updated for domain access
- [ ] SSL auto-renewal configured
- [ ] All services tested through domain
- [ ] Monitoring and logging setup
- [ ] Troubleshooting procedures documented

---

## 🎯 **FINAL VERIFICATION**

### 9.1 Complete System Test

```bash
# Test all services through domain
echo "Testing main website..."
curl -I https://yourdomain.com

echo "Testing explorer..."
curl -I https://explorer.yourdomain.com

echo "Testing pool..."
curl -I https://pool.yourdomain.com

echo "Testing API..."
curl -s https://api.yourdomain.com/json_rpc -d '{"jsonrpc":"2.0","id":"0","method":"get_info"}' | head -5

echo "All tests completed!"
```

### 9.2 External Access Test

```bash
# Test from external machine
echo "Visit these URLs in your browser:"
echo "Main Website: https://yourdomain.com"
echo "Explorer: https://explorer.yourdomain.com"
echo "Pool: https://pool.yourdomain.com"
echo "API: https://api.yourdomain.com"
```

---

## 🚀 **NEXT STEPS**

1. **Content Management**: Add more content to main website
2. **Analytics**: Set up Google Analytics or similar
3. **CDN**: Configure CloudFlare or similar CDN
4. **Backup**: Set up automated backups
5. **Monitoring**: Implement comprehensive monitoring
6. **Security**: Add additional security headers and measures

**Your RSDT blockchain is now fully accessible through your domain!** 🎉

**Domain Configuration Complete!** Your RSDT blockchain services are now accessible through your professional domain with SSL encryption.

