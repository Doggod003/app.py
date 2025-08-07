import streamlit as st
from data_fetchers import get_tax_rates, get_insurance_premiums

st.title("State & County Tax ➔ Insurance Explorer")

state = st.text_input("Enter a state", help="e.g. Pennsylvania")

if state:
    counties = load_counties_for(state)
    county = st.selectbox("Select county", counties)
    if county:
        taxes = get_tax_rates(state, county)
        premiums = get_insurance_premiums(state, county)

        st.subheader(f"🔖 {county}, {state}")
        st.metric("Median Home Price", f"${taxes['median_price'].iloc[0]:,.0f}")
        st.metric("Effective Tax Rate", f"{taxes['effective_rate'].iloc[0]:.2%}")
        st.metric("Avg Insurance Premium", f"${premiums['avg_premium'].iloc[0]:,.0f}")

        st.plotly_chart(make_choropleth(taxes))
        st.dataframe(taxes)
        st.dataframe(premiums)

        if st.button("Save Snapshot"):
            save_snapshot(state, county, taxes, premiums)
            st.success("Snapshot saved!")

        st.download_button("Export CSV", data=merge(taxes, premiums).to_csv(), file_name="snapshot.csv")
        st.markdown(generate_pdf_link(state, county))

