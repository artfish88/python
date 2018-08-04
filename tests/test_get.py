import requests

base_url = 'https://www.mjam.net'
header = {'Authorization': 'Token 9d5cae911bedd4bfa2831684896ffcfa716a3bce'}
params_address = {'address': 'Wels'}
params_cuisine = {'address': 'Wels', 'super_cuisines': 'Asiatisch'}
params_flag = {'address': 'Wels', 'flags': 'deals'}
params_sort = {'address': 'Wels', 'sort': 'orders'}
resp_header = 'application/json'

success = 200
not_allowed = 405


def resp(params, headers):
    return requests.get(
        base_url + '/api/v3/restaurants/search/', params=params, headers=headers)

response = resp(params_address, header)
resp_json = response.json()

def test_response_code():
    assert response.status_code == success

def test_header_conetnt_type():
    assert response.headers.get('content-type') == resp_header

def test_correct_number_of_restaurants_is_returned():
    assert len(resp_json['restaurants']) == 18

def test_address_is_returned():
    assert len(resp_json['restaurants'][0]['address']) != 0
    assert resp_json['restaurants'][0]['address_components']['city'] == 'Wels'

filter = resp(params_cuisine, header)
filter_json = filter.json()

def test_filter_by_cuisine():
    super_cuisines = [x['super_cuisines'] for x in filter_json['restaurants']]
    assert len(filter_json['restaurants']) == 2
    assert filter_json['used_params']['filters']['super_cuisines'][0] == 'Asiatisch'
    assert ['Asiatisch'] in super_cuisines

flag = resp(params_flag, header)
flag_json = flag.json()

def test_filter_by_flag():
    assert len(flag_json['restaurants']) == 2
    assert flag_json['used_params']['filters']['flags'][0] == 'deals'

sort = resp(params_sort, header)
sort_json = sort.json()

def test_sort_by_orders():
    order = [x['orders_for_last_7_days'] for x in sort_json['restaurants']]
    ordered = all(order[i] <= order[i+1] for i in range(len(order)-1))
    assert len(sort_json['restaurants']) == 18
    assert ordered

# Test that POST method is not allowed
def test_post_negative():
    post = requests.post(base_url + '/api/v3/restaurants/search/', params=params_address, headers=header)
    assert post.status_code == not_allowed