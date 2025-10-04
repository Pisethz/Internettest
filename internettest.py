import speedtest
import datetime

BANNER = r'''
  ____  _          _   _         
 |  _ \(_)___  ___| |_| |__  ____
 | |_) | / __|/ _ \ __| '_ \|_  /
 |  __/| \__ \  __/ |_| | | |/ / 
 |_|   |_|___/\___|\__|_| |_/___|
         Internet Speed Test
       Pisethz x JackyJackyHunt
'''

def format_speed(bits_per_sec):
    mbps = bits_per_sec / 1_000_000
    mBps = bits_per_sec / 8 / 1_000_000
    return f"{mbps:.2f} Mbps ({mBps:.2f} MB/s)"

def run_speedtest():
    print(BANNER)
    print(f"Test started at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        st = speedtest.Speedtest()
        print("Finding best server...")
        best = st.get_best_server()
        print(f"Server: {best['sponsor']} ({best['name']}, {best['country']}) [{best['host']}]\n")
        print("Testing download speed...")
        download_speed = st.download()
        print("Testing upload speed...")
        upload_speed = st.upload()
        ping_result = st.results.ping
        print("\n--- Test Results ---")
        print(f"Ping: {ping_result:.2f} ms")
        print(f"Download: {format_speed(download_speed)}")
        print(f"Upload:   {format_speed(upload_speed)}")
        print(f"ISP: {st.results.client.get('isp', 'Unknown')}")
        print(f"External IP: {st.results.client.get('ip', 'Unknown')}")
        # Offer to export results
        export = input("\nExport results to text file? (y/n): ").strip().lower()
        if export == 'y':
            filename = f"speedtest_result_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(BANNER)
                f.write(f"Test time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Server: {best['sponsor']} ({best['name']}, {best['country']}) [{best['host']}]\n")
                f.write(f"Ping: {ping_result:.2f} ms\n")
                f.write(f"Download: {format_speed(download_speed)}\n")
                f.write(f"Upload:   {format_speed(upload_speed)}\n")
                f.write(f"ISP: {st.results.client.get('isp', 'Unknown')}\n")
                f.write(f"External IP: {st.results.client.get('ip', 'Unknown')}\n")
            print(f"Results exported to {filename}")
    except Exception as e:
        print(f"\n❌ Error running speed test: {e}")

if __name__ == "__main__":
    run_speedtest()