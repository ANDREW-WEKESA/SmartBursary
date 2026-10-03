# SmartBursary 4-Features Enhancement: Technical Design

## Overview

This design covers four features to enhance SmartBursary: email notifications, application deadlines, reports/analytics dashboard, and enhanced filtering/sorting. The system uses Python/FastAPI backend with SQLAlchemy ORM (SQLite database), and React frontend in a single App.jsx file. All features maintain existing code patterns and architecture.

Implementation proceeds sequentially (Feature 1 → 2 → 3 → 4), with each feature fully implemented and tested before moving to the next.

---

## Feature 1: Email Notifications

### Overview
Add email notification system to send transactional emails for application lifecycle events. Use Python's built-in smtplib for SMTP delivery, avoiding external services initially.

### Data Model Changes
**No database schema changes required.** The existing `Notification` model stores in-app notifications; emails are sent at the same trigger points but delivered via SMTP rather than stored.

### Backend Implementation

#### 1.1 Email Configuration (config.py)
Add SMTP settings to the `Settings` class:
```python
smtp_host: str = "smtp.gmail.com"
smtp_port: int = 587
smtp_username: str = ""
smtp_password: str = ""
smtp_from_email: str = "noreply@smartbursary.com"
smtp_from_name: str = "SmartBursary"
smtp_enabled: bool = False  # Disabled by default
```

#### 1.2 Email Service Module (app/email_service.py)
Create new file with:
- `send_email(to_email: str, subject: str, body_html: str, body_plain: str)` - core sending function
- Template functions:
  - `send_application_submitted(user: User, application: Application)`
  - `send_status_changed(user: User, application: Application, old_status: str, new_status: str)`
  - `send_reviewer_notification(reviewer: User, application: Application)` - when new app assigned to constituency

**Error Handling:**
- SMTP connection failures: log error, continue without raising (email is non-critical)
- Invalid recipient email: log warning, skip sending
- All email failures logged to audit log with `action="Email send failed"`
- Function returns `(success: bool, error_msg: str | None)`

**Email Templates:**
HTML and plain-text templates inline in functions using f-strings. Templates include:
- Application submitted: confirmation with reference number, next steps
- Status changed: notify applicant of status update (Approved/Rejected/Disbursed)
- New application for reviewers: notify when app submitted for their constituency

**When SMTP is disabled** (smtp_enabled=False), functions log the email intent but don't send.

#### 1.3 Integration Points
Modify `main.py` at these locations:

**Application submission** (`submit_application`):
```python
# After creating application and in-app notification
from .email_service import send_application_submitted
send_application_submitted(user, a)
```

**Status update** (`update_status`):
```python
# After updating status
from .email_service import send_status_changed
send_status_changed(a.applicant, a, old, a.status)
```

**Reviewer notification on submission** (`submit_application`):
```python
# After application created, find reviewers for constituency
reviewers = db.scalars(select(User).where(
    User.role == "reviewer",
    User.constituency == b.constituency
)).all()
for reviewer in reviewers:
    send_reviewer_notification(reviewer, a)
```

#### 1.4 Environment Configuration
Update `.env.example`:
```
# Email configuration (optional)
SMTP_ENABLED=false
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@smartbursary.com
SMTP_FROM_NAME=SmartBursary
```

### Frontend Changes
**No UI changes required.** Emails are sent server-side automatically. Consider adding an admin settings page in future to test SMTP configuration (out of scope for this feature).

### Testing Strategy
- Unit tests: mock smtplib, verify template rendering and recipient logic
- Integration test: configure test SMTP (Mailtrap/Ethereal), verify emails sent at correct lifecycle points
- Manual: enable SMTP with real credentials, submit application and update status, verify emails received

### Edge Cases & Validation
- Missing SMTP credentials with smtp_enabled=true: log error on startup, don't crash
- Malformed applicant email (should be validated at registration, but defensive): skip email, log warning
- Reviewer has no email or invalid email: skip, log warning
- Multiple reviewers in same constituency: send to all
- Application status changed to non-notifiable status (e.g., "Under Review"): send generic update email or skip (design: send for Approved/Rejected/Disbursed only)

---

## Feature 2: Application Deadline Enforcement

### Overview
Add deadline enforcement to prevent applications after a bursary's deadline. Backend validation rejects late submissions; frontend shows deadline status and disables apply button.

### Data Model Changes

#### 2.1 Model Update (models.py)
**No change needed** - `Bursary.deadline` already exists as `Mapped[date]` (non-nullable).

#### 2.2 Migration Approach
**No migration required** - deadline field already exists in the schema. All existing bursaries have deadlines from seed data.

**Verification step:** Confirm all existing bursaries have valid deadline values (run query on startup or migration check).

### Backend Implementation

#### 2.1 Schema Updates (schemas.py)
**No changes needed** - `BursaryIn` and `BursaryOut` already include `deadline: date` field.

#### 2.2 Validation Logic (main.py)
The `submit_application` function already has deadline validation:
```python
if b.deadline < date.today(): 
    raise HTTPException(400, "The deadline for this bursary has passed")
```

**Enhance error message:**
```python
from datetime import date
if b.deadline < date.today():
    raise HTTPException(400, f"Applications closed. The deadline for {b.name} was {b.deadline.strftime('%B %d, %Y')}.")
```

**Additional validation:** When admin edits a bursary deadline, warn (but don't prevent) if moving deadline earlier than current date and active applications exist.

#### 2.3 List Bursaries Enhancement (main.py)
Add computed field to response indicating deadline status. Modify `bursary_out` helper:
```python
def bursary_out(b: Bursary):
    today = date.today()
    deadline_passed = b.deadline < today
    days_until_deadline = (b.deadline - today).days if not deadline_passed else 0
    
    return {
        "id": b.id,
        "name": b.name,
        # ... existing fields ...
        "deadline": b.deadline,
        "deadline_passed": deadline_passed,
        "days_until_deadline": days_until_deadline,
        "required_documents": json.loads(b.required_documents or "[]"),
        "active": b.active
    }
```

### Frontend Changes (App.jsx)

#### 2.1 Bursary Card Display
In `BursariesPage`, the program card already shows deadline. **Enhance badge logic:**
```javascript
<Badge tone={b.active ? (b.deadline_passed ? 'danger' : 'success') : 'danger'}>
  {b.active ? (b.deadline_passed ? 'Deadline passed' : 'Open') : 'Closed'}
</Badge>
```

**Add countdown display** (if deadline within 14 days and not passed):
```javascript
{b.active && !b.deadline_passed && b.days_until_deadline <= 14 && (
  <div className="deadline-warning">
    <Clock3 size={14} /> {b.days_until_deadline} {b.days_until_deadline === 1 ? 'day' : 'days'} remaining
  </div>
)}
```

**Disable apply button:**
```javascript
{!staff && (
  b.deadline_passed ? (
    <Button block disabled>Applications Closed</Button>
  ) : isEligible ? (
    <Button block onClick={() => go('apply')}>Apply for this program <ArrowRight size={16}/></Button>
  ) : (
    <Button block disabled>Not eligible to apply</Button>
  )
)}
```

#### 2.2 Apply Page Filtering
In `ApplyPage`, filter out bursaries with passed deadlines:
```javascript
const eligibleBursaries = bursaries.filter(b => 
  !b.deadline_passed && 
  (!user.constituency || !b.constituency || user.constituency === b.constituency)
);
```

**Error handling:** If user somehow submits application for expired bursary (e.g., deadline passed while form open), backend returns 400 error with clear message, shown in Notice component.

### CSS Additions (styles.css)
Add styles for deadline warning:
```css
.deadline-warning {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: var(--yellow-bg);
  border-left: 3px solid var(--yellow);
  font-size: 0.82rem;
  font-weight: 500;
  color: var(--yellow-dark);
  margin-top: 12px;
}
```

### Testing Strategy
- Backend: test submit_application with deadline in past (expect 400), deadline today (expect success), deadline future (expect success)
- Frontend: mock bursary data with various deadlines (past, today, 3 days, 30 days), verify badge/button states
- Integration: create bursary with tomorrow's deadline, wait until tomorrow (or manually adjust system date), verify apply button disabled and backend rejects

### Edge Cases
- User starts application form before deadline, submits after: backend rejects with clear message
- Admin extends deadline while applications in progress: backend allows, users can apply again
- Timezone handling: all date comparisons use `date.today()` (system date, no time component), consistent server-side
- Deadline on today's date: allowed (deadline is inclusive, passes at midnight)

---

## Feature 3: Reports and Analytics Dashboard

### Overview
Add analytics dashboard for admins/reviewers with summary statistics, charts, and breakdowns by constituency, bursary, and time periods. Use simple charting library (Recharts via CDN or native SVG).

### Data Model Changes
**No database schema changes required.** Analytics computed from existing Application and Bursary tables.

### Backend Implementation

#### 3.1 New Endpoints (main.py)

**Endpoint: GET /api/reports/overview**
```python
@app.get("/api/reports/overview")
def reports_overview(
    start_date: date | None = None,
    end_date: date | None = None,
    constituency: str = "",
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("admin", "reviewer"))
):
    """
    Summary statistics: total apps, breakdown by status, total disbursed amount.
    Filterable by date range and constituency.
    """
    query = select(Application)
    
    # Reviewer sees only their constituency
    if user.role == "reviewer" and user.constituency:
        query = query.join(Application.bursary).where(Bursary.constituency == user.constituency)
    
    # Optional filters
    if constituency and user.role == "admin":
        query = query.join(Application.bursary).where(Bursary.constituency == constituency)
    if start_date:
        query = query.where(Application.submitted_at >= datetime.combine(start_date, datetime.min.time()))
    if end_date:
        query = query.where(Application.submitted_at <= datetime.combine(end_date, datetime.max.time()))
    
    apps = db.scalars(query).all()
    
    status_counts = {}
    for status in STATUSES:
        status_counts[status] = sum(1 for a in apps if a.status == status)
    
    total_disbursed = sum(a.bursary.amount_kes for a in apps if a.status == "Disbursed")
    
    return {
        "total_applications": len(apps),
        "status_breakdown": status_counts,
        "total_disbursed": total_disbursed,
        "approval_rate": round(status_counts["Approved"] / len(apps) * 100, 1) if apps else 0,
        "filters_applied": {
            "start_date": start_date,
            "end_date": end_date,
            "constituency": constituency
        }
    }
```

**Error Handling:** 
- Invalid date range (end before start): return 400 with message "End date must be after start date"
- No applications match filters: return valid response with zero counts (not an error)

**Endpoint: GET /api/reports/bursary-stats**
```python
@app.get("/api/reports/bursary-stats")
def bursary_stats(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("admin", "reviewer"))
):
    """
    Per-bursary statistics: application count, approval rate, total disbursed.
    """
    query = select(Bursary).options(joinedload(Bursary.applications))
    
    if user.role == "reviewer" and user.constituency:
        query = query.where(Bursary.constituency == user.constituency)
    
    bursaries = db.scalars(query).unique().all()
    
    stats = []
    for b in bursaries:
        # Need to load applications separately due to lazy loading
        apps_query = select(Application).where(Application.bursary_id == b.id)
        apps = db.scalars(apps_query).all()
        
        approved = sum(1 for a in apps if a.status in ["Approved", "Disbursed"])
        disbursed_count = sum(1 for a in apps if a.status == "Disbursed")
        total_disbursed = sum(a.bursary.amount_kes for a in apps if a.status == "Disbursed")
        
        stats.append({
            "bursary_id": b.id,
            "bursary_name": b.name,
            "constituency": b.constituency,
            "total_applications": len(apps),
            "approved": approved,
            "disbursed": disbursed_count,
            "approval_rate": round(approved / len(apps) * 100, 1) if apps else 0,
            "total_disbursed": total_disbursed
        })
    
    return stats
```

**Endpoint: GET /api/reports/constituency-breakdown**
```python
@app.get("/api/reports/constituency-breakdown")
def constituency_breakdown(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("admin", "reviewer"))
):
    """
    Statistics grouped by constituency.
    Reviewers see only their constituency; admins see all.
    """
    # Get all bursaries with their constituencies
    bursaries_query = select(Bursary)
    if user.role == "reviewer" and user.constituency:
        bursaries_query = bursaries_query.where(Bursary.constituency == user.constituency)
    
    bursaries = db.scalars(bursaries_query).all()
    
    # Group by constituency
    constituency_map = {}
    for b in bursaries:
        const = b.constituency or "General"
        if const not in constituency_map:
            constituency_map[const] = {
                "constituency": const,
                "total_applications": 0,
                "approved": 0,
                "disbursed": 0,
                "total_disbursed": 0,
                "bursaries_count": 0
            }
        
        constituency_map[const]["bursaries_count"] += 1
        
        # Get applications for this bursary
        apps = db.scalars(select(Application).where(Application.bursary_id == b.id)).all()
        constituency_map[const]["total_applications"] += len(apps)
        constituency_map[const]["approved"] += sum(1 for a in apps if a.status in ["Approved", "Disbursed"])
        constituency_map[const]["disbursed"] += sum(1 for a in apps if a.status == "Disbursed")
        constituency_map[const]["total_disbursed"] += sum(b.amount_kes for a in apps if a.status == "Disbursed")
    
    return list(constituency_map.values())
```

**Endpoint: GET /api/reports/timeline**
```python
@app.get("/api/reports/timeline")
def applications_timeline(
    days: int = 30,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("admin", "reviewer"))
):
    """
    Applications over time (last N days), grouped by date.
    """
    from datetime import timedelta
    
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    query = select(Application).where(
        Application.submitted_at >= datetime.combine(start_date, datetime.min.time())
    )
    
    if user.role == "reviewer" and user.constituency:
        query = query.join(Application.bursary).where(Bursary.constituency == user.constituency)
    
    apps = db.scalars(query).all()
    
    # Group by date
    date_map = {}
    for a in apps:
        submission_date = a.submitted_at.date()
        if submission_date not in date_map:
            date_map[submission_date] = 0
        date_map[submission_date] += 1
    
    # Fill in missing dates with 0
    timeline = []
    current = start_date
    while current <= end_date:
        timeline.append({
            "date": current.isoformat(),
            "count": date_map.get(current, 0)
        })
        current += timedelta(days=1)
    
    return timeline
```

#### 3.2 Error Handling & Logging
All report endpoints:
- Log access to audit log: `audit(db, user, "Viewed reports: {endpoint}", "Report")`
- Database query failures: return 500 with generic message "Failed to generate report"
- Large result sets (>1000 apps): consider pagination or aggregation in future; for now, accept potential slowness with all data

### Frontend Implementation (App.jsx)

#### 3.1 Reports Page Component
Add new `ReportsPage` component after existing page components:

```javascript
function ReportsPage({busy, run}) {
  const [overview, setOverview] = useState(null);
  const [bursaryStats, setBursaryStats] = useState([]);
  const [constituencyStats, setConstituencyStats] = useState([]);
  const [timeline, setTimeline] = useState([]);
  const [filters, setFilters] = useState({
    startDate: '',
    endDate: '',
    constituency: ''
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    setLoading(true);
    try {
      const [overviewData, bursaryData, constituencyData, timelineData] = await Promise.all([
        api('/reports/overview?' + new URLSearchParams(filters)),
        api('/reports/bursary-stats'),
        api('/reports/constituency-breakdown'),
        api('/reports/timeline?days=30')
      ]);
      setOverview(overviewData);
      setBursaryStats(bursaryData);
      setConstituencyStats(constituencyData);
      setTimeline(timelineData);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = () => {
    loadReports();
  };

  if (loading) {
    return <div style={{textAlign: 'center', padding: '60px'}}>Loading reports...</div>;
  }

  return (
    <>
      <PageHeading 
        eyebrow="INSIGHTS" 
        title="Reports & Analytics" 
        desc="Summary statistics and trends across applications and bursaries."
      />
      
      {/* Filter controls */}
      <div className="panel" style={{marginBottom: '24px'}}>
        <h3>Filters</h3>
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginTop: '16px'}}>
          <Field label="Start date">
            <input 
              type="date" 
              value={filters.startDate}
              onChange={e => setFilters({...filters, startDate: e.target.value})}
            />
          </Field>
          <Field label="End date">
            <input 
              type="date" 
              value={filters.endDate}
              onChange={e => setFilters({...filters, endDate: e.target.value})}
            />
          </Field>
          <Field label="Constituency">
            <input 
              value={filters.constituency}
              onChange={e => setFilters({...filters, constituency: e.target.value})}
              placeholder="Filter by constituency..."
            />
          </Field>
        </div>
        <div style={{marginTop: '16px', display: 'flex', gap: '12px'}}>
          <Button onClick={applyFilters}>Apply Filters</Button>
          <Button kind="ghost" onClick={() => {
            setFilters({startDate: '', endDate: '', constituency: ''});
            setTimeout(loadReports, 50);
          }}>Clear</Button>
        </div>
      </div>

      {/* Summary cards */}
      <div className="stat-grid" style={{gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))'}}>
        <Stat icon={ClipboardCheck} label="Total Applications" value={overview?.total_applications} tone="blue" />
        <Stat icon={CheckCircle2} label="Approval Rate" value={`${overview?.approval_rate}%`} tone="green" />
        <Stat icon={Wallet} label="Total Disbursed" value={money(overview?.total_disbursed)} tone="purple" />
        <Stat icon={Activity} label="Pending Review" value={overview?.status_breakdown?.['Under Review'] || 0} tone="amber" />
      </div>

      {/* Charts section */}
      <div className="two-col" style={{marginTop: '32px', gap: '24px'}}>
        {/* Status breakdown */}
        <div className="panel">
          <h3>Applications by Status</h3>
          <div style={{marginTop: '20px'}}>
            {overview && Object.entries(overview.status_breakdown).map(([status, count]) => (
              <div key={status} style={{display: 'flex', justifyContent: 'space-between', padding: '10px 0', borderBottom: '1px solid var(--border)'}}>
                <span><Badge tone={statusClass(status)}>{status}</Badge></span>
                <b>{count}</b>
              </div>
            ))}
          </div>
        </div>

        {/* Constituency breakdown */}
        <div className="panel">
          <h3>By Constituency</h3>
          <div style={{marginTop: '20px'}}>
            {constituencyStats.map(c => (
              <div key={c.constituency} style={{padding: '12px 0', borderBottom: '1px solid var(--border)'}}>
                <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '6px'}}>
                  <b>{c.constituency}</b>
                  <span>{c.total_applications} applications</span>
                </div>
                <div style={{fontSize: '.85rem', color: 'var(--mute)'}}>
                  {c.approved} approved · {money(c.total_disbursed)} disbursed
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bursary performance table */}
      <div className="panel" style={{marginTop: '24px'}}>
        <h3>Bursary Performance</h3>
        <div style={{overflowX: 'auto', marginTop: '16px'}}>
          <table style={{width: '100%', borderCollapse: 'collapse'}}>
            <thead>
              <tr style={{borderBottom: '2px solid var(--border)', textAlign: 'left'}}>
                <th style={{padding: '12px'}}>Bursary</th>
                <th style={{padding: '12px'}}>Constituency</th>
                <th style={{padding: '12px'}}>Applications</th>
                <th style={{padding: '12px'}}>Approved</th>
                <th style={{padding: '12px'}}>Approval Rate</th>
                <th style={{padding: '12px'}}>Total Disbursed</th>
              </tr>
            </thead>
            <tbody>
              {bursaryStats.map(b => (
                <tr key={b.bursary_id} style={{borderBottom: '1px solid var(--border)'}}>
                  <td style={{padding: '12px'}}>{b.bursary_name}</td>
                  <td style={{padding: '12px'}}>{b.constituency || '—'}</td>
                  <td style={{padding: '12px'}}>{b.total_applications}</td>
                  <td style={{padding: '12px'}}>{b.approved}</td>
                  <td style={{padding: '12px'}}>{b.approval_rate}%</td>
                  <td style={{padding: '12px'}}>{money(b.total_disbursed)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Timeline chart (simple bar representation) */}
      <div className="panel" style={{marginTop: '24px'}}>
        <h3>Applications Over Time (Last 30 Days)</h3>
        <div style={{marginTop: '20px', display: 'flex', alignItems: 'flex-end', gap: '4px', height: '200px'}}>
          {timeline.map(d => {
            const maxCount = Math.max(...timeline.map(t => t.count), 1);
            const height = (d.count / maxCount) * 100;
            return (
              <div 
                key={d.date} 
                style={{
                  flex: 1,
                  height: `${height}%`,
                  background: 'var(--blue)',
                  borderRadius: '4px 4px 0 0',
                  minHeight: d.count > 0 ? '8px' : '2px',
                  opacity: d.count > 0 ? 1 : 0.2,
                  position: 'relative'
                }}
                title={`${d.date}: ${d.count} applications`}
              />
            );
          })}
        </div>
        <div style={{fontSize: '.8rem', color: 'var(--mute)', marginTop: '12px', textAlign: 'center'}}>
          {timeline[0]?.date} to {timeline[timeline.length - 1]?.date}
        </div>
      </div>
    </>
  );
}
```

#### 3.2 Navigation Integration
The "Reports" nav item already exists in the staff nav items array. Route to ReportsPage:
```javascript
{page === 'reports' && staff && <ReportsPage busy={busy} run={run} />}
```

#### 3.3 CSV Export Enhancement
The existing `/api/reports/applications.csv` endpoint provides CSV download. Add button to reports page:
```javascript
<Button onClick={downloadReport}>
  <ArrowDownToLine size={16} /> Export Applications CSV
</Button>
```

### CSS Additions
Add table and chart styles to styles.css:
```css
table {
  font-size: 0.9rem;
}
table th {
  font-weight: 600;
  color: var(--mute);
  font-size: 0.82rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}
table td {
  color: var(--text);
}
```

### Testing Strategy
- Backend: unit test each endpoint with various filters, verify aggregations correct
- Frontend: mock API responses, verify chart rendering and filter application
- Integration: seed database with diverse data (multiple constituencies, statuses, dates), verify reports match database state
- Performance: test with 1000+ applications, ensure queries complete <2s

### Edge Cases
- No applications in system: return zero counts, empty arrays (not errors)
- All applications same status: charts show single bar/row
- Invalid date range: backend returns 400, frontend shows error Notice
- Reviewer with no applications in constituency: valid empty report
- Division by zero in approval rate: handled with conditional (if apps else 0)

---

## Feature 4: Enhanced Filters and Sorting

### Overview
Add comprehensive filtering and sorting to Applications and Bursaries pages for reviewers/admins. Persist state in URL query parameters for shareability.

### Data Model Changes
**No database changes required.** Filtering/sorting done via SQL WHERE and ORDER BY clauses on existing columns.

### Backend Implementation

#### 4.1 Applications Endpoint Enhancement (main.py)
Modify `list_applications` endpoint to accept additional query params:

```python
@app.get("/api/applications", response_model=list[ApplicationOut])
def list_applications(
    q: str = "",
    status_filter: str = "",
    bursary_id: int | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    sort_by: str = "date_desc",  # date_desc, date_asc, amount_desc, amount_asc, name_asc, name_desc
    db: Session = Depends(get_db),
    user: User = Depends(current_user)
):
    query = app_query(db)
    
    # Role-based filtering (existing)
    if user.role == "applicant":
        query = query.where(Application.applicant_id == user.id)
    elif user.role == "reviewer" and user.constituency:
        query = query.join(Application.bursary).where(Bursary.constituency == user.constituency)
    
    # Status filter (existing)
    if status_filter and status_filter in STATUSES:
        query = query.where(Application.status == status_filter)
    
    # NEW: Bursary filter
    if bursary_id:
        query = query.where(Application.bursary_id == bursary_id)
    
    # NEW: Date range filter
    if start_date:
        query = query.where(Application.submitted_at >= datetime.combine(start_date, datetime.min.time()))
    if end_date:
        query = query.where(Application.submitted_at <= datetime.combine(end_date, datetime.max.time()))
    
    # Search query (existing)
    if q.strip():
        like = f"%{q.strip()}%"
        query = query.join(Application.applicant).where(or_(
            Application.application_number.ilike(like),
            Application.institution.ilike(like),
            Application.student_number.ilike(like),
            Application.national_id.ilike(like),
            User.full_name.ilike(like)
        ))
    
    # NEW: Sorting
    if sort_by == "date_asc":
        query = query.order_by(Application.submitted_at.asc())
    elif sort_by == "date_desc":
        query = query.order_by(Application.submitted_at.desc())
    elif sort_by == "amount_desc":
        query = query.join(Application.bursary).order_by(Bursary.amount_kes.desc())
    elif sort_by == "amount_asc":
        query = query.join(Application.bursary).order_by(Bursary.amount_kes.asc())
    elif sort_by == "name_asc":
        query = query.join(Application.applicant).order_by(User.full_name.asc())
    elif sort_by == "name_desc":
        query = query.join(Application.applicant).order_by(User.full_name.desc())
    else:
        query = query.order_by(Application.submitted_at.desc())  # default
    
    return [application_out(a) for a in db.scalars(query).unique().all()]
```

**Error Handling:**
- Invalid status_filter: ignore (don't apply filter)
- Invalid bursary_id (doesn't exist): ignore filter
- Invalid sort_by: default to date_desc
- Invalid date range: return 400 with message

#### 4.2 Bursaries Endpoint Enhancement (main.py)
The `list_bursaries` endpoint already supports `constituency` and `search` filters. **Add sorting:**

```python
@app.get("/api/bursaries", response_model=list[BursaryOut])
def list_bursaries(
    include_inactive: bool = False,
    constituency: str = "",
    search: str = "",
    sort_by: str = "deadline_asc",  # deadline_asc, deadline_desc, name_asc, name_desc
    db: Session = Depends(get_db),
    user: User = Depends(current_user)
):
    q = select(Bursary)
    
    # Active filter
    if not include_inactive or user.role == "applicant":
        q = q.where(Bursary.active.is_(True))
    
    # Constituency filter (existing)
    if constituency.strip():
        q = q.where(Bursary.constituency.ilike(f"%{constituency.strip()}%"))
    
    # Search filter (existing)
    if search.strip():
        search_term = f"%{search.strip()}%"
        q = q.where(or_(
            Bursary.name.ilike(search_term),
            Bursary.description.ilike(search_term),
            Bursary.eligibility.ilike(search_term),
            Bursary.constituency.ilike(search_term)
        ))
    
    # NEW: Sorting
    if sort_by == "deadline_asc":
        q = q.order_by(Bursary.deadline.asc())
    elif sort_by == "deadline_desc":
        q = q.order_by(Bursary.deadline.desc())
    elif sort_by == "name_asc":
        q = q.order_by(Bursary.name.asc())
    elif sort_by == "name_desc":
        q = q.order_by(Bursary.name.desc())
    else:
        q = q.order_by(Bursary.deadline.asc())  # default
    
    return [bursary_out(x) for x in db.scalars(q).all()]
```

### Frontend Implementation (App.jsx)

#### 4.1 Applications Page Enhancement
Modify `ApplicationsPage` component to add filter/sort controls and URL persistence:

```javascript
function ApplicationsPage({items, staff, go, onSelect}) {
  // Parse URL query params
  const urlParams = new URLSearchParams(window.location.search);
  const [query, setQuery] = useState(urlParams.get('q') || '');
  const [filter, setFilter] = useState(urlParams.get('status') || '');
  const [bursaryFilter, setBursaryFilter] = useState(urlParams.get('bursary') || '');
  const [startDate, setStartDate] = useState(urlParams.get('start') || '');
  const [endDate, setEndDate] = useState(urlParams.get('end') || '');
  const [sortBy, setSortBy] = useState(urlParams.get('sort') || 'date_desc');
  const [showFilters, setShowFilters] = useState(false);
  
  // Update URL when filters change
  useEffect(() => {
    const params = new URLSearchParams();
    if (query) params.set('q', query);
    if (filter) params.set('status', filter);
    if (bursaryFilter) params.set('bursary', bursaryFilter);
    if (startDate) params.set('start', startDate);
    if (endDate) params.set('end', endDate);
    if (sortBy !== 'date_desc') params.set('sort', sortBy);
    
    const newUrl = params.toString() ? `?${params}` : window.location.pathname;
    window.history.replaceState({}, '', newUrl);
    
    // Trigger API refetch with filters
    fetchFilteredApplications();
  }, [query, filter, bursaryFilter, startDate, endDate, sortBy]);
  
  const fetchFilteredApplications = async () => {
    try {
      const params = new URLSearchParams({
        q: query,
        status_filter: filter,
        bursary_id: bursaryFilter,
        start_date: startDate,
        end_date: endDate,
        sort_by: sortBy
      });
      const apps = await api(`/applications?${params}`);
      // Update applications state in parent (requires refactoring)
      // For now, client-side filtering as interim solution
    } catch (e) {
      console.error(e);
    }
  };
  
  // Client-side filtering for MVP (backend filtering preferred in production)
  const filtered = useMemo(() => {
    let result = items;
    
    if (filter) {
      result = result.filter(a => a.status === filter);
    }
    
    if (bursaryFilter) {
      result = result.filter(a => String(a.bursary_id) === bursaryFilter);
    }
    
    if (startDate) {
      result = result.filter(a => new Date(a.submitted_at) >= new Date(startDate));
    }
    
    if (endDate) {
      result = result.filter(a => new Date(a.submitted_at) <= new Date(endDate));
    }
    
    if (query) {
      const q = query.toLowerCase();
      result = result.filter(a => 
        [a.application_number, a.applicant_name, a.institution, a.student_number, a.bursary_name]
          .join(' ').toLowerCase().includes(q)
      );
    }
    
    // Sorting
    if (sortBy === 'date_asc') {
      result = [...result].sort((a, b) => new Date(a.submitted_at) - new Date(b.submitted_at));
    } else if (sortBy === 'date_desc') {
      result = [...result].sort((a, b) => new Date(b.submitted_at) - new Date(a.submitted_at));
    } else if (sortBy === 'amount_desc') {
      result = [...result].sort((a, b) => b.amount_kes - a.amount_kes);
    } else if (sortBy === 'amount_asc') {
      result = [...result].sort((a, b) => a.amount_kes - b.amount_kes);
    } else if (sortBy === 'name_asc') {
      result = [...result].sort((a, b) => a.applicant_name.localeCompare(b.applicant_name));
    } else if (sortBy === 'name_desc') {
      result = [...result].sort((a, b) => b.applicant_name.localeCompare(a.applicant_name));
    }
    
    return result;
  }, [items, query, filter, bursaryFilter, startDate, endDate, sortBy]);
  
  // Get unique bursaries for filter dropdown
  const uniqueBursaries = [...new Map(items.map(a => [a.bursary_id, a.bursary_name])).entries()];
  
  const clearFilters = () => {
    setQuery('');
    setFilter('');
    setBursaryFilter('');
    setStartDate('');
    setEndDate('');
    setSortBy('date_desc');
  };
  
  const hasActiveFilters = filter || bursaryFilter || startDate || endDate || query;
  
  return (
    <>
      <PageHeading 
        eyebrow="REVIEW QUEUE" 
        title="Applications" 
        desc="Review and manage bursary applications."
      />
      
      {/* Search and filter controls */}
      <div className="filter-bar">
        <div className="searchbox">
          <Search size={18}/>
          <input 
            value={query} 
            onChange={e => setQuery(e.target.value)} 
            placeholder="Search by applicant, reference, or student number…"
          />
        </div>
        
        <div className="filter-controls">
          <Button kind="outline" onClick={() => setShowFilters(!showFilters)}>
            <Filter size={16}/> Filters {hasActiveFilters && `(${[filter, bursaryFilter, startDate, endDate].filter(Boolean).length})`}
          </Button>
          
          <div className="selectbox">
            <select value={sortBy} onChange={e => setSortBy(e.target.value)}>
              <option value="date_desc">Newest first</option>
              <option value="date_asc">Oldest first</option>
              <option value="amount_desc">Highest amount</option>
              <option value="amount_asc">Lowest amount</option>
              <option value="name_asc">Name A-Z</option>
              <option value="name_desc">Name Z-A</option>
            </select>
          </div>
        </div>
      </div>
      
      {/* Expandable filter panel */}
      {showFilters && (
        <div className="panel filter-panel">
          <div className="form-grid">
            <Field label="Status">
              <select value={filter} onChange={e => setFilter(e.target.value)}>
                <option value="">All statuses</option>
                {statuses.map(s => <option key={s} value={s}>{s}</option>)}
              </select>
            </Field>
            
            <Field label="Bursary">
              <select value={bursaryFilter} onChange={e => setBursaryFilter(e.target.value)}>
                <option value="">All bursaries</option>
                {uniqueBursaries.map(([id, name]) => (
                  <option key={id} value={id}>{name}</option>
                ))}
              </select>
            </Field>
            
            <Field label="Start date">
              <input 
                type="date" 
                value={startDate}
                onChange={e => setStartDate(e.target.value)}
              />
            </Field>
            
            <Field label="End date">
              <input 
                type="date" 
                value={endDate}
                onChange={e => setEndDate(e.target.value)}
              />
            </Field>
          </div>
          
          {hasActiveFilters && (
            <Button kind="ghost" onClick={clearFilters} style={{marginTop: '12px'}}>
              <X size={14}/> Clear all filters
            </Button>
          )}
        </div>
      )}
      
      {/* Results */}
      <div className="results-header">
        <span>{filtered.length} {filtered.length === 1 ? 'application' : 'applications'}</span>
      </div>
      
      {filtered.length === 0 ? (
        <Empty 
          title="No applications found" 
          desc={hasActiveFilters ? "Try adjusting your filters." : "Applications will appear here once submitted."}
        />
      ) : (
        <div className="application-list">
          {filtered.map(a => (
            <button 
              key={a.id} 
              className="application-row" 
              onClick={() => onSelect(a)}
            >
              <div className="program-icon">
                <FileText size={19}/>
              </div>
              <div className="application-row-main">
                <b>{a.applicant_name}</b>
                <small>{a.application_number} · {a.bursary_name}</small>
              </div>
              <div style={{textAlign: 'right'}}>
                <Badge>{a.status}</Badge>
                <small>{dateFmt(a.submitted_at)}</small>
              </div>
              <ArrowRight size={16} className="row-arrow"/>
            </button>
          ))}
        </div>
      )}
    </>
  );
}
```

#### 4.2 Bursaries Page Enhancement
Add filter/sort controls to `BursariesPage` (already has constituency and search):

```javascript
// Inside BursariesPage component, add sortBy state:
const [sortBy, setSortBy] = useState('deadline_asc');

// Add sort control in filter bar:
<div className="selectbox">
  <select value={sortBy} onChange={e => setSortBy(e.target.value)}>
    <option value="deadline_asc">Deadline (soonest)</option>
    <option value="deadline_desc">Deadline (latest)</option>
    <option value="name_asc">Name A-Z</option>
    <option value="name_desc">Name Z-A</option>
  </select>
</div>

// Apply sorting to list:
const list = bursaries
  .filter(b => {
    const searchMatch = !search || (b.name + ' ' + b.description + ' ' + b.eligibility + ' ' + (b.constituency || '')).toLowerCase().includes(search.toLowerCase());
    const constituencyMatch = !selectedConstituency || b.constituency === selectedConstituency;
    return searchMatch && constituencyMatch;
  })
  .sort((a, b) => {
    if (sortBy === 'deadline_asc') return new Date(a.deadline) - new Date(b.deadline);
    if (sortBy === 'deadline_desc') return new Date(b.deadline) - new Date(a.deadline);
    if (sortBy === 'name_asc') return a.name.localeCompare(b.name);
    if (sortBy === 'name_desc') return b.name.localeCompare(a.name);
    return 0;
  });
```

### CSS Additions (styles.css)

```css
.filter-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  align-items: center;
}

.filter-bar .searchbox {
  flex: 1;
  min-width: 280px;
}

.filter-controls {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.filter-panel {
  margin-bottom: 20px;
  animation: slideDown 0.2s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.results-header {
  font-size: 0.88rem;
  color: var(--mute);
  margin-bottom: 12px;
  padding: 0 4px;
}

.selectbox select {
  padding: 10px 32px 10px 12px;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--panel);
  color: var(--text);
  font-size: 0.9rem;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23666' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
}
```

### Testing Strategy
- Backend: test each filter parameter individually and in combination, verify SQL query correctness
- Frontend: test filter interactions, verify URL updates, test browser back/forward buttons preserve filters
- Integration: apply filters, share URL with another user (simulate), verify same filtered view
- Edge cases: invalid dates, nonexistent bursary IDs, empty result sets

### Edge Cases & Validation
- End date before start date: backend returns 400, frontend shows error message
- Invalid status value: ignore filter (backend), show all
- Nonexistent bursary_id in filter: returns empty results (valid behavior)
- URL manipulation (invalid sort_by): backend defaults to date_desc
- Clearing filters: reset to initial state, remove query params from URL
- No results after filtering: show Empty component with helpful message
- Sorting while filtered: applies sort to filtered subset
- URL length limits: not a concern with typical filter values, but consider server-side storage (e.g., saved searches) for future

---

## Cross-Cutting Concerns

### Database Transactions
All write operations (email audit logs, application updates) already wrapped in session transactions. Ensure email sending happens AFTER database commit to avoid sending emails for rolled-back transactions.

### Logging & Observability
- Email send attempts logged to audit_logs table: action="Email sent: {type}" or "Email send failed: {type}"
- Report generation logged: action="Viewed reports: {endpoint}"
- All API endpoints use existing audit() helper

### Performance Considerations
- Reports endpoints: queries may be slow with large datasets (10k+ apps). Mitigation: add indexes on Application.submitted_at, Application.status, Bursary.constituency in future; for MVP, accept <5s query time
- Email sending: asynchronous dispatch recommended for production (e.g., background task queue), but synchronous acceptable for MVP
- Frontend filtering: client-side filtering OK for MVP (<500 items), but recommend refactoring to server-side filtering for production

### Security
- All new endpoints require authentication (Depends(current_user))
- Reports endpoints require admin/reviewer role (Depends(require_roles()))
- SMTP credentials stored in .env, never exposed to frontend
- SQL injection: protected by SQLAlchemy parameterized queries
- No new file uploads or external data ingestion (low risk)

### Backward Compatibility
- No breaking API changes (only additions)
- Existing frontend pages unaffected by new features
- Database schema changes (Feature 2) are additive only
- Existing tests should continue passing

---

## Implementation Order & Sequencing

### Feature 1: Email Notifications (Estimated: 4-6 hours)
1. Add SMTP config to config.py and .env.example
2. Create app/email_service.py with send_email and template functions
3. Integrate email calls in main.py (submit_application, update_status)
4. Test with test SMTP server
5. Commit: "feat: add email notification system"

### Feature 2: Application Deadline Enforcement (Estimated: 2-3 hours)
1. Enhance error message in submit_application deadline check
2. Update bursary_out helper to include deadline_passed and days_until_deadline
3. Update BursariesPage badge logic and apply button states
4. Update ApplyPage to filter out expired bursaries
5. Add CSS for deadline warning
6. Test deadline scenarios
7. Commit: "feat: enforce application deadlines with UI indicators"

### Feature 3: Reports and Analytics Dashboard (Estimated: 6-8 hours)
1. Add report endpoints to main.py (/reports/overview, /bursary-stats, /constituency-breakdown, /timeline)
2. Create ReportsPage component in App.jsx
3. Add routing for reports page
4. Add table and chart CSS
5. Test with diverse seed data
6. Commit: "feat: add reports and analytics dashboard"

### Feature 4: Enhanced Filters and Sorting (Estimated: 5-7 hours)
1. Enhance list_applications endpoint with new query params
2. Enhance list_bursaries endpoint with sort_by param
3. Refactor ApplicationsPage with filter controls and URL persistence
4. Enhance BursariesPage with sort controls
5. Add filter bar CSS
6. Test filter combinations and URL persistence
7. Commit: "feat: add enhanced filtering and sorting"

### Total Estimated Time: 17-24 hours

---

## Dependencies & Prerequisites

### External Libraries
- No new Python dependencies (smtplib is built-in)
- No new frontend dependencies (charts use native HTML/CSS)
- Existing: FastAPI, SQLAlchemy, React, lucide-react

### Environment Setup
- SMTP server credentials required for email testing (Gmail with app password, or Mailtrap)
- Seed diverse test data for reports/analytics testing

### Testing Environment
- Backend: pytest for unit tests (existing setup)
- Frontend: manual testing (no test framework currently)
- Integration: run full stack locally, test end-to-end workflows

---

## Assumptions & Open Questions

### Assumptions
1. **Email deliverability:** Assumes SMTP credentials provided are valid and not rate-limited. No retry logic or queue system in MVP.
2. **Timezone handling:** All dates use server local time (datetime.utcnow for timestamps, date.today() for date-only fields). No timezone localization.
3. **Constituency matching:** Assumes exact string match between User.constituency and Bursary.constituency. No fuzzy matching or normalization.
4. **Chart library:** Using native HTML/CSS for simple bar charts. For production, recommend Recharts or Chart.js, but avoided CDN dependency per constraints.
5. **URL persistence:** Uses window.location for URL manipulation. In future, consider React Router for cleaner history management.
6. **Performance limits:** Assumes <1000 applications and <50 bursaries for MVP. Pagination not implemented.

### Open Questions (to verify during implementation)
1. Should emails be sent for ALL status changes, or only Approved/Rejected/Disbursed? **Design choice:** Send for major statuses only (Approved, Rejected, Disbursed, Additional Information Required).
2. Should reviewers receive daily digest emails or immediate notification per application? **Design choice:** Immediate per application for MVP.
3. How to handle multiple reviewers in same constituency? **Design choice:** Send email to all reviewers in constituency.
4. Should deadline countdown show on home page bursary cards for applicants? **Design choice:** Yes, add to homepage bursary display if within 14 days.
5. Should CSV export respect active filters? **Design choice:** No for MVP, exports all applications. Add filtered export in future.

---

## Risk Mitigation

### High Risk: Email Sending Failures
**Risk:** SMTP misconfiguration or rate limits cause email failures, blocking application workflow.  
**Mitigation:** Email sending is non-blocking (failures logged but don't raise exceptions). smtp_enabled flag allows disabling email entirely.

### Medium Risk: Performance Degradation with Large Datasets
**Risk:** Reports and filtering slow with 1000+ applications.  
**Mitigation:** Add database indexes if needed (Application.submitted_at, Application.status, Bursary.constituency). Document performance limits in README.

### Medium Risk: URL State Management Complexity
**Risk:** URL query params get out of sync with component state, causing bugs.  
**Mitigation:** Single source of truth: parse URL params on mount, update URL on state change. Test browser navigation (back/forward).

### Low Risk: Deadline Timezone Confusion
**Risk:** Deadline cutoff at midnight server time may confuse users in different timezones.  
**Mitigation:** Document that deadlines are based on server time. In future, add timezone display or use UTC with local conversion.

---

## Verification Checklist (Implementation Phase)

- [ ] Feature 1: Send test email on application submission
- [ ] Feature 1: Verify email templates render correctly (HTML and plain text)
- [ ] Feature 1: Confirm email failure doesn't block application workflow
- [ ] Feature 2: Submit application after deadline, verify rejection
- [ ] Feature 2: Confirm deadline badge shows "Applications Closed" when passed
- [ ] Feature 2: Test apply button disabled for expired bursaries
- [ ] Feature 3: Access reports page, verify all endpoints return data
- [ ] Feature 3: Apply filters, verify report updates
- [ ] Feature 3: Verify reviewer sees only their constituency data
- [ ] Feature 4: Apply multiple filters, verify results correct
- [ ] Feature 4: Change sort order, verify applications reorder
- [ ] Feature 4: Share URL with filters, verify another session shows same view
- [ ] All features: Run existing tests, verify no regressions
- [ ] All features: Check browser console for errors
- [ ] All features: Verify responsive design (mobile, tablet)

---

## Future Enhancements (Out of Scope)

- Asynchronous email sending with background task queue (Celery/Redis)
- Advanced charting with Recharts or Chart.js library
- Saved filter presets for staff users
- Email template customization via admin UI
- Notification preferences (email vs in-app only)
- Pagination for large datasets
- Export filtered reports to CSV/PDF
- Real-time notifications via WebSockets
- Email bounce handling and deliverability monitoring
- Timezone-aware deadlines with user localization

---

## File Change Summary

### New Files
- `backend/app/email_service.py` - Email sending functions and templates

### Modified Files
- `backend/app/config.py` - Add SMTP configuration settings
- `backend/app/main.py` - Add report endpoints, enhance filtering/sorting, integrate email sending
- `backend/.env.example` - Add SMTP environment variables
- `frontend/src/App.jsx` - Add ReportsPage component, enhance ApplicationsPage and BursariesPage with filters/sorting
- `frontend/src/styles.css` - Add filter bar, table, chart, and deadline warning styles

### No Changes Required
- `backend/app/models.py` - No schema changes (deadline already exists)
- `backend/app/schemas.py` - No new schemas required
- `backend/app/database.py` - No changes
- `backend/app/security.py` - No changes

---

**Design Document Status:** Ready for Implementation  
**Author:** Kiro AI Agent  
**Date:** October 3, 2026  
**Version:** 1.0
