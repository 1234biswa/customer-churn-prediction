import streamlit as st

def apply_custom_css():
    """Injects modern SaaS-style custom CSS into Streamlit UI."""
    st.markdown("""
        <style>
        /* Modern Font & Color System */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        /* Main Container Padding */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }
        
        /* Metric Card Styling */
        .metric-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.01) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1.25rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
            text-align: center;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .metric-card:hover {
            transform: translateY(-4px);
            border-color: #3b82f6;
        }
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #3b82f6;
            margin-bottom: 0.25rem;
        }
        .metric-label {
            font-size: 0.875rem;
            color: #9ca3af;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* Risk Badges */
        .badge-low {
            background-color: #064e3b;
            color: #34d399;
            padding: 0.4rem 1rem;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 0.9rem;
            display: inline-block;
            border: 1px solid #059669;
        }
        .badge-medium {
            background-color: #78350f;
            color: #fbbf24;
            padding: 0.4rem 1rem;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 0.9rem;
            display: inline-block;
            border: 1px solid #d97706;
        }
        .badge-high {
            background-color: #7f1d1d;
            color: #f87171;
            padding: 0.4rem 1rem;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 0.9rem;
            display: inline-block;
            border: 1px solid #dc2626;
        }

        /* Hero Container */
        .hero-container {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid #334155;
            border-radius: 16px;
            padding: 2.5rem;
            margin-bottom: 2rem;
            text-align: center;
        }
        .hero-title {
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(90deg, #60a5fa 0%, #a78bfa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }
        .hero-subtitle {
            font-size: 1.1rem;
            color: #94a3b8;
            max-width: 800px;
            margin: 0 auto 1.5rem auto;
            line-height: 1.6;
        }

        /* Form Subheaders */
        .form-section-header {
            font-size: 1.1rem;
            font-weight: 600;
            color: #60a5fa;
            border-bottom: 2px solid #1e293b;
            padding-bottom: 0.5rem;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
