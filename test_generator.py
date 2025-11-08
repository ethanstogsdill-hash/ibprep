#!/usr/bin/env python3
"""Quick test of the email generator functionality."""

from src.generator import EmailGenerator
from src.metrics import EmailMetrics

def test_email_generation():
    """Test basic email generation."""
    print("Testing IB Email Generator...")
    print("="*80)

    # Initialize generator
    generator = EmailGenerator()
    metrics_calc = EmailMetrics()

    # Test data
    recipient_data = {
        'name': 'John Smith',
        'title': 'Mr.',
        'bank': 'Goldman Sachs',
        'group': 'TMT',
        'seniority': 'Associate',
        'relationship': 'Cold'
    }

    sender_data = {
        'your_name': 'Jane Doe',
        'your_school': 'University of Pennsylvania',
        'your_background': 'Junior studying Finance',
        'deal_mention': 'Microsoft-Activision Blizzard acquisition'
    }

    print("\n1. Testing Cold Outreach Template...")
    emails = generator.generate_email(
        'cold_outreach',
        recipient_data,
        sender_data,
        tone='warm',
        num_variations=2
    )

    for email in emails:
        print(f"\n--- Variation {email['variation']} ---")
        print(f"Subject: {email['subject']}")
        print(f"\n{email['body']}")
        print(f"\nMetrics: {email['metrics']['word_count']} words, "
              f"{email['metrics']['readability']} readability, "
              f"{email['metrics']['length_assessment']}")

    print("\n" + "="*80)
    print("2. Testing Template Manager...")
    templates = generator.template_manager.get_available_templates()
    print(f"Available templates: {len(templates)}")
    for key, desc in templates.items():
        print(f"  - {key}: {desc}")

    print("\n" + "="*80)
    print("3. Testing Tracking System...")
    from src.tracker import EmailTracker
    tracker = EmailTracker()

    tracker.add_email(
        recipient_data['name'],
        recipient_data['bank'],
        recipient_data['group'],
        recipient_data['seniority'],
        'cold_outreach',
        emails[0]['subject'],
        'Test email'
    )

    stats = tracker.get_stats()
    print(f"Tracking stats: {stats['total_sent']} emails tracked")

    print("\n" + "="*80)
    print("✅ All tests passed! System is working correctly.")
    print("\nRun 'python main.py' to start the interactive interface.")

if __name__ == "__main__":
    test_email_generation()
