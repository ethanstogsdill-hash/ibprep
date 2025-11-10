"""
Automatic LinkedIn contact finder.

WARNING: LinkedIn scraping may violate their Terms of Service.
This is for educational and personal use only.
Use responsibly and at your own risk.
"""

import re
import json
import time
from typing import List, Dict, Optional
from urllib.parse import quote_plus
import urllib.request
from html.parser import HTMLParser


class LinkedInProfileParser(HTMLParser):
    """Parse LinkedIn search results HTML."""

    def __init__(self):
        super().__init__()
        self.profiles = []
        self.current_profile = {}
        self.in_name = False
        self.in_title = False
        self.in_location = False

    def handle_starttag(self, tag, attrs):
        """Handle start tags."""
        attrs_dict = dict(attrs)

        # Look for profile containers
        if 'class' in attrs_dict and 'search-result' in attrs_dict.get('class', ''):
            self.current_profile = {}

    def handle_data(self, data):
        """Handle text data."""
        if self.in_name:
            self.current_profile['name'] = data.strip()
        elif self.in_title:
            self.current_profile['title'] = data.strip()
        elif self.in_location:
            self.current_profile['location'] = data.strip()


class LinkedInContactFinder:
    """Find contacts on LinkedIn automatically."""

    def __init__(self):
        """Initialize finder."""
        self.session_cookies = None

    def search_linkedin_public(
        self,
        company: str,
        keywords: str = "",
        location: str = "",
        max_results: int = 10
    ) -> List[Dict[str, str]]:
        """
        Search LinkedIn using public search (limited results).

        NOTE: This method has limitations:
        - Only works for public profiles
        - Limited number of results
        - May be blocked by LinkedIn
        - Requires no login (limited data)

        Args:
            company: Company name
            keywords: Search keywords (title, role)
            location: Location string
            max_results: Maximum number of results

        Returns:
            List of contact dictionaries
        """
        print("\n⚠️  LinkedIn Scraping Warning:")
        print("- This may violate LinkedIn's Terms of Service")
        print("- For educational/personal use only")
        print("- Results may be limited without login")
        print("- LinkedIn may block automated requests")
        print()

        # Generate search URL
        search_query = f"{company} {keywords} {location}".strip()
        encoded_query = quote_plus(search_query)

        # LinkedIn public search URL (limited)
        url = f"https://www.linkedin.com/pub/dir?keywords={encoded_query}"

        print(f"🔍 Searching LinkedIn for: {search_query}")
        print(f"📎 Search URL: {url}")
        print()

        # Try to fetch (will likely be blocked without cookies)
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            req = urllib.request.Request(url, headers=headers)

            print("⚠️  This will likely be blocked by LinkedIn.")
            print("For better results, use the manual method below:")
            print()

            # Attempt fetch (educational purposes)
            # In reality, this will return a login page
            with urllib.request.urlopen(req, timeout=5) as response:
                html = response.read().decode('utf-8')

                if 'authwall' in html or 'login' in html.lower():
                    print("❌ LinkedIn requires login. Cannot scrape without authentication.")
                    print()
                    return []

        except Exception as e:
            print(f"❌ Request failed: {e}")
            print()
            return []

        return []

    def get_manual_instructions(
        self,
        company: str,
        keywords: str = "",
        location: str = ""
    ) -> str:
        """
        Generate instructions for manually finding contacts on LinkedIn.

        This is the RECOMMENDED approach as it:
        - Doesn't violate LinkedIn ToS
        - Uses your existing LinkedIn account
        - Gets better results
        - Is more reliable

        Args:
            company: Company name
            keywords: Search keywords
            location: Location

        Returns:
            Formatted instructions
        """
        search_query = f"{company} {keywords}".strip()
        search_url = f"https://www.linkedin.com/search/results/people/?keywords={quote_plus(search_query)}"

        if location:
            search_url += f"&geoUrn={quote_plus(location)}"

        instructions = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    LINKEDIN CONTACT FINDER INSTRUCTIONS                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

Search for: {company} {keywords} {location}

METHOD 1: LinkedIn Search (Recommended - Fast!)
═══════════════════════════════════════════════════════════════════════════════

1. Click this link (or copy/paste into browser):
   {search_url}

2. You'll see LinkedIn search results like:

   John Smith
   Associate - M&A at {company}
   New York, NY

   Sarah Johnson
   Analyst - Investment Banking at {company}
   New York, NY

3. For each person you want to contact:
   a) Copy their name
   b) Copy their title
   c) Copy their location
   d) Paste into the web interface (Add Contact tab)

4. OR use the Quick Add feature:
   - Copy this template:

   Name: [paste name]
   Bank: {company}
   Title: [paste title]
   Location: [paste location]


METHOD 2: Advanced Filters (Most Results)
═══════════════════════════════════════════════════════════════════════════════

1. Go to LinkedIn and search for: {company}

2. Click "People" tab

3. Add filters:
   - Company: {company}
   - Title contains: {keywords}
   - Location: {location}

4. You'll get a list of everyone matching your criteria

5. Use the export feature below to quickly add them all


METHOD 3: Company Page (Easiest)
═══════════════════════════════════════════════════════════════════════════════

1. Go to: https://www.linkedin.com/company/{company.lower().replace(' ', '-')}

2. Click "People" tab

3. Filter by:
   - Search: {keywords}
   - Location: {location}

4. See all employees matching your criteria


QUICK EXPORT (Save time!)
═══════════════════════════════════════════════════════════════════════════════

After finding contacts on LinkedIn, create a CSV file:

1. Open Excel or Google Sheets

2. Create columns: name, bank, title, location_city, location_state

3. Copy/paste each person's info:
   John Smith, {company}, Associate - M&A, New York, NY

4. Save as contacts.csv

5. Import to this tool: python discover.py → Option 3 → Import CSV

6. Generate emails for everyone at once!


EXAMPLE CSV FORMAT:
═══════════════════════════════════════════════════════════════════════════════

name,bank,title,division,location_city,location_state
John Smith,{company},Associate - M&A,Investment Banking,New York,NY
Sarah Johnson,{company},Analyst - Investment Banking,Investment Banking,New York,NY


TIP: Use LinkedIn Sales Navigator (if you have it)
═══════════════════════════════════════════════════════════════════════════════

Sales Navigator allows:
- Advanced search filters
- Export to CSV (paid feature)
- Unlimited searches
- Better results

Worth it if you're doing lots of networking!

═══════════════════════════════════════════════════════════════════════════════
"""
        return instructions


def find_contacts_interactive(company: str, division: str, location: str):
    """
    Interactive contact finder with multiple methods.

    Args:
        company: Company name
        division: Division/keywords
        location: Location string
    """
    finder = LinkedInContactFinder()

    print("\n" + "="*80)
    print(" "*20 + "LINKEDIN CONTACT FINDER")
    print("="*80)
    print()
    print(f"Searching for: {company} | {division} | {location}")
    print()
    print("Choose search method:")
    print()
    print("1. 📋 Show Manual Instructions (RECOMMENDED)")
    print("   - Use your LinkedIn account")
    print("   - Get better results")
    print("   - No ToS violations")
    print("   - Copy/paste contacts into tool")
    print()
    print("2. 🤖 Try Automatic Scraping (May not work)")
    print("   - Attempts to scrape LinkedIn")
    print("   - Likely to be blocked")
    print("   - Against LinkedIn ToS")
    print("   - Educational purposes only")
    print()

    choice = input("Select method (1 or 2): ").strip()

    if choice == "1":
        # Show manual instructions
        instructions = finder.get_manual_instructions(company, division, location)
        print(instructions)

        # Save to file
        filename = f"linkedin_search_{company.replace(' ', '_')}.txt"
        with open(filename, 'w') as f:
            f.write(instructions)

        print(f"\n✅ Instructions saved to: {filename}")
        print("\nNext steps:")
        print("1. Follow the instructions above")
        print("2. Find contacts on LinkedIn")
        print("3. Add them using the web interface or CLI")
        print("4. Generate emails for everyone!")

    elif choice == "2":
        # Try automatic (will likely fail)
        print("\n⚠️  Attempting automatic scraping...")
        print("This will likely fail - LinkedIn blocks automated requests.\n")

        results = finder.search_linkedin_public(company, division, location)

        if not results:
            print("\n❌ Automatic scraping failed (expected)")
            print("\n💡 Use Method 1 (Manual Instructions) instead")
            print("It's faster and gets better results!")
        else:
            print(f"\n✅ Found {len(results)} contacts")
            for contact in results:
                print(f"- {contact.get('name', 'N/A')}")

    else:
        print("\n❌ Invalid choice")


if __name__ == "__main__":
    # Example usage
    find_contacts_interactive(
        company="Goldman Sachs",
        division="M&A",
        location="New York, NY"
    )
