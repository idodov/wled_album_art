# AppDaemon WLED Album Art Sync

Sync your WLED lights with your media player's album art for an immersive lighting experience! This AppDaemon app for Home Assistant dynamically adjusts your WLED lights to match the dominant colors of the currently playing media's album art.

## Features

*   **Dynamic Album Art Color Sync:** Automatically extracts colors from your media player's album art and applies them to your WLED lights in real-time.
*   **Vibrant Color Palette Generation:** Identifies the top three most vibrant and saturated colors from album art to create a visually appealing lighting effect.
*   **Highly Configurable WLED Settings:** Customize the WLED effect, speed, intensity, color palette, segment ID, and transition time directly from your `apps.yaml` configuration.
*   **Easy to Install and Setup:** Simple configuration through the `apps.yaml` file and flexible installation options via HACS or manual download.

## Prerequisites

Before you begin, ensure you have the following:

*   **Home Assistant:**  A working Home Assistant installation.
*   **AppDaemon:** AppDaemon installed and configured within Home Assistant.
*   **WLED Controller:** A WLED-enabled light controller connected to your network.
*   **Pillow (PIL) Python Library:**  Required for image processing. This will be installed as part of the setup.

## Installation

You can install the WLED Album Art Sync app using either **HACS (Home Assistant Community Store - Recommended)** for easy updates or **Manual Download** if you prefer manual management.

### Method 1: Installation via HACS (Recommended)

1.  **Install HACS (if not already installed):**
    *   If you don't have HACS, follow the installation guide on the [HACS website](https://hacs.xyz/).
2.  **Enable AppDaemon Discovery in HACS (if needed):**
    *   Go to **Settings** > **Integrations** in Home Assistant.
    *   Find the **HACS** integration and click **Configure**.
    *   Ensure **"AppDaemon apps discovery & tracking"** is enabled. If not, enable it and submit.
3.  **Add Custom Repository in HACS:**
    *   Navigate to the **HACS** page in Home Assistant.
    *   Click **Custom Repositories** (three dots menu in the top right corner).
    *   Add the following information:
        *   **Repository URL:** `https://github.com/idodov/wled_album_art`
        *   **Category:**  Select **AppDaemon**
    *   Click **ADD**.
4.  **Install WLED Album Art App:**
    *   Go back to the main **HACS** page.
    *   Click on **Integrations**.
    *   Search for and install **"WLED Album Art Sync"**.
5.  **Move App Files to AppDaemon Apps Directory (Important):**
    *   **After installing through HACS, you MUST manually move the app files.** HACS places files in the `/addon_configs/a0d7b954_appdaemon/apps/` directory, but AppDaemon expects them in `/homeassistant/appdaemon/apps/`.
    *   Use the Home Assistant File Editor or Samba share to move all files from `/addon_configs/a0d7b954_appdaemon/apps/wled_album_art/` to `/homeassistant/appdaemon/apps/wled_album_art/`.  Create the `wled_album_art` directory in `/homeassistant/appdaemon/apps/` if it doesn't exist.
6.  **Configure `appdaemon.yaml` (if not already configured):**
    *   Open your `appdaemon.yaml` file. This file is often located in `/addon_configs/a0d7b954_appdaemon/` when using the AppDaemon add-on.
    *   Ensure you have the `app_dir` parameter configured under the `appdaemon:` section to point to your AppDaemon apps directory. **Add this line if it's missing, do not remove existing lines.**
       ```yaml
       appdaemon:
         app_dir: /homeassistant/appdaemon/apps/
       ```
7.  **Install Python Package (Pillow):**
    *   Go to the AppDaemon add-on configuration page in Home Assistant (Settings > Add-ons > AppDaemon > Configuration).
    *   In the **Python packages** section, add `pillow` to the list.
        ```yaml
        python_packages:
          - pillow
        ```
    *   Save the configuration and restart the AppDaemon add-on for the changes to take effect.

### Method 2: Manual Download

1.  **Download the Python Script:**
    *   Download the `wled_album_art.py` file directly from the GitHub repository:
        [https://github.com/idodov/wled_album_art/blob/main/wled_album_art.py](https://github.com/idodov/wled_album_art/blob/main/wled_album_art.py)
2.  **Create App Directory (if needed):**
    *   If you don't already have an `apps` directory for AppDaemon, create it at `/homeassistant/appdaemon/apps/`.
    *   Inside the `apps` directory, create a subdirectory named `wled_album_art`.
3.  **Place the Script:**
    *   Move the downloaded `wled_album_art.py` file into the `/homeassistant/appdaemon/apps/wled_album_art/` directory.
4.  **Configure `appdaemon.yaml` and Install Pillow:**
    *   Follow steps 6 and 7 from the HACS installation method to configure your `appdaemon.yaml` and install the `pillow` Python package.

## Configuration

1.  **Edit `apps.yaml`:**
    *   Open your `apps.yaml` file, located in the `/homeassistant/appdaemon/apps/` directory.
2.  **Add the App Configuration:**
    *   Add the following configuration block to your `apps.yaml` file, adjusting the parameters to match your setup.

    ```yaml
    wled_album_art:
        module: wled_album_art
        class: WLEDImageSync
        ha_url: "http://homeassistant.local:8123"       # Home Assistant URL (e.g., your Home Assistant IP or homeassistant.local:8123)
        media_player: "media_player.living_room"        # Entity ID of your media player
        wled_ip: "192.168.86.50"                        # IP address of your WLED controller
        segment_id: 0                                   # Segment ID on WLED (optional, default: 0)
        transition_time: 2                             # Transition time in seconds for color changes (optional, default: 1 second)
        effect_name: 38                                 # WLED Effect ID to use (optional, default: 38 - Solid)
        speed_value: 128                                # Effect speed (optional, default: 128)
        intensity_value: 128                            # Effect intensity (optional, default: 128)
        pallete: 5                                      # WLED Color Palette ID (optional, default: 5)
    ```

3.  **Configuration Parameters:**

    *   **`ha_url`:**  The URL of your Home Assistant instance.  Usually `http://<your_ha_ip_address>:8123` or `http://homeassistant.local:8123`.
    *   **`media_player`:** The entity ID of the media player you want to monitor for album art (e.g., `media_player.spotify`, `media_player.plex`).
    *   **`wled_ip`:** The IP address of your WLED controller on your local network.
    *   **`segment_id` (Optional):** The WLED segment ID to control. Defaults to `0` (the first segment).
    *   **`transition_time` (Optional):** The time in seconds for WLED to smoothly transition between colors. Defaults to `1` second.
    *   **`effect_name` (Optional):** The WLED effect ID to use. Defaults to `38` (Solid color). Refer to the WLED Effects list for other IDs.
    *   **`speed_value` (Optional):** The speed of the WLED effect (if applicable). Defaults to `128`.
    *   **`intensity_value` (Optional):** The intensity of the WLED effect (if applicable). Defaults to `128`.
    *   **`pallete` (Optional):** The WLED color palette ID to use. Defaults to `5`. Refer to the WLED Palettes list for other IDs.

## Usage

Once installed and configured, the app will automatically start synchronizing your WLED lights with your media player's album art whenever media playback starts or the album art changes.

Enjoy your immersive lighting experience!
