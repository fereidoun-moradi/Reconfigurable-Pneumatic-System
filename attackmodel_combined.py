
import itertools
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
        "msg_vals": [0, 1, 2]
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



for var1, var2 in itertools.combinations(vars_to_change.keys(), 2):
    if vars_to_change[var1]["time_vals"] and vars_to_change[var1]["msg_vals"] and vars_to_change[var2]["time_vals"] and vars_to_change[var2]["msg_vals"]:
        input_lines = open(input_file).readlines()
        var1_index = [i for i, line in enumerate(input_lines) if var1 in line][0]
        bool_val1 = input_lines[var1_index].split()[-1].strip(";")
        var2_index = [i for i, line in enumerate(input_lines) if var2 in line][0]
        bool_val2 = input_lines[var2_index].split()[-1].strip(";")
        if bool_val1 == "true" and bool_val2 == "true":
            for time_val1 in vars_to_change[var1]["time_vals"]:
                for msg_val1 in vars_to_change[var1]["msg_vals"]:
                    for time_val2 in vars_to_change[var2]["time_vals"]:
                        for msg_val2 in vars_to_change[var2]["msg_vals"]:
                            # Update variable values
                            input_lines[var1_index + 1] = f"env int {vars_to_change[var1]['time_var']} = {time_val1};\n"
                            input_lines[var1_index + 2] = f"env int {vars_to_change[var1]['msg_var']} = {msg_val1};\n"
                            input_lines[var2_index + 1] = f"env int {vars_to_change[var2]['time_var']} = {time_val2};\n"
                            input_lines[var2_index + 2] = f"env int {vars_to_change[var2]['msg_var']} = {msg_val2};\n"
                            
                            # Write new file
                            file_name = f"{var1}_time_{time_val1}_msg_{msg_val1}_{var2}_time_{time_val2}_msg_{msg_val2}.rebeca"
                            with open(file_name, "w") as f:
                                f.writelines(input_lines)
        else:
            print(f"{var1} and/or {var2} is not true, skipping...")
    else:
        print(f"{var1} and/or {var2} does not have enough values, skipping...")

print("Done!")
