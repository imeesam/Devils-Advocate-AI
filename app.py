import streamlit as st
import time
from agents import pro_agent, con_agent, judge_agent, reflection_agent
import os
import re

def clear_question():
    st.session_state["question_input"] = ""
    st.session_state.pop("history", None)

def fill_example(ex):
    st.session_state["question_input"] = ex

def is_valid_question(text: str) -> bool:
    text = text.strip().lower()

    # Too short
    if len(text) < 10:
        return False

    # Must contain at least one space (not a single word)
    if " " not in text:
        return False

    # Must contain a question mark OR decision keyword
    decision_keywords = [
        "should", "is it", "is this", "do we", "can we",
        "worth", "better", "viable", "good idea", "risk"
    ]

    if "?" not in text and not any(k in text for k in decision_keywords):
        return False

    # Reject obvious junk
    if re.fullmatch(r"[a-zA-Z]+", text) and len(text) < 15:
        return False

    return True

# Page config
st.set_page_config(
    page_title="Devil's Advocate AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .agent-box {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid #4CAF50;
    }
    .con-agent-box {
        border-left: 5px solid #F44336;
    }
    .verdict-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 7px;
        border-radius: 6px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">⚖️ Devil\'s Advocate AI</h1>', unsafe_allow_html=True)
st.markdown("### Multi-Agent Decision System • Powered by **Google Gemini**")
st.caption("Get balanced perspectives before making important decisions")

# Sidebar
with st.sidebar:
    st.markdown('<div class="agent-card">', unsafe_allow_html=True)
    st.markdown("### 🤖 About This System")
    st.markdown("""
    **How It Works:**
    1. 🤝 **Pro Agent** argues FOR
    2. 🚫 **Con Agent** argues AGAINST  
    3. ⚖️ **Judge Agent** evaluates
    4. 🎯 **Final Verdict** delivered
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### 💡 Quick Examples")
    examples = [
        "Should we use microservices architecture?",
        "Is remote work better than in-office?",
        "Should we invest in AI features?",
        "Is this startup idea viable?",
        "Should we expand to international markets?"
    ]
    
    for ex in examples:
        st.button(
            f"• {ex}",
            use_container_width=True,
            on_click=fill_example,
            args=(ex,)
        )
    
    st.divider()
    
    # API status
    st.markdown("### 🔧 System Status")
    st.success("✅ Gemini API: Ready")
    # model_name1 = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
    st.caption(f"Powered by {model_name}")

# Main input
st.markdown("## 📝 Enter Your Decision Question")
question = st.text_area(
    "",
    placeholder="Example: Should hospitals use AI for triage?",
    height=100,
    key="question_input",
    label_visibility="collapsed"
)

# Buttons
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    debate_btn = st.button("🚀 Start AI Debate", type="primary", use_container_width=True)
with col2:
    st.button(
        "🗑️ Clear",
        use_container_width=True,
        on_click=clear_question
    )
with col3:
    advanced = st.toggle("🔍 Advanced", help="Adds reflection agent")

if debate_btn and is_valid_question(question):

    # Progress tracking
    progress_bar = st.progress(0)
    status_container = st.empty()
    
    # Create placeholders for results
    pro_placeholder = st.empty()
    con_placeholder = st.empty()
    verdict_placeholder = st.empty()
    
    # Step 1: Pro Agent
    with status_container.container():
        st.markdown("### 🤝 **Pro Agent**: Building positive case...")
    
    with st.spinner("Generating arguments in favor..."):
        pro_result = pro_agent(question)
        progress_bar.progress(25)
        time.sleep(0.5)
        
        with pro_placeholder.container():
            st.markdown('<div class="agent-card">', unsafe_allow_html=True)
            st.markdown("### 🤝 PRO AGENT")
            st.markdown(pro_result)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 2: Con Agent
    with status_container.container():
        st.markdown("### 🚫 **Con Agent**: Analyzing risks...")
    
    with st.spinner("Identifying potential issues..."):
        con_result = con_agent(question)
        progress_bar.progress(50)
        time.sleep(0.5)
        
        with con_placeholder.container():
            st.markdown('<div class="agent-card">', unsafe_allow_html=True)
            st.markdown("### 🚫 CON AGENT")
            st.markdown(con_result)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 3: Judge Agent
    with status_container.container():
        st.markdown("### ⚖️ **Judge Agent**: Evaluating debate...")
    
    with st.spinner("Making final decision..."):
        verdict = judge_agent(pro_result, con_result, question)
        progress_bar.progress(75)
        time.sleep(0.5)
        
        with verdict_placeholder.container():
            st.markdown('<div class="verdict-box">', unsafe_allow_html=True)
            st.markdown("### ⚖️ FINAL VERDICT")
            
            # Parse and display verdict
            if "CONFIDENCE:" in verdict:
                lines = verdict.split('\n')
                for line in lines:
                    if line.startswith("VERDICT:"):
                        st.markdown(f"#### 🎯 **{line.replace('VERDICT:', '').strip()}**")
                    elif line.startswith("CONFIDENCE:"):
                        try:
                            conf = line.replace("CONFIDENCE:", "").strip()
                            if '/' in conf:
                                conf_num = float(conf.split('/')[0])
                            else:
                                conf_num = float(conf)
                            st.metric("Confidence Score", f"{conf_num:.0%}")
                            st.progress(conf_num)
                        except:
                            pass
                    elif line.startswith("KEY RISKS:"):
                        st.markdown("#### 📋 **Key Risks**")
                    elif line.strip() and line[0].isdigit() and '.' in line:
                        st.warning(line.strip())
                    elif line.startswith("RECOMMENDATIONS:"):
                        st.markdown("#### 🎯 **Recommendations**")
                    elif line.strip().startswith("-"):
                        st.success(line.strip())
                    elif line.strip() and not line.startswith("KEY RISKS") and not line.startswith("RECOMMENDATIONS"):
                        st.markdown(line.strip())
            else:
                st.markdown(verdict)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 4: Reflection (Optional)
    if advanced:
        with status_container.container():
            st.markdown("### 🔍 **Reflection Agent**: Meta-analysis...")
        
        with st.spinner("Critiquing the verdict..."):
            reflection = reflection_agent(verdict)
            progress_bar.progress(100)
            time.sleep(0.5)
            
            st.markdown("#### 🔍 Meta-Analysis")
            st.info(reflection)
    else:
        progress_bar.progress(100)
    
    # Clear status
    status_container.empty()
    
    # Success celebration
    st.success("✅ Debate completed successfully!")
    
    # Add to history
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    st.session_state.history.append({
        "question": question[:50] + "..." if len(question) > 50 else question,
        "timestamp": time.strftime("%H:%M:%S")
    })
    
    # Show history
    with st.expander("📜 Debate History"):
        if st.session_state.history:
            for i, item in enumerate(reversed(st.session_state.history[-5:])):
                st.write(f"{len(st.session_state.history)-i}. **{item['question']}** ({item['timestamp']})")
        else:
            st.write("No debates yet.")

elif debate_btn:
    st.error(
        "❌ Please enter a **clear decision-style question**.\n\n"
        "Examples:\n"
        "- Should we adopt microservices?\n"
        "- Is this startup idea viable?\n"
        "- Should hospitals use AI for triage?"
    )


# Footer
st.divider()
st.caption("Built with ❤️ for the Gemini 3 Hackathon | Powered by Google Gemini")