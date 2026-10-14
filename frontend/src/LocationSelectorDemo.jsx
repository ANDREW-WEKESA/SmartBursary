import React, { useState } from 'react';
import { SearchableLocationSelect } from './SearchableLocationSelect';
import { MapPin, CheckCircle2 } from 'lucide-react';

/**
 * Demo page showing how to use the SearchableLocationSelect component
 * This demonstrates the county and sub-county selection pattern
 */
export function LocationSelectorDemo() {
  const [county, setCounty] = useState('');
  const [subCounty, setSubCounty] = useState('');
  const [submitted, setSubmitted] = useState(false);

  function handleSubmit(e) {
    e.preventDefault();
    setSubmitted(true);
    console.log('Selected Location:', { county, subCounty });
  }

  function handleReset() {
    setCounty('');
    setSubCounty('');
    setSubmitted(false);
  }

  return (
    <div style={{ maxWidth: '700px', margin: '40px auto', padding: '0 20px' }}>
      <div style={{ 
        background: 'var(--green-soft)', 
        padding: '20px', 
        borderRadius: '12px',
        marginBottom: '30px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
          <MapPin size={24} color="var(--green)" />
          <h2 style={{ margin: 0 }}>Location Selector Demo</h2>
        </div>
        <p style={{ color: 'var(--mute)', margin: 0, fontSize: '0.9rem' }}>
          Select your county and sub-county using the searchable dropdowns below.
          Type to search or scroll through the options.
        </p>
      </div>

      <div className="panel">
        <h3>Select Your Location</h3>
        <p className="muted" style={{ fontSize: '0.85rem', marginBottom: '24px' }}>
          Choose your county first, then select the sub-county within that county.
        </p>

        <form onSubmit={handleSubmit}>
          <div style={{ display: 'grid', gap: '20px', marginBottom: '24px' }}>
            <SearchableLocationSelect
              label="County"
              value={county}
              onChange={(value) => {
                setCounty(value);
                // Reset sub-county when county changes
                if (subCounty) {
                  setSubCounty('');
                }
              }}
              placeholder="Select your county"
              required
            />

            <SearchableLocationSelect
              label="Sub-County"
              value={subCounty}
              onChange={setSubCounty}
              county={county}
              placeholder={county ? "Select your sub-county" : "Select a county first"}
              required
              disabled={!county}
            />
          </div>

          {submitted && (
            <div style={{
              background: '#effaf3',
              border: '1px solid #c4e1d0',
              borderRadius: '10px',
              padding: '16px',
              marginBottom: '20px',
              display: 'flex',
              alignItems: 'flex-start',
              gap: '10px'
            }}>
              <CheckCircle2 size={20} color="#0e6b4a" style={{ flexShrink: 0, marginTop: '2px' }} />
              <div>
                <strong style={{ display: 'block', marginBottom: '6px', color: '#155c3f' }}>
                  Location Submitted Successfully!
                </strong>
                <p style={{ margin: 0, fontSize: '0.85rem', color: '#2d7555' }}>
                  County: <strong>{county}</strong><br />
                  Sub-County: <strong>{subCounty}</strong>
                </p>
              </div>
            </div>
          )}

          <div style={{ display: 'flex', gap: '10px' }}>
            <button 
              type="submit" 
              className="btn primary"
              disabled={!county || !subCounty}
            >
              Submit Location
            </button>
            <button 
              type="button" 
              className="btn ghost"
              onClick={handleReset}
            >
              Reset
            </button>
          </div>
        </form>
      </div>

      <div className="panel" style={{ marginTop: '20px' }}>
        <h3>Features</h3>
        <ul style={{ 
          listStyle: 'none', 
          padding: 0, 
          display: 'grid', 
          gap: '12px',
          fontSize: '0.85rem' 
        }}>
          <li style={{ display: 'flex', gap: '10px' }}>
            <CheckCircle2 size={18} color="var(--green)" style={{ flexShrink: 0 }} />
            <span>Search and filter counties and sub-counties by typing</span>
          </li>
          <li style={{ display: 'flex', gap: '10px' }}>
            <CheckCircle2 size={18} color="var(--green)" style={{ flexShrink: 0 }} />
            <span>Keyboard navigation (Arrow keys, Enter, Escape)</span>
          </li>
          <li style={{ display: 'flex', gap: '10px' }}>
            <CheckCircle2 size={18} color="var(--green)" style={{ flexShrink: 0 }} />
            <span>Sub-counties load dynamically based on selected county</span>
          </li>
          <li style={{ display: 'flex', gap: '10px' }}>
            <CheckCircle2 size={18} color="var(--green)" style={{ flexShrink: 0 }} />
            <span>Clear button to quickly reset selection</span>
          </li>
          <li style={{ display: 'flex', gap: '10px' }}>
            <CheckCircle2 size={18} color="var(--green)" style={{ flexShrink: 0 }} />
            <span>Accessible and responsive design</span>
          </li>
          <li style={{ display: 'flex', gap: '10px' }}>
            <CheckCircle2 size={18} color="var(--green)" style={{ flexShrink: 0 }} />
            <span>Dark mode support</span>
          </li>
        </ul>
      </div>

      <div style={{
        marginTop: '30px',
        padding: '16px',
        background: '#f3f7f4',
        borderRadius: '10px',
        fontSize: '0.8rem',
        color: 'var(--mute)'
      }}>
        <strong>Data Source:</strong> Kenya administrative divisions data with 47 counties
        and their respective sub-counties. The data is loaded from the backend API.
      </div>
    </div>
  );
}
