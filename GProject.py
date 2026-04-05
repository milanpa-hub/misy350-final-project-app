import streamlit as st
import json
from pathlib import Path
from datetime import datetime, date
import uuid

st.set_page_config(page_title="Campus Collab", layout="wide", initial_sidebar_state="expanded")

# ==========================================================
# SESSION STATE
# ==========================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = ""
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_role" not in st.session_state:
    st.session_state.user_role = ""
if "page" not in st.session_state:
    st.session_state.page = "Welcome"
if "selected_session_id" not in st.session_state:
    st.session_state.selected_session_id = ""
if "selected_claim_id" not in st.session_state:
    st.session_state.selected_claim_id = ""
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": "Hi! I can answer simple questions like: What sessions still need items? What did I sign up to bring? Which sessions are open?"
        }
    ]

# ==========================================================
# JSON FILE SETUP
# ==========================================================
users_path = Path("users.json")
sessions_path = Path("sessions.json")
needs_path = Path("needs.json")
claims_path = Path("claims.json")

if not users_path.exists():
    users_path.write_text(json.dumps([
        {
            "user_id": "host-demo-1",
            "full_name": "Demo Host",
            "email": "host@udel.edu",
            "password": "host123",
            "role": "Host",
            "registered_at": str(datetime.now())
        },
        {
            "user_id": "contrib-demo-1",
            "full_name": "Demo Contributor",
            "email": "student@udel.edu",
            "password": "student123",
            "role": "Contributor",
            "registered_at": str(datetime.now())
        }
    ], indent=4), encoding="utf-8")

if not sessions_path.exists():
    sessions_path.write_text(json.dumps([
        {
            "session_id": "session-1",
            "host_id": "host-demo-1",
            "title": "MISY350 Debugging Night",
            "category": "Study Session",
            "date": "2026-04-15",
            "time": "6:00 PM",
            "location": "Morris Library Room 114",
            "description": "Bring your Streamlit bugs and we will work through them together.",
            "status": "Open",
            "created_at": str(datetime.now())
        }
    ], indent=4), encoding="utf-8")

if not needs_path.exists():
    needs_path.write_text(json.dumps([
        {
            "need_id": "need-1",
            "session_id": "session-1",
            "item_name": "Extension Cord",
            "quantity_needed": 2,
            "quantity_claimed": 0,
            "notes": "Any length is fine"
        },
        {
            "need_id": "need-2",
            "session_id": "session-1",
            "item_name": "Practice Questions",
            "quantity_needed": 5,
            "quantity_claimed": 0,
            "notes": "Printed or digital"
        }
    ], indent=4), encoding="utf-8")

if not claims_path.exists():
    claims_path.write_text(json.dumps([], indent=4), encoding="utf-8")

try:
    users = json.loads(users_path.read_text(encoding="utf-8"))
except:
    users = []

try:
    sessions = json.loads(sessions_path.read_text(encoding="utf-8"))
except:
    sessions = []

try:
    needs = json.loads(needs_path.read_text(encoding="utf-8"))
except:
    needs = []

try:
    claims = json.loads(claims_path.read_text(encoding="utf-8"))
except:
    claims = []

# ==========================================================
# REUSABLE DERIVED DATA (NO FUNCTIONS / NO CLASSES)
# ==========================================================
current_user = None
for u in users:
    if u["user_id"] == st.session_state.user_id:
        current_user = u
        break

selected_session = None
if st.session_state.selected_session_id != "":
    for s in sessions:
        if s["session_id"] == st.session_state.selected_session_id:
            selected_session = s
            break

selected_claim = None
if st.session_state.selected_claim_id != "":
    for c in claims:
        if c["claim_id"] == st.session_state.selected_claim_id:
            selected_claim = c
            break

open_sessions_count = 0
for s in sessions:
    if s["status"] == "Open":
        open_sessions_count += 1

# ==========================================================
# SIDEBAR NAVIGATION
# ==========================================================
with st.sidebar:
    st.markdown("## Campus Collab")
    st.caption("Study sessions, project prep, and contribution tracking")

    if st.session_state.logged_in:
        st.success(f"Logged in as {st.session_state.user_name}")
        st.caption(f"Role: {st.session_state.user_role}")
        st.divider()

        if st.session_state.user_role == "Host":
            if st.button("Host Dashboard", use_container_width=True, key="nav_host_dashboard"):
                st.session_state.page = "Host Dashboard"
                st.rerun()
            if st.button("Create Session", use_container_width=True, key="nav_create_session"):
                st.session_state.page = "Create Session"
                st.rerun()
            if st.button("Manage Session", use_container_width=True, key="nav_manage_session"):
                st.session_state.page = "Manage Session"
                st.rerun()

        if st.session_state.user_role == "Contributor":
            if st.button("Contributor Dashboard", use_container_width=True, key="nav_contrib_dashboard"):
                st.session_state.page = "Contributor Dashboard"
                st.rerun()
            if st.button("Browse Sessions", use_container_width=True, key="nav_browse_sessions"):
                st.session_state.page = "Browse Sessions"
                st.rerun()
            if st.button("My Contributions", use_container_width=True, key="nav_my_contributions"):
                st.session_state.page = "My Contributions"
                st.rerun()

        st.divider()
        if st.button("Log Out", type="primary", use_container_width=True, key="logout_button"):
            st.session_state.logged_in = False
            st.session_state.user_id = ""
            st.session_state.user_name = ""
            st.session_state.user_role = ""
            st.session_state.page = "Welcome"
            st.session_state.selected_session_id = ""
            st.session_state.selected_claim_id = ""
            st.session_state.chat_messages = [
                {
                    "role": "assistant",
                    "content": "Hi! I can answer simple questions like: What sessions still need items? What did I sign up to bring? Which sessions are open?"
                }
            ]
            st.rerun()
    else:
        if st.button("Welcome", use_container_width=True, key="nav_welcome"):
            st.session_state.page = "Welcome"
            st.rerun()
        if st.button("Register", use_container_width=True, key="nav_register"):
            st.session_state.page = "Register"
            st.rerun()
        if st.button("Log In", use_container_width=True, key="nav_login"):
            st.session_state.page = "Log In"
            st.rerun()

# ==========================================================
# PUBLIC PAGES
# ==========================================================
if st.session_state.logged_in == False and st.session_state.page == "Welcome":
    st.markdown("# Campus Collab")
    st.markdown("### Organize study sessions, club prep meetings, and group project meetups")

    top_col1, top_col2, top_col3 = st.columns(3)
    top_col1.metric("Open Sessions", open_sessions_count)
    top_col2.metric("Registered Users", len(users))
    top_col3.metric("Active Claims", len(claims))

    left_col, right_col = st.columns([2, 1])
    with left_col:
        with st.container(border=True):
            st.markdown("#### What this app does")
            st.write("Hosts create small campus collaboration sessions and list what they need.")
            st.write("Contributors browse sessions and claim an item or resource they will bring.")
            st.write("The app supports authentication, role-based dashboards, JSON-backed storage, and meaningful CRUD workflows.")
    with right_col:
        with st.container(border=True):
            st.markdown("#### Quick Start")
            st.write("1. Register for an account")
            st.write("2. Log in as a Host or Contributor")
            st.write("3. Use the sidebar to manage your workflow")

elif st.session_state.logged_in == False and st.session_state.page == "Register":
    st.markdown("# Register")
    with st.container(border=True):
        register_name = st.text_input("Full Name", key="register_name")
        register_email = st.text_input("Email", key="register_email")
        register_password = st.text_input("Password", type="password", key="register_password")
        register_role = st.selectbox("Role", ["Select a role", "Host", "Contributor"], key="register_role")

        if st.button("Create Account", type="primary", use_container_width=True, key="create_account_button"):
            duplicate_email = False
            for u in users:
                if u["email"].strip().lower() == register_email.strip().lower():
                    duplicate_email = True

            if register_name.strip() == "" or register_email.strip() == "" or register_password.strip() == "" or register_role == "Select a role":
                st.warning("All registration fields are required.")
            elif "@" not in register_email or "." not in register_email:
                st.warning("Please enter a valid email address.")
            elif duplicate_email:
                st.error("That email is already registered.")
            else:
                users.append(
                    {
                        "user_id": str(uuid.uuid4()),
                        "full_name": register_name.strip(),
                        "email": register_email.strip().lower(),
                        "password": register_password,
                        "role": register_role,
                        "registered_at": str(datetime.now())
                    }
                )
                users_path.write_text(json.dumps(users, indent=4), encoding="utf-8")
                st.success("Account created successfully. You can now log in.")
                st.session_state.page = "Log In"
                st.rerun()

elif st.session_state.logged_in == False and st.session_state.page == "Log In":
    st.markdown("# Log In")
    with st.container(border=True):
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")

        if st.button("Log In", type="primary", use_container_width=True, key="login_button"):
            found_user = None
            for u in users:
                if u["email"].strip().lower() == login_email.strip().lower() and u["password"] == login_password:
                    found_user = u
                    break

            if login_email.strip() == "" or login_password.strip() == "":
                st.warning("Email and password are required.")
            elif found_user is None:
                st.error("Invalid email or password.")
            else:
                st.session_state.logged_in = True
                st.session_state.user_id = found_user["user_id"]
                st.session_state.user_name = found_user["full_name"]
                st.session_state.user_role = found_user["role"]
                st.session_state.selected_session_id = ""
                st.session_state.selected_claim_id = ""
                if found_user["role"] == "Host":
                    st.session_state.page = "Host Dashboard"
                else:
                    st.session_state.page = "Contributor Dashboard"
                st.success("Login successful.")
                st.rerun()

# ==========================================================
# HOST PAGES
# ==========================================================
elif st.session_state.logged_in and st.session_state.user_role == "Host" and st.session_state.page == "Host Dashboard":
    st.markdown("# Host Dashboard")

    my_sessions = []
    for s in sessions:
        if s["host_id"] == st.session_state.user_id:
            my_sessions.append(s)

    total_host_claims = 0
    total_open_host_sessions = 0
    for s in my_sessions:
        if s["status"] == "Open":
            total_open_host_sessions += 1
        for c in claims:
            if c["session_id"] == s["session_id"]:
                total_host_claims += 1

    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("My Sessions", len(my_sessions))
    metric_col2.metric("My Open Sessions", total_open_host_sessions)
    metric_col3.metric("Claims on My Sessions", total_host_claims)

    tab1, tab2 = st.tabs(["Session Overview", "Session Assistant"])

    with tab1:
        if len(my_sessions) == 0:
            st.info("You have not created any sessions yet. Use Create Session to add one.")
        else:
            display_rows = []
            for s in my_sessions:
                claim_total = 0
                for c in claims:
                    if c["session_id"] == s["session_id"]:
                        claim_total += 1
                display_rows.append(
                    {
                        "Title": s["title"],
                        "Category": s["category"],
                        "Date": s["date"],
                        "Time": s["time"],
                        "Location": s["location"],
                        "Status": s["status"],
                        "Claims": claim_total
                    }
                )
            st.dataframe(display_rows, use_container_width=True)

            host_selected_label_options = []
            for s in my_sessions:
                host_selected_label_options.append(f"{s['title']} | {s['date']} | {s['time']} | {s['session_id']}")

            host_selected_label = st.selectbox("Select a session to inspect", host_selected_label_options, key="host_session_selectbox")

            chosen_session_id = host_selected_label.split(" | ")[-1]
            st.session_state.selected_session_id = chosen_session_id

            selected_session = None
            for s in sessions:
                if s["session_id"] == chosen_session_id:
                    selected_session = s
                    break

            if selected_session is not None:
                details_col1, details_col2 = st.columns([2, 1])
                with details_col1:
                    with st.container(border=True):
                        st.markdown(f"### {selected_session['title']}")
                        st.write(f"**Category:** {selected_session['category']}")
                        st.write(f"**Date:** {selected_session['date']}")
                        st.write(f"**Time:** {selected_session['time']}")
                        st.write(f"**Location:** {selected_session['location']}")
                        st.write(f"**Status:** {selected_session['status']}")
                        st.write(f"**Description:** {selected_session['description']}")
                with details_col2:
                    with st.container(border=True):
                        open_need_count = 0
                        for n in needs:
                            if n["session_id"] == selected_session["session_id"]:
                                remaining_qty = int(n["quantity_needed"]) - int(n["quantity_claimed"])
                                if remaining_qty > 0:
                                    open_need_count += 1
                        st.metric("Open Need Items", open_need_count)

                needs_rows = []
                claims_rows = []
                for n in needs:
                    if n["session_id"] == selected_session["session_id"]:
                        needs_rows.append(
                            {
                                "Item": n["item_name"],
                                "Needed": n["quantity_needed"],
                                "Claimed": n["quantity_claimed"],
                                "Remaining": int(n["quantity_needed"]) - int(n["quantity_claimed"]),
                                "Notes": n["notes"]
                            }
                        )

                for c in claims:
                    if c["session_id"] == selected_session["session_id"]:
                        contributor_name = "Unknown"
                        for u in users:
                            if u["user_id"] == c["contributor_id"]:
                                contributor_name = u["full_name"]
                        claims_rows.append(
                            {
                                "Contributor": contributor_name,
                                "Item": c["claimed_item"],
                                "Status": c["status"]
                            }
                        )

                table_col1, table_col2 = st.columns(2)
                with table_col1:
                    st.markdown("#### Needs List")
                    if len(needs_rows) == 0:
                        st.info("No needed items have been added yet.")
                    else:
                        st.dataframe(needs_rows, use_container_width=True)
                with table_col2:
                    st.markdown("#### Claims")
                    if len(claims_rows) == 0:
                        st.info("No claims yet.")
                    else:
                        st.dataframe(claims_rows, use_container_width=True)

                if st.button("Go to Manage Session", use_container_width=True, key="go_manage_session_button"):
                    st.session_state.page = "Manage Session"
                    st.rerun()

    with tab2:
        caption_col1, caption_col2 = st.columns([3, 1])
        with caption_col1:
            st.caption("Try: What sessions still need items? Which sessions are open? Help")
        with caption_col2:
            if st.button("Clear Chat", use_container_width=True, key="clear_host_chat"):
                st.session_state.chat_messages = [
                    {
                        "role": "assistant",
                        "content": "Hi! I can answer simple questions like: What sessions still need items? What did I sign up to bring? Which sessions are open?"
                    }
                ]
                st.rerun()

        with st.container(border=True, height=300):
            for msg in st.session_state.chat_messages:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

        host_question = st.chat_input("Ask about your sessions...", key="host_chat_input")
        if host_question:
            st.session_state.chat_messages.append({"role": "user", "content": host_question})
            lower_prompt = host_question.strip().lower()
            reply = "I could not find an answer for that. Try one of the suggested questions."

            if "what sessions still need items" in lower_prompt or "sessions still need items" in lower_prompt:
                answer_lines = []
                for s in sessions:
                    if s["status"] == "Open":
                        missing_list = []
                        for n in needs:
                            if n["session_id"] == s["session_id"]:
                                remaining_qty = int(n["quantity_needed"]) - int(n["quantity_claimed"])
                                if remaining_qty > 0:
                                    missing_list.append(f"{n['item_name']} ({remaining_qty} left)")
                        if len(missing_list) > 0:
                            answer_lines.append(f"{s['title']}: " + ", ".join(missing_list))
                if len(answer_lines) == 0:
                    reply = "No open sessions currently need items."
                else:
                    reply = "Here are the sessions that still need items:\n\n" + "\n".join(answer_lines)

            elif "open sessions" in lower_prompt or "browse sessions" in lower_prompt:
                open_titles = []
                for s in sessions:
                    if s["status"] == "Open":
                        open_titles.append(s["title"])
                if len(open_titles) == 0:
                    reply = "There are no open sessions right now."
                else:
                    reply = "Open sessions:\n\n" + "\n".join(open_titles)

            elif "help" in lower_prompt:
                reply = "Try asking: What sessions still need items? Which sessions are open?"

            st.session_state.chat_messages.append({"role": "assistant", "content": reply})
            st.rerun()

elif st.session_state.logged_in and st.session_state.user_role == "Host" and st.session_state.page == "Create Session":
    st.markdown("# Create Session")

    with st.container(border=True):
        create_title = st.text_input("Session Title", key="create_title")
        create_category = st.selectbox("Category", ["Study Session", "Club Prep", "Project Work", "Workshop", "Presentation Practice"], key="create_category")
        create_date = st.date_input("Date", value=date.today(), key="create_date")
        create_time = st.text_input("Time", placeholder="Example: 7:00 PM", key="create_time")
        create_location = st.text_input("Location", key="create_location")
        create_description = st.text_area("Description", key="create_description")

        st.markdown("### Add up to 4 needed items")
        item1 = st.text_input("Item 1", key="item1")
        qty1 = st.number_input("Quantity 1", min_value=0, step=1, key="qty1")
        note1 = st.text_input("Notes 1", key="note1")

        item2 = st.text_input("Item 2", key="item2")
        qty2 = st.number_input("Quantity 2", min_value=0, step=1, key="qty2")
        note2 = st.text_input("Notes 2", key="note2")

        item3 = st.text_input("Item 3", key="item3")
        qty3 = st.number_input("Quantity 3", min_value=0, step=1, key="qty3")
        note3 = st.text_input("Notes 3", key="note3")

        item4 = st.text_input("Item 4", key="item4")
        qty4 = st.number_input("Quantity 4", min_value=0, step=1, key="qty4")
        note4 = st.text_input("Notes 4", key="note4")

        if st.button("Save Session", type="primary", use_container_width=True, key="save_session_button"):
            item_count = 0
            if item1.strip() != "" and int(qty1) > 0:
                item_count += 1
            if item2.strip() != "" and int(qty2) > 0:
                item_count += 1
            if item3.strip() != "" and int(qty3) > 0:
                item_count += 1
            if item4.strip() != "" and int(qty4) > 0:
                item_count += 1

            if create_title.strip() == "" or create_time.strip() == "" or create_location.strip() == "":
                st.warning("Title, time, and location are required.")
            elif item_count == 0:
                st.warning("Please add at least one needed item with a quantity greater than 0.")
            else:
                new_session_id = str(uuid.uuid4())
                sessions.append(
                    {
                        "session_id": new_session_id,
                        "host_id": st.session_state.user_id,
                        "title": create_title.strip(),
                        "category": create_category,
                        "date": str(create_date),
                        "time": create_time.strip(),
                        "location": create_location.strip(),
                        "description": create_description.strip(),
                        "status": "Open",
                        "created_at": str(datetime.now())
                    }
                )

                if item1.strip() != "" and int(qty1) > 0:
                    needs.append({
                        "need_id": str(uuid.uuid4()),
                        "session_id": new_session_id,
                        "item_name": item1.strip(),
                        "quantity_needed": int(qty1),
                        "quantity_claimed": 0,
                        "notes": note1.strip()
                    })
                if item2.strip() != "" and int(qty2) > 0:
                    needs.append({
                        "need_id": str(uuid.uuid4()),
                        "session_id": new_session_id,
                        "item_name": item2.strip(),
                        "quantity_needed": int(qty2),
                        "quantity_claimed": 0,
                        "notes": note2.strip()
                    })
                if item3.strip() != "" and int(qty3) > 0:
                    needs.append({
                        "need_id": str(uuid.uuid4()),
                        "session_id": new_session_id,
                        "item_name": item3.strip(),
                        "quantity_needed": int(qty3),
                        "quantity_claimed": 0,
                        "notes": note3.strip()
                    })
                if item4.strip() != "" and int(qty4) > 0:
                    needs.append({
                        "need_id": str(uuid.uuid4()),
                        "session_id": new_session_id,
                        "item_name": item4.strip(),
                        "quantity_needed": int(qty4),
                        "quantity_claimed": 0,
                        "notes": note4.strip()
                    })

                sessions_path.write_text(json.dumps(sessions, indent=4), encoding="utf-8")
                needs_path.write_text(json.dumps(needs, indent=4), encoding="utf-8")
                st.session_state.selected_session_id = new_session_id
                st.success("Session created successfully.")
                st.session_state.page = "Manage Session"
                st.rerun()

elif st.session_state.logged_in and st.session_state.user_role == "Host" and st.session_state.page == "Manage Session":
    st.markdown("# Manage Session")

    my_sessions = []
    for s in sessions:
        if s["host_id"] == st.session_state.user_id:
            my_sessions.append(s)

    if len(my_sessions) == 0:
        st.info("You do not have any sessions to manage yet.")
    else:
        manage_options = []
        for s in my_sessions:
            manage_options.append(f"{s['title']} | {s['date']} | {s['time']} | {s['session_id']}")

        default_index = 0
        if st.session_state.selected_session_id != "":
            i = 0
            while i < len(my_sessions):
                if my_sessions[i]["session_id"] == st.session_state.selected_session_id:
                    default_index = i
                i += 1

        selected_manage_label = st.selectbox("Choose a session to manage", manage_options, index=default_index, key="manage_session_selectbox")
        manage_session_id = selected_manage_label.split(" | ")[-1]
        st.session_state.selected_session_id = manage_session_id

        selected_session = None
        for s in sessions:
            if s["session_id"] == manage_session_id:
                selected_session = s
                break

        if selected_session is not None:
            st.markdown("### Edit Session Details")
            edit_col1, edit_col2 = st.columns(2)
            with edit_col1:
                edit_title = st.text_input("Title", value=selected_session["title"], key=f"edit_title_{manage_session_id}")
                edit_category = st.text_input("Category", value=selected_session["category"], key=f"edit_category_{manage_session_id}")
                edit_date = st.date_input("Date", value=datetime.strptime(selected_session["date"], "%Y-%m-%d").date(), key=f"edit_date_{manage_session_id}")
                edit_time = st.text_input("Time", value=selected_session["time"], key=f"edit_time_{manage_session_id}")
            with edit_col2:
                edit_location = st.text_input("Location", value=selected_session["location"], key=f"edit_location_{manage_session_id}")
                edit_status = st.selectbox("Status", ["Open", "Closed"], index=0 if selected_session["status"] == "Open" else 1, key=f"edit_status_{manage_session_id}")
                edit_description = st.text_area("Description", value=selected_session["description"], key=f"edit_description_{manage_session_id}")

            update_col1, update_col2 = st.columns(2)
            with update_col1:
                if st.button("Update Session Details", type="primary", use_container_width=True, key=f"update_session_details_{manage_session_id}"):
                    if edit_title.strip() == "" or edit_category.strip() == "" or edit_time.strip() == "" or edit_location.strip() == "":
                        st.warning("Title, category, time, and location are required.")
                    else:
                        selected_session["title"] = edit_title.strip()
                        selected_session["category"] = edit_category.strip()
                        selected_session["date"] = str(edit_date)
                        selected_session["time"] = edit_time.strip()
                        selected_session["location"] = edit_location.strip()
                        selected_session["status"] = edit_status
                        selected_session["description"] = edit_description.strip()
                        sessions_path.write_text(json.dumps(sessions, indent=4), encoding="utf-8")
                        st.success("Session details updated.")
                        st.rerun()
            with update_col2:
                if st.button("Delete Entire Session", use_container_width=True, key=f"delete_entire_session_{manage_session_id}"):
                    sessions = [s for s in sessions if s["session_id"] != manage_session_id]
                    needs = [n for n in needs if n["session_id"] != manage_session_id]
                    claims = [c for c in claims if c["session_id"] != manage_session_id]
                    sessions_path.write_text(json.dumps(sessions, indent=4), encoding="utf-8")
                    needs_path.write_text(json.dumps(needs, indent=4), encoding="utf-8")
                    claims_path.write_text(json.dumps(claims, indent=4), encoding="utf-8")
                    st.session_state.selected_session_id = ""
                    st.success("Session deleted.")
                    st.session_state.page = "Host Dashboard"
                    st.rerun()

            st.divider()
            st.markdown("### Manage Needed Items")

            session_needs = []
            for n in needs:
                if n["session_id"] == manage_session_id:
                    session_needs.append(n)

            if len(session_needs) == 0:
                st.info("This session does not have any needed items yet.")
            else:
                for n in session_needs:
                    with st.container(border=True):
                        need_col1, need_col2, need_col3 = st.columns([2, 1, 1])
                        with need_col1:
                            edit_need_item = st.text_input("Item Name", value=n["item_name"], key=f"need_item_{n['need_id']}")
                            edit_need_note = st.text_input("Notes", value=n["notes"], key=f"need_note_{n['need_id']}")
                        with need_col2:
                            edit_need_qty = st.number_input("Quantity Needed", min_value=int(n["quantity_claimed"]), step=1, value=int(n["quantity_needed"]), key=f"need_qty_{n['need_id']}")
                            st.caption(f"Already Claimed: {n['quantity_claimed']}")
                        with need_col3:
                            if st.button("Update Item", use_container_width=True, key=f"update_need_{n['need_id']}"):
                                if edit_need_item.strip() == "":
                                    st.warning("Item name cannot be blank.")
                                else:
                                    n["item_name"] = edit_need_item.strip()
                                    n["notes"] = edit_need_note.strip()
                                    n["quantity_needed"] = int(edit_need_qty)
                                    for c in claims:
                                        if c["need_id"] == n["need_id"]:
                                            c["claimed_item"] = edit_need_item.strip()
                                    needs_path.write_text(json.dumps(needs, indent=4), encoding="utf-8")
                                    claims_path.write_text(json.dumps(claims, indent=4), encoding="utf-8")
                                    st.success("Need item updated.")
                                    st.rerun()
                            if st.button("Delete Item", use_container_width=True, key=f"delete_need_{n['need_id']}"):
                                if int(n["quantity_claimed"]) > 0:
                                    st.warning("You cannot delete an item that already has claims. Remove the claims first.")
                                else:
                                    needs = [x for x in needs if x["need_id"] != n["need_id"]]
                                    needs_path.write_text(json.dumps(needs, indent=4), encoding="utf-8")
                                    st.success("Need item deleted.")
                                    st.rerun()

            st.divider()
            st.markdown("### Add a New Needed Item")
            add_item_col1, add_item_col2, add_item_col3 = st.columns([2, 1, 1])
            with add_item_col1:
                add_need_name = st.text_input("New Item Name", key=f"new_need_name_{manage_session_id}")
                add_need_note = st.text_input("New Item Notes", key=f"new_need_note_{manage_session_id}")
            with add_item_col2:
                add_need_qty = st.number_input("New Item Quantity", min_value=1, step=1, value=1, key=f"new_need_qty_{manage_session_id}")
            with add_item_col3:
                st.write("")
                st.write("")
                if st.button("Add Needed Item", type="primary", use_container_width=True, key=f"add_need_item_{manage_session_id}"):
                    if add_need_name.strip() == "":
                        st.warning("Item name is required.")
                    else:
                        needs.append(
                            {
                                "need_id": str(uuid.uuid4()),
                                "session_id": manage_session_id,
                                "item_name": add_need_name.strip(),
                                "quantity_needed": int(add_need_qty),
                                "quantity_claimed": 0,
                                "notes": add_need_note.strip()
                            }
                        )
                        needs_path.write_text(json.dumps(needs, indent=4), encoding="utf-8")
                        st.success("Needed item added.")
                        st.rerun()

# ==========================================================
# CONTRIBUTOR PAGES
# ==========================================================
elif st.session_state.logged_in and st.session_state.user_role == "Contributor" and st.session_state.page == "Contributor Dashboard":
    st.markdown("# Contributor Dashboard")

    my_claims = []
    for c in claims:
        if c["contributor_id"] == st.session_state.user_id:
            my_claims.append(c)

    joined_session_ids = []
    for c in my_claims:
        if c["session_id"] not in joined_session_ids:
            joined_session_ids.append(c["session_id"])

    dashboard_col1, dashboard_col2, dashboard_col3 = st.columns(3)
    dashboard_col1.metric("Open Sessions", open_sessions_count)
    dashboard_col2.metric("My Claims", len(my_claims))
    dashboard_col3.metric("Sessions I Joined", len(joined_session_ids))

    lower_col1, lower_col2 = st.columns(2)
    with lower_col1:
        with st.container(border=True):
            st.markdown("### My Recent Claims")
            if len(my_claims) == 0:
                st.info("You have not claimed anything yet.")
            else:
                claim_rows = []
                for c in my_claims:
                    session_title = "Unknown"
                    for s in sessions:
                        if s["session_id"] == c["session_id"]:
                            session_title = s["title"]
                    claim_rows.append(
                        {
                            "Session": session_title,
                            "Item": c["claimed_item"],
                            "Status": c["status"]
                        }
                    )
                st.dataframe(claim_rows, use_container_width=True)
    with lower_col2:
        with st.container(border=True):
            st.markdown("### Open Sessions")
            open_rows = []
            for s in sessions:
                if s["status"] == "Open":
                    open_rows.append(
                        {
                            "Title": s["title"],
                            "Date": s["date"],
                            "Time": s["time"],
                            "Location": s["location"]
                        }
                    )
            if len(open_rows) == 0:
                st.warning("No open sessions are available right now.")
            else:
                st.dataframe(open_rows, use_container_width=True)

elif st.session_state.logged_in and st.session_state.user_role == "Contributor" and st.session_state.page == "Browse Sessions":
    st.markdown("# Browse Sessions")

    browse_sessions = []
    for s in sessions:
        if s["status"] == "Open":
            browse_sessions.append(s)

    if len(browse_sessions) == 0:
        st.warning("There are no open sessions right now.")
    else:
        browse_options = []
        for s in browse_sessions:
            browse_options.append(f"{s['title']} | {s['date']} | {s['time']} | {s['session_id']}")

        browse_selected_label = st.selectbox("Select a session", browse_options, key="browse_session_selectbox")
        browse_session_id = browse_selected_label.split(" | ")[-1]
        st.session_state.selected_session_id = browse_session_id

        selected_session = None
        for s in sessions:
            if s["session_id"] == browse_session_id:
                selected_session = s
                break

        if selected_session is not None:
            info_col1, info_col2 = st.columns([2, 1])
            with info_col1:
                with st.container(border=True):
                    st.markdown(f"### {selected_session['title']}")
                    st.write(f"**Category:** {selected_session['category']}")
                    st.write(f"**Date:** {selected_session['date']}")
                    st.write(f"**Time:** {selected_session['time']}")
                    st.write(f"**Location:** {selected_session['location']}")
                    st.write(f"**Description:** {selected_session['description']}")
            with info_col2:
                with st.container(border=True):
                    available_count = 0
                    for n in needs:
                        if n["session_id"] == browse_session_id:
                            remaining = int(n["quantity_needed"]) - int(n["quantity_claimed"])
                            if remaining > 0:
                                available_count += 1
                    st.metric("Available Item Types", available_count)

            available_needs = []
            available_needs_labels = []
            for n in needs:
                if n["session_id"] == browse_session_id:
                    remaining = int(n["quantity_needed"]) - int(n["quantity_claimed"])
                    if remaining > 0:
                        available_needs.append(n)
                        available_needs_labels.append(f"{n['item_name']} | {remaining} left | {n['need_id']}")

            st.markdown("### Available Items to Claim")
            if len(available_needs) == 0:
                st.info("Everything for this session has already been claimed.")
            else:
                display_available = []
                for n in available_needs:
                    display_available.append(
                        {
                            "Item": n["item_name"],
                            "Remaining": int(n["quantity_needed"]) - int(n["quantity_claimed"]),
                            "Notes": n["notes"]
                        }
                    )
                st.dataframe(display_available, use_container_width=True)

                selected_need_label = st.selectbox("Choose an item to bring", available_needs_labels, key="available_need_selectbox")
                selected_need_id = selected_need_label.split(" | ")[-1]

                selected_need = None
                for n in needs:
                    if n["need_id"] == selected_need_id:
                        selected_need = n
                        break

                if st.button("Claim This Item", type="primary", use_container_width=True, key="claim_this_item_button"):
                    already_claimed_same_item = False
                    for c in claims:
                        if c["contributor_id"] == st.session_state.user_id and c["need_id"] == selected_need_id:
                            already_claimed_same_item = True

                    if already_claimed_same_item:
                        st.warning("You already claimed this exact item.")
                    else:
                        remaining = int(selected_need["quantity_needed"]) - int(selected_need["quantity_claimed"])
                        if remaining <= 0:
                            st.warning("That item is no longer available.")
                        else:
                            selected_need["quantity_claimed"] = int(selected_need["quantity_claimed"]) + 1
                            claims.append(
                                {
                                    "claim_id": str(uuid.uuid4()),
                                    "need_id": selected_need_id,
                                    "session_id": browse_session_id,
                                    "contributor_id": st.session_state.user_id,
                                    "claimed_item": selected_need["item_name"],
                                    "status": "Claimed",
                                    "claimed_at": str(datetime.now())
                                }
                            )
                            needs_path.write_text(json.dumps(needs, indent=4), encoding="utf-8")
                            claims_path.write_text(json.dumps(claims, indent=4), encoding="utf-8")
                            st.success("Item claimed successfully.")
                            st.session_state.page = "My Contributions"
                            st.rerun()

elif st.session_state.logged_in and st.session_state.user_role == "Contributor" and st.session_state.page == "My Contributions":
    st.markdown("# My Contributions")

    my_claims = []
    for c in claims:
        if c["contributor_id"] == st.session_state.user_id:
            my_claims.append(c)

    tab1, tab2 = st.tabs(["Manage Claims", "Contributor Assistant"])

    with tab1:
        if len(my_claims) == 0:
            st.info("You do not have any claims yet.")
        else:
            contribution_rows = []
            for c in my_claims:
                session_title = "Unknown"
                for s in sessions:
                    if s["session_id"] == c["session_id"]:
                        session_title = s["title"]
                contribution_rows.append(
                    {
                        "Session": session_title,
                        "Item": c["claimed_item"],
                        "Status": c["status"]
                    }
                )
            st.dataframe(contribution_rows, use_container_width=True)

            claim_labels = []
            for c in my_claims:
                session_title = "Unknown"
                for s in sessions:
                    if s["session_id"] == c["session_id"]:
                        session_title = s["title"]
                claim_labels.append(f"{session_title} | {c['claimed_item']} | {c['claim_id']}")

            selected_claim_label = st.selectbox("Select one of your claims", claim_labels, key="manage_claims_selectbox")
            selected_claim_id = selected_claim_label.split(" | ")[-1]
            st.session_state.selected_claim_id = selected_claim_id

            selected_claim = None
            for c in claims:
                if c["claim_id"] == selected_claim_id:
                    selected_claim = c
                    break

            if selected_claim is not None:
                related_session = None
                related_need = None
                for s in sessions:
                    if s["session_id"] == selected_claim["session_id"]:
                        related_session = s
                for n in needs:
                    if n["need_id"] == selected_claim["need_id"]:
                        related_need = n

                with st.container(border=True):
                    st.markdown("### Claim Details")
                    st.write(f"**Session:** {related_session['title'] if related_session else 'Unknown'}")
                    st.write(f"**Current Item:** {selected_claim['claimed_item']}")
                    st.write(f"**Status:** {selected_claim['status']}")

                alternative_needs = []
                alternative_labels = []
                if related_session is not None:
                    for n in needs:
                        if n["session_id"] == related_session["session_id"]:
                            remaining = int(n["quantity_needed"]) - int(n["quantity_claimed"])
                            if remaining > 0 or n["need_id"] == selected_claim["need_id"]:
                                alternative_needs.append(n)
                                alternative_labels.append(f"{n['item_name']} | {remaining} left | {n['need_id']}")

                if len(alternative_labels) > 0:
                    selected_new_need_label = st.selectbox("Update your claimed item", alternative_labels, key=f"update_claim_selectbox_{selected_claim_id}")
                    selected_new_need_id = selected_new_need_label.split(" | ")[-1]

                    selected_new_need = None
                    for n in needs:
                        if n["need_id"] == selected_new_need_id:
                            selected_new_need = n
                            break

                    manage_col1, manage_col2 = st.columns(2)
                    with manage_col1:
                        if st.button("Update Claim", type="primary", use_container_width=True, key=f"update_claim_button_{selected_claim_id}"):
                            if selected_new_need_id == selected_claim["need_id"]:
                                st.info("That is already your current claimed item.")
                            else:
                                old_need = None
                                for n in needs:
                                    if n["need_id"] == selected_claim["need_id"]:
                                        old_need = n
                                        break

                                remaining_new = int(selected_new_need["quantity_needed"]) - int(selected_new_need["quantity_claimed"])
                                if remaining_new <= 0:
                                    st.warning("That item is no longer available.")
                                else:
                                    if old_need is not None:
                                        old_need["quantity_claimed"] = int(old_need["quantity_claimed"]) - 1
                                    selected_new_need["quantity_claimed"] = int(selected_new_need["quantity_claimed"]) + 1
                                    selected_claim["need_id"] = selected_new_need["need_id"]
                                    selected_claim["claimed_item"] = selected_new_need["item_name"]
                                    needs_path.write_text(json.dumps(needs, indent=4), encoding="utf-8")
                                    claims_path.write_text(json.dumps(claims, indent=4), encoding="utf-8")
                                    st.success("Claim updated successfully.")
                                    st.rerun()
                    with manage_col2:
                        if st.button("Delete Claim", use_container_width=True, key=f"delete_claim_button_{selected_claim_id}"):
                            old_need = None
                            for n in needs:
                                if n["need_id"] == selected_claim["need_id"]:
                                    old_need = n
                                    break
                            if old_need is not None and int(old_need["quantity_claimed"]) > 0:
                                old_need["quantity_claimed"] = int(old_need["quantity_claimed"]) - 1
                            claims = [c for c in claims if c["claim_id"] != selected_claim_id]
                            needs_path.write_text(json.dumps(needs, indent=4), encoding="utf-8")
                            claims_path.write_text(json.dumps(claims, indent=4), encoding="utf-8")
                            st.session_state.selected_claim_id = ""
                            st.success("Claim deleted successfully.")
                            st.rerun()

    with tab2:
        caption_col1, caption_col2 = st.columns([3, 1])
        with caption_col1:
            st.caption("Try: What did I sign up to bring? What sessions still need items? Which sessions are open?")
        with caption_col2:
            if st.button("Clear Chat", use_container_width=True, key="clear_contrib_chat"):
                st.session_state.chat_messages = [
                    {
                        "role": "assistant",
                        "content": "Hi! I can answer simple questions like: What sessions still need items? What did I sign up to bring? Which sessions are open?"
                    }
                ]
                st.rerun()

        with st.container(border=True, height=300):
            for msg in st.session_state.chat_messages:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

        contributor_question = st.chat_input("Ask about your contributions...", key="contrib_chat_input")
        if contributor_question:
            st.session_state.chat_messages.append({"role": "user", "content": contributor_question})
            lower_prompt = contributor_question.strip().lower()
            reply = "I could not find an answer for that. Try one of the suggested questions."

            if "what did i sign up to bring" in lower_prompt or "my contributions" in lower_prompt:
                my_answer_lines = []
                for c in claims:
                    if c["contributor_id"] == st.session_state.user_id:
                        session_title = "Unknown Session"
                        for s in sessions:
                            if s["session_id"] == c["session_id"]:
                                session_title = s["title"]
                        my_answer_lines.append(f"{c['claimed_item']} for {session_title}")
                if len(my_answer_lines) == 0:
                    reply = "You have not claimed any items yet."
                else:
                    reply = "You signed up to bring:\n\n" + "\n".join(my_answer_lines)

            elif "what sessions still need items" in lower_prompt or "sessions still need items" in lower_prompt:
                answer_lines = []
                for s in sessions:
                    if s["status"] == "Open":
                        missing_list = []
                        for n in needs:
                            if n["session_id"] == s["session_id"]:
                                remaining_qty = int(n["quantity_needed"]) - int(n["quantity_claimed"])
                                if remaining_qty > 0:
                                    missing_list.append(f"{n['item_name']} ({remaining_qty} left)")
                        if len(missing_list) > 0:
                            answer_lines.append(f"{s['title']}: " + ", ".join(missing_list))
                if len(answer_lines) == 0:
                    reply = "No open sessions currently need items."
                else:
                    reply = "Here are the sessions that still need items:\n\n" + "\n".join(answer_lines)

            elif "open sessions" in lower_prompt or "which sessions are open" in lower_prompt:
                open_titles = []
                for s in sessions:
                    if s["status"] == "Open":
                        open_titles.append(s["title"])
                if len(open_titles) == 0:
                    reply = "There are no open sessions right now."
                else:
                    reply = "Open sessions:\n\n" + "\n".join(open_titles)

            elif "help" in lower_prompt:
                reply = "Try asking: What did I sign up to bring? What sessions still need items? Which sessions are open?"

            st.session_state.chat_messages.append({"role": "assistant", "content": reply})
            st.rerun()

# ==========================================================
# SAFETY FALLBACK
# ==========================================================
else:
    st.markdown("# Campus Collab")
    st.info("Use the sidebar to continue.")
