SINGLE_ECMI_CUSTTOMER_METERING_INFO = """SELECT 
                                    ecmi_customers_new.AccountNo,
                                    ecmi_customers_new.MeterNo,
                                    msms_meter_details_tbl.*,
                                    M.*
                                                                        
                                    FROM
                                    ecmi_customers_new
                                    INNER JOIN msms_meter_details_tbl ON msms_meter_details_tbl.meter_number = ecmi_customers_new.MeterNo
                                    INNER JOIN (SELECT * FROM gis_distribution_substation_11KV_415
                                                                        union 
                                                    SELECT * FROM gis_distribution_substation_33KV_415
                                                    ) as gis_distribution_substation_agg
                                    on ecmi_customers_new.DSS_ID = gis_distribution_substation_agg.Assetid
                                    INNER JOIN msms_customers AS M ON M.previous_account_number = ecmi_customers_new.AccountNo
                                    WHERE ecmi_customers_new.AccountNo = '#AccountNo#'
                                

                                    """
                                    
SINGLE_EMS_CUSTTOMER_METERING_INFO = """SELECT 
                                        ems_customers_new.AccountNo,
                                        ems_customers_new.MeterNo,
                                        msms_meter_details_tbl.*
                                                                                                                
                                        FROM
                                        ems_customers_new
                                        INNER JOIN msms_meter_details_tbl ON msms_meter_details_tbl.meter_number = ems_customers_new.MeterNo
                                        INNER JOIN (SELECT * FROM gis_distribution_substation_11KV_415
                                                                            union 
                                                        SELECT * FROM gis_distribution_substation_33KV_415
                                                        ) as gis_distribution_substation_agg
                                        on ems_customers_new.DSS_ID = gis_distribution_substation_agg.Assetid
                                        INNER JOIN msms_customers AS M ON M.previous_account_number = ems_customers_new.AccountNo
                                        WHERE ems_customers_new.AccountNo = '#AccountNo#'"""