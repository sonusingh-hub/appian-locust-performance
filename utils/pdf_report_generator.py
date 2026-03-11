import csv
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


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

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    y = height - 40

    def write_line(text, size=10, gap=16):
        nonlocal y
        c.setFont("Helvetica", size)
        c.drawString(40, y, text)
        y -= gap

    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y, "Performance Test Summary Report")
    y -= 24

    write_line(f"Scenario: {scenario}", 11)
    write_line(f"Environment: {environment}", 11)
    write_line(f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 11)
    y -= 8

    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Overall Summary")
    y -= 18

    if summary:
        write_line(f"Requests: {summary.get('# Requests', '')}")
        write_line(f"Failures: {summary.get('# Fails', '')}")
        write_line(f"Median Response Time: {summary.get('Median Response Time', summary.get('Median (ms)', ''))} ms")
        write_line(f"95th Percentile: {summary.get('95%', summary.get('95%ile (ms)', ''))} ms")
        write_line(f"Average Response Time: {summary.get('Average Response Time', summary.get('Average (ms)', ''))} ms")
        write_line(f"Throughput: {summary.get('Requests/s', summary.get('Current RPS', ''))}")
    else:
        write_line("No aggregate summary found.")

    y -= 8
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Top Request Metrics")
    y -= 18

    count = 0
    for row in details:
        if count >= 10:
            break

        name = row.get("Name", "")
        avg = row.get("Average Response Time", row.get("Average (ms)", ""))
        p95 = row.get("95%", row.get("95%ile (ms)", ""))
        fails = row.get("# Fails", "")

        line = f"{name} | Avg: {avg} ms | P95: {p95} ms | Fails: {fails}"
        write_line(line, 9, 14)
        count += 1

        if y < 60:
            c.showPage()
            y = height - 40

    c.save()
    return pdf_path