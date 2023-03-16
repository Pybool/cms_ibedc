let metadata = {"appname": "customers",  "advanced_filters": false, "paginate": true, "can_approve": true, "create_perm": true, "caad_perm": false,has_field:true, current_user: "Devops"}



let field_names = {"Firstname": "firstname", "Surname": "surname", "Othernames": "othernames", "Mobile": "mobile", "Email": "email", "Customer Address": "address", "City": "city", "Account No": "accountno", "Account Type": "accounttype", "Account Balance": "outstanding_amnt", "Business Hub": "buid", "Address 2": "address2", "Meter Model": "meter_model", "Meter Type": "meter_type", "Meter Number": "meterno", "Meter Status": "meter_status", "Meter Manufacturer": "meter_manufacturer", "Manufacture Year": "manufacture_year", "Meter Rating": "meter_rating", "Application Date": "applicationdate", "Giscoordinate": "giscoordinate", "Guarantor Name": "guarantorname", "Guarantor Address": "guarantoraddress", "V Rating": "v_rating", "Meter Class": "meter_classification", "Meter Category": "meter_category", "State": "state", "Account Status": "statuscode", "DSSID": "dss_id", "Service Center": "servicecenter", "Feeder Name": "feeder_name", "Service Band": "service_band"}

let defaults =  ["Surname", "Firstname", "Othernames", "Account No", "Meter Number", "DSS Name", "Mobile", "Email", "Customer Address", "State", "Business Hub", "Service Center", "Feeder Name", "Service Band", "Account Balance", "Account Status", "DSSID", "Meter Status"]

let transients = ["Surname", "Firstname", "Othernames", "Account No", "Meter Number", "Mobile", "Email", "Customer Address", "State", "Business Hub", "Service Center", "Feeder Name", "Service Band", "Account Balance", "Account Status", "DSSID", "Account Type", "City", "Address 2", "Meter Model", "Meter Type", "Meter Manufacturer", "Manufacture Year", "Meter Rating", "Application Date", "Giscoordinate", "Guarantor Name", "Guarantor Address", "V Rating", "Meter Class", "Meter Category", "Meter Status"]

exports.customerData = {
            metadata:metadata,
            customer_data:[],
            field_names:field_names,
            defaults:defaults,
            transients:transients,
            mockresponse:{status:true,data:[]},
            
        }
