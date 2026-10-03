# Implementation Plan

## Context
Adding constituency-based multi-tenancy to SmartBursary. Reviewers will be scoped to specific constituencies, seeing only applications for bursaries in their assigned constituency. Admins retain global access. Bursaries gain an open/close toggle. A staff management UI allows admins to create reviewer accounts with constituency assignments.

## Database Schema Changes

### User Model (backend/app/models.py)
- [ ] 1. Add `constituency` column to User model after the `role` field:
      ```python
      constituency: Mapped[str | None] = mapped_column(String(100), nullable=True, default=None)
      ```
      Files: backend/app/models.py (line ~18 after role field)
      Verify: Start backend server, check GET /api/auth/me response includes constituency field

- [ ] 2. Create migration script at backend/add_user_constituency.py:
      ```python
      from sqlalchemy import text
      from app.database import engine
      
      try:
          with engine.connect() as conn:
              conn.execute(text("ALTER TABLE users ADD COLUMN constituency VARCHAR(100)"))
              conn.commit()
          print("✓ Added constituency column to users table")
      except Exception as e:
          if "already exists" in str(e).lower() or "duplicate column" in str(e).lower():
              print("✓ Column already exists, skipping")
          else:
              raise
      ```
      Files: backend/add_user_constituency.py (new file)
      Verify: Run `cd backend && python add_user_constituency.py` twice, second run shows "already exists"

## Backend API Endpoints

- [ ] 3. Update StaffUserIn schema to accept constituency field:
      Add `constituency: str = ""` field to StaffUserIn class in backend/app/schemas.py (after role field)
      Files: backend/app/schemas.py
      Verify: POST /api/admin/users with constituency in payload does not raise validation error

- [ ] 4. Update UserOut schema to expose constituency:
      Add `constituency: str` field to UserOut class in backend/app/schemas.py
      Files: backend/app/schemas.py
      Verify: GET /api/auth/me returns constituency field in response

- [ ] 5. Modify POST /api/admin/users to save constituency:
      In backend/app/main.py create_staff_user function (line ~141), add after password_hash assignment:
      ```python
      staff_user = User(
          full_name=data.full_name.strip(),
          email=email,
          password_hash=hash_password(data.password),
          role=data.role,
          constituency=data.constituency.strip() if data.constituency else None,
          active=True
      )
      ```
      Update audit log call to include constituency in details:
      ```python
      audit(db, user, f"Created {data.role} account", "User", staff_user.id, f"{email} - {data.constituency or 'No constituency'}")
      ```
      Files: backend/app/main.py
      Verify: Create staff user with constituency via POST /api/admin/users, check audit log and db

- [ ] 6. Add PATCH /api/bursaries/{bursary_id}/toggle endpoint in backend/app/main.py after existing PATCH /api/bursaries/{bursary_id}:
      ```python
      @app.patch("/api/bursaries/{bursary_id}/toggle", response_model=BursaryOut)
      def toggle_bursary(bursary_id: int, db: Session = Depends(get_db), user: User = Depends(require_roles("admin"))):
          b = db.get(Bursary, bursary_id)
          if not b:
              raise HTTPException(404, "Bursary not found")
          b.active = not b.active
          status_text = "opened" if b.active else "closed"
          audit(db, user, f"Toggled bursary status to {status_text}", "Bursary", b.id, b.name)
          db.commit()
          db.refresh(b)
          return bursary_out(b)
      ```
      Files: backend/app/main.py
      Verify: PATCH /api/bursaries/1/toggle as admin, check bursary active field flips, audit log created

- [ ] 7. Add constituency filter to GET /api/applications for reviewers:
      In backend/app/main.py list_applications function (line ~214), after `if user.role == "applicant"` block, add:
      ```python
      elif user.role == "reviewer" and user.constituency:
          query = query.join(Application.bursary).where(Bursary.constituency == user.constituency)
      ```
      Files: backend/app/main.py
      Verify: GET /api/applications as reviewer with constituency returns only matching applications

- [ ] 8. Add constituency filter to GET /api/dashboard/stats for reviewers:
      In backend/app/main.py dashboard_stats function (line ~245), wrap all count queries with constituency filter:
      ```python
      if user.role == "reviewer" and user.constituency:
          base_filter = select(Application.id).join(Application.bursary).where(Bursary.constituency == user.constituency).subquery()
          total = db.scalar(select(func.count()).select_from(base_filter)) or 0
          statuses = {s: db.scalar(select(func.count(Application.id)).where(Application.id.in_(select(base_filter.c.id)), Application.status == s)) or 0 for s in sorted(STATUSES)}
          duplicate_flags = db.scalar(select(func.count(Application.id)).where(Application.id.in_(select(base_filter.c.id)), Application.duplicate_risk == "HIGH")) or 0
          bursaries = db.scalar(select(func.count(Bursary.id)).where(Bursary.constituency == user.constituency, Bursary.active.is_(True))) or 0
      else:
          # existing unfiltered queries
          total = db.scalar(select(func.count(Application.id))) or 0
          statuses = {s: db.scalar(select(func.count(Application.id)).where(Application.status == s)) or 0 for s in sorted(STATUSES)}
          duplicate_flags = db.scalar(select(func.count(Application.id)).where(Application.duplicate_risk == "HIGH")) or 0
          bursaries = db.scalar(select(func.count(Bursary.id)).where(Bursary.active.is_(True))) or 0
      ```
      Files: backend/app/main.py
      Verify: GET /api/dashboard/stats as reviewer with constituency returns scoped counts

- [ ] 9. Add GET /api/staff endpoint to list staff users:
      In backend/app/main.py after POST /api/admin/users, add:
      ```python
      @app.get("/api/staff")
      def list_staff(db: Session = Depends(get_db), user: User = Depends(require_roles("admin"))):
          staff_users = db.scalars(select(User).where(User.role.in_(["admin", "reviewer"])).order_by(User.full_name)).all()
          return [{"id": u.id, "full_name": u.full_name, "email": u.email, "role": u.role, "constituency": u.constituency or "", "active": u.active} for u in staff_users]
      ```
      Files: backend/app/main.py
      Verify: GET /api/staff as admin returns list of staff users with all fields

## Frontend Changes

- [ ] 10. Update bursary card badges to use active field in BursariesPage component (frontend/src/App.jsx):
       Locate program-card rendering in BursariesPage (around line in map over list). Change the Badge logic:
       Replace `<Badge tone={new Date(\`${b.deadline}T23:59:59\`)<new Date()?'danger':'success'}>{new Date(\`${b.deadline}T23:59:59\`)<new Date()?'Closed':'Open'}</Badge>`
       with `<Badge tone={b.active ? 'success' : 'danger'}>{b.active ? 'Open' : 'Closed'}</Badge>`
       Files: frontend/src/App.jsx
       Verify: Open bursary page, badges show Open for active=true, Closed for active=false

- [ ] 11. Add toggle button to bursary cards (staff view only):
       In same program-card-top div after Badge, add:
       ```jsx
       {staff && <button className="icon-btn" onClick={async (e) => {
           e.stopPropagation();
           await run(async () => {
               await api(`/bursaries/${b.id}/toggle`, {method: 'PATCH'});
               await refresh();
               await loadConstituencies();
           });
       }} title={b.active ? 'Close applications' : 'Open applications'}>
           {b.active ? <X size={16}/> : <Plus size={16}/>}
       </button>}
       ```
       Ensure X is imported from lucide-react at top of file
       Files: frontend/src/App.jsx
       Verify: As admin, click toggle button, badge changes immediately

- [ ] 12. Add constituency banner to Dashboard component:
       In Dashboard component (frontend/src/App.jsx), after PageHeading and before stat-grid, add:
       ```jsx
       {user.constituency && <div className="notice" style={{marginBottom: '20px', background: 'var(--green-soft)', borderColor: 'var(--green)', color: 'var(--green)'}}>
           <MapPin size={18}/><span><b>Your Constituency:</b> {user.constituency}</span>
       </div>}
       ```
       Ensure MapPin is imported from lucide-react
       Files: frontend/src/App.jsx
       Verify: Login as reviewer with constituency, dashboard shows banner

- [ ] 13. Add constituency banner to ApplicationsPage:
       In ApplicationsPage component, after PageHeading and before toolbar, add:
       ```jsx
       {staff && user.constituency && <div className="notice" style={{marginBottom: '18px', background: 'var(--green-soft)', borderColor: 'var(--green)', color: 'var(--green)'}}>
           <MapPin size={18}/><span><b>Filtering by constituency:</b> {user.constituency}</span>
       </div>}
       ```
       Files: frontend/src/App.jsx
       Verify: As reviewer with constituency, applications page shows filter banner

- [ ] 14. Add constituency column to applications table (staff view):
       In ApplicationsPage table thead, after 'Program' th, add: `{staff && <th>Constituency</th>}`
       In tbody tr, after bursary name td, add:
       ```jsx
       {staff && <td><span className="badge" style={{fontSize: '.7rem'}}>
           <MapPin size={11} style={{marginRight: '4px', verticalAlign: 'middle'}}/>
           {a.bursary_name} constituency (needs bursary object passed)
       </span></td>}
       ```
       Note: May need to modify application_out in backend to include bursary.constituency in response
       Files: frontend/src/App.jsx, backend/app/main.py
       Verify: Applications table shows constituency column with badge

- [ ] 15. Add 'Team' navigation item and page:
       In App component, add to navItems staff array (before 'reports'): `['staff', 'Team', Users]`
       Add state: `const [staffList, setStaffList] = useState([]); const [constituencies, setConstituencies] = useState([]);`
       Update refresh function to load staff list for admin:
       ```javascript
       if (getSavedUser()?.role === "admin") {
           setStaffList(await api("/staff"));
           const constData = await api("/bursaries/constituencies");
           setConstituencies(constData.map(c => c.constituency));
       }
       ```
       Add page conditional: `{page==='staff' && staff && <StaffPage staffList={staffList} setStaffList={setStaffList} busy={busy} run={run} refresh={refresh} constituencies={constituencies} setConstituencies={setConstituencies}/>}`
       Files: frontend/src/App.jsx
       Verify: 'Team' appears in admin sidebar navigation

- [ ] 16. Implement StaffPage component:
       Create StaffPage function component in frontend/src/App.jsx before App return:
       ```javascript
       function StaffPage({staffList, setStaffList, busy, run, refresh, constituencies, setConstituencies}) {
           const [showCreate, setShowCreate] = useState(false);
           async function createStaff(e) {
               e.preventDefault();
               const fd = new FormData(e.currentTarget);
               await run(async () => {
                   await api('/admin/users', {
                       method: 'POST',
                       body: {
                           full_name: fd.get('full_name'),
                           email: fd.get('email'),
                           password: fd.get('password'),
                           role: fd.get('role'),
                           constituency: fd.get('constituency')
                       }
                   });
                   setShowCreate(false);
                   await refresh();
               });
           }
           return <>
               <PageHeading eyebrow="TEAM MANAGEMENT" title="Staff & Reviewers" 
                   desc="Manage admin and reviewer accounts with constituency assignments."
                   action={<Button onClick={() => setShowCreate(!showCreate)}><Plus size={17}/> Add staff member</Button>}/>
               {showCreate && <form className="panel create-form" onSubmit={createStaff}>
                   <h3>New staff account</h3>
                   <div className="form-grid">
                       <Field label="Full name"><input name="full_name" required/></Field>
                       <Field label="Email"><input name="email" type="email" required/></Field>
                       <Field label="Password"><input name="password" type="password" minLength="12" required placeholder="Minimum 12 characters"/></Field>
                       <Field label="Role"><select name="role" required><option value="admin">Administrator</option><option value="reviewer">Reviewer</option></select></Field>
                       <Field label="Constituency"><select name="constituency"><option value="">No assignment</option>{constituencies.map(c => <option key={c} value={c}>{c}</option>)}</select></Field>
                   </div>
                   <div className="form-actions">
                       <Button type="submit" disabled={busy}>{busy ? 'Creating...' : 'Create account'}</Button>
                       <Button kind="ghost" type="button" onClick={() => setShowCreate(false)}>Cancel</Button>
                   </div>
               </form>}
               <div className="panel table-panel">
                   {staffList.length === 0 ? <Empty title="No staff accounts" desc="Create admin and reviewer accounts to manage bursary review."/> :
                   <table><thead><tr><th>Name</th><th>Email</th><th>Role</th><th>Constituency</th><th>Status</th></tr></thead>
                   <tbody>{staffList.map(s => <tr key={s.id}>
                       <td><b>{s.full_name}</b></td>
                       <td>{s.email}</td>
                       <td><Badge tone={s.role === 'admin' ? 'success' : 'info'}>{s.role}</Badge></td>
                       <td>{s.constituency ? <span className="badge" style={{fontSize:'.72rem'}}><MapPin size={11} style={{marginRight:'4px',verticalAlign:'middle'}}/>{s.constituency}</span> : <span className="muted" style={{fontSize:'.78rem'}}>—</span>}</td>
                       <td><Badge tone={s.active ? 'success' : 'danger'}>{s.active ? 'Active' : 'Disabled'}</Badge></td>
                   </tr>)}</tbody></table>}
               </div>
           </>;
       }
       ```
       Files: frontend/src/App.jsx
       Verify: Navigate to Team page, see staff list table and create form

## Integration Verification

- [ ] 17. End-to-end test: Create reviewer with constituency, verify scoped dashboard:
       - Login as admin at http://localhost:5173
       - Navigate to Team page, create reviewer: email=reviewer@test.com, password=TestReviewer123!, role=reviewer, constituency=County Education Fund
       - Logout, login as reviewer@test.com
       - Verify Dashboard shows "Your Constituency: County Education Fund" banner
       - Verify Applications page shows only County Education Fund applications
       - Verify dashboard stats reflect only County Education Fund applications
       Files: All modified files
       Verify: Manual browser testing

- [ ] 18. End-to-end test: Toggle bursary status and verify applicant view:
       - Login as admin
       - Navigate to Bursary programs page
       - Toggle "STEM Merit Bursary" to Closed
       - Logout, login as applicant (register new account if needed)
       - Navigate to bursaries list, verify STEM Merit Bursary does NOT appear
       - Login as admin again, toggle back to Open
       - Login as applicant, verify STEM Merit Bursary reappears
       Files: All modified files
       Verify: Manual browser testing with admin and applicant accounts
