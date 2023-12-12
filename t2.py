from google.ads.googleads.client import GoogleAdsClient

from main import google_ads_client



def authorize_gads_api():
    config_path = 'google-ads.yaml'
    credentials_path = 'diesel-monitor.json'
    # version = 'your_api_version'

    gads_client = GoogleAdsClient.load_from_storage(config_path)
    return gads_client


def get_campaign_data(gads_client, customer_id):
    query = (
        f"SELECT ad_group.id, ad_group_criterion.criterion_id, "
        f"ad_group_criterion.keyword.text, metrics.impressions, "
        f"metrics.average_cpc, metrics.cost_micros "
        f"FROM keyword_view "
        f"WHERE segments.date DURING LAST_7_DAYS "
        f"AND ad_group.status = 'ENABLED' "
        f"AND campaign.status = 'ENABLEED' "
        f"AND ad_group_criterion.status = 'ENABLED' "
        f"AND campaign_criterion.status = 'ENABLED' "
        f"AND segments.click_type = 'Sponsored' "
        f"AND customer.id = {customer_id} "
        f"ORDER BY metrics.impressions DESC "
    )
    google_ads_service = google_ads_client.service.google_ads

    response = google_ads_service.search(customer_id, query=query)

    data = []
    for row in response:
        ad_group_id = row.ad_group.id.value
        keyword_id = row.ad_group_criterion.criterion_id.value
        keyword = row.ad_group_criterion.keyword.text.value
        impressions = row.metrics.impressions.value
        avg_cpc_micros = row.metrics.average_cpc.micros_value
        cost_micros = row.metrics.cost_micros.value

        data.append({
            "Ad Group ID": ad_group_id,
            "Keyword ID": keyword_id,
            "Keyword": keyword,
            "Impressions": impressions,
            "Average CPC (Micros)": avg_cpc_micros,
            "Cost (Micros)": cost_micros,
        })

    return data


if __name__ == "__main__":
    customer_id = '2327722076'

    gads_client = authorize_gads_api()
    campaign_data = get_campaign_data(gads_client, customer_id)
    print(campaign_data)

