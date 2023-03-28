LOCATIONS = """
            SELECT [crm_service_centre].id,
                REGION.name as region, 
                BHUB.name as business_unit,
                [crm_service_centre].name as service_center, 
                COALESCE(BHUB.buid,emsBHUB.BUID) as BUID,
                [crm_service_centre].service_center_address
            FROM [CMS_IBEDC_DATABASE].[dbo].[crm_service_centre]
            INNER JOIN [crm_business_hub] AS BHUB ON BHUB.id = [crm_service_centre].business_hub
            INNER JOIN [crm_region] as REGION ON REGION.id = [crm_service_centre].region
            LEFT JOIN [ems_business_unit] as emsBHUB ON emsBHUB.Name = BHUB.name
            ORDER BY region
  """