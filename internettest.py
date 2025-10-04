import speedtest
import datetime
import requests
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_TOKEN = "8437446585:AAH9SsyplshYavOe-hOV0UZ4TdDTXAmsW9Q"
BANNER = "🌐 Internet Speed Test Bot\nPisethz x JackyJackyHunt"

def format_speed(bits_per_sec):
    mbps = bits_per_sec / 1_000_000
    mBps = bits_per_sec / 8 / 1_000_000
    return f"{mbps:.2f} Mbps ({mBps:.2f} MB/s)"

def speed_color(mbps):
    if mbps >= 100:
        return "🟢"
    elif mbps >= 50:
        return "🟡"
    else:
        return "🔴"

def ping_color(ping):
    if ping <= 30:
        return "🟢"
    elif ping <= 100:
        return "🟡"
    else:
        return "🔴"

def create_progress_bar(value, max_value, length=20):
    filled_length = int(length * min(value, max_value) / max_value)
    empty_length = length - filled_length
    return "█" * filled_length + "░" * empty_length

def create_speed_graph(download_mbps, upload_mbps, max_speed):
    total_blocks = 20
    down_blocks = int(download_mbps / max_speed * total_blocks)
    up_blocks = int(upload_mbps / max_speed * total_blocks)
    down_graph = "🟦" * down_blocks + "⬜" * (total_blocks - down_blocks)
    up_graph = "🟩" * up_blocks + "⬜" * (total_blocks - up_blocks)
    return f"📊 Speed Graph (relative):\nDownload: {down_graph} {download_mbps:.2f} Mbps\nUpload:   {up_graph} {upload_mbps:.2f} Mbps\n"

def get_network_info():
    try:
        response = requests.get("https://ipinfo.io/json", timeout=5)
        data = response.json()
        return {
            "IP": data.get("ip", "N/A"),
            "Hostname": data.get("hostname", "N/A"),
            "City": data.get("city", "N/A"),
            "Region": data.get("region", "N/A"),
            "Country": data.get("country", "N/A"),
            "Location": data.get("loc", "N/A"),
            "Org": data.get("org", "N/A"),
            "Postal": data.get("postal", "N/A"),
            "Timezone": data.get("timezone", "N/A"),
            "ASN": data.get("asn", {}).get("asn", "N/A") if "asn" in data else "N/A",
        }
    except Exception as e:
        return {"Error": f"Failed to fetch network info: {e}"}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text(f"{BANNER}\n\n🕒 Running speed test on the best server...", parse_mode=None)
    await run_speedtest_live(msg)

async def run_speedtest_live(msg):
    try:
        st = speedtest.Speedtest()
        server = st.get_best_server()
        net_info = get_network_info()
        max_speed = 200  # Max Mbps for scaling bars

        # Simulated live progress
        download_mbps = 0
        upload_mbps = 0

        # Simulate download
        for i in range(1, 21):
            await asyncio.sleep(0.2)  # simulate speed progress
            download_mbps = max_speed * i / 20  # scale linearly
            down_bar = create_progress_bar(download_mbps, max_speed)
            text = f"🕒 Downloading...\n[{down_bar}] {download_mbps:.2f} Mbps"
            await msg.edit_text(text)

        # Actual download test
        download_speed_bits = st.download()
        download_mbps = download_speed_bits / 1_000_000

        # Simulate upload
        for i in range(1, 21):
            await asyncio.sleep(0.2)
            upload_mbps = max_speed * i / 20
            up_bar = create_progress_bar(upload_mbps, max_speed)
            text = f"🕒 Uploading...\n[{up_bar}] {upload_mbps:.2f} Mbps"
            await msg.edit_text(text)

        # Actual upload test
        upload_speed_bits = st.upload()
        upload_mbps = upload_speed_bits / 1_000_000
        ping_result = st.results.ping

        down_color = speed_color(download_mbps)
        up_color = speed_color(upload_mbps)
        ping_indicator = ping_color(ping_result)

        down_bar = create_progress_bar(download_mbps, max_speed)
        up_bar = create_progress_bar(upload_mbps, max_speed)
        speed_graph = create_speed_graph(download_mbps, upload_mbps, max_speed)

        # Final dashboard
        result_text = f"""
📅 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🌍 Server Information:
┌────────────────────────
│ Sponsor: {server['sponsor']}
│ Name: {server['name']}, {server['country']}
│ Host: {server['host']}
└────────────────────────

⚡ Speed Test Results:
┌────────────────────────
│ Ping: {ping_indicator} {ping_result:.2f} ms
│ Download: {down_color} {format_speed(download_speed_bits)}
│ [{down_bar}]
│ Upload:   {up_color} {format_speed(upload_speed_bits)}
│ [{up_bar}]
└────────────────────────

{speed_graph}

🌐 Network Information:
┌────────────────────────
"""
        for k, v in net_info.items():
            result_text += f"│ {k}: {v}\n"
        result_text += "└────────────────────────"

        await msg.edit_text(result_text, parse_mode=None)

    except Exception as e:
        await msg.edit_text(f"❌ Error running speed test: {e}", parse_mode=None)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("🚀 Telegram Live Speed Test Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
