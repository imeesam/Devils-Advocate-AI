import streamlit as st
import time
from agents import pro_agent, con_agent, judge_agent, reflection_agent

# Page config
st.set_page_config(
    page_title="Devil's Advocate AI",
    page_icon="⚖️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .agent-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .verdict-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">⚖️ Devil\'s Advocate AI</h1>', unsafe_allow_html=True)
st.markdown("### Multi-Agent Decision System • Powered by Groq")
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
        if st.button(f"• {ex}", use_container_width=True):
            st.session_state.question = ex
            st.rerun()
    
    st.divider()
    
    # API status
    st.markdown("### 🔧 System Status")
    st.success("✅ Groq API: Ready")
    st.caption("Powered by Llama 3.3 70B")

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
    clear_btn = st.button("🗑️ Clear", use_container_width=True)
with col3:
    advanced = st.toggle("🔍 Advanced", help="Adds reflection agent")

if clear_btn:
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

if debate_btn and question.strip():
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
            st.markdown("### 🤝 PRO AGENT (Arguments FOR)")
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
            st.markdown("### 🚫 CON AGENT (Arguments AGAINST)")
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
            st.markdown('<div class="verdict-card">', unsafe_allow_html=True)
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
    st.balloons()
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
    st.error("❌ Please enter a question first!")

# Footer
st.divider()
st.caption("Built with ❤️ for the Gemini 3 Hackathon | Powered by Groq Llama 3.3 70B")