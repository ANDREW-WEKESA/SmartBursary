# Design Review: SmartBursary Four-Feature Enhancement

**Review Date:** 2026-01-03  
**Document:** design.md  
**Reviewer:** Design Review Subagent

---

## Verified Assumptions

✓ **Bursary.deadline field exists** - Confirmed in models.py as `Mapped[date]`  
✓ **Bursary.show_amount field exists** - Confirmed in models.py as `Mapped[bool]`  
✓ **Application.status field exists** - Confirmed in models.py with proper index  
✓ **Notification and AuditLog tables exist** - Confirmed in models.py  
✓ **User.constituency field exists** - Confirmed in models.py  
✓ **Bursary.constituency field exists** - Confirmed in models.py  
✓ **submit_application endpoint exists** - Confirmed at POST /api/applications  
✓ **update_status endpoint exists** - Confirmed at PATCH /api/applications/{application_number}/status  
✓ **Deadline validation exists** - Confirmed: `if b.deadline < date.today(): raise HTTPException(400,...)`  
✓ **STATUSES set includes "Disbursed"** - Confirmed in main.py  
✓ **Application.bursary relationship** - Confirmed as mapped relationship in models.py  
✓ **Config.py uses pydantic_settings** - Confirmed Settings class structure  

---

## Unverified/Wrong Assumptions

❌ **Amount per application is dynamic** - Design assumes all applications receive `bursary.amount_kes`, but user requirements indicate admins should be able to "edit amount allocated after allocation" (message 4). There is NO `allocated_amount` field on the Application model. The design incorrectly assumes disbursed amount = bursary.amount_kes for all applications.

❌ **Reports calculate total disbursed correctly** - Feature 3 reports endpoint calculates `total_disbursed = func.sum(Bursary.amount_kes)` for all Disbursed applications, but this doesn't match reality if allocations vary per applicant. This is a **data model gap**.

❌ **Chart.js URL in design** - Design specifies `https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js` but this should be added to index.html, which is not part of App.jsx. The design says "In index.html, add before closing `</body>`" but doesn't specify the path or verify index.html exists.

⚠️ **Frontend single-file constraint** - Design claims "React (frontend single App.jsx file)" but doesn't verify if there's an index.html, how Chart.js would be loaded into a Vite/React environment, or whether the project even has a traditional index.html structure.

---

## Findings

### HIGH Severity

**1. Missing allocated_amount field for per-application allocation tracking**

**Where:** Feature 3 (Reports), Data Model section, and application_out() function

**Problem:** The design's report calculations assume all approved/disbursed applications receive the full `bursary.amount_kes`. However, user requirement message 4 states "administrator can edit amount allocated after allocation," implying each application can have a custom allocation. The Application model lacks an `allocated_amount` field, and the design does not add one. This means:
- Reports will show incorrect total disbursed amounts
- Admins cannot edit per-application allocations
- The system cannot track actual payments vs. bursary program budgets

**Fix:**
Add to Feature 3 Data Model Changes section:
```python
# In models.py Application class, add:
allocated_amount: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)
```

Add migration instruction:
```python
# Migration: Add allocated_amount column
# alembic revision --autogenerate -m "Add allocated_amount to applications"
```

Update `application_out()` to include:
```python
"allocated_amount": a.allocated_amount or a.bursary.amount_kes,
```

Update Feature 3 reports endpoint `total_disbursed` calculation:
```python
disbursed_query = select(
    func.sum(func.coalesce(Application.allocated_amount, Bursary.amount_kes))
).join(Bursary).where(Application.status == "Disbursed")
```

Add a new endpoint for admins to edit allocation:
```python
@app.patch("/api/applications/{application_number}/allocation")
def update_allocation(
    application_number: str,
    allocated_amount: int = Query(..., ge=0),
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("admin"))
):
    a = db.scalar(select(Application).where(Application.application_number == application_number))
    if not a: raise HTTPException(404, "Application not found")
    a.allocated_amount = allocated_amount
    audit(db, user, f"Updated allocated amount to {allocated_amount}", "Application", a.id)
    db.commit()
    return {"allocated_amount": a.allocated_amount}
```

---

**2. Ambiguous email delivery mechanism and missing error logging specification**

**Where:** Feature 1, Email Module section

**Problem:** The design states "Logs errors but does not raise exceptions" and "logged via Python's `logging` module" but does not specify:
- Which logger instance to use (module-level logger? root logger?)
- What log level (ERROR? WARNING?)
- What information to include in the log message (recipient email? SMTP error details? which could contain sensitive data)

This is ambiguous and could lead to inconsistent error logging or inadvertently logging sensitive credentials.

**Fix:**
In Feature 1 Email Module section, replace "logged via Python's `logging` module" with:

```python
# At top of email.py:
import logging
logger = logging.getLogger(__name__)

# In send_email function:
except Exception as e:
    logger.error(
        f"Email send failed: to={to_email}, subject={subject[:50]}, error={type(e).__name__}: {str(e)}",
        exc_info=False  # Don't log full traceback to avoid credential exposure
    )
    return False
```

---

**3. Chart.js integration path and index.html location not specified**

**Where:** Feature 3, "Add Chart Library via CDN" section

**Problem:** The design says "In `index.html`, add before closing `</body>`" but:
- The path to index.html is not specified (is it `frontend/index.html`? `frontend/public/index.html`?)
- The design does not verify this file exists or can be edited
- For a Vite + React project, the correct approach may be different (Vite's index.html is in the project root, not public/)

The design does not investigate the actual project structure before specifying this change.

**Fix:**
Replace "In `index.html`, add before closing `</body>`" with:

"Locate the project's HTML entry point (typically `frontend/index.html` in Vite projects). Before the closing `</body>` tag, add:
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
```
If the project uses a different bundler or React setup without a direct index.html file, install Chart.js as an npm dependency instead:
```bash
npm install chart.js
```
Then import in App.jsx:
```javascript
import Chart from 'chart.js/auto';
```
And replace `window.Chart` references with `Chart`."

---

**4. Missing status filter value in ApplicationOut schema export**

**Where:** Feature 4, Backend Changes, Applications List Endpoint

**Problem:** The enhanced `list_applications` endpoint accepts `status_filter` as a parameter, but the design does not verify that the existing ApplicationOut schema and application_out() function properly handle all filter scenarios. The endpoint uses `ApplicationOut` as response_model but the design never verifies this schema exists or includes all necessary fields for the enhanced filters (like `show_amount` in the response).

Looking at the existing code, `application_out()` is a custom function, not a Pydantic schema, so the `response_model=list[ApplicationOut]` may fail at runtime if ApplicationOut schema doesn't match the dict structure returned by `application_out()`.

**Fix:**
In Feature 4 Backend Changes section, add verification step:

"Before implementing filter enhancements, verify that the ApplicationOut schema in schemas.py matches the dict structure returned by application_out() in main.py. Specifically confirm these fields exist in ApplicationOut:
- show_amount: bool
- amount_kes: int

If ApplicationOut is missing fields, update it to match. If application_out() returns extra fields not in ApplicationOut, either remove them or add them to the schema to prevent Pydantic validation errors."

Add this check to the Implementation Order section for Feature 4.

---

**5. Missing constituency-based access control in reports endpoints**

**Where:** Feature 3, reports endpoints for constituency_breakdown

**Problem:** The design correctly adds constituency filtering for reviewers in `/api/reports/overview` and `/api/reports/bursary-stats`, but the `/api/reports/constituency-breakdown` endpoint has this code:

```python
if user.role == "reviewer" and user.constituency:
    query = query.where(Bursary.constituency == user.constituency)
```

This means a reviewer will ONLY see their own constituency in the breakdown, which defeats the purpose of a "constituency breakdown" view. The endpoint would return an array with a single constituency, which is not useful.

**Fix:**
Change Feature 3 constituency_breakdown endpoint implementation to:

For reviewers, return only their own constituency as a single-item list (and rename the endpoint or its purpose to "my constituency stats"), OR remove this endpoint from reviewer access entirely and make it admin-only. Specify this clearly:

```python
@app.get("/api/reports/constituency-breakdown")
def constituency_breakdown(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("admin"))  # Admin only - reviewers see single constituency
):
    # No reviewer filtering - this is a cross-constituency view
    query = select(...)
    ...
```

Then in the frontend ReportsPage, conditionally render the constituency breakdown table:
```javascript
{user.role === 'admin' && constituencyStats.length > 1 && (
  <div className="panel">
    <h3>Constituency Statistics</h3>
    ...
  </div>
)}
```

---

### MEDIUM Severity

**6. Deadline countdown calculation doesn't account for timezone edge cases**

**Where:** Feature 2, Frontend Changes, `deadlineStatus` helper function

**Problem:** The function creates deadlines with `new Date(\`${deadline}T23:59:59\`)` but does not specify timezone. JavaScript Date constructor will interpret this as local time, which may not match the server's date comparison (server uses `date.today()` which is server timezone, likely UTC or Kenya EAT).

This creates a discrepancy: a deadline on 2026-10-30 at 23:59:59 local time (user's browser) may have already passed on the server if the user is in a timezone behind the server, causing applications to be rejected even though the frontend shows "Open".

**Fix:**
Add timezone clarification to Feature 2 Testing Strategy section:

"Testing Strategy (updated):
- Verify deadline enforcement works correctly for users in different timezones by:
  - Setting system timezone to UTC-8 (PST) and attempting to submit on deadline day
  - Confirming server date.today() comparison uses Kenya EAT or UTC consistently
- Consider updating deadlineStatus to use UTC explicitly:
  ```javascript
  const deadlineDate = new Date(`${deadline}T23:59:59Z`); // Z suffix = UTC
  ```
  And update server deadline check to:
  ```python
  # Use end of day in Kenya timezone (EAT = UTC+3)
  from datetime import datetime, timezone, timedelta
  eat = timezone(timedelta(hours=3))
  deadline_end = datetime.combine(b.deadline, datetime.max.time()).replace(tzinfo=eat)
  if datetime.now(eat) > deadline_end:
      raise HTTPException(400, "The deadline for this bursary has passed")
  ```"

---

**7. Client-side filtering in ApplicationsPage duplicates server filtering**

**Where:** Feature 4, Frontend Changes, ApplicationsPage Enhancements

**Problem:** The enhanced ApplicationsPage component performs client-side filtering AND the design updates the backend endpoint to accept filter params. This creates two problems:
- The design says "Client-side filtering (backend already does this, but keep for immediate feedback)" but then implements full client-side filter logic that duplicates the server queries, which is confusing
- The useEffect that calls setQueryParams would trigger on EVERY filter state change, but there's no corresponding API call to fetch filtered data from the server. The filters only work on the already-loaded `items` prop.

This means the URL params are set, but the backend filter params are never sent, making the backend enhancements useless.

**Fix:**
In Feature 4 ApplicationsPage section, add:

"To use the backend filtering, add a useEffect that fetches filtered applications when query params change:

```javascript
const [items, setItems] = useState([]);
const [loading, setLoading] = useState(false);

useEffect(() => {
  loadApplications();
}, [query, statusFilter, bursaryFilter, dateFrom, dateTo, sortBy, sortOrder]);

async function loadApplications() {
  setLoading(true);
  try {
    const params = new URLSearchParams({
      q: query,
      status_filter: statusFilter,
      bursary_id: bursaryFilter,
      date_from: dateFrom,
      date_to: dateTo,
      sort_by: sortBy,
      sort_order: sortOrder
    });
    const data = await api(`/applications?${params.toString()}`);
    setItems(data);
  } catch (e) {
    console.error(e);
  } finally {
    setLoading(false);
  }
}
```

Then update the component to use `items` state instead of the `items` prop, and remove the client-side filtering and sorting logic (lines 'const filtered = ...' and 'const sorted = ...'), since the server now handles this."

---

**8. Missing sort column for Bursary.constituency in Feature 4 backend**

**Where:** Feature 4, Backend Changes, Bursaries List Endpoint enhancement

**Problem:** The design adds sorting logic with:
```python
sort_column = {
    "deadline": Bursary.deadline,
    "name": Bursary.name,
    "amount": Bursary.amount_kes,
    "constituency": Bursary.constituency
}.get(sort_by, Bursary.deadline)
```

But `Bursary.constituency` is a string column. Sorting on strings in SQLite is case-sensitive by default, which will produce unexpected ordering (e.g., "Webuye East" comes before "kilifi" because 'W' < 'k' in ASCII). This is likely not the intended behavior for user-facing constituency sorting.

**Fix:**
Update the sort_column mapping to use case-insensitive collation:

```python
if sort_by == "constituency":
    sort_column = func.lower(Bursary.constituency)
elif sort_by == "name":
    sort_column = func.lower(Bursary.name)
else:
    sort_column = {
        "deadline": Bursary.deadline,
        "amount": Bursary.amount_kes,
    }.get(sort_by, Bursary.deadline)
```

---

**9. Error handling for invalid date formats is silent, not graceful**

**Where:** Feature 4, Backend Changes, Applications List Endpoint date parsing

**Problem:** The design has:
```python
if date_from:
    try:
        date_from_parsed = datetime.strptime(date_from, "%Y-%m-%d")
        query = query.where(Application.submitted_at >= date_from_parsed)
    except ValueError:
        pass  # Ignore invalid date
```

While this prevents the endpoint from crashing, it silently ignores invalid date formats. A user who mistakenly sends `date_from=10/02/2026` (wrong format) will get unfiltered results with no indication that their filter was ignored. This is confusing and violates the principle of providing clear feedback.

**Fix:**
Replace `pass` with a 400 error response:

```python
if date_from:
    try:
        date_from_parsed = datetime.strptime(date_from, "%Y-%m-%d")
        query = query.where(Application.submitted_at >= date_from_parsed)
    except ValueError:
        raise HTTPException(400, f"Invalid date_from format. Use YYYY-MM-DD, received: {date_from}")
```

Apply the same fix to `date_to` parsing.

---

**10. BursariesPage filter/sort state not persisted to URL**

**Where:** Feature 4, Frontend Changes, BursariesPage Enhancements

**Problem:** The design adds `activeFilter`, `sortBy`, and `sortOrder` state to BursariesPage but does NOT integrate the `useQueryParams` hook or update URL query params like ApplicationsPage does. This means:
- Bursary filters are not shareable via URL
- Browser back/forward doesn't preserve bursary filters
- The stated goal "Persist filter state in URL query params for shareable links" is not met for the BursariesPage

**Fix:**
In BursariesPage Enhancements section, add after state declarations:

```javascript
const [queryParams, setQueryParams] = useQueryParams();
const [activeFilter, setActiveFilter] = useState(queryParams.get('active') || '');
const [sortBy, setSortBy] = useState(queryParams.get('sort') || 'deadline');
const [sortOrder, setSortOrder] = useState(queryParams.get('order') || 'asc');

useEffect(() => {
  setQueryParams({ active: activeFilter, sort: sortBy, order: sortOrder });
}, [activeFilter, sortBy, sortOrder]);
```

---

**11. Email templates use inline HTML but no sanitization or escaping specified**

**Where:** Feature 1, Email Module, Email Templates section

**Problem:** The design states email templates are "inline functions" that return HTML, with variables like `applicant_name`, `application_number`, `reviewer_comment` embedded. However, it does not specify whether these values should be HTML-escaped.

If a user enters a name like `<script>alert('xss')</script>` or a reviewer comment with HTML tags, these could be rendered as HTML in the email client. While email clients generally sanitize scripts, HTML injection is still a risk (e.g., rendering misleading links or formatting).

**Fix:**
Add to Feature 1 Email Module section:

"All user-provided values (applicant_name, reviewer_comment, bursary_name, etc.) must be HTML-escaped before embedding in email templates. Use Python's `html.escape()`:

```python
import html

def status_changed_email(applicant_name, application_number, old_status, new_status, reviewer_comment):
    safe_name = html.escape(applicant_name)
    safe_comment = html.escape(reviewer_comment)
    safe_old = html.escape(old_status)
    safe_new = html.escape(new_status)
    html_body = f'''<html>...{safe_name}...{safe_comment}...</html>'''
    text_body = f'''Plain text version with {applicant_name}...'''
    return html_body, text_body
```

System-controlled strings (application_number, bursary_name from database) can be assumed safe, but apply escaping to all user input."

---

**12. Reviewer notification query may send duplicate emails**

**Where:** Feature 1, Integration Points, POST /api/applications

**Problem:** The design states:
> "query all users with `role='reviewer'` where `user.constituency == b.constituency`, and for each: [send email]"

But does not specify:
- The SQL query to use (select statement)
- Whether to check `user.active` flag (disabled reviewers shouldn't get emails)
- Whether to check if `reviewer.email` is valid/non-empty

If a constituency has 10 reviewers and 3 are inactive, all 10 will still receive emails.

**Fix:**
Add explicit query to Feature 1 integration section:

```python
reviewers = db.scalars(
    select(User)
    .where(User.role == 'reviewer')
    .where(User.constituency == b.constituency)
    .where(User.active == True)
    .where(User.email != '')
).all()

for reviewer in reviewers:
    html, text = new_application_assigned_email(
        reviewer.full_name, a.application_number, user.full_name, b.name, b.constituency
    )
    send_email(reviewer.email, f"New Application: {a.application_number}", html, text)
```

---

### NIT Severity

**13. SMTP connection not reused, performance overhead**

**Where:** Feature 1, Email Module, send_email function

**Problem:** The design implies each `send_email()` call opens a new SMTP connection, sends one email, and closes the connection. For bulk notifications (e.g., 10 reviewers notified when one application is submitted), this creates 10 sequential SMTP connections, which is slow (~200ms per connection).

**Fix (optional optimization):**
For MVP, this is acceptable. For production, consider adding an SMTP connection pool or batching emails. Add to Feature 1 Performance Considerations:

"Current implementation opens a new SMTP connection per email. For bulk notifications (>5 emails), consider implementing a context manager that reuses the connection:
```python
from contextlib import contextmanager

@contextmanager
def smtp_connection():
    smtp = smtplib.SMTP(settings.smtp_host, settings.smtp_port)
    smtp.starttls()
    smtp.login(settings.smtp_username, settings.smtp_password)
    try:
        yield smtp
    finally:
        smtp.quit()
```

This is a future optimization, not required for initial implementation."

---

**14. Chart.js version pinned, but no fallback if CDN unavailable**

**Where:** Feature 3, Add Chart Library via CDN

**Problem:** The design pins Chart.js to version 4.4.0 from a CDN but provides no fallback if the CDN is unreachable (offline environment, CDN outage, corporate firewall blocking jsdelivr.net). The ReportsPage will fail to render charts with no error message shown to the user.

**Fix:**
Add error handling to Feature 3 renderCharts function:

```javascript
function renderCharts(ovw, bursary, constituency) {
  if (!window.Chart) {
    console.warn('Chart.js not loaded, skipping chart rendering');
    // Optionally show a message to the user
    document.querySelectorAll('canvas').forEach(canvas => {
      const parent = canvas.parentElement;
      const msg = document.createElement('p');
      msg.style.color = 'var(--mute)';
      msg.textContent = 'Chart library unavailable. Data shown in tables below.';
      parent.replaceChild(msg, canvas);
    });
    return;
  }
  // ... rest of chart rendering
}
```

---

**15. Empty state messages could be more actionable**

**Where:** Feature 4, ApplicationsPage filtered empty state

**Problem:** When filters produce no results, the empty state says "Try adjusting your filters." This is generic and doesn't tell the user WHICH filter might be too restrictive. For example, if they filtered by "Approved" status but also by a date range that has no approved applications, it's unclear which constraint to relax.

**Fix (optional UX improvement):**
Enhance empty state to show active filters:

```javascript
{sorted.length === 0 ? (
  <Empty 
    title="No applications found" 
    desc={
      (statusFilter || bursaryFilter || dateFrom || dateTo) 
        ? `No applications match your current filters${statusFilter ? ` (Status: ${statusFilter})` : ''}${bursaryFilter ? ` (Bursary: ${bursaries.find(b => String(b.id) === bursaryFilter)?.name})` : ''}. Try clearing some filters.`
        : "No applications have been submitted yet."
    }
  />
) : (
  ...
)}
```

---

**16. Reports page lacks loading skeleton or spinner**

**Where:** Feature 3, ReportsPage component

**Problem:** The ReportsPage shows "Loading reports..." as plain text while fetching data. For a dashboard with multiple aggregation queries, this could take 1-2 seconds. The sudden appearance of charts and tables after loading completes is jarring.

**Fix (optional UX improvement):**
Replace the loading text with skeleton placeholders that match the final layout:

```javascript
if (loading) {
  return (
    <>
      <PageHeading eyebrow="INSIGHTS" title="Reports & Analytics" desc="Application statistics and constituency performance." />
      <div className="stat-grid">
        {[1,2,3,4].map(i => <div key={i} className="stat-card skeleton" style={{height: '100px'}}></div>)}
      </div>
      <div className="two-col">
        <div className="panel skeleton" style={{height: '300px'}}></div>
        <div className="panel skeleton" style={{height: '300px'}}></div>
      </div>
    </>
  );
}
```

Add skeleton CSS:
```css
.skeleton {
  background: linear-gradient(90deg, var(--bg-secondary) 25%, var(--bg) 50%, var(--bg-secondary) 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
}
@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

---

**17. Email from_name uses generic "SmartBursary" instead of constituency name**

**Where:** Feature 1, Configuration, smtp_from_name

**Problem:** All emails come from "SmartBursary" even though applications and decisions are constituency-specific. For reviewers managing multiple constituencies, or applicants applying to different programs, seeing which constituency sent the email at a glance would be helpful.

**Fix (optional enhancement):**
Make from_name dynamic based on constituency:

```python
def send_email(to_email: str, subject: str, body_html: str, body_text: str = None, from_name: str = None):
    from_name = from_name or settings.smtp_from_name
    # ... rest of function uses from_name parameter
```

Then in integration points:
```python
send_email(
    reviewer.email, 
    f"New Application: {a.application_number}", 
    html, 
    text,
    from_name=f"SmartBursary - {b.constituency}"
)
```

---

**18. Priority score calculation helper is redundant in reports**

**Where:** Feature 3, constituency_breakdown endpoint includes `func.avg(Application.priority_score)`

**Problem:** The design includes average priority score in constituency breakdown reports, but the existing codebase comment in main.py states:
> "Transparent demo heuristic only; it is not an eligibility or award decision."

Including average priority score in official reports may give it unintended weight, implying it's a decision factor when it's explicitly labeled as a demo indicator only. This could cause confusion.

**Fix (optional clarification):**
Remove `avg_priority_score` from constituency_breakdown response, or add a disclaimer in the frontend table:

```javascript
<th>Avg Priority<sup>*</sup></th>
// And add footnote:
<small style={{color: 'var(--mute)', fontSize: '.75rem'}}>
  * Demo indicator only, not used in award decisions
</small>
```

---

## Verdict

**CHANGES_REQUESTED**

**Summary:**  
5 HIGH severity findings and 7 MEDIUM severity findings block approval. Key issues:
- Missing `allocated_amount` field breaks disbursement tracking and per-application allocation editing (requirement from user message 4)
- Ambiguous error logging specification could expose credentials
- Chart.js integration assumes index.html exists without verification
- ApplicationOut schema compatibility not verified before filter enhancements
- Reports constituency breakdown has illogical access control for reviewers
- Timezone handling creates deadline enforcement discrepancies
- Backend filter enhancements are implemented but never called from frontend
- String sorting lacks case-insensitive collation
- Invalid date formats fail silently instead of returning errors
- Bursary page filters don't persist to URL despite stated objective
- Email template HTML injection not addressed
- Reviewer notification query doesn't filter inactive users

The design is well-structured and comprehensive, but these gaps must be resolved before implementation to avoid rework and ensure the system meets user requirements (especially the allocation editing requirement).

---

**Recommendations:**
1. Add the `allocated_amount` field and migration as top priority (HIGH #1)
2. Clarify email error logging to prevent credential leakage (HIGH #2)
3. Investigate actual project structure for Chart.js integration (HIGH #3)
4. Fix the frontend-backend filter coordination mismatch (MEDIUM #7)
5. Resolve timezone ambiguity to prevent deadline enforcement bugs (MEDIUM #6)
6. Address the remaining HIGH and MEDIUM findings listed above

Once these are addressed, re-review for approval.
