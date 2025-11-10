"""CLI for contact discovery and email generation."""

import os
import csv
from typing import List, Dict
from .database import ContactDatabase
from .scraper import LinkedInScraper, ContactFinder
from .generator import EmailGenerator
from .tracker import EmailTracker


class DiscoveryCLI:
    """Command-line interface for contact discovery workflow."""

    def __init__(self):
        """Initialize CLI."""
        self.db = ContactDatabase()
        self.scraper = LinkedInScraper()
        self.generator = EmailGenerator()
        self.tracker = EmailTracker()

    def run(self):
        """Main CLI loop."""
        self.print_header()

        while True:
            self.print_menu()
            choice = input("\nSelect an option (1-8): ").strip()

            if choice == '1':
                self.search_and_generate_emails()
            elif choice == '2':
                self.add_contact_manually()
            elif choice == '3':
                self.import_contacts_csv()
            elif choice == '4':
                self.view_all_contacts()
            elif choice == '5':
                self.get_search_instructions()
            elif choice == '6':
                self.view_database_stats()
            elif choice == '7':
                self.load_sample_data()
            elif choice == '8':
                print("\n👋 Good luck with your networking!")
                self.db.close()
                break
            else:
                print("\n❌ Invalid option. Please try again.")

    def print_header(self):
        """Print application header."""
        print("\n" + "="*80)
        print(" "*15 + "IB CONTACT DISCOVERY & EMAIL GENERATOR")
        print("="*80)
        print("\nFind IB contacts by bank/division/location and generate emails automatically\n")

    def print_menu(self):
        """Print main menu."""
        print("\n" + "-"*80)
        print("MAIN MENU")
        print("-"*80)
        print("1. 🔍 Search Contacts & Generate Emails")
        print("2. ➕ Add Contact Manually")
        print("3. 📁 Import Contacts from CSV")
        print("4. 👥 View All Contacts")
        print("5. 📋 Get Search Instructions (LinkedIn, Alumni DB)")
        print("6. 📊 View Database Stats")
        print("7. 🧪 Load Sample Contact Data")
        print("8. ❌ Exit")

    def search_and_generate_emails(self):
        """Search for contacts and generate emails for them."""
        print("\n" + "="*80)
        print("SEARCH CONTACTS & GENERATE EMAILS")
        print("="*80)

        print("\nEnter search criteria (leave blank to skip):")

        bank = input("Bank (e.g., Goldman Sachs): ").strip()
        division = input("Division (e.g., M&A, Investment Banking): ").strip()
        group = input("Group (e.g., TMT, Healthcare): ").strip()
        city = input("City (e.g., New York): ").strip()
        state = input("State (e.g., NY): ").strip()
        seniority = input("Seniority (e.g., Analyst, Associate, VP, MD): ").strip()

        # Search database
        results = self.db.search_contacts(
            bank=bank if bank else None,
            division=division if division else None,
            group=group if group else None,
            location_city=city if city else None,
            location_state=state if state else None,
            seniority=seniority if seniority else None
        )

        if not results:
            print(f"\n❌ No contacts found matching criteria.")
            print("\n💡 Tip: Try broader search terms or add contacts first (options 2, 3, or 7)")
            return

        print(f"\n✅ Found {len(results)} contact(s):")
        print("-" * 80)

        for i, contact in enumerate(results, 1):
            print(f"{i}. {contact['name']}")
            print(f"   {contact['title']} at {contact['bank']}")
            if contact.get('division'):
                print(f"   Division: {contact['division']}")
            if contact.get('group_name'):
                print(f"   Group: {contact['group_name']}")
            if contact.get('location_city'):
                print(f"   Location: {contact['location_city']}, {contact['location_state']}")
            print()

        # Ask if they want to generate emails
        generate = input(f"\nGenerate emails for these {len(results)} contact(s)? (y/n): ").strip().lower()

        if generate != 'y':
            return

        # Get sender information
        print("\n--- Your Information ---")
        sender_data = self._get_sender_data()

        # Select email template
        print("\nEmail Template Types:")
        templates = self.generator.template_manager.get_available_templates()
        for i, (key, description) in enumerate(templates.items(), 1):
            print(f"{i}. {description}")

        template_choice = self._get_numeric_input(
            f"\nSelect template (1-{len(templates)}): ",
            1,
            len(templates)
        )
        template_type = list(templates.keys())[template_choice - 1]

        # Optional: global deal mention
        deal_mention = input("\nGlobal deal mention (optional, applies to all): ").strip()

        # Generate emails for each contact
        print(f"\n🔄 Generating emails for {len(results)} contacts...\n")

        output_dir = "output/batch_discovery"
        os.makedirs(output_dir, exist_ok=True)

        for contact in results:
            # Prepare recipient data
            recipient_data = {
                'name': contact['name'],
                'bank': contact['bank'],
                'group': contact.get('group_name', contact.get('division', 'Investment Banking')),
                'seniority': contact.get('seniority', 'Professional'),
                'relationship': 'Cold'
            }

            # Prepare sender data with optional deal
            full_sender_data = sender_data.copy()
            if deal_mention:
                full_sender_data['deal_mention'] = deal_mention

            # Generate email
            emails = self.generator.generate_email(
                template_type,
                recipient_data,
                full_sender_data,
                None,  # Auto-determine tone
                1  # One variation per person
            )

            # Save to file
            safe_name = contact['name'].replace(' ', '_').replace('/', '_')
            filename = os.path.join(output_dir, f"{safe_name}_{contact['bank'].replace(' ', '_')}.txt")
            self.tracker.export_to_file(filename, emails)

            # Add to tracking
            self.tracker.add_email(
                contact['name'],
                contact['bank'],
                recipient_data['group'],
                recipient_data['seniority'],
                template_type,
                emails[0]['subject'],
                f"Generated from database contact ID: {contact['id']}"
            )

            print(f"✅ {contact['name']} - {contact['bank']}")

        print(f"\n🎉 Successfully generated {len(results)} emails!")
        print(f"📁 Saved to: {output_dir}/")
        print(f"📊 Added all to tracking system")

    def add_contact_manually(self):
        """Add a single contact manually."""
        print("\n" + "="*80)
        print("ADD CONTACT MANUALLY")
        print("="*80)

        print("\nEnter contact information:")

        name = input("Full name: ").strip()
        bank = input("Bank: ").strip()
        title = input("Job title (e.g., 'Associate - M&A'): ").strip()
        location = input("Location (e.g., 'New York, NY'): ").strip()
        linkedin_url = input("LinkedIn URL (optional): ").strip()
        notes = input("Notes (optional): ").strip()

        # Create contact using scraper helper
        contact_data = self.scraper.create_contact_from_manual_entry(
            name=name,
            bank=bank,
            title=title,
            location=location,
            linkedin_url=linkedin_url,
            notes=notes
        )

        # Add to database
        contact_id = self.db.add_contact(contact_data)

        print(f"\n✅ Contact added successfully! (ID: {contact_id})")
        print(f"   {name} - {title} at {bank}")

    def import_contacts_csv(self):
        """Import contacts from CSV file."""
        print("\n" + "="*80)
        print("IMPORT CONTACTS FROM CSV")
        print("="*80)

        print("\nCSV should have columns: name, bank, title, division, group_name, ")
        print("location_city, location_state, linkedin_url, etc.")

        csv_file = input("\nEnter CSV filename (or 'sample' to create template): ").strip()

        if csv_file.lower() == 'sample':
            self._create_sample_contacts_csv()
            return

        if not os.path.exists(csv_file):
            print(f"\n❌ File '{csv_file}' not found.")
            return

        try:
            count = self.db.import_from_csv(csv_file)
            print(f"\n✅ Successfully imported {count} contacts!")
        except Exception as e:
            print(f"\n❌ Error importing: {e}")

    def view_all_contacts(self):
        """View all contacts in database."""
        print("\n" + "="*80)
        print("ALL CONTACTS")
        print("="*80)

        results = self.db.search_contacts(limit=1000)

        if not results:
            print("\n❌ No contacts in database yet.")
            print("💡 Add contacts using options 2, 3, or 7")
            return

        print(f"\nShowing {len(results)} contact(s):\n")

        for i, contact in enumerate(results, 1):
            print(f"{i}. {contact['name']} - {contact['bank']}")
            print(f"   {contact.get('title', 'N/A')}")
            if contact.get('division'):
                print(f"   {contact['division']}" + (f" - {contact['group_name']}" if contact.get('group_name') else ''))
            if contact.get('location_city'):
                print(f"   {contact['location_city']}, {contact['location_state']}")
            print()

            if i % 20 == 0 and i < len(results):
                cont = input(f"--- Showing {i}/{len(results)}. Continue? (y/n): ").strip().lower()
                if cont != 'y':
                    break

    def get_search_instructions(self):
        """Get instructions for finding contacts on LinkedIn/alumni databases."""
        print("\n" + "="*80)
        print("SEARCH INSTRUCTIONS")
        print("="*80)

        print("\nWhat are you looking for?")
        bank = input("Bank (e.g., Goldman Sachs): ").strip()
        division = input("Division (e.g., M&A, Investment Banking): ").strip()
        location = input("Location (e.g., New York, NY): ").strip()

        print("\nSelect search method:")
        print("1. LinkedIn Manual Search")
        print("2. Google Search for LinkedIn Profiles")
        print("3. Alumni Database Search")

        choice = self._get_numeric_input("Select method (1-3): ", 1, 3)

        methods = {
            1: 'linkedin_manual',
            2: 'google_search',
            3: 'alumni_database'
        }

        instructions = ContactFinder.get_search_instructions(
            bank=bank,
            division=division,
            location=location,
            method=methods[choice]
        )

        print("\n" + "="*80)
        print(instructions)
        print("="*80)

        save = input("\nSave these instructions to a file? (y/n): ").strip().lower()
        if save == 'y':
            filename = f"search_instructions_{bank.replace(' ', '_')}.txt"
            with open(filename, 'w') as f:
                f.write(instructions)
            print(f"✅ Saved to {filename}")

    def view_database_stats(self):
        """View database statistics."""
        print("\n" + "="*80)
        print("DATABASE STATISTICS")
        print("="*80)

        stats = self.db.get_stats()

        print(f"\nTotal Contacts: {stats['total']}")

        if stats['by_bank']:
            print("\n--- Top Banks ---")
            for bank, count in list(stats['by_bank'].items())[:10]:
                print(f"  {bank}: {count}")

        if stats['by_division']:
            print("\n--- Top Divisions ---")
            for division, count in list(stats['by_division'].items())[:10]:
                print(f"  {division}: {count}")

        if stats['by_location']:
            print("\n--- Top Locations ---")
            for location, count in list(stats['by_location'].items())[:10]:
                print(f"  {location}: {count}")

    def load_sample_data(self):
        """Load sample contact data for testing."""
        print("\n" + "="*80)
        print("LOAD SAMPLE DATA")
        print("="*80)

        confirm = input("\nThis will add 20 sample IB contacts to your database. Continue? (y/n): ").strip().lower()

        if confirm != 'y':
            return

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
            contact['source'] = 'Sample Data'
            self.db.add_contact(contact)
            count += 1

        print(f"\n✅ Successfully loaded {count} sample contacts!")
        print("💡 Try option 1 to search for contacts and generate emails")

    def _get_sender_data(self) -> Dict[str, str]:
        """Get sender information interactively."""
        data = {}
        data['your_name'] = input("Your full name: ").strip()
        data['your_school'] = input("Your university: ").strip()
        data['your_background'] = input("Your background (e.g., Junior studying Finance): ").strip()
        return data

    def _get_numeric_input(self, prompt: str, min_val: int, max_val: int) -> int:
        """Get numeric input with validation."""
        while True:
            try:
                value = int(input(prompt).strip())
                if min_val <= value <= max_val:
                    return value
                else:
                    print(f"Please enter a number between {min_val} and {max_val}.")
            except ValueError:
                print("Please enter a valid number.")

    def _create_sample_contacts_csv(self):
        """Create a sample CSV template for contact import."""
        filename = "sample_contacts_import.csv"

        headers = ['name', 'bank', 'title', 'division', 'group_name', 'seniority',
                   'location_city', 'location_state', 'linkedin_url', 'notes']

        sample_data = [
            {
                'name': 'John Doe',
                'bank': 'Goldman Sachs',
                'title': 'Associate - M&A',
                'division': 'Investment Banking',
                'group_name': 'M&A',
                'seniority': 'Associate',
                'location_city': 'New York',
                'location_state': 'NY',
                'linkedin_url': 'https://linkedin.com/in/johndoe',
                'notes': 'Met at conference'
            },
            {
                'name': 'Jane Smith',
                'bank': 'Morgan Stanley',
                'title': 'Analyst - Healthcare',
                'division': 'Investment Banking',
                'group_name': 'Healthcare',
                'seniority': 'Analyst',
                'location_city': 'San Francisco',
                'location_state': 'CA',
                'linkedin_url': '',
                'notes': 'Alumni'
            }
        ]

        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(sample_data)

        print(f"\n✅ Sample CSV template created: '{filename}'")
        print("   Edit this file with your contacts and use option 3 to import")
