# TJX Canada Store Performance and Operations Reporting

## What each view shows

**View 1, Header KPI Row:** The executive view shows a 96.4% overall store productivity rate against a 95.0% target, 412 active stores out of 415 mapped, 1,284 KPI reconciliations or exceptions, 97.1% automation success against a 98.0% benchmark, 8,940 report opens, and a -1.2% variance against target.

**View 2, Store and Regional Operations Funnel:** The operations funnel follows completion from Data Ingestion through KPI Calculation, Process Audit, and Report Publishing, with filters for region, department, banner, and Actual or Target scenario.

**View 3, Productivity and Process Efficiency:** The productivity view compares the prior two quarters with the last two quarters by region and places those results beside six months of median exception-resolution time.

**View 4, Reporting and Source System Integration:** The source-system view compares pipeline accuracy with record volume and shows report opens by report type.

**View 5, Automation and Audit Readiness:** The automation view compares the share of RPA and Power Automate jobs completed before store opening with the 98.0% readiness benchmark by department.

## Three things the data is saying

### 1. The largest operational weakness is concentrated in Quebec and the Prairies

Quebec productivity declined from 93.0% to 92.4% between the prior two quarters and the last two quarters, a decrease of 0.6 percentage points. Prairies productivity declined from 92.8% to 92.1%, a decrease of 0.7 percentage points.

Both regions are below the 95.0% productivity target. Quebec is 2.6 percentage points below target, and Prairies is 2.9 percentage points below target.

The six-month resolution-time slice shows the same two regions deteriorating. Quebec increased from 11.5 hours in April to 14.6 hours in September, an increase of 3.1 hours. Prairies increased from 10.2 hours to 13.5 hours, an increase of 3.3 hours.

The regional productivity and resolution-time views reveal a linked operating problem. The two regions with falling productivity are also the two regions with rising exception-resolution time.

### 2. The reporting funnel loses the most coverage before audit completion

Across all regions, the funnel begins with Data Ingestion, moves through KPI Calculation and Process Audit, and ends with Report Publishing. The regional slices show that the largest practical gap is between the calculation and audit stages rather than between audit and final publishing.

Quebec moves from 98.7% at Data Ingestion to 97.9% at KPI Calculation, 93.4% at Process Audit, and 91.2% at Report Publishing. The total fall from ingestion to publishing is 7.5 percentage points.

Prairies moves from 98.9% at Data Ingestion to 98.1% at KPI Calculation, 94.7% at Process Audit, and 92.6% at Report Publishing. The total fall from ingestion to publishing is 6.3 percentage points.

British Columbia publishes at 96.0%, while Quebec publishes at 91.2%. The 4.8-point difference makes Quebec the first regional process slice to investigate.

The dashboard therefore points to KPI Calculation and Process Audit as the first control points for investigation, with Report Publishing as the visible downstream result.

### 3. The weakest data sources are also the lowest-volume sources

Legacy Store Ops DB has 91.0% pipeline accuracy while processing 54 thousand records. RPA Bot Farm has 94.2% accuracy while processing 128 thousand records.

Power Automate has 96.5% accuracy and processes 340 thousand records. Oracle Retail DW has 97.8% accuracy and processes 615 thousand records. SAP BW has the highest accuracy at 99.1% and processes the largest volume at 842 thousand records.

The source-system slice shows that the two lowest-accuracy systems are Legacy Store Ops DB and RPA Bot Farm. The finding is not that low volume causes low accuracy. The dashboard shows that these systems deserve the first data-quality review because they combine the lowest accuracy with 54 thousand and 128 thousand records.

The automation view identifies a separate readiness gap. Beauty is at 95.4%, which is 2.6 percentage points below the 98.0% benchmark. Footwear is at 96.2%, which is 1.8 percentage points below the benchmark. Apparel is at 98.6%, Home & Gifts is at 98.3%, and Accessories is at 98.9%.

## What I would do next with real data

### 1. Query the regional exception funnel by store, department, source system, and activity stage

The first query should return each store in Quebec and Prairies with its region, banner, department, source system, KPI, activity type, exception status, opened timestamp, resolved timestamp, and audit status.

The query should calculate the number of exceptions, the median hours to resolution, and the completion rate at Data Ingestion, KPI Calculation, Process Audit, and Report Publishing.

The action is to identify the stores and departments creating the 14.6-hour Quebec median and the 13.5-hour Prairies median. The output should assign an owner to each unresolved exception and show whether the issue begins in KPI Calculation, Process Audit, or an upstream source system.

### 2. Audit Legacy Store Ops DB and RPA Bot Farm before changing the workflow

The second query should compare record status by source system and return total records, error records, error rate, KPI, report, region, department, and activity type.

The priority is Legacy Store Ops DB at 91.0% accuracy across 54 thousand records and RPA Bot Farm at 94.2% accuracy across 128 thousand records.

The question for the data and technology teams is whether the errors are caused by missing records, duplicate records, late records, failed transformations, or incorrect status mapping.

The action is to correct the dominant error category and then compare the source accuracy with the 91.2% Quebec publishing result, the 92.6% Prairies publishing result, and the 94.2% or lower audit outcomes shown in the funnel.

### 3. Investigate the 2.6-point Beauty automation gap and the 1.8-point Footwear gap

The third query should return every automated job by department, source system, report, store, scheduled time, completion time, store opening time, job status, and failure reason.

The query should separate jobs completed before opening from jobs completed after opening. It should calculate the result against the 98.0% benchmark.

The starting points are Beauty at 95.4% and Footwear at 96.2%. The question for operations and IT is whether late completion is concentrated in a particular report, source system, banner, region, or job type.

The action is to correct the highest-volume or highest-impact failure path and monitor whether Beauty reaches 98.0% and Footwear reaches 98.0% without increasing the 1,284 open exceptions.

## What I could not do with generated data

I could not determine the sales impact of the 96.4% productivity rate because the model contains no sales-dollar field and no sales fact table.

I could not determine the customer impact of the 1,284 exceptions because the model contains no customer-footfall field, customer-transaction field, or customer-outcome field.

I could not determine whether the 0.6-point Quebec decline or the 0.7-point Prairies decline was caused by source-system errors, staffing, store conditions, process design, department mix, or reporting delays.

I could not prove that the increase from 11.5 to 14.6 hours in Quebec or from 10.2 to 13.5 hours in Prairies caused the productivity declines. The dashboard shows that the trends occur together. It does not establish causation.

I could not validate the quality of the 8,940 report opens because the model does not show whether a report open led to an operational action, an exception resolution, a productivity improvement, or a business result.

I could not identify the exact stores responsible for the regional patterns from the dashboard summary alone. The model supports store-level analysis through `dim_store`, but that requires the company’s real rows in `fact_retail_reporting`.

I could not use the Target scenario as evidence of actual company performance. The dashboard displays Target or Budget values as a comparison scenario, not as observed operational results.

## Caveat

Every number on this page is synthetic and modelled on the TJX Reporting and Analytics Specialist job description. The data is shaped to the provided star schema, with `fact_retail_reporting` joined to the listed date, store, region, department, KPI, report, role, source-system, activity-type, and scenario dimensions. It is not TJX data, it is not validated against TJX systems, and it says nothing about the company’s real performance.

## Next steps

### 1. Confirm the regional problem in the real data

Run a store-level query for Quebec and Prairies covering the last six months. Return store, region, banner, department, KPI, source system, exception status, exception-open date, exception-resolution date, and report-publishing status.

Calculate productivity, exception count, median resolution time, and publishing completion for each store.

Start with the stores contributing to the Quebec result of 92.4% productivity and 14.6 hours median resolution time, and the Prairies result of 92.1% productivity and 13.5 hours median resolution time.

The decision is whether the problem is concentrated in a small number of stores or spread across both regions. If a small number of stores explain most of the result, assign corrective owners to those stores. If the result is broad, review the regional process and staffing model.

### 2. Find the point where the reporting funnel breaks

Compare Data Ingestion, KPI Calculation, Process Audit, and Report Publishing for every store, department, KPI, and source system.

The query must return the first failed activity, the failure reason, the responsible system or role, the time of failure, and the time of resolution.

Use Quebec’s 91.2% publishing result and Prairies’ 92.6% publishing result as the starting slices. Compare both with British Columbia’s 96.0% publishing result.

The decision is whether the largest loss occurs during KPI Calculation, Process Audit, or Report Publishing. Correct the first failed activity rather than treating the final publishing result as the root cause.

### 3. Test source-system accuracy against operational impact

Reconcile the source systems record by record. Return source system, store, department, KPI, report, record count, rejected count, duplicate count, missing-field count, late-record count, and transformation error count.

Prioritise Legacy Store Ops DB at 91.0% accuracy across 54 thousand records and RPA Bot Farm at 94.2% accuracy across 128 thousand records.

Compare each error category with the regional funnel. Check whether source errors appear more frequently in Quebec and Prairies or in departments below the automation benchmark.

The decision is whether to repair the source feed, change the transformation rule, or change the validation control.

### 4. Recover the automation gap before store opening

Pull every RPA and Power Automate job for Beauty and Footwear. Return department, store, report, source system, job type, scheduled time, completion time, store-opening time, completion status, and failure reason.

Measure the percentage completed before store opening against the 98.0% benchmark. Beauty is currently at 95.4%, leaving a 2.6-point gap. Footwear is at 96.2%, leaving a 1.8-point gap.

The decision is whether late completion is caused by failed jobs, slow source systems, scheduling conflicts, or data that arrives after the job starts. Fix the highest-volume failure category first.

### 5. Validate whether report usage leads to action

Join report opens to the store, user role, report, KPI, exception, and subsequent activity where the real system permits it.

Measure how many of the 8,940 report opens are followed by an exception review, a correction, a manager sign-off, or a completed operational action.

The decision is whether report usage is producing measurable action. If report opens are not followed by action, simplify the report, remove low-value views, or change the escalation process.

### 6. Establish a controlled weekly review

Create a weekly operating review using the same definitions for productivity, automation success, exception count, source accuracy, and report completion.

Track the 96.4% overall productivity rate against the 95.0% target, the 97.1% automation rate against the 98.0% benchmark, and the 1,284 exceptions by age and owner.

Review Quebec’s 92.4% productivity, Prairies’ 92.1% productivity, Beauty’s 95.4% automation result, and Footwear’s 96.2% automation result every week until each measure is at or above target.

The review should record the metric, the owner, the root cause, the corrective action, the due date, and the next observed result.

## What success would look like

Success means the real data identifies the stores, departments, systems, and process stages behind the regional results.

The immediate targets are to bring Quebec and Prairies above the 95.0% productivity target, bring Beauty and Footwear to the 98.0% pre-open automation benchmark, reduce the 1,284 exceptions, improve the 91.0% Legacy Store Ops DB accuracy, and reduce the 14.6-hour Quebec and 13.5-hour Prairies median resolution times.

These targets must be tested against the company’s real data before they are treated as business commitments.
