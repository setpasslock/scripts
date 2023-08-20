# Use with the mitmproxy -s parameter when listening for packets.
# This will save the contents of the packets as human readable for you.
# -w is unnecessary.
# script in development phase, not stable

from mitmproxy import ctx
from mitmproxy.net.http.http1.assemble import assemble_request, assemble_response

class ResponseLogger:
    def __init__(self):
        self.file = open('/tmp/dumpformitm', 'w', encoding='utf-8')

    def response(self, flow):
        request_data = assemble_request(flow.request).decode('utf-8', 'replace')
        response_data = assemble_response(flow.response).decode('utf-8', 'replace')


        clean_response_data = self.clean_binary_data(response_data)

        self.file.write("\n-------- Request --------\n")
        self.file.write(request_data)
        
        self.file.write("\n-------- Response --------\n")
        self.file.write(clean_response_data)
        
        self.file.write("\n" + "="*50 + "\n")  # seperator for req-response pair

    def clean_binary_data(self, data):
        cleaned_data = data.replace('\x00', '') 
        return cleaned_data

addons = [ResponseLogger()]
 
