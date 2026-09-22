from pathlib import Path
from datetime import date, timedelta
import csv
import random


# ============================================================
# Configuration
# ============================================================

random.seed(42)

PROJECT_FOLDER = Path(__file__).resolve().parent
DATA_FOLDER = PROJECT_FOLDER / "data"
DATA_FOLDER.mkdir(exist_ok=True)

START_DATE = date(2025, 4, 1)
END_DATE = date(2026, 9, 30)


# ============================================================
# Utility functions
# ============================================================

def write_csv(filename, rows, columns):
    """
    Write a list of dictionaries to a CSV file.
    """

    path = DATA_FOLDER / filename

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    print(f"{filename:<40} {len(rows):>10,} rows")


def date_range(start_date, end_date):
    current_date = start_date

    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days=1)


def date_key(current_date):
    return int(current_date.strftime("%Y%m%d"))


def is_hidden_decline(current_date, region_name, department_name):
    """
    Deliberate business trend for later dashboard analysis.
    """

    return (
        region_name == "Atlantic"
        and department_name == "Womens Apparel"
        and date(2026, 1, 1) <= current_date <= date(2026, 6, 30)
    )


# ============================================================
# Dimension tables
# ============================================================

def create_dim_date():
    rows = []

    for current_date in date_range(START_DATE, END_DATE):
        rows.append({
            "DateKey": date_key(current_date),
            "FullDate": current_date.isoformat(),
            "Year": current_date.year,
            "Quarter": f"Q{((current_date.month - 1) // 3) + 1}",
            "MonthNumber": current_date.month,
            "MonthName": current_date.strftime("%B"),
            "YearMonth": current_date.strftime("%Y-%m"),
            "WeekNumber": current_date.isocalendar().week,
            "DayOfMonth": current_date.day,
            "DayName": current_date.strftime("%A"),
            "IsWeekend": int(current_date.weekday() >= 5),
        })

    columns = [
        "DateKey",
        "FullDate",
        "Year",
        "Quarter",
        "MonthNumber",
        "MonthName",
        "YearMonth",
        "WeekNumber",
        "DayOfMonth",
        "DayName",
        "IsWeekend",
    ]

    write_csv("dim_date.csv", rows, columns)


def create_dim_region():
    region_names = [
        "Ontario",
        "Quebec",
        "Western Canada",
        "Atlantic",
        "British Columbia",
        "Prairies",
        "Northern Canada",
    ]

    rows = []

    for number, region_name in enumerate(region_names, start=1):
        rows.append({
            "RegionKey": f"REG{number:02d}",
            "RegionName": region_name,
            "RegionManager": f"Regional Manager {number}",
        })

    write_csv(
        "dim_region.csv",
        rows,
        [
            "RegionKey",
            "RegionName",
            "RegionManager",
        ],
    )

    return rows


def create_dim_store(regions):
    """
    Creates exactly 56 stores:
    8 stores for each of 7 regions.
    """

    rows = []
    store_number = 1

    for region in regions:
        for store_in_region in range(1, 9):
            store_key = f"STR{store_number:03d}"

            rows.append({
                "StoreKey": store_key,
                "StoreNumber": store_number,
                "StoreName": (
                    f"{region['RegionName']} Store "
                    f"{store_in_region}"
                ),
                "RegionKey": region["RegionKey"],
                "StoreFormat": random.choice([
                    "Standard",
                    "Large Format",
                    "Urban",
                ]),
                "StoreStatus": "Open",
                "OpeningDate": (
                    date(2017, 1, 1)
                    + timedelta(days=random.randint(0, 3000))
                ).isoformat(),
            })

            store_number += 1

    write_csv(
        "dim_store.csv",
        rows,
        [
            "StoreKey",
            "StoreNumber",
            "StoreName",
            "RegionKey",
            "StoreFormat",
            "StoreStatus",
            "OpeningDate",
        ],
    )

    return rows


def create_dim_department():
    departments = [
        ("DEP01", "Womens Apparel"),
        ("DEP02", "Mens Apparel"),
        ("DEP03", "Kids"),
        ("DEP04", "Home"),
        ("DEP05", "Footwear"),
        ("DEP06", "Accessories"),
    ]

    rows = [
        {
            "DepartmentKey": key,
            "DepartmentName": name,
        }
        for key, name in departments
    ]

    write_csv(
        "dim_department.csv",
        rows,
        [
            "DepartmentKey",
            "DepartmentName",
        ],
    )

    return rows


def create_dim_kpi():
    kpis = [
        ("KPI01", "Sales"),
        ("KPI02", "Units Sold"),
        ("KPI03", "Inventory"),
        ("KPI04", "Productivity"),
        ("KPI05", "Report Timeliness"),
        ("KPI06", "Data Quality"),
        ("KPI07", "Automation Success"),
    ]

    units = {
        "Sales": "CAD",
        "Units Sold": "Units",
        "Inventory": "Units",
        "Productivity": "CAD per Labour Hour",
        "Report Timeliness": "Percentage",
        "Data Quality": "Issue Count",
        "Automation Success": "Percentage",
    }

    rows = [
        {
            "KPIKey": key,
            "KPIName": name,
            "UnitOfMeasure": units[name],
        }
        for key, name in kpis
    ]

    write_csv(
        "dim_kpi.csv",
        rows,
        [
            "KPIKey",
            "KPIName",
            "UnitOfMeasure",
        ],
    )

    return rows


def create_dim_report():
    reports = [
        ("RPT01", "Daily Store Sales Report", "Daily"),
        ("RPT02", "Weekly Inventory Report", "Weekly"),
        ("RPT03", "Monthly Productivity Report", "Monthly"),
        ("RPT04", "Data Quality Exception Report", "Daily"),
        ("RPT05", "Automation Monitoring Report", "Daily"),
    ]

    rows = [
        {
            "ReportKey": key,
            "ReportName": name,
            "ReportFrequency": frequency,
            "BusinessOwner": owner,
        }
        for (key, name, frequency), owner in zip(
            reports,
            [
                "Retail Operations",
                "Merchandising",
                "Finance",
                "Data Governance",
                "Analytics",
            ],
        )
    ]

    write_csv(
        "dim_report.csv",
        rows,
        [
            "ReportKey",
            "ReportName",
            "ReportFrequency",
            "BusinessOwner",
        ],
    )

    return rows


def create_dim_role():
    roles = [
        ("ROL01", "Reporting Analyst"),
        ("ROL02", "Store Manager"),
        ("ROL03", "Regional Manager"),
        ("ROL04", "Merchandising Analyst"),
        ("ROL05", "Data Quality Analyst"),
        ("ROL06", "Automation Developer"),
    ]

    rows = [
        {
            "RoleKey": key,
            "RoleName": name,
        }
        for key, name in roles
    ]

    write_csv(
        "dim_role.csv",
        rows,
        [
            "RoleKey",
            "RoleName",
        ],
    )

    return rows


def create_dim_source_system():
    systems = [
        ("SYS01", "Point of Sale"),
        ("SYS02", "Inventory Management"),
        ("SYS03", "Workforce Management"),
        ("SYS04", "Enterprise Data Warehouse"),
        ("SYS05", "Power BI"),
        ("SYS06", "Vendor Portal"),
        ("SYS07", "Automation Platform"),
    ]

    rows = [
        {
            "SourceSystemKey": key,
            "SourceSystemName": name,
            "SystemOwner": owner,
        }
        for (key, name), owner in zip(
            systems,
            [
                "Store Operations",
                "Merchandising",
                "Human Resources",
                "Technology",
                "Analytics",
                "External Vendors",
                "Automation Centre",
            ],
        )
    ]

    write_csv(
        "dim_source_system.csv",
        rows,
        [
            "SourceSystemKey",
            "SourceSystemName",
            "SystemOwner",
        ],
    )

    return rows


def create_dim_activity_type():
    activities = [
        ("ACT01", "KPI Performance"),
        ("ACT02", "Productivity"),
        ("ACT03", "Reporting Activity"),
        ("ACT04", "Data Quality"),
        ("ACT05", "Automation"),
    ]

    rows = [
        {
            "ActivityTypeKey": key,
            "ActivityType": name,
        }
        for key, name in activities
    ]

    write_csv(
        "dim_activity_type.csv",
        rows,
        [
            "ActivityTypeKey",
            "ActivityType",
        ],
    )

    return rows


def create_dim_scenario():
    scenarios = [
        ("SCN01", "Actual"),
        ("SCN02", "Target"),
        ("SCN03", "Prior Year"),
        ("SCN04", "Forecast"),
    ]

    rows = [
        {
            "ScenarioKey": key,
            "ScenarioName": name,
        }
        for key, name in scenarios
    ]

    write_csv(
        "dim_scenario.csv",
        rows,
        [
            "ScenarioKey",
            "ScenarioName",
        ],
    )

    return rows


# ============================================================
# Central fact table
# ============================================================

def create_fact_retail_reporting(
    stores,
    regions,
    departments,
):
    """
    Creates the only fact table in the model.

    The fact table contains rows for:
    - KPI performance
    - Productivity
    - Reporting activity
    - Data quality
    - Automation

    All quantitative measures are stored in this table.
    """

    rows = []
    fact_key = 1

    region_lookup = {
        region["RegionKey"]: region["RegionName"]
        for region in regions
    }

    department_lookup = {
        department["DepartmentKey"]: department["DepartmentName"]
        for department in departments
    }

    # --------------------------------------------------------
    # 1. Daily store-department KPI performance
    # --------------------------------------------------------

    for current_date in date_range(START_DATE, END_DATE):
        for store in stores:
            region_name = region_lookup[store["RegionKey"]]

            for department in departments:
                department_key = department["DepartmentKey"]
                department_name = department_lookup[department_key]

                sales_amount = random.uniform(3000, 9500)

                # Seasonal pattern
                if current_date.month in (11, 12):
                    sales_amount *= 1.20
                elif current_date.month in (1, 2):
                    sales_amount *= 0.88

                # Store-format pattern
                if store["StoreFormat"] == "Large Format":
                    sales_amount *= 1.25
                elif store["StoreFormat"] == "Urban":
                    sales_amount *= 1.10

                # Deliberate hidden decline
                decline = is_hidden_decline(
                    current_date,
                    region_name,
                    department_name,
                )

                if decline:
                    sales_amount *= 0.68

                sales_amount *= random.uniform(0.92, 1.08)

                sales_target = sales_amount * random.uniform(
                    1.02,
                    1.15,
                )

                units_sold = max(
                    1,
                    int(sales_amount / random.uniform(35, 85)),
                )

                if decline:
                    inventory_units = random.randint(850, 1350)
                else:
                    inventory_units = random.randint(450, 1050)

                labour_hours = random.uniform(50, 145)
                productivity = sales_amount / labour_hours

                rows.append({
                    "FactRetailReportingKey": fact_key,
                    "DateKey": date_key(current_date),
                    "StoreKey": store["StoreKey"],
                    "RegionKey": store["RegionKey"],
                    "DepartmentKey": department_key,
                    "KPIKey": "KPI01",
                    "ReportKey": "RPT01",
                    "RoleKey": "ROL01",
                    "SourceSystemKey": "SYS01",
                    "ActivityTypeKey": "ACT01",
                    "ScenarioKey": "SCN01",

                    "ActualValue": round(sales_amount, 2),
                    "TargetValue": round(sales_target, 2),
                    "VarianceValue": round(
                        sales_amount - sales_target,
                        2,
                    ),

                    "SalesAmount": round(sales_amount, 2),
                    "SalesTarget": round(sales_target, 2),
                    "UnitsSold": units_sold,
                    "InventoryUnits": inventory_units,
                    "LabourHours": round(labour_hours, 2),
                    "ProductivityValue": round(productivity, 2),

                    "ReportCount": 0,
                    "ReportDeliveryMinutes": 0,

                    "IssueCount": 0,
                    "IssueResolvedCount": 0,

                    "AutomationRunCount": 0,
                    "AutomationSuccessCount": 0,
                    "AutomationFailureCount": 0,

                    "ProcessingMinutes": 0,
                })

                fact_key += 1

    # --------------------------------------------------------
    # 2. Reporting activity
    # --------------------------------------------------------

    for current_date in date_range(START_DATE, END_DATE):
        for report in [
            ("RPT01", "SYS05"),
            ("RPT02", "SYS02"),
            ("RPT03", "SYS04"),
            ("RPT04", "SYS05"),
            ("RPT05", "SYS07"),
        ]:
            report_key, system_key = report

            report_count = random.randint(1, 8)
            delivery_minutes = random.randint(5, 45)

            store = random.choice(stores)
            region_key = store["RegionKey"]

            rows.append({
                "FactRetailReportingKey": fact_key,
                "DateKey": date_key(current_date),
                "StoreKey": store["StoreKey"],
                "RegionKey": region_key,
                "DepartmentKey": "DEP01",
                "KPIKey": "KPI05",
                "ReportKey": report_key,
                "RoleKey": "ROL01",
                "SourceSystemKey": system_key,
                "ActivityTypeKey": "ACT03",
                "ScenarioKey": "SCN01",

                "ActualValue": report_count,
                "TargetValue": 5,
                "VarianceValue": report_count - 5,

                "SalesAmount": 0,
                "SalesTarget": 0,
                "UnitsSold": 0,
                "InventoryUnits": 0,
                "LabourHours": 0,
                "ProductivityValue": 0,

                "ReportCount": report_count,
                "ReportDeliveryMinutes": delivery_minutes,

                "IssueCount": 0,
                "IssueResolvedCount": 0,

                "AutomationRunCount": 0,
                "AutomationSuccessCount": 0,
                "AutomationFailureCount": 0,

                "ProcessingMinutes": 0,
            })

            fact_key += 1

    # --------------------------------------------------------
    # 3. Data-quality activity
    # --------------------------------------------------------

    for _ in range(2500):
        current_date = START_DATE + timedelta(
            days=random.randint(
                0,
                (END_DATE - START_DATE).days,
            )
        )

        store = random.choice(stores)
        issue_count = random.randint(1, 5)
        resolved_count = random.randint(0, issue_count)

        rows.append({
            "FactRetailReportingKey": fact_key,
            "DateKey": date_key(current_date),
            "StoreKey": store["StoreKey"],
            "RegionKey": store["RegionKey"],
            "DepartmentKey": random.choice(departments)["DepartmentKey"],
            "KPIKey": "KPI06",
            "ReportKey": "RPT04",
            "RoleKey": "ROL05",
            "SourceSystemKey": random.choice([
                "SYS01",
                "SYS02",
                "SYS03",
                "SYS04",
                "SYS06",
            ]),
            "ActivityTypeKey": "ACT04",
            "ScenarioKey": "SCN01",

            "ActualValue": issue_count,
            "TargetValue": 0,
            "VarianceValue": issue_count,

            "SalesAmount": 0,
            "SalesTarget": 0,
            "UnitsSold": 0,
            "InventoryUnits": 0,
            "LabourHours": 0,
            "ProductivityValue": 0,

            "ReportCount": 0,
            "ReportDeliveryMinutes": 0,

            "IssueCount": issue_count,
            "IssueResolvedCount": resolved_count,

            "AutomationRunCount": 0,
            "AutomationSuccessCount": 0,
            "AutomationFailureCount": 0,

            "ProcessingMinutes": 0,
        })

        fact_key += 1

    # --------------------------------------------------------
    # 4. Automation activity
    # --------------------------------------------------------

    for _ in range(3000):
        current_date = START_DATE + timedelta(
            days=random.randint(
                0,
                (END_DATE - START_DATE).days,
            )
        )

        store = random.choice(stores)

        automation_runs = random.randint(1, 5)
        failures = random.choices(
            [0, 1, 2],
            weights=[85, 12, 3],
            k=1,
        )[0]

        failures = min(failures, automation_runs)
        successes = automation_runs - failures
        processing_minutes = random.randint(2, 25)

        rows.append({
            "FactRetailReportingKey": fact_key,
            "DateKey": date_key(current_date),
            "StoreKey": store["StoreKey"],
            "RegionKey": store["RegionKey"],
            "DepartmentKey": random.choice(departments)["DepartmentKey"],
            "KPIKey": "KPI07",
            "ReportKey": "RPT05",
            "RoleKey": "ROL06",
            "SourceSystemKey": "SYS07",
            "ActivityTypeKey": "ACT05",
            "ScenarioKey": "SCN01",

            "ActualValue": successes,
            "TargetValue": automation_runs,
            "VarianceValue": successes - automation_runs,

            "SalesAmount": 0,
            "SalesTarget": 0,
            "UnitsSold": 0,
            "InventoryUnits": 0,
            "LabourHours": 0,
            "ProductivityValue": 0,

            "ReportCount": 0,
            "ReportDeliveryMinutes": 0,

            "IssueCount": 0,
            "IssueResolvedCount": 0,

            "AutomationRunCount": automation_runs,
            "AutomationSuccessCount": successes,
            "AutomationFailureCount": failures,

            "ProcessingMinutes": processing_minutes,
        })

        fact_key += 1

    columns = [
        "FactRetailReportingKey",
        "DateKey",
        "StoreKey",
        "RegionKey",
        "DepartmentKey",
        "KPIKey",
        "ReportKey",
        "RoleKey",
        "SourceSystemKey",
        "ActivityTypeKey",
        "ScenarioKey",
        "ActualValue",
        "TargetValue",
        "VarianceValue",
        "SalesAmount",
        "SalesTarget",
        "UnitsSold",
        "InventoryUnits",
        "LabourHours",
        "ProductivityValue",
        "ReportCount",
        "ReportDeliveryMinutes",
        "IssueCount",
        "IssueResolvedCount",
        "AutomationRunCount",
        "AutomationSuccessCount",
        "AutomationFailureCount",
        "ProcessingMinutes",
    ]

    write_csv(
        "fact_retail_reporting.csv",
        rows,
        columns,
    )


# ============================================================
# Main execution
# ============================================================

def main():
    print("Generating strict star-schema retail data...\n")

    regions = create_dim_region()
    stores = create_dim_store(regions)
    departments = create_dim_department()

    create_dim_date()
    create_dim_kpi()
    create_dim_report()
    create_dim_role()
    create_dim_source_system()
    create_dim_activity_type()
    create_dim_scenario()

    create_fact_retail_reporting(
        stores=stores,
        regions=regions,
        departments=departments,
    )

    print("\nGeneration complete.")
    print(f"Output folder: {DATA_FOLDER.resolve()}")


if __name__ == "__main__":
    main()
