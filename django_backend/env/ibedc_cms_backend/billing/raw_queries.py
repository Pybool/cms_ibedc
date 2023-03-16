SINGLE_CUSTOMER_BILLS = """
                        DECLARE @PageSize INT = '#page_size#';
                        DECLARE @PageNumber INT = '#page_no#';
                        DECLARE @AccountNo NVARCHAR(50) = '#AccountNo#';
                        
                        SELECT  *,
                        (
                            SELECT COUNT(*)
                            FROM [CMS_IBEDC_DATABASE].[dbo].[ems_bills]
                            WHERE AccountNo = @AccountNo
                        ) AS TotalCount
                        FROM [CMS_IBEDC_DATABASE].[dbo].[ems_bills]
                        WHERE AccountNo = @AccountNo
                        ORDER BY BillID
                        OFFSET (@PageNumber - 1) * @PageSize ROWS
                        FETCH NEXT @PageSize ROWS ONLY;
                      """
  
  
BILLING_HISTORY_HIERARCHY = """DECLARE @PageSize INT = '#page_size#';
                        DECLARE @PageNumber INT = '#page_no#';
                        DECLARE @Hierarchy VARCHAR(50) = '#hierarchy#';
                        DECLARE @HierarchyValue VARCHAR(50) = '#hierarchy_value#';

                        SELECT ems_bills.*,
                        (
                            SELECT COUNT(*)
                            FROM [CMS_IBEDC_DATABASE].[dbo].[ems_bills]
                            INNER JOIN ems_customers_new ON ems_customers_new.AccountNo = ems_bills.AccountNo
                            WHERE ems_customers_new.#hierarchy# = '#hierarchy_value#'
                        ) AS TotalCount
                        FROM [CMS_IBEDC_DATABASE].[dbo].[ems_bills]
                        INNER JOIN ems_customers_new ON ems_customers_new.AccountNo = ems_bills.AccountNo
                        WHERE ems_customers_new.#hierarchy# = '#hierarchy_value#'
                        ORDER BY ems_bills.BillID
                        OFFSET (@PageNumber - 1) * @PageSize ROWS
                        FETCH NEXT @PageSize ROWS ONLY;
                     """

BILLING_HISTORY_NO_HIERARCHY = """DECLARE @PageSize INT = '#page_size#';
                        DECLARE @PageNumber INT = '#page_no#';
                        DECLARE @Hierarchy VARCHAR(50) = '#hierarchy#';
                        DECLARE @HierarchyValue VARCHAR(50) = '#hierarchy_value#';

                        SELECT ems_bills.*,
                        (
                            SELECT COUNT(*)
                            FROM [CMS_IBEDC_DATABASE].[dbo].[ems_bills]
                            INNER JOIN ems_customers_new ON ems_customers_new.AccountNo = ems_bills.AccountNo
                        ) AS TotalCount
                        FROM [CMS_IBEDC_DATABASE].[dbo].[ems_bills]
                        INNER JOIN ems_customers_new ON ems_customers_new.AccountNo = ems_bills.AccountNo
                        ORDER BY ems_bills.BillID
                        OFFSET (@PageNumber - 1) * @PageSize ROWS
                        FETCH NEXT @PageSize ROWS ONLY;
                     """