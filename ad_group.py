from google.ads.googleads.client import GoogleAdsClient

google_ads_client = GoogleAdsClient.load_from_storage("config/google-ads.yaml")


customer_id = "1958588682"
query = """SELECT
    ad_group_criterion.criterion_id,
    ad_group_criterion.keyword.text,
    ad_group_criterion.effective_cpc_bid_micros,
    ad_group_criterion.criterion_id,
    ad_group_criterion.status
FROM
    ad_group_criterion
WHERE
    ad_group_criterion.status = ENABLED"""
query2 = """
SELECT
  customer.conversion_tracking_setting.google_ads_conversion_customer,
  customer.conversion_tracking_setting.conversion_tracking_status,
  customer.conversion_tracking_setting.conversion_tracking_id,
  customer.conversion_tracking_setting.cross_account_conversion_tracking_id
FROM customer"""

google_ads_service = google_ads_client.get_service("GoogleAdsService")

response_1 = google_ads_service.search(customer_id=customer_id, query=query)
response_2 = google_ads_service.search(customer_id=customer_id, query=query2)
print()
with open("output.txt", "w") as f:
    for row in response_1:
        Ad_Group = row.ad_group_criterion.resource_name.split("/")
        ad_group_id = Ad_Group[3].split("~")[0]
        copmain_id = Ad_Group[1]
        f.write(f"Gclid: {row.ad_group_criterion.criterion_id}\n")
        f.write(f"Keyword: {row.ad_group_criterion.keyword.text}\n")
        f.write(f"CPC Bid: {row.ad_group_criterion.effective_cpc_bid_micros}\n")
        f.write(f"Ad Group ID: {ad_group_id}\n")
        f.write(f"Ad Group Status: {row.ad_group_criterion.status}\n")
        f.write(f"Campaign ID: {copmain_id}\n\n")
        f.write("======================\n\n")