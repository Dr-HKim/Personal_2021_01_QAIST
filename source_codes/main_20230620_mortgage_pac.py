import pandas as pd
import numpy as np
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
# PAC 구조
df_pool = mortgage_schedule(pool_amount=1000000, term_years=30, interest_rate=0.10, prepayment_speed=0.5, pmt_per_year=12)
df_psa_low = mortgage_schedule(pool_amount=1000000, term_years=30, interest_rate=0.10, prepayment_speed=0.9, pmt_per_year=12)
df_psa_high = mortgage_schedule(pool_amount=1000000, term_years=30, interest_rate=0.10, prepayment_speed=3.0, pmt_per_year=12)

# Calculate installment payments and outstanding balances
tranche_a_amount = 300000
tranche_b_amount = 200000
tranche_s_amount = 1000000 - tranche_a_amount - tranche_b_amount
pmt_per_year = 12

tranche_term = len(df_pool["MONTH"])

tranche_schedule = []
a_olb = tranche_a_amount
b_olb = tranche_b_amount
s_olb = tranche_s_amount

for month in range(1, tranche_term + 1):
    # MBS Cashflow
    mbs_principal = df_pool["PRINCIPAL_TOTAL"][month-1]

    # PAC Band
    pac_band = min(df_psa_low["PRINCIPAL_TOTAL"][month-1], df_psa_high["PRINCIPAL_TOTAL"][month-1])

    # Tranche A
    a_olb_beg = a_olb  # Tranche A Outstanding Loan Balance (Beginning)
    if mbs_principal - pac_band <= s_olb:
        a_principal = min(min(mbs_principal, pac_band), a_olb)
    else:
        a_principal = min(mbs_principal - s_olb, a_olb)
    a_olb = a_olb - a_principal
    a_olb_end = a_olb  # Tranche A Outstanding Loan Balance (Ending)

    # Tranche B
    b_olb_beg = b_olb  # Tranche B Outstanding Loan Balance (Beginning)
    if mbs_principal - pac_band <= s_olb:
        b_principal = min(min(mbs_principal, pac_band) - a_principal, b_olb)
    else:
        b_principal = min(mbs_principal - a_principal - s_olb, b_olb)

    b_olb = b_olb - b_principal
    b_olb_end = b_olb  # Tranche B Outstanding Loan Balance (Ending)

    # Tranche S
    s_olb_beg = s_olb  # Tranche S Outstanding Loan Balance (Beginning)
    s_payment = min(mbs_principal - a_principal - b_principal, s_olb)
    s_principal = min(s_payment, s_olb)
    # s_principal = min(mbs_principal + z_interest - a_principal - b_principal, s_olb)
    s_olb = s_olb - s_principal
    s_olb_end = s_olb  # Tranche S Outstanding Loan Balance (Ending)

    tranche_schedule.append(
        (month, mbs_principal,pac_band, a_olb_beg, a_principal, a_olb_end,
         b_olb_beg, b_principal, b_olb_end,
         s_olb_beg, s_payment, s_principal, s_olb_end))


df_pac = pd.DataFrame(tranche_schedule, columns=[
    "MONTH", "MBS_PRINCIPAL", "PAC_BAND",
    "A_OLB(beg)", "A_PRINCIPAL", "A_OLB(end)",
    "B_OLB(beg)", "B_PRINCIPAL", "B_OLB(end)",
    "S_OLB(beg)", "S_PAYMENT", "S_PRINCIPAL", "S_OLB(end)"])


df_pac["MBS_PRINCIPAL"][42] - df_pac["PAC_BAND"][42]
df_pac["S_OLB(beg)"][42]

########################################################################################################################
x = df_pac["MONTH"]
y1 = df_pac["MBS_PRINCIPAL"]

fig, ax = plt.subplots()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300

ax.stackplot(x, y1, labels=["MBS_PRINCIPAL (PSA 50)"])
ax.plot(x, df_pac["PAC_BAND"], color='r', label="PAC 90-300")
ax.legend(loc='upper right')
plt.ylim(0, 15000)
plt.show()
plt.savefig("./pac90-300_psa50_mbs.png")



x = df_pac["MONTH"]
y1 = df_pac["A_PRINCIPAL"]
y2 = df_pac["B_PRINCIPAL"]
y3 = df_pac["S_PRINCIPAL"]

fig, ax = plt.subplots()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300

ax.stackplot(x, y1, y2, y3, labels=["PAC A", "PAC B", "Support"])
ax.plot(x, df_pac["PAC_BAND"], color='r', label="PAC 90-300")
ax.legend(loc='upper right')
plt.ylim(0, 15000)
plt.show()
plt.savefig("./pac90-300_psa50_tranche.png")
