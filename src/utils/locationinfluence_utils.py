import pycountry 
import base64
import os

def get_png(country_name):
    exceptions = {"turkey": "TR",
                  "ascension island": "AC"}
    
    if country_name.lower() in exceptions:
        code = exceptions[country_name.lower()].lower()
    else:
        code = pycountry.countries.search_fuzzy(country_name)[0].alpha_2.lower()
    return os.path.abspath("./src/utils/flags/" + code + ".png")

def get_base64_flag(country_name):
    image_path = get_png(country_name)
    # Read in binary mode!
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
        
    return f"data:image/png;base64,{base64_image}"

