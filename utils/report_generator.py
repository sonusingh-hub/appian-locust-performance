import csv
import os
import json
import html as html_lib
import webbrowser
from datetime import datetime


def _read_csv_rows(path):
    rows = []
    if not path or not os.path.exists(path):
        return rows

    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows.extend(reader)

    return rows


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


def _pick(row, *keys, default=""):
    for key in keys:
        value = row.get(key, "")
        if value not in (None, ""):
            return value
    return default


def generate_html_report(results_folder, scenario, environment, auto_open=True):
    stats_file = None
    failures_file = None
    history_file = None

    for file_name in os.listdir(results_folder):
        if file_name.endswith("_stats.csv"):
            stats_file = os.path.join(results_folder, file_name)
        elif file_name.endswith("_failures.csv"):
            failures_file = os.path.join(results_folder, file_name)
        elif file_name.endswith("_stats_history.csv"):
            history_file = os.path.join(results_folder, file_name)

    stats_rows = _read_csv_rows(stats_file) if stats_file else []
    failure_rows = _read_csv_rows(failures_file) if failures_file else []
    history_rows = _read_csv_rows(history_file) if history_file else []

    html_path = os.path.abspath(os.path.join(results_folder, "performance_report.html"))

    summary_rows = []
    request_rows = []

    for row in stats_rows:
        name = row.get("Name", "")
        if name == "Aggregated":
            summary_rows.append(row)
        else:
            request_rows.append(row)

    generated_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    summary_row = summary_rows[0] if summary_rows else {}

    total_requests = _to_int(_pick(summary_row, "# Requests", "Request Count", default=0))
    total_failures = _to_int(_pick(summary_row, "# Fails", "Failure Count", default=0))
    avg_response = _to_float(_pick(summary_row, "Average Response Time", "Average (ms)", default=0))
    median_response = _to_float(_pick(summary_row, "Median Response Time", "Median (ms)", default=0))
    p95_response = _to_float(_pick(summary_row, "95%", "95%ile (ms)", default=0))
    p99_response = _to_float(_pick(summary_row, "99%", "99%ile (ms)", default=0))
    current_rps = _to_float(_pick(summary_row, "Requests/s", "Current RPS", default=0))

    success_rate = 0.0
    if total_requests > 0:
        success_rate = round(((total_requests - total_failures) / total_requests) * 100, 2)

    percentile_labels = ["Median", "Average", "P95", "P99"]
    percentile_values = [median_response, avg_response, p95_response, p99_response]

    request_chart_names = []
    request_chart_avg = []
    request_chart_p95 = []

    request_rows_sorted = sorted(
        request_rows,
        key=lambda row: _to_float(_pick(row, "Average Response Time", "Average (ms)", default=0)),
        reverse=True
    )

    for row in request_rows_sorted[:12]:
        request_chart_names.append(_pick(row, "Name", default=""))
        request_chart_avg.append(_to_float(_pick(row, "Average Response Time", "Average (ms)", default=0)))
        request_chart_p95.append(_to_float(_pick(row, "95%", "95%ile (ms)", default=0)))

    time_labels = []
    rps_values = []
    response_time_values = []
    failure_values = []

    for row in history_rows:
        history_name = row.get("Name", "")
        if history_name not in ("Aggregated", ""):
            continue

        timestamp = row.get("Timestamp", "")
        if not timestamp:
            continue

        label = timestamp.split(" ")[-1] if " " in timestamp else timestamp

        time_labels.append(label)
        rps_values.append(_to_float(_pick(row, "Requests/s", "Current RPS", default=0)))
        response_time_values.append(_to_float(_pick(row, "Average Response Time", "Average (ms)", default=0)))
        failure_values.append(_to_float(_pick(row, "Failures/s", "Current Failures/s", default=0)))

    history_note = ""
    if not history_rows:
        history_note = "Trend charts are limited because no *_stats_history.csv file was found. Run Locust with --csv-full-history."

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Performance Report - {html_lib.escape(str(scenario))}</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            * {{
                box-sizing: border-box;
            }}
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                background-color: #f5f7fb;
                color: #222;
            }}
            .container {{
                max-width: 1400px;
                margin: 0 auto;
                padding: 24px;
            }}
            .header {{
                background: linear-gradient(135deg, #1f3c88, #2563eb);
                color: #fff;
                padding: 24px;
                border-radius: 16px;
                margin-bottom: 24px;
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
            }}
            .header h1 {{
                margin: 0 0 12px 0;
                font-size: 28px;
            }}
            .meta {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 10px;
                font-size: 14px;
            }}
            .cards {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 16px;
                margin-bottom: 24px;
            }}
            .card {{
                background: #fff;
                border-radius: 16px;
                padding: 18px;
                box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
            }}
            .card-title {{
                font-size: 13px;
                color: #666;
                margin-bottom: 8px;
                text-transform: uppercase;
            }}
            .card-value {{
                font-size: 28px;
                font-weight: bold;
            }}
            .blue {{
                color: #2563eb;
            }}
            .green {{
                color: #15803d;
            }}
            .orange {{
                color: #d97706;
            }}
            .red {{
                color: #dc2626;
            }}
            .grid-2 {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-bottom: 24px;
            }}
            .grid-1 {{
                display: grid;
                grid-template-columns: 1fr;
                gap: 20px;
                margin-bottom: 24px;
            }}
            .panel {{
                background: #fff;
                border-radius: 16px;
                padding: 20px;
                box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
            }}
            .panel h2 {{
                margin-top: 0;
                font-size: 20px;
            }}
            .note {{
                margin-top: 8px;
                color: #b45309;
                font-size: 13px;
                background: #fff7ed;
                padding: 10px;
                border-radius: 10px;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin-bottom: 24px;
            }}
            th, td {{
                border-bottom: 1px solid #e5e7eb;
                padding: 10px 12px;
                text-align: left;
                font-size: 13px;
                vertical-align: top;
            }}
            th {{
                background-color: #f3f6fb;
                font-weight: 600;
            }}
            tr:hover {{
                background-color: #f9fbff;
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
            canvas {{
                width: 100% !important;
                max-height: 360px;
            }}
            .footer {{
                text-align: center;
                color: #6b7280;
                font-size: 12px;
                margin-top: 8px;
            }}
            @media (max-width: 1000px) {{
                .grid-2 {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Performance Test Dashboard</h1>
                <div class="meta">
                    <div><strong>Scenario:</strong> {html_lib.escape(str(scenario))}</div>
                    <div><strong>Environment:</strong> {html_lib.escape(str(environment))}</div>
                    <div><strong>Generated On:</strong> {generated_on}</div>
                    <div><strong>Results Folder:</strong> {html_lib.escape(str(results_folder))}</div>
                </div>
            </div>

            <div class="cards">
                <div class="card">
                    <div class="card-title">Total Requests</div>
                    <div class="card-value blue">{total_requests}</div>
                </div>
                <div class="card">
                    <div class="card-title">Total Failures</div>
                    <div class="card-value {'red' if total_failures > 0 else 'green'}">{total_failures}</div>
                </div>
                <div class="card">
                    <div class="card-title">Success Rate</div>
                    <div class="card-value {'green' if success_rate >= 99 else 'orange' if success_rate >= 95 else 'red'}">{success_rate}%</div>
                </div>
                <div class="card">
                    <div class="card-title">Average Response Time</div>
                    <div class="card-value blue">{avg_response:.2f} ms</div>
                </div>
                <div class="card">
                    <div class="card-title">P95 Response Time</div>
                    <div class="card-value orange">{p95_response:.2f} ms</div>
                </div>
                <div class="card">
                    <div class="card-title">Current RPS</div>
                    <div class="card-value blue">{current_rps:.2f}</div>
                </div>
            </div>

            <div class="grid-2">
                <div class="panel">
                    <h2>Response Time Trend</h2>
                    {"<div class='note'>" + html_lib.escape(history_note) + "</div>" if history_note else ""}
                    <canvas id="responseTimeChart"></canvas>
                </div>
                <div class="panel">
                    <h2>RPS Trend</h2>
                    {"<div class='note'>" + html_lib.escape(history_note) + "</div>" if history_note else ""}
                    <canvas id="rpsChart"></canvas>
                </div>
            </div>

            <div class="grid-2">
                <div class="panel">
                    <h2>Failures Trend</h2>
                    {"<div class='note'>" + html_lib.escape(history_note) + "</div>" if history_note else ""}
                    <canvas id="failuresChart"></canvas>
                </div>
                <div class="panel">
                    <h2>Percentile Visualization</h2>
                    <canvas id="percentileChart"></canvas>
                </div>
            </div>

            <div class="grid-1">
                <div class="panel">
                    <h2>Top Request Performance (Avg vs P95)</h2>
                    <canvas id="requestComparisonChart"></canvas>
                </div>
            </div>

            <div class="grid-1">
                <div class="panel">
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

    if summary_rows:
        for row in summary_rows:
            html += f"""
                        <tr>
                            <td>{html_lib.escape(str(row.get("Type", "")))}</td>
                            <td>{html_lib.escape(str(row.get("Name", "")))}</td>
                            <td>{html_lib.escape(str(row.get("# Requests", "")))}</td>
                            <td>{html_lib.escape(str(row.get("# Fails", "")))}</td>
                            <td>{html_lib.escape(str(row.get("Median Response Time", row.get("Median (ms)", ""))))}</td>
                            <td>{html_lib.escape(str(row.get("95%", row.get("95%ile (ms)", ""))))}</td>
                            <td>{html_lib.escape(str(row.get("Average Response Time", row.get("Average (ms)", ""))))}</td>
                            <td>{html_lib.escape(str(row.get("Requests/s", row.get("Current RPS", ""))))}</td>
                        </tr>
            """
    else:
        html += """
                        <tr>
                            <td colspan="8">No summary data found</td>
                        </tr>
        """

    html += """
                    </table>
                </div>
            </div>

            <div class="grid-1">
                <div class="panel">
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
                            <th>Status</th>
                        </tr>
    """

    if request_rows:
        for row in request_rows:
            req_fails = _to_int(row.get("# Fails", 0))
            req_p95 = _to_float(row.get("95%", row.get("95%ile (ms)", 0)))

            if req_fails == 0 and req_p95 < 2000:
                status = '<span class="ok">Healthy</span>'
            elif req_fails < 5 and req_p95 < 5000:
                status = '<span class="warn">Needs Review</span>'
            else:
                status = '<span class="bad">Critical</span>'

            html += f"""
                        <tr>
                            <td>{html_lib.escape(str(row.get("Type", "")))}</td>
                            <td>{html_lib.escape(str(row.get("Name", "")))}</td>
                            <td>{html_lib.escape(str(row.get("# Requests", "")))}</td>
                            <td>{html_lib.escape(str(row.get("# Fails", "")))}</td>
                            <td>{html_lib.escape(str(row.get("Median Response Time", row.get("Median (ms)", ""))))}</td>
                            <td>{html_lib.escape(str(row.get("95%", row.get("95%ile (ms)", ""))))}</td>
                            <td>{html_lib.escape(str(row.get("Average Response Time", row.get("Average (ms)", ""))))}</td>
                            <td>{status}</td>
                        </tr>
            """
    else:
        html += """
                        <tr>
                            <td colspan="8">No request-level data found</td>
                        </tr>
        """

    html += """
                    </table>
                </div>
            </div>

            <div class="grid-1">
                <div class="panel">
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
                            <td>{html_lib.escape(str(row.get("Method", "")))}</td>
                            <td>{html_lib.escape(str(row.get("Name", "")))}</td>
                            <td>{html_lib.escape(str(row.get("Error", "")))}</td>
                            <td>{html_lib.escape(str(row.get("Occurrences", "")))}</td>
                        </tr>
            """
    else:
        html += """
                        <tr>
                            <td colspan="4">No failures recorded</td>
                        </tr>
        """

    html += f"""
                    </table>
                </div>
            </div>

            <div class="footer">
                Generated by Locust Custom HTML Reporter
            </div>
        </div>

        <script>
            const timeLabels = {json.dumps(time_labels)};
            const rpsValues = {json.dumps(rps_values)};
            const responseTimeValues = {json.dumps(response_time_values)};
            const failureValues = {json.dumps(failure_values)};

            const percentileLabels = {json.dumps(percentile_labels)};
            const percentileValues = {json.dumps(percentile_values)};

            const requestChartNames = {json.dumps(request_chart_names)};
            const requestChartAvg = {json.dumps(request_chart_avg)};
            const requestChartP95 = {json.dumps(request_chart_p95)};

            function createLineChart(chartId, labels, data, label) {{
                new Chart(document.getElementById(chartId), {{
                    type: 'line',
                    data: {{
                        labels: labels,
                        datasets: [{{
                            label: label,
                            data: data,
                            tension: 0.3,
                            fill: false
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            y: {{
                                beginAtZero: true
                            }}
                        }}
                    }}
                }});
            }}

            function createBarChart(chartId, labels, data, label) {{
                new Chart(document.getElementById(chartId), {{
                    type: 'bar',
                    data: {{
                        labels: labels,
                        datasets: [{{
                            label: label,
                            data: data
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            y: {{
                                beginAtZero: true
                            }}
                        }}
                    }}
                }});
            }}

            createLineChart('responseTimeChart', timeLabels, responseTimeValues, 'Average Response Time (ms)');
            createLineChart('rpsChart', timeLabels, rpsValues, 'Requests Per Second');
            createLineChart('failuresChart', timeLabels, failureValues, 'Failures Per Second');
            createBarChart('percentileChart', percentileLabels, percentileValues, 'Response Time (ms)');

            new Chart(document.getElementById('requestComparisonChart'), {{
                type: 'bar',
                data: {{
                    labels: requestChartNames,
                    datasets: [
                        {{
                            label: 'Average (ms)',
                            data: requestChartAvg
                        }},
                        {{
                            label: 'P95 (ms)',
                            data: requestChartP95
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{
                            beginAtZero: true
                        }}
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    """

    with open(html_path, "w", encoding="utf-8") as file:
        file.write(html)

    if auto_open:
        webbrowser.open(f"file:///{html_path.replace(os.sep, '/')}")

    return html_path