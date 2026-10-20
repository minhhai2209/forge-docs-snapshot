# The Forge REST API

`1curl --request POST \
2 --url '{FORGE_EGRESS_PROXY_URL}/forge/llm/{model}' \
3 --header 'Accept: application/json' \
4 --header 'forge-proxy-authorization: Forge as=app,id=invocation-123' \
5 --header 'Content-Type: application/json' \
6 --data '{
7 "messages": [
8 {
9 "role": "system",
10 "content": "You are a helpful assistant."
11 },
12 {
13 "role": "user",
14 "content": [
15 {
16 "type": "text",
17 "text": "What is the weather like in Melbourne?"
18 }
19 ]
20 }
21 ],
22 "max_completion_tokens": 1000,
23 "temperature": 0.7,
24 "tools": [
25 {
26 "type": "function",
27 "function": {
28 "name": "get_current_weather",
29 "description": "Get the current weather in a given location",
30 "parameters": {
31 "type": "object",
32 "properties": {
33 "location": {
34 "type": "string",
35 "description": "The city and state, e.g. Sydney, NSW"
36 },
37 "unit": {
38 "type": "string",
39 "enum": [
40 "celsius",
41 "fahrenheit"
42 ],
43 "description": "The unit of temperature"
44 }
45 },
46 "required": [
47 "location"
48 ]
49 }
50 }
51 }
52 ],
53 "tool_choice": "auto"
54}'`
