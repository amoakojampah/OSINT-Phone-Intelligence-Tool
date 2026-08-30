#!/usr/bin/env python3
"""
Linux OSINT Tool - Deep Phone Number Search
Enhanced with multiple APIs and comprehensive phone number intelligence
"""

import requests
import socket
import dns.resolver
import whois
import phonenumbers
from phonenumbers import carrier, geocoder, timezone, PhoneNumberType
import json
import sys
import argparse
import os
import time
from datetime import datetime
import re
import subprocess
import hashlib
import base64
from urllib.parse import urlencode

class Color:
    """Terminal colors for better output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

class DeepPhoneSearch:
    """Enhanced phone number intelligence gathering"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9'
        })
        self.results = {}
        self.api_keys = self._load_api_keys()
        
    def _load_api_keys(self):
        """Load API keys from environment or config file"""
        return {
            'numverify': os.getenv('NUMVERIFY_API_KEY', ''),
            'abstractapi': os.getenv('ABSTRACT_API_KEY', ''),
            'veriphone': os.getenv('VERIPHONE_API_KEY', '')
        }
    
    def print_header(self, text):
        print(f"\n{Color.CYAN}{Color.BOLD}═══ {text} ═══{Color.RESET}")
        
    def print_info(self, text):
        print(f"{Color.GREEN}[+] {text}{Color.RESET}")
        
    def print_error(self, text):
        print(f"{Color.RED}[-] Error: {text}{Color.RESET}")
        
    def print_warning(self, text):
        print(f"{Color.YELLOW}[!] Warning: {text}{Color.RESET}")
        
    def print_result(self, key, value):
        print(f"{Color.MAGENTA}{key}:{Color.RESET} {value}")
        
    def print_subresult(self, key, value):
        print(f"  {Color.DIM}├─{Color.RESET} {Color.CYAN}{key}:{Color.RESET} {value}")

class OSINTTool:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
        self.results = {}
        self.deep_search = DeepPhoneSearch()
        
    def print_header(self, text):
        print(f"\n{Color.CYAN}{Color.BOLD}═══ {text} ═══{Color.RESET}")
        
    def print_info(self, text):
        print(f"{Color.GREEN}[+] {text}{Color.RESET}")
        
    def print_error(self, text):
        print(f"{Color.RED}[-] Error: {text}{Color.RESET}")
        
    def print_warning(self, text):
        print(f"{Color.YELLOW}[!] Warning: {text}{Color.RESET}")
        
    def print_result(self, key, value):
        print(f"{Color.MAGENTA}{key}:{Color.RESET} {value}")
        
    def print_subresult(self, key, value):
        print(f"  {Color.DIM}├─{Color.RESET} {Color.CYAN}{key}:{Color.RESET} {value}")

    # ============================================
    # ENHANCED PHONE NUMBER SEARCH
    # ============================================
    
    def get_phone_info_deep(self, phone_number):
        """Deep phone number intelligence gathering"""
        self.print_header(f"DEEP PHONE NUMBER SEARCH: {phone_number}")
        
        results = {}
        
        try:
            # Parse number
            parsed_num = phonenumbers.parse(phone_number, None)
            
            # Basic Information
            self.print_info("Basic Number Information")
            self.print_result("Country Code", f"+{parsed_num.country_code}")
            self.print_result("National Number", parsed_num.national_number)
            
            # Number type
            num_type = phonenumbers.number_type(parsed_num)
            type_names = {
                PhoneNumberType.FIXED_LINE: "Fixed Line",
                PhoneNumberType.MOBILE: "Mobile",
                PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line or Mobile",
                PhoneNumberType.TOLL_FREE: "Toll Free",
                PhoneNumberType.PREMIUM_RATE: "Premium Rate",
                PhoneNumberType.SHARED_COST: "Shared Cost",
                PhoneNumberType.VOIP: "VoIP",
                PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
                PhoneNumberType.PAGER: "Pager",
                PhoneNumberType.UAN: "UAN",
                PhoneNumberType.UNKNOWN: "Unknown"
            }
            self.print_result("Number Type", type_names.get(num_type, "Unknown"))
            
            # Validity
            is_valid = phonenumbers.is_valid_number(parsed_num)
            is_possible = phonenumbers.is_possible_number(parsed_num)
            self.print_result("Validity", f"{Color.GREEN}Valid{Color.RESET}" if is_valid else f"{Color.RED}Invalid{Color.RESET}")
            self.print_result("Possible", f"{Color.GREEN}Yes{Color.RESET}" if is_possible else f"{Color.RED}No{Color.RESET}")
            
            # Carrier
            carrier_name = carrier.name_for_number(parsed_num, "en")
            if carrier_name:
                self.print_result("Carrier", carrier_name)
                
            # Location
            location = geocoder.description_for_number(parsed_num, "en")
            if location:
                self.print_result("Location", location)
                
            # Timezone
            tz = timezone.time_zones_for_number(parsed_num)
            if tz:
                self.print_result("Timezone", ', '.join(tz))
            
            # === ADVANCED SEARCHES ===
            
            # 1. NumVerify API (if key available)
            if self.deep_search.api_keys.get('numverify'):
                self._search_numverify(phone_number)
            
            # 2. AbstractAPI (if key available)
            if self.deep_search.api_keys.get('abstractapi'):
                self._search_abstractapi(phone_number)
            
            # 3. Veriphone (if key available)
            if self.deep_search.api_keys.get('veriphone'):
                self._search_veriphone(phone_number)
            
            # 4. Free OVH API
            self._search_ovh(phone_number)
            
            # 5. Find phone pattern/format
            self._analyze_phone_pattern(phone_number)
            
            # 6. Check against known spam databases
            self._check_spam_databases(phone_number)
            
            # 7. Google dork search for phone number
            self._google_dork_search(phone_number)
            
            # 8. Social media presence check
            self._check_social_media_phone(phone_number)
            
            # 9. WhatsApp/Telegram check
            self._check_messaging_apps(phone_number)
            
            # 10. Generate variations
            self._generate_variations(phone_number)
            
        except phonenumbers.NumberParseException as e:
            self.print_error(f"Invalid phone number format: {e}")
            self.print_info("Please use format: +1234567890")
            
        return results
    
    def _search_numverify(self, phone_number):
        """Search using NumVerify API"""
        self.print_header("NumVerify API Check")
        
        api_key = self.deep_search.api_keys.get('numverify')
        if not api_key:
            self.print_warning("NumVerify API key not set (set NUMVERIFY_API_KEY)")
            return
            
        try:
            url = f"http://apilayer.net/api/validate"
            params = {
                'access_key': api_key,
                'number': phone_number,
                'country_code': '',
                'format': '1'
            }
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('valid'):
                    self.print_result("Number Valid", data.get('valid'))
                    self.print_subresult("Country", data.get('country_name', 'N/A'))
                    self.print_subresult("Country Code", data.get('country_code', 'N/A'))
                    self.print_subresult("Carrier", data.get('carrier', 'N/A'))
                    self.print_subresult("Line Type", data.get('line_type', 'N/A'))
                    self.print_subresult("Location", data.get('location', 'N/A'))
                    self.print_subresult("International Format", data.get('international_format', 'N/A'))
                    self.print_subresult("Local Format", data.get('local_format', 'N/A'))
                    
                    # Additional info
                    if data.get('country_prefix'):
                        self.print_subresult("Country Prefix", data.get('country_prefix'))
                else:
                    self.print_warning("Number not valid according to NumVerify")
        except Exception as e:
            self.print_warning(f"NumVerify API error: {e}")
    
    def _search_abstractapi(self, phone_number):
        """Search using AbstractAPI"""
        self.print_header("AbstractAPI Check")
        
        api_key = self.deep_search.api_keys.get('abstractapi')
        if not api_key:
            self.print_warning("AbstractAPI key not set (set ABSTRACT_API_KEY)")
            return
            
        try:
            url = f"https://phonevalidation.abstractapi.com/v1/"
            params = {
                'api_key': api_key,
                'phone': phone_number
            }
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('valid'):
                    self.print_result("Number Valid", data.get('valid'))
                    self.print_subresult("Country", data.get('country', {}).get('name', 'N/A'))
                    self.print_subresult("Country Code", data.get('country', {}).get('code', 'N/A'))
                    self.print_subresult("Location", data.get('location', 'N/A'))
                    self.print_subresult("Carrier", data.get('carrier', 'N/A'))
                    self.print_subresult("Line Type", data.get('line_type', 'N/A'))
                    
                    if data.get('local_format'):
                        self.print_subresult("Local Format", data.get('local_format'))
                    if data.get('international_format'):
                        self.print_subresult("International Format", data.get('international_format'))
        except Exception as e:
            self.print_warning(f"AbstractAPI error: {e}")
    
    def _search_veriphone(self, phone_number):
        """Search using Veriphone"""
        self.print_header("Veriphone Check")
        
        api_key = self.deep_search.api_keys.get('veriphone')
        if not api_key:
            self.print_warning("Veriphone key not set (set VERIPHONE_API_KEY)")
            return
            
        try:
            url = f"https://api.veriphone.io/v2/verify"
            params = {
                'phone': phone_number,
                'api_key': api_key
            }
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('phone_valid'):
                    self.print_result("Number Valid", data.get('phone_valid'))
                    self.print_subresult("Country", data.get('country', {}).get('name', 'N/A'))
                    self.print_subresult("Country Code", data.get('country', {}).get('code', 'N/A'))
                    self.print_subresult("Carrier", data.get('carrier', 'N/A'))
                    self.print_subresult("Line Type", data.get('type', 'N/A'))
                    
                    if data.get('phone'):
                        self.print_subresult("International", data.get('phone'))
        except Exception as e:
            self.print_warning(f"Veriphone error: {e}")
    
    def _search_ovh(self, phone_number):
        """Free OVH phone validation"""
        self.print_header("OVH Phone Validation (Free)")
        
        try:
            # Remove + from number for OVH
            clean_number = phone_number.replace('+', '')
            
            url = f"https://api.ovh.com/1.0/telephony/phone/{clean_number}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.print_result("Status", "Number found in OVH database")
                
                # Extract any useful info
                if data.get('country'):
                    self.print_subresult("Country", data.get('country'))
                if data.get('type'):
                    self.print_subresult("Type", data.get('type'))
                if data.get('domain'):
                    self.print_subresult("Domain", data.get('domain'))
            else:
                self.print_warning("No OVH information found for this number")
        except Exception as e:
            self.print_warning(f"OVH API error: {e}")
    
    def _analyze_phone_pattern(self, phone_number):
        """Analyze phone number patterns"""
        self.print_header("Number Pattern Analysis")
        
        clean_number = phone_number.replace('+', '').replace(' ', '').replace('-', '')
        
        # Check for repeated digits
        repeated = {}
        for digit in clean_number:
            repeated[digit] = repeated.get(digit, 0) + 1
        
        repeated_digits = {d: c for d, c in repeated.items() if c > 2}
        if repeated_digits:
            self.print_result("Repeated Digits", str(repeated_digits))
        
        # Check for sequential patterns
        has_sequential = False
        for i in range(len(clean_number) - 2):
            if all(int(clean_number[i+j]) == int(clean_number[i]) + j for j in range(3)):
                has_sequential = True
                break
        if has_sequential:
            self.print_result("Sequential Pattern", "Yes - contains 3+ sequential digits")
        
        # Check for palindrome
        if clean_number == clean_number[::-1]:
            self.print_result("Palindrome", "Yes")
        
        # Number length analysis
        self.print_result("Number Length", f"{len(clean_number)} digits")
        
        # Check if number is premium/expensive
        if clean_number.startswith('90') or clean_number.startswith('89'):
            self.print_warning("This appears to be a premium-rate number")
    
    def _check_spam_databases(self, phone_number):
        """Check against known spam databases"""
        self.print_header("Spam Database Check")
        
        # Free spam databases
        spam_apis = [
            {
                'name': 'SpamCalls',
                'url': f"https://spamcalls.net/en/{phone_number.replace('+', '')}"
            },
            {
                'name': 'SpamTracker',
                'url': f"https://www.spamtracker.net/phone/{phone_number}"
            }
        ]
        
        for api in spam_apis:
            try:
                response = self.session.get(api['url'], timeout=5)
                if response.status_code == 200:
                    self.print_result(f"{api['name']}", "Number found in database")
                else:
                    self.print_subresult(f"{api['name']}", "Not found or inaccessible")
            except Exception as e:
                self.print_subresult(f"{api['name']}", f"Error: {str(e)[:30]}")
    
    def _google_dork_search(self, phone_number):
        """Generate Google dorks for phone number"""
        self.print_header("Google Dorks")
        
        clean_number = phone_number.replace('+', '')
        queries = [
            f'"{phone_number}"',
            f'"{clean_number}"',
            f'intitle:"{phone_number}"',
            f'intext:"{phone_number}"',
            f'inurl:"{phone_number}"',
            f'{phone_number} "contact"',
            f'{phone_number} "phone"',
            f'{phone_number} "call"',
            f'{phone_number} filetype:pdf',
            f'{phone_number} filetype:doc',
            f'{phone_number} site:facebook.com',
            f'{phone_number} site:twitter.com',
            f'{phone_number} site:linkedin.com'
        ]
        
        print(f"{Color.DIM}Try these Google searches:{Color.RESET}")
        for i, query in enumerate(queries[:5], 1):
            print(f"  {i}. https://google.com/search?q={requests.utils.quote(query)}")
    
    def _check_social_media_phone(self, phone_number):
        """Check social media presence by phone number"""
        self.print_header("Social Media Presence (Phone Search)")
        
        # Platforms that support phone search
        platforms = [
            {'name': 'Facebook', 'url': f"https://facebook.com/search/top/?q={phone_number}"},
            {'name': 'Twitter', 'url': f"https://twitter.com/search?q={phone_number}"},
            {'name': 'LinkedIn', 'url': f"https://linkedin.com/search/results/all/?keywords={phone_number}"},
            {'name': 'Google', 'url': f"https://google.com/search?q={phone_number}"}
        ]
        
        for platform in platforms:
            print(f"  {Color.CYAN}{platform['name']}:{Color.RESET} {platform['url']}")
        
        print(f"\n{Color.DIM}Note: Manual verification required for these searches{Color.RESET}")
    
    def _check_messaging_apps(self, phone_number):
        """Check if number exists on messaging apps"""
        self.print_header("Messaging Apps Presence")
        
        clean_number = phone_number.replace('+', '').replace(' ', '').replace('-', '')
        
        # WhatsApp
        whatsapp_url = f"https://wa.me/{clean_number}?text=Hello"
        print(f"{Color.CYAN}WhatsApp:{Color.RESET} {whatsapp_url}")
        
        # Telegram
        telegram_url = f"https://t.me/{clean_number}"
        print(f"{Color.CYAN}Telegram:{Color.RESET} {telegram_url}")
        
        # Signal (no direct URL, but can be checked)
        print(f"{Color.CYAN}Signal:{Color.RESET} Check manually via Signal app")
        
        # Viber
        viber_url = f"viber://contact?number={clean_number}"
        print(f"{Color.CYAN}Viber:{Color.RESET} {viber_url}")
        
        # WeChat (China)
        print(f"{Color.CYAN}WeChat:{Color.RESET} Check manually via WeChat app")
        
        # Line (popular in Asia)
        print(f"{Color.CYAN}Line:{Color.RESET} Check manually via Line app")
    
    def _generate_variations(self, phone_number):
        """Generate phone number variations"""
        self.print_header("Number Variations")
        
        clean_number = phone_number.replace('+', '').replace(' ', '').replace('-', '')
        
        # Format variations
        variations = [
            phone_number,
            clean_number,
            f"+{clean_number}",
            f"({clean_number[:3]}) {clean_number[3:6]}-{clean_number[6:]}",
            f"{clean_number[:3]}-{clean_number[3:6]}-{clean_number[6:]}",
            f"{clean_number[:3]}.{clean_number[3:6]}.{clean_number[6:]}"
        ]
        
        # Remove duplicates and limit
        unique_variations = list(dict.fromkeys(variations))[:5]
        
        for i, variant in enumerate(unique_variations, 1):
            print(f"  {i}. {variant}")
        
        # Check if number exists in different formats
        self.print_result("Potential Local Format", f"0{clean_number[1:]}" if clean_number.startswith('233') else clean_number)

    # ============================================
    # OTHER METHODS (from original code)
    # ============================================
    
    def get_ip_info(self, domain_or_ip):
        # ... (keep original code)
        pass
    
    def get_whois_info(self, domain):
        # ... (keep original code)
        pass
    
    def get_dns_records(self, domain):
        # ... (keep original code)
        pass
    
    def check_social_media(self, username):
        # ... (keep original code)
        pass
    
    def get_phone_info(self, phone_number):
        # Enhanced phone search
        self.get_phone_info_deep(phone_number)
    
    def get_email_info(self, email):
        # ... (keep original code)
        pass
    
    def port_scan(self, target, ports=None):
        # ... (keep original code)
        pass
    
    def run(self, target):
        # ... (keep original code with enhanced phone search)
        self.print_header("OSINT TOOL - DEEP INFORMATION GATHERING")
        print(f"Target: {Color.BOLD}{target}{Color.RESET}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Enhanced phone number detection
        if re.match(r'^\+?\d{7,15}$', target.replace(' ', '').replace('-', '')):
            self.get_phone_info_deep(target)
        elif '@' in target:
            self.get_email_info(target)
        else:
            ip = self.get_ip_info(target)
            if ip:
                if not re.match(r'^\d+\.\d+\.\d+\.\d+$', target):
                    self.get_whois_info(target)
                    self.get_dns_records(target)
                    self.port_scan(target)
                else:
                    self.port_scan(target)
        
        print("\n" + "=" * 60)
        self.print_info("Deep scan completed!")

def main():
    parser = argparse.ArgumentParser(
        description="Linux OSINT Tool - Deep Phone Number Search",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 osint_tool.py -t +233593332092
  python3 osint_tool.py -t google.com
  python3 osint_tool.py -t user@gmail.com
  
Set API keys for better results:
  export NUMVERIFY_API_KEY=your_key
  export ABSTRACT_API_KEY=your_key
  export VERIPHONE_API_KEY=your_key
        """
    )
    
    parser.add_argument(
        '-t', '--target',
        required=True,
        help='Target to investigate (phone, domain, IP, or email)'
    )
    
    parser.add_argument(
        '--output',
        help='Save results to JSON file'
    )
    
    args = parser.parse_args()
    
    if not os.name == 'posix':
        print(f"{Color.YELLOW}Warning: This tool is optimized for Linux systems{Color.RESET}")
    
    tool = OSINTTool()
    tool.run(args.target)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(tool.results, f, indent=2)
        print(f"{Color.GREEN}[+] Results saved to {args.output}{Color.RESET}")

if __name__ == "__main__":
    main()
