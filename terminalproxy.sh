#!/bin/bash
firefox-esr -P Proxy 2>/dev/null &
mitmproxy --listen-port 8383 --listen-host 127.0.0.1
