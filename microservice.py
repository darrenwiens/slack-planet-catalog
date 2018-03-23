import requests, json, ast

params = Hook['params']['text'].split(' | ')

api_key = params[0]
item_type = params[1]
asset_type = params[2]
cc = float(params[3])
aoi = ast.literal_eval(params[4])

session = requests.Session()
session.auth = (api_key, "")

geometry_filter = {
  "type": "GeometryFilter",
  "field_name": "geometry",
  "config": aoi
}

cloud_filter = {
  "type": "RangeFilter",
  "field_name": "cloud_cover",
  "config": {'lte': cc}
}

permission_filter = {
  "type": "PermissionFilter",
  "config": ["assets.{}:download".format(asset_type)]
}

filters = {
  "type": "AndFilter",
  "config": [geometry_filter, cloud_filter, permission_filter]
}

search_endpoint_request = {
  "item_types": [item_type],
  "filter": filters
}

data = json.dumps(search_endpoint_request)

session.headers['Content-Type'] = 'application/json'
result = session.post(
  'https://api.planet.com/data/v1/quick-search',
  data=data
)

data = json.loads(result.text)

out_data = [i['id'] for i in data['features']]

send_to_slack = session.post(
  Hook['params']['response_url'],
  data='{{"text":"{}" }}'.format(out_data)
)
