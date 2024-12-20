import json
json_input = {
    "obstacles": (
        [[i,i] for i in range(20) if i not in [4,5,14,15]] + 
        [[i,19-i] for i in range(20) if i not in [4,5,14,15]]
    ),
    "rows": 20, 
    "cols": 20
}

with open("input.json", "w") as f:
    json.dump(json_input, f)


