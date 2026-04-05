
import streamlit as st
import json
from pathlib import Path
from datetime import datetime, date
import uuid

st.set_page_config(page_title="Campus Collab MVP", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None
if "role" not in st.session_state:
    st.session_state["role"] = ""
if "page" not in st.session_state:
    st.session_state["page"] = "welcome"
if "selected_session_id" not in st.session_state:
    st.session_state["selected_session_id"] = ""
if "selected_claim_id" not in st.session_state:
    st.session_state["selected_claim_id"] = ""

users_path = Path("users.json")
sessions_path = Path("sessions.json")
needs_path = Path("needs.json")
claims_path = Path("claims.json")

if not users_path.exists():
    users_path.write_text(json.dumps([
        {
            "user_id": "host-1",
            "full_name": "Demo Host",
            "email": "host@udel.edu",
            "password": "host123",
            "role": "Host",
            "registered_at": str(datetime.now())
        },
        {
            "user_id": "contrib-1",
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
            "host_id": "host-1",
            "title": "MISY350 Study Night",
            "date": str(date.today()),
            "location": "Morris Library",
            "description": "Come study and bring one helpful item.",
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
            "quantity_claimed": 0
        },
        {
            "need_id": "need-2",
            "session_id": "session-1",
            "item_name": "Practice Questions",
            "quantity_needed": 3,
            "quantity_claimed": 0
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

with st.sidebar:
    st.markdown("## Campus Collab MVP")

    if st.session_state["logged_in"]:
        st.success(f"Logged in as {st.session_state['user']['full_name']}")
        st.caption(f"Role: {st.session_state['role']}")

        if st.session_state["role"] == "Host":
            if st.button("Host Dashboard", use_container_width=True, key="host_dash_btn"):
                st.session_state["page"] = "host_dashboard"
                st.rerun()
            if st.button("Create Session", use_container_width=True, key="create_session_btn"):
                st.session_state["page"] = "create_session"
                st.rerun()

        if st.session_state["role"] == "Contributor":
            if st.button("Contributor Dashboard", use_container_width=True, key="contrib_dash_btn"):
                st.session_state["page"] = "contributor_dashboard"
                st.rerun()
            if st.button("Browse Sessions", use_container_width=True, key="browse_sessions_btn"):
                st.session_state["page"] = "browse_sessions"
                st.rerun()
            if st.button("My Claims", use_container_width=True, key="my_claims_btn"):
                st.session_state["page"] = "my_claims"
                st.rerun()

        st.divider()
        if st.button("Log Out", type="primary", use_container_width=True, key="logout_btn"):
            st.session_state["logged_in"] = False
            st.session_state["user"] = None
            st.session_state["role"] = ""
            st.session_state["page"] = "welcome"
            st.session_state["selected_session_id"] = ""
            st.session_state["selected_claim_id"] = ""
            st.rerun()

    else:
        if st.button("Welcome", use_container_width=True, key="welcome_btn"):
            st.session_state["page"] = "welcome"
            st.rerun()
        if st.button("Register", use_container_width=True, key="register_btn_nav"):
            st.session_state["page"] = "register"
            st.rerun()
        if st.button("Log In", use_container_width=True, key="login_btn_nav"):
            st.session_state["page"] = "login"
            st.rerun()

if st.session_state["logged_in"] == False and st.session_state["page"] == "welcome":
    st.title("Campus Collab MVP")
    st.write("A simple app for campus study sessions and contribution tracking.")

    open_count = 0
    for s in sessions:
        if s["status"] == "Open":
            open_count += 1

    col1, col2, col3 = st.columns(3)
    col1.metric("Open Sessions", open_count)
    col2.metric("Users", len(users))
    col3.metric("Claims", len(claims))

    with st.container(border=True):
        st.markdown("### How it works")
        st.write("Hosts create study sessions and list items they need.")
        st.write("Contributors browse sessions and claim one item to bring.")

    with st.container(border=True):
        st.markdown("### Demo Accounts")
        st.write("Host: host@udel.edu / host123")
        st.write("Contributor: student@udel.edu / student123")

elif st.session_state["logged_in"] == False and st.session_state["page"] == "register":
    st.title("Register")
    with st.container(border=True):
        new_name = st.text_input("Full Name", key="reg_name")
        new_email = st.text_input("Email", key="reg_email")
        new_password = st.text_input("Password", type="password", key="reg_password")
        new_role = st.selectbox("Role", ["Select a role", "Host", "Contributor"], key="reg_role")

        if st.button("Create Account", type="primary", use_container_width=True, key="create_account_btn"):
            duplicate_email = False
            for user in users:
                if user["email"].strip().lower() == new_email.strip().lower():
                    duplicate_email = True

            if new_name.strip() == "" or new_email.strip() == "" or new_password.strip() == "" or new_role == "Select a role":
                st.warning("All fields are required.")
            elif duplicate_email:
                st.error("That email is already registered.")
            else:
                users.append({
                    "user_id": str(uuid.uuid4()),
                    "full_name": new_name.strip(),
                    "email": new_email.strip().lower(),
                    "password": new_password,
                    "role": new_role,
                    "registered_at": str(datetime.now())
                })
                users_path.write_text(json.dumps(users, indent=4), encoding="utf-8")
                st.success("Account created.")
                st.session_state["page"] = "login"
                st.rerun()

elif st.session_state["logged_in"] == False and st.session_state["page"] == "login":
    st.title("Log In")
    with st.container(border=True):
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")

        if st.button("Log In", type="primary", use_container_width=True, key="login_submit_btn"):
            found_user = None
            for user in users:
                if user["email"].strip().lower() == login_email.strip().lower() and user["password"] == login_password:
                    found_user = user
                    break

            if login_email.strip() == "" or login_password.strip() == "":
                st.warning("Email and password are required.")
            elif found_user is None:
                st.error("Invalid credentials.")
            else:
                st.session_state["logged_in"] = True
                st.session_state["user"] = found_user
                st.session_state["role"] = found_user["role"]
                st.session_state["selected_session_id"] = ""
                st.session_state["selected_claim_id"] = ""
                if found_user["role"] == "Host":
                    st.session_state["page"] = "host_dashboard"
                else:
                    st.session_state["page"] = "contributor_dashboard"
                st.rerun()

elif st.session_state["logged_in"] and st.session_state["role"] == "Host" and st.session_state["page"] == "host_dashboard":
    st.title("Host Dashboard")

    my_sessions = []
    for session in sessions:
        if session["host_id"] == st.session_state["user"]["user_id"]:
            my_sessions.append(session)

    total_claims = 0
    for session in my_sessions:
        for claim in claims:
            if claim["session_id"] == session["session_id"]:
                total_claims += 1

    col1, col2 = st.columns(2)
    col1.metric("My Sessions", len(my_sessions))
    col2.metric("Claims on My Sessions", total_claims)

    if len(my_sessions) == 0:
        st.info("You have not created any sessions yet.")
    else:
        table_rows = []
        for session in my_sessions:
            table_rows.append({
                "Title": session["title"],
                "Date": session["date"],
                "Location": session["location"],
                "Status": session["status"]
            })
        st.dataframe(table_rows, use_container_width=True)

        session_options = []
        for session in my_sessions:
            session_options.append(f"{session['title']} | {session['session_id']}")

        selected_label = st.selectbox("Select a session", session_options, key="host_selected_session")
        selected_session_id = selected_label.split(" | ")[-1]
        st.session_state["selected_session_id"] = selected_session_id

        selected_session = None
        for session in sessions:
            if session["session_id"] == selected_session_id:
                selected_session = session
                break

        if selected_session:
            with st.container(border=True):
                st.markdown(f"### {selected_session['title']}")
                st.write(f"**Date:** {selected_session['date']}")
                st.write(f"**Location:** {selected_session['location']}")
                st.write(f"**Description:** {selected_session['description']}")
                st.write(f"**Status:** {selected_session['status']}")

            edit_title = st.text_input("Edit Title", value=selected_session["title"], key="edit_title")
            edit_location = st.text_input("Edit Location", value=selected_session["location"], key="edit_location")
            edit_description = st.text_area("Edit Description", value=selected_session["description"], key="edit_description")
            edit_status = st.selectbox("Edit Status", ["Open", "Closed"], index=0 if selected_session["status"] == "Open" else 1, key="edit_status")

            col_upd, col_del = st.columns(2)
            with col_upd:
                if st.button("Update Session", type="primary", use_container_width=True, key="update_session_btn"):
                    if edit_title.strip() == "" or edit_location.strip() == "":
                        st.warning("Title and location are required.")
                    else:
                        selected_session["title"] = edit_title.strip()
                        selected_session["location"] = edit_location.strip()
                        selected_session["description"] = edit_description.strip()
                        selected_session["status"] = edit_status
                        sessions_path.write_text(json.dumps(sessions, indent=4), encoding="utf-8")
                        st.success("Session updated.")
                        st.rerun()

            with col_del:
                if st.button("Delete Session", use_container_width=True, key="delete_session_btn"):
                    sessions = [s for s in sessions if s["session_id"] != selected_session_id]
                    needs = [n for n in needs if n["session_id"] != selected_session_id]
                    claims = [c for c in claims if c["session_id"] != selected_session_id]
                    sessions_path.write_text(json.dumps(sessions, indent=4), encoding="utf-8")
                    needs_path.write_text(json.dumps(needs, indent=4), encoding="utf-8")
                    claims_path.write_text(json.dumps(claims, indent=4), encoding="utf-8")
                    st.success("Session deleted.")
                    st.rerun()

elif st.session_state["logged_in"] and st.session_state["role"] == "Host" and st.session_state["page"] == "create_session":
    st.title("Create Session")
    with st.container(border=True):
        title = st.text_input("Session Title", key="new_title")
        session_date = st.date_input("Date", value=date.today(), key="new_date")
        location = st.text_input("Location", key="new_location")
        description = st.text_area("Description", key="new_description")
        need_item = st.text_input("Needed Item", key="new_need_item")
        need_quantity = st.number_input("Needed Quantity", min_value=1, step=1, key="new_need_quantity")

        if st.button("Save Session", type="primary", use_container_width=True, key="save_session_btn"):
            if title.strip() == "" or location.strip() == "" or need_item.strip() == "":
                st.warning("Title, location, and needed item are required.")
            else:
                new_session_id = str(uuid.uuid4())
                sessions.append({
                    "session_id": new_session_id,
                    "host_id": st.session_state["user"]["user_id"],
                    "title": title.strip(),
                    "date": str(session_date),
                    "location": location.strip(),
                    "description": description.strip(),
                    "status": "Open",
                    "created_at": str(datetime.now())
                })
                needs.append({
                    "need_id": str(uuid.uuid4()),
                    "session_id": new_session_id,
                    "item_name": need_item.strip(),
                    "quantity_needed": int(need_quantity),
                    "quantity_claimed": 0
                })
                sessions_path.write_text(json.dumps(sessions, indent=4), encoding="utf-8")
                needs_path.write_text(json.dumps(needs, indent=4), encoding="utf-8")
                st.success("Session created.")
                st.session_state["page"] = "host_dashboard"
                st.rerun()

elif st.session_state["logged_in"] and st.session_state["role"] == "Contributor" and st.session_state["page"] == "contributor_dashboard":
    st.title("Contributor Dashboard")

    my_claims = []
    for claim in claims:
        if claim["contributor_id"] == st.session_state["user"]["user_id"]:
            my_claims.append(claim)

    open_count = 0
    for session in sessions:
        if session["status"] == "Open":
            open_count += 1

    col1, col2 = st.columns(2)
    col1.metric("My Claims", len(my_claims))
    col2.metric("Open Sessions", open_count)

    if len(my_claims) == 0:
        st.info("You have not claimed anything yet.")
    else:
        rows = []
        for claim in my_claims:
            session_title = "Unknown"
            for session in sessions:
                if session["session_id"] == claim["session_id"]:
                    session_title = session["title"]
                    break
            rows.append({
                "Session": session_title,
                "Item": claim["claimed_item"],
                "Status": claim["status"]
            })
        st.dataframe(rows, use_container_width=True)

elif st.session_state["logged_in"] and st.session_state["role"] == "Contributor" and st.session_state["page"] == "browse_sessions":
    st.title("Browse Sessions")

    open_sessions = []
    for session in sessions:
        if session["status"] == "Open":
            open_sessions.append(session)

    if len(open_sessions) == 0:
        st.warning("There are no open sessions.")
    else:
        options = []
        for session in open_sessions:
            options.append(f"{session['title']} | {session['session_id']}")

        selected_label = st.selectbox("Select a session", options, key="browse_selected_session")
        selected_session_id = selected_label.split(" | ")[-1]
        st.session_state["selected_session_id"] = selected_session_id

        selected_session = None
        for session in sessions:
            if session["session_id"] == selected_session_id:
                selected_session = session
                break

        if selected_session:
            with st.container(border=True):
                st.markdown(f"### {selected_session['title']}")
                st.write(f"**Date:** {selected_session['date']}")
                st.write(f"**Location:** {selected_session['location']}")
                st.write(f"**Description:** {selected_session['description']}")

            available_needs = []
            for need in needs:
                if need["session_id"] == selected_session_id:
                    remaining = int(need["quantity_needed"]) - int(need["quantity_claimed"])
                    if remaining > 0:
                        available_needs.append(need)

            if len(available_needs) == 0:
                st.info("This session does not need any more items.")
            else:
                need_options = []
                for need in available_needs:
                    remaining = int(need["quantity_needed"]) - int(need["quantity_claimed"])
                    need_options.append(f"{need['item_name']} ({remaining} left) | {need['need_id']}")

                selected_need_label = st.selectbox("Choose an item", need_options, key="need_to_claim")
                selected_need_id = selected_need_label.split(" | ")[-1]

                already_claimed = False
                for claim in claims:
                    if claim["need_id"] == selected_need_id and claim["contributor_id"] == st.session_state["user"]["user_id"]:
                        already_claimed = True

                if st.button("Claim Item", type="primary", use_container_width=True, key="claim_item_btn"):
                    if already_claimed:
                        st.warning("You already claimed this item.")
                    else:
                        chosen_need = None
                        for need in needs:
                            if need["need_id"] == selected_need_id:
                                chosen_need = need
                                break

                        if chosen_need:
                            chosen_need["quantity_claimed"] = int(chosen_need["quantity_claimed"]) + 1
                            claims.append({
                                "claim_id": str(uuid.uuid4()),
                                "session_id": selected_session_id,
                                "need_id": selected_need_id,
                                "contributor_id": st.session_state["user"]["user_id"],
                                "claimed_item": chosen_need["item_name"],
                                "status": "Claimed"
                            })
                            needs_path.write_text(json.dumps(needs, indent=4), encoding="utf-8")
                            claims_path.write_text(json.dumps(claims, indent=4), encoding="utf-8")
                            st.success("Item claimed.")
                            st.rerun()

elif st.session_state["logged_in"] and st.session_state["role"] == "Contributor" and st.session_state["page"] == "my_claims":
    st.title("My Claims")

    my_claims = []
    for claim in claims:
        if claim["contributor_id"] == st.session_state["user"]["user_id"]:
            my_claims.append(claim)

    if len(my_claims) == 0:
        st.info("You do not have any claims yet.")
    else:
        claim_options = []
        for claim in my_claims:
            claim_options.append(f"{claim['claimed_item']} | {claim['claim_id']}")

        selected_claim_label = st.selectbox("Select a claim", claim_options, key="selected_claim")
        selected_claim_id = selected_claim_label.split(" | ")[-1]
        st.session_state["selected_claim_id"] = selected_claim_id

        selected_claim = None
        for claim in claims:
            if claim["claim_id"] == selected_claim_id:
                selected_claim = claim
                break

        if selected_claim:
            with st.container(border=True):
                st.write(f"**Item:** {selected_claim['claimed_item']}")
                st.write(f"**Status:** {selected_claim['status']}")

            update_status = st.selectbox("Update Status", ["Claimed", "Canceled"], index=0 if selected_claim["status"] == "Claimed" else 1, key="update_claim_status")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Update Claim", type="primary", use_container_width=True, key="update_claim_btn"):
                    selected_claim["status"] = update_status
                    claims_path.write_text(json.dumps(claims, indent=4), encoding="utf-8")
                    st.success("Claim updated.")
                    st.rerun()

            with col2:
                if st.button("Delete Claim", use_container_width=True, key="delete_claim_btn"):
                    for need in needs:
                        if need["need_id"] == selected_claim["need_id"] and int(need["quantity_claimed"]) > 0:
                            need["quantity_claimed"] = int(need["quantity_claimed"]) - 1
                    claims = [claim for claim in claims if claim["claim_id"] != selected_claim_id]
                    needs_path.write_text(json.dumps(needs, indent=4), encoding="utf-8")
                    claims_path.write_text(json.dumps(claims, indent=4), encoding="utf-8")
                    st.success("Claim deleted.")
                    st.rerun()
