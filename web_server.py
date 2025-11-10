#!/usr/bin/env python3
"""
Web server for IB Contact Discovery & Email Generator
No external dependencies - uses only Python standard library
"""

import os
import sys
import json
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Add parent directory to path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import ContactDatabase
from src.scraper import LinkedInScraper
from src.generator import EmailGenerator
from src.tracker import EmailTracker


class APIHandler(SimpleHTTPRequestHandler):
    """Handle HTTP requests for the web interface."""

    def __init__(self, *args, **kwargs):
        # Set the web directory as the base
        super().__init__(*args, directory='web', **kwargs)

    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # API endpoints
        if path == '/api/search':
            self.handle_search(parsed_path.query)
        elif path == '/api/stats':
            self.handle_stats()
        else:
            # Serve static files
            super().do_GET()

    def do_POST(self):
        """Handle POST requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # Read POST data
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')

        try:
            data = json.loads(post_data) if post_data else {}
        except json.JSONDecodeError:
            data = {}

        # API endpoints
        if path == '/api/load_sample_data':
            self.handle_load_sample_data()
        elif path == '/api/add_contact':
            self.handle_add_contact(data)
        elif path == '/api/generate_emails':
            self.handle_generate_emails(data)
        else:
            self.send_error(404, "Not Found")

    def handle_search(self, query_string):
        """Handle contact search."""
        try:
            db = ContactDatabase()
            params = parse_qs(query_string)

            # Extract search parameters
            search_params = {}
            for key in ['bank', 'division', 'group', 'seniority', 'city', 'state']:
                if key in params and params[key][0]:
                    if key == 'city':
                        search_params['location_city'] = params[key][0]
                    elif key == 'state':
                        search_params['location_state'] = params[key][0]
                    else:
                        search_params[key] = params[key][0]

            # Search database
            contacts = db.search_contacts(**search_params)
            db.close()

            self.send_json_response({'contacts': contacts})

        except Exception as e:
            self.send_json_response({'error': str(e)}, status=500)

    def handle_stats(self):
        """Handle statistics request."""
        try:
            db = ContactDatabase()
            stats = db.get_stats()
            db.close()

            self.send_json_response(stats)

        except Exception as e:
            self.send_json_response({'error': str(e)}, status=500)

    def handle_load_sample_data(self):
        """Handle loading sample data."""
        try:
            db = ContactDatabase()

            sample_contacts = [
                # Goldman Sachs
                {"name": "John Smith", "bank": "Goldman Sachs", "title": "Analyst - M&A", "division": "Investment Banking", "group_name": "M&A", "seniority": "Analyst", "location_city": "New York", "location_state": "NY"},
                {"name": "Sarah Johnson", "bank": "Goldman Sachs", "title": "Associate - TMT", "division": "Investment Banking", "group_name": "TMT", "seniority": "Associate", "location_city": "San Francisco", "location_state": "CA"},
                {"name": "Michael Chen", "bank": "Goldman Sachs", "title": "VP - Healthcare M&A", "division": "Investment Banking", "group_name": "Healthcare", "seniority": "VP", "location_city": "New York", "location_state": "NY"},
                {"name": "Emily Davis", "bank": "Goldman Sachs", "title": "MD - FIG", "division": "Investment Banking", "group_name": "FIG", "seniority": "MD", "location_city": "New York", "location_state": "NY"},

                # Morgan Stanley
                {"name": "Robert Martinez", "bank": "Morgan Stanley", "title": "Analyst - Healthcare M&A", "division": "Investment Banking", "group_name": "Healthcare", "seniority": "Analyst", "location_city": "New York", "location_state": "NY"},
                {"name": "Jennifer Park", "bank": "Morgan Stanley", "title": "Associate - Technology M&A", "division": "Investment Banking", "group_name": "TMT", "seniority": "Associate", "location_city": "Menlo Park", "location_state": "CA"},
                {"name": "David Lee", "bank": "Morgan Stanley", "title": "VP - Energy & Power", "division": "Investment Banking", "group_name": "Energy", "seniority": "VP", "location_city": "Houston", "location_state": "TX"},

                # JP Morgan
                {"name": "Amanda Wilson", "bank": "JP Morgan", "title": "Analyst - Leveraged Finance", "division": "Investment Banking", "group_name": "Leveraged Finance", "seniority": "Analyst", "location_city": "New York", "location_state": "NY"},
                {"name": "Christopher Brown", "bank": "JP Morgan", "title": "Associate - M&A", "division": "Investment Banking", "group_name": "M&A", "seniority": "Associate", "location_city": "New York", "location_state": "NY"},
                {"name": "Lisa Anderson", "bank": "JP Morgan", "title": "VP - Consumer Retail", "division": "Investment Banking", "group_name": "Consumer/Retail", "seniority": "VP", "location_city": "Chicago", "location_state": "IL"},

                # Evercore
                {"name": "James Taylor", "bank": "Evercore", "title": "Analyst - M&A", "division": "M&A", "seniority": "Analyst", "location_city": "New York", "location_state": "NY"},
                {"name": "Michelle Kim", "bank": "Evercore", "title": "Associate - Technology M&A", "division": "M&A", "group_name": "TMT", "seniority": "Associate", "location_city": "San Francisco", "location_state": "CA"},
                {"name": "Daniel White", "bank": "Evercore", "title": "MD - Energy & Infrastructure", "division": "M&A", "group_name": "Energy", "seniority": "MD", "location_city": "Houston", "location_state": "TX"},

                # Lazard
                {"name": "Rachel Green", "bank": "Lazard", "title": "Analyst - Restructuring", "division": "Restructuring", "seniority": "Analyst", "location_city": "New York", "location_state": "NY"},
                {"name": "Kevin Zhang", "bank": "Lazard", "title": "Associate - M&A", "division": "M&A", "seniority": "Associate", "location_city": "New York", "location_state": "NY"},

                # Bank of America
                {"name": "Stephanie Moore", "bank": "Bank of America", "title": "Analyst - Healthcare M&A", "division": "Investment Banking", "group_name": "Healthcare", "seniority": "Analyst", "location_city": "Charlotte", "location_state": "NC"},
                {"name": "Brian Thompson", "bank": "Bank of America", "title": "Associate - TMT", "division": "Investment Banking", "group_name": "TMT", "seniority": "Associate", "location_city": "San Francisco", "location_state": "CA"},

                # Citi
                {"name": "Angela Rodriguez", "bank": "Citi", "title": "VP - FIG M&A", "division": "Investment Banking", "group_name": "FIG", "seniority": "VP", "location_city": "New York", "location_state": "NY"},
                {"name": "Thomas Harris", "bank": "Citi", "title": "Analyst - Leveraged Finance", "division": "Investment Banking", "group_name": "Leveraged Finance", "seniority": "Analyst", "location_city": "New York", "location_state": "NY"},

                # Barclays
                {"name": "Laura Martinez", "bank": "Barclays", "title": "Associate - M&A", "division": "Investment Banking", "group_name": "M&A", "seniority": "Associate", "location_city": "New York", "location_state": "NY"},
            ]

            count = 0
            for contact in sample_contacts:
                contact['source'] = 'Sample Data (Web)'
                db.add_contact(contact)
                count += 1

            db.close()

            self.send_json_response({'count': count, 'success': True})

        except Exception as e:
            self.send_json_response({'error': str(e)}, status=500)

    def handle_add_contact(self, data):
        """Handle adding a new contact."""
        try:
            db = ContactDatabase()
            scraper = LinkedInScraper()

            # Create contact using scraper helper
            contact_data = scraper.create_contact_from_manual_entry(
                name=data.get('name', ''),
                bank=data.get('bank', ''),
                title=data.get('title', ''),
                location=data.get('location', ''),
                linkedin_url=data.get('linkedin_url', ''),
                notes=data.get('notes', '')
            )

            contact_data['source'] = 'Web Interface'

            # Add to database
            contact_id = db.add_contact(contact_data)
            db.close()

            self.send_json_response({'id': contact_id, 'success': True})

        except Exception as e:
            self.send_json_response({'error': str(e)}, status=500)

    def handle_generate_emails(self, data):
        """Handle email generation."""
        try:
            generator = EmailGenerator()
            tracker = EmailTracker()

            contacts = data.get('contacts', [])
            sender = data.get('sender', {})

            if not contacts or not sender:
                self.send_json_response({'error': 'Missing contacts or sender data'}, status=400)
                return

            # Create output directory
            output_dir = "output/batch_discovery"
            os.makedirs(output_dir, exist_ok=True)

            count = 0
            for contact in contacts:
                # Prepare recipient data
                recipient_data = {
                    'name': contact['name'],
                    'bank': contact['bank'],
                    'group': contact.get('group_name', contact.get('division', 'Investment Banking')),
                    'seniority': contact.get('seniority', 'Professional'),
                    'relationship': 'Cold'
                }

                # Prepare sender data
                sender_data = {
                    'your_name': sender.get('your_name', ''),
                    'your_school': sender.get('your_school', ''),
                    'your_background': sender.get('your_background', ''),
                }

                if sender.get('deal_mention'):
                    sender_data['deal_mention'] = sender['deal_mention']

                # Generate email
                emails = generator.generate_email(
                    sender.get('template_type', 'cold_outreach'),
                    recipient_data,
                    sender_data,
                    None,  # Auto-determine tone
                    1  # One variation
                )

                # Save to file
                safe_name = contact['name'].replace(' ', '_').replace('/', '_')
                filename = os.path.join(output_dir, f"{safe_name}_{contact['bank'].replace(' ', '_')}.txt")
                tracker.export_to_file(filename, emails)

                # Add to tracking
                tracker.add_email(
                    contact['name'],
                    contact['bank'],
                    recipient_data['group'],
                    recipient_data['seniority'],
                    sender.get('template_type', 'cold_outreach'),
                    emails[0]['subject'],
                    f"Generated via web interface (ID: {contact.get('id', 'N/A')})"
                )

                count += 1

            self.send_json_response({
                'count': count,
                'output_dir': output_dir,
                'success': True
            })

        except Exception as e:
            import traceback
            traceback.print_exc()
            self.send_json_response({'error': str(e)}, status=500)

    def send_json_response(self, data, status=200):
        """Send JSON response."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def log_message(self, format, *args):
        """Custom log message format."""
        # Suppress logging for static files, only show API calls
        if '/api/' in args[0]:
            print(f"[API] {args[0]}")


def run_server(port=8000):
    """Run the web server."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, APIHandler)

    print("\n" + "="*80)
    print(" "*20 + "IB CONTACT DISCOVERY WEB INTERFACE")
    print("="*80)
    print(f"\n🌐 Server running at: http://localhost:{port}")
    print(f"\n📂 Open your browser to: http://localhost:{port}")
    print("\nPress Ctrl+C to stop the server")
    print("="*80 + "\n")

    # Try to open browser automatically
    try:
        webbrowser.open(f'http://localhost:{port}')
    except:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down server...")
        httpd.shutdown()


if __name__ == "__main__":
    # Check if custom port specified
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number, using default 8000")

    run_server(port)
