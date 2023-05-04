import os
import subprocess
import xml.etree.ElementTree as ET

directory = '/Users/fmi04/Downloads/lfc-0.1.0-alpha_work/rebeca_files/rebeca_files_lib2'  # replace with your directory path
safety_property = '/Users/fmi04/Downloads/lfc-0.1.0-alpha_work/RPS_V2024_attackmodel.property'  # replace with your safety property file path
log_file = 'logfile_c.txt'  # replace with your log file path

result_file = open(log_file, 'a')

# get a list of all .rebeca files in the directory
rebeca_files = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith('.rebeca')]

total_files = len(rebeca_files)
processed_files = 0

for filename in os.listdir(directory):
    if filename.endswith('.rebeca'):
        rebeca_file = os.path.join(directory, filename)
        rebeca_file_name = os.path.basename(rebeca_file)

        
        processed_files += 1
        print(f'Processing file {processed_files} of {total_files}: {rebeca_file_name}')

        
        # run RMC and generate output.xml
        rmc_cmd = ['/Library/Java/JavaVirtualMachines/jdk-14.jdk/Contents/Home/bin/java', '-jar', './rmc-2.7.6.jar', '-s', rebeca_file, '-p', safety_property, '-o', 'rmc', '-v', '2.1', '-e', 'TimedRebeca', '-x']
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
                print(f"{rebeca_file_name}: analysis result: {result}")
                result_file.write(f"{rebeca_file_name}: analysis result: {result}\n")
                if result == 'assertion failed':
                    message = child.find('message').text
                    print(f"{rebeca_file_name}: message: {message}")
                    result_file.write(f"{rebeca_file_name}: message: {message}\n")
        result_file.write(f"{rebeca_file_name}: -------------------------------------\n")

result_file.close()
