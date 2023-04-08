from django.db import models


class EcmiPaymentHistory(models.Model):
    transref = models.CharField(primary_key = True,max_length=360)
    enteredby = models.IntegerField(blank=True, null=True)
    transdate = models.DateTimeField(blank=True, null=True)
    transamount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    transstatus = models.CharField(max_length=10, blank=True, null=True)
    meterno = models.CharField(max_length=20, blank=True, null=True)
    transactionresponsemessage = models.TextField(blank=True, null=True)
    paymenttype = models.IntegerField(blank=True, null=True)
    units = models.DecimalField(db_column='Units', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    costofunits = models.DecimalField(db_column='CostOfUnits', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made
    


    class Meta:
        managed = False
        db_table = 'ecmi_payment_history'
        
class EcmiTransactions(models.Model):
    transactionno = models.IntegerField(primary_key = True,db_column='TransactionNo')  # Field name made lowercase.
    cspclientid = models.CharField(db_column='CSPClientID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    transactiondatetime = models.DateTimeField(db_column='TransactionDateTime', blank=True, null=True)  # Field name made lowercase.
    operatorid = models.CharField(db_column='OperatorID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    meterno = models.CharField(db_column='MeterNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    accountno = models.CharField(db_column='AccountNo', max_length=24, blank=True, null=True)  # Field name made lowercase.
    transactiontype = models.IntegerField(db_column='TransactionType', blank=True, null=True)  # Field name made lowercase.
    units = models.DecimalField(db_column='Units', max_digits=11, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=11, decimal_places=2, blank=True, null=True)  # Field name made lowercase.    costofunits = models.DecimalField(db_column='CostOfUnits', max_digits=11, decimal_places=2, blank=True, null=True)  # Field name made
    fc = models.DecimalField(db_column='FC', max_digits=11, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mmf = models.DecimalField(db_column='MMF', max_digits=11, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    kva = models.DecimalField(db_column='KVA', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    vat = models.DecimalField(db_column='VAT', max_digits=11, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    token = models.CharField(db_column='Token', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tokentype = models.IntegerField(db_column='TokenType', blank=True, null=True)  # Field name made lowercase.
    reasons = models.CharField(db_column='Reasons', max_length=200, blank=True, null=True)  # Field name made lowercase.
    transactioncomplete = models.BooleanField(db_column='TransactionComplete', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(max_length=1, blank=True, null=True)
    status1 = models.CharField(max_length=1, blank=True, null=True)
    buid = models.CharField(db_column='BUID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    transref = models.CharField(max_length=20, blank=True, null=True)
    year = models.IntegerField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    month = models.IntegerField(db_column='Month', blank=True, null=True)  # Field name made lowercase.
    day = models.IntegerField(db_column='Day', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ecmi_transactions'
        
class EmsPayments(models.Model):
    rowguid = models.CharField(max_length=36, blank=True, null=True)
    paymentid = models.CharField(primary_key = True, max_length=360,db_column='PaymentID')  # Field name made lowercase.
    billid = models.CharField(db_column='BillID', max_length=36, blank=True, null=True)  # Field name made lowercase.
    paymenttransactionid = models.CharField(db_column='PaymentTransactionId', max_length=36, blank=True, null=True)  # Field name made lowercase.
    receiptnumber = models.CharField(max_length=20, blank=True, null=True)
    paymentsource = models.CharField(db_column='PaymentSource', max_length=5, blank=True, null=True)  # Field name made lowercase.
    meterno = models.CharField(db_column='MeterNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    accountno = models.CharField(db_column='AccountNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    paydate = models.DateTimeField(db_column='PayDate', blank=True, null=True)  # Field name made lowercase.
    paymonth = models.IntegerField(db_column='PayMonth', blank=True, null=True)  # Field name made lowercase.
    payyear = models.IntegerField(db_column='PayYear', blank=True, null=True)  # Field name made lowercase.
    operatorid = models.IntegerField(db_column='OperatorID', blank=True, null=True)  # Field name made lowercase.
    totaldue = models.DecimalField(db_column='TotalDue', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    payments = models.DecimalField(db_column='Payments', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    balance = models.DecimalField(db_column='Balance', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    processed = models.BooleanField(db_column='Processed', blank=True, null=True)  # Field name made lowercase.
    processeddate = models.DateTimeField(db_column='ProcessedDate', blank=True, null=True)  # Field name made lowercase.
    businessunit = models.CharField(db_column='BusinessUnit', max_length=10, blank=True, null=True)  # Field name made lowercase.
    reconciled = models.BooleanField(db_column='Reconciled', blank=True, null=True)  # Field name made lowercase.
    reconciledby = models.IntegerField(db_column='ReconciledBy', blank=True, null=True)  # Field name made lowercase.
    reversedby = models.IntegerField(db_column='ReversedBy', blank=True, null=True)  # Field name made lowercase.
    batchuniqueid = models.CharField(db_column='BatchUniqueID', max_length=36, blank=True, null=True)  # Field name made lowercase.
    dateengtered = models.DateTimeField(db_column='DateEngtered', blank=True, null=True)  # Field name made lowercase.
    customerid = models.CharField(db_column='CustomerID', max_length=36, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ems_payments'
        

class EmsPaymentTrans(models.Model):
    transid = models.CharField(primary_key = True, max_length=360)
    transref = models.CharField(max_length=30, blank=True, null=True)
    enteredby = models.IntegerField(blank=True, null=True)
    transdate = models.DateTimeField(blank=True, null=True)
    transamount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    transstatus = models.CharField(max_length=10, blank=True, null=True)
    accountno = models.CharField(max_length=20, blank=True, null=True)
    transactionresponsemessage = models.TextField(blank=True, null=True)
    paymenttype = models.IntegerField(blank=True, null=True)
    transactionbusinessunit = models.CharField(db_column='TransactionBusinessUnit', max_length=10, blank=True, null=True)  # Field name made lowercase.
    rowguid = models.CharField(max_length=36, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ems_payment_trans'