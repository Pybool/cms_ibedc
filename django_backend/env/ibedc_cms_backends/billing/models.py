from django.db import models

# Create your models here.
class EmsBills(models.Model):
    billid = models.CharField(primary_key=True,db_column='BillID', max_length=36)  # Field name made lowercase.
    buid = models.CharField(db_column='BUID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pageno1 = models.IntegerField(db_column='PageNo1', blank=True, null=True)  # Field name made lowercase.
    buname1 = models.CharField(db_column='BUName1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    bmmobile = models.CharField(db_column='BMMobile', max_length=20, blank=True, null=True)  # Field name made lowercase.
    csomobile = models.CharField(db_column='CSOMobile', max_length=20, blank=True, null=True)  # Field name made lowercase.
    accttye = models.CharField(db_column='AcctTye', max_length=50, blank=True, null=True)  # Field name made lowercase.
    accountno = models.CharField(db_column='AccountNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    billyear = models.IntegerField(db_column='BillYear', blank=True, null=True)  # Field name made lowercase.
    billmonth = models.IntegerField(db_column='BillMonth', blank=True, null=True)  # Field name made lowercase.
    billmonthname = models.CharField(db_column='BillMonthName', max_length=10, blank=True, null=True)  # Field name made lowercase.
    customername = models.CharField(db_column='CustomerName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    duedate = models.DateTimeField(db_column='DueDate', blank=True, null=True)  # Field name made lowercase.
    prevbalance = models.DecimalField(db_column='PrevBalance', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    meterno = models.CharField(db_column='MeterNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    payment = models.DecimalField(db_column='Payment', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    serviceaddress1 = models.CharField(db_column='ServiceAddress1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    serviceaddress2 = models.CharField(db_column='ServiceAddress2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    serviceaddress3 = models.CharField(db_column='ServiceAddress3', max_length=255, blank=True, null=True)  # Field name made lowercase.
    adc = models.DecimalField(db_column='ADC', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    adjustment = models.DecimalField(db_column='Adjustment', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    dials = models.IntegerField(db_column='DIALS', blank=True, null=True)  # Field name made lowercase.
    netarrears = models.DecimalField(db_column='NetArrears', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    tariffcode = models.CharField(db_column='TariffCode', max_length=5, blank=True, null=True)  # Field name made lowercase.
    energyreaddate = models.DateTimeField(db_column='EnergyReadDate', blank=True, null=True)  # Field name made lowercase.
    minimumchgreaddate = models.DateTimeField(db_column='MinimumChgReadDate', blank=True, null=True)  # Field name made lowercase.
    minimumcurrentchg = models.DecimalField(db_column='MinimumCurrentChg', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    presentkwh = models.DecimalField(db_column='PresentKWH', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    previouskwh = models.DecimalField(db_column='PreviousKWH', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    demandreaddate = models.DateTimeField(db_column='DemandReadDate', blank=True, null=True)  # Field name made lowercase.
    presentdemand = models.DecimalField(db_column='PresentDemand', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    previousdemand = models.DecimalField(db_column='PreviousDemand', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    multiplier = models.DecimalField(db_column='Multiplier', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    consumptionkwh = models.DecimalField(db_column='ConsumptionKWH', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    consumptionmd = models.DecimalField(db_column='ConsumptionMD', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    currentkwh = models.DecimalField(db_column='CurrentKWH', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    currentmd = models.DecimalField(db_column='CurrentMD', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    rate = models.DecimalField(db_column='Rate', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    fc = models.DecimalField(db_column='FC', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mmf = models.DecimalField(db_column='MMF', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    reconnectionfee = models.DecimalField(db_column='ReconnectionFee', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    lastpay = models.DateTimeField(db_column='LastPay', blank=True, null=True)  # Field name made lowercase.
    currentchgtotal = models.DecimalField(db_column='CurrentChgTotal', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    vat = models.DecimalField(db_column='VAT', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    totaldue = models.DecimalField(db_column='TotalDue', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    customercare = models.CharField(db_column='CustomerCare', max_length=50, blank=True, null=True)  # Field name made lowercase.
    oldacctno = models.CharField(db_column='OldAcctNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    vatno = models.CharField(db_column='VATNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lardate = models.DateTimeField(db_column='LARDate', blank=True, null=True)  # Field name made lowercase.
    lar = models.DecimalField(db_column='LAR', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mobile = models.CharField(db_column='Mobile', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lastpayamount = models.DecimalField(db_column='LastPayAmount', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(max_length=50, blank=True, null=True)
    tariffcodefull = models.CharField(db_column='tariffCodeFull', max_length=10, blank=True, null=True)  # Field name made lowercase.
    isselected = models.BooleanField(db_column='IsSelected', blank=True, null=True)  # Field name made lowercase.
    email2 = models.CharField(max_length=50, blank=True, null=True)
    email3 = models.CharField(max_length=50, blank=True, null=True)
    isconfirmed = models.BooleanField(db_column='IsConfirmed', blank=True, null=True)  # Field name made lowercase.
    issmssent = models.BooleanField(db_column='isSmsSent', blank=True, null=True)  # Field name made lowercase.
    readmode = models.CharField(db_column='ReadMode', max_length=1, blank=True, null=True)  # Field name made lowercase.
    billdate = models.DateTimeField(db_column='Billdate', blank=True, null=True)  # Field name made lowercase.
    rowguid = models.CharField(max_length=36, blank=True, null=True)
    refund = models.DecimalField(db_column='Refund', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    backarrears = models.DecimalField(db_column='BackArrears', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    backcharges = models.DecimalField(db_column='BackCharges', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    backkwh = models.IntegerField(db_column='BackKWH', blank=True, null=True)  # Field name made lowercase.
    bvat = models.DecimalField(db_column='BVat', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    netbackarrears = models.DecimalField(db_column='NetBackArrears', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    grandtotaldue = models.DecimalField(db_column='GrandTotaldue', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    backbalance = models.DecimalField(db_column='BackBalance', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    serviceid = models.CharField(db_column='ServiceID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    bandadjustment = models.DecimalField(db_column='BandAdjustment', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        ordering = ('-billdate',)
        db_table = 'ems_bills'
