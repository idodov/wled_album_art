
# AppDaemon WLED Album Art Sync

This AppDaemon app for Home Assistant synchronizes the colors of your WLED lights with the album art of your currently playing media. It extracts the three most dominant vibrant colors from the album art and sends them to your WLED controller to create an immersive lighting experience.

## Features

*   **Dynamic Color Sync:** Automatically adjusts WLED colors based on the album art of your media player.
*   **Vibrant Color Extraction:** Extracts the three most dominant and saturated colors from the album art.
*   **Configurable WLED Settings:** Allows you to control the WLED effect, speed, intensity, and segment ID.
*   **Simple Setup:** Easy to configure through your `apps.yaml` file.

## Prerequisites

*   Home Assistant installed and configured
*   AppDaemon installed and configured
*   A WLED controller set up on your network
*  `Pillow` python library installed.

## Installation

1.  **Install AppDaemon:**
    *   Open Home Assistant in your web browser.
    *   Navigate to **Settings** > **Add-ons**.
    *   Click the **Add-on Store** button (lower right).
    *   Search for "AppDaemon" and install it.
    *   After installation, start the AppDaemon add-on.

2.  **Install Required Python Packages:**
    *   Go to the AppDaemon add-on configuration page (found in the same Add-ons page where you started AppDaemon).
    *   Locate the section for **Python packages**.
    *   Add `pillow` to the list. This package is **required** for image processing.
    *   Save the changes. This will install the necessary Python libraries.
    
    ```yaml
    python_packages:
        - pillow
    ```

3.  **Download the Script:**
    You can install the script using either **HACS** (Home Assistant Community Store, recommended) or by manually downloading the Python file.

    **HACS (Recommended):**

    *   If you don't have HACS installed, follow the instructions on the [HACS's GitHub page](https://hacs.xyz/) to install it.
    *   After HACS is set up, go to the HACS page in Home Assistant.
    *   **If "AppDaemon" repositories are not found**: You need to enable AppDaemon apps discovery and tracking in HACS settings. Go to `Settings` > `Integrations` > `HACS` > `Configure` and enable `AppDaemon apps discovery & tracking`.
    *   Click on **Custom Repositories** and add `https://github.com/idodov/wled_album_art` as an **AppDaemon** repository.
    *   Search for and download `WLED Album Art` in HACS.
    *   **Important:** After installing through HACS, you **MUST** manually move all files from `/addon_configs/a0d7b954_appdaemon/apps/` to `/homeassistant/appdaemon/apps/`. HACS places files in the `/addon_configs` directory, while AppDaemon expects them in the `/homeassistant` directory.
    *  Open `/addon_configs/a0d7b954_appdaemon/appdaemon.yaml` to configure it (add `app_dir` line under `appdaemon:`). Do not remove any lines from the file, just add the new line:
       ```yaml
       appdaemon:
         app_dir: /homeassistant/appdaemon/apps/
       ```

    **Manual Download:**

    *   Alternatively, you can download the Python script directly from the GitHub repository:
        [https://github.com/idodov/pixoo64-media-album-art/blob/main/apps/wled_album_art/wled_album_art.py](https://github.com/idodov/wled_album_art/blob/main/apps/wled_album_art/wled_album_art.py)
    *   Place this file into the directory `/addon_configs/a0d7b954_appdaemon/apps`.
    *   **Note:** With this method, you will not receive automatic updates.

4.  **Configure AppDaemon:**
    *   You will need to modify the `apps.yaml` file to activate the script.
    *   This file is typically located in the `/appdaemon/apps` directory that you added in the previous step.

```yaml
wled_album_art:
    module: wled_album_art
    class: WLEDImageSync
    ha_url: "http://homeassistant.local:8123"       # Home Assistant URL
    media_player: "media_player.living_room"        # Replace with your media player entity ID
    wled_ip: "192.168.86.50"                        # Replace with your WLED's IP address
    segment_id: 0                                   # Segment ID on WLED (optional default 0)
    transition_time: 2 # Transition time in seconds # Transition time in seconds (defualt 1)
    effect_name: 38                                 # Effect ID on WLED (optional default Solid)
    speed_value: 128                                # Effect speed (optional default 128)
    intensity_value: 128                            # Effect intensity (optional default 128)
    pallete: 5                                      # Color pallete ID
```
