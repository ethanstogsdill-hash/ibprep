"""Contact database management for IB professionals."""

import sqlite3
import os
from typing import List, Dict, Optional
from datetime import datetime


class ContactDatabase:
    """Manage database of IB contacts."""

    DB_FILE = "data/contacts.db"

    def __init__(self):
        """Initialize database connection."""
        os.makedirs(os.path.dirname(self.DB_FILE), exist_ok=True)
        self.conn = sqlite3.connect(self.DB_FILE)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        """Create database tables if they don't exist."""
        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                first_name TEXT,
                last_name TEXT,
                bank TEXT NOT NULL,
                division TEXT,
                group_name TEXT,
                title TEXT,
                seniority TEXT,
                location_city TEXT,
                location_state TEXT,
                location_country TEXT,
                linkedin_url TEXT,
                email TEXT,
                phone TEXT,
                notes TEXT,
                source TEXT,
                date_added TEXT,
                last_updated TEXT
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_bank ON contacts(bank)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_division ON contacts(division)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_location ON contacts(location_city, location_state)
        """)

        self.conn.commit()

    def add_contact(self, contact_data: Dict[str, str]) -> int:
        """
        Add a contact to the database.

        Args:
            contact_data: Dictionary with contact information

        Returns:
            ID of inserted contact
        """
        # Extract first/last name if not provided
        if 'name' in contact_data and 'first_name' not in contact_data:
            parts = contact_data['name'].split()
            contact_data['first_name'] = parts[0] if parts else ''
            contact_data['last_name'] = ' '.join(parts[1:]) if len(parts) > 1 else ''

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        contact_data['date_added'] = now
        contact_data['last_updated'] = now

        cursor = self.conn.cursor()

        columns = list(contact_data.keys())
        placeholders = ', '.join(['?'] * len(columns))
        column_names = ', '.join(columns)

        query = f"INSERT INTO contacts ({column_names}) VALUES ({placeholders})"
        cursor.execute(query, list(contact_data.values()))

        self.conn.commit()
        return cursor.lastrowid

    def search_contacts(
        self,
        bank: Optional[str] = None,
        division: Optional[str] = None,
        group: Optional[str] = None,
        location_city: Optional[str] = None,
        location_state: Optional[str] = None,
        seniority: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, any]]:
        """
        Search contacts by criteria.

        Args:
            bank: Bank name (partial match)
            division: Division (e.g., Investment Banking, M&A)
            group: Group name (e.g., TMT, Healthcare)
            location_city: City
            location_state: State
            seniority: Seniority level
            limit: Maximum results

        Returns:
            List of matching contacts
        """
        cursor = self.conn.cursor()

        query = "SELECT * FROM contacts WHERE 1=1"
        params = []

        if bank:
            query += " AND LOWER(bank) LIKE LOWER(?)"
            params.append(f"%{bank}%")

        if division:
            query += " AND LOWER(division) LIKE LOWER(?)"
            params.append(f"%{division}%")

        if group:
            query += " AND LOWER(group_name) LIKE LOWER(?)"
            params.append(f"%{group}%")

        if location_city:
            query += " AND LOWER(location_city) LIKE LOWER(?)"
            params.append(f"%{location_city}%")

        if location_state:
            query += " AND LOWER(location_state) LIKE LOWER(?)"
            params.append(f"%{location_state}%")

        if seniority:
            query += " AND LOWER(seniority) LIKE LOWER(?)"
            params.append(f"%{seniority}%")

        query += f" ORDER BY bank, seniority, name LIMIT {limit}"

        cursor.execute(query, params)
        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    def get_contact(self, contact_id: int) -> Optional[Dict[str, any]]:
        """Get a specific contact by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
        row = cursor.fetchone()

        return dict(row) if row else None

    def update_contact(self, contact_id: int, contact_data: Dict[str, str]):
        """Update a contact's information."""
        contact_data['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor = self.conn.cursor()

        set_clause = ', '.join([f"{key} = ?" for key in contact_data.keys()])
        query = f"UPDATE contacts SET {set_clause} WHERE id = ?"

        params = list(contact_data.values()) + [contact_id]
        cursor.execute(query, params)

        self.conn.commit()

    def delete_contact(self, contact_id: int):
        """Delete a contact."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        self.conn.commit()

    def get_stats(self) -> Dict[str, any]:
        """Get database statistics."""
        cursor = self.conn.cursor()

        # Total contacts
        cursor.execute("SELECT COUNT(*) as total FROM contacts")
        total = cursor.fetchone()['total']

        # By bank
        cursor.execute("""
            SELECT bank, COUNT(*) as count
            FROM contacts
            GROUP BY bank
            ORDER BY count DESC
            LIMIT 10
        """)
        by_bank = {row['bank']: row['count'] for row in cursor.fetchall()}

        # By division
        cursor.execute("""
            SELECT division, COUNT(*) as count
            FROM contacts
            WHERE division IS NOT NULL AND division != ''
            GROUP BY division
            ORDER BY count DESC
            LIMIT 10
        """)
        by_division = {row['division']: row['count'] for row in cursor.fetchall()}

        # By location
        cursor.execute("""
            SELECT location_city, location_state, COUNT(*) as count
            FROM contacts
            WHERE location_city IS NOT NULL AND location_city != ''
            GROUP BY location_city, location_state
            ORDER BY count DESC
            LIMIT 10
        """)
        by_location = {f"{row['location_city']}, {row['location_state']}": row['count']
                       for row in cursor.fetchall()}

        return {
            'total': total,
            'by_bank': by_bank,
            'by_division': by_division,
            'by_location': by_location
        }

    def import_from_csv(self, filepath: str) -> int:
        """
        Import contacts from CSV file.

        Args:
            filepath: Path to CSV file

        Returns:
            Number of contacts imported
        """
        import csv

        count = 0

        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)

            for row in reader:
                # Clean up the data
                contact_data = {k: v for k, v in row.items() if v and v.strip()}

                # Add source
                contact_data['source'] = f"CSV Import: {os.path.basename(filepath)}"

                self.add_contact(contact_data)
                count += 1

        return count

    def close(self):
        """Close database connection."""
        self.conn.close()
