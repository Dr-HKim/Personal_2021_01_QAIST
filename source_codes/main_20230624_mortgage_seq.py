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
# SEQ 구조
df_pool = mortgage_schedule(pool_amount=1000000, term_years=30, interest_rate=0.10, prepayment_speed=0.5, pmt_per_year=12)

# Calculate installment payments and outstanding balances
# tranche_a_amount = 500000
# tranche_a_rate = 0.0925
# tranche_b_amount = 300000
# tranche_b_rate = 0.10
# tranche_c_amount = 1000000 - tranche_a_amount - tranche_b_amount
# tranche_c_rate = (1000000*0.11 - tranche_a_amount*tranche_a_rate - tranche_b_amount*tranche_b_rate) / tranche_c_amount
# pmt_per_year = 12

tranche_a_amount = 300000
tranche_a_rate = 0.08
tranche_b_amount = 200000
tranche_b_rate = 0.09
tranche_c_amount = 1000000 - tranche_a_amount - tranche_b_amount
tranche_c_rate = (1000000*0.09 - tranche_a_amount*tranche_a_rate - tranche_b_amount*tranche_b_rate) / tranche_c_amount
pmt_per_year = 12

tranche_term = len(df_pool["MONTH"])

tranche_schedule = []
a_olb = tranche_a_amount
b_olb = tranche_b_amount
c_olb = tranche_c_amount

for month in range(1, tranche_term + 1):
    # MBS Cashflow
    mbs_principal = df_pool["PRINCIPAL_TOTAL"][month-1]
    mbs_interest = df_pool["INTEREST"][month-1]
    mbs_cashflow = mbs_principal + mbs_interest

    # Tranche A
    a_olb_beg = a_olb  # Tranche A Outstanding Loan Balance (Beginning)
    a_interest = a_olb * tranche_a_rate / pmt_per_year
    a_principal = min(mbs_principal, a_olb)
    a_olb = a_olb - a_principal
    a_olb_end = a_olb  # Tranche A Outstanding Loan Balance (Ending)
    a_cf = a_interest + a_principal

    # Tranche B
    b_olb_beg = b_olb  # Tranche B Outstanding Loan Balance (Beginning)
    b_interest = b_olb * tranche_b_rate / pmt_per_year
    b_principal = min(mbs_principal - a_principal, b_olb)
    b_olb = b_olb - b_principal
    b_olb_end = b_olb  # Tranche B Outstanding Loan Balance (Ending)
    b_cf = b_interest + b_principal

    # Tranche C
    c_olb_beg = c_olb  # Tranche B Outstanding Loan Balance (Beginning)
    c_interest = c_olb * tranche_c_rate / pmt_per_year
    c_principal = min(mbs_principal - a_principal - b_principal, c_olb)
    c_olb = c_olb - c_principal
    c_olb_end = c_olb  # Tranche B Outstanding Loan Balance (Ending)
    c_cf = c_interest + c_principal

    # Residual
    residual_cf = mbs_principal + mbs_interest - a_interest - a_principal - b_interest - b_principal - c_interest - c_principal

    tranche_schedule.append(
        (month, mbs_principal, mbs_interest, mbs_cashflow, a_olb_beg, a_interest, a_principal, a_olb_end,
         b_olb_beg, b_interest, b_principal, b_olb_end,
         c_olb_beg, c_interest, c_principal, c_olb_end, residual_cf))


df_seq = pd.DataFrame(tranche_schedule, columns=[
    "MONTH", "MBS_PRINCIPAL", "MBS_INTEREST", "MBS_CF",
    "A_OLB(beg)", "A_INTEREST", "A_PRINCIPAL", "A_OLB(end)",
    "B_OLB(beg)", "B_INTEREST", "B_PRINCIPAL", "B_OLB(end)",
    "C_OLB(beg)", "C_INTEREST", "C_PRINCIPAL", "C_OLB(end)", "RESIDUAL_CF"])

wal_a = sum(df_seq["MONTH"] * df_seq["A_PRINCIPAL"])/tranche_a_amount
wal_b = sum(df_seq["MONTH"] * df_seq["B_PRINCIPAL"])/tranche_b_amount
wal_c = sum(df_seq["MONTH"] * df_seq["C_PRINCIPAL"])/tranche_c_amount

print("Tranche A WAL: " + str(wal_a))
print("Tranche B WAL: " + str(wal_b))
print("Tranche S WAL: " + str(wal_c))
########################################################################################################################
x = df_seq["MONTH"]
y1 = df_seq["MBS_PRINCIPAL"]
y2 = df_seq["MBS_INTEREST"]

fig, ax = plt.subplots()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
ax.stackplot(x, y1, y2, labels=["MBS_PRINCIPAL", "MBS_INTEREST"])
ax.legend(loc='upper right')
plt.ylim(0, 15000)
plt.show()
plt.savefig("./seq_mbs_psa50.png")

x = df_seq["MONTH"]
y1 = df_seq["A_PRINCIPAL"]
y2 = df_seq["A_INTEREST"]
y3 = df_seq["B_PRINCIPAL"]
y4 = df_seq["B_INTEREST"]
y5 = df_seq["C_PRINCIPAL"]
y6 = df_seq["C_INTEREST"]
y7 = df_seq["RESIDUAL_CF"]

fig, ax = plt.subplots()
fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
ax.stackplot(x, y1, y2, y3, y4, y5, y6, y7, labels=["A_PRINCIPAL", "A_INTEREST", "B_PRINCIPAL", "B_INTEREST", "C_PRINCIPAL", "C_INTEREST", "RESIDUAL_CF"])
ax.legend(loc='upper right')
plt.ylim(0, 15000)
plt.show()
plt.savefig("./seq_tranche_psa50.png")





########################################################################################################################


# df_psa80 = mortgage_schedule(pool_amount=100000, term_years=30, interest_rate=0.095, prepayment_speed=0.8)
# df_psa300 = mortgage_schedule(pool_amount=100000, term_years=30, interest_rate=0.095, prepayment_speed=3.0)
#
# df_psa80["PRINCIPAL_TOTAL"]
# df_psa300["PRINCIPAL_TOTAL"]
#
#
# # 시각화
# fig = plt.figure()
# fig.set_size_inches(3600/300, 1800/300)  # 그래프 크기 지정, DPI=300
# # fig.set_size_inches(1800/300, 1200/300)  # 그래프 크기 지정, DPI=300
#
# plt.plot(df_psa80["MONTH"], df_psa80["PRINCIPAL_TOTAL"], color='r', label="PRINCIPAL_TOTAL")
# plt.plot(df_psa300["MONTH"], df_psa300["PRINCIPAL_TOTAL"], color='r', label="PRINCIPAL_TOTAL")
# plt.fill_betweenx(x, df_psa80["PRINCIPAL_TOTAL"], df_psa300["PRINCIPAL_TOTAL"], where=(df_psa80["PRINCIPAL_TOTAL"] < df_psa300["PRINCIPAL_TOTAL"]), color='blue', alpha=0.3)
#
# #plt.xlim(1, )
# # plt.ylim(30, 120)
# # plt.axhline(y=0, color='green', linestyle='dotted')
# plt.xlabel('Months', fontsize=10)
# plt.ylabel('Consumer Price Index (2020=100)', fontsize=10)
# plt.legend(loc='upper left')
# plt.show()
#
# # plt.savefig("./Lecture_Figures_output/fig1.1_cpi.png")
#
#
#
# # Sample principal payment cashflows for each tranche by month
# tranche1_cashflow = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550]
# tranche2_cashflow = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
# tranche3_cashflow = [25, 50, 75, 100, 125, 150, 175, 200, 225, 250]
#
# months = [f'Month {i+1}' for i in range(len(tranche1_cashflow))]  # Month labels
#
# plt.plot(months, tranche1_cashflow, label='Tranche 1')
# plt.plot(months, tranche2_cashflow, label='Tranche 2')
# plt.plot(months, tranche3_cashflow, label='Tranche 3')
#
# plt.xlabel('Month')
# plt.ylabel('Principal Payment Cashflow')
# plt.title('Principal Payment Cashflow by Tranche')
# plt.legend()
#
# plt.show()
#
#
# import numpy as np
#
#
# # Generate data points for the curves
# x = np.linspace(0, 10, 100)
# curve1 = np.sin(x)
# curve2 = np.cos(x)
#
# # Plot the curves
# plt.plot(x, curve1, label='Curve 1')
# plt.plot(x, curve2, label='Curve 2')
#
# # Fill the area where Curve 1 is lower than Curve 2
# plt.fill_betweenx(x, curve1, curve2, where=(curve1 < curve2), color='blue', alpha=0.3)
#
# # Add labels and a legend
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.title('Convex Curves')
# plt.legend()
#
# # Show the figure
# plt.show()