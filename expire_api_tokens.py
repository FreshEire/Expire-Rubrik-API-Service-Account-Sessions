import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# User input
rubrik_ip=input("Please enter Rubrik node IP: ") 
api_token=input("Please enter admin API token: ")
print("\n")

basic_headers = {"accept": "application/json", "authorization": f"Bearer {api_token}", "Content-Type": "application/json"} 

# List Service Accounts
list_sa_url = f"https://{rubrik_ip}/api/v1/principal?is_service_account=true&limit=51&offset=0&sort_by=Name&sort_order=asc" 
try: 
    list_sa_response = requests.get(list_sa_url, headers=basic_headers, verify=False) 
    if list_sa_response.status_code == 200:
        sa_user_details = list_sa_response.json()
    else: 
        print(f"Request failed with status code {list_sa_response.status_code}") 
except Exception as e: 
    print(f"An error occurred: {e}")

# Choose which user to clear tokens for
sa_usernames = []
username_count = 0

print("Service Account User List: ")
for user in sa_user_details['data']:
    username_count += 1
    sa_usernames.append(user['name'])
    print(str(username_count) + ". " + user['name'])

while True:
    user_choice = int(input("\nPlease choose a user from the list (input the number): ")) - 1
    if user_choice in range(username_count):
        selected_user_name = sa_usernames[user_choice]
        break
    else:
        print("\nPlease input a valid selection")

for user in sa_user_details['data']:
    if user['name'] == selected_user_name:
        selected_user_id = user['id']
        selected_user_id_truncated = selected_user_id[7:]
        print(f"\nSelected user is: " + selected_user_name + " with ID: " + selected_user_id)
        
        
# Get currently open sessions for the user
get_open_sessions_url = f"https://{rubrik_ip}/api/internal/session?user_id={selected_user_id_truncated}" 
try: 
    get_open_sessions_response = requests.get(get_open_sessions_url, headers=basic_headers, verify=False) 
    if get_open_sessions_response.status_code == 200:
        open_sessions_details = get_open_sessions_response.json()
    else: 
        print(f"Request failed with status code {get_open_sessions_response.status_code}") 
except Exception as e: 
    print(f"An error occurred: {e}")

open_sessions_list = []

print(f"\nThere are currently " + str(open_sessions_details['total']) + " open sessions for user " + selected_user_name + ":")
for session in open_sessions_details['data']:
    open_sessions_list.append(session['id'])

print(open_sessions_list)

# Validate and process request

while True:
    if open_sessions_details['total'] > 0:
        user_confirmation = input("\nAre you sure you wish to clear API sessions for user " + selected_user_name + " Y/N?: ")
        if user_confirmation.lower() == "y":
            
            print("\nConfirmed token delete... processing...")
            
            delete_sessions_url = f"https://{rubrik_ip}/api/internal/session/bulk_delete"
            delete_sessions_data = {
                "tokenIds": open_sessions_list,
                "userId": selected_user_id_truncated
            }
            
            try: 
                delete_sessions_response = requests.post(delete_sessions_url, headers=basic_headers, json=delete_sessions_data, verify=False) 
                if delete_sessions_response.status_code == 204:
                    #print(delete_sessions_response.json())
                    print(f"\nSessions successfully deleted for user {selected_user_name}\n")
                else: 
                    print(f"Request failed with status code {delete_sessions_response.status_code}") 
            except Exception as e: 
                print(f"An error occurred: {e}")
                
            break
        
        elif user_confirmation.lower() == "n":
            print("\n\"No\" selected, exiting...")
            break
        else:
            print("\nPlease enter a valid choice (Y/N)")
            continue
    else:
        print("\nExiting...")
        break