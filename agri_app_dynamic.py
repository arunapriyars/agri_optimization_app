import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Calculation", "Visualization"])

# -----------------------------
# Dashboard Page
# -----------------------------
if page == "Dashboard":
    st.title("🌾 Agricultural Optimization Model")
    st.markdown("""
    This project helps farmers find the **optimal pesticide level** to maximize crop yield while minimizing environmental impact.
    """)

    # Use session state values if available
    optimal_pesticide = st.session_state.get('X_opt', 2.4)
    predicted_yield = st.session_state.get('predicted_yield', 8.7)
    env_impact_score = st.session_state.get('predicted_env_damage', 35)

    col1, col2, col3 = st.columns(3)
    col1.metric("Optimal Pesticide", f"{optimal_pesticide:.2f} units/ha")
    col2.metric("Predicted Yield", f"{predicted_yield:.2f} t/ha")
    col3.metric("Environmental Impact", f"{env_impact_score:.2f}")

    st.subheader("Preview Graph")
    x = np.linspace(0, 5, 100)
    y = -1*(x-optimal_pesticide)**2 + 9  # simple preview curve
    plt.figure(figsize=(5,2))
    plt.plot(x, y, label="Crop Yield")
    plt.axvline(optimal_pesticide, color='r', linestyle='--', label="Optimal")
    plt.xlabel("Pesticide Level")
    plt.ylabel("Yield")
    plt.legend()
    st.pyplot(plt)

# -----------------------------
# Calculation Page
# -----------------------------
elif page == "Calculation":
    st.title("⚙️ Calculation Page")
    st.markdown("Enter the values to calculate **optimal pesticide level**:")

    # User Inputs
    a = st.number_input("Crop yield coefficient (a)", value=1.0)
    b = st.number_input("Yield reduction factor (b)", value=1.0)
    d = st.number_input("Ecological damage factor (d)", value=1.0)
    lam = st.number_input("Environmental weight (λ)", value=1.0)

    if st.button("Compute Optimal Pesticide Level"):
        if a != 0:
            X_opt = 2 * (b + lam*d) / a
            predicted_yield = a*X_opt - b*X_opt**2
            predicted_env_damage = d * X_opt**2

            st.success(f"✅ Optimal Pesticide Level = {X_opt:.2f} units/ha")
            st.info(f"Predicted Crop Yield = {predicted_yield:.2f} t/ha")
            st.warning(f"Predicted Environmental Damage = {predicted_env_damage:.2f}")

            # Store in session state
            st.session_state['a'] = a
            st.session_state['b'] = b
            st.session_state['d'] = d
            st.session_state['X_opt'] = X_opt
            st.session_state['predicted_yield'] = predicted_yield
            st.session_state['predicted_env_damage'] = predicted_env_damage
        else:
            st.error("Coefficient 'a' cannot be zero.")

# -----------------------------
# Visualization Page
# -----------------------------
elif page == "Visualization":
    st.title("📊 Visualization Page")
    st.markdown("Graphs showing crop yield and environmental damage:")

    # Use values from session state
    a = st.session_state.get('a', 1)
    b = st.session_state.get('b', 1)
    d = st.session_state.get('d', 1)
    X_opt = st.session_state.get('X_opt', 2.4)

    x = np.linspace(0, 5, 100)
    y_yield = a*x - b*x**2
    y_env = d * x**2

    # Crop Yield vs Pesticide
    st.subheader("Crop Yield vs Pesticide")
    plt.figure(figsize=(6,4))
    plt.plot(x, y_yield, label="Crop Yield")
    plt.axvline(X_opt, color='r', linestyle='--', label="Optimal Point")
    plt.xlabel("Pesticide Level")
    plt.ylabel("Yield")
    plt.legend()
    st.pyplot(plt)

    # Environmental Damage vs Pesticide
    st.subheader("Environmental Damage vs Pesticide")
    plt.figure(figsize=(6,4))
    plt.plot(x, y_env, label="Environmental Damage", color='orange')
    plt.axvline(X_opt, color='r', linestyle='--', label="Optimal Point")
    plt.xlabel("Pesticide Level")
    plt.ylabel("Damage")
    plt.legend()
    st.pyplot(plt)

    # Combined Graph
    st.subheader("Combined Graph")
    plt.figure(figsize=(6,4))
    plt.plot(x, y_yield, label="Yield")
    plt.plot(x, y_env, label="Environmental Damage", color='orange')
    plt.axvline(X_opt, color='r', linestyle='--', label="Optimal Point")
    plt.xlabel("Pesticide Level")
    plt.ylabel("Values")
    plt.legend()
    st.pyplot(plt)