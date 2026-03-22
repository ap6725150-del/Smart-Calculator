######   SMART CALCULATOR   #######
####  Loan|Investment|SI- DEF  ####

import streamlit as st
import pandas as pd
import math
import io

### -------- LOAN FUNCTION DEFINITION --------
def loan_table(PV, PMT, MR, MN):
    
    data = []
    balance = PV

    for month in range(1, int(MN)+1):
        IPMT = balance * MR
        PPMT = PMT - IPMT
        closing = balance - PPMT

        if closing < 0:
            PPMT += closing
            closing = 0

        data.append([month, round(balance,2), round(PMT,2), round(PPMT,2), round(IPMT,2), round(closing,2)])
        balance = closing

    df = pd.DataFrame(data, columns=["Months","Loan Amt","PMT","PPMT","IPMT","Closing Amt"])
    st.dataframe(df)

    st.write("Download Excel File Below:")
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    
    st.download_button(label = "Download Excel", data=buffer.getvalue(), file_name="Loan_EMI_Table.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

### ----- INVESTMENT FUNCTION DEFINITION -------

def policy_table(FV, PMT, MR, MN):
    
    data = []
    running_fv = 0

    for month in range(1, int(MN)+1):
        interest = running_fv * MR
        running_fv = running_fv + interest + PMT

        data.append([month, round(PMT,2), round(interest,2), round(running_fv,2)])

    df = pd.DataFrame(data, columns=["Months", "PMT", "Interest", "Future Value"])
    st.dataframe(df)

    st.write("Download Excel File Below:")
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    
    st.download_button(label = "Download Excel", data=buffer.getvalue(), file_name="Policy_EMI_Table.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

### ================ MAIN PROGRAM ================ ###

st.title("SMART CALCULATOR")

SECTION = st.selectbox("SELECT SECTION",["LOAN", "INVESTMENT", "SIMPLE INTEREST"])

# ================ LOAN SECTION =======================

if SECTION == "LOAN":
    Field = st.selectbox("Select Field",["PV", "PMT", "Tenure", "Rate"])

    if Field == "PMT":
        PV = st.number_input("Loan Amount", min_value=0.0)
        R = st.number_input("Rate % (yearly)", min_value=0.0)
        N = st.number_input("Tenure (years)", min_value=0.0)

        if st.button("Calculate PMT"):
            MR = R/100/12
            MN = N*12

            PMT = (PV*MR) / (1-(1+MR)**(-MN))

            st.subheader("Result")
            st.write(f"Loan Amt = {PV:.2f}")
            st.write(f"Rate% (yearly) = {R:.2f}")
            st.write(f"Tenure (years) = {N:.2f}")
            st.write(f"PMT (monthly) = {PMT:.2f}")

            # Loan FUNCTION CALL
            loan_table(PV, PMT, MR, MN)

    elif Field == "PV":
        PMT = st.number_input("PMT (monthly)", min_value=0.0)
        R = st.number_input("Rate % (yearly)", min_value=0.0)
        N = st.number_input("Tenure (years)", min_value=0.0)

        if st.button("Calculate PV"):
            MR = R/100/12
            MN = N*12

            PV = (PMT*(1-(1+MR)**(-MN))) / MR

            st.subheader("Result")
            st.write(f"Loan Amt = {PV:.2f}")
            st.write(f"Rate% (yearly) = {R:.2f}")
            st.write(f"Tenure (years) = {N:.2f}")
            st.write(f"PMT (monthly) = {PMT:.2f}")

            # Loan FUNCTION CALL
            loan_table(PV, PMT, MR, MN)

    elif Field == "Tenure":
        PV = st.number_input("Loan Amt", min_value=0.0)
        R = st.number_input("Rate% (yearly)", min_value=0.0)
        PMT = st.number_input("PMT (monthly)", min_value=0.0)

        if st.button("Calculate Tenure"):
            MR = R/100/12

            if PMT <= PV*MR:
                st.error("PMT is too small to cover monthly interest")
            else:
                N = (-math.log(1-(PV*MR)/PMT) / math.log(1+MR)) / 12
                MN = N*12

                st.subheader("Result")
                st.write(f"Loan Amt = {PV:.2f}")
                st.write(f"Rate% (yearly) = {R:.2f}")
                st.write(f"Tenure (years) = {N:.2f}")
                st.write(f"PMT (monthly) = {PMT:.2f}")

                # Loan FUNCTION CALL
                loan_table(PV, PMT, MR, MN)

    elif Field == "Rate":
        PV = st.number_input("Loan Amt", min_value=0.0)
        PMT = st.number_input("PMT (monthly)", min_value=0.0)
        N = st.number_input("Tenure (years)", min_value=0.0)

        if st.button("Calculate Rate"):
            MN = N*12
            MR = 0.01

            for i in range(100):
                f = (PV*MR) / (1-(1+ MR)**(-MN)) - PMT
                df = (PV * (1-(1+MR)**(-MN)) - PV*MR*MN * (1+MR)**(-MN-1)) / (1-(1+MR)**(-MN))**2
        
                MR = MR - f/df
        
                R = MR*12*100

            st.subheader("Result")
            st.write(f"Loan Amt = {PV:.2f}")
            st.write(f"Rate% (yearly) = {R:.2f}")
            st.write(f"Tenure (years) = {N:.2f}")
            st.write(f"PMT (monthly) = {PMT:.2f}")

            # Loan FUNCTION CALL
            loan_table(PV, PMT, MR, MN)

# ================ INVESTMENT SECTION =================

if SECTION == "INVESTMENT":
    Field = st.selectbox("Select Field",["FV", "PMT", "Tenure", "Rate"])

    if Field == "FV":
        PMT = st.number_input("PMT (monthly)", min_value=0.0)
        R = st.number_input("Rate% (yearly)", min_value=0.0)
        N = st.number_input("Tenure (years)", min_value=0.0)

        if st.button("Calculate FV"):
            MR = R/100/12
            MN = N*12
            
            FV = PMT * (((1+MR)**MN -1) / MR)

            st.subheader("Result")
            st.write(f"PMT (monthly) = {PMT:.2f}")
            st.write(f"Rate% (yearly) = {R:.2f}")
            st.write(f"Tenure (years) = {N:.2f}")
            st.write(f"Future Value = {FV:.2f}")

            # INVESTMENT FUNCTION CALL
            policy_table(FV, PMT, MR, MN)

    elif Field == "PMT":
        FV = st.number_input("Future Value", min_value=0.0)
        R = st.number_input("Rate% (yearly)", min_value=0.0)
        N = st.number_input("Tenure (years)", min_value=0.0)

        if st.button("Calculate PMT"):
            MR = R/100/12
            MN = N*12

            PMT = FV / (((1+MR)**MN -1) / MR)
            
            st.subheader("Result")
            st.write(f"PMT (monthly) = {PMT:.2f}")
            st.write(f"Rate% (yearly) = {R:.2f}")
            st.write(f"Tenure (years) = {N:.2f}")
            st.write(f"Future Value = {FV:.2f}")

            # INVESTMENT FUNCTION CALL
            policy_table(FV, PMT, MR, MN)

    elif Field == "Tenure":
        FV = st.number_input("Future Value", min_value=0.0)
        R = st.number_input("Rate% (yearly)", min_value=0.0)
        PMT = st.number_input("PMT (monthly)", min_value=0.0)

        if st.button("Calculate Tenure"):
            MR = R/100/12

            N = (math.log(1+(FV*MR/PMT)) / math.log(1+MR)) / 12
            MN = N*12

            st.subheader("Result")
            st.write(f"PMT (monthly) = {PMT:.2f}")
            st.write(f"Rate% (yearly) = {R:.2f}")
            st.write(f"Tenure (years) = {N:.2f}")
            st.write(f"Future Value = {FV:.2f}")

            # INVESTMENT FUNCTION CALL
            policy_table(FV, PMT, MR, MN)

    elif Field == "Rate":
        FV = st.number_input("Future Value", min_value=0.0)
        PMT = st.number_input("PMT (monthly)", min_value=0.0)
        N = st.number_input("Tenure (years)", min_value=0.0)

        if st.button("Calculate Rate"):
            MR = 0.01
            MN = N*12

            for i in range(100):
                f = PMT * (((1+MR)**MN - 1) / MR) - FV
                df = PMT * ((MR*MN*(1+MR)**(MN-1) - ((1+MR)**MN - 1)) / (MR**2))
                MR = MR - f/df

                R = MR*12*100

            st.subheader("Result")
            st.write(f"PMT (monthly) = {PMT:.2f}")
            st.write(f"Rate% (yearly) = {R:.2f}")
            st.write(f"Tenure (years) = {N:.2f}")
            st.write(f"Future Value = {FV:.2f}")

            # INVESTMENT FUNCTION CALL
            policy_table(FV, PMT, MR, MN)

# =========== SIMPLE INTEREST SECTION =============

if SECTION == "SIMPLE INTEREST":
    Field = st.selectbox("Select Field",["SI", "Rate", "Tenure", "P.Amt"])

    if Field == "SI":
        P = st.number_input("Principal Amount", min_value=0.0)
        R = st.number_input("Rate(%)", min_value=0.0)
        rate_type = st.selectbox("Rate Type", ["Yearly", "Monthly"])
        N = st.number_input("Tenure", min_value=0.0)
        tenure_type = st.selectbox("Tenure Type", ["Yearly", "Monthly"])

        if st.button("Calculate SI"):
            if P <= 0 or R <= 0 or N <= 0:
                st.error("Principal, Rate, and Time must be greater than 0.")
            else:
                if rate_type == "Monthly":
                    R = R * 12
                if tenure_type == "Monthly":
                    N = N / 12

                SI = (P * R * N) / 100
                TA = P + SI
                MR = R / 12
                MN = N * 12

                st.subheader("Result")
                st.write(f"Principal Amt = {P:.2f}")
                st.write(f"Rate% (yearly) = {R:.2f}")
                st.write(f"Rate% (monthly) = {MR:.2f}")
                st.write(f"Tenure (years) = {N:.2f}")
                st.write(f"Tenure (months) = {MN:.2f}")
                st.write(f"Interest = {SI:.2f}")
                st.write(f"Total Amount = {TA:.2f}")

    elif Field == "Rate":
        P = st.number_input("Principal Amount", min_value=0.0)
        SI = st.number_input("Interest", min_value=0.0)
        N = st.number_input("Tenure", min_value=0.0)
        tenure_type = st.selectbox("Tenure Type", ["Yearly", "Monthly"])

        if st.button("Calculate Rate"):
            if P <= 0 or SI <= 0 or N <= 0:
                st.error("Principal, Interest, and Time must be greater than 0.")
            else:
                if tenure_type == "Monthly":
                    N = N / 12

                R = (SI * 100) / (P * N)
                TA = P + SI
                MR = R / 12
                MN = N * 12

                st.subheader("Result")
                st.write(f"Principal Amt = {P:.2f}")
                st.write(f"Rate% (yearly) = {R:.2f}")
                st.write(f"Rate% (monthly) = {MR:.2f}")
                st.write(f"Tenure (years) = {N:.2f}")
                st.write(f"Tenure (months) = {MN:.2f}")
                st.write(f"Interest = {SI:.2f}")
                st.write(f"Total Amount = {TA:.2f}")

    elif Field == "Tenure":
        P = st.number_input("Principal Amount", min_value=0.0)
        SI = st.number_input("Interest", min_value=0.0)
        R = st.number_input("Rate (%)", min_value=0.0)
        rate_type = st.selectbox("Rate Type", ["Yearly", "Monthly"])

        if st.button("Calculate Tenure"):
            if P <= 0 or R <= 0 or SI <= 0:
                st.error("Principal, Rate, and Interest must be greater than 0.")
            else:
                if rate_type == "Monthly":
                    R = R * 12

                N = (SI * 100) / (P * R)
                TA = P + SI
                MR = R / 12
                MN = N * 12

                st.subheader("Result")
                st.write(f"Principal Amt = {P:.2f}")
                st.write(f"Rate% (yearly) = {R:.2f}")
                st.write(f"Rate% (monthly) = {MR:.2f}")
                st.write(f"Tenure (years) = {N:.2f}")
                st.write(f"Tenure (months) = {MN:.2f}")
                st.write(f"Interest = {SI:.2f}")
                st.write(f"Total Amount = {TA:.2f}")

    elif Field == "P.Amt":
        R = st.number_input("Rate (%)", min_value=0.0)
        rate_type = st.selectbox("Rate Type", ["Yearly", "Monthly"])
        N = st.number_input("Tenure", min_value=0.0)
        tenure_type = st.selectbox("Tenure Type", ["Yearly", "Monthly"])
        SI = st.number_input("Interest", min_value=0.0)

        if st.button("Calculate P.Amt"):
            if SI <= 0 or R <= 0 or N <= 0:
                st.error("Rate, Time, and Interest must be greater than 0.")
            else:
                if rate_type == "Monthly":
                    R = R * 12
                if tenure_type == "Monthly":
                    N = N / 12

                P = (SI * 100) / (R * N)
                TA = P + SI
                MR = R / 12
                MN = N * 12

                st.subheader("Result")
                st.write(f"Principal Amt = {P:.2f}")
                st.write(f"Rate% (yearly) = {R:.2f}")
                st.write(f"Rate% (monthly) = {MR:.2f}")
                st.write(f"Tenure (years) = {N:.2f}")
                st.write(f"Tenure (months) = {MN:.2f}")
                st.write(f"Interest = {SI:.2f}")
                st.write(f"Total Amount = {TA:.2f}")

    
        
