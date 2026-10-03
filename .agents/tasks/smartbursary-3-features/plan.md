# Implementation Plan

## Feature 1: Application Deadline Enforcement

- [ ] 1. Verify backend deadline validation works correctly in POST /api/applications.
      Backend already has validation at line 328 of main.py: `if b.deadline < date.today(): raise HTTPException(400,"The deadline for this bursary has passed")`.
      Test via API docs at http://127.0.0.1:8000/docs by attempting to POST an application for a past-deadline bursary.
      Files: c:/dev/SmartBursary-Complete/SmartBursary-Complete/backend/app/main.py
      Verify: Test POST /api/applications with expired bursary_id via API docs; should return 400 error.

- [ ] 2. Add deadline display, countdown, and Open/Closed badge to frontend bursary cards.
      In BursariesPage component (frontend/src/App.jsx around line 600), calculate days remaining: `Math.ceil((new Date(b.deadline + 'T23:59:59') - new Date()) / (1000*60*60*24))`.
      Show countdown text like "5 days left" or "Expired".
      Add Badge showing "Open" (green tone) if active and deadline future, "Closed" (red tone) if past deadline or inactive.
      Pattern: `<Badge tone={b.active?(new Date(b.deadline+'T23:59:59')<new Date()?'danger':'success'):'danger'}>{b.active?(new Date(b.deadline+'T23:59:59')<new Date()?'Closed':'Open'):'Closed'}</Badge>`
      Files: c:/dev/SmartBursary-Complete/SmartBursary-Complete/frontend/src/App.jsx
      Verify: Browse bursaries as applicant; verify badges show correctly and countdown displays.

- [ ] 3. Disable Apply button for expired bursaries and show "Applications Closed" message.
      In BursariesPage program-card rendering, find Apply button.
      Replace with conditional: if deadline passed, show `<Button block disabled>Applications Closed</Button>`, else show normal Apply button.
      Preserve existing constituency eligibility check logic.
      Files: c:/dev/SmartBursary-Complete/SmartBursary-Complete/frontend/src/App.jsx
      Verify: Click on expired bursary card; Apply button should be disabled with "Applications Closed" text.

- [ ] 4. Update seed data with mix of active and expired deadlines.
      In seed_test_data.py (around line 29), modify bursary deadline creation to use `deadline=date.today() + timedelta(days=random.randint(5,60))` for half, `deadline=date.today() - timedelta(days=random.randint(1,30))` for other half.
      In main.py lifespan seed (around line 21), change STEM Merit Bursary to `deadline=date(2024,9,20)` (past).
      Files: c:/dev/SmartBursary-Complete/SmartBursary-Complete/backend/seed_test_data.py, c:/dev/SmartBursary-Complete/SmartBursary-Complete/backend/app/main.py
      Verify: Restart backend (delete smartbursary.db first or run seed_test_data.py); browse bursaries; verify mix of Open and Closed bursaries.

## Feature 2: Reports and Analytics Dashboard

- [ ] 5. Create backend endpoint /api/reports/overview returning aggregated stats.
      Add new GET endpoint in main.py after /api/reports/applications.csv (around line 599).
      Query: total applications count, approved/rejected/pending/disbursed counts.
      Group by constituency: SELECT Bursary.constituency, COUNT(Application.id), SUM(CASE WHEN status='Approved'), etc. Join Application.bursary.
      Group by status: SELECT status, COUNT(*).
      Group by bursary: SELECT Bursary.name, COUNT(Application.id), COUNT(CASE WHEN status='Approved'), AVG(amount).
      Return JSON: `{"total_applications": int, "approved": int, "rejected": int, "pending": int, "disbursed": int, "by_constituency": [...], "by_status": [...], "by_bursary": [...]}`
      Files: c:/dev/SmartBursary-Complete/SmartBursary-Complete/backend/app/main.py
      Verify: Test endpoint at http://127.0.0.1:8000/docs as admin; verify JSON structure and data correctness.

- [ ] 6. Create ReportsPage component displaying summary cards and three tables.
      In App.jsx, update existing ReportsPage (around line 1180).
      Add state for overview data, fetch from /api/reports/overview on mount.
      Display 4 summary cards: Total Applications (green), Approval Rate % (blue), Total Disbursed Amount (purple), Pending Review (amber).
      Use existing Stat component pattern from Dashboard.
      Files: c:/dev/SmartBursary-Complete/SmartBursary-Complete/frontend/src/App.jsx
      Verify: Navigate to Reports page as admin; verify 4 cards display with real numbers.

- [ ] 7. Add "Applications by Constituency" table with progress bars.
      In ReportsPage, add table using existing .panel.table-panel and <table> markup from ApplicationsPage.
      Columns: Constituency, Total Applications, Approved, Pending, Approval Rate %.
      Map over overview.by_constituency array.
      Show CSS progress bar using .bar-track pattern: `<div className="bar-track"><i style={{width: approvalRate+'%'}}/></div>`
      Files: c:/dev/SmartBursary-Complete/SmartBursary-Complete/frontend/src/App.jsx
      Verify: Verify table renders with constituency rows and progress bars show approval rates visually.

- [ ] 8. Add "Applications by Status" and "Applications by Bursary" tables.
      Add second table for by_status data: columns Status, Count, Percentage, with progress bars.
      Add third table for by_bursary data: columns Bursary Name, Total Apps, Approved, Avg Amount.
      Use money() formatter for amounts, Math.round() for percentages.
      Files: c:/dev/SmartBursary-Complete/SmartBursary-Complete/frontend/src/App.jsx
      Verify: All three tables display correctly with real data; CSV export button still works.

## Feature 3: Enhanced Filters and Sorting

- [ ] 9. Add filter state and localStorage persistence to ApplicationsPage.
      In App.jsx, locate ApplicationsPage component (around line 640).
      Add state: bursaryFilter, sortBy='newest', constituencyFilter.
      Add useEffect to load from localStorage on mount: `JSON.parse(localStorage.getItem('appFilters'))`.
      Add useEffect to save to localStorage when filters change.
      Files: c:/dev/SmartBursary-Complete/SmartBursary-Complete/frontend/src/App.jsx
      Verify: Set filters, navigate away, return; filters should be restored.

- [ ] 10. Add bursary filter, sort dropdown, constituency filter, and Clear button to toolbar.
      In ApplicationsPage toolbar (after existing searchbox and status selectbox), add:
      - Bursary filter selectbox: `<div className="selectbox"><GraduationCap size={17}/><select value={bursaryFilter}...><option value="">All bursaries</option>{bursaries.map...}</select></div>`
      - Sort selectbox: 4 options (Newest first, Oldest first, Amount high-low, Priority score high-low)
      - Constituency selectbox (admin only): `{staff&&user.role==='admin'&&...}`
      - Clear filters button: `{(filter||bursaryFilter||sortBy!=='newest'||constituencyFilter)&&<Button kind="ghost"...><X/> Clear filters</Button>}`
      Pass bursaries prop from parent App component.
      Files: c:/dev/SmartBursary-Complete/SmartBursary-Complete/frontend/src/App.jsx
      Verify: Toolbar shows all 5 filter controls; Clear button appears when filters active.

- [ ] 11. Implement filter and sort logic in filtered useMemo.
      Move filtered useMemo from main App component into ApplicationsPage.
      Update ApplicationsPage signature to receive full applications array instead of pre-filtered.
      Extend filter logic to include bursaryFilter check: `&&(!bursaryFilter||String(a.bursary_id)===bursaryFilter)`.
      Add sorting after filtering: `.sort((a,b)=>{if(sortBy==='newest')return new Date(b.submitted_at)-new Date(a.submitted_at); ...})`.
      Handle all 4 sort options: newest, oldest, amount-high, priority-high.
      Files: c:/dev/SmartBursary-Complete/SmartBursary-Complete/frontend/src/App.jsx
      Verify: Test each filter and sort option; verify they work together correctly; verify Clear button resets all.

