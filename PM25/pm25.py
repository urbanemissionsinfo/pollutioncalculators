import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="PM2.5 calculator")
# PM2.5 Emission Factor (g/kg bricks)    
st.title("India | PM 2.5 Sector wise emissions and interventions")
tab1, tab2, tab3 = st.tabs(["Energy", "Bricks", "Waste"])

with tab1:
    st.write("Current PM2.5 emissions at 1295 BUs fired by CFPPs: **228 - 317 kilo Tonnes**")
    pmef_cfpp_lower = 49 #tons/PJ
    pmef_cfpp_upper = 68 #tons/PJ
    total_electricity = st.number_input(
                        label="Total number of units produced (in Billion Units)",
                        label_visibility="visible",
                        value=1717,
                        step=10,
                        help="1717 BU produced in 2023-24 FY | 2440 BU by 2029-30")
        
    col1, col2= st.columns(2)
    # Sliders to input the percentage for each technology (displayed in columns)
    
    with col1:
        st.subheader("Intervention 1 - Replace Coal with non-fossil sources")
        cfpp_percentage = st.slider("Units produced by Coal Fired Powerplants (CFPPs) (%)", 0, 100, 75)
        cfpp_electricity = cfpp_percentage*total_electricity/100 #BUs
        coal_burnt = cfpp_electricity* 10**9 *0.666 #kg
        coal_burnt = (coal_burnt/100 + coal_burnt)/1000000000 #Million Tonnes
        st.write("CFPPs produced **{}** BUs of electricity by burning **{}** Million Tonnes of Coal".format(round(cfpp_electricity),
                                                                                            round(coal_burnt)))
        cfpp_electricity_pj = (cfpp_electricity* 10**9)/(277.788 * 10**6) #PJ
        pm25_lower = pmef_cfpp_lower*cfpp_electricity_pj / 1000 #kilo Tonnes
        pm25_upper = pmef_cfpp_upper*cfpp_electricity_pj / 1000 #kilo Tonnes
        st.write("PM2.5 emissions from CFPPs: **{}-{} kilo Tonnes**".format(round(pm25_lower),
                                                                            round(pm25_upper)))
    
    with col2:
        emission_control_dict = {"Washed Coal": 20,
                                 "FGD": 30,
                                 "Upgraded ESP":99.4} #Ref case - ESP - 97
        st.subheader("Intervention 2 - Emission Control Technologies in CFPPs")
        techniques = st.multiselect(
            "Emission Control Techniques",
            emission_control_dict.keys(),
            ["Washed Coal"],
        )

        pm25_actual_lower = pm25_lower/0.03 #kT - Without even the ESPs
        pm25_actual_upper = pm25_upper/0.03 #kT - Without even the ESPs
        if "Upgraded ESP" not in techniques:
            pm25_reduced_lower = pm25_actual_lower*(1-0.97)
            pm25_reduced_upper = pm25_actual_upper*(1-0.97)
        else:
            pm25_reduced_lower = pm25_actual_lower #Upgraded ESP reduction added below
            pm25_reduced_upper = pm25_actual_upper  #Upgraded ESP reduction added below

        for technique in techniques:
            pm25_reduced_lower = pm25_reduced_lower*(1-emission_control_dict[technique]/100)
            pm25_reduced_upper = pm25_reduced_upper*(1-emission_control_dict[technique]/100)
        st.write("PM2.5 emissions from CFPPs after Emission Control: **{}-{} kilo Tonnes**".format(round(pm25_reduced_lower),
                                                                                               round(pm25_reduced_upper)))
 
    col1, col2= st.columns(2)
    with col1:
        st.subheader("Intervention 3 - Replace Coal with Gas")
        pm_gas_ef = 121.6 #kg/MMSCM
        gas_percentage = st.slider("Percentage of Coal based electricity replaced with Gas",0,100,10)
        gas_electricity = cfpp_electricity*gas_percentage/100 #BUs
        cfpp_electricity_rem =(cfpp_electricity - gas_electricity)* 10**9 #Units
        gas_required = (gas_electricity*10**9/1000000)/5 #MMSC
        cfpp_electricity_pj =cfpp_electricity_rem/(277.788 * 10**6) #PJ
        pm_cfpp_l = pmef_cfpp_lower*cfpp_electricity_pj / 1000 #kilo Tonnes
        pm_cfpp_u = pmef_cfpp_upper*cfpp_electricity_pj / 1000 #kilo Tonnes
        pm_gas = pm_gas_ef*gas_required /1000000 #kiloTonne
        pml = round(pm_cfpp_l + pm_gas)
        pmu = round(pm_cfpp_u + pm_gas)
        st.write("PM2.5 emissions from CFPPs + Gas: **{}-{} Kilo Tonnes**".format(pml, pmu))

    with col2:
        st.subheader("Intervention 4: Blend imported coal")
        blending_ratio = st.slider("Blending Ratio", 0,30,6)/100
        sp = 0.666 #Specific Energy CEA
        spi = 0.45 #Specific Energy - Imports
        spd = (0.94*sp*spi/(spi-0.06*sp)) #Specific Energy - Domestic consndering the present 6% blending
        sp = (spi*spd)/(blending_ratio*(spd-spi) + spi)
        coal_required=(cfpp_electricity* 10**9)*sp/1000 #Tonnes
        coal_required = (coal_required/100 +coal_required) # Tonnes - Transportation losses added
        
        pm_emission_factor_lower = pm25_reduced_lower/coal_burnt #kg/Tonne Coa
        pm_emission_factor_upper = pm25_reduced_upper/coal_burnt #kg/Tonne Coa

        pm_l = round(pm_emission_factor_lower*coal_required /1000000)
        pm_u = round(pm_emission_factor_upper*coal_required /1000000)
        st.write("PM2.5 emissions from CFPPs after Emission Control and blending:**{}-{} Kilo Tonnes**".format(pm_l, pm_u))

        




    # Show the dataframe
    st.subheader("Appendix")
    st.write("PM2.5 Emission Factors for the CFPPs in India: 49-68 tons/PJ")


with tab2:
    pmef_fcbtk  = 0.18 #g/kg bricks
    pmef_clamp = 1 #g/kg bricks
    pmef_zzk = 0.6*pmef_fcbtk
    brick_weight = 3.5 #kgs

        
    col1, col2, col3 = st.columns(3)
    # Sliders to input the percentage for each technology (displayed in columns)
    with col1:
        total_bricks = st.number_input(
                        label="Total number of bricks produced (in Billions)",
                        label_visibility="visible",
                        value=233,
                        step=1)
        fcbtk_percentage = st.slider(" Bricks produced by FCBTKs (%)", 0, 100, 74)

    with col2:
        st.subheader("Intervention 1: Unclamping bricks sector")
        clamps_percentage = st.slider("Bricks produced by Clamps (%)", 0, 100, 21)

    with col3:
        st.subheader("Intervention 2: Transition FCBTKs to Zigzag kilns")
        zzk_percentage = st.slider("Bricks produced by ZZKs (%)", 0, 100, 5)


    # Ensure the total percentages add up to 100
    if fcbtk_percentage + clamps_percentage + zzk_percentage != 100:
        st.warning("The percentages for all technologies must add up to 100%. Please adjust the sliders.")
    else:
        # Calculate the number of bricks produced by each technology
        fcbtk_bricks = (fcbtk_percentage / 100) * total_bricks
        clamps_bricks = (clamps_percentage / 100) * total_bricks
        zzk_bricks = (zzk_percentage / 100) * total_bricks

        with col1:
            st.write(f"FCBTK Bricks: {fcbtk_bricks:.0f} Billion bricks")
            pm25_fcbtk = round(fcbtk_bricks*brick_weight*pmef_fcbtk) #Kilo Tonnes
            st.write("PM2.5 emissions from FCBTKs: {} Kilo Tonnes".format(pm25_fcbtk))

        with col2:
            st.write(f"Clamps Bricks: {clamps_bricks:.0f} Billion bricks")
            pm25_clamp = round(clamps_bricks*brick_weight*pmef_clamp) #Kilo Tonnes
            st.write("PM2.5 emissions from Clamps: {} Kilo Tonnes".format(pm25_clamp))

            st.subheader("Intervention 3: Co-fire coal in FCBTKs with biomass pellets")
            replace_coal = st.slider("Replace coal in FCBTKs with biomass pellets (%)", 0, 100, 0)/100
            coal = fcbtk_bricks/6.6571428571428575 #MT
            coal_reduced = coal*(1-replace_coal)
            coal_pmef = 3.03 #g/kg coal 

            biomass = fcbtk_bricks/9.32 #MT
            biomass_increased = biomass*(1+replace_coal)
            biomass_pmef = coal_pmef*0.54 #g/kg biomass 
            pm25_after_cofire = (coal_pmef*coal_reduced) + (biomass_pmef*biomass_increased)#kilotons
            st.write(coal_reduced)
            st.write(biomass_increased)
            st.write("PM2.5 emissions from FCBTKs after cofiring: {} Kilo Tonnes".format(round(pm25_after_cofire)))

        with col3:
            st.write(f"ZZKs Bricks: {zzk_bricks:.0f} Billion bricks")
            pm25_zzk = round(zzk_bricks*brick_weight*pmef_zzk) #Kilo Tonnes
            st.write("PM2.5 emissions from ZZKs: {} Kilo Tonnes".format(pm25_zzk))

            total_pm25 = round(pm25_after_cofire + pm25_clamp + pm25_zzk)
            if total_pm25 < 284:
                delta_text = "{} % less than business as usual".format(round(total_pm25/2.84 - 100)),
            else:
                delta_text = "{} % more than business as usual".format(round(total_pm25/2.84 - 100)),
            st.subheader("Total PM2.5 Emissions")
            st.metric(
                    label="Total PM2.5 Emissions",
                    label_visibility="collapsed",
                    value="{} kilo Tonnes".format(total_pm25),
                    delta=delta_text[0],
                    delta_color="inverse",
                    help="Business as usual= 74+21+5 = 284 kT"
                )


    data = {
        "Technology": ["FCBTK", "Clamps", "ZZKs"],
        "PM2.5 Emission Factor (g/kg bricks)": [pmef_fcbtk,pmef_clamp, pmef_zzk],
    }

    df = pd.DataFrame(data)

    # Show the dataframe
    st.subheader("Appendix")
    st.dataframe(df)



