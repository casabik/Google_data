from google.ads.googleads.client import GoogleAdsClient

google_ads_client = GoogleAdsClient.load_from_storage("config/google-ads.yaml")


customer_id = "1958588682"
query = """SELECT
    click_view.ad_group_ad,
    click_view.resource_name,
    click_view.gclid,
    click_view.page_number,
    click_view.ad_group_ad,
    click_view.user_list,
    click_view.keyword,
    click_view.keyword_info.match_type,
    click_view.keyword_info.text
FROM
    click_view
WHERE
    segments.date =  '2023-11-12'
    """   

google_ads_service = google_ads_client.get_service("GoogleAdsService")

response = google_ads_service.search(customer_id=customer_id, query=query)
print(response)