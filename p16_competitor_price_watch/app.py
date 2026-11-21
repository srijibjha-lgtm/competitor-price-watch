"""Competitor & Pricing Watch Agent — run with:  streamlit run p16_competitor_price_watch/app.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "..", "common")]

import pandas as pd
import streamlit as st

import core
from ui import get_queue, render_audit, render_queue, show_trace, sidebar_llm

st.set_page_config(page_title="Competitor & Pricing Watch Agent", layout="wide")
st.title("🏷️ Competitor & Pricing Watch Agent · Brewmate")
st.caption("The model reads messy competitor pages; code verifies every quote and price. The agent proposes a response per product. "
           "Rules enforce the floor margin and the 8% weekly limit. A pricing manager approves every change.")

llm, approver = sidebar_llm()
DATA_DIR = os.path.join(HERE, "data")
data = core.load_data(DATA_DIR)
queue = get_queue(os.path.join(DATA_DIR, "audit_log.jsonl"))

tab_cat, tab_pages, tab_run, tab_queue, tab_audit, tab_policy = st.tabs(
    ["Our catalogue", "Competitor pages", "Run the watch", "Approval queue", "Audit log", "Pricing policy"])

with tab_cat:
    st.dataframe(data["catalogue"].reset_index()[["sku", "name", "our_price", "cost", "floor_margin_pct", "floor_price",
                                                   "weekly_units", "stock"]], width="stretch", hide_index=True)

with tab_pages:
    week = st.radio("Week", ["week2", "week1"], horizontal=True)
    for comp in core.COMPETITORS:
        with st.expander(f"{comp} · {week}", expanded=(comp == "brewbazaar" and week == "week2")):
            st.code(data["snapshots"][(week, comp)])

with tab_run:
    if st.button("Run the weekly watch", type="primary", disabled=llm is None):
        with st.spinner("Reading pages, verifying offers and proposing prices…"):
            st.session_state["watch"] = core.run_watch(llm, data, queue)
    if "watch" in st.session_state:
        results, snaps = st.session_state["watch"]
        rows = [{"page": f"{w}/{c}", "verified": len(s["offers"]), "rejected": len(s["rejected"]),
                 "AI-instruction signals": ", ".join(s["injection"])} for (w, c), s in snaps.items()]
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
        for r in results:
            c, imp, e = r["choice"] or {}, r["impact"] or {}, r["exposure"]
            with st.container(border=True):
                st.markdown(f"**{e['sku']} {e['name']}** · ours ₹{e['our_price']:,} · cheapest {e['cheapest']['competitor']} "
                            f"₹{e['cheapest']['effective_price']:,} (gap {e['gap_pct']}%)")
                st.markdown(f"Proposal: **{c.get('action')}** at ₹{imp.get('new_price')} · margin {imp.get('margin_now_pct')}% → {imp.get('margin_after_pct')}%")
                st.write(c.get("reason", ""))
                st.caption(f"Weekly gross-margin change at the same volume: ₹{imp.get('weekly_gross_margin_change_inr_at_same_volume')}")
                for p in r["problems"]:
                    st.warning(p)
                show_trace(r["agent"]["trace"])

with tab_queue:
    render_queue(queue, approver, executors={"price_change": core.apply_price_change(DATA_DIR)})

with tab_audit:
    render_audit(queue)

with tab_policy:
    st.markdown(data["policy"])
