import os
import subprocess
import xml.etree.ElementTree as ET

directory = '/Users/fmi04/Downloads/lfc-0.1.0-alpha_work/rebeca_files_SWaT_Combine'  # replace with your directory path
safety_property = '/Users/fmi04/Downloads/lfc-0.1.0-alpha_work/SWaT_V2023_attackmodel.property'  # replace with your safety property file path
log_file = 'logfile_SWaT_Combied_new.txt'  # replace with your log file path

result_file = open(log_file, 'a')

with open('logfile_combination_attacks_satisfied_SWaT.txt', 'r') as f:
    log_files = [line.strip() for line in f.readlines()]

total_files = len(log_files)
processed_files = 0

for log_file in log_files:
    # check if file exists in directory or subdirectories
    if not log_file.endswith('.rebeca'):
        log_file += '.rebeca'
    found_file = False
    for root, dirs, files in os.walk(directory):
        if log_file in files:
            found_file = True
            rebeca_file = os.path.join(root, log_file)
            break
    if not found_file:
        print(f"{log_file} not found, skipping...")
        continue

    processed_files += 1
    print(f'Processing file {processed_files} of {total_files}: {log_file}')

    # run RMC and generate output.xml
    rmc_cmd = ['/Library/Java/JavaVirtualMachines/jdk-14.jdk/Contents/Home/bin/java', '-jar', './rmc-2.11.jar', '-s', rebeca_file, '-p', safety_property, '-o', 'rmc', '-v', '2.3', '-e', 'TIMED_REBECA', '-x']
    subprocess.run(rmc_cmd, check=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)

    # compile and run executable
    compile_cmd = 'g++ ./rmc/*.cpp -w -o executable'
    subprocess.run(compile_cmd, check=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)

    run_cmd = ['./executable', '-o', 'output.xml'] 
    subprocess.run(run_cmd, check=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)

    # parse output.xml and write analysis result to log file
    tree = ET.parse('output.xml')
    root = tree.getroot()
    for child in root:
        if child.tag == 'checked-property':
            result = child.find('result').text
            print(f"{log_file}: analysis result: {result}")
            result_file.write(f"{log_file}: analysis result: {result}\n")
            if result == 'assertion failed':
                message = child.find('message').text
                print(f"{log_file}: message: {message}")
                result_file.write(f"{log_file}: message: {message}\n")
    result_file.write(f"{log_file}: -------------------------------------\n")

result_file.close()
