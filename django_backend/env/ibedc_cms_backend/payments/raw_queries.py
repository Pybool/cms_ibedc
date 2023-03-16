SINGLE_CUSTOMER_PAYMENTS_EMS = """DECLARE @PageSize INT = '#page_size#';
                                DECLARE @PageNumber INT = '#page_no#';
                                DECLARE @AccountNo NVARCHAR(50) = '#AccountNo#';
                                
                                SELECT  [ems_payments].*, EMSPT.*,
                                (
                                    SELECT COUNT(*)
                                    FROM [CMS_IBEDC_DATABASE].[dbo].[ems_payments]
                                    INNER JOIN [ems_payment_trans] AS EMSPT ON EMSPT.[transid] = [ems_payments].PaymentTransactionId
                                    WHERE [ems_payments].AccountNo = @AccountNo
                                ) AS TotalCount
                                FROM [CMS_IBEDC_DATABASE].[dbo].[ems_payments]
                                INNER JOIN [ems_payment_trans] AS EMSPT ON EMSPT.[transid] = [ems_payments].PaymentTransactionId
                                WHERE [ems_payments].AccountNo = @AccountNo
                                ORDER BY [ems_payments].PaymentTransactionId
                                OFFSET (@PageNumber - 1) * @PageSize ROWS
                                FETCH NEXT @PageSize ROWS ONLY;"""
                                
SINGLE_CUSTOMER_PAYMENTS_ECMI = """"""