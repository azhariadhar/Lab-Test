import streamlit as st

# ---------------- RULE DEFINITIONS ----------------
RULES = [
    {
        "name": "Windows open -> turn AC off",
        "priority": 100,
        "condition": lambda f: f["windows_open"] is True,
        "action": {
            "AC Mode": "OFF",
            "Fan Speed": "LOW",
            "Setpoint": "-",
            "Reason": "Windows are open"
        }
    },
    {
        "name": "Too cold -> turn off",
        "priority": 85,
        "condition": lambda f: f["temperature"] <= 22,
        "action": {
            "AC Mode": "OFF",
            "Fan Speed": "LOW",
            "Setpoint": "-",
            "Reason": "Already cold"
        }
    },
    {
        "name": "No one home -> eco mode",
        "priority": 90,
        "condition": lambda f: f["occupancy"] == "EMPTY" and f["temperature"] >= 24,
        "action": {
            "AC Mode": "ECO",
            "Fan Speed": "LOW",
            "Setpoint": "27°C",
            "Reason": "Home empty; save energy"
        }
    },
    {
        "name": "Hot & humid (occupied) -> cool strong",
        "priority": 80,
        "condition": lambda f: f["occupancy"] == "OCCUPIED"
                               and f["temperature"] >= 30
                               and f["humidity"] >= 70,
        "action": {
            "AC Mode": "COOL",
            "Fan Speed": "HIGH",
            "Setpoint": "23°C",
            "Reason": "Hot and humid"
        }
    },
    {
        "name": "Night (occupied) -> sleep mode",
        "priority": 75,
        "condition": lambda f: f["occupancy"] == "OCCUPIED"
                               and f["time_of_day"] == "NIGHT"
                               and f["temperature"] >= 26,
        "action": {
            "AC Mode": "SLEEP",
            "Fan Speed": "LOW",
            "Setpoint": "26°C",
            "Reason": "Night comfort"
        }
    },
    {
        "name": "Hot (occupied) -> cool",
        "priority": 70,
        "condition": lambda f: f["occupancy"] == "OCCUPIED"
                               and f["temperature"] >= 28,
        "action": {
            "AC Mode": "COOL",
            "Fan Speed": "MEDIUM",
            "Setpoint": "24°C",
            "Reason": "Temperature high"
        }
    },
    {
        "name": "Slightly warm (occupied) -> gentle cool",
        "priority": 60,
        "condition": lambda f: f["occupancy"] == "OCCUPIED"
                               and 26 <= f["temperature"] < 28,
        "action": {
            "AC Mode": "COOL",
            "Fan Speed": "LOW",
            "Setpoint": "25°C",
            "Reason": "Slightly warm"
        }
    },
]

# ---------------- RULE ENGINE ----------------
def evaluate_rules(facts):
    matched = [r for r in RULES if r["condition"](facts)]
    matched.sort(key=lambda r: r["priority"], reverse=True)
    return matched[0] if matched else None


# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="Smart AC Controller", layout="centered")

st.title("Smart Home Air Conditioner Controller")
st.write("Rule-Based Decision System")

st.sidebar.header("Home Conditions")

temperature = st.sidebar.number_input("Temperature (°C)", value=22)
humidity = st.sidebar.number_input("Humidity (%)", value=46)
occupancy = st.sidebar.selectbox("Occupancy", ["OCCUPIED", "EMPTY"])
time_of_day = st.sidebar.selectbox(
    "Time of Day", ["MORNING", "AFTERNOON", "EVENING", "NIGHT"]
)
windows_open = st.sidebar.checkbox("Windows Open", value=False)

facts = {
    "temperature": temperature,
    "humidity": humidity,
    "occupancy": occupancy,
    "time_of_day": time_of_day,
    "windows_open": windows_open
}

st.subheader("Current Home Facts")
st.json(facts)

if st.button("Evaluate AC Setting"):
    result = evaluate_rules(facts)

    if result:
        st.success(f"Rule Applied: {result['name']}")
        st.subheader("AC Decision")
        st.write(f"**AC Mode:** {result['action']['AC Mode']}")
        st.write(f"**Fan Speed:** {result['action']['Fan Speed']}")
        st.write(f"**Setpoint:** {result['action']['Setpoint']}")
        st.write(f"**Reason:** {result['action']['Reason']}")
    else:
        st.warning("No matching rule found.")
