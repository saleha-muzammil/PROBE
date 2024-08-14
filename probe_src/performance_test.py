import subprocess
import datetime
import csv
import time
import os
import shutil
import resource
from dataclasses import dataclass
import psutil
import errno

@dataclass
class Result:
    returncode: int
    stdout: str
    stderr: str
    duration: float
    rusage: resource.struct_rusage

LOG_FILE = "probe_log"
RECORD_DIR = "probe_record"

class ResourcePopen(subprocess.Popen):
    def _try_wait(self, wait_flags):
        try:
            (pid, sts, res) = os.wait4(self.pid, wait_flags)
        except OSError as e:
            if e.errno != errno.ECHILD:
                raise
            pid = self.pid
            sts = 0
        else:
            self.rusage = res
        return (pid, sts)

def resource_call(*popenargs, timeout=None, **kwargs) -> Result:
    with ResourcePopen(*popenargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs) as p:
        start = datetime.datetime.now()
        try:
            stdout, stderr = p.communicate(timeout=timeout)
        except:
            p.kill()
            stdout, stderr = p.communicate()
            raise
        stop = datetime.datetime.now()
        return Result(p.returncode, stdout.decode(), stderr.decode(), (stop - start).total_seconds(), p.rusage)
def cleanup():
    if os.path.exists(LOG_FILE):
        print("Removing log file.")
        subprocess.run("rm probe_log", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if os.path.exists(RECORD_DIR):
        print("Removing record directory.")
        shutil.rmtree(RECORD_DIR)
    time.sleep(3)

def benchmark_command(command: list[str], warmup_iterations: int, benchmark_iterations: int, transcribe_flag: bool) -> list[Result]:
    results = []

    for _ in range(warmup_iterations):
        print(f"Running warmup command: {' '.join(command)}")
        subprocess.run("rm probe_log", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    for _ in range(benchmark_iterations):
        cleanup()
        start_time = datetime.datetime.now()
        print(f"Starting process with command: {' '.join(command)}")
        returncode, rusage, stdout, stderr = resource_call(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        end_time = datetime.datetime.now()
        
        pid = os.getpid()

        result = Result(
            rusage=rusage,
            returncode=returncode,
            stdout=stdout.decode('utf-8'),
            stderr=stderr.decode('utf-8'),
            duration=(end_time - start_time).total_seconds()
        )
        results.append(result)
        time.sleep(3)

        if transcribe_flag:
            start_time = datetime.datetime.now()
            print(f"Running probe transcribe -i {RECORD_DIR} -o {LOG_FILE}")
            returncode, rusage, stdout, stderr = resource_call(["probe", "transcribe", "-i", RECORD_DIR, "-o", LOG_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            end_time = datetime.datetime.now()

            result = Result(
                rusage=rusage,
                returncode=returncode,
                stdout=stdout.decode('utf-8'),
                stderr=stderr.decode('utf-8'),
                duration= (end_time - start_time).total_seconds()
            )
            results.append(result)
            time.sleep(3)

    return results

def write_results_to_csv(writer, command_to_run, phase, results):
    for idx, result in enumerate(results, start=1):
        rusage = result.rusage
        writer.writerow({
            'Command': command_to_run,
            'Phase': phase,
            'Return Code': result.returncode,
            'Duration': result.duration,
            'ru_utime': f"{rusage.ru_utime:.6f}",
            'ru_stime': f"{rusage.ru_stime:.6f}",
            'ru_maxrss': rusage.ru_maxrss,
            'ru_ixrss': rusage.ru_ixrss,
            'ru_idrss': rusage.ru_idrss,
            'ru_isrss': rusage.ru_isrss,
            'ru_minflt': rusage.ru_minflt,
            'ru_majflt': rusage.ru_majflt,
            'ru_nswap': rusage.ru_nswap,
            'ru_inblock': rusage.ru_inblock,
            'ru_oublock': rusage.ru_oublock,
            'ru_msgsnd': rusage.ru_msgsnd,
            'ru_msgrcv': rusage.ru_msgrcv,
            'ru_nsignals': rusage.ru_nsignals,
            'ru_nvcsw': rusage.ru_nvcsw,
            'ru_nivcsw': rusage.ru_nivcsw
        })

def benchmark_with_transcription(commands_to_run: list[str], warmup_count: int, benchmark_count: int):
    with open('benchmark_results.csv', mode='w', newline='') as csv_file:
        fieldnames = [
            'Command', 'Phase', 'Return Code', 'Duration',
            'ru_utime', 'ru_stime', 'ru_maxrss', 'ru_ixrss', 'ru_idrss', 'ru_isrss',
            'ru_minflt', 'ru_majflt', 'ru_nswap', 'ru_inblock', 'ru_oublock',
            'ru_msgsnd', 'ru_msgrcv', 'ru_nsignals', 'ru_nvcsw', 'ru_nivcsw'
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for command_to_run in commands_to_run:
            command_args = command_to_run.split()

            print(f"Running benchmark for command (No PROBE): {command_to_run}")
            transcribe_flag = False
            no_probe_results = benchmark_command(command_args, warmup_count, benchmark_count, transcribe_flag)
            write_results_to_csv(writer, command_to_run, 'No PROBE', no_probe_results)

<<<<<<< HEAD
            # Run ./PROBE record for both execution and transcription
            record_command = f"probe record {command_to_run}"
=======
            cleanup()

<<<<<<< HEAD
            record_command = f"./probe record {command_to_run}"
>>>>>>> 76a5b4b (feat: performance tests for rust)
            print(f"Running benchmark for command (Record): {record_command}")
            record_results = benchmark_command(record_command, warmup_count, benchmark_count, flag)

            for idx, result in enumerate(record_results, start=1):
                writer.writerow({
                    'Command': command_to_run,
                    'Phase': 'Record',
                    'Return Code': result.returncode,
                    'CPU Times': result.cpu_times,
                    'Memory Usage': result.memory_usage,
                    'IO Counters': result.io_counters,
                    'Start Time': result.start_time,
                    'End Time': result.end_time,
                    'Duration (s)': (result.end_time - result.start_time).total_seconds(),
                    'CPU Usage (%)': result.cpu_usage_percent
                })
=======
            record_command_args = ["probe", "record"] + command_args
            print(f"Running benchmark for command (Record): {' '.join(record_command_args)}")
            record_results = benchmark_command(record_command_args, warmup_count, benchmark_count, transcribe_flag)
            write_results_to_csv(writer, command_to_run, 'Record', record_results)
>>>>>>> 3c7eff4 (Update performance_test.py)

<<<<<<< HEAD
            # Run ./PROBE record --no-transcribe for execution only
            no_transcribe_command = f"probe record --no-transcribe {command_to_run}"
=======
            cleanup()

<<<<<<< HEAD
            no_transcribe_command = f"./probe record --no-transcribe {command_to_run}"
>>>>>>> 76a5b4b (feat: performance tests for rust)
            print(f"Running benchmark for command (No Transcribe): {no_transcribe_command}")
            flag = True
            no_transcribe_results = benchmark_command(no_transcribe_command, warmup_count, benchmark_count, flag)

            for idx, result in enumerate(no_transcribe_results, start=1):
                writer.writerow({
                    'Command': command_to_run,
                    'Phase': 'No Transcribe',
                    'Return Code': result.returncode,
                    'CPU Times': result.cpu_times,
                    'Memory Usage': result.memory_usage,
                    'IO Counters': result.io_counters,
                    'Start Time': result.start_time,
                    'End Time': result.end_time,
                    'Duration (s)': (result.end_time - result.start_time).total_seconds(),
                    'CPU Usage (%)': result.cpu_usage_percent
                })
=======
            transcribe_flag = True
            print(f"Running benchmark for command probe no-transcribe: {command_to_run}")
            no_transcribe_args= ["probe", "record", "--no-transcribe"] + command_args
            probe_results = benchmark_command(no_transcribe_args, warmup_count, benchmark_count, transcribe_flag)
            write_results_to_csv(writer, command_to_run, 'no-transcribe', probe_results)
>>>>>>> 3c7eff4 (Update performance_test.py)

<<<<<<< HEAD
                # Run ./PROBE transcribe-only using the temporary probe directory
                if result.returncode == 0:
                    probe_log_dir = result.stdout.strip().split(': ')[-1]  # Extracting the probe log directory
                    transcribe_command = f"probe transcribe-only {probe_log_dir} --output probe_log"
                    print(f"Running transcription for command: {command_to_run}")
                    transcribe_proc = subprocess.run(transcribe_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    transcribe_err = transcribe_proc.stderr
                    if transcribe_proc.returncode == 0:
                        transcribe_duration_seconds = (datetime.datetime.now() - result.end_time).total_seconds()

                        writer.writerow({
                            'Command': command_to_run,
                            'Phase': 'Transcription',
                            'Return Code': transcribe_proc.returncode,
                            'CPU Times': '',
                            'Memory Info': '',
                            'IO Counters': '',
                            'Start Time': result.end_time,
                            'End Time': datetime.datetime.now(),
                            'Duration (s)': transcribe_duration_seconds
                        })

                        print(f"Transcription completed for command: {command_to_run}")
                    else:
                        print(f"Error in transcription for command: {command_to_run}")
                        print(f"Error message:\n{transcribe_err.decode('utf-8')}")
                else:
                    print(f"Skipping transcription for command due to previous error: {command_to_run}")

if __name__ == "__main__":
=======
            cleanup()
<<<<<<< HEAD
         
if __name__ == "__main__":   
>>>>>>> 76a5b4b (feat: performance tests for rust)
    commands_to_run = [
        "echo 'Hello, World!'",
        "ls -l",
        "pwd",
        "head ../flake.nix",
        "python3 -c 'print(2 + 2)'",
        "cat tasks.md"
    ]
    warmup_count = 1
    benchmark_count = 2
=======
>>>>>>> 3c7eff4 (Update performance_test.py)

if __name__ == "__main__":
    commands = [
    "ls -l", 
    "echo Hello World", 
    "pwd",
    "gcc hello_world.c -o hello_world && ./hello_world",   
    "gcc pthreads_example.c -o pthreads_example -lpthread && ./pthreads_example",  
    "python3 hello_world.py",
    "date", 
    "uptime"
]

    benchmark_with_transcription(commands, warmup_count=1, benchmark_count=2)
