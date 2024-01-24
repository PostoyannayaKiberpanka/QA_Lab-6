import json
import subprocess

server_ip = "192.168.4.122"


def client(server_ip):
    try:
        command = f"iperf3 -c {server_ip} -J"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        result, error = process.communicate()

        if process.returncode != 0:
            raise subprocess.CalledProcessError(
                process.returncode, command, output=result
            )

        return result, error

    except subprocess.CalledProcessError as e:
        error_output = json.loads(e.output)
        error_message = error_output.get("error", str(error_output))
        print(f"Script failed with return code {e.returncode}: {error_message}")
        return None, None


def parser(output):
    json_data = json.loads(output)
    result_data = json_data["intervals"]
    return result_data


if __name__ == "__main__":
    result, error = client(server_ip)

    if result:
        result_list = parser(result)
        for interval in result_list:
            transfer = f"{interval['sum']['bytes'] / 1e6:.2f}"
            bitrate = f"{interval['sum']['bits_per_second'] / 1e9:.2f}"
            retr = interval['sum']['retransmits']
            cwnd = f"{interval['streams'][0]['snd_cwnd'] / 1e6:.2f}"
            if float(transfer) > 20 and float(bitrate) > 1.5:
                print(
                    f"Interval: {interval['sum']['start']:.2f}-{interval['sum']['end']:.2f} sec, Transfer: {transfer} "
                    f"Mbytes, Bitrate: {bitrate} Gbits/s, Retr: {retr}, Cwnd: {cwnd} MBytes")
