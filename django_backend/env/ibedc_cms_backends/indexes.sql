CREATE NONCLUSTERED INDEX idx_ems_payments_PaymentTransactionId ON [ems_payments] (PaymentTransactionId);

CREATE NONCLUSTERED INDEX idx_ems_payment_trans_transid ON [ems_payment_trans] (transid)

CREATE INDEX idx_EmsBillID ON dbo.ems_bills (BillID)

CREATE NONCLUSTERED INDEX ix_ems_customers_new_AccountNo ON ems_customers_new(AccountNo);

CREATE NONCLUSTERED INDEX ix_ems_bills_BillID ON ems_bills(BillID)

CREATE INDEX idx_EmsCustState ON dbo.ems_customers_new (State)

CREATE INDEX idx_EcmiCustState ON [CMS_DB].[dbo].[ems_customers_new] (State)

CREATE INDEX idx_EcmiCustAccountType ON [CMS_DB].[dbo].[ecmi_customers_new] ([AccountType])

CREATE INDEX idx_EcmiCustBuid ON [CMS_DB].[dbo].[ems_customers_new] (BUID)

CREATE INDEX idx_EcmiCustServicecenter ON [CMS_DB].[dbo].[ems_customers_new] (ServiceCenter)

CREATE INDEX idx_EmsCustAccountNo ON dbo.ems_customers_new (AccountNo)

CREATE INDEX idx_AccountNo ON dbo.ems_bills (AccountNo)

CREATE NONCLUSTERED INDEX IX_ems_payments_AccountNo ON [CMS_DB].[dbo].[ems_payments] ([AccountNo]);

CREATE INDEX IX_ems_payments_receiptnumber ON [CMS_DB].[dbo].[ems_payments] (receiptnumber);

CREATE INDEX IX_ems_payments_billid ON [CMS_DB].[dbo].[ems_payments] (PaymentId);

CREATE INDEX IX_ems_payments_PaymentTransId ON [CMS_DB].[dbo].[ems_payments] (PaymentTransactionId);

CREATE INDEX IX_ems_payments_PayDate ON [CMS_DB].[dbo].[ems_payments] (PayDate);

CREATE INDEX idx_ecmi_customers_new_AccountNo ON ecmi_customers_new (AccountNo);
CREATE INDEX idx_ecmi_customers_new_MeterNo ON ecmi_customers_new (MeterNo);
CREATE INDEX idx_msms_meter_details_tbl_meter_number ON msms_meter_details_tbl (meter_number);
CREATE INDEX idx_gis_distribution_substation_11KV_415_Assetid ON gis_distribution_substation_11KV_415 (Assetid);
CREATE INDEX idx_gis_distribution_substation_33KV_415_Assetid ON gis_distribution_substation_33KV_415 (Assetid);
CREATE INDEX idx_msms_customers_previous_account_number ON msms_customers (previous_account_number);
CREATE INDEX idx_ecmi_customers_new_Surname ON ecmi_customers_new (Surname);


CREATE INDEX idx_ems_customers_new_DSS_ID ON ems_customers_new (DSS_ID);

CREATE INDEX idx_ecmi_customers_new_DSS_ID ON ecmi_customers_new (DSS_ID);

CREATE INDEX idx_gis_Service_Units_name ON [gis_Service Units]  (name);

CREATE INDEX idx_High_Tension_Pole_33KV_assetid ON [High Tension Pole 33KV] (assetid);

CREATE INDEX idx_gis_33KV_Feeder_assetid ON [gis_33KV Feeder] (assetid);

CREATE INDEX idx_gis_Power_Transformer_33KV_11KV_assetid ON [gis_Power Transformer 33KV_11KV] (assetid);

CREATE INDEX idx_gis_InjectionSub_Station_assetid ON [gis_InjectionSub Station] (assetid);


CREATE INDEX IX_ecmi_customers_new_State_BUID_AccountNo
ON [CMS_DB].[dbo].[ecmi_customers_new] (State, BUID, AccountNo);


CREATE INDEX idx_ops_meter_readings_account_number ON ops_meter_readings(account_number);
CREATE INDEX idx_ops_meter_readings_created_at ON ops_meter_readings(created_at);
CREATE INDEX idx_ops_bill_distribution_account_number ON ops_bill_distribution(account_number);
CREATE INDEX idx_ops_bill_distribution_created_at ON ops_bill_distribution(created_at);
CREATE INDEX idx_ops_evaluated_customers_account_no ON ops_evaluated_customers(account_no);
CREATE INDEX idx_ops_evaluated_customers_created_at ON ops_evaluated_customers(created_at);
CREATE INDEX idx_ops_enumerated_customers_account_number ON ops_enumerated_customers(account_number);
CREATE INDEX idx_ops_enumerated_customers_created_at ON ops_enumerated_customers(created_at);

CREATE INDEX idx_emspayments_processeddate ON [CMS_DB].[dbo].[ems_payments] (ProcessedDate);

CREATE INDEX idx_ecmi_payment_history_transdate ON [CMS_DB].[dbo].[ecmi_payment_history] (transdate DESC);
CREATE INDEX idx_ecmi_payment_history_transref ON [CMS_DB].[dbo].[ecmi_payment_history] (transref);
CREATE INDEX idx_ecmi_transactions_transref ON [CMS_DB].[dbo].[ecmi_transactions] (transref);


CREATE INDEX idx_ems_bills_AccountNo ON ems_bills (AccountNo);

CREATE INDEX IX_AccountNo ON ems_customers_new(AccountNo);
CREATE INDEX IX_State_BUID ON ems_customers_new(state, BUID);
CREATE INDEX IX_AccountNo_BillDate ON ems_bills(AccountNo, BillDate DESC);


CREATE INDEX IX_ecmi_customers_new_State_BUID_ServiceCenter
ON [CMS_DB].[dbo].[ecmi_customers_new] (State, BUID, ServiceCenter);

CREATE INDEX IX_ecmi_payment_history_transdate
ON [CMS_DB].[dbo].[ecmi_payment_history] (transdate);

CREATE INDEX IX_ecmi_transactions_transref
ON [CMS_DB].[dbo].[ecmi_transactions] (transref);


CREATE INDEX IX_ecmi_customers_new_AccountNo ON [ecmi_customers_new] (AccountNo) INCLUDE (firstname, Surname, othernames, BUID)

CREATE INDEX IX_ecmi_transactions_transref_AccountNo ON [ecmi_transactions] (transref) INCLUDE (AccountNo)

CREATE INDEX IX_ecmi_payment_history_transref ON [CMS_DB].[dbo].[ecmi_payment_history] (transref) INCLUDE (transdate)

CREATE INDEX IX_ems_payments_receiptnumber ON [CMS_DB].[dbo].[ems_payments] (receiptnumber);

CREATE INDEX IX_ems_payments_billid ON [CMS_DB].[dbo].[ems_payments] (PaymentId);

CREATE INDEX IX_ems_payments_PaymentTransId ON [CMS_DB].[dbo].[ems_payments] (PaymentTransactionId);

CREATE INDEX IX_ems_payments_PayDate ON [CMS_DB].[dbo].[ems_payments] (PayDate);

CREATE INDEX IX_ems_payments_MeterNo ON [CMS_DB].[dbo].[ems_payments] (MeterNo);

CREATE INDEX IX_ems_payments_CustomerID ON [CMS_DB].[dbo].[ems_payments] (CustomerID);













