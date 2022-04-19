# APRS 434

Welcome to the home of APRS 434, the 434 MHz LoRa APRS amateur radio project that **extends range by saving bytes.**

Unlike other ham radio LoRa APRS projects, this project aims at **deploying LoRa the way it was intended;** namely by being frugal about the number of bytes put on air. Doing so, reaps a number of benefits:

- Increased battery life,
- Higher chances of good packet reception,
- Hence, increased range,
- Lower probability of packet collisions,
- Therefore, more channel capacity.


## ESP32 Firmware Downloads
Stay put for TTGO T-Beam and i-gate firmware that will soon be freely available here for downloading.


## News
Feel free to join our public [Telegram Group](https://t.me/aprs434) for the latest news.


## Opportunity to Set a Standard for LoRa Data Compression
LoRa permits sending any of the [full 128 ASCII character set](https://en.wikipedia.org/wiki/ASCII#Character_set). Hence, there are ample opportunities for data compression, namely:

|**Frame Field**|**Characters or Codes**|
|:-:|:-:|
|_Destination Address_|not required; provided by the i‑gate|
|_Source Address_|any 6 out of **37** characters: 26 capital letters + 10 digits + space|
|_SSID_|1 out of **16** hexadecimal digits|
|_Digipeater Address_|1 of **6** recommended n‑N paradigm paths|
|_Information Field_|up to 256 out of **95** [printable ASCII characters](https://en.wikipedia.org/wiki/ASCII#Printable_characters)|

Inside the _Information Field,_ it is customary to compress latitude, longitude, symbol, course and speed a second time using base91.


## Recommended n-N paradigm paths

|station|generic digipeating path|
|:-----:|:----------------------:|
|metropolitan fixed|`WIDE2-1`|
|extremely remote fixed|`WIDE2-2`|
|metropolitan mobile|`WIDE1-1,WIDE2-1`|
|extremely remote mobile|`WIDE1-1,WIDE2-2`|
|balloons\ & aircraft|`WIDE2-1`|
|145.825\ MHz|`ARISS,WIDE2-1`|

- The first n digit in n-N paradigm paths indicates the coverage level of the digipeater, whereby 1 is for domestic fill‑in digipeaters and 2 is for county-level digipeaters.
- The second N digit indicates the number of repeats at the indicated coverage level.


## Opportunities to Reduce Power Consumption

1. OLED displays have a limited life span and consume quite a bit of power. An OLED screen and its driver can be put to sleep when the tracker is idle. The same holds true for the LoRa radio module and the ESP32. This needs to be investigated.
2. A GPS module is also a power hog. 


## Messaging Pager
Up to now, APRS has been considered mainly as a localisation technology. 
