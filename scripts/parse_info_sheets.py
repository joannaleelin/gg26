#!/usr/bin/env python3
"""
Parse all .txt files in /tmp/gg26-info-sheets-txt/ (converted from .docx)
into a single JS file: assets/info-sheets.js

Schema:
{
  role_title: str,
  staff_call_time: str,            # e.g. "11:00 AM"
  assignments: [ { phase, time, role, location, role_leader }, ... ],
  assignment_notes: [str, ...],
  role_descriptions: [
    {
      title: str,
      sections: [ { heading, body? , items? }, ... ],
      lead_name, lead_phone, lead_tel,
    }, ...
  ],
  additional_contacts: STANDARD_CONTACTS (refs the constant),
  ideal_break: str,
}
"""

import os
import re
import json
import sys

SRC_DIR = "/tmp/gg26-info-sheets-txt"
REPO   = "/Users/joannalin/Dropbox/Repositories/Gold Gala GG26 Staffing/Staffing Repo"
OUT    = os.path.join(REPO, "assets/info-sheets.js")
DATA_JS  = os.path.join(REPO, "assets/data.js")
EXCEL_PATH = "/Users/joannalin/Dropbox/Repositories/Gold Gala GG26 Staffing/Reference for Content/Gold Gala 2026 - Day of Staffing Kit.xlsx"

# --- Phase keywords used in YOUR ASSIGNMENTS table ---
PHASE_NAMES = {
    "Pre-Event", "Cocktails", "Transition to Dinner",
    "Dinner & Program", "Transition to Afterparty", "Founders Party"
}

# --- Section markers in the .docx text ---
SEC_TIMELINE = "TIMELINE"
SEC_ASSIGNMENTS = "YOUR ASSIGNMENTS"
SEC_ROLES = "YOUR ROLE(S)"
SEC_CONTACTS = "ADDITIONAL KEY CONTACTS"
SEC_BREAKS = "BREAKS"
SEC_DAYOF = "DAY-OF PROFESSIONALISM"
SEC_QUESTIONS = "QUESTIONS?"

# Sub-section markers within a role description
ROLE_SUB_HEADERS = {
    "YOUR ROLE": "Your role",
    "YOUR ROLES": "Your role",
    "WHAT YOU'LL DO": "What you'll do",
    "WHAT YOU’LL DO": "What you'll do",  # smart apostrophe variant
    "IMPORTANT PARTNER INFO": "Important partner info",
    "IMPORTANT GUEST INFO": "Important guest info",
    "YOUR LEAD": "_LEAD_",
    "YOUR LEADS": "_LEAD_",
}

# These appear with a colon in the .docx; we strip the colon
COLON_SUB_PATTERNS = [
    "What you'll do",
    "Before the event",
]

# ----------------------------------------------------------------

def title_case_name(raw):
    """Convert ALL CAPS name to Title Case, preserving particles."""
    parts = raw.split()
    out = []
    for p in parts:
        # Keep all-caps acronyms (e.g. VIP), or words with internal caps
        if len(p) <= 2 and p.isupper():
            out.append(p)
        else:
            out.append(p.capitalize())
    return " ".join(out)


def slugify(name):
    """Match the JS slugify() in the site."""
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s


def phone_to_tel(phone):
    """Convert '(713) 628-1389' or '713-628-1389' → '+17136281389'."""
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 10:
        return "+1" + digits
    if len(digits) == 11 and digits.startswith("1"):
        return "+" + digits
    return ""


def split_lead(line):
    """Parse 'Caro Delfin — (224) 345-8309' or 'Caro Delfin - (224) 345-8309'.
    Returns (name, phone) or (line, '') if not parseable."""
    # Try em dash, en dash, or hyphen separator
    m = re.match(r"^(.+?)\s*[—–-]\s*(\(?\d.+)$", line)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return line.strip(), ""


# ----------------------------------------------------------------
# Per-section parsers
# ----------------------------------------------------------------

def parse_assignments(lines, i):
    """Starting at the line after 'YOUR ASSIGNMENTS', read the table.
    Layout: 5 header lines (Phase / Time / Role / Location / Role Leader),
    then groups of 5 lines per row. Stops on first bullet line or section marker."""
    assignments = []
    notes = []

    # Skip the 5 header rows
    expected_headers = ["Phase", "Time", "Role", "Location", "Role Leader"]
    # Sometimes there's a blank line first
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    # Skip headers
    for h in expected_headers:
        if i < len(lines) and lines[i].strip() == h:
            i += 1
        else:
            # Headers may not match exactly if a non-standard sheet — bail safely
            break

    # Now read rows of 5 lines until we hit a bullet, section, or empty
    while i < len(lines):
        line = lines[i].strip()
        # Detect end of table
        if not line:
            i += 1
            continue
        if line.startswith("•") or line.startswith("•"):
            # Notes section starts
            break
        if line == SEC_ROLES or line == "YOUR ROLE(S)":
            break
        # Try to read 5 cells starting here
        if i + 4 >= len(lines):
            break
        # First cell of a row must EXACTLY match a known phase name
        phase = lines[i].strip()
        if phase not in PHASE_NAMES:
            # Not a row start — stop
            break
        time_  = lines[i+1].strip()
        role   = lines[i+2].strip()
        loc    = lines[i+3].strip()
        leader = lines[i+4].strip()
        i += 5
        # Some rows have a second lead (e.g. Kat Yu: "Caro Delfin — (224) 345-8309 / blank / Chiharu Iijima — (817) 487-1574").
        # If the next non-empty line looks like a continuation (a phone-bearing line),
        # append it to the leader cell. Stop on phase names, bullets, or section markers.
        STOP_TOKENS = {SEC_ROLES, SEC_CONTACTS, SEC_BREAKS, SEC_DAYOF, SEC_QUESTIONS}
        j = i
        # Peek at the next non-empty line
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines):
            peek = lines[j].strip()
            if (
                peek not in PHASE_NAMES
                and peek not in STOP_TOKENS
                and not peek.startswith("•") and not peek.startswith("•")
                and re.search(r"\d{3}", peek)  # contains 3+ digits → looks like a phone line
            ):
                leader = leader + " · " + peek
                i = j + 1
        assignments.append({
            "phase": phase,
            "time": time_,
            "role": role,
            "location": loc,
            "role_leader": leader,
        })

    # Read bullet notes after the table, until we hit YOUR ROLE(S)
    while i < len(lines):
        line = lines[i].strip()
        if line == SEC_ROLES or line == "YOUR ROLE(S)":
            break
        if line.startswith("•") or line.startswith("•"):
            note = re.sub(r"^[••]\s*", "", line).strip()
            notes.append(note)
        i += 1

    return assignments, notes, i


def parse_role_blocks(lines, i):
    """From the line after 'YOUR ROLE(S)', parse one or more role description blocks.
    Boundaries: each role ends at 'YOUR LEAD' (followed by 1 lead line). The next
    non-empty line then is either 'ADDITIONAL KEY CONTACTS' (end of all roles) or
    the next role's title."""

    roles = []
    # Skip leading "You hold the same/different role..." sentence
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith("You hold "):
            i += 1
            break  # done with that intro line
        break

    def is_bullet(s):
        return s.startswith("•") or s.startswith("•")

    while i < len(lines):
        # Find next non-empty line — should be either the next role title, or ADDITIONAL KEY CONTACTS
        while i < len(lines) and not lines[i].strip():
            i += 1
        if i >= len(lines):
            break
        if lines[i].strip() == SEC_CONTACTS:
            break

        # Title is whatever this first non-empty line is
        title = lines[i].strip()
        i += 1

        # Parse sections until we hit YOUR LEAD (which terminates the role)
        sections = []
        current_heading = None
        current_body_lines = []
        current_items = []
        lead_name = ""
        lead_phone = ""
        lead_tel = ""

        def flush():
            nonlocal current_heading, current_body_lines, current_items
            if current_heading is None:
                return
            section = {"heading": current_heading}
            if current_items:
                section["items"] = current_items[:]
            elif current_body_lines:
                section["body"] = " ".join(current_body_lines).strip()
            else:
                current_heading = None
                current_body_lines = []
                current_items = []
                return
            sections.append(section)
            current_heading = None
            current_body_lines = []
            current_items = []

        while i < len(lines):
            ln = lines[i].rstrip()
            stripped = ln.strip()

            # End of all roles
            if stripped == SEC_CONTACTS:
                flush()
                roles.append({
                    "title": title,
                    "sections": sections,
                    "lead_name": lead_name,
                    "lead_phone": lead_phone,
                    "lead_tel": lead_tel,
                })
                return roles, i

            # YOUR LEAD / YOUR LEADS = end of this role.  Either:
            #   - YOUR LEAD: single lead line on next non-empty line
            #   - YOUR LEADS: list of bullet lines, each "<station>: Name — phone"
            if stripped in ROLE_SUB_HEADERS and ROLE_SUB_HEADERS[stripped] == "_LEAD_":
                flush()
                is_plural = stripped == "YOUR LEADS"
                i += 1
                while i < len(lines) and not lines[i].strip():
                    i += 1
                # Consume lead lines: bullets if plural, otherwise one line
                lead_lines = []
                if is_plural:
                    while i < len(lines):
                        ln2 = lines[i].strip()
                        if not ln2:
                            i += 1
                            break
                        if ln2 == SEC_CONTACTS:
                            break
                        if ln2.startswith("•"):
                            lead_lines.append(re.sub(r"^•\s*", "", ln2))
                            i += 1
                            continue
                        # Non-bullet, non-empty: probably the next role title
                        break
                else:
                    if i < len(lines):
                        lead_lines.append(lines[i].strip())
                        i += 1
                # Use first lead as the primary (if plural, names are usually
                # like "Grand Check-in: Lorrie Chan — (510) 219-2666")
                if lead_lines:
                    first = lead_lines[0]
                    if ":" in first:
                        # Strip "Station: " prefix
                        first = first.split(":", 1)[1].strip()
                    lead_name, lead_phone = split_lead(first)
                    lead_tel = phone_to_tel(lead_phone)
                roles.append({
                    "title": title,
                    "sections": sections,
                    "lead_name": lead_name,
                    "lead_phone": lead_phone,
                    "lead_tel": lead_tel,
                })
                break  # outer loop will find next title or ADDITIONAL KEY CONTACTS

            # Known uppercase sub-headers (everything except YOUR LEAD)
            if stripped in ROLE_SUB_HEADERS and ROLE_SUB_HEADERS[stripped] != "_LEAD_":
                flush()
                current_heading = ROLE_SUB_HEADERS[stripped]
                i += 1
                continue

            # "Foo:" sub-headers (line ends with colon, not a bullet)
            if stripped.endswith(":") and len(stripped) < 100 and not is_bullet(stripped):
                flush()
                current_heading = stripped[:-1]
                i += 1
                continue

            # Bullets
            if is_bullet(stripped):
                if current_heading is None:
                    current_heading = "Notes"
                item = re.sub(r"^[••]\s*", "", stripped).strip()
                current_items.append(item)
                i += 1
                continue

            # Body line
            if not current_heading and stripped:
                current_heading = "Your role"
            if stripped:
                current_body_lines.append(stripped)
            i += 1

        # Outer loop continues, looking for the next role's title

    return roles, i


def parse_breaks(lines, i):
    """Find 'Your ideal break: 7:00 - 7:45 PM'."""
    while i < len(lines):
        line = lines[i].strip()
        if line == SEC_DAYOF:
            break
        m = re.match(r"^Your ideal break:\s*(.+)$", line)
        if m:
            return m.group(1).strip(), i
        i += 1
    return "", i


# ----------------------------------------------------------------

def parse_file(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    raw_lines = text.split("\n")
    # Normalize tabs at line starts (textutil emits "\t•")
    lines = [re.sub(r"^\t+", "", l) for l in raw_lines]

    # Skip blanks at top
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1

    name_raw = lines[i].strip()
    name = title_case_name(name_raw)
    i += 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    role_title = lines[i].strip()
    i += 1

    # Find the staff-call-time line directly — works whether the .docx has the
    # literal "TIMELINE" header or not (some sheets omit it).
    staff_call_time = ""
    saturday_re = re.compile(r"^Saturday,?\s*May\s*9\s*[—–-]\s*(.+)$")
    j = i
    while j < len(lines) and lines[j].strip() != SEC_ASSIGNMENTS:
        m = saturday_re.match(lines[j].strip())
        if m:
            staff_call_time = m.group(1).strip()
            break
        j += 1
    i = j

    # Find YOUR ASSIGNMENTS
    while i < len(lines) and lines[i].strip() != SEC_ASSIGNMENTS:
        i += 1
    i += 1  # past header
    assignments, assignment_notes, i = parse_assignments(lines, i)

    # Find YOUR ROLE(S)
    while i < len(lines) and lines[i].strip() != SEC_ROLES:
        i += 1
    i += 1
    role_descriptions, i = parse_role_blocks(lines, i)

    # Find ADDITIONAL KEY CONTACTS — skip (we use STANDARD_CONTACTS), advance past
    while i < len(lines) and lines[i].strip() != SEC_CONTACTS:
        i += 1
    while i < len(lines) and lines[i].strip() != SEC_BREAKS:
        i += 1
    i += 1
    ideal_break, i = parse_breaks(lines, i)

    return {
        "_name": name,
        "_slug": slugify(name),
        "role_title": role_title,
        "staff_call_time": staff_call_time,
        "assignments": assignments,
        "assignment_notes": assignment_notes,
        "role_descriptions": role_descriptions,
        "ideal_break": ideal_break,
    }


def js_escape(s):
    """Escape a string for inclusion in a single-quoted JS string."""
    return (
        s.replace("\\", "\\\\")
         .replace("\"", "\\\"")
    )


def js_dump_string(s):
    """Output a string as a JS double-quoted literal."""
    return '"' + js_escape(s) + '"'


def js_dump(value, indent=0):
    """Emit JS literal (similar to JSON but with double-quoted keys/strings).
    JSON is valid JS, so we use json.dumps with ensure_ascii=False."""
    return json.dumps(value, ensure_ascii=False, indent=2)


# ----------------------------------------------------------------
# FTE entry generation (people without .docx info sheets)
# ----------------------------------------------------------------

def read_data_js_staff(path):
    """Pull window.GG_DATA.staff out of data.js as a list of dicts."""
    src = open(path, "r", encoding="utf-8").read()
    # Trim 'window.GG_DATA = ' and trailing ';'
    start = src.find("{")
    end   = src.rfind("}")
    obj_text = src[start:end+1]
    data = json.loads(obj_text)
    return data["staff"]


def read_excel_call_times_and_breaks():
    """Returns (call_times, ideal_breaks) keyed by lowercased name.
    Also returns dietary keyed by lowercased name."""
    import zipfile, xml.etree.ElementTree as ET
    z = zipfile.ZipFile(EXCEL_PATH)
    ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    ss_xml = z.read("xl/sharedStrings.xml").decode()
    ss_root = ET.fromstring(ss_xml)
    shared = [
        "".join((t.text or "") for t in si.iter(f"{ns}t"))
        for si in ss_root.findall(f"{ns}si")
    ]
    def grid(sheet_path):
        root = ET.fromstring(z.read(sheet_path).decode())
        rows = []
        for row in root.findall(f".//{ns}row"):
            r = {}
            for c in row.findall(f"{ns}c"):
                ref = c.attrib.get("r", "")
                ctype = c.attrib.get("t", "")
                v = c.find(f"{ns}v")
                if v is None:
                    continue
                val = v.text
                if ctype == "s":
                    val = shared[int(val)] if int(val) < len(shared) else ""
                col = re.match(r"([A-Z]+)", ref).group(1) if ref else ""
                r[col] = val
            rows.append(r)
        return rows

    # Sheet 1 = Roster (ideal break in col H, dietary in col N)
    roster = grid("xl/worksheets/sheet1.xml")
    ideal_breaks = {}
    dietary = {}
    for row in roster:
        name = (row.get("B") or "").strip()
        if not name or name.upper().startswith("GOLD GALA") or name.lower() == "name":
            continue
        ideal_breaks[name.lower()] = (row.get("H") or "").strip()
        dietary[name.lower()] = (row.get("N") or "").strip()

    # Sheet 2 = Check-In (expected arrival in col D)
    checkin = grid("xl/worksheets/sheet2.xml")
    call_times = {}
    for row in checkin:
        name = (row.get("A") or "").strip()
        if not name or name.lower() == "name":
            continue
        call_times[name.lower()] = (row.get("D") or "").strip()
    return call_times, ideal_breaks, dietary


def normalize_call_time(raw):
    """'Saturday, May 9 - 12 PM' or 'Saturday May 9 -- 11:30 AM' → '12:00 PM'."""
    if not raw:
        return ""
    m = re.search(r"(\d{1,2}(?::\d{2})?)\s*(AM|PM|am|pm)", raw)
    if not m:
        return ""
    t, ampm = m.group(1), m.group(2).upper()
    if ":" not in t:
        t += ":00"
    return f"{t} {ampm}"


def fmt_lead_cell(name, phone):
    """Build the role_leader cell from data.js fields."""
    if name and phone:
        return f"{name} — {phone}"
    if name:
        return name
    return "—"


def make_fte_entry(s, call_time_raw, ideal_break):
    """Build an info-sheet entry from data.js fields + Excel call_time.
    Used for staff who don't have a personalized .docx info sheet."""
    name = s["name"]
    return {
        "_name": name,
        "_slug": slugify(name),
        "role_title": "",
        "staff_call_time": normalize_call_time(call_time_raw),
        "assignments": [
            {"phase": "Pre-Event",                "time": "2:30–4:30 PM",   "role": "—",                                "location": "—", "role_leader": "—"},
            {"phase": "Cocktails",                "time": "4:30–6:30 PM",   "role": s.get("cocktails_role") or "—",     "location": "—",
             "role_leader": fmt_lead_cell(s.get("cocktails_lead_name"), s.get("cocktails_lead_phone"))},
            {"phase": "Transition to Dinner",     "time": "6:20–7:00 PM",   "role": "—",                                "location": "—", "role_leader": "—"},
            {"phase": "Dinner & Program",         "time": "7:00–9:30 PM",   "role": s.get("dinner_role") or "—",        "location": "—",
             "role_leader": fmt_lead_cell(s.get("dinner_lead_name"), s.get("dinner_lead_phone"))},
            {"phase": "Transition to Afterparty", "time": "~9:30–10:00 PM", "role": "—",                                "location": "—", "role_leader": "—"},
            {"phase": "Founders Party",           "time": "10:00 PM–1:00 AM","role": s.get("founders_role") or "—",     "location": "—",
             "role_leader": fmt_lead_cell(s.get("founders_lead_name"), s.get("founders_lead_phone"))},
        ],
        "assignment_notes": [],
        "role_descriptions": [],
        "ideal_break": (ideal_break or "").strip(),
    }


def main():
    files = sorted(os.listdir(SRC_DIR))
    files = [f for f in files if f.endswith(".txt")]
    parsed = []
    for f in files:
        path = os.path.join(SRC_DIR, f)
        try:
            entry = parse_file(path)
            parsed.append(entry)
        except Exception as e:
            print(f"FAILED {f}: {e}", file=sys.stderr)
            raise

    print(f"Parsed {len(parsed)} .docx files", file=sys.stderr)

    # Now generate FTE entries for staff in data.js but not in .docx-derived parsed list
    docx_slugs = {e["_slug"] for e in parsed}
    staff = read_data_js_staff(DATA_JS)
    call_times, ideal_breaks, dietary = read_excel_call_times_and_breaks()

    fte_entries = []
    missing_call_times = []
    for s in staff:
        slug = slugify(s["name"])
        if slug in docx_slugs:
            continue
        ct_raw = call_times.get(s["name"].lower(), "")
        ib = ideal_breaks.get(s["name"].lower(), "")
        if not ct_raw:
            missing_call_times.append(s["name"])
        fte_entries.append(make_fte_entry(s, ct_raw, ib))

    print(f"Generated {len(fte_entries)} FTE entries from data.js + Excel", file=sys.stderr)
    if missing_call_times:
        print(f"  WARN: no Excel call time for: {missing_call_times}", file=sys.stderr)

    # Combine; dedupe by slug just to be safe; sort by name
    combined = parsed + fte_entries
    combined.sort(key=lambda e: e["_name"].lower())
    parsed = combined

    # Build output JS
    out_lines = []
    out_lines.append("// Per-person info-sheet content extracted from .docx files in")
    out_lines.append("// /Individual Assignments/. Auto-generated by scripts/parse_info_sheets.py.")
    out_lines.append("// Re-run that script after the .docx files are updated.")
    out_lines.append("//")
    out_lines.append("// Schema:")
    out_lines.append("//   role_title         string")
    out_lines.append("//   staff_call_time    string  — fills the first timeline row")
    out_lines.append("//   assignments        array of { phase, time, role, location, role_leader }")
    out_lines.append("//   assignment_notes   array of strings")
    out_lines.append("//   role_descriptions  array of { title, sections, lead_name, lead_phone, lead_tel }")
    out_lines.append("//                      sections is an array of { heading, body? OR items? }")
    out_lines.append("//   additional_contacts  array of { name, role, phone, tel }")
    out_lines.append("//   ideal_break        string")
    out_lines.append("")
    out_lines.append("const STANDARD_CONTACTS = [")
    out_lines.append('  { name: "Joanna Lin",  role: "Staffing Lead",              phone: "734-674-6795", tel: "+17346746795" },')
    out_lines.append('  { name: "Linda Chu",   role: "Production / Gifting Lead",  phone: "860-398-0834", tel: "+18603980834" },')
    out_lines.append('  { name: "Rose Yan",    role: "EVP Marketing & Growth",     phone: "323-381-8898", tel: "+13233818898" },')
    out_lines.append("];")
    out_lines.append("")
    out_lines.append("window.GG_INFO_SHEETS = {")
    out_lines.append("")

    for entry in parsed:
        slug = entry["_slug"]
        name = entry["_name"]
        body = {k: v for k, v in entry.items() if not k.startswith("_")}
        body["additional_contacts"] = "__STANDARD_CONTACTS__"  # placeholder
        # JSON-serialize then post-process to swap the placeholder for the JS reference
        s = json.dumps(body, ensure_ascii=False, indent=2)
        # Re-indent so the object sits cleanly under the slug key
        s = "\n".join("  " + ln if ln else ln for ln in s.split("\n"))
        s = s.replace('"__STANDARD_CONTACTS__"', "STANDARD_CONTACTS")
        out_lines.append(f'  // {name}')
        out_lines.append(f'  "{slug}":')
        out_lines.append(s + ",")
        out_lines.append("")

    out_lines.append("};")

    out_text = "\n".join(out_lines) + "\n"
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(out_text)
    print(f"Wrote {OUT}", file=sys.stderr)
    print(f"  - entries: {len(parsed)}", file=sys.stderr)


if __name__ == "__main__":
    main()
