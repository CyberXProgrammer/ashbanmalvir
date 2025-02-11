import requests
import random
from urllib.parse import quote

def get_profile(session_id, device_id, iid):
    """Retrieve the current TikTok username for a given session, device, and iid."""
    try:
        url = f"https://api.tiktokv.com/passport/account/info/v2/?id=kaa&version_code=34.0.0&language=en&app_name=lite&app_version=34.0.0&carrier_region=SA&device_id=7256623439258404357&tz_offset=10800&mcc_mnc=42001&locale=en&sys_region=SA&aid=473824&screen_width=1284&os_api=18&ac=WIFI&os_version=17.3&app_language=en&tz_name=Asia/Riyadh&carrier_region1=SA&build_number=340002&device_platform=iphone&iid=7353686754157692689&device_type=iPhone13,4"
        headers = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": f"sessionid={session_id}",
            "sdk-version": "2",
            "user-agent": "com.zhiliaoapp.musically/432424234 (Linux; U; Android 5; en; fewfwdw; Build/PI;tt-ok/3.12.13.1)",
        }
        
        response = requests.get(url, headers=headers, cookies={"sessionid": session_id})
        return response.json().get("data", {}).get("username", "None")
    except Exception as e:
        return "None"


def check_is_changed(last_username, session_id, device_id, iid):
    """Check if the username has been changed in the TikTok profile."""
    return get_profile(session_id, device_id, iid) != last_username


def change_username(session_id, device_id, iid, last_username, new_username):
    """Attempt to change a TikTok username."""
    data = f"aid=364225&unique_id={quote(new_username)}"
    parm = f"aid=364225&residence=&device_id={device_id}&version_name=1.1.0&os_version=17.4.1&iid={iid}&app_name=tiktok_snail&locale=en&ac=4G&sys_region=SA&version_code=1.1.0&channel=App%20Store&op_region=SA&os_api=18&device_brand=iPad&idfv=16045E07-1ED5-4350-9318-77A1469C0B89&device_platform=iPad&device_type=iPad13,4&carrier_region1=&tz_name=Asia/Riyadh&account_region=sa&build_number=11005&tz_offset=10800&app_language=en&carrier_region=&current_region=&aid=364225&mcc_mnc=&screen_width=1284&uoo=1&content_language=&language=en&cdid=B75649A607DA449D8FF2ADE97E0BC3F1&openudid=7b053588b18d61b89c891592139b68d918b44933&app_version=1.1.0"
    
    sig = run(parm, md5(data.encode("utf-8")).hexdigest() if data else None, None)  
    url = f"https://api.tiktokv.com/aweme/v1/commit/user/?{parm}"
    headers = {
        "Connection": "keep-alive",
        "User-Agent": "Whee 1.1.0 rv:11005 (iPad; iOS 17.4.1; en_SA@calendar=gregorian) Cronet",
        "Cookie": f"sessionid={session_id}",
    }
    headers.update(sig)
    response = requests.post(url, data=data, headers=headers)
    result = response.text
    if "unique_id" in result:
        if check_is_changed(last_username, session_id, device_id, iid):
            return "Username change successful."
        else:
            return "Failed to change username: " + str(result)
    else:
        return "Failed to change username: " + str(result)


def process_ids(input_file, output_file):
    """Process session IDs from an input file and save successful ones to an output file."""
    with open(input_file, 'r') as infile, open(output_file, 'a') as outfile:
        for line in infile:
            session_id = line.strip()
            device_id = str(random.randint(777777788, 999999999999))
            iid = str(random.randint(777777788, 999999999999))
            
            username = get_profile(session_id, device_id, iid)
            if username != "None":
                print(f"Session ID: {session_id} - Username: {username}")
                if username != "dummy_username":
                    with open(output_file, 'a') as outfile:
                        outfile.write(f"Session ID: {session_id} - Username: {username}\n")
            else:
                print(f"Session ID: {session_id} - Username: Invalid session ID or username not found")


def main():
    """Main function to handle file processing."""
    input_file = "ids.txt"
    output_file = "sid.txt"
    process_ids(input_file, output_file)
    print("Processing complete. Successful session IDs saved to sid.txt.")


if __name__ == "__main__":
    main()
