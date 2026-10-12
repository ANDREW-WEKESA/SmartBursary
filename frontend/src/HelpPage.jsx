import React, { useState } from 'react';
import { HelpCircle, MessageCircle, Mail, Phone, Book, Search, ChevronDown, ChevronUp } from 'lucide-react';

function FAQItem({ question, answer }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div style={{
      border: '1px solid var(--border)',
      borderRadius: '8px',
      marginBottom: '12px',
      overflow: 'hidden'
    }}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          width: '100%',
          padding: '16px',
          border: 'none',
          background: isOpen ? 'var(--bg-subtle)' : 'white',
          textAlign: 'left',
          cursor: 'pointer',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          fontSize: '0.95rem',
          fontWeight: '600'
        }}
      >
        <span>{question}</span>
        {isOpen ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
      </button>
      {isOpen && (
        <div style={{
          padding: '16px',
          borderTop: '1px solid var(--border)',
          fontSize: '0.9rem',
          lineHeight: '1.6',
          color: 'var(--text)'
        }}>
          {answer}
        </div>
      )}
    </div>
  );
}

export function HelpPage() {
  const [searchQuery, setSearchQuery] = useState('');

  const faqs = [
    {
      category: "Getting Started",
      questions: [
        {
          q: "How do I create an account?",
          a: "Click 'Create an account' on the login page. Fill in your details, verify your email with the OTP code sent to you, then complete your profile before applying."
        },
        {
          q: "What documents do I need to apply?",
          a: "You'll need: National ID or Birth Certificate, Admission Letter or Student ID, Fee Structure, and Parent/Guardian ID. Upload these in your profile before applying."
        },
        {
          q: "Which bursary can I apply for?",
          a: "You can only apply for bursaries in your home constituency. When browsing bursaries, only those matching your constituency will be available."
        }
      ]
    },
    {
      category: "Application Process",
      questions: [
        {
          q: "How do I track my application?",
          a: "Go to 'My Applications' to see all your submissions. Each application has a status (Submitted, Under Review, Approved, etc.). You'll also receive email and SMS notifications when status changes."
        },
        {
          q: "Can I apply for multiple bursaries?",
          a: "Yes, you can apply for multiple bursaries if you're eligible. Each application is reviewed separately."
        },
        {
          q: "What happens after I submit my application?",
          a: "Your application goes through several stages: Submitted → Under Review → Verification → Committee Review → Approved/Rejected. You'll be notified at each stage."
        },
        {
          q: "How long does the review process take?",
          a: "Review times vary by constituency and application volume. Typically 2-4 weeks. Check your dashboard for real-time status updates."
        }
      ]
    },
    {
      category: "After Approval",
      questions: [
        {
          q: "What do I do if my application is approved?",
          a: "Download your award letter from the application details page. Print it and submit to your school/college with other enrollment documents."
        },
        {
          q: "How do I download my award letter?",
          a: "Go to 'My Applications', click on an approved application, and click the 'Download Award Letter' button. The PDF is ready to print."
        },
        {
          q: "When will I receive the bursary funds?",
          a: "Disbursement timelines are managed by the CDF office. Your award letter includes instructions for your institution to claim the funds."
        }
      ]
    },
    {
      category: "Account & Profile",
      questions: [
        {
          q: "I forgot my password, what should I do?",
          a: "Click 'Forgot password?' on the login page. Enter your email, receive an OTP code, and set a new password."
        },
        {
          q: "How do I update my profile?",
          a: "Go to 'My Profile' from the menu. Update any field and click 'Save Changes'. Keep your documents up-to-date."
        },
        {
          q: "Why can't I apply for bursaries?",
          a: "You must complete your profile first, including uploading required documents (National ID, Student ID, Admission Letter). Check 'My Profile' to see what's missing."
        }
      ]
    },
    {
      category: "Technical Issues",
      questions: [
        {
          q: "My email verification code isn't working",
          a: "Make sure you entered the code correctly. Codes expire after 10 minutes. If expired, request a new code."
        },
        {
          q: "I'm not receiving emails",
          a: "Check your spam/junk folder. Add support@smartbursary.com to your contacts. If still not receiving, contact support."
        },
        {
          q: "How do I contact technical support?",
          a: "Email: support@smartbursary.com | Phone: +254 700 000 000 | We respond within 24 hours."
        }
      ]
    }
  ];

  const filteredFAQs = faqs.map(category => ({
    ...category,
    questions: category.questions.filter(item =>
      item.q.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.a.toLowerCase().includes(searchQuery.toLowerCase())
    )
  })).filter(category => category.questions.length > 0);

  return (
    <div>
      {/* Header */}
      <div style={{
        background: 'linear-gradient(135deg, var(--green) 0%, #0a5438 100%)',
        padding: '48px 24px',
        borderRadius: '12px',
        marginBottom: '32px',
        color: 'white',
        textAlign: 'center'
      }}>
        <div style={{ fontSize: '48px', marginBottom: '16px' }}>
          <HelpCircle size={48} />
        </div>
        <h1 style={{ fontSize: '2rem', marginBottom: '12px' }}>How can we help you?</h1>
        <p style={{ fontSize: '1.1rem', opacity: 0.9 }}>
          Find answers to common questions or contact our support team
        </p>
      </div>

      {/* Search */}
      <div className="panel" style={{ marginBottom: '32px' }}>
        <div style={{ position: 'relative' }}>
          <Search size={20} style={{
            position: 'absolute',
            left: '16px',
            top: '50%',
            transform: 'translateY(-50%)',
            color: 'var(--mute)'
          }} />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search for help... e.g. 'how to apply'"
            style={{
              width: '100%',
              padding: '16px 16px 16px 48px',
              border: '1px solid var(--border)',
              borderRadius: '8px',
              fontSize: '1rem'
            }}
          />
        </div>
      </div>

      {/* Quick Contact */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
        gap: '16px',
        marginBottom: '32px'
      }}>
        <div className="panel" style={{ textAlign: 'center', padding: '24px' }}>
          <Mail size={32} style={{ color: 'var(--green)', marginBottom: '12px' }} />
          <h3 style={{ marginBottom: '8px' }}>Email Support</h3>
          <p style={{ fontSize: '0.9rem', color: 'var(--mute)', marginBottom: '12px' }}>
            We respond within 24 hours
          </p>
          <a href="mailto:support@smartbursary.com" style={{ color: 'var(--green)', fontWeight: '600' }}>
            support@smartbursary.com
          </a>
        </div>

        <div className="panel" style={{ textAlign: 'center', padding: '24px' }}>
          <Phone size={32} style={{ color: 'var(--green)', marginBottom: '12px' }} />
          <h3 style={{ marginBottom: '8px' }}>Phone Support</h3>
          <p style={{ fontSize: '0.9rem', color: 'var(--mute)', marginBottom: '12px' }}>
            Mon-Fri, 8am-5pm EAT
          </p>
          <a href="tel:+254700000000" style={{ color: 'var(--green)', fontWeight: '600' }}>
            +254 700 000 000
          </a>
        </div>

        <div className="panel" style={{ textAlign: 'center', padding: '24px' }}>
          <MessageCircle size={32} style={{ color: 'var(--green)', marginBottom: '12px' }} />
          <h3 style={{ marginBottom: '8px' }}>CDF Office</h3>
          <p style={{ fontSize: '0.9rem', color: 'var(--mute)', marginBottom: '12px' }}>
            Visit your constituency office
          </p>
          <span style={{ color: 'var(--green)', fontWeight: '600' }}>
            Find your local office
          </span>
        </div>
      </div>

      {/* FAQs */}
      <div className="panel">
        <div style={{ marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '12px' }}>
          <Book size={24} style={{ color: 'var(--green)' }} />
          <h2 style={{ margin: 0 }}>Frequently Asked Questions</h2>
        </div>

        {filteredFAQs.length === 0 && searchQuery && (
          <div style={{
            textAlign: 'center',
            padding: '48px 24px',
            color: 'var(--mute)'
          }}>
            <HelpCircle size={48} style={{ marginBottom: '16px', opacity: 0.5 }} />
            <p>No results found for "{searchQuery}"</p>
            <p style={{ fontSize: '0.9rem' }}>Try a different search term or contact support</p>
          </div>
        )}

        {filteredFAQs.map((category, idx) => (
          <div key={idx} style={{ marginBottom: '32px' }}>
            <h3 style={{
              fontSize: '1.1rem',
              marginBottom: '16px',
              color: 'var(--green)',
              paddingBottom: '8px',
              borderBottom: '2px solid var(--border)'
            }}>
              {category.category}
            </h3>
            {category.questions.map((item, qIdx) => (
              <FAQItem key={qIdx} question={item.q} answer={item.a} />
            ))}
          </div>
        ))}
      </div>

      {/* Still need help */}
      <div className="panel" style={{
        marginTop: '32px',
        background: 'var(--bg-subtle)',
        textAlign: 'center',
        padding: '32px'
      }}>
        <h3 style={{ marginBottom: '12px' }}>Still need help?</h3>
        <p style={{ color: 'var(--mute)', marginBottom: '20px' }}>
          Our support team is here to assist you
        </p>
        <a
          href="mailto:support@smartbursary.com"
          className="btn primary"
          style={{ display: 'inline-block', textDecoration: 'none' }}
        >
          <Mail size={17} /> Contact Support
        </a>
      </div>
    </div>
  );
}
