import React, { useState, useEffect, useRef } from 'react';
import { ChevronDown, Search, X } from 'lucide-react';
import { api } from './api';

/**
 * SearchableLocationSelect - A dropdown component for selecting Kenya counties and sub-counties
 * Features:
 * - Search/filter functionality
 * - Hierarchical data (county -> sub-county)
 * - Keyboard navigation
 * - Accessible
 * 
 * Usage:
 * <SearchableLocationSelect
 *   label="County"
 *   value={county}
 *   onChange={(value) => setCounty(value)}
 *   placeholder="Select your county"
 * />
 * 
 * <SearchableLocationSelect
 *   label="Sub-County"
 *   value={subCounty}
 *   onChange={(value) => setSubCounty(value)}
 *   county={county}  // Pass county to load its sub-counties
 *   placeholder="Select your sub-county"
 * />
 */
export function SearchableLocationSelect({ 
  label, 
  value, 
  onChange, 
  county, // For sub-counties: which county to load sub-counties from
  placeholder = 'Select...',
  required = false,
  disabled = false 
}) {
  const [isOpen, setIsOpen] = useState(false);
  const [search, setSearch] = useState('');
  const [options, setOptions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(0);
  const containerRef = useRef(null);
  const searchInputRef = useRef(null);
  const listRef = useRef(null);

  // Determine if this is a county or sub-county selector
  const isSubCounty = !!county;

  // Load options when component mounts or county changes
  useEffect(() => {
    loadOptions();
  }, [county]);

  async function loadOptions() {
    if (isSubCounty && !county) {
      setOptions([]);
      return;
    }

    setLoading(true);
    try {
      const data = await api('/kenya-locations');
      
      if (isSubCounty) {
        // Find the selected county and get its sub-counties
        const countyData = data.counties.find(c => c.name === county);
        if (countyData) {
          setOptions(countyData.sub_counties.map(sc => ({ value: sc, label: sc })));
        } else {
          setOptions([]);
        }
      } else {
        // Load all counties
        setOptions(data.counties.map(c => ({ value: c.name, label: c.name, code: c.code })));
      }
    } catch (error) {
      console.error('Failed to load location data:', error);
      setOptions([]);
    } finally {
      setLoading(false);
    }
  }

  // Filter options based on search
  const filteredOptions = options.filter(opt =>
    opt.label.toLowerCase().includes(search.toLowerCase())
  );

  // Handle click outside to close dropdown
  useEffect(() => {
    function handleClickOutside(event) {
      if (containerRef.current && !containerRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
    }
  }, [isOpen]);

  // Focus search input when dropdown opens
  useEffect(() => {
    if (isOpen && searchInputRef.current) {
      searchInputRef.current.focus();
    }
  }, [isOpen]);

  // Reset highlighted index when search changes
  useEffect(() => {
    setHighlightedIndex(0);
    if (listRef.current) {
      listRef.current.scrollTop = 0;
    }
  }, [search]);

  function handleSelect(option) {
    onChange(option.value);
    setIsOpen(false);
    setSearch('');
  }

  function handleClear(e) {
    e.stopPropagation();
    onChange('');
    setSearch('');
  }

  function handleKeyDown(e) {
    if (!isOpen) {
      if (e.key === 'Enter' || e.key === ' ' || e.key === 'ArrowDown') {
        e.preventDefault();
        setIsOpen(true);
      }
      return;
    }

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setHighlightedIndex(prev => 
          prev < filteredOptions.length - 1 ? prev + 1 : prev
        );
        // Scroll into view
        if (listRef.current && listRef.current.children && listRef.current.children.length > 0) {
          const items = listRef.current.children;
          const nextIndex = Math.min(highlightedIndex + 1, items.length - 1);
          if (items[nextIndex]) {
            items[nextIndex].scrollIntoView({ block: 'nearest' });
          }
        }
        break;
      case 'ArrowUp':
        e.preventDefault();
        setHighlightedIndex(prev => prev > 0 ? prev - 1 : 0);
        // Scroll into view
        if (listRef.current && listRef.current.children && listRef.current.children.length > 0) {
          const items = listRef.current.children;
          const prevIndex = Math.max(highlightedIndex - 1, 0);
          if (items[prevIndex]) {
            items[prevIndex].scrollIntoView({ block: 'nearest' });
          }
        }
        break;
      case 'Enter':
        e.preventDefault();
        if (filteredOptions[highlightedIndex]) {
          handleSelect(filteredOptions[highlightedIndex]);
        }
        break;
      case 'Escape':
        e.preventDefault();
        setIsOpen(false);
        setSearch('');
        break;
      default:
        break;
    }
  }

  const displayValue = value || '';
  const showClear = value && !disabled;

  return (
    <label className="field">
      <span>
        {label}
        {required && <span style={{ color: 'var(--color-red)' }}> *</span>}
      </span>
      <div className="searchable-select" ref={containerRef}>
        <button
          type="button"
          className={`searchable-select-trigger ${isOpen ? 'open' : ''} ${disabled ? 'disabled' : ''}`}
          onClick={() => !disabled && setIsOpen(!isOpen)}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          aria-haspopup="listbox"
          aria-expanded={isOpen}
        >
          <span className={displayValue ? '' : 'placeholder'}>
            {displayValue || placeholder}
          </span>
          <div className="searchable-select-icons">
            {showClear && (
              <button
                type="button"
                className="searchable-select-clear"
                onClick={handleClear}
                aria-label="Clear selection"
              >
                <X size={14} />
              </button>
            )}
            <ChevronDown size={16} className={`searchable-select-chevron ${isOpen ? 'rotate' : ''}`} />
          </div>
        </button>

        {isOpen && (
          <div className="searchable-select-dropdown">
            <div className="searchable-select-search">
              <Search size={16} />
              <input
                ref={searchInputRef}
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder={`Search ${isSubCounty ? 'sub-counties' : 'counties'}...`}
                className="searchable-select-search-input"
              />
            </div>

            <ul 
              ref={listRef}
              className="searchable-select-list" 
              role="listbox"
            >
              {loading ? (
                <li className="searchable-select-loading">Loading...</li>
              ) : filteredOptions.length === 0 ? (
                <li className="searchable-select-empty">
                  {search ? `No results for "${search}"` : 
                   isSubCounty && !county ? 'Select a county first' : 
                   'No options available'}
                </li>
              ) : (
                filteredOptions.map((option, index) => (
                  <li
                    key={option.value}
                    className={`searchable-select-option ${
                      index === highlightedIndex ? 'highlighted' : ''
                    } ${value === option.value ? 'selected' : ''}`}
                    onClick={() => handleSelect(option)}
                    onMouseEnter={() => setHighlightedIndex(index)}
                    role="option"
                    aria-selected={value === option.value}
                  >
                    {option.label}
                    {option.code && <span className="option-code">#{option.code}</span>}
                  </li>
                ))
              )}
            </ul>
          </div>
        )}
      </div>
    </label>
  );
}
