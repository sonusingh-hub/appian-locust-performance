import csv
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors


def _read_stats_file(results_folder):
    stats_file = None

    for file_name in os.listdir(results_folder):
        if file_name.endswith("_stats.csv"):
            stats_file = os.path.join(results_folder, file_name)
            break

    if not stats_file:
        return []

    rows = []
    with open(stats_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows.extend(reader)

    return rows


def _pick(row, *keys, default=""):
    for key in keys:
        value = row.get(key, "")
        if value not in (None, ""):
            return value
    return default


def _to_float(value, default=0.0):
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (ValueError, TypeError):
        return default


def _to_int(value, default=0):
    try:
        if value is None or value == "":
            return default
        return int(float(value))
    except (ValueError, TypeError):
        return default


def _fmt_number(value, decimals=2):
    try:
        return f"{float(value):,.{decimals}f}"
    except (ValueError, TypeError):
        return str(value) if value not in (None, "") else "0"


def _fmt_ms(value):
    return f"{_fmt_number(value, 2)} ms"


def generate_pdf_summary(results_folder, scenario, environment):
    rows = _read_stats_file(results_folder)
    pdf_path = os.path.join(results_folder, "performance_summary.pdf")

    summary = None
    details = []

    for row in rows:
        if row.get("Name") == "Aggregated":
            summary = row
        else:
            details.append(row)

    # Sort details by average response time descending
    details = sorted(
        details,
        key=lambda row: _to_float(_pick(row, "Average Response Time", "Average (ms)", default=0)),
        reverse=True
    )

    total_requests = _to_int(_pick(summary or {}, "# Requests", "Request Count", default=0))
    total_failures = _to_int(_pick(summary or {}, "# Fails", "Failure Count", default=0))
    median_response = _to_float(_pick(summary or {}, "Median Response Time", "Median (ms)", default=0))
    p95_response = _to_float(_pick(summary or {}, "95%", "95%ile (ms)", default=0))
    avg_response = _to_float(_pick(summary or {}, "Average Response Time", "Average (ms)", default=0))
    throughput = _to_float(_pick(summary or {}, "Requests/s", "Current RPS", default=0))
    p99_response = _to_float(_pick(summary or {}, "99%", "99%ile (ms)", default=0))

    success_rate = 0.0
    if total_requests > 0:
        success_rate = ((total_requests - total_failures) / total_requests) * 100

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    y = height - 40

    left_margin = 40
    right_margin = width - 40
    usable_width = right_margin - left_margin

    def new_page():
        nonlocal y
        c.showPage()
        y = height - 40

    def ensure_space(required=40):
        nonlocal y
        if y < required:
            new_page()

    def write_line(text, x=40, size=10, gap=16, font="Helvetica", color=colors.black):
        nonlocal y
        ensure_space(60)
        c.setFont(font, size)
        c.setFillColor(color)
        c.drawString(x, y, text)
        y -= gap

    def draw_section_title(title):
        nonlocal y
        ensure_space(80)
        y -= 4
        c.setFillColor(colors.HexColor("#1f3c88"))
        c.setFont("Helvetica-Bold", 13)
        c.drawString(left_margin, y, title)
        y -= 10
        c.setStrokeColor(colors.HexColor("#d1d5db"))
        c.line(left_margin, y, right_margin, y)
        y -= 16

    def draw_kpi_box(x, y_top, w, h, title, value, value_color=colors.black):
        c.setFillColor(colors.white)
        c.setStrokeColor(colors.HexColor("#d9e2f2"))
        c.roundRect(x, y_top - h, w, h, 8, stroke=1, fill=1)

        c.setFillColor(colors.HexColor("#6b7280"))
        c.setFont("Helvetica", 8)
        c.drawString(x + 10, y_top - 16, title)

        c.setFillColor(value_color)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(x + 10, y_top - 34, value)

    def trim_text(text, max_len=55):
        text = str(text)
        return text if len(text) <= max_len else text[:max_len - 3] + "..."

    # Header
    c.setFillColor(colors.HexColor("#1f3c88"))
    c.roundRect(left_margin, y - 45, usable_width, 50, 10, stroke=0, fill=1)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(left_margin + 15, y - 18, "Performance Test Summary Report")

    c.setFont("Helvetica", 10)
    c.drawString(left_margin + 15, y - 34, f"Scenario: {scenario}   |   Environment: {environment}")

    y -= 70

    write_line(f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", size=10, gap=14)
    write_line(f"Results Folder: {results_folder}", size=10, gap=18, color=colors.HexColor("#4b5563"))

    # KPI Section
    draw_section_title("Overall Summary")

    box_width = (usable_width - 18) / 4
    box_height = 45
    box_y_top = y

    fail_color = colors.HexColor("#15803d") if total_failures == 0 else colors.HexColor("#dc2626")
    success_color = (
        colors.HexColor("#15803d") if success_rate >= 99
        else colors.HexColor("#d97706") if success_rate >= 95
        else colors.HexColor("#dc2626")
    )

    draw_kpi_box(left_margin, box_y_top, box_width, box_height, "Total Requests", str(total_requests), colors.HexColor("#2563eb"))
    draw_kpi_box(left_margin + box_width + 6, box_y_top, box_width, box_height, "Total Failures", str(total_failures), fail_color)
    draw_kpi_box(left_margin + (box_width + 6) * 2, box_y_top, box_width, box_height, "Success Rate", f"{success_rate:.2f}%", success_color)
    draw_kpi_box(left_margin + (box_width + 6) * 3, box_y_top, box_width, box_height, "Throughput", f"{throughput:.2f} RPS", colors.HexColor("#2563eb"))

    y -= 62

    write_line(f"Median Response Time: {_fmt_ms(median_response)}", size=10, gap=14)
    write_line(f"95th Percentile: {_fmt_ms(p95_response)}", size=10, gap=14)
    write_line(f"99th Percentile: {_fmt_ms(p99_response)}", size=10, gap=14)
    write_line(f"Average Response Time: {_fmt_ms(avg_response)}", size=10, gap=18)

    # Assessment
    draw_section_title("Assessment")

    if total_failures == 0 and p95_response <= 2000:
        assessment = "Healthy: no failures observed and response times are within a strong range."
        assessment_color = colors.HexColor("#15803d")
    elif total_failures <= max(1, total_requests * 0.01) and p95_response <= 5000:
        assessment = "Needs Review: test is broadly stable, but response time and/or limited failures should be reviewed."
        assessment_color = colors.HexColor("#d97706")
    else:
        assessment = "Critical: performance issues or failures were observed and need investigation."
        assessment_color = colors.HexColor("#dc2626")

    write_line(assessment, size=10, gap=18, font="Helvetica-Bold", color=assessment_color)

    # Top Requests
    draw_section_title("Top Request Metrics")

    ensure_space(120)

    table_x = left_margin
    col_positions = [table_x, table_x + 210, table_x + 295, table_x + 375, table_x + 450]
    row_height = 18

    c.setFillColor(colors.HexColor("#eef3fb"))
    c.rect(table_x, y - row_height + 4, usable_width, row_height, stroke=0, fill=1)

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(col_positions[0] + 2, y - 8, "Request Name")
    c.drawString(col_positions[1] + 2, y - 8, "Avg (ms)")
    c.drawString(col_positions[2] + 2, y - 8, "P95 (ms)")
    c.drawString(col_positions[3] + 2, y - 8, "Fails")
    c.drawString(col_positions[4] + 2, y - 8, "Status")

    y -= row_height

    count = 0
    for row in details:
        if count >= 12:
            break

        ensure_space(70)

        name = trim_text(row.get("Name", ""))
        avg = _to_float(_pick(row, "Average Response Time", "Average (ms)", default=0))
        p95 = _to_float(_pick(row, "95%", "95%ile (ms)", default=0))
        fails = _to_int(_pick(row, "# Fails", "Failure Count", default=0))

        if fails == 0 and p95 < 2000:
            status = "Healthy"
            status_color = colors.HexColor("#15803d")
        elif fails < 5 and p95 < 5000:
            status = "Needs Review"
            status_color = colors.HexColor("#d97706")
        else:
            status = "Critical"
            status_color = colors.HexColor("#dc2626")

        c.setStrokeColor(colors.HexColor("#e5e7eb"))
        c.line(table_x, y - 2, right_margin, y - 2)

        c.setFont("Helvetica", 8.5)
        c.setFillColor(colors.black)
        c.drawString(col_positions[0] + 2, y - 12, name)
        c.drawRightString(col_positions[2] - 8, y - 12, _fmt_number(avg, 2))
        c.drawRightString(col_positions[3] - 8, y - 12, _fmt_number(p95, 2))
        c.drawRightString(col_positions[4] - 20, y - 12, str(fails))

        c.setFillColor(status_color)
        c.drawString(col_positions[4] + 2, y - 12, status)

        y -= row_height
        count += 1

    # Notes
    y -= 10
    draw_section_title("Notes")

    write_line("• This PDF is a compact management summary of the Locust execution.", size=9, gap=13)
    write_line("• Refer to performance_report.html for richer charts and request-level analysis.", size=9, gap=13)
    write_line("• CSV artifacts remain the source data for detailed validation and trend review.", size=9, gap=13)

    c.save()
    return pdf_path