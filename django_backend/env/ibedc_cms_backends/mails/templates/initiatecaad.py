template = """
	<head>
		<link rel="stylesheet" href="https://cdn.datatables.net/responsive/2.3.0/css/responsive.bootstrap.css">
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  		<link rel="stylesheet" href="{14}/assets/css/mail.css">
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
	</head>
	<table border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout:fixed;background-color:#f9f9f9" id="bodyTable">
		<tbody>
			<tr>
				<td style="padding-right:10px;padding-left:10px;" align="center" valign="top" id="bodyCell">
					<table border="0" cellpadding="0" cellspacing="0" width="100%" class="wrapperWebview" style="max-width:800px">
						<tbody>
							<tr>
								<td align="center" valign="top">
									<table border="0" cellpadding="0" cellspacing="0" width="100%">
										<tbody>
											<tr>
												
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
					<table border="0" cellpadding="0" cellspacing="0" width="100%" class="wrapperBody" style="max-width:800px">
						<tbody>
							<tr>
								<td align="center" valign="top">
									<table border="0" cellpadding="0" cellspacing="0" width="100%" class="tableCard" style="background-color:#fff;border-color:#e5e5e5;border-style:solid;border-width:0 1px 1px 1px;">
										<tbody>
											<tr>
												<td style="background-color:#00d2f4;font-size:1px;line-height:3px" class="topBorder" height="3">&nbsp;</td>
											</tr>
											<tr>
												<td style="padding-top: 60px; padding-bottom: 20px;" align="center" valign="middle" class="emailLogo">
													<a href="#" style="text-decoration:none" target="_blank">
														<img alt="" border="0" src="{14}/assets/docimages/logo-dark.png" style="width:100%;max-width:36px;max-height:60px;display:block" >
													</a>
												</td>
											</tr>
											<tr>
												<td style="padding-bottom: 20px;" align="center" valign="top" class="imgHero">
													
												</td>
											</tr>
											<tr>
												<td style="padding-bottom: 5px; padding-left: 20px; padding-right: 20px;" align="center" valign="top" class="mainTitle">
													<h2 class="text" style="color:#000;font-family:Poppins,Helvetica,Arial,sans-serif;font-size:28px;font-weight:500;font-style:normal;letter-spacing:normal;line-height:36px;text-transform:none;text-align:center;padding:0;margin:0">Hi "{1}"</h2>
												</td>
											</tr>
											<tr>
												<td style="padding-bottom: 30px; padding-left: 20px; padding-right: 20px;" align="center" valign="top" class="subTitle">
													<h4 class="text" style="color:#999;font-family:Poppins,Helvetica,Arial,sans-serif;font-size:16px;font-weight:500;font-style:normal;letter-spacing:normal;line-height:24px;text-transform:none;text-align:center;padding:0;margin:0">{0}</h4>
                                                    <p style="color:#999;font-family:Poppins,Helvetica,Arial,sans-serif;font-size:16px;font-weight:500;font-style:normal;letter-spacing:normal;line-height:24px;text-transform:none;text-align:center;padding:0;margin:0">Please conduct a second level validation at the premises of the customer in this mail</p>

												</td>
											</tr>
											<tr>
												<td style="padding-left:20px;padding-right:20px" align="center" valign="top" class="containtTable ui-sortable">
												<table class="content">
													<thead class="theader">
														<tr>
														<th>Variable</th>
														<th>Type</th>
														</tr>
													</thead>
													<tbody class="table-content">
														<tr>
														<td style="white-space:nowrap"><strong>Firstname</strong></td>
														<td style="white-space:nowrap">{2}</td>
														</tr>
														<tr>
														<td style="white-space:nowrap"><strong>Surname</strong></td>
														<td style="white-space:nowrap">{3}</td>
														</tr>
														<tr>
														<td style="white-space:nowrap"><strong>Othername</strong></td>
														<td style="white-space:nowrap">{4}</td>
														</tr>
														<tr>
														<td style="white-space:nowrap"><strong>Mobile</strong></td>
														<td style="white-space:nowrap">{5}</td>
														</tr>					
														<tr>
														<td style="white-space:nowrap"><strong>Account No</strong></td>
														<td style="white-space:nowrap">{6}</td>
														</tr>
														<tr>
														<td style="white-space:nowrap"><strong>Meter No</strong></td>
														<td style="white-space:nowrap">{7}</td>
														</tr>
														<tr>
														<td style="white-space:nowrap"><strong>Address</strong></td>
														<td style="white-space:nowrap">{8}</td>
														</tr>
														<tr>
														<td style="white-space:nowrap"><strong>Region</strong></td>
														<td style="white-space:nowrap">{9}</td>
														</tr>
														<tr>
														<td style="white-space:nowrap"><strong>Business Unit</strong></td>
														<td style="white-space:nowrap">{10}</td>
														</tr>
														<tr>
														<td style="white-space:nowrap"><strong>Service Center</strong></td>
														<td style="white-space:nowrap">{11}</td>
														</tr>
														<tr>
														<td style="white-space:nowrap"><strong>DSSID</strong></td>
														<td style="white-space:nowrap">{12}</td>
														</tr>
													</tbody>
													</table>
													
													<table border="0" cellpadding="0" cellspacing="0" width="100%" class="tableButton" style="">
														<tbody>
															<tr>
																<td style="padding-top:20px;padding-bottom:20px" align="center" valign="top">
																	<table border="0" cellpadding="0" cellspacing="0" align="center">
																		<tbody>
																			<tr>
																				<td style="background-color: orange; padding: 12px 35px; border-radius: 50px;" align="center" class="ctaButton"> <a href="{14}/customer/information/basic-information?accountno={6}&accounttype={13}&meterno={7}" style="color:#fff;font-size:13px;letter-spacing:1px;line-height:20px;text-transform:sentencecase;text-decoration:none;display:block" target="_blank" class="text">View Customer Information</a>
																				</td>
																			</tr>
																		</tbody>
																	</table>
																</td>
															</tr>
														</tbody>
													</table>
												</td>
											</tr>
											<tr>
												<td style="font-size:1px;line-height:1px" height="20">&nbsp;</td>
											</tr>
											<tr>
												<td align="center" valign="middle" style="padding-bottom: 40px;" class="emailRegards">
													<!-- Image and Link // -->
													
												</td>
											</tr>
										</tbody>
									</table>
									

									<table border="0" cellpadding="0" cellspacing="0" width="100%" class="space">
										<tbody>
											<tr>
												<td style="font-size:1px;line-height:1px" height="30">&nbsp;</td>
											</tr>
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
					
				</td>
			</tr>
		</tbody>
	</table>
"""

# print(template)

css = """
<style>	
 body {
	background: #fafafa url(https://jackrugile.com/images/misc/noise-diagonal.png);
	color: #444;
	font: 100%/30px 'Helvetica Neue', helvetica, arial, sans-serif;
	text-shadow: 0 1px 0 #fff;
}

strong {
	font-weight: bold; 
}

em {
	font-style: italic; 
}

table.content {
	background: #f5f5f5;
	border-collapse: separate;
	box-shadow: inset 0 1px 0 #fff;
	font-size: 12px;
	line-height: 12px;
	margin: 30px auto;
	text-align: left;
	width: 250px;
}	

.theader th {
	background: url(https://jackrugile.com/images/misc/noise-diagonal.png), linear-gradient(#777, #444);
	border-left: 1px solid #555;
	border-right: 1px solid #777;
	border-top: 1px solid #555;
	border-bottom: 1px solid #333;
	box-shadow: inset 0 1px 0 #999;
	color: #fff;
  font-weight: bold;
	padding: 10px 15px;
	position: relative;
	text-shadow: 0 1px 0 #000;
  text-align: center;
}

.theader th:after {
	background: linear-gradient(rgba(255,255,255,0), rgba(255,255,255,.08));
	content: '';
	display: block;
	height: 25%;
	left: 0;
	margin: 1px 0 0 0;
	position: absolute;
	top: 25%;
	width: 100%;
}

.theader th:first-child {
	border-left: 1px solid #777;	
	box-shadow: inset 1px 1px 0 #999;
}

.theader th:last-child {
	box-shadow: inset -1px 1px 0 #999;
}

.table-content tr td {
	border-right: 1px solid #fff;
	border-left: 1px solid #e8e8e8;
	border-top: 1px solid #fff;
	border-bottom: 1px solid #e8e8e8;
	padding: 10px 15px;
	position: relative;
	transition: all 300ms;
}

.table-content tr td:first-child {
	box-shadow: inset 1px 0 0 #fff;
}	

.table-content tr td:last-child {
	border-right: 1px solid #e8e8e8;
	box-shadow: inset -1px 0 0 #fff;
}	

.table-content tr:last-of-type td {
	box-shadow: inset 0 -1px 0 #fff; 
}

.table-content tr:last-of-type td:first-child {
	box-shadow: inset 1px -1px 0 #fff;
}	

.table-content tr:last-of-type td:last-child {
	box-shadow: inset -1px -1px 0 #fff;
}	

.table-content:hover td {
	color: transparent;
	text-shadow: 0 0 3px #aaa;
}

.table-content:hover tr:hover td {
	color: #444;
	text-shadow: 0 1px 0 #fff;
}
</style>
"""

