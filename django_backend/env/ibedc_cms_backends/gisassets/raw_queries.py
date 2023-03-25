SINGLE_CUSTOMER_ASSETS_INFO_11KV = """SELECT
                                    E.Surname
                                    ,E.dss_id as dss_id
                                    ,E.AccountNo
                                    ,E.state
                                    ,E.MeterNo
                                    ,D11.DSS_11KV_415V_Name as dss_415v_name
                                    ,D11.DSS_11KV_415V_parent as  dss_415v_parent
                                    ,D11.DSS_11KV_415V_Owner as dss_415v_owner
                                    ,D11.DSS_11KV_415V_Address as dss_415v_address
                                    ,D11.DSS_11KV_415V_Rating as dss_415v_rating
                                    ,D11.assettype as asset_type
                                    ,S.Name AS servicecenter
                                    ,S.Biz_Hub as biz_hub
                                    ,S.Region as region
                                    ,H.HT_11KV_Street
                                    ,H.HT_11KV_Remark
                                    ,F.F11kvFeeder_Name as feeder_name
                                    ,F.F11kvFeeder_parent as feeder_parent
                                                        
                                    ,P.PT_33KV_11KV_Name as pt33kv_11kv_name
                                    ,P.PT_33KV_11KV_Rating as pt33kv_11kv_name
                                    ,P.PT_33KV_11KV_make as pt33kv_11kv_make
                                    ,I.ISS_Name AS iis_name
                                    ,I.longtitude as IIS_longitude
                                    ,I.latitude as IIS_latitude
                                    ,I.naccode as IIS_naccode
                                                            
                                                        
                                FROM

                                    #CUSTOMER_TABLE# as E
                                                            
                                INNER JOIN gis_distribution_substation_11KV_415 AS D11 ON D11.assetid = E.DSS_ID
                                INNER JOIN [gis_Service Units] AS S ON S.name = D11.dss_11kv_415v_owner    
                                INNER JOIN [gis_High_Tension_Pole 11KV] AS H ON H.assetid = D11.dss_11kv_415v_parent   
                                INNER JOIN [gis_11KV Feeder] AS F ON F.assetid = H.ht_11kv_parent 
                                INNER JOIN [gis_Power Transformer 33KV_11KV] AS P ON P.assetid = F.F11kvFeeder_parent
                                INNER JOIN [gis_InjectionSub Station] AS I ON I.assetid = P.pt_33kv_11kv_parent
                                WHERE E.AccountNo = '#AccountNo#'

                            """

SINGLE_CUSTOMER_ASSETS_INFO_33KV = """SELECT 
                                    E.Surname
                                    ,E.dss_id as dss_id
                                    ,E.AccountNo
                                    ,E.state
                                    ,E.MeterNo
                                    ,D33.DSS_33KV_415V_Name as dss_415v_name
                                    ,D33.DSS_33KV_415V_parent as  dss_415v_parent
                                    ,D33.DSS_33KV_415V_Owner as dss_415v_owner
                                    ,D33.DSS_33KV_415V_Address as dss_415v_address
                                    ,D33.DSS_33KV_415V_Rating as dss_415v_rating
                                    ,D33.assettype as asset_type
                                    ,S.Name AS servicecenter
                                    ,S.Biz_Hub as biz_hub
                                    ,S.Region as region
                                    ,H.HT_33KV_Street
                                    ,H.HT_33KV_Remark
                                    ,F.F33kv_Feeder_Name as feeder_name
                                    ,F.F33kv_Feeder_parent as feeder_parent
                                                        
                                    ,P.PT_33KV_11KV_Name as pt33kv_11kv_name
                                    ,P.PT_33KV_11KV_Rating as pt33kv_11kv_name
                                    ,P.PT_33KV_11KV_make as pt33kv_11kv_make
                                    ,I.ISS_Name AS iis_name
                                    ,I.longtitude as IIS_longitude
                                    ,I.latitude as IIS_latitude
                                    ,I.naccode as IIS_naccode
                                                            
                                                        
                                FROM

                                    #CUSTOMER_TABLE# as E
                                                            
                                INNER JOIN gis_distribution_substation_33KV_415 AS D33 ON D33.assetid = E.DSS_ID
                                INNER JOIN [gis_Service Units] AS S ON S.name = D33.dss_33kv_415v_owner    
                                INNER JOIN [High Tension Pole 33KV] AS H ON H.assetid = D33.dss_33kv_415v_parent   
                                INNER JOIN [gis_33KV Feeder] AS F ON F.assetid = H.ht_33kv_parent 
                                INNER JOIN [gis_Power Transformer 33KV_11KV] AS P ON P.assetid = F.F33kv_Feeder_parent
                                INNER JOIN [gis_InjectionSub Station] AS I ON I.assetid = P.pt_33kv_11kv_parent
								WHERE E.AccountNo = '#AccountNo#'
"""

FETCH_GIS_ASSETS_INFO = """ SELECT DSS_11KV_415V_Name as dss_name, assetid FROM [gis_distribution_substation_11KV_415] WHERE dss_11kv_415v_owner = '#dss_owner#'
                                UNION
                            SELECT DSS_33KV_415V_Name,assetid FROM [gis_distribution_substation_33KV_415] WHERE dss_33kv_415v_owner = '#dss_owner#'
                        """
                        
FETCH_GIS_ASSETS_INFO_DSS_OWNER  = """SELECT distinct dss_11kv_415v_owner as dss_owner FROM [gis_distribution_substation_11KV_415]
                                          UNION
                                      SELECT distinct dss_33kv_415v_owner FROM [gis_distribution_substation_33KV_415]"""
                                        
FETCH_GIS_FEEDER_INFO = """   
                            SELECT 
                                    DISTINCT F.assetid,
                                    F.F33kv_Feeder_Name as feeders,
                                    F.assettype 
                            FROM [gis_33KV Feeder]
                            INNER JOIN [gis_distribution_substation_33KV_415] AS D33 ON D33.assetid ='#assetid#'
                                
                            INNER JOIN [High Tension Pole 33KV] AS H ON H.assetid = D33.dss_33kv_415v_parent   
                            INNER JOIN [gis_33KV Feeder] AS F ON F.assetid = H.ht_33kv_parent 

                            UNION

                            SELECT 
                                    DISTINCT F.assetid,
                                    F.F11kvFeeder_Name as feeders,
                                    F.assettype 
                            FROM [gis_11KV Feeder]
                            INNER JOIN [gis_distribution_substation_11KV_415] AS D11 ON D11.assetid ='#assetid#'
                                
                            INNER JOIN [gis_High_Tension_Pole 11KV] AS H ON H.assetid = D11.dss_11kv_415v_parent   
                            INNER JOIN [gis_11KV Feeder] AS F ON F.assetid = H.ht_11kv_parent
                        """