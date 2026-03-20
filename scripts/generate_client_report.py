"""
Client-facing consolidated performance test report generator.

Produces a single PDF covering discovered scenario runs with charts and
comparison tables.
"""

import argparse
import csv
import io
import os
import re
from datetime import datetime

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Image


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.dirname(SCRIPT_DIR)
DEFAULT_RESULTS_ROOT = os.path.join(WORKSPACE_ROOT, "results")
DEFAULT_MAX_RUNS = 5
ENCODINGS = ("utf-8-sig", "utf-8", "cp1252", "latin-1")

SCENARIO_USER_HINTS = {
    "smoke": 5,
    "smoke_10": 10,
    "baseline_25": 25,
    "baseline_50": 50,
    "baseline_100": 100,
    "standard": 200,
    "standard_200": 200,
    "peak": 300,
    "peak_300": 300,
    "stress400": 400,
    "stress_400": 400,
    "stress500": 500,
    "stress_500": 500,
    "spike": 300,
    "spike_300": 300,
}

KEY_OPS = [
    ("Login / Authentication", "Login.SubmitAuth"),
    ("Report Page Navigation", "reports.Nav"),
    ("Vehicle Search", "ClickStartProcessLink.Vehicle Search"),
    ("Vehicles On Order", "ClickClickableByText.Vehicles On Order"),
    ("Fleet Schedule", "ClickClickableByText.Fleet Schedule"),
    ("Imminent Contract Expiry", "ClickClickableByText.Imminent Contract Expiry"),
    ("Service Overdue", "ClickClickableByText.Service Overdue"),
    ("Vehicle Utilisation", "ClickClickableByText.Vehicle Utilisation"),
    ("Sustainability", "ClickClickableByText.Sustainability"),
    ("Alerts", "ClickClickableByText.Alerts"),
    ("Active Vehicles (card)", "ClickCardByText.Active Vehicles"),
    ("Delivery Overdue (card)", "ClickCardByText.Delivery Overdue"),
    ("Registration Overdue (card)", "ClickCardByText.Registration Overdue"),
]

NAVY = colors.HexColor("#1f3c88")
BLUE = colors.HexColor("#2563eb")
GREEN = colors.HexColor("#15803d")
ORANGE = colors.HexColor("#d97706")
RED = colors.HexColor("#dc2626")
GREY = colors.HexColor("#6b7280")
LGREY = colors.HexColor("#f3f4f6")
DGREY = colors.HexColor("#374151")
WHITE = colors.white
BLACK = colors.black
DIVIDER = colors.HexColor("#d1d5db")

MPL_LOW = "#2563eb"
MPL_HIGH = "#f97316"


def _read_csv(path):
    for encoding in ENCODINGS:
        try:
            with open(path, newline="", encoding=encoding) as file:
                return list(csv.DictReader(file))
        except UnicodeDecodeError:
            continue

    with open(path, newline="", encoding="utf-8", errors="replace") as file:
        return list(csv.DictReader(file))


def _float(row, *keys):
    for key in keys:
        value = row.get(key, "")
        if value not in (None, ""):
            try:
                return float(value)
            except ValueError:
                continue
    return 0.0


def _int(row, *keys):
    return int(_float(row, *keys))


def _avg(values):
    return sum(values) / len(values) if values else 0.0


def _format_dir_date(date_token):
    try:
        return datetime.strptime(date_token, "%Y%m%d").strftime("%d %b")
    except ValueError:
        return date_token


def _stats_file_for_run(results_root, run_dir_name, prefix):
    return os.path.join(results_root, run_dir_name, f"{prefix}_stats.csv")


def _parse_run_folder(name):
    parts = name.split("_")
    if len(parts) >= 3 and re.fullmatch(r"\d{8}", parts[-2]) and re.fullmatch(r"\d{6}", parts[-1]):
        scenario = "_".join(parts[:-2])
        return scenario, parts[-2], parts[-1]
    return name, "00000000", "000000"


def _infer_users(scenario_name, csv_prefix):
    if scenario_name in SCENARIO_USER_HINTS:
        return SCENARIO_USER_HINTS[scenario_name]
    if csv_prefix in SCENARIO_USER_HINTS:
        return SCENARIO_USER_HINTS[csv_prefix]

    match = re.search(r"(?:^|_)(\d+)$", csv_prefix)
    if match:
        return int(match.group(1))

    match = re.search(r"(\d+)$", scenario_name)
    if match:
        return int(match.group(1))

    return 0


def _parse_scenarios_arg(scenarios):
    if not scenarios:
        return []

    tokens = []
    for value in scenarios:
        for item in value.split(","):
            token = item.strip().lower()
            if token:
                tokens.append(token)
    return tokens


def _scenario_matches_filters(scenario_name, filters):
    if not filters:
        return True

    normalized = scenario_name.lower()
    for token in filters:
        if normalized == token:
            return True
        if normalized.startswith(f"{token}_"):
            return True
    return False


def discover_runs(results_root, max_runs=DEFAULT_MAX_RUNS, scenario_filters=None):
    if not os.path.isdir(results_root):
        return []

    discovered = []
    for name in os.listdir(results_root):
        full_path = os.path.join(results_root, name)
        if not os.path.isdir(full_path):
            continue

        stats_files = [file for file in os.listdir(full_path) if file.endswith("_stats.csv")]
        if not stats_files:
            continue

        stats_files.sort()
        stats_file = stats_files[0]
        csv_prefix = stats_file[: -len("_stats.csv")]
        scenario_name, date_token, time_token = _parse_run_folder(name)
        if not scenario_name:
            continue
        if not _scenario_matches_filters(scenario_name, scenario_filters or []):
            continue

        users = _infer_users(scenario_name, csv_prefix)

        discovered.append(
            {
                "dir": name,
                "scenario": scenario_name,
                "users": users,
                "prefix": csv_prefix,
                "date_token": date_token,
                "time_token": time_token,
            }
        )

    discovered.sort(key=lambda run: (run["date_token"], run["time_token"], run["dir"]))

    if max_runs and len(discovered) > max_runs:
        selected = discovered[-max_runs:]
    else:
        selected = list(discovered)

    sequence_by_scenario = {}
    for run in selected:
        sequence_by_scenario[run["scenario"]] = sequence_by_scenario.get(run["scenario"], 0) + 1
        run["sequence"] = sequence_by_scenario[run["scenario"]]
        run["label"] = f"{run['scenario']} - {run['users']}u R{run['sequence']}\n({_format_dir_date(run['date_token'])})"

    return selected


def load_run(results_root, run):
    stats_path = _stats_file_for_run(results_root, run["dir"], run["prefix"])
    rows = _read_csv(stats_path)
    aggregated = next((row for row in rows if row.get("Name") == "Aggregated"), None)
    details = {row["Name"]: row for row in rows if row.get("Name") != "Aggregated"}
    return aggregated, details


def find_op(details, pattern):
    for name, row in details.items():
        if pattern in name:
            return row
    return None


def build_operation_comparison(all_details_by_group, low_users, high_users):
    op_data = []
    low_group = all_details_by_group.get(low_users, [])
    high_group = all_details_by_group.get(high_users, [])

    for label, pattern in KEY_OPS:
        low_rows = [find_op(details, pattern) for details in low_group]
        high_rows = [find_op(details, pattern) for details in high_group]
        low_rows = [row for row in low_rows if row]
        high_rows = [row for row in high_rows if row]

        if not low_rows or not high_rows:
            continue

        median_low = _avg([_float(row, "Median Response Time") for row in low_rows])
        median_high = _avg([_float(row, "Median Response Time") for row in high_rows])
        p95_low = _avg([_float(row, "95%") for row in low_rows])
        p95_high = _avg([_float(row, "95%") for row in high_rows])
        delta = round(((median_high - median_low) / median_low) * 100) if median_low else 0

        op_data.append(
            {
                "label": label,
                "median_low": median_low,
                "median_high": median_high,
                "p95_low": p95_low,
                "p95_high": p95_high,
                "delta": delta,
            }
        )

    return op_data


def chart_aggregated_bar(run_data):
    labels = [run["label"].replace("\n", " ") for run in run_data]
    medians = [run["median"] / 1000 for run in run_data]
    avgs = [run["avg"] / 1000 for run in run_data]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(9, 3.5))
    median_bars = ax.bar(x - width / 2, medians, width, label="Median (s)", color=MPL_LOW, alpha=0.88)
    avg_bars = ax.bar(x + width / 2, avgs, width, label="Average (s)", color=MPL_HIGH, alpha=0.88)

    ax.set_ylabel("Response Time (seconds)", fontsize=9)
    ax.set_title("Median vs Average Response Time - All Runs", fontsize=10, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.legend(fontsize=8)
    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)

    for bar in list(median_bars) + list(avg_bars):
        ax.annotate(
            f"{bar.get_height():.1f}s",
            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            fontsize=7,
        )

    fig.tight_layout()
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=130)
    plt.close(fig)
    buffer.seek(0)
    return buffer


def chart_percentiles_line(run_data):
    labels = [run["label"].replace("\n", " ") for run in run_data]
    p50s = [run["p50"] / 1000 for run in run_data]
    p90s = [run["p90"] / 1000 for run in run_data]
    p95s = [run["p95"] / 1000 for run in run_data]

    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(9, 3.2))
    ax.plot(x, p50s, "o-", label="P50 (Median)", color="#2563eb", linewidth=2)
    ax.plot(x, p90s, "s-", label="P90", color="#f97316", linewidth=2)
    ax.plot(x, p95s, "^-", label="P95", color="#dc2626", linewidth=2)

    for index, values in enumerate(zip(p50s, p90s, p95s)):
        p50, p90, p95 = values
        ax.annotate(f"{p50:.1f}s", (index, p50), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=7, color="#2563eb")
        ax.annotate(f"{p90:.1f}s", (index, p90), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=7, color="#f97316")
        ax.annotate(f"{p95:.1f}s", (index, p95), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=7, color="#dc2626")

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("Response Time (seconds)", fontsize=9)
    ax.set_title("Response Time Percentiles Across Runs", fontsize=10, fontweight="bold")
    ax.legend(fontsize=8)
    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)

    fig.tight_layout()
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=130)
    plt.close(fig)
    buffer.seek(0)
    return buffer


def chart_ops_comparison(op_data, low_users, high_users):
    labels = [item["label"] for item in op_data]
    low_values = [item["median_low"] / 1000 for item in op_data]
    high_values = [item["median_high"] / 1000 for item in op_data]

    y = np.arange(len(labels))
    height = 0.35

    fig, ax = plt.subplots(figsize=(9, max(4, len(labels) * 0.55)))
    ax.barh(y + height / 2, low_values, height, label=f"{low_users} Users", color=MPL_LOW, alpha=0.88)
    ax.barh(y - height / 2, high_values, height, label=f"{high_users} Users", color=MPL_HIGH, alpha=0.88)

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlabel("Median Response Time (seconds)", fontsize=9)
    ax.set_title(f"{low_users} Users vs {high_users} Users - Median Response Time per Operation", fontsize=10, fontweight="bold")
    ax.legend(fontsize=8)
    ax.xaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)

    for index, values in enumerate(zip(low_values, high_values)):
        low_value, high_value = values
        ax.text(low_value + 0.1, index + height / 2, f"{low_value:.1f}s", va="center", fontsize=7, color="#1e3a8a")
        ax.text(high_value + 0.1, index - height / 2, f"{high_value:.1f}s", va="center", fontsize=7, color="#9a3412")

    fig.tight_layout()
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=130)
    plt.close(fig)
    buffer.seek(0)
    return buffer


class PDFReport:
    def __init__(self, path):
        self.path = path
        self.c = canvas.Canvas(path, pagesize=A4)
        self.width, self.height = A4
        self.lm = 30 * mm
        self.rm = self.width - 30 * mm
        self.uw = self.rm - self.lm
        self.y = self.height - 40
        self.page_num = 0
        self._start_page()

    def _start_page(self):
        self.page_num += 1
        self.y = self.height - 40

    def new_page(self):
        self._draw_footer()
        self.c.showPage()
        self._start_page()

    def _draw_footer(self):
        self.c.setFont("Helvetica", 7)
        self.c.setFillColor(GREY)
        self.c.drawString(self.lm, 18, "APAC Reporting - Performance Test Results | Confidential")
        self.c.drawRightString(self.rm, 18, f"Page {self.page_num}")
        self.c.setStrokeColor(DIVIDER)
        self.c.line(self.lm, 25, self.rm, 25)

    def ensure(self, needed=40):
        if self.y < needed + 30:
            self.new_page()

    def section(self, title):
        self.ensure(80)
        self.y -= 6
        self.c.setFillColor(NAVY)
        self.c.setFont("Helvetica-Bold", 12)
        self.c.drawString(self.lm, self.y, title)
        self.y -= 8
        self.c.setStrokeColor(BLUE)
        self.c.setLineWidth(1.5)
        self.c.line(self.lm, self.y, self.rm, self.y)
        self.c.setLineWidth(1)
        self.y -= 14

    def line(self, text, size=9.5, gap=14, font="Helvetica", color=BLACK, x=None):
        self.ensure(gap + 20)
        self.c.setFont(font, size)
        self.c.setFillColor(color)
        self.c.drawString(x or self.lm, self.y, text)
        self.y -= gap

    def bullet(self, text, size=9, gap=13, color=BLACK, indent=8):
        self.ensure(gap + 20)
        self.c.setFont("Helvetica", size)
        self.c.setFillColor(BLUE)
        self.c.drawString(self.lm + indent, self.y, "-")
        self.c.setFillColor(color)
        max_len = 105
        if len(text) <= max_len:
            self.c.drawString(self.lm + indent + 10, self.y, text)
            self.y -= gap
            return

        words = text.split()
        current = ""
        first = True
        for word in words:
            if len(current) + len(word) + 1 <= max_len:
                current = (current + " " + word).strip()
                continue
            x_pos = self.lm + indent + (10 if first else 20)
            self.c.drawString(x_pos, self.y, current)
            self.y -= gap
            self.ensure(gap + 20)
            current = word
            first = False
        if current:
            x_pos = self.lm + indent + (10 if first else 20)
            self.c.drawString(x_pos, self.y, current)
            self.y -= gap

    def hline(self, gap=10):
        self.y -= gap / 2
        self.c.setStrokeColor(DIVIDER)
        self.c.line(self.lm, self.y, self.rm, self.y)
        self.y -= gap / 2

    def kpi_boxes(self, items):
        count = len(items)
        box_width = (self.uw - 5 * (count - 1)) / count
        box_height = 42
        self.ensure(box_height + 20)
        for index, (label, value, value_color) in enumerate(items):
            box_x = self.lm + index * (box_width + 5)
            box_y = self.y - box_height
            self.c.setFillColor(WHITE)
            self.c.setStrokeColor(colors.HexColor("#bfdbfe"))
            self.c.roundRect(box_x, box_y, box_width, box_height, 6, stroke=1, fill=1)
            self.c.setFillColor(GREY)
            self.c.setFont("Helvetica", 7.5)
            self.c.drawString(box_x + 8, self.y - 13, label)
            self.c.setFillColor(value_color)
            self.c.setFont("Helvetica-Bold", 13)
            self.c.drawString(box_x + 8, self.y - 30, str(value))
        self.y -= box_height + 10

    def table_header(self, columns, x_positions, row_height=16):
        self.ensure(row_height + 30)
        self.c.setFillColor(colors.HexColor("#1e3a8a"))
        self.c.rect(self.lm, self.y - row_height + 4, self.uw, row_height, stroke=0, fill=1)
        self.c.setFillColor(WHITE)
        self.c.setFont("Helvetica-Bold", 8)
        for index, (column, x_pos) in enumerate(zip(columns, x_positions)):
            if index + 1 < len(x_positions):
                col_width = x_positions[index + 1] - x_pos
            else:
                col_width = self.rm - x_pos
            text = self._fit_text(column, max(col_width - 4, 8), "Helvetica-Bold", 8)
            self.c.drawString(x_pos + 2, self.y - row_height + 7, text)
        self.y -= row_height

    def table_row(self, cells, x_positions, row_height=15, alt=False, cell_colors=None):
        self.ensure(row_height + 20)
        if alt:
            self.c.setFillColor(LGREY)
            self.c.rect(self.lm, self.y - row_height + 4, self.uw, row_height, stroke=0, fill=1)
        self.c.setStrokeColor(DIVIDER)
        self.c.line(self.lm, self.y - row_height + 4, self.rm, self.y - row_height + 4)
        self.c.setFont("Helvetica", 8)
        for index, (cell, x_pos) in enumerate(zip(cells, x_positions)):
            if index + 1 < len(x_positions):
                col_width = x_positions[index + 1] - x_pos
            else:
                col_width = self.rm - x_pos
            text_color = BLACK
            if cell_colors and cell_colors[index]:
                text_color = cell_colors[index]
            self.c.setFillColor(text_color)
            text = self._fit_text(str(cell), max(col_width - 4, 8), "Helvetica", 8)
            self.c.drawString(x_pos + 2, self.y - row_height + 7, text)
        self.y -= row_height

    def _fit_text(self, text, max_width, font_name, font_size):
        if self.c.stringWidth(text, font_name, font_size) <= max_width:
            return text
        if max_width <= self.c.stringWidth("...", font_name, font_size):
            return "..."

        trimmed = text
        while trimmed and self.c.stringWidth(trimmed + "...", font_name, font_size) > max_width:
            trimmed = trimmed[:-1]
        return (trimmed + "...") if trimmed else "..."

    def insert_chart(self, buffer, width_points, height_points):
        self.ensure(height_points + 20)
        Image(buffer, width=width_points, height=height_points).drawOn(self.c, self.lm, self.y - height_points)
        self.y -= height_points + 12

    def save(self):
        self._draw_footer()
        self.c.save()


def build_findings(run_data, op_data, low_users, high_users):
    findings = []
    total_requests = sum(run["rc"] for run in run_data)
    total_failures = sum(run["fc"] for run in run_data)

    positive = [f"Processed {total_requests:,} requests across {len(run_data)} baseline runs with {total_failures} failures."]
    if total_failures == 0:
        positive.append("No request failures were recorded in any included run, indicating strong functional stability.")

    grouped = {}
    for run in run_data:
        grouped.setdefault(run["users"], []).append(run)
    for users, group in sorted(grouped.items()):
        if len(group) > 1:
            medians = [run["median"] / 1000 for run in group]
            positive.append(
                f"{users}-user baselines were repeatable across {len(group)} runs with median response times between {min(medians):.1f}s and {max(medians):.1f}s."
            )
    findings.append(("POSITIVE", GREEN, positive))

    review = []
    slowest_ops = sorted(op_data, key=lambda item: item["median_high"], reverse=True)[:3]
    if slowest_ops:
        ops_text = ", ".join(f"{item['label']} ({item['median_high'] / 1000:.1f}s)" for item in slowest_ops)
        review.append(f"Slowest operations at {high_users} users were {ops_text} based on average median response time.")

    low_group = grouped.get(low_users, [])
    high_group = grouped.get(high_users, [])
    if low_group and high_group and low_users != high_users:
        low_median = _avg([run["median"] for run in low_group])
        high_median = _avg([run["median"] for run in high_group])
        low_rps = _avg([run["rps"] for run in low_group])
        high_rps = _avg([run["rps"] for run in high_group])
        median_delta = round(((high_median - low_median) / low_median) * 100) if low_median else 0
        throughput_delta = round(((high_rps - low_rps) / low_rps) * 100) if low_rps else 0
        review.append(
            f"Moving from {low_users} to {high_users} users increased average median response time by {median_delta}% while throughput improved by {throughput_delta}%."
        )

    login_op = next((item for item in op_data if item["label"] == "Login / Authentication"), None)
    if login_op:
        review.append(
            f"Login / Authentication increased from {login_op['median_low'] / 1000:.1f}s to {login_op['median_high'] / 1000:.1f}s across the comparison loads and should be reviewed separately from report execution."
        )
    findings.append(("AREAS TO REVIEW", ORANGE, review or ["No major performance hot spots were detected in the comparison set."]))

    trend_items = []
    highest_load_runs = grouped.get(high_users, [])
    if len(highest_load_runs) > 1:
        medians = [run["median"] / 1000 for run in highest_load_runs]
        if medians[-1] > medians[0]:
            trend_items.append(
                f"At {high_users} users, median response time moved from {medians[0]:.1f}s to {medians[-1]:.1f}s across consecutive runs and should be monitored in longer endurance testing."
            )
    if not trend_items:
        trend_items.append("No sustained degradation pattern was strong enough to classify as a confirmed endurance issue from the included runs alone.")
    findings.append(("TREND TO MONITOR", RED, trend_items))

    return findings


def generate_report(results_root, output_pdf, max_runs=DEFAULT_MAX_RUNS, scenarios=None):
    scenario_filters = _parse_scenarios_arg(scenarios)
    runs = discover_runs(results_root, max_runs=max_runs, scenario_filters=scenario_filters)
    if not runs:
        if scenario_filters:
            filters_text = ", ".join(scenario_filters)
            raise SystemExit(
                f"No matching scenario result folders with stats CSVs were found under: {results_root} "
                f"for filters: {filters_text}"
            )
        raise SystemExit(f"No scenario result folders with stats CSVs were found under: {results_root}")

    print("Loading run data...")
    report_date = datetime.now().strftime("%d %B %Y")
    run_data = []
    all_details = []
    all_details_by_group = {}

    for run in runs:
        aggregated, details = load_run(results_root, run)
        if not aggregated:
            continue

        summary = {
            "dir": run["dir"],
            "scenario": run["scenario"],
            "label": run["label"],
            "users": run["users"],
            "sequence": run["sequence"],
            "date": run["date_token"],
            "rc": _int(aggregated, "Request Count", "# Requests"),
            "fc": _int(aggregated, "Failure Count", "# Fails"),
            "median": _float(aggregated, "Median Response Time", "Median (ms)"),
            "avg": _float(aggregated, "Average Response Time", "Average (ms)"),
            "p50": _float(aggregated, "50%"),
            "p90": _float(aggregated, "90%"),
            "p95": _float(aggregated, "95%"),
            "p99": _float(aggregated, "99%"),
            "rps": _float(aggregated, "Requests/s"),
            "max": _float(aggregated, "Max Response Time"),
        }
        run_data.append(summary)
        all_details.append(details)
        all_details_by_group.setdefault(run["users"], []).append(details)

    if not run_data:
        raise SystemExit(f"No aggregated stats rows were found under: {results_root}")

    users_available = sorted(all_details_by_group)
    low_users = users_available[0]
    high_users = users_available[-1]
    op_data = build_operation_comparison(all_details_by_group, low_users, high_users)

    print("Generating charts...")
    chart_summary = chart_aggregated_bar(run_data)
    chart_percentiles = chart_percentiles_line(run_data)
    chart_comparison = chart_ops_comparison(op_data, low_users, high_users) if op_data else None
    findings = build_findings(run_data, op_data, low_users, high_users)

    date_tokens = sorted({run["date"] for run in run_data})
    if len(date_tokens) == 1:
        test_date_text = _format_dir_date(date_tokens[0])
    else:
        test_date_text = f"{_format_dir_date(date_tokens[0])} to {_format_dir_date(date_tokens[-1])}"

    print("Building PDF...")
    output_dir = os.path.dirname(output_pdf)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    pdf = PDFReport(output_pdf)
    c = pdf.c
    width, height = pdf.width, pdf.height

    c.setFillColor(NAVY)
    c.rect(0, height - 160, width, 160, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(pdf.lm, height - 60, "APAC Reporting Platform")
    c.setFont("Helvetica-Bold", 18)
    c.drawString(pdf.lm, height - 85, "Performance Baseline Test Report")
    c.setFont("Helvetica", 11)
    c.drawString(pdf.lm, height - 108, f"Consolidated scenario load testing across {len(run_data)} runs")
    c.setFont("Helvetica", 10)
    c.drawString(pdf.lm, height - 126, f"Test dates: {test_date_text} | Report date: {report_date}")
    c.setFillColor(colors.HexColor("#f97316"))
    c.rect(pdf.lm, height - 170, 60, 5, stroke=0, fill=1)

    pdf.y = height - 210
    pdf.section("Executive Snapshot")

    grouped_runs = {}
    for run in run_data:
        grouped_runs.setdefault(run["users"], []).append(run)

    total_requests = sum(run["rc"] for run in run_data)
    total_failures = sum(run["fc"] for run in run_data)
    user_label = ", ".join(str(users) for users in users_available)
    pdf.kpi_boxes(
        [
            ("Total Requests", f"{total_requests:,}", BLUE),
            ("Total Failures", str(total_failures), GREEN if total_failures == 0 else RED),
            ("Overall Error Rate", f"{(total_failures / total_requests * 100) if total_requests else 0:.2f}%", GREEN if total_failures == 0 else RED),
            ("Runs Included", str(len(run_data)), NAVY),
        ]
    )

    second_row = []
    for users in users_available[:2]:
        avg_median = _avg([run["median"] for run in grouped_runs[users]]) / 1000
        value_color = colors.HexColor(MPL_LOW if users == low_users else MPL_HIGH)
        second_row.append((f"Avg Median - {users} Users", f"{avg_median:.1f}s", value_color))
    while len(second_row) < 3:
        second_row.append(("Users Covered", user_label, NAVY))
    second_row.append(("User Loads", user_label, NAVY))
    pdf.kpi_boxes(second_row[:4])

    pdf.y -= 6
    pdf.line("Test Objective", size=10, font="Helvetica-Bold", gap=14, color=NAVY)
    pdf.line(
        "Establish a performance baseline for the APAC Reporting platform using discovered scenario result folders",
        size=9,
        gap=13,
        color=DGREY,
    )
    pdf.line(
        "and compare end-to-end response times across major report journeys and load levels.",
        size=9,
        gap=16,
        color=DGREY,
    )
    pdf.line("Scope of Testing", size=10, font="Helvetica-Bold", gap=14, color=NAVY)
    for item in [
        "Login and Authentication",
        "Report navigation: Alerts, Fleet Schedule, Imminent Contract Expiry, Service Overdue, Sustainability, Vehicle Utilisation, Vehicles On Order",
        "Dashboard card drill-downs: Active Vehicles, Delivery Overdue, Registration Overdue",
        "Vehicle Search, dropdown interactions, grid paging, data export and refresh",
    ]:
        pdf.bullet(item, size=9, gap=13)
    pdf.hline(18)
    pdf.line("Disclaimer", size=8.5, font="Helvetica-Bold", gap=12, color=GREY)
    pdf.line(
        "Response times represent end-to-end timings from the load generator to the application server,",
        size=8,
        gap=11,
        color=GREY,
    )
    pdf.line(
        "including network travel and server-side processing.",
        size=8,
        gap=11,
        color=GREY,
    )
    pdf.line(
        "Relative comparisons between runs and load levels remain valid because the same execution path",
        size=8,
        gap=11,
        color=GREY,
    )
    pdf.line(
        "is used throughout the test set.",
        size=8,
        gap=11,
        color=GREY,
    )

    pdf.new_page()
    pdf.section("Test Runs - Aggregated Summary")
    col_labels = ["Run", "Users", "Requests", "Failures", "Error %", "Median", "P95", "P99", "Throughput"]
    col_widths = [110, 28, 46, 36, 36, 38, 34, 34, 63]
    x_pos = [pdf.lm]
    for width in col_widths[:-1]:
        x_pos.append(x_pos[-1] + width)
    pdf.table_header(col_labels, x_pos, row_height=16)

    for index, run in enumerate(run_data):
        failure_rate = round(run["fc"] / run["rc"] * 100, 2) if run["rc"] else 0
        cells = [
            run["label"].replace("\n", " "),
            str(run["users"]),
            f"{run['rc']:,}",
            str(run["fc"]),
            f"{failure_rate:.2f}%",
            f"{run['median'] / 1000:.1f}s",
            f"{run['p95'] / 1000:.1f}s",
            f"{run['p99'] / 1000:.1f}s",
            f"{run['rps']:.2f}/s",
        ]
        failure_color = GREEN if run["fc"] == 0 else RED
        pdf.table_row(cells, x_pos, row_height=15, alt=(index % 2 == 1), cell_colors=[None, None, None, failure_color, failure_color, None, None, None, None])

    pdf.y -= 8
    pdf.section("Response Time Trends - All Runs")
    pdf.insert_chart(chart_summary, pdf.uw, 165)
    pdf.insert_chart(chart_percentiles, pdf.uw, 155)

    if chart_comparison:
        pdf.new_page()
        pdf.section(f"{low_users} Users vs {high_users} Users - Per-Operation Comparison")
        pdf.line(
            "Operation medians are averaged within each user-load group when multiple runs are present.",
            size=8.5,
            gap=14,
            color=GREY,
        )
        col2 = ["Operation", f"Median {low_users}u", f"Median {high_users}u", "Delta", f"P95 {low_users}u", f"P95 {high_users}u", "Impact"]
        x2 = [pdf.lm, pdf.lm + 148, pdf.lm + 200, pdf.lm + 254, pdf.lm + 295, pdf.lm + 340, pdf.lm + 385]
        pdf.table_header(col2, x2, row_height=16)

        for index, op in enumerate(op_data):
            if op["delta"] <= 50:
                impact, impact_color = "Low", GREEN
            elif op["delta"] <= 100:
                impact, impact_color = "Moderate", ORANGE
            else:
                impact, impact_color = "High", RED

            delta_color = GREEN if op["delta"] <= 50 else ORANGE if op["delta"] <= 100 else RED
            cells = [
                op["label"][:38],
                f"{op['median_low'] / 1000:.1f}s",
                f"{op['median_high'] / 1000:.1f}s",
                f"+{op['delta']}%",
                f"{op['p95_low'] / 1000:.1f}s",
                f"{op['p95_high'] / 1000:.1f}s",
                impact,
            ]
            pdf.table_row(cells, x2, row_height=15, alt=(index % 2 == 1), cell_colors=[None, None, None, delta_color, None, None, impact_color])

        pdf.y -= 10
        pdf.section(f"{low_users} Users vs {high_users} Users - Visual Comparison")
        pdf.insert_chart(chart_comparison, pdf.uw, 220)

    pdf.new_page()
    pdf.section("Key Findings")
    for category, category_color, items in findings:
        pdf.ensure(60)
        pdf.y -= 4
        c.setFillColor(category_color)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(pdf.lm, pdf.y, f"[ {category} ]")
        pdf.y -= 14
        for item in items:
            pdf.bullet(item, size=8.5, gap=12, color=DGREY)
        pdf.y -= 6

    pdf.section("Recommendations")
    for recommendation in [
        "Review the slowest report journeys identified in this summary and profile the underlying database queries or record aggregations.",
        "Treat authentication separately from report execution, because login delays can materially affect user perception before report pages are reached.",
        f"Run a longer endurance test at {high_users} users if you want to confirm whether the highest observed load degrades further over time.",
        "Expand the baseline set to include higher user loads only after the current slowest operations have been reviewed, so later results isolate capacity rather than known hot spots.",
        "Use the per-run HTML and PDF artifacts alongside this consolidated PDF when you need request-level detail behind a summarized finding.",
    ]:
        pdf.bullet(recommendation, size=8.5, gap=13, color=DGREY)

    pdf.new_page()
    pdf.section("Appendix - Detailed Metrics Comparison")
    pdf.line(
        f"Latest {len(run_data)} discovered scenario runs are shown below. Values are median response time in seconds.",
        size=8.5,
        gap=14,
        color=GREY,
    )

    appendix_columns = ["Operation"] + [f"{run['scenario']} R{run['sequence']}" for run in run_data]
    appendix_first_col_width = 145
    appendix_positions = [pdf.lm]
    appendix_positions.append(pdf.lm + appendix_first_col_width)
    appendix_run_count = max(len(run_data), 1)
    appendix_run_col_width = (pdf.uw - appendix_first_col_width) / appendix_run_count
    for _ in range(max(appendix_run_count - 1, 0)):
        appendix_positions.append(appendix_positions[-1] + appendix_run_col_width)
    pdf.table_header(appendix_columns, appendix_positions[: len(appendix_columns)], row_height=16)
    for index, (label, pattern) in enumerate(KEY_OPS):
        cells = [label[:34]]
        for details in all_details:
            row = find_op(details, pattern)
            cells.append(f"{_float(row, 'Median Response Time') / 1000:.1f}s" if row else "-")
        pdf.table_row(cells, appendix_positions[: len(cells)], row_height=14, alt=(index % 2 == 1))

    pdf.y -= 12
    pdf.section("Appendix - Overall Aggregated Stats")
    metric_columns = ["Metric"] + [f"{run['scenario']} R{run['sequence']}" for run in run_data]
    metric_first_col_width = 100
    metric_positions = [pdf.lm]
    metric_positions.append(pdf.lm + metric_first_col_width)
    metric_run_count = max(len(run_data), 1)
    metric_run_col_width = (pdf.uw - metric_first_col_width) / metric_run_count
    for _ in range(max(metric_run_count - 1, 0)):
        metric_positions.append(metric_positions[-1] + metric_run_col_width)
    pdf.table_header(metric_columns, metric_positions[: len(metric_columns)], row_height=16)
    metrics = [
        ("Total Requests", lambda run: f"{run['rc']:,}"),
        ("Failures", lambda run: str(run["fc"])),
        ("Throughput", lambda run: f"{run['rps']:.2f}/s"),
        ("Median", lambda run: f"{run['median'] / 1000:.1f}s"),
        ("Average", lambda run: f"{run['avg'] / 1000:.1f}s"),
        ("P50", lambda run: f"{run['p50'] / 1000:.1f}s"),
        ("P90", lambda run: f"{run['p90'] / 1000:.1f}s"),
        ("P95", lambda run: f"{run['p95'] / 1000:.1f}s"),
        ("P99", lambda run: f"{run['p99'] / 1000:.1f}s"),
        ("Max", lambda run: f"{run['max'] / 1000:.1f}s"),
    ]
    for index, (name, formatter) in enumerate(metrics):
        cells = [name] + [formatter(run) for run in run_data]
        pdf.table_row(cells, metric_positions[: len(cells)], row_height=14, alt=(index % 2 == 1))

    pdf.save()
    return output_pdf


def parse_args():
    parser = argparse.ArgumentParser(description="Generate a consolidated client PDF from Locust scenario results.")
    parser.add_argument("--results-root", default=DEFAULT_RESULTS_ROOT, help="Folder containing scenario result subdirectories.")
    parser.add_argument("--output", default=None, help="Output PDF path. Defaults to <results-root>/apac_performance_report.pdf")
    parser.add_argument(
        "--max-runs",
        type=int,
        default=DEFAULT_MAX_RUNS,
        help="Maximum number of latest runs to include globally after scenario filtering.",
    )
    parser.add_argument(
        "--scenarios",
        nargs="+",
        default=None,
        help="Optional scenario filter list. Supports comma-separated or space-separated values, e.g. baseline,smoke baseline_25",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    results_root = os.path.abspath(args.results_root)
    output_pdf = os.path.abspath(args.output or os.path.join(results_root, "apac_performance_report.pdf"))
    report_path = generate_report(results_root=results_root, output_pdf=output_pdf, max_runs=args.max_runs, scenarios=args.scenarios)
    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()
