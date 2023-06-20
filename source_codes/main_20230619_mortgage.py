import pandas as pd
import matplotlib.pyplot as plt


def mortgage_schedule(pool_amount, term_years, interest_rate, prepayment_speed, pmt_per_year=12):
    # Calculate installment payments and outstanding balances
    term_months = term_years * pmt_per_year
    monthly_interest_rate = interest_rate / pmt_per_year
    schedule = []
    outstanding_balance = pool_amount
    for month in range(1, term_months + 1):
        cpr = min(month * 2, 60) / 1000 * prepayment_speed
        smm = 1 - (1 - cpr) ** (1 / pmt_per_year)
        remaining_month = (term_months + 1 - month)
        payment = (outstanding_balance * monthly_interest_rate * ((1 + monthly_interest_rate) ** remaining_month)) / (
                    (1 + monthly_interest_rate) ** remaining_month - 1)
        interest = outstanding_balance * monthly_interest_rate
        principal_scheduled = payment - interest
        prepayment = (outstanding_balance - principal_scheduled) * smm
        principal_total = principal_scheduled + prepayment
        outstanding_balance = outstanding_balance - principal_scheduled - prepayment
        schedule.append(
            (month, cpr, smm, payment, interest, principal_scheduled, prepayment, principal_total, outstanding_balance))

        # Stop calculation if outstanding balance becomes negative (fully paid)
        if outstanding_balance <= 0:
            break

    df_schedule = pd.DataFrame(schedule, columns=["MONTH", 'CPR', 'SMM', "PAYMENT", "INTEREST", "PRINCIPAL_SCHEDULED",
                                                  "PREPAYMENT", "PRINCIPAL_TOTAL", "OB"])
    return df_schedule


########################################################################################################################
# SEQ 구조
df_pool = mortgage_schedule(pool_amount=75000, term_years=10, interest_rate=0.11, prepayment_speed=2.0, pmt_per_year=12)

# Calculate installment payments and outstanding balances
tranche_a_amount = 27000
tranche_a_rate = 0.0925
tranche_b_amount = 15000
tranche_b_rate = 0.10
tranche_z_amount = 30000
tranche_z_rate = 0.11
residual_amount = 75000 - tranche_a_amount - tranche_b_amount - tranche_z_amount

pmt_per_year = 12

tranche_term = len(df_pool["MONTH"])

tranche_schedule = []
a_olb = tranche_a_amount
b_olb = tranche_b_amount
z_olb = tranche_z_amount
residual = residual_amount

for month in range(1, tranche_term + 1):
    # MBS Cashflow
    mbs_principal = df_pool["PRINCIPAL_TOTAL"][month-1]
    mbs_interest = df_pool["INTEREST"][month-1]
    mbs_cashflow = mbs_principal + mbs_interest

    # Class Z Tranche
    z_interest = z_olb * tranche_z_rate / pmt_per_year # Z 클래스 이자가 accrued 되어 들어온다

    # Tranche A
    a_olb_beg = a_olb  # Tranche A Outstanding Loan Balance (Beginning)
    a_interest = a_olb * tranche_a_rate / pmt_per_year
    a_principal = min(mbs_principal + z_interest, a_olb)
    a_olb = a_olb - a_principal
    a_olb_end = a_olb  # Tranche A Outstanding Loan Balance (Ending)
    a_cf = a_interest + a_principal

    # Tranche B
    b_olb_beg = b_olb  # Tranche B Outstanding Loan Balance (Beginning)
    b_interest = b_olb * tranche_b_rate / pmt_per_year
    b_principal = min(mbs_principal + z_interest - a_principal, b_olb)
    b_olb = b_olb - b_principal
    b_olb_end = b_olb  # Tranche B Outstanding Loan Balance (Ending)
    b_cf = b_interest + b_principal

    # Tranche Z
    z_olb_beg = z_olb  # Tranche Z Outstanding Loan Balance (Beginning)
    z_payment = min(mbs_principal + z_interest - a_principal - b_principal, z_olb + z_interest)
    z_olb = z_olb + z_interest - z_payment
    z_olb_end = z_olb  # Tranche Z Outstanding Loan Balance (Ending)

    # Residual
    residual_cf = mbs_principal + mbs_interest - a_interest - a_principal - b_interest - b_principal - z_payment

    tranche_schedule.append(
        (month, mbs_principal, mbs_interest, mbs_cashflow, a_olb_beg, a_interest, a_principal, a_olb_end,
         b_olb_beg, b_interest, b_principal, b_olb_end, z_olb_beg, z_interest, z_payment, z_olb_end, residual_cf))


df_seq = pd.DataFrame(tranche_schedule, columns=[
    "MONTH", "MBS_PRINCIPAL", "MBS_INTEREST", "MBS_CF",
    "A_OLB(beg)", "A_INTEREST", "A_PRINCIPAL", "A_OLB(end)",
    "B_OLB(beg)", "B_INTEREST", "B_PRINCIPAL", "B_OLB(end)",
    "Z_OLB(beg)", "Z_INTEREST", "Z_PAYMENT", "Z_OLB(end)", "RESIDUAL_CF"])


########################################################################################################################
# PAC 구조
df_pool = mortgage_schedule(pool_amount=100000000, term_years=30, interest_rate=0.10, prepayment_speed=2.0, pmt_per_year=12)
df_psa_low = mortgage_schedule(pool_amount=100000000, term_years=30, interest_rate=0.10, prepayment_speed=0.8, pmt_per_year=12)
df_psa_high = mortgage_schedule(pool_amount=100000000, term_years=30, interest_rate=0.10, prepayment_speed=3.0, pmt_per_year=12)

# Calculate installment payments and outstanding balances
tranche_a_amount = 30000000
tranche_a_rate = 0.0925
tranche_b_amount = 15000000
tranche_b_rate = 0.10
tranche_s_amount = 55000000
tranche_s_rate = 0.11
tranche_z_amount = 0
tranche_z_rate = 0.11
residual_amount = 100000000 - tranche_a_amount - tranche_b_amount - tranche_s_amount - tranche_z_amount

pmt_per_year = 12

tranche_term = len(df_pool["MONTH"])

tranche_schedule = []
a_olb = tranche_a_amount
b_olb = tranche_b_amount
s_olb = tranche_s_amount
z_olb = tranche_z_amount
residual = residual_amount


for month in range(1, tranche_term + 1):
    # MBS Cashflow
    mbs_principal = df_pool["PRINCIPAL_TOTAL"][month-1]
    mbs_interest = df_pool["INTEREST"][month-1]
    mbs_cashflow = mbs_principal + mbs_interest

    # Class Z Tranche
    z_interest = z_olb * tranche_z_rate / pmt_per_year # Z 클래스 이자가 accrued 되어 들어온다

    # PAC Band
    pac_band = min(df_psa_low["PRINCIPAL_TOTAL"][month-1], df_psa_high["PRINCIPAL_TOTAL"][month-1])

    # Tranche A
    a_olb_beg = a_olb  # Tranche A Outstanding Loan Balance (Beginning)
    a_interest = a_olb * tranche_a_rate / pmt_per_year
    a_principal = min(min(mbs_principal + z_interest, pac_band), a_olb)
    a_olb = a_olb - a_principal
    a_olb_end = a_olb  # Tranche A Outstanding Loan Balance (Ending)
    a_cashflow = a_interest + a_principal

    # Tranche B
    b_olb_beg = b_olb  # Tranche B Outstanding Loan Balance (Beginning)
    b_interest = b_olb * tranche_b_rate / pmt_per_year
    b_principal = min(min(mbs_principal + z_interest, pac_band) - a_principal, b_olb)
    b_olb = b_olb - b_principal
    b_olb_end = b_olb  # Tranche B Outstanding Loan Balance (Ending)
    b_cashflow = b_interest + b_principal

    # Tranche S
    s_olb_beg = s_olb  # Tranche S Outstanding Loan Balance (Beginning)
    s_interest = s_olb * tranche_s_rate / pmt_per_year
    s_payment = mbs_cashflow - a_cashflow - b_cashflow
    s_principal = min(s_payment - s_interest, s_olb)
    # s_principal = min(mbs_principal + z_interest - a_principal - b_principal, s_olb)
    s_olb = s_olb - s_principal
    s_olb_end = s_olb  # Tranche S Outstanding Loan Balance (Ending)
    s_cf = s_interest + s_principal

    # Tranche Z
    z_olb_beg = z_olb  # Tranche Z Outstanding Loan Balance (Beginning)
    z_payment = min(mbs_principal + z_interest - a_principal - b_principal, z_olb + z_interest)
    z_olb = z_olb + z_interest - z_payment
    z_olb_end = z_olb  # Tranche Z Outstanding Loan Balance (Ending)

    # Residual
    residual_cf = mbs_cashflow - a_cashflow - b_cashflow - s_payment - z_payment

    tranche_schedule.append(
        (month, mbs_principal, mbs_interest, mbs_cashflow, pac_band, a_olb_beg, a_interest, a_principal, a_olb_end,
         b_olb_beg, b_interest, b_principal, b_olb_end, s_olb_beg, s_interest, s_principal, s_olb_end,
         z_olb_beg, z_interest, z_payment, z_olb_end, residual_cf))


df_pac = pd.DataFrame(tranche_schedule, columns=[
    "MONTH", "MBS_PRINCIPAL", "MBS_INTEREST", "MBS_CF", "PAC_BAND",
    "A_OLB(beg)", "A_INTEREST", "A_PRINCIPAL", "A_OLB(end)",
    "B_OLB(beg)", "B_INTEREST", "B_PRINCIPAL", "B_OLB(end)",
    "S_OLB(beg)", "S_INTEREST", "S_PRINCIPAL", "S_OLB(end)",
    "Z_OLB(beg)", "Z_INTEREST", "Z_PAYMENT", "Z_OLB(end)", "RESIDUAL_CF"])



########################################################################################################################



df_psa80 = mortgage_schedule(pool_amount=100000, term_years=30, interest_rate=0.095, prepayment_speed=0.8)
df_psa300 = mortgage_schedule(pool_amount=100000, term_years=30, interest_rate=0.095, prepayment_speed=3.0)

df_psa80["PRINCIPAL_TOTAL"]
df_psa300["PRINCIPAL_TOTAL"]


# 시각화
fig = plt.figure()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
# fig.set_size_inches(1800/300, 1200/300)  # 그래프 크기 지정, DPI=300

plt.plot(df_psa80["MONTH"], df_psa80["PRINCIPAL_TOTAL"], color='r', label="PRINCIPAL_TOTAL")
plt.plot(df_psa300["MONTH"], df_psa300["PRINCIPAL_TOTAL"], color='r', label="PRINCIPAL_TOTAL")
plt.fill_betweenx(x, df_psa80["PRINCIPAL_TOTAL"], df_psa300["PRINCIPAL_TOTAL"], where=(df_psa80["PRINCIPAL_TOTAL"] < df_psa300["PRINCIPAL_TOTAL"]), color='blue', alpha=0.3)

#plt.xlim(1, )
# plt.ylim(30, 120)
# plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlabel('Months', fontsize=10)
plt.ylabel('Consumer Price Index (2020=100)', fontsize=10)
plt.legend(loc='upper left')
plt.show()

# plt.savefig("./Lecture_Figures_output/fig1.1_cpi.png")



# Sample principal payment cashflows for each tranche by month
tranche1_cashflow = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550]
tranche2_cashflow = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
tranche3_cashflow = [25, 50, 75, 100, 125, 150, 175, 200, 225, 250]

months = [f'Month {i+1}' for i in range(len(tranche1_cashflow))]  # Month labels

plt.plot(months, tranche1_cashflow, label='Tranche 1')
plt.plot(months, tranche2_cashflow, label='Tranche 2')
plt.plot(months, tranche3_cashflow, label='Tranche 3')

plt.xlabel('Month')
plt.ylabel('Principal Payment Cashflow')
plt.title('Principal Payment Cashflow by Tranche')
plt.legend()

plt.show()


import numpy as np


# Generate data points for the curves
x = np.linspace(0, 10, 100)
curve1 = np.sin(x)
curve2 = np.cos(x)

# Plot the curves
plt.plot(x, curve1, label='Curve 1')
plt.plot(x, curve2, label='Curve 2')

# Fill the area where Curve 1 is lower than Curve 2
plt.fill_betweenx(x, curve1, curve2, where=(curve1 < curve2), color='blue', alpha=0.3)

# Add labels and a legend
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Convex Curves')
plt.legend()

# Show the figure
plt.show()