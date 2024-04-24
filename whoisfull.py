import argparse
import requests
import json

arg_parser = argparse.ArgumentParser(description="Whois Full Text Searcher")
arg_parser.add_argument("-t", "--text",required=True, help="Search Text")
arg_parser.add_argument("-t", "--text",required=True, help="Search Text")


args = vars(arg_parser.parse_args())
query_text = args["text"]

API_PATH = "https://apps.db.ripe.net/db-web-ui/api/rest/fulltextsearch/select?facet=true&format=xml&hl=false&"

quer_parts = []

headers = {
    "Accept" : "application/json, text/plain, */*",
}

file_name = query_text


def format_set_and(query_text):
    if " " in query_text:
        parts_q = query_text.split(" ")
        for part in parts_q:
            new_part = '"'+part+'"'
            query_text = query_text.replace(part,new_part)
        
    
        query_text = query_text.replace(" "," AND ")
    else:
        query_text = '"'+query_text+'"'
         
    
    q_for = f"q=({query_text})&start=0&wt=json"
    
    return q_for



def main():
    q_for = format_set_and(query_text=query_text)
    
    URL = API_PATH+q_for
    req = requests.get(URL,headers=headers)
    json_response = req.text
    
    print(json_response)
    
    # with open(f"{file_name}-output.json", "w") as file:
    #     file.write(json_response)
        
    
    
    

main()
