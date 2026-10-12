# Populate All 290 Kenya Constituencies

## 📊 What This Does

Adds **all 290 constituencies** from **all 47 counties** in Kenya as bursary programs in your database.

## 🚀 How to Run

### Option 1: On Render (Production)

1. Go to Render Dashboard → **smartbursary-backend**
2. Click **"Shell"** tab
3. Run these commands:

```bash
python seed_constituencies.py
```

You'll see output like:
```
🇰🇪 Seeding all Kenya constituencies...
Total: 290 constituencies
Counties: 47

📍 Baringo County (6 constituencies)
   ✅ Baringo Central
   ✅ Baringo North
   ...

✅ SUCCESS!
Created: 290 new bursaries
Total in database: 294
```

### Option 2: Locally (Development)

```powershell
cd backend
python seed_constituencies.py
```

## 📋 What Gets Created

For **each constituency**, a bursary program is created with:

- **Name**: `{Constituency} CDF Bursary`
- **Description**: Details about the constituency and county
- **Eligibility**: Must be resident of that constituency
- **Amount**: KES 20,000 (standard)
- **Deadline**: March 31, 2027
- **Documents Required**:
  - National ID or Birth Certificate
  - Admission Letter or Student ID
  - Fee Structure
  - Parent/Guardian ID Copy
- **Status**: Active

## 🔍 Search & Filter Features

Once populated, users can:

1. **Search by constituency**: Type "Westlands" → Shows Westlands
2. **Search by county**: Type "Nairobi" → Shows all 17 Nairobi constituencies
3. **Autocomplete**: As you type, suggestions appear
4. **Filter dropdown**: Select county → See only those constituencies

## 📍 Complete List

### Counties & Their Constituencies

**Nairobi (17)**: Westlands, Kasarani, Embakasi Central, Embakasi East, Embakasi North, Embakasi South, Embakasi West, Dagoretti North, Dagoretti South, Kamukunji, Kibra, Lang'ata, Makadara, Mathare, Roysambu, Ruaraka, Starehe

**Mombasa (6)**: Changamwe, Jomvu, Kisauni, Likoni, Mvita, Nyali

**Kisumu (7)**: Kisumu Central, Kisumu East, Kisumu West, Muhoroni, Nyakach, Nyando, Seme

**Nakuru (11)**: Bahati, Gilgil, Kuresoi North, Kuresoi South, Molo, Naivasha, Nakuru Town East, Nakuru Town West, Njoro, Rongai, Subukia

**Kiambu (12)**: Gatundu North, Gatundu South, Githunguri, Juja, Kabete, Kiambaa, Kiambu Town, Kikuyu, Lari, Limuru, Ruiru, Thika Town

... and **42 more counties** with all their constituencies!

## 🧪 Testing

After seeding, test the search:

```bash
# Search constituencies
curl https://smartbursary-backend.onrender.com/api/constituencies?search=west

# Get all counties
curl https://smartbursary-backend.onrender.com/api/counties

# Get constituencies for specific county
curl https://smartbursary-backend.onrender.com/api/constituencies?county=Nairobi
```

## ⚠️ Important Notes

1. **Run only once** - Script checks for existing constituencies and skips them
2. **No duplicates** - Safe to run multiple times
3. **Editable** - You can edit constituencies later via admin panel
4. **Searchable** - All 290 are immediately searchable
5. **Filterable** - Users can filter by their home county

## 🎯 User Experience After Seeding

**For Applicants:**
1. Register → Select home county
2. Browse bursaries → Auto-filtered to home county constituencies
3. Apply → Only eligible constituencies shown
4. Constituency-based eligibility enforced

**For Admins:**
1. See all 290 constituencies
2. Filter by county for management
3. Edit specific constituency programs
4. Generate county-wide reports

## 📊 Statistics

- **Total Counties**: 47
- **Total Constituencies**: 290
- **Bursaries Created**: 290
- **Average per County**: 6.2 constituencies
- **Largest County**: Nairobi (17 constituencies)
- **Smallest Counties**: Isiolo, Lamu (2 constituencies each)

## 🔄 Update Existing Data

If you already have some constituencies and want to add the rest:

```bash
# Script automatically skips existing ones
python seed_constituencies.py
```

Output will show:
```
   ⏭️  Westlands - already exists
   ✅ Kasarani
   ✅ Embakasi Central
   ...
```

## ✅ Verification

After running, verify in database:

```sql
-- Count total bursaries
SELECT COUNT(*) FROM bursaries;  -- Should be 290+ 

-- List by county
SELECT constituency, name FROM bursaries WHERE constituency != '' ORDER BY constituency;

-- Check Nairobi
SELECT name FROM bursaries WHERE name LIKE '%Nairobi%';
```

## 🎉 Result

Your system now covers **ALL OF KENYA** - every constituency in all 47 counties! 🇰🇪

Students from anywhere in Kenya can:
- Find their constituency bursary
- Apply online
- Track their application
- Download award letters

**SmartBursary is now nationally ready!** 🚀
