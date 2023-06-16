import streamlit as st
import numpy as np
import plotly.express as px

st.title('Monte Carlo Simulation for STOIP')
st.write('There will be explanation of Monte Carlo works here')


input_tab, output_tab = st.tabs(['Input', 'Output'])

with input_tab:
# Input parameters
    GRV_oil = st.number_input('Enter Gross Rock Volume of oil in acre-ft', value=556448)
    GRV_gas = st.number_input('Enter Gross Rock Volume of gas in acre-ft', value=668067)

    NTG_oil = st.number_input('Enter Net to Gross Ratio of oil', value=0.34)
    NTG_gas = st.number_input('Enter Net to Gross Ratio of gas', value=0.45)

    NRV_oil = GRV_oil * NTG_oil
    NRV_gas = GRV_gas * NTG_gas

    PHI_oil = st.number_input('Enter Porosity in fraction for oil', value=0.3)
    PHI_gas = st.number_input('Enter Porosity in fraction for gas', value=0.23)

    SW_oil = st.number_input('Enter Water Saturation in fraction for oil', value=0.29)
    SW_gas = st.number_input('Enter Water Saturation in fraction for gas', value=0.24)


    Bo = st.number_input('Enter Oil Formation Volume Factor in bbl/STB', value=1.169)
    Bg = st.number_input('Enter Gas Formation Volume Factor in bbl/STB', value=0.00698)

    # Generating normal distributions for each parameter
    NRV_oil_dist = np.random.normal(NRV_oil, 0.1*NRV_oil, 100000)
    PHI_oil_dist = np.clip(np.random.normal(PHI_oil, 0.1*PHI_oil, 100000),0,1)
    SW_oil_dist = np.clip(np.random.normal(SW_oil, 0.1*SW_oil, 100000),0,1)
    Bo_dist = np.random.normal(Bo, 0.1*Bo, 100000)

    NRV_gas_dist = np.random.normal(NRV_gas, 0.1*NRV_gas, 100000)
    PHI_gas_dist = np.clip(np.random.normal(PHI_gas, 0.1*PHI_gas, 100000),0,1)
    SW_gas_dist = np.clip(np.random.normal(SW_gas, 0.1*SW_gas, 100000),0,1)
    Bg_dist = np.random.normal(Bg, 0.1*Bg, 100000)

    # Calculate STOIP using Monte Carlo Simulation and distribution values
    STOIP_dist = 7758 * NRV_oil_dist * PHI_oil_dist * (1 - SW_oil_dist) / Bo_dist
    GIIP_dist = 43560 * NRV_gas_dist * PHI_gas_dist * (1 - SW_gas_dist) / Bg_dist
    Solution_gas = STOIP_dist * 336
    GIIP_dist = GIIP_dist + Solution_gas

    # Calculate P10, P50, P90
    P90_oil = np.percentile(STOIP_dist, 10)
    P50_oil = np.percentile(STOIP_dist, 50)
    P10_oil = np.percentile(STOIP_dist, 90)

    P90_gas = np.percentile(GIIP_dist, 10)
    P50_gas = np.percentile(GIIP_dist, 50)
    P10_gas = np.percentile(GIIP_dist, 90)

    # Calculate Deterministic STOIP
    STOIP_det = 7758 * NRV_oil * PHI_oil * (1 - SW_oil) / Bo
    GIIP_det = 43560 * NRV_gas * PHI_gas * (1 - SW_gas) / Bg
    Solution_gas_det = STOIP_det * 336
    GIIP_det = GIIP_det + Solution_gas_det


with output_tab:

    col1, col2 = st.columns(2)

    with col1:

        st.write('STOIP distribution')
        fig = px.histogram(STOIP_dist, nbins=100)
        st.plotly_chart(fig)

        st.write('STOIP summary')
        st.write('P10 =', np.round(P10_oil/10**6,2), 'MSTB')
        st.write('P50 =', np.round(P50_oil/10**6,2), 'MSTB')
        st.write('P90 =', np.round(P90_oil/10**6,2), 'MSTB')
        st.write('Deterministic STOIP =', np.round(STOIP_det/10**6,2), 'MSTB')

        # calculate the error between deterministic and P50
        error = (P50_oil - STOIP_det) / STOIP_det * 100
        st.write('Error between deterministic and P50 =', np.round(error,2), '%')

    with col2:
        st.write('GIIP distribution')
        fig = px.histogram(GIIP_dist, nbins=100)
        st.plotly_chart(fig)

        st.write('GIIP summary')
        st.write('P10 =', np.round(P10_gas/10**9,2), 'BSCF')
        st.write('P50 =', np.round(P50_gas/10**9,2), 'BSCF')
        st.write('P90 =', np.round(P90_gas/10**9,2), 'BSCF')
        st.write('Deterministic GIIP =', np.round(GIIP_det/10**9,2), 'BSCF')

        # calculate the error between deterministic and P50
        error = (P50_gas - GIIP_det) / GIIP_det * 100
        st.write('Error between deterministic and P50 =', np.round(error,2), '%')

    # done by Elnur