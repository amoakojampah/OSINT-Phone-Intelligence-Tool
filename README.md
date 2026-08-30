# 🔍 OSINT Phone Intelligence Tool

**Advanced Open Source Intelligence (OSINT) tool for deep phone number analysis, domain investigation, and email tracking with multi-API integration.**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Kali](https://img.shields.io/badge/OS-Kali_Linux-black.svg)](https://www.kali.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey.svg)](https://www.linux.org/)

## 🌟 Features

### 📱 Phone Number Intelligence
- **Carrier Detection** - Identify mobile network operators (MTN, Vodafone, etc.)
- **Geolocation** - Country, region, and timezone information
- **Number Validation** - Check if number is valid and possible
- **Number Type** - Mobile, landline, VoIP, toll-free, premium rate
- **Pattern Analysis** - Repeated digits, sequential patterns, palindromes
- **Spam Database Check** - Cross-reference with known spam numbers
- **Messaging Apps** - Check WhatsApp, Telegram, Signal, Viber presence
- **Social Media** - Generate search links for Facebook, Twitter, LinkedIn

### 🌐 Domain & IP Analysis
- **WHOIS Lookup** - Registrar, creation date, expiration, name servers
- **DNS Records** - A, AAAA, MX, NS, TXT, SOA, CNAME
- **IP Geolocation** - Country, region, city, ISP, organization
- **Reverse DNS** - Hostname resolution
- **Port Scanning** - 14 common ports with service banner detection
- **Subdomain Enumeration** - Find subdomains with custom wordlist

### 📧 Email Investigation
- **Domain Verification** - Check if email domain is active
- **Disposable Email Detection** - Identify temporary email providers
- **WHOIS Information** - Domain creation date and registrar

### 🔌 Multi-API Integration
- **NumVerify** - Comprehensive phone validation
- **AbstractAPI** - Phone number intelligence
- **Veriphone** - Advanced phone verification
- **OVH** - Free phone validation

## 🚀 Quick Start

### Installation

# Clone your repository
git clone https://github.com/amoakojampah/OSINT-Phone-Intelligence-Tool
cd OSINT-Phone-Intelligence-Tool

# Set up virtual environment
python3 -m venv osint_env
source osint_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make executable
chmod +x OSINT-Phone-Intelligence-Tool.py

###💡 Simple Usage Examples
# Deep phone number search (Ghana number example)
./OSINT-Phone-Intelligence-Tool.py -t +233593332092

# Domain investigation
./OSINT-Phone-Intelligence-Tool.py -t example.com

# Email analysis
./OSINT-Phone-Intelligence-Tool.py -t user@example.com

# Save results to a JSON file
./OSINT-Phone-Intelligence-Tool.py -t +233593332092 --output results.json

###🎯 Use Cases
    # Security Research - Investigate unknown callers

  #Penetration Testing - Reconnaissance and intelligence gathering

  #  Fraud Prevention - Verify phone numbers and emails

  #  Background Checks - Validate contact information

   # OSINT Investigations - Open source intelligence gathering
