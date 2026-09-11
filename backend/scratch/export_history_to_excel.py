"""
WriteFlow Production History Export
====================================
Fetches all post history from the production backend:
  GET https://writeflow-yuwk.onrender.com/api/history

Exports to Excel with full post content preserved.
Run: python backend/scratch/export_history_to_excel.py
"""

import sys
import json
import math
import datetime
import urllib.request
import urllib.error

PRODUCTION_URL = "https://writeflow-yuwk.onrender.com"
HISTORY_ENDPOINT = f"{PRODUCTION_URL}/api/history"
LIMIT = 200  # max per the API (max allowed is 200)

# Output filename with timestamp
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_FILENAME = f"writeflow_history_export_{timestamp}.xlsx"


def fetch_history():
    """Fetch all history records from production /api/history."""
    url = f"{HISTORY_ENDPOINT}?limit={LIMIT}&skip=0"
    print(f"[1/3] Fetching production history from:\n      {url}")
    try:
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "WriteFlow-ExportScript/1.0"
            }
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read().decode("utf-8")
            data = json.loads(raw)
            print(f"      ✓ Response OK — {len(data)} records fetched")
            return data
    except urllib.error.HTTPError as e:
        print(f"      ✗ HTTP Error {e.code}: {e.reason}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"      ✗ Network Error: {e.reason}")
        print("      Make sure you are connected to the internet and the Render service is awake.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"      ✗ Failed to parse JSON response: {e}")
        sys.exit(1)


def try_import_openpyxl():
    """Check openpyxl is available, guide the user if not."""
    try:
        import openpyxl
        return openpyxl
    except ImportError:
        print("\n[ERROR] openpyxl is not installed.")
        print("Install it with:")
        print("  ..\\venv\\Scripts\\pip.exe install openpyxl")
        print("  -- or --")
        print("  pip install openpyxl")
        sys.exit(1)


def export_to_excel(records, openpyxl):
    """Write fetched records to a formatted Excel workbook."""
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Post History"

    # ── Column definitions ──────────────────────────────────────────────────
    columns = [
        ("id",              "ID",               20),
        ("created_at",      "Created At",       22),
        ("topic",           "Topic",            35),
        ("post_type",       "Post Type",        18),
        ("tone",            "Tone",             18),
        ("language",        "Language",         14),
        ("length",          "Length",           12),
        ("target_audience", "Target Audience",  25),
        ("writing_style",   "Writing Style",    30),
        ("personal_context","Personal Context", 35),
        ("key_points",      "Key Points",       30),
        ("post",            "Post Content",     70),
        ("word_count",      "Word Count",       12),
        ("reading_time",    "Reading Time",     15),
        ("emoji_count",     "Emoji Count",      13),
        ("hashtag_count",   "Hashtag Count",    14),
        ("action",          "Action",           15),
        ("parent_id",       "Parent ID",        20),
    ]

    # ── Header row styling ──────────────────────────────────────────────────
    header_fill   = PatternFill("solid", fgColor="0A66C2")
    header_font   = Font(color="FFFFFF", bold=True, name="Calibri", size=11)
    header_align  = Alignment(horizontal="center", vertical="center", wrap_text=False)
    thin_border   = Border(
        left=Side(style="thin", color="D0D7DE"),
        right=Side(style="thin", color="D0D7DE"),
        bottom=Side(style="medium", color="FFFFFF")
    )

    for col_idx, (_, header_label, col_width) in enumerate(columns, start=1):
        cell = ws.cell(row=1, column=col_idx, value=header_label)
        cell.font    = header_font
        cell.fill    = header_fill
        cell.alignment = header_align
        cell.border  = thin_border
        ws.column_dimensions[get_column_letter(col_idx)].width = col_width

    ws.row_dimensions[1].height = 22
    ws.freeze_panes = "A2"

    # ── Data rows ───────────────────────────────────────────────────────────
    data_align_wrap = Alignment(vertical="top", wrap_text=True)
    data_align_nowrap = Alignment(vertical="top", wrap_text=False)
    row_fill_even = PatternFill("solid", fgColor="F0F6FF")

    for row_idx, record in enumerate(records, start=2):
        fill = row_fill_even if row_idx % 2 == 0 else None
        for col_idx, (field_key, _, _) in enumerate(columns, start=1):
            value = record.get(field_key, "")
            if value is None:
                value = ""
            # For the post content column (index 12), use wrap text
            wrap = field_key in ("post", "topic", "personal_context", "key_points", "writing_style")
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.alignment = data_align_wrap if wrap else data_align_nowrap
            if fill:
                cell.fill = fill

        # Taller rows for post content readability
        post_text = record.get("post", "") or ""
        line_count = post_text.count("\n") + 1
        approx_height = max(18, min(line_count * 15, 120))
        ws.row_dimensions[row_idx].height = approx_height

    # ── Summary sheet ───────────────────────────────────────────────────────
    ws2 = wb.create_sheet("Export Summary")
    summary_font_bold = Font(bold=True, name="Calibri", size=11)
    summary_rows = [
        ("Export Date",       datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ("Source URL",        HISTORY_ENDPOINT),
        ("Total Records",     len(records)),
        ("Output File",       OUTPUT_FILENAME),
        ("Has Post Content",  "YES — full post text in 'Post Content' column"),
    ]
    for r_idx, (label, value) in enumerate(summary_rows, start=1):
        ws2.cell(row=r_idx, column=1, value=label).font = summary_font_bold
        ws2.cell(row=r_idx, column=2, value=value)
    ws2.column_dimensions["A"].width = 20
    ws2.column_dimensions["B"].width = 60

    wb.save(OUTPUT_FILENAME)
    return OUTPUT_FILENAME


def main():
    # Ensure stdout handles unicode on Windows
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print("=" * 60)
    print("  WriteFlow Production History -> Excel Export")
    print("=" * 60)

    # Step 1: fetch
    records = fetch_history()

    if not records:
        print("\n[WARN] No records returned from production. The database may be empty.")
        print("       (Render Free tier resets the DB on every deploy.)")
        sys.exit(0)

    # Step 2: check openpyxl
    print(f"\n[2/3] Checking openpyxl dependency...")
    openpyxl = try_import_openpyxl()
    print(f"      ✓ openpyxl {openpyxl.__version__} is available")

    # Step 3: export
    print(f"\n[3/3] Writing Excel file...")
    output = export_to_excel(records, openpyxl)
    print(f"      ✓ Saved: {output}")

    # ── Report ─────────────────────────────────────────────────────────────
    posts_with_content = sum(1 for r in records if r.get("post", "").strip())
    languages   = {}
    post_types  = {}
    for r in records:
        lang = r.get("language", "Unknown")
        pt   = r.get("post_type", "Unknown")
        languages[lang]   = languages.get(lang, 0) + 1
        post_types[pt]    = post_types.get(pt, 0) + 1

    print("\n" + "=" * 60)
    print("  Export Report")
    print("=" * 60)
    print(f"  Source URL    : {HISTORY_ENDPOINT}")
    print(f"  Records       : {len(records)}")
    print(f"  With content  : {posts_with_content}/{len(records)} have post_content")
    print(f"  Languages     : {dict(sorted(languages.items()))}")
    print(f"  Post Types    : {dict(sorted(post_types.items()))}")
    print(f"  Output File   : {output}")
    print(f"  Columns       : 18 (includes full Post Content)")
    print("=" * 60)
    print("\nDone. Open the Excel file to review your export.")


if __name__ == "__main__":
    main()
