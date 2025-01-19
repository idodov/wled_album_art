"""
App configuration:

# apps.yaml
wled_album_art:
    module: wled_album_art
    class: WLEDImageSync
    ha_url: "http://homeassistant.local:8123"                       # Home Assistant URL
    media_player: "media_player.living_room"                        # Replace with your media player entity ID
    wled_ip: "192.168.86.50"                                        # Replace with your WLED's IP address
    pallete: 5                                                      # Color pallete ID
    segment_id: 0 # Segment ID on WLED                              # Optional default 0
    effect_name: 38 # Effect ID on WLED                             # Optional default Solid
    speed_value: 128 # Effect speed                                 # Optional defualt 128
    intensity_value: 128 # Effect intensity                         # Optional default 128

"""
import appdaemon.plugins.hass.hassapi as hass
from io import BytesIO
from PIL import Image, ImageEnhance
import json
import aiohttp
from collections import Counter, OrderedDict
import random
import math


class WLEDImageSync(hass.Hass):

    def initialize(self):
        self.listen_state(self.media_player_change, self.args.get('media_player'), attribute='media_title')
        self.wled_ip = self.args.get('wled_ip')
        self.ha_url = self.args.get('ha_url')
        self.segment_id = self.args.get('segment_id', 0)
        self.effect_name = self.args.get('effect_name', 38)  # Default effect
        self.speed_value = self.args.get('speed_value', 128)  # Default speed
        self.intensity_value = self.args.get('intensity_value', 128)  # Default intensity
        self.pallete = self.args.get('pallete', 5)  # Default colors pallete
        self.image_cache = OrderedDict() # Initialize cache
        self.cache_size = 100


    async def media_player_change(self, entity, attribute, old, new, kwargs):
        if new and new != old:            
            media_content_id = await self.get_state(entity, attribute="media_content_id")
            if media_content_id:
                try:
                    # Attempt to get image URL
                    image_url = await self.get_state(entity, attribute="entity_picture")
                    if image_url:
                        image_url = image_url if image_url.startswith('http') else f"{self.ha_url}{image_url}"
                        
                    media_artist = await self.get_state(entity, attribute="media_artist")
                    media_album_name = await self.get_state(entity, attribute="media_album_name")
                    
                    if media_artist and media_album_name:
                        cache_key = f"{media_artist}-{media_album_name}"
                        await self.process_image_and_update_wled(image_url, cache_key)
                    elif image_url:
                        await self.process_image_and_update_wled(image_url, None) # Skip cache, process and update
                except Exception as e:
                    self.log(f"Error getting Media Data: {e}")

    async def process_image_and_update_wled(self, image_url, cache_key):
        if cache_key and cache_key in self.image_cache:
            self.log("Image found in cache")
            cached_colors = self.image_cache.pop(cache_key) # Move item to the end
            self.image_cache[cache_key] = cached_colors
            await self.update_wled(cached_colors)
            return

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as response:
                    if response.status != 200:
                        self.log(f"Error fetching image {image_url}: {response.status}")
                        return None

                    image_data = await response.read()

        except Exception as e:
            self.log(f"Error processing image {image_url}: {e}")
            return None
        try:
            image = Image.open(BytesIO(image_data)).convert('RGB')
            image = image.resize((16, 16))  # Resize for faster processing
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(3.0)
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            dominant_colors = await self.most_vibrant_colors_wled(image)

            if cache_key:
                if len(self.image_cache) >= self.cache_size:
                    self.image_cache.popitem(last=False)
                
                self.image_cache[cache_key] = dominant_colors # Save colors to the cache
            await self.update_wled(dominant_colors)

        except Exception as e:
            self.log(f"Error processing image or updating WLED: {e}")

    def is_strong_color(self, color):
        """Check if at least one RGB component is greater than 200."""
        return any(c > 200 for c in color)

    async def most_vibrant_colors_wled(self, full_img):
        """Extract the three most dominant vibrant colors from an image, ensuring diverse hues and strong colors."""
        full_img = full_img.resize((16, 16), Image.Resampling.LANCZOS)
        
        color_counts = Counter(full_img.getdata())
        most_common_colors = color_counts.most_common(50)  # Get more colors
    
        # Filter only vibrant colors
        vibrant_colors = [(color, count) for color, count in most_common_colors if self.is_vibrant_color(*color)]
    
        # Sort by frequency and saturation
        def color_score(color_count):
            color, count = color_count
            max_val = max(color)
            min_val = min(color)
            saturation = (max_val - min_val) / max_val if max_val > 0 else 0
            return count * saturation  # Score = frequency * saturation
        
        vibrant_colors.sort(key=color_score, reverse=True)

        if len(vibrant_colors) < 3: # If we have less then 3 vibrant color, return random
            while len(vibrant_colors) < 3:
                vibrant_colors.append((tuple(random.randint(100, 200) for _ in range(3)), 1)) # Added count for the sort
                vibrant_colors.sort(key=color_score, reverse=True)
            
        # Select top 3 unique colors by checking for distance between them and if at least one value > 200
        selected_colors = []
        
        for color, _ in vibrant_colors:
            if self.is_strong_color(color):
                is_similar = False
                for selected_color, _ in selected_colors:
                    if self.color_distance(color, selected_color) < 50: # Threshold for color distance
                        is_similar = True
                        break
                if not is_similar:
                    selected_colors.append((color, _))
                    if len(selected_colors) == 3:
                        break

        # If less then 3 colors found - return the current result
        while len(selected_colors) < 3:
            selected_colors.append((tuple(random.randint(100, 255) for _ in range(3)),1)) # Added count for the sort
            selected_colors.sort(key=color_score, reverse=True)

        return self.rgb_to_hex(selected_colors[0][0]), self.rgb_to_hex(selected_colors[1][0]), self.rgb_to_hex(selected_colors[2][0])
        

    def color_distance(self, color1, color2):
        """Calculate the Euclidean distance between two RGB colors."""
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)


    def is_vibrant_color(self, r, g, b):
        """Check if a color is vibrant and not black, gray, or white"""
        max_color = max(r, g, b)
        min_color = min(r, g, b)
        if max_color + min_color > 400 or max_color - min_color < 50:
            return False
        if max_color - min_color < 100:
            return False
        return True

    def rgb_to_hex(self, rgb):
        return '{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])


    async def update_wled(self, colors):
        """Sends the color data to WLED asynchronously"""
        # Create WLED JSON payload
        payload = {
            'seg': [
                {
                    'id': int(self.segment_id),
                    'col': [
                        colors[0],
                        colors[1],
                        colors[2]
                    ],
                    'fx': self.effect_name,
                    'sx': int(self.speed_value),
                    'ix': int(self.intensity_value),
                    'pal': int(self.pallete)
                }
            ]
        }

        url = f"http://{self.wled_ip}/json/state"
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            try:
                async with session.post(url, data=json.dumps(payload)) as response:
                    response.raise_for_status()  # Raise an error for bad status codes
                    if response.status != 200:
                        self.log(f"WLED Update Fail. Response code: {response.status} Response: {await response.text()}")
            except aiohttp.ClientError as e:
                self.log(f"Error sending WLED control command: {e}")
