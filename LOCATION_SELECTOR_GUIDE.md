# Kenya Location Selector - Integration Guide

## Overview

The SmartBursary application now includes a searchable location selector component for selecting Kenyan counties and sub-counties with accurate, verified data.

## Features

✅ **Searchable Dropdowns** - Type to filter counties and sub-counties  
✅ **Accurate Data** - 47 counties with correct administrative sub-counties (not constituencies)  
✅ **Hierarchical Selection** - Sub-counties load dynamically based on selected county  
✅ **Keyboard Navigation** - Full keyboard support (Arrow keys, Enter, Escape)  
✅ **Clear Button** - Quick reset of selections  
✅ **Accessible** - ARIA attributes and semantic HTML  
✅ **Dark Mode** - Automatic theme adaptation  
✅ **Mobile Responsive** - Works on all screen sizes

## Data Source

- **File**: `backend/kenya_locations.json`
- **47 Counties** with verified administrative sub-counties
- **API Endpoint**: `/api/kenya-locations`
- **Note**: Sub-counties are administrative divisions, NOT constituencies (e.g., Tongaren is correctly listed as a sub-county in Bungoma, not as a constituency)

## Quick Start

### 1. Import the Component

```jsx
import { SearchableLocationSelect } from './SearchableLocationSelect';
```

### 2. Add State Variables

```jsx
const [county, setCounty] = useState('');
const [subCounty, setSubCounty] = useState('');
```

### 3. Use in Your Form

```jsx
<SearchableLocationSelect
  label="County"
  value={county}
  onChange={(value) => {
    setCounty(value);
    // Reset sub-county when county changes
    if (subCounty) setSubCounty('');
  }}
  placeholder="Select your county"
  required
/>

<SearchableLocationSelect
  label="Sub-County"
  value={subCounty}
  onChange={setSubCounty}
  county={county}  // Pass county to load its sub-counties
  placeholder="Select your sub-county"
  required
  disabled={!county}  // Disable until county is selected
/>
```

## Props Reference

### SearchableLocationSelect Props

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `label` | string | Yes | - | Label displayed above the select |
| `value` | string | Yes | - | Currently selected value |
| `onChange` | function | Yes | - | Callback when selection changes |
| `county` | string | No | - | For sub-county selector: which county to load sub-counties from |
| `placeholder` | string | No | 'Select...' | Placeholder text |
| `required` | boolean | No | false | Whether field is required |
| `disabled` | boolean | No | false | Whether field is disabled |

## Integration Examples

### Example 1: Profile Form

```jsx
function ProfilePage() {
  const [county, setCounty] = useState('');
  const [subCounty, setSubCounty] = useState('');
  
  async function handleSubmit(e) {
    e.preventDefault();
    await api('/profile', {
      method: 'PATCH',
      body: { county, sub_county: subCounty }
    });
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <SearchableLocationSelect
        label="County of Residence"
        value={county}
        onChange={(val) => {
          setCounty(val);
          setSubCounty(''); // Clear sub-county on county change
        }}
        required
      />
      
      <SearchableLocationSelect
        label="Sub-County"
        value={subCounty}
        onChange={setSubCounty}
        county={county}
        disabled={!county}
        required
      />
      
      <button type="submit">Save Profile</button>
    </form>
  );
}
```

### Example 2: Application Form

```jsx
function ApplyPage() {
  const [county, setCounty] = useState('');
  const [subCounty, setSubCounty] = useState('');
  
  return (
    <form>
      <div className="form-grid">
        <SearchableLocationSelect
          label="County"
          value={county}
          onChange={setCounty}
          placeholder="Select your county"
          required
        />
        
        <SearchableLocationSelect
          label="Sub-County"
          value={subCounty}
          onChange={setSubCounty}
          county={county}
          placeholder={county ? "Select sub-county" : "Select county first"}
          disabled={!county}
          required
        />
      </div>
    </form>
  );
}
```

### Example 3: Filter/Search

```jsx
function BursariesPage() {
  const [filterCounty, setFilterCounty] = useState('');
  const [filterSubCounty, setFilterSubCounty] = useState('');
  
  return (
    <>
      <div className="toolbar">
        <SearchableLocationSelect
          label="Filter by County"
          value={filterCounty}
          onChange={(val) => {
            setFilterCounty(val);
            setFilterSubCounty('');
          }}
          placeholder="All counties"
        />
        
        {filterCounty && (
          <SearchableLocationSelect
            label="Filter by Sub-County"
            value={filterSubCounty}
            onChange={setFilterSubCounty}
            county={filterCounty}
            placeholder="All sub-counties"
          />
        )}
      </div>
    </>
  );
}
```

## Testing

A demo page is available to test the component:

**File**: `frontend/src/LocationSelectorDemo.jsx`

To view the demo:
1. Import and add to your App.jsx navigation
2. Navigate to the demo page
3. Test county and sub-county selection

## Backend API

The component fetches data from:

```
GET /api/kenya-locations
```

**Response:**
```json
{
  "_attribution": "Compiled from official Kenya government sources",
  "counties": [
    {
      "code": 1,
      "name": "Mombasa",
      "capital": "Mombasa City",
      "sub_counties": ["Changamwe", "Jomvu", "Kisauni", "Likoni", "Mvita", "Nyali"]
    },
    ...
  ]
}
```

## Data Accuracy Note

⚠️ **Important**: This dataset contains administrative sub-counties, NOT electoral constituencies.

- ✅ **Tongaren** is correctly listed as a sub-county in Bungoma County
- ✅ Sub-counties are administrative divisions headed by Deputy County Commissioners
- ❌ Do not confuse with constituencies (electoral divisions)

The data has been verified against official Kenya government sources (KNBS, County Governments).

## Styling

The component uses the existing SmartBursary design system:
- CSS classes prefixed with `.searchable-select-*`
- Respects the app's color variables
- Supports light and dark modes
- Mobile responsive

Custom styling can be added by targeting these classes in your CSS.

## Keyboard Shortcuts

- **Tab**: Navigate between fields
- **Space / Enter**: Open dropdown
- **Arrow Down/Up**: Navigate options
- **Enter**: Select highlighted option
- **Escape**: Close dropdown
- **Type**: Filter options

## Accessibility

- ARIA attributes for screen readers
- Keyboard navigation support
- Clear focus indicators
- Semantic HTML structure
- Descriptive labels and placeholders

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Troubleshooting

### Sub-counties not loading
- Ensure county is selected first
- Check that backend API is running
- Verify `county` prop is passed correctly

### Search not working
- Check that you're typing in the search input (not the trigger button)
- Verify search input is focused when dropdown opens

### Styling issues
- Ensure `styles.css` includes the searchable-select styles
- Check for CSS conflicts with existing styles
- Verify CSS variables are defined in `:root`

## Future Enhancements

Potential improvements:
- Add ward-level selection (Kenya has ~1,450 wards)
- Add constituency selection (290 constituencies)
- Caching of location data
- Offline support with localStorage
- Multi-select for filtering
- Location search across all levels

## Support

For issues or questions:
1. Check this guide first
2. Review the LocationSelectorDemo.jsx example
3. Inspect browser console for errors
4. Verify backend API is accessible

## License

Part of the SmartBursary application.
Location data compiled from official Kenya government sources (CC-BY-4.0 compatible).
