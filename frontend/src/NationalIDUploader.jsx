import React, { useState } from 'react';
import { Upload, CheckCircle2, X, AlertCircle } from 'lucide-react';

export function NationalIDUploader({ onUpload, disabled }) {
  const [frontFile, setFrontFile] = useState(null);
  const [backFile, setBackFile] = useState(null);
  const [frontPreview, setFrontPreview] = useState(null);
  const [backPreview, setBackPreview] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');

  function handleFileSelect(side, event) {
    const file = event.target.files?.[0];
    if (!file) return;

    // Validate file type
    if (!file.type.match(/image\/(jpeg|jpg|png)/)) {
      setError(`${side} image must be JPG or PNG`);
      return;
    }

    // Validate file size (5MB)
    if (file.size > 5 * 1024 * 1024) {
      setError(`${side} image must be less than 5MB`);
      return;
    }

    setError('');

    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
      if (side === 'Front') {
        setFrontFile(file);
        setFrontPreview(e.target.result);
      } else {
        setBackFile(file);
        setBackPreview(e.target.result);
      }
    };
    reader.readAsDataURL(file);
  }

  function clearFile(side) {
    if (side === 'Front') {
      setFrontFile(null);
      setFrontPreview(null);
    } else {
      setBackFile(null);
      setBackPreview(null);
    }
    setError('');
  }

  async function handleUpload() {
    if (!frontFile || !backFile) {
      setError('Please select both front and back images');
      return;
    }

    setUploading(true);
    setError('');

    try {
      await onUpload(frontFile, backFile);
      // Clear files after successful upload
      setFrontFile(null);
      setBackFile(null);
      setFrontPreview(null);
      setBackPreview(null);
    } catch (err) {
      setError(err.message || 'Upload failed');
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="national-id-uploader">
      <style>{`
        .national-id-uploader {
          border: 1px solid var(--border);
          border-radius: 8px;
          padding: 16px;
          background: var(--bg-subtle);
        }
        .id-upload-header {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-bottom: 12px;
        }
        .id-upload-header h4 {
          margin: 0;
          font-size: 0.95rem;
        }
        .id-upload-instruction {
          font-size: 0.85rem;
          color: var(--mute);
          margin-bottom: 16px;
        }
        .id-upload-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 16px;
          margin-bottom: 16px;
        }
        .id-upload-side {
          border: 2px dashed var(--border);
          border-radius: 8px;
          padding: 16px;
          text-align: center;
          background: white;
          position: relative;
        }
        .id-upload-side.has-file {
          border-color: var(--green);
          border-style: solid;
        }
        .id-side-label {
          font-weight: 600;
          font-size: 0.9rem;
          margin-bottom: 8px;
          display: block;
        }
        .id-preview {
          width: 100%;
          max-height: 200px;
          object-fit: contain;
          border-radius: 4px;
          margin-bottom: 8px;
        }
        .id-file-input-label {
          display: inline-flex;
          align-items: center;
          gap: 8px;
          padding: 8px 16px;
          background: var(--green);
          color: white;
          border-radius: 6px;
          cursor: pointer;
          font-size: 0.85rem;
          transition: background 0.2s;
        }
        .id-file-input-label:hover {
          background: #0a5438;
        }
        .id-file-input-label input {
          display: none;
        }
        .id-clear-btn {
          position: absolute;
          top: 8px;
          right: 8px;
          background: #dc2626;
          color: white;
          border: none;
          border-radius: 50%;
          width: 28px;
          height: 28px;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          transition: background 0.2s;
        }
        .id-clear-btn:hover {
          background: #b91c1c;
        }
        .id-upload-actions {
          display: flex;
          gap: 12px;
          align-items: center;
        }
        .id-upload-btn {
          flex: 1;
          padding: 12px 24px;
          background: var(--green);
          color: white;
          border: none;
          border-radius: 6px;
          font-weight: 600;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 8px;
          transition: background 0.2s;
        }
        .id-upload-btn:hover:not(:disabled) {
          background: #0a5438;
        }
        .id-upload-btn:disabled {
          background: var(--mute);
          cursor: not-allowed;
        }
        .id-error {
          color: #dc2626;
          font-size: 0.85rem;
          padding: 8px 12px;
          background: #fee2e2;
          border-radius: 6px;
          display: flex;
          align-items: center;
          gap: 8px;
          margin-top: 12px;
        }
        .id-success-badge {
          color: var(--green);
          display: flex;
          align-items: center;
          gap: 4px;
          font-size: 0.85rem;
          font-weight: 600;
        }
        @media (max-width: 640px) {
          .id-upload-grid {
            grid-template-columns: 1fr;
          }
        }
      `}</style>

      <div className="id-upload-header">
        <Upload size={20} style={{ color: 'var(--green)' }} />
        <h4>Upload National ID (Front & Back)</h4>
      </div>

      <p className="id-upload-instruction">
        Upload clear photos of both sides of your National ID. They will be automatically combined into a single PDF document.
      </p>

      <div className="id-upload-grid">
        <div className={`id-upload-side ${frontFile ? 'has-file' : ''}`}>
          {frontFile && (
            <button
              type="button"
              className="id-clear-btn"
              onClick={() => clearFile('Front')}
              title="Remove"
            >
              <X size={16} />
            </button>
          )}
          <span className="id-side-label">Front Side</span>
          {frontPreview && (
            <>
              <img src={frontPreview} alt="Front of ID" className="id-preview" />
              <div className="id-success-badge">
                <CheckCircle2 size={14} />
                Selected
              </div>
            </>
          )}
          {!frontPreview && (
            <label className="id-file-input-label">
              <Upload size={16} />
              Select Front
              <input
                type="file"
                accept="image/jpeg,image/jpg,image/png"
                onChange={(e) => handleFileSelect('Front', e)}
                disabled={disabled || uploading}
              />
            </label>
          )}
        </div>

        <div className={`id-upload-side ${backFile ? 'has-file' : ''}`}>
          {backFile && (
            <button
              type="button"
              className="id-clear-btn"
              onClick={() => clearFile('Back')}
              title="Remove"
            >
              <X size={16} />
            </button>
          )}
          <span className="id-side-label">Back Side</span>
          {backPreview && (
            <>
              <img src={backPreview} alt="Back of ID" className="id-preview" />
              <div className="id-success-badge">
                <CheckCircle2 size={14} />
                Selected
              </div>
            </>
          )}
          {!backPreview && (
            <label className="id-file-input-label">
              <Upload size={16} />
              Select Back
              <input
                type="file"
                accept="image/jpeg,image/jpg,image/png"
                onChange={(e) => handleFileSelect('Back', e)}
                disabled={disabled || uploading}
              />
            </label>
          )}
        </div>
      </div>

      <div className="id-upload-actions">
        <button
          type="button"
          className="id-upload-btn"
          onClick={handleUpload}
          disabled={!frontFile || !backFile || uploading || disabled}
        >
          {uploading ? (
            <>Uploading & Converting...</>
          ) : (
            <>
              <Upload size={18} />
              Upload & Convert to PDF
            </>
          )}
        </button>
      </div>

      {error && (
        <div className="id-error">
          <AlertCircle size={16} />
          {error}
        </div>
      )}
    </div>
  );
}
