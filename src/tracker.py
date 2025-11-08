"""Email tracking system for managing outreach."""

import csv
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class EmailTracker:
    """Track sent emails and manage follow-ups."""

    TRACKING_FILE = "data/tracking.csv"

    HEADERS = [
        'date_sent',
        'recipient_name',
        'bank',
        'group',
        'seniority',
        'email_type',
        'subject_line',
        'status',
        'response_received',
        'follow_up_date',
        'notes'
    ]

    # Follow-up timing recommendations (in days)
    FOLLOWUP_TIMING = {
        'cold_outreach': 5,
        'coffee_followup': 7,
        'thank_you': 14,
        'referral': 4,
        'alumni': 5
    }

    def __init__(self):
        """Initialize tracker and ensure tracking file exists."""
        self._ensure_tracking_file()

    def _ensure_tracking_file(self):
        """Create tracking file if it doesn't exist."""
        os.makedirs(os.path.dirname(self.TRACKING_FILE), exist_ok=True)

        if not os.path.exists(self.TRACKING_FILE):
            with open(self.TRACKING_FILE, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.HEADERS)
                writer.writeheader()

    def add_email(
        self,
        recipient_name: str,
        bank: str,
        group: str,
        seniority: str,
        email_type: str,
        subject_line: str,
        notes: str = ""
    ):
        """
        Add a sent email to tracking system.

        Args:
            recipient_name: Name of recipient
            bank: Bank name
            group: Group/division
            seniority: Seniority level
            email_type: Type of email sent
            subject_line: Subject line used
            notes: Additional notes
        """
        date_sent = datetime.now().strftime("%Y-%m-%d")
        followup_days = self.FOLLOWUP_TIMING.get(email_type, 7)
        follow_up_date = (datetime.now() + timedelta(days=followup_days)).strftime("%Y-%m-%d")

        entry = {
            'date_sent': date_sent,
            'recipient_name': recipient_name,
            'bank': bank,
            'group': group,
            'seniority': seniority,
            'email_type': email_type,
            'subject_line': subject_line,
            'status': 'Sent',
            'response_received': 'No',
            'follow_up_date': follow_up_date,
            'notes': notes
        }

        with open(self.TRACKING_FILE, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.HEADERS)
            writer.writerow(entry)

    def get_all_emails(self) -> List[Dict[str, str]]:
        """Get all tracked emails."""
        emails = []

        if os.path.exists(self.TRACKING_FILE):
            with open(self.TRACKING_FILE, 'r') as f:
                reader = csv.DictReader(f)
                emails = list(reader)

        return emails

    def get_pending_followups(self) -> List[Dict[str, str]]:
        """Get emails that need follow-up."""
        today = datetime.now().date()
        pending = []

        for email in self.get_all_emails():
            if email['response_received'].lower() == 'no':
                follow_up_date = datetime.strptime(email['follow_up_date'], "%Y-%m-%d").date()
                if follow_up_date <= today:
                    pending.append(email)

        return pending

    def update_response_status(self, recipient_name: str, bank: str, status: str = "Yes"):
        """
        Update response status for an email.

        Args:
            recipient_name: Name of recipient
            bank: Bank name
            status: Response status (Yes/No)
        """
        emails = self.get_all_emails()
        updated = False

        for email in emails:
            if email['recipient_name'] == recipient_name and email['bank'] == bank:
                email['response_received'] = status
                updated = True

        if updated:
            self._write_all_emails(emails)

    def _write_all_emails(self, emails: List[Dict[str, str]]):
        """Write all emails back to tracking file."""
        with open(self.TRACKING_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.HEADERS)
            writer.writeheader()
            writer.writerows(emails)

    def get_stats(self) -> Dict[str, any]:
        """Get tracking statistics."""
        emails = self.get_all_emails()

        if not emails:
            return {
                'total_sent': 0,
                'responses_received': 0,
                'response_rate': 0,
                'pending_followups': 0
            }

        total = len(emails)
        responses = sum(1 for e in emails if e['response_received'].lower() == 'yes')
        response_rate = (responses / total * 100) if total > 0 else 0
        pending = len(self.get_pending_followups())

        # Group by bank
        by_bank = {}
        for email in emails:
            bank = email['bank']
            if bank not in by_bank:
                by_bank[bank] = 0
            by_bank[bank] += 1

        # Group by email type
        by_type = {}
        for email in emails:
            email_type = email['email_type']
            if email_type not in by_type:
                by_type[email_type] = 0
            by_type[email_type] += 1

        return {
            'total_sent': total,
            'responses_received': responses,
            'response_rate': round(response_rate, 1),
            'pending_followups': pending,
            'by_bank': by_bank,
            'by_type': by_type
        }

    def export_to_file(self, filename: str, emails: List[Dict[str, any]]):
        """
        Export generated emails to a file.

        Args:
            filename: Output filename
            emails: List of email dictionaries
        """
        with open(filename, 'w') as f:
            for i, email in enumerate(emails, 1):
                f.write(f"{'='*80}\n")
                f.write(f"EMAIL VARIATION {email['variation']}\n")
                f.write(f"{'='*80}\n\n")
                f.write(f"Subject: {email['subject']}\n\n")
                f.write(f"{email['body']}\n\n")
                f.write(f"--- Metrics ---\n")
                f.write(self._format_metrics_simple(email['metrics']))
                f.write(f"\n\n")

    def _format_metrics_simple(self, metrics: Dict[str, any]) -> str:
        """Format metrics in simple text format."""
        return f"""Words: {metrics['word_count']} ({metrics['length_assessment']})
Characters: {metrics['character_count']}
Readability: {metrics['readability']}
"""
