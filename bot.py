"""
Papaji Mummy Family — WhatsApp Birthday & Anniversary Bot
=========================================================
Runs daily at 8 AM IST. Checks today's date and sends a
WhatsApp message to every family member if someone is celebrating.

Setup: See SETUP_GUIDE.md
"""

import datetime
import requests
import os
import time

# ─── CONFIGURATION ────────────────────────────────────────────────

WHATSAPP_TOKEN  = os.getenv("WHATSAPP_TOKEN", "EAANZClboAFY0BQ4xiB7Hx213r5Pz0tmZBHgeIS8bMsbXGj2toRSrmZA0jR2qy8tnRkH34fFmSOPNks9vi6UUUWnBWkk49tPMIt4c5Nq4IHGaCYl8FbYj2jyJurIZCeGn5BzG06MRzRVe2nkJKZBIDvqX5mFeJJSGnzuZBpCExX9pErRMuX0kzEeaqjL46sYLcnf2jWNVFWpznKzh3mss7oO88jwdmhmeytln1gr5cFntjUe4pCvvmlKW1ZBOPSP6GsuzK9SpDP5P2UNIvjMCUWGGPAZBHzwZD")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID", "963537020181180")

# ─── FAMILY MEMBERS (Papaji Family Group) ─────────────────────────

FAMILY_MEMBERS = [
    ("Radhika",       "919680145121"),
    ("Rinky",         "19132023810"),
    ("Shubhi",        "15109449432"),
    ("Kunj Bihari",   "919828168152"),
    ("Anjana",        "919509887714"),
    ("Ayushi",        "918273732506"),
    ("Paritosh",      "918698086545"),
    ("Bankey Bihari", "919950384163"),
    ("Hanu",          "918824887714"),
    ("Kusum",         "919950384213"),
    ("Mona",          "919929647380"),
    ("Mohit",         "917052039333"),
    ("Neha",          "919928410893"),
    ("Nisheeth",      "919587397885"),
    ("Payal",         "919784648339"),
    ("Prashant",      "919799931559"),
    ("Rasik",         "919352387714"),
    ("Ravindra",      "919828563834"),
    ("Reena",         "918112206288"),
    ("Shashank",      "917742968152"),
    ("Shyama",        "919828563835"),
    ("Swati",         "919414069554"),
    ("Vipul",         "19086569013"),
    ("Kishori",       "919829066474"),
    ("Vanshika",      "919664491634"),
]

# ─── FAMILY EVENTS ────────────────────────────────────────────────

EVENTS = [
    # ── Bankey Bihari Mathur / Kusum Mathur ──
    ("Papa (Bankey Bihari Mathur)",      "birthday",     24,  8),
    ("Mummy (Kusum Mathur)",             "birthday",     27, 11),
    ("Bankey Bihari ji & Kusum ji",      "anniversary",  17,  7),
    ("Neha",                             "birthday",     11,  6),
    ("Radhika",                          "birthday",     23, 12),
    ("Radhika & Jijaji",                 "anniversary",   9, 12),
    ("Nisheeth",                         "birthday",     23, 10),
    ("Dileesha",                         "birthday",     23,  4),
    ("Gaurang",                          "birthday",     15, 10),
    # ── Kishori Mathur / Narendra Mohan Mathur ──
    ("Kishori Bhua",                     "birthday",     19,  4),
    ("Fufaji (Narendra Mohan Mathur)",   "birthday",      3,  7),
    ("Kishori Bhua & Narendra Mohan ji", "anniversary",  27,  4),
    ("Payal Didi",                       "birthday",     25,  5),
    ("Jiyaji (Payal Didi ke)",           "birthday",     15,  5),
    ("Payal Didi & Jiyaji",              "anniversary",  23,  6),
    ("Sakhi",                            "birthday",     11,  7),
    ("Krishna",                          "birthday",     11,  8),
    ("Prashant Bhaiya",                  "birthday",     11, 11),
    ("Swati Bhabhi",                     "birthday",     14, 10),
    ("Prashant Bhaiya & Swati Bhabhi",   "anniversary",  16,  5),
    ("Vanshika",                         "birthday",     11,  3),
    ("Varnika",                          "birthday",     18, 12),
    # ── Shyama Mathur / Ravindra Nath Mathur ──
    ("Shyama Bhua",                      "birthday",     12, 11),
    ("Fufaji (Ravindra Nath Mathur)",    "birthday",     29,  1),
    ("Shyama Bhua & Ravindra Nath ji",   "anniversary",  19, 11),
    ("Rinky Didi",                       "birthday",      8, 12),
    ("Jiyaji (Rinky Didi ke)",           "birthday",      6,  9),
    ("Rinky Didi & Jiyaji",              "anniversary",   9,  2),
    ("Punyah",                           "birthday",      3,  5),
    ("Jisha",                            "birthday",     24, 11),
    ("Babloo",                           "birthday",      3, 12),
    ("Reena Bhabhi",                     "birthday",     25,  7),
    ("Babloo & Reena Bhabhi",            "anniversary",  30,  5),
    ("Kaashni",                          "birthday",      4,  3),
    # ── Kunj Bihari Mathur / Mona Mathur ──
    ("Kunju Chacha",                     "birthday",     26, 11),
    ("Mona Chachi",                      "birthday",     25,  7),
    ("Kunju Chacha & Mona Chachi",       "anniversary",  28,  1),
    ("Shubhi",                           "birthday",     21,  2),
    ("Mohit ji",                         "birthday",     30, 11),
    ("Shubhi & Mohit ji",                "anniversary",  16,  2),
    ("Shashank",                         "birthday",     10, 12),
    # ── Rasik Bihari Mathur / Anjana Mathur ──
    ("Rasik Chacha",                     "birthday",     21,  2),
    ("Anjana Chachi",                    "birthday",     26,  1),
    ("Rasik Chacha & Anjana Chachi",     "anniversary",  27,  4),
    ("Hanu",                             "birthday",     24,  6),
    ("Ayushi",                           "birthday",     14,  7),
    ("Hanu & Ayushi",                    "anniversary",  30,  1),
    ("Chotu",                            "birthday",     12,  1),
    # ── Death Anniversaries ──
    ("Papaji",                           "remembrance",   2,  1),
    ("Mummy",                            "remembrance",  21,  4),
]

# ─── MESSAGE BUILDER ──────────────────────────────────────────────

def build_message(today_events):
    today = datetime.date.today()
    date_str = today.strftime("%d %B %Y")

    birthdays     = [e for e in today_events if e[1] == "birthday"]
    anniversaries = [e for e in today_events if e[1] == "anniversary"]
    remembrances  = [e for e in today_events if e[1] == "remembrance"]

    lines = ["🌸 *Papaji Mummy Family* 🌸", f"_{date_str}_", ""]

    if birthdays:
        lines.append("🎂 *Happy Birthday!*")
        for e in birthdays:
            lines.append(f"  • {e[0]}")
        lines.append("")

    if anniversaries:
        lines.append("💍 *Happy Anniversary!*")
        for e in anniversaries:
            lines.append(f"  • {e[0]}")
        lines.append("")

    if remembrances:
        lines.append("🕯️ *We Remember With Love*")
        for e in remembrances:
            lines.append(f"  • {e[0]} ji ki Punyatithi")
        lines.append("")

    lines.append("Please share your wishes with the family! 🙏❤️")
    return "\n".join(lines)

# ─── SEND TO WHATSAPP ─────────────────────────────────────────────

def send_whatsapp(message, name, phone):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message}
    }
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code == 200:
        print(f"  ✅ Sent to {name} ({phone})")
    else:
        print(f"  ❌ Failed for {name} ({phone}): {resp.status_code} — {resp.text}")

# ─── MAIN ─────────────────────────────────────────────────────────

def main():
    today = datetime.date.today()
    today_events = [e for e in EVENTS if e[2] == today.day and e[3] == today.month]

    if not today_events:
        print(f"No events today ({today}). Nothing sent.")
        return

    print(f"\n🎉 {len(today_events)} event(s) today ({today}):")
    for e in today_events:
        print(f"  → {e[0]} ({e[1]})")

    message = build_message(today_events)
    print(f"\n--- Message Preview ---\n{message}\n-----------------------\n")
    print(f"Sending to {len(FAMILY_MEMBERS)} family members...\n")

    for name, phone in FAMILY_MEMBERS:
        send_whatsapp(message, name, phone)
        time.sleep(0.5)  # avoid rate limits

    print(f"\nDone! 🌸")

if __name__ == "__main__":
    main()
