import React, { useState, useEffect } from 'react';
import { MapPin, ChevronDown } from 'lucide-react';
import { api } from './api';

/**
 * Cascading Location Selector
 * County → Sub-County → Ward → Constituency
 * All 47 counties, sub-counties, wards fully listed
 */
export function CascadingLocationSelector({ 
  county, 
  subCounty, 
  ward, 
  constituency,
  onCountyChange,
  onSubCountyChange,
  onWardChange,
  onConstituencyChange,
  required = false 
}) {
  const [counties, setCounties] = useState([]);
  const [subCounties, setSubCounties] = useState([]);
  const [wards, setWards] = useState([]);
  const [constituencies, setConstituencies] = useState([]);
  const [loading, setLoading] = useState(false);

  // Load all counties on mount
  useEffect(() => {
    loadCounties();
  }, []);

  // Load sub-counties when county changes
  useEffect(() => {
    if (county) {
      loadSubCounties(county);
    } else {
      setSubCounties([]);
      setWards([]);
      setConstituencies([]);
    }
  }, [county]);

  // Load wards when sub-county changes
  useEffect(() => {
    if (county && subCounty) {
      loadWards(county, subCounty);
    } else {
      setWards([]);
    }
  }, [county, subCounty]);

  // Load constituencies when county changes (or sub-county)
  useEffect(() => {
    if (county) {
      loadConstituencies(county, subCounty);
    } else {
      setConstituencies([]);
    }
  }, [county, subCounty]);

  async function loadCounties() {
    try {
      setLoading(true);
      const data = await api('/counties');
      setCounties(data.counties || []);
    } catch (error) {
      console.error('Failed to load counties:', error);
    } finally {
      setLoading(false);
    }
  }

  async function loadSubCounties(countyName) {
    try {
      setLoading(true);
      const data = await api(`/locations/sub-counties?county=${encodeURIComponent(countyName)}`);
      setSubCounties(data.sub_counties || []);
    } catch (error) {
      console.error('Failed to load sub-counties:', error);
      setSubCounties([]);
    } finally {
      setLoading(false);
    }
  }

  async function loadWards(countyName, subCountyName) {
    try {
      setLoading(true);
      const data = await api(`/locations/wards?county=${encodeURIComponent(countyName)}&sub_county=${encodeURIComponent(subCountyName)}`);
      setWards(data.wards || []);
    } catch (error) {
      console.error('Failed to load wards:', error);
      setWards([]);
    } finally {
      setLoading(false);
    }
  }

  async function loadConstituencies(countyName, subCountyName = null) {
    try {
      setLoading(true);
      let url = `/locations/constituencies?county=${encodeURIComponent(countyName)}`;
      if (subCountyName) {
        url += `&sub_county=${encodeURIComponent(subCountyName)}`;
      }
      const data = await api(url);
      setConstituencies(data.constituencies || []);
    } catch (error) {
      console.error('Failed to load constituencies:', error);
      setConstituencies([]);
    } finally {
      setLoading(false);
    }
  }

  function handleCountyChange(e) {
    const value = e.target.value;
    onCountyChange(value);
    // Reset dependent fields
    onSubCountyChange('');
    onWardChange('');
    onConstituencyChange('');
  }

  function handleSubCountyChange(e) {
    const value = e.target.value;
    onSubCountyChange(value);
    // Reset dependent fields
    onWardChange('');
    if (!value) {
      onConstituencyChange('');
    }
  }

  function handleWardChange(e) {
    const value = e.target.value;
    onWardChange(value);
  }

  function handleConstituencyChange(e) {
    const value = e.target.value;
    onConstituencyChange(value);
  }

  return (
    <div className="cascading-location-selector">
      <style>{`
        .cascading-location-selector {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 16px;
        }
        .location-field {
          position: relative;
        }
        .location-field label {
          display: block;
          font-weight: 600;
          font-size: 0.9rem;
          margin-bottom: 6px;
          color: var(--text);
        }
        .location-field label .required {
          color: #dc2626;
          margin-left: 2px;
        }
        .location-select-wrapper {
          position: relative;
        }
        .location-select-wrapper select {
          width: 100%;
          padding: 10px 36px 10px 12px;
          border: 1px solid var(--border);
          border-radius: 6px;
          font-size: 0.95rem;
          background: white;
          appearance: none;
          cursor: pointer;
          transition: border-color 0.2s;
        }
        .location-select-wrapper select:focus {
          outline: none;
          border-color: var(--green);
          box-shadow: 0 0 0 3px rgba(16, 142, 89, 0.1);
        }
        .location-select-wrapper select:disabled {
          background: var(--bg-subtle);
          cursor: not-allowed;
          color: var(--mute);
        }
        .location-select-wrapper .select-icon {
          position: absolute;
          right: 12px;
          top: 50%;
          transform: translateY(-50%);
          pointer-events: none;
          color: var(--mute);
        }
        .location-select-wrapper .map-icon {
          position: absolute;
          left: 12px;
          top: 50%;
          transform: translateY(-50%);
          pointer-events: none;
          color: var(--green);
        }
        .location-select-wrapper.has-icon select {
          padding-left: 40px;
        }
        .location-help-text {
          font-size: 0.85rem;
          color: var(--mute);
          margin-top: 4px;
        }
        .location-loading {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 0.85rem;
          color: var(--mute);
          margin-top: 4px;
        }
        .spinner {
          width: 14px;
          height: 14px;
          border: 2px solid var(--border);
          border-top-color: var(--green);
          border-radius: 50%;
          animation: spin 0.8s linear infinite;
        }
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
        @media (max-width: 640px) {
          .cascading-location-selector {
            grid-template-columns: 1fr;
          }
        }
      `}</style>

      {/* County */}
      <div className="location-field">
        <label>
          County
          {required && <span className="required">*</span>}
        </label>
        <div className="location-select-wrapper has-icon">
          <MapPin size={16} className="map-icon" />
          <select 
            value={county} 
            onChange={handleCountyChange}
            required={required}
            disabled={loading || counties.length === 0}
          >
            <option value="">Select county...</option>
            {counties.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
          <ChevronDown size={16} className="select-icon" />
        </div>
        {loading && counties.length === 0 && (
          <div className="location-loading">
            <div className="spinner"></div>
            Loading counties...
          </div>
        )}
        {!loading && counties.length > 0 && (
          <div className="location-help-text">Select from 47 counties</div>
        )}
      </div>

      {/* Sub-County */}
      <div className="location-field">
        <label>
          Sub-County
          {required && <span className="required">*</span>}
        </label>
        <div className="location-select-wrapper">
          <select 
            value={subCounty} 
            onChange={handleSubCountyChange}
            required={required}
            disabled={!county || loading || subCounties.length === 0}
          >
            <option value="">Select sub-county...</option>
            {subCounties.map((sc) => (
              <option key={sc} value={sc}>{sc}</option>
            ))}
          </select>
          <ChevronDown size={16} className="select-icon" />
        </div>
        {loading && county && (
          <div className="location-loading">
            <div className="spinner"></div>
            Loading sub-counties...
          </div>
        )}
        {!county && (
          <div className="location-help-text">Select county first</div>
        )}
      </div>

      {/* Ward */}
      <div className="location-field">
        <label>
          Ward
          {required && <span className="required">*</span>}
        </label>
        <div className="location-select-wrapper">
          <select 
            value={ward} 
            onChange={handleWardChange}
            required={required}
            disabled={!subCounty || loading || wards.length === 0}
          >
            <option value="">Select ward...</option>
            {wards.map((w) => (
              <option key={w} value={w}>{w}</option>
            ))}
          </select>
          <ChevronDown size={16} className="select-icon" />
        </div>
        {loading && subCounty && (
          <div className="location-loading">
            <div className="spinner"></div>
            Loading wards...
          </div>
        )}
        {!subCounty && (
          <div className="location-help-text">Select sub-county first</div>
        )}
      </div>

      {/* Constituency */}
      <div className="location-field">
        <label>
          Constituency
          {required && <span className="required">*</span>}
        </label>
        <div className="location-select-wrapper">
          <select 
            value={constituency} 
            onChange={handleConstituencyChange}
            required={required}
            disabled={!county || loading || constituencies.length === 0}
          >
            <option value="">Select constituency...</option>
            {constituencies.map((const_name) => (
              <option key={const_name} value={const_name}>{const_name}</option>
            ))}
          </select>
          <ChevronDown size={16} className="select-icon" />
        </div>
        {loading && county && (
          <div className="location-loading">
            <div className="spinner"></div>
            Loading constituencies...
          </div>
        )}
        {!county && (
          <div className="location-help-text">Bursary eligibility area</div>
        )}
      </div>
    </div>
  );
}
