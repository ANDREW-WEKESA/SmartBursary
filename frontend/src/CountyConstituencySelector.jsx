import React, { useState, useEffect, useRef } from 'react';
import { Search, MapPin, X } from 'lucide-react';

/**
 * Autocomplete selector for County and Constituency
 * Searches all 290 constituencies across 47 counties
 */
export function CountySelector({ value, onChange, required }) {
  const [search, setSearch] = useState(value || '');
  const [counties, setCounties] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [loading, setLoading] = useState(false);
  const wrapperRef = useRef(null);

  // Load all counties on mount
  useEffect(() => {
    loadCounties();
  }, []);

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setShowDropdown(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  async function loadCounties() {
    try {
      setLoading(true);
      const response = await fetch(`${import.meta.env.VITE_API_BASE || 'http://localhost:8000'}/api/counties`);
      const data = await response.json();
      setCounties(data.counties || []);
    } catch (error) {
      console.error('Failed to load counties:', error);
    } finally {
      setLoading(false);
    }
  }

  function handleSelect(county) {
    setSearch(county);
    onChange(county);
    setShowDropdown(false);
  }

  function handleInputChange(e) {
    const val = e.target.value;
    setSearch(val);
    setShowDropdown(val.length > 0);
    onChange(val);
  }

  function clearSelection() {
    setSearch('');
    onChange('');
    setShowDropdown(false);
  }

  const filteredCounties = counties.filter(c =>
    c.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div ref={wrapperRef} style={{ position: 'relative' }}>
      <div style={{ position: 'relative' }}>
        <input
          type="text"
          value={search}
          onChange={handleInputChange}
          onFocus={() => setShowDropdown(true)}
          placeholder="e.g. Nairobi, Mombasa, Kisumu..."
          required={required}
          autoComplete="off"
          style={{ paddingRight: search ? '80px' : '40px' }}
        />
        <div style={{
          position: 'absolute',
          right: '10px',
          top: '50%',
          transform: 'translateY(-50%)',
          display: 'flex',
          gap: '8px',
          alignItems: 'center'
        }}>
          {search && (
            <button
              type="button"
              onClick={clearSelection}
              style={{
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                padding: '4px',
                display: 'flex',
                color: 'var(--mute)'
              }}
              title="Clear"
            >
              <X size={16} />
            </button>
          )}
          <MapPin size={16} style={{ color: 'var(--mute)' }} />
        </div>
      </div>

      {showDropdown && filteredCounties.length > 0 && (
        <div style={{
          position: 'absolute',
          top: '100%',
          left: 0,
          right: 0,
          backgroundColor: 'white',
          border: '1px solid var(--border)',
          borderRadius: '8px',
          marginTop: '4px',
          maxHeight: '300px',
          overflowY: 'auto',
          boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
          zIndex: 1000
        }}>
          {filteredCounties.map((county) => (
            <button
              key={county}
              type="button"
              onClick={() => handleSelect(county)}
              style={{
                width: '100%',
                padding: '12px 16px',
                border: 'none',
                background: 'none',
                textAlign: 'left',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                fontSize: '0.95rem'
              }}
              onMouseEnter={(e) => e.currentTarget.style.backgroundColor = 'var(--bg-subtle)'}
              onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
            >
              <MapPin size={16} style={{ color: 'var(--green)', flexShrink: 0 }} />
              <span style={{ fontWeight: '500' }}>{county}</span>
            </button>
          ))}
        </div>
      )}

      {showDropdown && search && filteredCounties.length === 0 && (
        <div style={{
          position: 'absolute',
          top: '100%',
          left: 0,
          right: 0,
          backgroundColor: 'white',
          border: '1px solid var(--border)',
          borderRadius: '8px',
          marginTop: '4px',
          padding: '16px',
          textAlign: 'center',
          color: 'var(--mute)',
          fontSize: '0.9rem',
          zIndex: 1000
        }}>
          No counties found matching "{search}"
        </div>
      )}
    </div>
  );
}

export function ConstituencySelector({ county, value, onChange, required }) {
  const [search, setSearch] = useState(value || '');
  const [constituencies, setConstituencies] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [loading, setLoading] = useState(false);
  const wrapperRef = useRef(null);

  // Load constituencies when county changes or on search
  useEffect(() => {
    if (search.length >= 2) {
      searchConstituencies();
    } else if (county) {
      loadConstituenciesByCounty();
    }
  }, [county, search]);

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setShowDropdown(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  async function searchConstituencies() {
    try {
      setLoading(true);
      const response = await fetch(
        `${import.meta.env.VITE_API_BASE || 'http://localhost:8000'}/api/constituencies?search=${encodeURIComponent(search)}`
      );
      const data = await response.json();
      setConstituencies(data.constituencies || []);
      setShowDropdown(true);
    } catch (error) {
      console.error('Failed to search constituencies:', error);
    } finally {
      setLoading(false);
    }
  }

  async function loadConstituenciesByCounty() {
    if (!county) return;
    try {
      setLoading(true);
      const response = await fetch(
        `${import.meta.env.VITE_API_BASE || 'http://localhost:8000'}/api/constituencies?county=${encodeURIComponent(county)}`
      );
      const data = await response.json();
      setConstituencies(data.constituencies || []);
    } catch (error) {
      console.error('Failed to load constituencies:', error);
    } finally {
      setLoading(false);
    }
  }

  function handleSelect(constituency) {
    const name = constituency.constituency || constituency;
    setSearch(name);
    onChange(name);
    setShowDropdown(false);
  }

  function handleInputChange(e) {
    const val = e.target.value;
    setSearch(val);
    onChange(val);
    if (val.length >= 2) {
      setShowDropdown(true);
    }
  }

  function clearSelection() {
    setSearch('');
    onChange('');
    setShowDropdown(false);
  }

  return (
    <div ref={wrapperRef} style={{ position: 'relative' }}>
      <div style={{ position: 'relative' }}>
        <input
          type="text"
          value={search}
          onChange={handleInputChange}
          onFocus={() => { if (constituencies.length > 0) setShowDropdown(true); }}
          placeholder="e.g. Westlands, Kasarani, Kisumu East..."
          required={required}
          autoComplete="off"
          style={{ paddingRight: search ? '80px' : '40px' }}
        />
        <div style={{
          position: 'absolute',
          right: '10px',
          top: '50%',
          transform: 'translateY(-50%)',
          display: 'flex',
          gap: '8px',
          alignItems: 'center'
        }}>
          {search && (
            <button
              type="button"
              onClick={clearSelection}
              style={{
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                padding: '4px',
                display: 'flex',
                color: 'var(--mute)'
              }}
              title="Clear"
            >
              <X size={16} />
            </button>
          )}
          {loading ? (
            <div style={{ width: '16px', height: '16px', borderRadius: '50%', border: '2px solid var(--border)', borderTopColor: 'var(--green)', animation: 'spin 1s linear infinite' }} />
          ) : (
            <Search size={16} style={{ color: 'var(--mute)' }} />
          )}
        </div>
      </div>

      {showDropdown && constituencies.length > 0 && (
        <div style={{
          position: 'absolute',
          top: '100%',
          left: 0,
          right: 0,
          backgroundColor: 'white',
          border: '1px solid var(--border)',
          borderRadius: '8px',
          marginTop: '4px',
          maxHeight: '300px',
          overflowY: 'auto',
          boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
          zIndex: 1000
        }}>
          {constituencies.map((item, idx) => {
            const constituencyName = item.constituency || item;
            const countyName = item.county || '';
            return (
              <button
                key={idx}
                type="button"
                onClick={() => handleSelect(item)}
                style={{
                  width: '100%',
                  padding: '12px 16px',
                  border: 'none',
                  background: 'none',
                  textAlign: 'left',
                  cursor: 'pointer',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '4px'
                }}
                onMouseEnter={(e) => e.currentTarget.style.backgroundColor = 'var(--bg-subtle)'}
                onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
              >
                <span style={{ fontWeight: '500', fontSize: '0.95rem' }}>{constituencyName}</span>
                {countyName && (
                  <span style={{ fontSize: '0.85rem', color: 'var(--mute)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <MapPin size={12} /> {countyName} County
                  </span>
                )}
              </button>
            );
          })}
        </div>
      )}

      {showDropdown && search.length >= 2 && constituencies.length === 0 && !loading && (
        <div style={{
          position: 'absolute',
          top: '100%',
          left: 0,
          right: 0,
          backgroundColor: 'white',
          border: '1px solid var(--border)',
          borderRadius: '8px',
          marginTop: '4px',
          padding: '16px',
          textAlign: 'center',
          color: 'var(--mute)',
          fontSize: '0.9rem',
          zIndex: 1000
        }}>
          No constituencies found matching "{search}"
        </div>
      )}
    </div>
  );
}
