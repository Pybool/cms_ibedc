SINGLE_CUSTOMER_BILLS = """
                       
                        
                        SELECT  *,
                        (
                            SELECT COUNT(*)
                            FROM [CMS_DB].[dbo].[ems_bills]
                            WHERE AccountNo = '#AccountNo#'
                        ) AS TotalCount
                        FROM [CMS_DB].[dbo].[ems_bills]
                        WHERE AccountNo = '#AccountNo#'
                        ORDER BY Billdate desc
                        
                      """
  
  
BILLING_HISTORY_HIERARCHY_REGION = """DECLARE @PageSize INT = '#page_size#';
                        DECLARE @PageNumber INT = '#page_no#';
                        DECLARE @Hierarchy VARCHAR(50) = '#hierarchy#';
                        DECLARE @HierarchyValue VARCHAR(50) = '#hierarchy_value#';

                        SELECT ems_bills.*,
                        (
                            SELECT COUNT(*)
                            FROM [CMS_DB].[dbo].[ems_bills]
                            INNER JOIN ems_customers_new ON ems_customers_new.AccountNo = ems_bills.AccountNo
                            WHERE ems_customers_new.#hierarchy# = '#hierarchy_value#'
                        ) AS TotalCount
                        FROM [CMS_DB].[dbo].[ems_bills]
                        INNER JOIN ems_customers_new ON ems_customers_new.AccountNo = ems_bills.AccountNo
                        WHERE ems_customers_new.#hierarchy# = '#hierarchy_value#'
                        #DATE_CONJUNCTION#
                        ORDER BY ems_bills.DueDate DESC
                        OFFSET (@PageNumber - 1) * @PageSize ROWS
                        FETCH NEXT @PageSize ROWS ONLY;
                     """
                

BILLING_HISTORY_HIERARCHY_BUID = """DECLARE @PageSize INT = '#page_size#';
                        DECLARE @PageNumber INT = '#page_no#';
                        DECLARE @Hierarchy VARCHAR(50) = '#hierarchy#';
                        DECLARE @HierarchyValue VARCHAR(50) = '#hierarchy_value#';

                        SELECT ems_bills.*
                        FROM [CMS_DB].[dbo].[ems_bills]
                        INNER JOIN ems_customers_new ON ems_customers_new.AccountNo = ems_bills.AccountNo
                        WHERE ems_customers_new.#hierarchy# = '#hierarchy_value#'
                        #DATE_CONJUNCTION#
                        AND ems_customers_new.BUID = '#BUID#'
                        ORDER BY ems_bills.DueDate DESC
                        OFFSET (@PageNumber - 1) * @PageSize ROWS
                        FETCH NEXT @PageSize ROWS ONLY;
                       
                     """
COUNT_BILLING_HISTORY_HIERARCHY_BUID = """DECLARE @PageSize INT = '#page_size#';
                        DECLARE @PageNumber INT = '#page_no#';
                        DECLARE @Hierarchy VARCHAR(50) = '#hierarchy#';
                        DECLARE @HierarchyValue VARCHAR(50) = '#hierarchy_value#';

                            SELECT COUNT(*)
                            FROM [CMS_DB].[dbo].[ems_bills]
                            INNER JOIN ems_customers_new ON ems_customers_new.AccountNo = ems_bills.AccountNo
                            WHERE ems_customers_new.#hierarchy# = '#hierarchy_value#'
                            #DATE_CONJUNCTION#
                            AND ems_customers_new.BUID = '#BUID#'
                        
                     """
                     

BILLING_HISTORY_HIERARCHY_SERVICECENTER = """DECLARE @PageSize INT = '#page_size#';
                        DECLARE @PageNumber INT = '#page_no#';
                        DECLARE @Hierarchy VARCHAR(50) = '#hierarchy#';
                        DECLARE @HierarchyValue VARCHAR(50) = '#hierarchy_value#';

                        SELECT ems_bills.*,
                        (
                            SELECT COUNT(*)
                            FROM [CMS_DB].[dbo].[ems_bills]
                            INNER JOIN ems_customers_new ON ems_customers_new.AccountNo = ems_bills.AccountNo
                            WHERE ems_customers_new.#hierarchy# = '#hierarchy_value#'
                            AND ems_customers_new.BUID = '#BUID#'
                            AND ems_customers_new.servicecenter = '#SERVICECENTER#"
                        ) AS TotalCount
                        FROM [CMS_DB].[dbo].[ems_bills]
                        INNER JOIN ems_customers_new ON ems_customers_new.AccountNo = ems_bills.AccountNo
                        WHERE ems_customers_new.#hierarchy# = '#hierarchy_value#'
                        AND ems_customers_new.BUID = '#BUID#'
                        AND ems_customers_new.servicecenter = '#SERVICECENTER#"
                        #DATE_CONJUNCTION#
                        ORDER BY ems_bills.DueDate DESC
                        OFFSET (@PageNumber - 1) * @PageSize ROWS
                        FETCH NEXT @PageSize ROWS ONLY;
                     """                    


BILLING_HISTORY_NO_HIERARCHY = """DECLARE @PageSize INT = '#page_size#';
                        DECLARE @PageNumber INT = '#page_no#';

                        SELECT  *
                        FROM [CMS_DB].[dbo].[ems_bills]
                        INNER JOIN ems_customers_new as EMS on EMS.AccountNo = [CMS_DB].[dbo].[ems_bills].AccountNo
                        WHERE EMS.state='Oyo' AND EMS.BUID = '21A'
                        #DATE_CONJUNCTION#
                        ORDER BY Billdate desc
                        OFFSET (@PageNumber - 1) * @PageSize ROWS
                        FETCH NEXT @PageSize ROWS ONLY;
                     """
                     
                     
"""BILLING HISTORY SEARCH QUERIES BELOW"""

SEARCH_BILLING_HISTORY_HIERARCHY_REGION = """DECLARE @PageSize INT = '#page_size#';
                        DECLARE @PageNumber INT = '#page_no#';
                        DECLARE @Hierarchy VARCHAR(50) = '#hierarchy#';
                        DECLARE @HierarchyValue VARCHAR(50) = '#hierarchy_value#';

                        SELECT ems_bills.*,
                        (
                            SELECT COUNT(*)
                            FROM [CMS_DB].[dbo].[ems_bills]
                            INNER JOIN ems_customers_new ON ems_customers_new.AccountNo = ems_bills.AccountNo
                            WHERE ems_customers_new.#hierarchy# = '#hierarchy_value#'
                        ) AS TotalCount
                        FROM [CMS_DB].[dbo].[ems_bills]
                        INNER JOIN ems_customers_new ON ems_customers_new.AccountNo = ems_bills.AccountNo
                        WHERE ems_customers_new.#hierarchy# = '#hierarchy_value#' #CONJUNCTION#
                        #DATE_CONJUNCTION#
                        ORDER BY ems_bills.DueDate DESC
                        OFFSET (@PageNumber - 1) * @PageSize ROWS
                        FETCH NEXT @PageSize ROWS ONLY;
                     """
                

SEARCH_BILLING_HISTORY_HIERARCHY_BUID = """DECLARE @PageSize INT = '#page_size#';
                        DECLARE @PageNumber INT = '#page_no#';
                        DECLARE @Hierarchy VARCHAR(50) = '#hierarchy#';
                        DECLARE @HierarchyValue VARCHAR(50) = '#hierarchy_value#';

                        SELECT ems_bills.*
                        FROM [CMS_DB].[dbo].[ems_bills]
                        INNER JOIN ems_customers_new ON ems_customers_new.AccountNo = ems_bills.AccountNo
                        WHERE ems_customers_new.#hierarchy# = '#hierarchy_value#' #CONJUNCTION#
                        AND ems_customers_new.BUID = '#BUID#'
                        #DATE_CONJUNCTION#
                        ORDER BY ems_bills.DueDate DESC
                        OFFSET (@PageNumber - 1) * @PageSize ROWS
                        FETCH NEXT @PageSize ROWS ONLY;
                     """
                     
COUNT_SEARCH_BILLING_HISTORY_HIERARCHY_BUID = """SELECT COUNT(*)
                            FROM [CMS_DB].[dbo].[ems_bills]
                            INNER JOIN ems_customers_new ON ems_customers_new.AccountNo = ems_bills.AccountNo
                            WHERE ems_customers_new.#hierarchy# = '#hierarchy_value#' #CONJUNCTION#
                            AND ems_customers_new.BUID = '#BUID#'
                            #DATE_CONJUNCTION#
                            
                            """
SEARCH_BILLING_HISTORY_HIERARCHY_SERVICECENTER = """DECLARE @PageSize INT = '#page_size#';
                                                    DECLARE @PageNumber INT = '#page_no#';
                                                    DECLARE @Hierarchy VARCHAR(50) = '#hierarchy#';
                                                    DECLARE @HierarchyValue VARCHAR(50) = '#hierarchy_value#';

                                                    SELECT ems_bills.*,
                                                    (
                                                        SELECT COUNT(*)
                                                        FROM [CMS_DB].[dbo].[ems_bills]
                                                        INNER JOIN ems_customers_new ON ems_customers_new.AccountNo = ems_bills.AccountNo
                                                        WHERE ems_customers_new.#hierarchy# = '#hierarchy_value#'
                                                        AND ems_customers_new.BUID = '#BUID#'
                                                        AND ems_customers_new.servicecenter = '#SERVICECENTER#"
                                                    ) AS TotalCount
                                                    FROM [CMS_DB].[dbo].[ems_bills]
                                                    INNER JOIN ems_customers_new ON ems_customers_new.AccountNo = ems_bills.AccountNo
                                                    WHERE ems_customers_new.#hierarchy# = '#hierarchy_value#' #CONJUNCTION#
                                                    AND ems_customers_new.BUID = '#BUID#'
                                                    AND ems_customers_new.servicecenter = '#SERVICECENTER#"
                                                    #DATE_CONJUNCTION#
                                                    ORDER BY ems_bills.DueDate DESC
                                                    OFFSET (@PageNumber - 1) * @PageSize ROWS
                                                    FETCH NEXT @PageSize ROWS ONLY;
                                                """                    


SEARCH_BILLING_HISTORY_NO_HIERARCHY = """DECLARE @PageSize INT = '#page_size#';
                        DECLARE @PageNumber INT = '#page_no#';

                        SELECT  *
                        FROM [CMS_DB].[dbo].[ems_bills]
                        INNER JOIN ems_customers_new as EMS on EMS.AccountNo = [CMS_DB].[dbo].[ems_bills].AccountNo
                        WHERE EMS.state='Oyo' #CONJUNCTION#
                        #DATE_CONJUNCTION#
                        ORDER BY Billdate desc
                        OFFSET (@PageNumber - 1) * @PageSize ROWS
                        FETCH NEXT @PageSize ROWS ONLY;
                     """