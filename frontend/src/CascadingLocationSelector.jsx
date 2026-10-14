import React, { useState, useEffect } from 'react';
import { MapPin, ChevronDown } from 'lucide-react';
import { api } from './api';

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

  useEffect(() => {
    loadCounties();
  }, []);

  useEffect(() => {
    if (county) {
      loadSubCounties(county);
      loadConstituencies(county, subCounty);
    } else {
      setSubCounties([]);
      setConstituencies([]);
    }
  }, [county]);

  useEffect(() => {
    if (county && subCounty) {
      loadWards(county, subCounty);
      loadConstituencies(county, subCounty);
    } else {
      setWards([]);
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
      const data = await api(`/locations/sub-counties?county=${encodeURIComponent(countyName)}`);
      setSubCounties(data.sub_counties || []);
    } catch (error) {
      console.error('Failed to load sub-counties:', error);
      setSubCounties([]);
    }
  }

  async function loadWards(countyName, subCountyName) {
    try {
      const data = await api(`/locations/wards?county=${encodeURIComponent(countyName)}&sub_county=${encodeURIComponent(subCountyName)}`);
      setWards(data.wards || []);
    } catch (error) {
      console.error('Failed to load wards:', error);
      setWards([]);
    }
  }

  async function loadConstituencies(countyName, subCountyName = null) {
    try {
      let url = `/locations/constituencies?county=${encodeURIComponent(countyName)}`;
      if (subCountyName) {
        url += `&sub_county=${encodeURIComponent(subCountyName)}`;
      }
      const data = await api(url);
      setConstituencies(data.constituencies || []);
    } catch (error) {
      console.error('Failed to load constituencies:', error);
      setConstituencies([]);
    }
  }

  return (
    <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:'16px'}}>
      <div>
        <label style={{display:'block',fontWeight:600,fontSize:'0.9rem',marginBottom:'6px'}}>
          County{required && <span style={{color:'#dc2626'}}>*</span>}
        </label>
        <select 
          value={county || ''} 
          onChange={(e) => {
            const val = e.target.value;
            if (val) {
              onCountyChange(val);
              onSubCountyChange('');
              onWardChange('');
              onConstituencyChange('');
            }
          }}
          required={required}
          style={{width:'100%',padding:'10px',border:'1px solid #ddd',borderRadius:'6px',fontSize:'0.95rem'}}
        >
          <option value="">Select county...</option>
          {counties.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
      </div>

      <div>
        <label style={{display:'block',fontWeight:600,fontSize:'0.9rem',marginBottom:'6px'}}>
          Sub-County{required && <span style={{color:'#dc2626'}}>*</span>}
        </label>
        <select 
          value={subCounty || ''} 
          onChange={(e) => {
            const val = e.target.value;
            onSubCountyChange(val);
            onWardChange('');
            if (!val) onConstituencyChange('');
          }}
          disabled={!county}
          required={required}
          style={{width:'100%',padding:'10px',border:'1px solid #ddd',borderRadius:'6px',fontSize:'0.95rem'}}
        >
          <option value="">Select sub-county...</option>
          {subCounties.map((sc) => (
            <option key={sc} value={sc}>{sc}</option>
          ))}
        </select>
      </div>

      <div>
        <label style={{display:'block',fontWeight:600,fontSize:'0.9rem',marginBottom:'6px'}}>
          Ward{required && <span style={{color:'#dc2626'}}>*</span>}
        </label>
        <select 
          value={ward || ''} 
          onChange={(e) => onWardChange(e.target.value)}
          disabled={!subCounty}
          required={required}
          style={{width:'100%',padding:'10px',border:'1px solid #ddd',borderRadius:'6px',fontSize:'0.95rem'}}
        >
          <option value="">Select ward...</option>
          {wards.map((w) => (
            <option key={w} value={w}>{w}</option>
          ))}
        </select>
      </div>

      <div>
        <label style={{display:'block',fontWeight:600,fontSize:'0.9rem',marginBottom:'6px'}}>
          Constituency{required && <span style={{color:'#dc2626'}}>*</span>}
        </label>
        <select 
          value={constituency || ''} 
          onChange={(e) => onConstituencyChange(e.target.value)}
          disabled={!county}
          required={required}
          style={{width:'100%',padding:'10px',border:'1px solid #ddd',borderRadius:'6px',fontSize:'0.95rem'}}
        >
          <option value="">Select constituency...</option>
          {constituencies.map((const_name) => (
            <option key={const_name} value={const_name}>{const_name}</option>
          ))}
        </select>
      </div>
    </div>
  );
}
