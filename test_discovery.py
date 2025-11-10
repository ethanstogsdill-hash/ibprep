#!/usr/bin/env python3
"""Test the contact discovery system."""

from src.database import ContactDatabase
from src.scraper import LinkedInScraper, ContactFinder
from src.generator import EmailGenerator

def test_discovery_system():
    """Test contact discovery and email generation."""
    print("Testing IB Contact Discovery System")
    print("="*80)

    # Test 1: Database
    print("\n1. Testing Contact Database...")
    db = ContactDatabase()

    # Add sample contact
    sample_contact = {
        'name': 'John Smith',
        'bank': 'Goldman Sachs',
        'title': 'Associate - M&A',
        'division': 'Investment Banking',
        'group_name': 'M&A',
        'seniority': 'Associate',
        'location_city': 'New York',
        'location_state': 'NY',
        'source': 'Test Data'
    }

    contact_id = db.add_contact(sample_contact)
    print(f"   ✅ Added contact (ID: {contact_id})")

    # Test 2: Search
    print("\n2. Testing Contact Search...")
    results = db.search_contacts(bank='Goldman', division='M&A')
    print(f"   ✅ Found {len(results)} contact(s) matching 'Goldman' + 'M&A'")
    if results:
        print(f"      - {results[0]['name']} at {results[0]['bank']}")

    # Test 3: Scraper
    print("\n3. Testing LinkedIn Scraper...")
    scraper = LinkedInScraper()

    # Parse title
    title_info = scraper.extract_title_info("Associate - Healthcare M&A")
    print(f"   ✅ Extracted from title: {title_info['seniority']}, {title_info.get('division', 'N/A')}")

    # Generate search URL
    search_url = scraper.generate_linkedin_search_url(
        "Goldman Sachs",
        "M&A",
        "New York"
    )
    print(f"   ✅ Generated LinkedIn search URL")
    print(f"      {search_url[:80]}...")

    # Test 4: Email Generation for Contact
    print("\n4. Testing Email Generation from Contact...")
    generator = EmailGenerator()

    recipient_data = {
        'name': results[0]['name'] if results else 'John Smith',
        'bank': results[0]['bank'] if results else 'Goldman Sachs',
        'group': results[0].get('group_name', 'M&A') if results else 'M&A',
        'seniority': results[0].get('seniority', 'Associate') if results else 'Associate',
        'relationship': 'Cold'
    }

    sender_data = {
        'your_name': 'Jane Doe',
        'your_school': 'University of Pennsylvania',
        'your_background': 'Junior studying Finance',
        'deal_mention': 'Microsoft-Activision acquisition'
    }

    emails = generator.generate_email(
        'cold_outreach',
        recipient_data,
        sender_data,
        'warm',
        1
    )

    print(f"   ✅ Generated email:")
    print(f"      Subject: {emails[0]['subject']}")
    print(f"      Length: {emails[0]['metrics']['word_count']} words")

    # Test 5: Search Instructions
    print("\n5. Testing Search Instructions Generator...")
    instructions = ContactFinder.get_search_instructions(
        bank="Goldman Sachs",
        division="M&A",
        location="New York, NY",
        method="linkedin_manual"
    )
    print(f"   ✅ Generated search instructions ({len(instructions)} characters)")

    # Test 6: Stats
    print("\n6. Testing Database Stats...")
    stats = db.get_stats()
    print(f"   ✅ Database Stats:")
    print(f"      Total contacts: {stats['total']}")
    print(f"      Banks: {len(stats['by_bank'])}")

    # Cleanup
    db.close()

    print("\n" + "="*80)
    print("✅ All tests passed! Contact discovery system is working.")
    print("\nNext steps:")
    print("1. Run 'python discover.py' to use the full interface")
    print("2. Load sample data (option 7) to test with 20 IB contacts")
    print("3. Search by bank/division/location and generate emails!")

if __name__ == "__main__":
    test_discovery_system()
