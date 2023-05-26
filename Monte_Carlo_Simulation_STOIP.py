import streamlit as st
import numpy as np
import pandas as pd
import plotly
import plotly.express as px

st.title('Monte Carlo Simulation for STOIP')
st.write('There will be explanation of Monte Carlo works here')

# Input parameters
GRV = st.number_input('Enter Gross Rock Volume in acre-ft', value=1000)
NTG = st.number_input('Enter Net to Gross Ratio', value=0.8)

NRV = GRV * NTG

PHI = st.number_input('Enter Porosity in fraction', value=0.2)
SW = st.number_input('Enter Water Saturation in fraction', value=0.2)
Bo = st.number_input('Enter Oil Formation Volume Factor in bbl/STB', value=1.2)
RF = st.number_input('Enter Recovery Factor in fraction', value=0.2)

# Generating normal distributions for each parameter
NRV_dist = np.random.normal(NRV, 0.1*NRV, 100000)
PHI_dist = np.clip(np.random.normal(PHI, 0.1*PHI, 100000),0,1)
SW_dist = np.clip(np.random.normal(SW, 0.1*SW, 100000),0,1)
Bo_dist = np.clip(np.random.normal(Bo, 0.1*Bo, 100000),0.8,1.2)
RF_dist = np.clip(np.random.normal(RF, 0.1*RF, 100000),0,1)

# Calculate STOIP using Monte Carlo Simulation and distribution values
STOIP_dist = NRV_dist * PHI_dist * (1 - SW_dist) / Bo_dist * RF_dist

# Calculate P10, P50, P90
P10 = np.percentile(STOIP_dist, 10)
P50 = np.percentile(STOIP_dist, 50)
P90 = np.percentile(STOIP_dist, 90)

# Calculate Deterministic STOIP
STOIP_det = NRV * PHI * (1 - SW) / Bo * RF

st.write('STOIP distribution')
fig = px.histogram(STOIP_dist, nbins=100)
st.plotly_chart(fig)

st.write('STOIP summary')
st.write('P10 =', P10, 'STB')
st.write('P50 =', P50, 'STB')
st.write('P90 =', P90, 'STB')
st.write('Deterministic STOIP =', STOIP_det, 'STB')

# calculate the error between deterministic and P50
error = (P50 - STOIP_det) / STOIP_det * 100
st.write('Error between deterministic and P50 =', error, '%')

# done by Elnur