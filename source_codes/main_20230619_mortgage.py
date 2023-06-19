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

#plt.xlim(1, )
# plt.ylim(30, 120)
# plt.axhline(y=0, color='green', linestyle='dotted')
plt.xlabel('Months', fontsize=10)
plt.ylabel('Consumer Price Index (2020=100)', fontsize=10)
plt.legend(loc='upper left')
plt.show()

# plt.savefig("./Lecture_Figures_output/fig1.1_cpi.png")


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

    # Class Z Tranche
    z_interest = z_olb * tranche_z_rate / pmt_per_year # Z 클래스 이자가 accrued 되어 들어온다

    # Tranche A
    a_interest = a_olb * tranche_a_rate / pmt_per_year
    a_principal = min(mbs_principal + z_interest, a_olb)
    a_olb = a_olb - a_principal
    a_cf = a_interest + a_principal

    # Tranche B
    b_interest = b_olb * tranche_b_rate / pmt_per_year
    b_principal = min(mbs_principal + z_interest - a_principal, b_olb)
    b_olb = b_olb - b_principal
    b_cf = b_interest + b_principal

    # Tranche Z
    z_payment = min(mbs_principal + z_interest - a_principal - b_principal, z_olb + z_interest)
    z_olb = z_olb + z_interest - z_payment

    # Residual
    residual_cf = mbs_principal + mbs_interest - a_interest - a_principal - b_interest - b_principal - z_payment

    tranche_schedule.append(
        (month, mbs_principal, mbs_interest, a_interest, a_principal, a_olb, a_cf, b_interest, b_principal, b_olb, b_cf, z_interest, z_olb, z_payment, residual_cf))


df_tranche = pd.DataFrame(tranche_schedule, columns=[
    "MONTH", "MBS_PRINCIPAL", "MBS_INTEREST",
    "A_INTEREST", "A_PRINCIPAL", "A_OLB", "A_CF",
    "B_INTEREST", "B_PRINCIPAL", "B_OLB", "B_CF",
    "Z_INTEREST", "Z_OLB", "Z_PAYMENT", "RESIDUAL_CF"])


########################################################################################################################
# PAC 구조
df_pool = mortgage_schedule(pool_amount=100000000, term_years=30, interest_rate=0.11, prepayment_speed=4.0, pmt_per_year=12)
df_psa_low = mortgage_schedule(pool_amount=100000000, term_years=30, interest_rate=0.11, prepayment_speed=0.8, pmt_per_year=12)
df_psa_high = mortgage_schedule(pool_amount=100000000, term_years=30, interest_rate=0.11, prepayment_speed=3.0, pmt_per_year=12)

# Calculate installment payments and outstanding balances
tranche_a_amount = 30000000
tranche_a_rate = 0.0925
tranche_b_amount = 15000000
tranche_b_rate = 0.10
tranche_s_amount = 40000000
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

    # PAC Band
    pac_band = min(df_psa_low["PRINCIPAL_TOTAL"][month-1], df_psa_high["PRINCIPAL_TOTAL"][month-1])

    # Class Z Tranche
    z_interest = z_olb * tranche_z_rate / pmt_per_year # Z 클래스 이자가 accrued 되어 들어온다

    # Tranche A
    a_interest = a_olb * tranche_a_rate / pmt_per_year
    a_principal = min(min(mbs_principal + z_interest, pac_band), a_olb)
    a_olb = a_olb - a_principal
    a_cf = a_interest + a_principal

    # Tranche B
    b_interest = b_olb * tranche_b_rate / pmt_per_year
    b_principal = min(min(mbs_principal + z_interest, pac_band) - a_principal, b_olb)
    b_olb = b_olb - b_principal
    b_cf = b_interest + b_principal

    # Tranche S
    s_interest = s_olb * tranche_s_rate / pmt_per_year
    s_principal = min(mbs_principal + z_interest - a_principal - b_principal, s_olb)
    s_olb = s_olb - s_principal
    s_cf = s_interest + s_principal

    # Tranche Z
    z_payment = min(mbs_principal + z_interest - a_principal - b_principal, z_olb + z_interest)
    z_olb = z_olb + z_interest - z_payment

    # Residual
    residual_cf = mbs_principal + mbs_interest - a_interest - a_principal - b_interest - b_principal - s_interest - s_principal - z_payment

    tranche_schedule.append(
        (month, mbs_principal, mbs_interest, pac_band, a_interest, a_principal, a_olb, a_cf, b_interest, b_principal, b_olb, b_cf, s_interest, s_principal, s_olb, s_cf, z_interest, z_olb, z_payment, residual_cf))


df_tranche = pd.DataFrame(tranche_schedule, columns=[
    "MONTH", "MBS_PRINCIPAL", "MBS_INTEREST", "PAC_BAND",
    "A_INTEREST", "A_PRINCIPAL", "A_OLB", "A_CF",
    "B_INTEREST", "B_PRINCIPAL", "B_OLB", "B_CF",
    "S_INTEREST", "S_PRINCIPAL", "S_OLB", "S_CF",
    "Z_INTEREST", "Z_OLB", "Z_PAYMENT", "RESIDUAL_CF"])

########################################################################################################################





