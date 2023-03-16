SINGLE_ECMI_CUSTTOMER_METERING_INFO = """SELECT 
                                    ecmi_customers_new.AccountNo,
                                    ecmi_customers_new.MeterNo,
                                    msms_meter_details_tbl.*,
                                    M.*
                                                                        
                                    FROM
                                    ecmi_customers_new
                                    LEFT OUTER JOIN msms_meter_details_tbl ON msms_meter_details_tbl.meter_number = ecmi_customers_new.MeterNo
                                    LEFT OUTER JOIN (SELECT * FROM gis_distribution_substation_11KV_415
                                                                        union 
                                                    SELECT * FROM gis_distribution_substation_33KV_415
                                                    ) as gis_distribution_substation_agg
                                    on ecmi_customers_new.DSS_ID = gis_distribution_substation_agg.Assetid
                                    LEFT OUTER JOIN msms_customers AS M ON M.previous_account_number = ecmi_customers_new.AccountNo
                                    WHERE ecmi_customers_new.AccountNo = '#AccountNo#'
                                    ORDER BY ecmi_customers_new.Surname

                                    """
                                    
SINGLE_EMS_CUSTTOMER_METERING_INFO = """"""