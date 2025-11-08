"""Interactive CLI interface for email generator."""

import csv
import os
import sys
from typing import Dict, List, Optional
from .generator import EmailGenerator
from .tracker import EmailTracker
from .metrics import EmailMetrics


class CLI:
    """Command-line interface for IB email generator."""

    def __init__(self):
        """Initialize CLI."""
        self.generator = EmailGenerator()
        self.tracker = EmailTracker()
        self.metrics_calculator = EmailMetrics()

    def run(self):
        """Main CLI loop."""
        self.print_header()

        while True:
            self.print_menu()
            choice = input("\nSelect an option (1-6): ").strip()

            if choice == '1':
                self.generate_single_email()
            elif choice == '2':
                self.batch_generate_emails()
            elif choice == '3':
                self.view_tracking_stats()
            elif choice == '4':
                self.view_pending_followups()
            elif choice == '5':
                self.update_response_status()
            elif choice == '6':
                print("\n👋 Good luck with your networking!")
                break
            else:
                print("\n❌ Invalid option. Please try again.")

    def print_header(self):
        """Print application header."""
        print("\n" + "="*80)
        print(" "*20 + "IB NETWORKING EMAIL GENERATOR")
        print("="*80)
        print("\nGenerate personalized, high-quality networking emails for IB recruiting\n")

    def print_menu(self):
        """Print main menu."""
        print("\n" + "-"*80)
        print("MAIN MENU")
        print("-"*80)
        print("1. Generate Single Email")
        print("2. Batch Generate from CSV")
        print("3. View Tracking Stats")
        print("4. View Pending Follow-ups")
        print("5. Update Response Status")
        print("6. Exit")

    def generate_single_email(self):
        """Interactive single email generation."""
        print("\n" + "="*80)
        print("GENERATE SINGLE EMAIL")
        print("="*80)

        # Select template type
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

        # Get recipient information
        print("\n--- Recipient Information ---")
        recipient_data = self._get_recipient_data()

        # Get sender information
        print("\n--- Your Information ---")
        sender_data = self._get_sender_data()

        # Get optional customization
        print("\n--- Optional Customization (press Enter to skip) ---")
        optional_data = self._get_optional_data(template_type)

        # Combine all data
        all_data = {**recipient_data, **sender_data, **optional_data}

        # Get tone preference
        tone = self._get_tone_preference(recipient_data)

        # Get number of variations
        num_variations = self._get_numeric_input(
            "\nHow many variations to generate? (1-5): ",
            1,
            5
        )

        # Generate emails
        print("\n🔄 Generating emails...")
        emails = self.generator.generate_email(
            template_type,
            recipient_data,
            {**sender_data, **optional_data},
            tone,
            num_variations
        )

        # Display emails
        self._display_emails(emails)

        # Ask to save
        save_choice = input("\nWould you like to save these emails? (y/n): ").strip().lower()
        if save_choice == 'y':
            self._save_emails(emails, recipient_data)

        # Ask to add to tracking
        track_choice = input("\nAdd to tracking system? (y/n): ").strip().lower()
        if track_choice == 'y':
            self._add_to_tracking(recipient_data, template_type, emails[0]['subject'])

    def batch_generate_emails(self):
        """Batch generate emails from CSV file."""
        print("\n" + "="*80)
        print("BATCH GENERATE FROM CSV")
        print("="*80)

        csv_file = input("\nEnter CSV filename (or 'sample' to create template): ").strip()

        if csv_file.lower() == 'sample':
            self._create_sample_csv()
            return

        if not os.path.exists(csv_file):
            print(f"\n❌ File '{csv_file}' not found.")
            return

        # Read CSV
        try:
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                recipients = list(reader)
        except Exception as e:
            print(f"\n❌ Error reading CSV: {e}")
            return

        if not recipients:
            print("\n❌ No recipients found in CSV.")
            return

        # Get sender data once (applies to all)
        print("\n--- Your Information (applies to all emails) ---")
        sender_data = self._get_sender_data()

        # Select template type
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

        # Generate for each recipient
        print(f"\n🔄 Generating emails for {len(recipients)} recipients...")
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        for i, recipient in enumerate(recipients, 1):
            print(f"\nProcessing {i}/{len(recipients)}: {recipient.get('name', 'Unknown')}")

            emails = self.generator.generate_email(
                template_type,
                recipient,
                sender_data,
                recipient.get('tone'),
                1  # One variation per person for batch
            )

            # Save to individual file
            filename = os.path.join(
                output_dir,
                f"{recipient.get('name', 'Unknown').replace(' ', '_')}_{template_type}.txt"
            )
            self.tracker.export_to_file(filename, emails)

            # Add to tracking
            self.tracker.add_email(
                recipient.get('name', 'Unknown'),
                recipient.get('bank', 'Unknown'),
                recipient.get('group', 'Unknown'),
                recipient.get('seniority', 'Unknown'),
                template_type,
                emails[0]['subject']
            )

        print(f"\n✅ Generated {len(recipients)} emails in '{output_dir}' directory")
        print(f"✅ Added all to tracking system")

    def view_tracking_stats(self):
        """View email tracking statistics."""
        print("\n" + "="*80)
        print("TRACKING STATISTICS")
        print("="*80)

        stats = self.tracker.get_stats()

        print(f"\nTotal Emails Sent: {stats['total_sent']}")
        print(f"Responses Received: {stats['responses_received']}")
        print(f"Response Rate: {stats['response_rate']}%")
        print(f"Pending Follow-ups: {stats['pending_followups']}")

        if stats['by_bank']:
            print("\n--- By Bank ---")
            for bank, count in sorted(stats['by_bank'].items(), key=lambda x: x[1], reverse=True):
                print(f"  {bank}: {count}")

        if stats['by_type']:
            print("\n--- By Email Type ---")
            for email_type, count in sorted(stats['by_type'].items(), key=lambda x: x[1], reverse=True):
                print(f"  {email_type}: {count}")

    def view_pending_followups(self):
        """View pending follow-ups."""
        print("\n" + "="*80)
        print("PENDING FOLLOW-UPS")
        print("="*80)

        pending = self.tracker.get_pending_followups()

        if not pending:
            print("\n✅ No pending follow-ups! Great job staying on top of things.")
            return

        print(f"\nYou have {len(pending)} pending follow-up(s):\n")

        for i, email in enumerate(pending, 1):
            print(f"{i}. {email['recipient_name']} - {email['bank']} ({email['group']})")
            print(f"   Sent: {email['date_sent']} | Follow-up by: {email['follow_up_date']}")
            print(f"   Type: {email['email_type']}")
            print()

    def update_response_status(self):
        """Update response status for an email."""
        print("\n" + "="*80)
        print("UPDATE RESPONSE STATUS")
        print("="*80)

        emails = self.tracker.get_all_emails()
        pending = [e for e in emails if e['response_received'].lower() == 'no']

        if not pending:
            print("\n✅ All emails have been marked as responded!")
            return

        print("\nPending responses:\n")
        for i, email in enumerate(pending, 1):
            print(f"{i}. {email['recipient_name']} - {email['bank']}")
            print(f"   Sent: {email['date_sent']}")

        choice = self._get_numeric_input(
            f"\nSelect email to update (1-{len(pending)}): ",
            1,
            len(pending)
        )

        selected = pending[choice - 1]
        self.tracker.update_response_status(
            selected['recipient_name'],
            selected['bank'],
            'Yes'
        )

        print(f"\n✅ Updated response status for {selected['recipient_name']}")

    def _get_recipient_data(self) -> Dict[str, str]:
        """Get recipient information interactively."""
        data = {}
        data['name'] = input("Recipient's full name: ").strip()
        data['title'] = input("Title (Mr./Ms./Dr., or press Enter to skip): ").strip() or "Mr./Ms."
        data['bank'] = input("Bank name: ").strip()
        data['group'] = input("Group (e.g., TMT, Healthcare M&A): ").strip()

        print("\nSeniority levels: Analyst, Associate, VP, Director, MD")
        data['seniority'] = input("Seniority: ").strip()

        print("\nRelationship types: Cold, Warm, Referral, Alumni")
        data['relationship'] = input("Relationship type: ").strip()

        return data

    def _get_sender_data(self) -> Dict[str, str]:
        """Get sender information interactively."""
        data = {}
        data['your_name'] = input("Your full name: ").strip()
        data['your_school'] = input("Your university: ").strip()
        data['your_background'] = input("Your background (e.g., Junior studying Finance): ").strip()
        return data

    def _get_optional_data(self, template_type: str) -> Dict[str, str]:
        """Get optional customization data."""
        data = {}

        # Always useful fields
        deal = input("Specific deal to mention (recommended): ").strip()
        if deal:
            data['deal_mention'] = deal

        # Template-specific fields
        if template_type in ['coffee_followup', 'thank_you']:
            topic = input("Discussion topic from your conversation: ").strip()
            if topic:
                data['discussion_topic'] = topic

            insight = input("Specific insight they shared: ").strip()
            if insight:
                data['specific_insight'] = insight

            timeframe = input("When you spoke (e.g., yesterday, last week): ").strip()
            if timeframe:
                data['timeframe'] = timeframe

        if template_type == 'referral':
            referrer = input("Referrer's name: ").strip()
            if referrer:
                data['referrer_name'] = referrer

            context = input("How you know the referrer: ").strip()
            if context:
                data['referrer_context'] = context

        if template_type == 'alumni':
            mascot = input("School mascot/team name: ").strip()
            if mascot:
                data['mascot'] = mascot

        return data

    def _get_tone_preference(self, recipient_data: Dict[str, str]) -> str:
        """Get tone preference with recommendation."""
        recommended_tone = self.generator._determine_tone(recipient_data)

        print(f"\nRecommended tone based on seniority/relationship: {recommended_tone.upper()}")
        print("Tone options: formal, warm, casual")

        custom = input("Use different tone? (press Enter for recommended): ").strip().lower()
        return custom if custom in ['formal', 'warm', 'casual'] else recommended_tone

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

    def _display_emails(self, emails: List[Dict[str, any]]):
        """Display generated emails."""
        for email in emails:
            print("\n" + "="*80)
            print(f"EMAIL VARIATION {email['variation']}")
            print("="*80)
            print(f"\nSubject: {email['subject']}")
            print("\n" + "-"*80)
            print(email['body'])
            print("-"*80)
            print(EmailMetrics.format_metrics(email['metrics']))

    def _save_emails(self, emails: List[Dict[str, any]], recipient_data: Dict[str, str]):
        """Save emails to file."""
        filename = input("\nEnter filename (e.g., john_smith_emails.txt): ").strip()

        if not filename:
            filename = f"{recipient_data['name'].replace(' ', '_')}_emails.txt"

        self.tracker.export_to_file(filename, emails)
        print(f"\n✅ Emails saved to '{filename}'")

    def _add_to_tracking(self, recipient_data: Dict[str, str], template_type: str, subject: str):
        """Add email to tracking system."""
        notes = input("Add notes (optional): ").strip()

        self.tracker.add_email(
            recipient_data['name'],
            recipient_data['bank'],
            recipient_data['group'],
            recipient_data['seniority'],
            template_type,
            subject,
            notes
        )

        print("\n✅ Added to tracking system")

    def _create_sample_csv(self):
        """Create a sample CSV template."""
        filename = "sample_batch_input.csv"

        headers = ['name', 'bank', 'group', 'seniority', 'relationship', 'deal_mention', 'tone']
        sample_data = [
            {
                'name': 'John Smith',
                'bank': 'Goldman Sachs',
                'group': 'TMT',
                'seniority': 'Associate',
                'relationship': 'Cold',
                'deal_mention': 'Microsoft-Activision deal',
                'tone': 'warm'
            },
            {
                'name': 'Jane Doe',
                'bank': 'Morgan Stanley',
                'group': 'Healthcare M&A',
                'seniority': 'VP',
                'relationship': 'Alumni',
                'deal_mention': 'Pfizer acquisition',
                'tone': ''
            }
        ]

        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(sample_data)

        print(f"\n✅ Sample CSV template created: '{filename}'")
        print("   Edit this file with your recipients and use it for batch generation.")
