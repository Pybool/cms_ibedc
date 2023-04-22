SINGLE_CUSTOMER_PAYMENTS_EMS = """DECLARE @PageSize INT = '#page_size#';
                                DECLARE @PageNumber INT = '#page_no#';
                                DECLARE @AccountNo NVARCHAR(50) = '#AccountNo#';
                                
                                SELECT  [ems_payments].*, EMSPT.*,
                                (
                                    SELECT COUNT(*)
                                    FROM [CMS_DB].[dbo].[ems_payments]
                                    INNER JOIN [ems_payment_trans] AS EMSPT ON EMSPT.[transid] = [ems_payments].PaymentTransactionId
                                    WHERE [ems_payments].AccountNo = '#AccountNo#'
                                ) AS TotalCount
                                FROM [CMS_DB].[dbo].[ems_payments]
                                INNER JOIN [ems_payment_trans] AS EMSPT ON EMSPT.[transid] = [ems_payments].PaymentTransactionId
                                WHERE [ems_payments].AccountNo = '#AccountNo#'
                                ORDER BY [ems_payments].PaymentTransactionId
                                OFFSET (@PageNumber - 1) * @PageSize ROWS
                                FETCH NEXT @PageSize ROWS ONLY;"""
                                
SINGLE_CUSTOMER_PAYMENTS_ECMI = """DECLARE @PageSize INT = '#page_size#';
                                DECLARE @PageNumber INT = '#page_no#';
                                DECLARE @AccountNo NVARCHAR(50) = '#AccountNo#';
                                
                                SELECT  [ecmi_payment_history].*, ECMIPT.*,
                                (
                                    SELECT COUNT(*)
                                    FROM [CMS_DB].[dbo].[ecmi_payment_history]
                                    INNER JOIN [ecmi_transactions] AS ECMIPT ON ECMIPT.[transref] = [ecmi_payment_history].transref
                                    WHERE [ecmi_payment_history].meterno = '#AccountNo#'
                                ) AS TotalCount
                                FROM [CMS_DB].[dbo].[ecmi_payment_history]
                                INNER JOIN [ecmi_transactions] AS ECMIPT ON ECMIPT.[transref] = [ecmi_payment_history].transref
                                WHERE [ecmi_payment_history].MeterNo = '#AccountNo#'
                                ORDER BY [ecmi_payment_history].transdate
                                OFFSET (@PageNumber - 1) * @PageSize ROWS
                                FETCH NEXT @PageSize ROWS ONLY;"""
                                
                                
CUSTOMER_PAYMENTS_ECMI_NO_HIERARCHY = ["""
                                    SELECT count(*)
                                    FROM [CMS_DB].[dbo].[ecmi_payment_history]
                                    INNER JOIN [ecmi_transactions] AS ECMIPT ON ECMIPT.[transref] = [ecmi_payment_history].transref
                                    INNER JOIN [ecmi_customers_new] ON [ecmi_customers_new].AccountNo = ECMIPT.AccountNo
                                    #DATE_CONJUNCTION#
                                    """, 
                                       """DECLARE @PageSize INT = '#page_size#';
                                    DECLARE @PageNumber INT = '#page_no#';                                    
                                    SELECT [ecmi_customers_new].firstname, [ecmi_customers_new].Surname, [ecmi_customers_new].AccountNo, 
                                    [ecmi_customers_new].othernames,[ecmi_customers_new].BUID, 
                                    [ecmi_payment_history].*, ECMIPT.*
                                    FROM [CMS_DB].[dbo].[ecmi_payment_history]
                                    INNER JOIN [ecmi_transactions] AS ECMIPT ON ECMIPT.[transref] = [ecmi_payment_history].transref
                                    INNER JOIN [ecmi_customers_new] ON [ecmi_customers_new].AccountNo = ECMIPT.AccountNo
                                    #DATE_CONJUNCTION#
                                    ORDER BY [ecmi_payment_history].transdate desc
                                    OFFSET (@PageNumber - 1) * @PageSize ROWS
                                    FETCH NEXT @PageSize ROWS ONLY;"""
                                    ]
                                    
                                    
CUSTOMER_PAYMENTS_ECMI_HIERARCHY_REGION = ["""                                    
                                                        
                                        SELECT count(*)
                                        FROM [CMS_DB].[dbo].[ecmi_payment_history]
                                        INNER JOIN [ecmi_transactions] AS ECMIPT ON ECMIPT.[transref] = [ecmi_payment_history].transref
                                        INNER JOIN [ecmi_customers_new] ON [ecmi_customers_new].AccountNo = ECMIPT.AccountNo
                                        WHERE ecmi_customers_new.State = '#REGION#' 
                                        
                                        """  ,
                                        """  DECLARE @PageSize INT = '#page_size#';
                                        DECLARE @PageNumber INT = '#page_no#';                                    
                                        SELECT [ecmi_customers_new].firstname, [ecmi_customers_new].Surname, [ecmi_customers_new].AccountNo, 
                                        [ecmi_customers_new].othernames,[ecmi_customers_new].BUID, 
                                        [ecmi_payment_history].*, ECMIPT.*
                                        FROM [CMS_DB].[dbo].[ecmi_payment_history]
                                        INNER JOIN [ecmi_transactions] AS ECMIPT ON ECMIPT.[transref] = [ecmi_payment_history].transref
                                        INNER JOIN [ecmi_customers_new] ON [ecmi_customers_new].AccountNo = ECMIPT.AccountNo
                                        WHERE ecmi_customers_new.State = '#REGION#'
                                        #DATE_CONJUNCTION#
                                        ORDER BY [ecmi_payment_history].transdate desc
                                        OFFSET (@PageNumber - 1) * @PageSize ROWS
                                        FETCH NEXT @PageSize ROWS ONLY;
                                        """
                                        ]


CUSTOMER_PAYMENTS_ECMI_HIERARCHY_BUSINESS_UNIT = ["""                                    
                                                        
                                                        SELECT count(*)
                                                        FROM [CMS_DB].[dbo].[ecmi_payment_history]
                                                        INNER JOIN [ecmi_transactions] AS ECMIPT ON ECMIPT.[transref] = [ecmi_payment_history].transref
                                                        INNER JOIN [ecmi_customers_new] ON [ecmi_customers_new].AccountNo = ECMIPT.AccountNo
                                                        WHERE ecmi_customers_new.State = '#REGION#' 
                                                        AND ecmi_customers_new.BUID = '#BUID#'
                                                        
                                                        """  ,
                                                        """  DECLARE @PageSize INT = '#page_size#';
                                                        DECLARE @PageNumber INT = '#page_no#';                                    
                                                        SELECT [ecmi_customers_new].firstname, [ecmi_customers_new].Surname, [ecmi_customers_new].AccountNo, 
                                                        [ecmi_customers_new].othernames,[ecmi_customers_new].BUID, 
                                                        [ecmi_payment_history].*, ECMIPT.*
                                                        
                                                        FROM [CMS_DB].[dbo].[ecmi_payment_history]
                                                        INNER JOIN [ecmi_transactions] AS ECMIPT ON ECMIPT.[transref] = [ecmi_payment_history].transref
                                                        INNER JOIN [ecmi_customers_new] ON [ecmi_customers_new].AccountNo = ECMIPT.AccountNo
                                                        WHERE ecmi_customers_new.State = '#REGION#' 
                                                        AND ecmi_customers_new.BUID = '#BUID#'
                                                        #DATE_CONJUNCTION#
                                                        ORDER BY [ecmi_payment_history].transdate desc
                                                        OFFSET (@PageNumber - 1) * @PageSize ROWS
                                                        FETCH NEXT @PageSize ROWS ONLY;
                                                        """  
                                                ]                                  

CUSTOMER_PAYMENTS_ECMI_HIERARCHY_SERVICE_CENTER = [
                                                     """                                    
                                                        
                                                        SELECT count(*)
                                                        FROM [CMS_DB].[dbo].[ecmi_payment_history]
                                                        INNER JOIN [ecmi_transactions] AS ECMIPT ON ECMIPT.[transref] = [ecmi_payment_history].transref
                                                        INNER JOIN [ecmi_customers_new] ON [ecmi_customers_new].AccountNo = ECMIPT.AccountNo
                                                        WHERE ecmi_customers_new.State = '#REGION#'
                                                        #DATE_CONJUNCTION#
                                                        AND ecmi_customers_new.BUID = '#BUID#' 
                                                        AND ecmi_customers_new.[ServiceCenter] ='#SERVICECENTER#'
                                                        
                                                        """  ,
                                                    """  DECLARE @PageSize INT = '#page_size#';
                                                        DECLARE @PageNumber INT = '#page_no#';                                    
                                                        SELECT [ecmi_customers_new].firstname, [ecmi_customers_new].Surname, [ecmi_customers_new].AccountNo, 
                                                        [ecmi_customers_new].othernames,[ecmi_customers_new].BUID, 
                                                        [ecmi_payment_history].*, ECMIPT.*
                                                        FROM [CMS_DB].[dbo].[ecmi_payment_history]
                                                        INNER JOIN [ecmi_transactions] AS ECMIPT ON ECMIPT.[transref] = [ecmi_payment_history].transref
                                                        INNER JOIN [ecmi_customers_new] ON [ecmi_customers_new].AccountNo = ECMIPT.AccountNo
                                                        WHERE ecmi_customers_new.State = '#REGION#' 
                                                        #DATE_CONJUNCTION#
                                                        AND ecmi_customers_new.BUID = '#BUID#' 
                                                        AND ecmi_customers_new.[ServiceCenter] ='#SERVICECENTER#'
                                                        ORDER BY [ecmi_payment_history].transdate desc
                                                        OFFSET (@PageNumber - 1) * @PageSize ROWS
                                                        FETCH NEXT @PageSize ROWS ONLY;
                                                        """
                                                    ]
                                        
                                        
CUSTOMER_PAYMENTS_EMS_NO_HIERARCHY = ["""                                    
                                                        
                                        SELECT count(*)
                                        
                                        FROM [CMS_DB].[dbo].[ems_payments]
                                        INNER JOIN [ems_payment_trans] AS EMSPT ON EMSPT.[transid] = [ems_payments].PaymentTransactionId
                                        INNER JOIN [ems_customers_new] ON [ems_customers_new].AccountNo = EMSPT.AccountNo
                                        #DATE_CONJUNCTION#
                                            
                                            """  ,
                                        """DECLARE @PageSize INT = '#page_size#';
                                        DECLARE @PageNumber INT = '#page_no#';                                    
                                        SELECT [ems_customers_new].firstname, [ems_customers_new].Surname, [ems_customers_new].AccountNo, 
                                        [ems_customers_new].othernames,[ems_customers_new].BUID, 
                                        [ems_payments].*, EMSPT.*
                                        FROM [CMS_DB].[dbo].[ems_payments]
                                        INNER JOIN [ems_payment_trans] AS EMSPT ON EMSPT.[transid] = [ems_payments].PaymentTransactionId
                                        INNER JOIN [ems_customers_new] ON [ems_customers_new].AccountNo = EMSPT.AccountNo
                                        #DATE_CONJUNCTION#
                                        ORDER BY [ems_payments].PayDate desc
                                        OFFSET (@PageNumber - 1) * @PageSize ROWS
                                        FETCH NEXT @PageSize ROWS ONLY;"""
                                    ]
                                        
                                    
CUSTOMER_PAYMENTS_EMS_HIERARCHY_REGION =["""
                                            SELECT count(*)
                                        FROM [CMS_DB].[dbo].[ems_payments]
                                        INNER JOIN [ems_payment_trans] AS EMSPT ON EMSPT.[transid] = [ems_payments].PaymentTransactionId
                                        INNER JOIN [ems_customers_new] ON [ems_customers_new].AccountNo = EMSPT.AccountNo
                                        WHERE ems_customers_new.State = '#REGION#'
                                        #DATE_CONJUNCTION#
                                        
                                         """, 
                                         """  DECLARE @PageSize INT = '#page_size#';
                                        DECLARE @PageNumber INT = '#page_no#';                                    
                                        SELECT [ems_customers_new].firstname, [ems_customers_new].Surname, [ems_customers_new].AccountNo, 
                                        [ems_customers_new].othernames,[ems_customers_new].BUID, 
                                        [ems_payments].*, EMSPT.*
                                        FROM [CMS_DB].[dbo].[ems_payments]
                                        INNER JOIN [ems_payment_trans] AS EMSPT ON EMSPT.[transid] = [ems_payments].PaymentTransactionId
                                        INNER JOIN [ems_customers_new] ON [ems_customers_new].AccountNo = EMSPT.AccountNo
                                        WHERE ems_customers_new.State = '#REGION#'
                                        #DATE_CONJUNCTION#
                                        ORDER BY [ems_payments].PayDate
                                        OFFSET (@PageNumber - 1) * @PageSize ROWS
                                        FETCH NEXT @PageSize ROWS ONLY;
                                        """]


CUSTOMER_PAYMENTS_EMS_HIERARCHY_BUSINESS_UNIT = ["""
                                                 SELECT count(*)
                                        FROM [CMS_DB].[dbo].[ems_payments]
                                        INNER JOIN [ems_payment_trans] AS EMSPT ON EMSPT.[transid] = [ems_payments].PaymentTransactionId
                                        INNER JOIN [ems_customers_new] ON [ems_customers_new].AccountNo = EMSPT.AccountNo
                                        WHERE ems_customers_new.State = '#REGION#' AND ems_customers_new.BUID = '#BUID#'
                                        #DATE_CONJUNCTION#
                                       
                                        """,
                                            """  DECLARE @PageSize INT = '#page_size#';
                                        DECLARE @PageNumber INT = '#page_no#';                                   
                                        SELECT [ems_customers_new].firstname, [ems_customers_new].Surname, [ems_customers_new].AccountNo, 
                                        [ems_customers_new].othernames,[ems_customers_new].BUID, 
                                        [ems_payments].*, EMSPT.*
                                        FROM [CMS_DB].[dbo].[ems_payments]
                                        INNER JOIN [ems_payment_trans] AS EMSPT ON EMSPT.[transid] = [ems_payments].PaymentTransactionId
                                        INNER JOIN [ems_customers_new] ON [ems_customers_new].AccountNo = EMSPT.AccountNo
                                        WHERE ems_customers_new.State = '#REGION#' AND ems_customers_new.BUID = '#BUID#'
                                        #DATE_CONJUNCTION#
                                        ORDER BY [ems_payments].PayDate Desc
                                        OFFSET (@PageNumber - 1) * @PageSize ROWS
                                        FETCH NEXT @PageSize ROWS ONLY;
                                        """  ]                                  

CUSTOMER_PAYMENTS_EMS_HIERARCHY_SERVICE_CENTER = ["""
                                                  SELECT count(*)
                                        FROM [CMS_DB].[dbo].[ems_payments]
                                        INNER JOIN [ems_payment_trans] AS EMSPT ON EMSPT.[transid] = [ems_payments].PaymentTransactionId
                                        INNER JOIN [ems_customers_new] ON [ems_customers_new].AccountNo = EMSPT.AccountNo
                                        WHERE ems_customers_new.State = '#REGION#' 
                                        AND ems_customers_new.BUID = '#BUID#' 
                                        AND ems_customers_new.[ServiceCenter] ='#SERVICECENTER#'
                                        #DATE_CONJUNCTION#
                                                  """,
                                                  """ DECLARE @PageSize INT = '#page_size#';
                                        DECLARE @PageNumber INT = '#page_no#';                                     
                                        SELECT [ems_customers_new].firstname, [ems_customers_new].Surname, [ems_customers_new].AccountNo, 
                                        [ems_customers_new].othernames,[ems_customers_new].BUID, 
                                        [ems_payments].*, EMSPT.*
                                        FROM [CMS_DB].[dbo].[ems_payments]
                                        INNER JOIN [ems_payment_trans] AS EMSPT ON EMSPT.[transid] = [ems_payments].PaymentTransactionId
                                        INNER JOIN [ems_customers_new] ON [ems_customers_new].AccountNo = EMSPT.AccountNo
                                        WHERE ems_customers_new.State = '#REGION#' 
                                        AND ems_customers_new.BUID = '#BUID#' 
                                        AND ems_customers_new.[ServiceCenter] ='#SERVICECENTER#'
                                        #DATE_CONJUNCTION#
                                        ORDER BY [ems_payments].PayDate
                                        OFFSET (@PageNumber - 1) * @PageSize ROWS
                                        FETCH NEXT @PageSize ROWS ONLY;
                                        """]