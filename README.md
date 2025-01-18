
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

1.  **Install Pillow:**
    Ensure you have the `Pillow` installed in your AppDaemon environment:

2.  **Place the `wled_album_art.py` Script in apps directory:**
    Copy the python script into the newly created directory, so it's located at `apps/wled_album_art.py`.
     
3. **Configure `apps.yaml`**
    Add the following to your `apps/apps.yaml` file, adjusting the parameters to match your setup:

```yaml
wled_album_art:
    module: wled_album_art
    class: WLEDImageSync
    ha_url: "http://homeassistant.local:8123"                      # Home Assistant URL
    media_player: "media_player.living_room"                       # Replace with your media player entity ID
    wled_ip: "192.168.86.50"                                       # Replace with your WLED's IP address
    segment_id: 0                                                  # Segment ID on WLED (optional default 0)
    effect_name: 38                                                # Effect ID on WLED (optional default Solid)
    speed_value: 128                                               # Effect speed (optional default 128)
    intensity_value: 128                                           # Effect intensity (optional default 128)
    pallete: 5                                                     # Color pallete ID
```
