import os

# Input .rebeca file
input_file = "RPS_V2024_attackmodel.rebeca"

# List of variables to change
vars_to_change = {
    "sACompromised": {
        "time_var": "sACompromised_time",
        "msg_var": "sAmaliciousMsg",
        "time_vals": [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28],
        "msg_vals": [0, 1, 2]
    },
    "sBCompromised": {
        "time_var": "sBCompromised_time",
        "msg_var": "sBmaliciousMsg",
        "time_vals": [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28],
        "msg_vals": [0, -1, -2]
    },
    "cACompromised": {
        "time_var": "cACompromised_time",
        "msg_var": "cAmaliciousMsg",
        "time_vals": [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28],
        "msg_vals": [-1, 1]
    },
    "cBCompromised": {
        "time_var": "cBCompromised_time",
        "msg_var": "cBmaliciousMsg",
        "time_vals": [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28],
        "msg_vals": [-1, 1]
    },
    "injection_attk": {
        "time_var": "attackTime",
        "msg_var": "maliciousMsg",
        "time_vals": [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28],
        "msg_vals": [0, 2]   
    }
}

# Generate new files for each variable value
for var in vars_to_change:
    input_lines = open(input_file).readlines()
    var_index = [i for i, line in enumerate(input_lines) if var in line][0]
    bool_val = input_lines[var_index].split()[-1].strip(";")
    if bool_val == "true":
        for time_val in vars_to_change[var]["time_vals"]:
            for msg_val in vars_to_change[var]["msg_vals"]:
                # Update variable values
                input_lines[var_index + 1] = f"env int {vars_to_change[var]['time_var']} = {time_val};\n"
                input_lines[var_index + 2] = f"env int {vars_to_change[var]['msg_var']} = {msg_val};\n"

                # Write new file
                file_name = f"{var}_time_{time_val}_msg_{msg_val}_chl2.rebeca"
                with open(file_name, "w") as f:
                    f.writelines(input_lines)
    else:
        print(f"{var} is not true, skipping...")

print("Done!")
