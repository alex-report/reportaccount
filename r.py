import requests
import json
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

class AutoReporter:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/json'
        })
        self.max_reports = 100
        self.successful_reports = 0
        self.failed_reports = 0
        self.common_report_reasons = [
            "Harassment or bullying",
            "Hate speech or symbols",
            "Violent or dangerous acts",
            "Suicide or self-harm",
            "Misinformation",
            "Scams or fraud",
            "Impersonation",
            "Intellectual property violation",
            "Nudity or sexual content",
            "Illegal activities"
        ]

    def set_cookies(self, cookie_string):
        cookies_dict = {}
        for item in cookie_string.split(';'):
            if '=' in item:
                key, value = item.strip().split('=', 1)
                cookies_dict[key] = value
        self.session.cookies.update(cookies_dict)

    def discover_report_api(self, platform_url):
        if 'tiktok' in platform_url:
            return "https://www.tiktok.com/api/report/user/"
        elif 'instagram' in platform_url:
            return "https://www.instagram.com/api/v1/web/reports/"
        else:
            return input("Enter the full report API URL for this platform: ").strip()

    def build_report_payload(self, target_identifier, platform='tiktok'):
        payload = {
            "object_id": target_identifier,
            "owner_id": target_identifier,
            "reason": random.randint(100, 300),
            "text": random.choice(self.common_report_reasons),
            "report_type": "user"
        }
        if platform == 'tiktok':
            payload['scene'] = 1200
            payload['from'] = 'profile'
        return payload

    def send_single_report(self, api_url, payload):
        try:
            delay = random.uniform(2, 6)
            time.sleep(delay)
            resp = self.session.post(api_url, json=payload, timeout=10)
            resp.raise_for_status()
            result = resp.json()
            if result.get('status_code') == 0 or result.get('success') is True:
                self.successful_reports += 1
                return True, f"Report {self.successful_reports}: Success."
            else:
                self.failed_reports += 1
                return False, f"Report failed. Response: {result}"
        except Exception as e:
            self.failed_reports += 1
            return False, f"Request error: {str(e)}"

    def execute_report_cycle(self, target_user, api_url, platform):
        print(f"Starting report cycle for user: {target_user}")
        print(f"Using API endpoint: {api_url}")
        futures = []
        with ThreadPoolExecutor(max_workers=3) as executor:
            for i in range(self.max_reports):
                payload = self.build_report_payload(target_user, platform)
                futures.append(executor.submit(self.send_single_report, api_url, payload))
            for future in as_completed(futures):
                success, message = future.result()
                status = "SUCCESS" if success else "FAILED"
                print(f"{status} {message}")
                if self.successful_reports >= self.max_reports:
                    break
        print(f"Cycle finished. Successful: {self.successful_reports}, Failed: {self.failed_reports}")

    def run(self):
        print("Auto Report Script")
        print("Author: Cyber N0d3z")
        print("Telegram: https://t.me/Xxxxx_Cloud")
        print("Contact: https://t.me/N0d3z")
        print("")
        cookie_input = input("Paste your session cookies: ").strip()
        self.set_cookies(cookie_input)
        target = input("Target user ID/username: ").strip()
        platform = input("Platform (e.g., tiktok): ").strip().lower()
        base_url = f"https://www.{platform}.com"
        api_url = self.discover_report_api(base_url)
        confirm = input(f"Ready to send up to {self.max_reports} reports. Proceed? (yes/no): ").strip().lower()
        if confirm == 'yes':
            self.execute_report_cycle(target, api_url, platform)
        else:
            print("Aborted.")

if __name__ == "__main__":
    reporter = AutoReporter()
    reporter.run()
