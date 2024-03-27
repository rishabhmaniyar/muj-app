from boot import *

api=ShoonyaApiPy()

class login:
    user= "FA164238"
    pwd= "Mali@1967"
    factor2 = api.generateTotp("6755I3PZ6L6GE2K7KBU2G2373Y2565H6")
    # factor2 = "AGFPM9510L"
    vc= "FA164238_U"
    app_key= "632b447eada0340705dd4318db03ce5f"
    imei= "abc1234"

    ret = api.login(userid=user, password=pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)
