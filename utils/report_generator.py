import csv
import os
from datetime import datetime


def _read_csv_rows(path):
    rows = []
    if not os.path.exists(path):
        return rows

    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows.extend(reader)

    return rows


def generate_html_report(results_folder, scenario, environment):
    stats_file = None
    failures_file = None

    for file_name in os.listdir(results_folder):
        if file_name.endswith("_stats.csv"):
            stats_file = os.path.join(results_folder, file_name)
        elif file_name.endswith("_failures.csv"):
            failures_file = os.path.join(results_folder, file_name)

    stats_rows = _read_csv_rows(stats_file) if stats_file else []
    failure_rows = _read_csv_rows(failures_file) if failures_file else []

    html_path = os.path.join(results_folder, "performance_report.html")

    summary_rows = []
    request_rows = []

    for row in stats_rows:
        name = row.get("Name", "")
        if name == "Aggregated":
            summary_rows.append(row)
        else:
            request_rows.append(row)

    generated_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = f"""
    <html>
    <head>
        <title>Performance Report - {scenario}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 24px;
            }}
            h1, h2 {{
                color: #222;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin-bottom: 24px;
            }}
            th, td {{
                border: 1px solid #ccc;
                padding: 8px;
                text-align: left;
                font-size: 13px;
            }}
            th {{
                background-color: #f3f3f3;
            }}
            .meta {{
                margin-bottom: 20px;
            }}
            .ok {{
                color: green;
                font-weight: bold;
            }}
            .warn {{
                color: darkorange;
                font-weight: bold;
            }}
            .bad {{
                color: red;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <h1>Performance Test Report</h1>

        <div class="meta">
            <p><strong>Scenario:</strong> {scenario}</p>
            <p><strong>Environment:</strong> {environment}</p>
            <p><strong>Generated On:</strong> {generated_on}</p>
        </div>

        <h2>Summary</h2>
        <table>
            <tr>
                <th>Type</th>
                <th>Name</th>
                <th># Requests</th>
                <th># Fails</th>
                <th>Median (ms)</th>
                <th>95%ile (ms)</th>
                <th>Average (ms)</th>
                <th>Current RPS</th>
            </tr>
    """

    for row in summary_rows:
        html += f"""
            <tr>
                <td>{row.get("Type", "")}</td>
                <td>{row.get("Name", "")}</td>
                <td>{row.get("# Requests", "")}</td>
                <td>{row.get("# Fails", "")}</td>
                <td>{row.get("Median Response Time", row.get("Median (ms)", ""))}</td>
                <td>{row.get("95%", row.get("95%ile (ms)", ""))}</td>
                <td>{row.get("Average Response Time", row.get("Average (ms)", ""))}</td>
                <td>{row.get("Requests/s", row.get("Current RPS", ""))}</td>
            </tr>
        """

    html += """
        </table>

        <h2>Request-Level Details</h2>
        <table>
            <tr>
                <th>Type</th>
                <th>Name</th>
                <th># Requests</th>
                <th># Fails</th>
                <th>Median (ms)</th>
                <th>95%ile (ms)</th>
                <th>Average (ms)</th>
            </tr>
    """

    for row in request_rows:
        html += f"""
            <tr>
                <td>{row.get("Type", "")}</td>
                <td>{row.get("Name", "")}</td>
                <td>{row.get("# Requests", "")}</td>
                <td>{row.get("# Fails", "")}</td>
                <td>{row.get("Median Response Time", row.get("Median (ms)", ""))}</td>
                <td>{row.get("95%", row.get("95%ile (ms)", ""))}</td>
                <td>{row.get("Average Response Time", row.get("Average (ms)", ""))}</td>
            </tr>
        """

    html += """
        </table>

        <h2>Failures</h2>
        <table>
            <tr>
                <th>Method</th>
                <th>Name</th>
                <th>Error</th>
                <th>Occurrences</th>
            </tr>
    """

    if failure_rows:
        for row in failure_rows:
            html += f"""
                <tr>
                    <td>{row.get("Method", "")}</td>
                    <td>{row.get("Name", "")}</td>
                    <td>{row.get("Error", "")}</td>
                    <td>{row.get("Occurrences", "")}</td>
                </tr>
            """
    else:
        html += """
            <tr>
                <td colspan="4">No failures recorded</td>
            </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    with open(html_path, "w", encoding="utf-8") as file:
        file.write(html)

    return html_path