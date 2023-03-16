"""...Settings for cms application go in here for easy customization..."""

QUERY_SETTINGS = {
    'LIMIT':250,
}

PAGINATION_SETTINGS = {
    'PER_PAGE':250,
    'USERS_PER_PAGE':30,
    'LOCATIONS_PER_PAGE':100,
}

REFUND_THRESHOLDS = {
    "range1_upper_limit":50000,
    "range2_lower_limit":50001,
    "range2_upper_limit":150000,
    "range3_lower_limit":150001,
    "range3_upper_limit":250000,
    "range4_lower_limit":250001,
}

CACHE_CONTROL = "max-age=500"

SETTINGS_CACHE_CONTROL = "max-age=100"

ASYNC_CUSTOMER_CACHE_CONTROL = "max-age=500"

ASYNC_CUSTOMER_CACHE_CONTROL_SHORT = "max-age=200"

ASYNC_PAYMENTS_CACHE_CONTROL = "max-age=500"

ASYNC_PAYMENTS_CACHE_CONTROL_SHORT = "max-age=100"

            