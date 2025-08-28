from plugp100 import TapoApiClient
from plugp100.common.credentials import AuthCredential
from plugp100.discovery.tapo_discovery import discover_single_device

EMAIL = "sanjaygovind1234@gmail.com"         # Tapo app email
PASSWORD = "Leo@messi1234"   # Tapo app password
PLUG_IP = "10.58.217.225"         # Plug IP from your router

def main():
    creds = AuthCredential(EMAIL, PASSWORD)
    device = discover_single_device(PLUG_IP, creds)
    client = TapoApiClient(device)

    print("Turning plug ON...")
    client.on()

    input("Press Enter to turn OFF...")

    print("Turning plug OFF...")
    client.off()

if __name__ == "__main__":
    main()
