###### SMART_CALCULATOR ######

import streamlit as st
import math

Section = st.selectbox("Select Required Section",["Loan","Investment","SI"]).strip().lower()

#--------------------------------LOAN SECTION--------------------------------------#

if Section == "loan":
    Field = st.selectbox("Select Required Field",["PMT","PV","Tenure","Rate"]).strip().lower()

    if Field == "pmt":
        PV = st.number_input("Loan Amt",min_value = 0.0)
        R = st.number_input("Rate% (yearly)",min_value = 0.0)
        N = st.number_input("Time (years)",min_value = 0.0)

        # convert Rate/Tenure to monthly
        MR = R/100/12
        MN = N*12

        PMT = (PV*MR) / (1-(1+MR)**(-MN))

        st.write("### Result Section:-")
        st.write(f"Loan Amt = {PV:.2f}")
        st.write(f"Rate% (yearly) = {R:.2f}")
        st.write(f"Tenure (years) = {N:.2f}")
        st.write(f"PMT (monthly) = {PMT:.2f}")
        
    elif Field == "pv":
        PMT = st.number_input("PMT (monthly)",min_value = 0.0)
        R = st.number_input("Rate% (yearly)",min_value = 0.0)
        N = st.number_input("Time (years)",min_value = 0.0)

        # convert Rate/Tenure to monthly
        MR = R/100/12
        MN = N*12

        PV = (PMT*(1-(1+MR)**(-MN))) / MR

        st.write("### Result Section:-")
        st.write(f"Loan Amt = {PV:.2f}")
        st.write(f"Rate% (yearly) = {R:.2f}")
        st.write(f"Tenure (years) = {N:.2f}")
        st.write(f"PMT (monthly) = {PMT:.2f}")
        
    elif Field == "tenure":
        PV = st.number_input("Loan Amt",min_value = 0.0)
        R = st.number_input("Rate% (yearly)",min_value = 0.0)
        PMT = st.number_input("PMT (monthly)",min_value = 0.0)

        # conver rate to monthly
        MR = R/100/12

        if PMT <= PV*MR:
            st.error("PMT is too small to cover monthly interest")
            N = 0
        else:
            N = (-math.log(1-(PV*MR)/PMT) / math.log(1+MR)) / 12

        st.write("### Result Section:-")
        st.write(f"Loan Amt = {PV:.2f}")
        st.write(f"Rate% (yearly) = {R:.2f}")
        st.write(f"Tenure (years) = {N:.2f}")
        st.write(f"PMT (monthly) = {PMT:.2f}")


        
    elif Field == "rate":
        PV = st.number_input("Loan Amt",min_value = 0.0)
        PMT = st.number_input("PMT (monthly)",min_value = 0.0)
        N = st.number_input("Tenure (years)",min_value = 0.0)

        # convert tenure to years
        MN = N*12
        # assuming/guessing monthly rate-
        MR = 0.01

        # Newton-Raphson Method
        for i in range(100):
            f = (PV*MR) / (1-(1+ MR)**(-MN)) - PMT
            df = (PV * (1-(1+MR)**(-MN)) - PV*MR*MN * (1+MR)**(-MN-1)) / (1-(1+MR)**(-MN))**2       
            MR = MR - f/df        

            R = MR*12*100

        st.write("### Result Section:-")
        st.write(f"Loan Amt = {PV:.2f}")
        st.write(f"Rate% (yearly) = {R:.2f}")
        st.write(f"Tenure (years) = {N:.2f}")
        st.write(f"PMT (monthly) = {PMT:.2f}")

#----------------------------INVESTMENT SECTION------------------------------------------#

elif Section == "investment":
    Field = st.selectbox("Select Required Field",["PMT","FV","Tenure","Rate"]).strip().lower()

    if Field == "fv":
        PMT = st.number_input("PMT (monthly)",min_value = 0.0)
        R = st.number_input("Rate% (yearly)",min_value = 0.0)
        N = st.number_input("Tenure (years)",min_value = 0.0)

        # convert Rate/Tenure to monthly
        MR = R/100/12
        MN = N*12

        FV = PMT * (((1+MR)**MN -1) / MR)

        st.write("### Result Section:-")
        st.write(f"PMT (monthly) = {PMT:.2f}")        
        st.write(f"Rate% (yearly) = {R:.2f}")
        st.write(f"Tenure (years) = {N:.2f}")
        st.write(f"Future Value = {FV:.2f}")

    elif Field == "pmt":
        FV = st.number_input("Future value",min_value = 0.0)
        R = st.number_input("Rate% (yearly)",min_value = 0.0)
        N = st.number_input("Tenure (years)",min_value = 0.0)

        # convert Rate/Tenure to monthly
        MR = R/100/12
        MN = N*12

        PMT = FV / (((1+MR)**MN -1) / MR)

        st.write("### Result Section:-")
        st.write(f"Future Value = {FV:.2f}")
        st.write(f"Rate% (yearly) = {R:.2f}")
        st.write(f"Tenure (years) = {N:.2f}")
        st.write(f"PMT (monthly) = {PMT:.2f}")

    elif Field == "tenure":
        FV = st.number_input("Future Value",min_value = 0.0)
        R = st.number_input("Rate% (yearly)",min_value = 0.0)
        PMT = st.number_input("PMT (monthly)",min_value = 0.0)

        # convert Rate to monthly
        MR = R/100/12

        N = (math.log(1+(FV*MR/PMT)) / math.log(1+MR)) / 12

        st.write("### Result Section:-")
        st.write(f"Future Value = {FV:.2f}")
        st.write(f"Rate% (yearly) = {R:.2f}")
        st.write(f"PMT (monthly) = {PMT:.2f}")
        st.write(f"Tenure (years) = {N:.2f}")

    elif Field == "rate":
        FV = st.number_input("Future Value",min_value = 0.0)
        N = st.number_input("Tenure (years)",min_value = 0.0)
        PMT = st.number_input("PMT (monthly)",min_value = 0.0)

        # convert Tenure to monthly
        MN = N*12
        # assuming/guessing monthly rate-
        MR = 0.01

        # Newton-Raphson Method
        for i in range(100):
            f = PMT * (((1+MR)**MN - 1) / MR) - FV
            df = PMT * ((MR*MN*(1+MR)**(MN-1) - ((1+MR)**MN - 1)) / (MR**2))
            MR = MR - f/df

            R = MR*12*100
        
        st.write("### Result Section:-")
        st.write(f"Future Value = {FV:.2f}")
        st.write(f"Tenure (years) = {N:.2f}")
        st.write(f"PMT (monthly) = {PMT:.2f}")
        st.write(f"Rate% (yearly) = {R:.2f}")

#-------------------------------SI SECTION---------------------------------------#

elif Section == "si":
    Field = st.selectbox("Select Required Field",["SI","Rate","Tenure","P.Amt"]).strip().lower()

    if Field == "si":
        P = st.number_input("Principal Amt",min_value = 0.0)
        R = st.number_input("Rate%",min_value = 0.0)
        rate_type = st.selectbox("Rate_Type",["m","y"]).strip().lower()
        N = st.number_input("Tenure",min_value = 0.0)
        tenure_type = st.selectbox("Tenure",["m","y"]).strip().lower()

        # conver rate/time to yearly if it is monthly
        if rate_type == "m":
            R = R*12   
        if tenure_type == "m":
            N = N/12

        SI = (P*R*N)/100
        TA = P+SI
        MR = R/12
        MN = N*12

        st.write("### Result Section:-")
        st.write(f"Principal Amt= {P:.2f}")
        st.write(f"Rate% (yearly)= {R:.2f}")
        st.write(f"Rate% (monthly)= {MR:.2f}")
        st.write(f"Tenure (years)= {N:.2f}")
        st.write(f"Tenure (months)= {MN:.2f}")
        st.write(f"Interest= {SI:.2f}")
        st.write(f"Total Amt= {TA:.2f}")

    elif Field == "rate":
        P = st.number_input("Principal Amt",min_value = 0.0)
        SI = st.number_input("Interest",min_value = 0.0)
        N = st.number_input("Tenure",min_value = 0.0)
        tenure_type = st.selectbox("Tenure",["m","y"]).strip().lower()

        # convert time to years if it is in months
        if tenure_type == "m":
            N = N/12

        R = (SI*100) / (P*N)
        TA = P+SI
        MR = R/12
        MN = N*12

        st.write("### Result Section:-")
        st.write(f"Principal Amt= {P:.2f}")
        st.write(f"Rate% (yearly)= {R:.2f}")
        st.write(f"Rate% (monthly)= {MR:.2f}")
        st.write(f"Tenure (years)= {N:.2f}")
        st.write(f"Tenure (months)= {MN:.2f}")
        st.write(f"Interest= {SI:.2f}")
        st.write(f"Total Amt= {TA:.2f}")

    elif Field == "tenure":
        P = st.number_input("Principal Amt",min_value = 0.0)
        SI = st.number_input("Interest",min_value = 0.0)
        R = st.number_input("Rate",min_value = 0.0)
        rate_type = st.selectbox("Rate_Type",["m","y"]).strip().lower()

        # conver rate to yearly if it is monthly
        if rate_type == "m":
            R = R*12

        N = (SI*100) / (P*R)
        TA = P+SI
        MR = R/12
        MN = N*12

        st.write("### Result Section:-")
        st.write(f"Principal Amt= {P:.2f}")
        st.write(f"Rate% (yearly)= {R:.2f}")
        st.write(f"Rate% (monthly)= {MR:.2f}")
        st.write(f"Tenure (years)= {N:.2f}")
        st.write(f"Tenure (months)= {MN:.2f}")
        st.write(f"Interest= {SI:.2f}")
        st.write(f"Total Amt= {TA:.2f}")

    elif Field == "p.amt":
        R = st.number_input("Rate%",min_value = 0.0)
        rate_type = st.selectbox("Rate_Type",["m","y"]).strip().lower()
        N = st.number_input("Tenure",min_value = 0.0)
        tenure_type = st.selectbox("Tenure_Type",["m","y"]).strip().lower()
        SI = st.number_input("Interest",min_value = 0.0)

        # convert rate/time to yearly if it is monthly
        if rate_type == "m":
            R = R*12        
        if tenure_type == "m":
            N = N/12

        P = (SI*100) / (R*N)
        TA = P+SI
        MR = R/12
        MN = N*12

        st.write("### Result Section:-")
        st.write(f"Principal Amt= {P:.2f}")
        st.write(f"Rate% (yearly)= {R:.2f}")
        st.write(f"Rate% (monthly)= {MR:.2f}")
        st.write(f"Tenure (years)= {N:.2f}")
        st.write(f"Tenure (months)= {MN:.2f}")
        st.write(f"Interest= {SI:.2f}")
        st.write(f"Total Amt= {TA:.2f}")
            
