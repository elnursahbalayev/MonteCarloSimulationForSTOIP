import streamlit as st
import numpy as np
import plotly.express as px

st.title('Monte Carlo Simulation for STOIP')
st.write('There will be explanation of Monte Carlo works here')

# Input parameters
GRV = st.number_input('Enter Gross Rock Volume in acre-ft', value=1000)
NTG = st.number_input('Enter Net to Gross Ratio', value=0.8)

NRV = GRV * NTG

PHI = st.number_input('Enter Porosity in fraction', value=0.2)
SW = st.number_input('Enter Water Saturation in fraction', value=0.2)
Bo_lower = st.number_input('Enter Oil Formation Volume Factor in bbl/STB lower value', value=1)
Bo_upper = st.number_input('Enter Oil Formation Volume Factor in bbl/STB higher value', value=1.7)
RF_lower = st.number_input('Enter Recovery Factor in fraction lower value', value=0.1)
RF_upper = st.number_input('Enter Recovery Factor in fraction higher value', value=0.9)

# Generating normal distributions for each parameter
NRV_dist = np.random.normal(NRV, 0.1*NRV, 100000)
PHI_dist = np.clip(np.random.normal(PHI, 0.1*PHI, 100000),0,1)
SW_dist = np.random.triangular(0,SW, 1, 100000) # TRIANGULAR
Bo_dist = np.random.uniform(Bo_lower, Bo_upper, 100000) # UNIFORM
RF_dist = np.random.uniform(RF_lower, RF_upper, 100000) # UNIFORM

# Calculate STOIP using Monte Carlo Simulation and distribution values
STOIP_dist = NRV_dist * PHI_dist * (1 - SW_dist) / Bo_dist * RF_dist

# Calculate P10, P50, P90
P10 = np.percentile(STOIP_dist, 10)
P50 = np.percentile(STOIP_dist, 50)
P90 = np.percentile(STOIP_dist, 90)

# Calculate Deterministic STOIP
STOIP_det = NRV * PHI * (1 - SW) / (Bo_upper+Bo_lower)/2 * (RF_lower+RF_upper)/2

st.write('STOIP distribution')
fig = px.histogram(STOIP_dist, nbins=100)
st.plotly_chart(fig)

st.write('STOIP summary')
st.write('P10 =', np.round(P10,2), 'STB')
st.write('P50 =', np.round(P50,2), 'STB')
st.write('P90 =', np.round(P90,2), 'STB')
st.write('Deterministic STOIP =', np.round(STOIP_det,2), 'STB')

# calculate the error between deterministic and P50
error = (P50 - STOIP_det) / STOIP_det * 100
st.write('Error between deterministic and P50 =', np.round(error,2), '%')

# done by Elnur