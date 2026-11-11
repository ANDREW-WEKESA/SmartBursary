import React, { useState } from 'react';
import { HelpCircle, MessageCircle, Mail, Phone, Book, Search, ChevronDown, ChevronUp, MapPin } from 'lucide-react';

function FAQItem({ question, answer }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div style={{
      border: '2px solid',
      borderColor: isOpen ? 'var(--green)' : 'var(--border)',
      borderRadius: '12px',
      marginBottom: '12px',
      overflow: 'hidden',
      transition: 'all 0.3s ease',
      boxShadow: isOpen ? '0 4px 12px rgba(0, 128, 0, 0.1)' : 'none'
    }}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          width: '100%',
          padding: '18px 20px',
          border: 'none',
          background: isOpen ? 'linear-gradient(135deg, #e8f5e9 0%, #f1f8f4 100%)' : 'white',
          textAlign: 'left',
          cursor: 'pointer',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          fontSize: '1rem',
          fontWeight: '600',
          color: isOpen ? 'var(--green)' : 'var(--text)',
          transition: 'all 0.2s ease'
        }}
        onMouseEnter={(e) => {
          if (!isOpen) e.currentTarget.style.background = '#f8f9fa';
        }}
        onMouseLeave={(e) => {
          if (!isOpen) e.currentTarget.style.background = 'white';
        }}
      >
        <span>{question}</span>
        <div style={{
          background: isOpen ? 'var(--green)' : 'var(--bg-subtle)',
          borderRadius: '50%',
          width: '28px',
          height: '28px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          transition: 'all 0.3s ease',
          color: isOpen ? 'white' : 'var(--text)'
        }}>
          {isOpen ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
        </div>
      </button>
      {isOpen && (
        <div style={{
          padding: '20px 24px',
          borderTop: '1px solid #e0e0e0',
          fontSize: '0.95rem',
          lineHeight: '1.8',
          color: '#424242',
          background: 'white',
          animation: 'slideDown 0.3s ease'
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
        background: 'linear-gradient(135deg, #1b5e20 0%, #2e7d32 50%, #388e3c 100%)',
        padding: '60px 24px',
        borderRadius: '16px',
        marginBottom: '40px',
        color: 'white',
        textAlign: 'center',
        boxShadow: '0 10px 30px rgba(0, 0, 0, 0.2)',
        position: 'relative',
        overflow: 'hidden'
      }}>
        <div style={{
          position: 'absolute',
          top: '-50px',
          right: '-50px',
          width: '200px',
          height: '200px',
          background: 'rgba(255, 255, 255, 0.1)',
          borderRadius: '50%'
        }} />
        <div style={{
          position: 'absolute',
          bottom: '-30px',
          left: '-30px',
          width: '150px',
          height: '150px',
          background: 'rgba(255, 255, 255, 0.1)',
          borderRadius: '50%'
        }} />
        <div style={{
          position: 'relative',
          zIndex: 1
        }}>
          <div style={{
            fontSize: '48px',
            marginBottom: '20px',
            display: 'inline-flex',
            padding: '20px',
            background: 'rgba(255, 255, 255, 0.15)',
            borderRadius: '50%',
            backdropFilter: 'blur(10px)'
          }}>
            <HelpCircle size={48} strokeWidth={2} />
          </div>
          <h1 style={{
            fontSize: '2.5rem',
            marginBottom: '16px',
            fontWeight: '700',
            textShadow: '0 2px 4px rgba(0,0,0,0.2)'
          }}>
            How can we help you?
          </h1>
          <p style={{
            fontSize: '1.15rem',
            opacity: 0.95,
            maxWidth: '600px',
            margin: '0 auto'
          }}>
            Find answers to common questions or contact our support team
          </p>
        </div>
      </div>

      {/* Search */}
      <div className="panel" style={{
        marginBottom: '40px',
        boxShadow: '0 4px 15px rgba(0, 0, 0, 0.08)',
        border: '2px solid var(--border)'
      }}>
        <div style={{ position: 'relative' }}>
          <Search size={22} style={{
            position: 'absolute',
            left: '20px',
            top: '50%',
            transform: 'translateY(-50%)',
            color: 'var(--green)'
          }} />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search for help... e.g. 'how to apply'"
            style={{
              width: '100%',
              padding: '20px 20px 20px 56px',
              border: 'none',
              borderRadius: '8px',
              fontSize: '1.05rem',
              outline: 'none',
              transition: 'all 0.2s ease'
            }}
            onFocus={(e) => {
              e.target.parentElement.parentElement.style.borderColor = 'var(--green)';
              e.target.parentElement.parentElement.style.boxShadow = '0 4px 20px rgba(0, 128, 0, 0.15)';
            }}
            onBlur={(e) => {
              e.target.parentElement.parentElement.style.borderColor = 'var(--border)';
              e.target.parentElement.parentElement.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.08)';
            }}
          />
        </div>
      </div>

      {/* Quick Contact */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
        gap: '20px',
        marginBottom: '40px'
      }}>
        <div className="panel" style={{
          textAlign: 'center',
          padding: '32px 24px',
          background: 'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)',
          border: '2px solid var(--border)',
          transition: 'all 0.3s ease',
          cursor: 'pointer'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'translateY(-5px)';
          e.currentTarget.style.boxShadow = '0 8px 25px rgba(0, 128, 0, 0.15)';
          e.currentTarget.style.borderColor = 'var(--green)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'translateY(0)';
          e.currentTarget.style.boxShadow = 'none';
          e.currentTarget.style.borderColor = 'var(--border)';
        }}>
          <div style={{
            background: 'linear-gradient(135deg, var(--green) 0%, #2e7d32 100%)',
            width: '64px',
            height: '64px',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 16px',
            boxShadow: '0 4px 12px rgba(0, 128, 0, 0.3)'
          }}>
            <Mail size={32} style={{ color: 'white' }} />
          </div>
          <h3 style={{ marginBottom: '10px', fontSize: '1.2rem', color: 'var(--green)' }}>Email Support</h3>
          <p style={{ fontSize: '0.9rem', color: 'var(--mute)', marginBottom: '16px' }}>
            We respond within 24 hours
          </p>
          <a href="mailto:support@smartbursary.com" style={{
            color: 'var(--green)',
            fontWeight: '700',
            fontSize: '1rem',
            textDecoration: 'none'
          }}>
            support@smartbursary.com
          </a>
        </div>

        <div className="panel" style={{
          textAlign: 'center',
          padding: '32px 24px',
          background: 'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)',
          border: '2px solid var(--border)',
          transition: 'all 0.3s ease',
          cursor: 'pointer'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'translateY(-5px)';
          e.currentTarget.style.boxShadow = '0 8px 25px rgba(0, 128, 0, 0.15)';
          e.currentTarget.style.borderColor = 'var(--green)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'translateY(0)';
          e.currentTarget.style.boxShadow = 'none';
          e.currentTarget.style.borderColor = 'var(--border)';
        }}>
          <div style={{
            background: 'linear-gradient(135deg, var(--green) 0%, #2e7d32 100%)',
            width: '64px',
            height: '64px',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 16px',
            boxShadow: '0 4px 12px rgba(0, 128, 0, 0.3)'
          }}>
            <Phone size={32} style={{ color: 'white' }} />
          </div>
          <h3 style={{ marginBottom: '10px', fontSize: '1.2rem', color: 'var(--green)' }}>Phone Support</h3>
          <p style={{ fontSize: '0.9rem', color: 'var(--mute)', marginBottom: '16px' }}>
            Mon-Fri, 8am-5pm EAT
          </p>
          <a href="tel:+254700000000" style={{
            color: 'var(--green)',
            fontWeight: '700',
            fontSize: '1rem',
            textDecoration: 'none'
          }}>
            +254 700 000 000
          </a>
        </div>

        <div className="panel" style={{
          textAlign: 'center',
          padding: '32px 24px',
          background: 'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)',
          border: '2px solid var(--border)',
          transition: 'all 0.3s ease',
          cursor: 'pointer'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'translateY(-5px)';
          e.currentTarget.style.boxShadow = '0 8px 25px rgba(0, 128, 0, 0.15)';
          e.currentTarget.style.borderColor = 'var(--green)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'translateY(0)';
          e.currentTarget.style.boxShadow = 'none';
          e.currentTarget.style.borderColor = 'var(--border)';
        }}>
          <div style={{
            background: 'linear-gradient(135deg, var(--green) 0%, #2e7d32 100%)',
            width: '64px',
            height: '64px',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 16px',
            boxShadow: '0 4px 12px rgba(0, 128, 0, 0.3)'
          }}>
            <MapPin size={32} style={{ color: 'white' }} />
          </div>
          <h3 style={{ marginBottom: '10px', fontSize: '1.2rem', color: 'var(--green)' }}>CDF Office</h3>
          <p style={{ fontSize: '0.9rem', color: 'var(--mute)', marginBottom: '16px' }}>
            Visit your constituency office
          </p>
          <span style={{
            color: 'var(--green)',
            fontWeight: '700',
            fontSize: '1rem'
          }}>
            Find your local office
          </span>
        </div>
      </div>

      {/* FAQs */}
      <div className="panel" style={{
        boxShadow: '0 4px 15px rgba(0, 0, 0, 0.08)'
      }}>
        <div style={{
          marginBottom: '32px',
          display: 'flex',
          alignItems: 'center',
          gap: '12px',
          paddingBottom: '16px',
          borderBottom: '3px solid var(--green)'
        }}>
          <div style={{
            background: 'var(--green)',
            padding: '10px',
            borderRadius: '8px',
            display: 'flex'
          }}>
            <Book size={24} style={{ color: 'white' }} />
          </div>
          <h2 style={{ margin: 0, fontSize: '1.6rem', color: 'var(--green)' }}>Frequently Asked Questions</h2>
        </div>

        {filteredFAQs.length === 0 && searchQuery && (
          <div style={{
            textAlign: 'center',
            padding: '60px 24px',
            color: 'var(--mute)'
          }}>
            <div style={{
              background: 'var(--bg-subtle)',
              width: '80px',
              height: '80px',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto 20px'
            }}>
              <HelpCircle size={48} style={{ opacity: 0.4 }} />
            </div>
            <p style={{ fontSize: '1.1rem', fontWeight: '600', marginBottom: '8px' }}>
              No results found for "{searchQuery}"
            </p>
            <p style={{ fontSize: '0.95rem' }}>
              Try a different search term or contact support
            </p>
          </div>
        )}

        {filteredFAQs.map((category, idx) => (
          <div key={idx} style={{ marginBottom: '40px' }}>
            <h3 style={{
              fontSize: '1.25rem',
              marginBottom: '20px',
              color: 'var(--green)',
              paddingBottom: '12px',
              borderBottom: '2px solid #e0e0e0',
              fontWeight: '700',
              display: 'flex',
              alignItems: 'center',
              gap: '10px'
            }}>
              <div style={{
                width: '6px',
                height: '24px',
                background: 'var(--green)',
                borderRadius: '3px'
              }} />
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
        marginTop: '40px',
        background: 'linear-gradient(135deg, #e8f5e9 0%, #f1f8f4 100%)',
        textAlign: 'center',
        padding: '48px 32px',
        border: '2px solid var(--green)',
        position: 'relative',
        overflow: 'hidden'
      }}>
        <div style={{
          position: 'absolute',
          top: '-20px',
          right: '-20px',
          width: '120px',
          height: '120px',
          background: 'rgba(0, 128, 0, 0.08)',
          borderRadius: '50%'
        }} />
        <div style={{
          position: 'absolute',
          bottom: '-30px',
          left: '-30px',
          width: '150px',
          height: '150px',
          background: 'rgba(0, 128, 0, 0.08)',
          borderRadius: '50%'
        }} />
        <div style={{ position: 'relative', zIndex: 1 }}>
          <h3 style={{
            marginBottom: '12px',
            fontSize: '1.5rem',
            color: 'var(--green)'
          }}>
            Still need help?
          </h3>
          <p style={{
            color: '#424242',
            marginBottom: '24px',
            fontSize: '1.05rem'
          }}>
            Our support team is here to assist you
          </p>
          <a
            href="mailto:support@smartbursary.com"
            className="btn primary"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '8px',
              textDecoration: 'none',
              fontSize: '1.05rem',
              padding: '14px 32px',
              boxShadow: '0 4px 12px rgba(0, 128, 0, 0.3)',
              transition: 'all 0.3s ease'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = '0 6px 16px rgba(0, 128, 0, 0.4)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(0, 128, 0, 0.3)';
            }}
          >
            <Mail size={20} /> Contact Support
          </a>
        </div>
      </div>
    </div>
  );
}
