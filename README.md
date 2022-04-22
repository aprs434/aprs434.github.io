# APRS 434

Welcome to the home of **APRS&nbsp;434**, the 434&nbsp;MHz LoRa APRS amateur radio project that **extends range by saving bytes.**

Unlike other ham radio LoRa APRS projects, this project aims at **deploying LoRa the way it was intended;** namely by being frugal about the number of bytes put on air. Doing so, reaps a number of benefits:

- Increased battery life,
- Higher chances of good packet reception,
- Hence, increased range,
- Lower probability of packet collisions,
- Therefore, more channel capacity.


## Setting a Standard for LoRa Frame Compression
LoRa permits sending any of the [full 128 ASCII character set](https://en.wikipedia.org/wiki/ASCII#Character_set). Hence, there are ample opportunities for frame compression at the [data link layer](https://en.wikipedia.org/wiki/Data_link_layer), namely:

|**frame field**|**characters or digits**|
|:-:|:-:|
|_Flag_|**not required;** provided by LoRa|
|_Destination Address_|**not required;** provided by the i‑gate|
|_Source Address_|any 6 out of **37** characters: 26 capital letters + 10 digits + space|
|_SSID_|1 out of [**16** hexadecimal digits](https://en.wikipedia.org/wiki/Hexadecimal)|
|_Digipeater Address_|1 of [**6** recommended n‑N paradigm paths](#recommended-n-n-paradigm-paths)|
|_Information Field_|up to 256 out of [**95** printable ASCII characters](https://en.wikipedia.org/wiki/ASCII#Printable_characters)|
|_Frame Check Sequence_|**not required;** provided by LoRa|

- _Source Address, SSID_ and _Digipeater Address_ can by combined into only 6 LoRa bytes, compared to 22 LoRa bytes with OE5BPA firmware.
- It is customary to compress latitude, longitude, symbol, course and speed using [Base91](https://en.wikipedia.org/wiki/List_of_numeral_systems#Standard_positional_numeral_systems), which results in another 13 LoRa bytes. **APRS&nbsp;434** will not differ in this respect. There is almost no gain to be made in compressing the _Information Field_ any further.

Hence, **APRS&nbsp;434** geolocation beacons will transmit **a total of only 19 LoRa bytes** at a time, tremendously increasing the chances of a flawless reception by an i-gate. Other firmware tends to consume three times as many LoRa bytes.


## Frequency = 434.000 MHz
Above mentioned LoRa data link compression techniques render our firmware uncompatible with other firmware proposed for LoRa APRS i‑gates.
Moreover, [other tracker firmware produces an insane amount of bytes](https://github.com/lora-aprs/LoRa_APRS_Tracker/issues/56) on air. This quickly congests channel capacity.
Therefore, we opted to migrate our i‑gate network to the centre frequency of 434.000&nbsp;MHz.

The choice of this frequency also serves the purpose of fending off any [ITU Region 1](https://en.wikipedia.org/wiki/ITU_Region) corporate secondary users who might be hankering after the longer range and the improved penetration of 434&nbsp;MHz as compared to the 868 MHz [ISM band](https://en.wikipedia.org/wiki/ISM_radio_band).

> Our motto: **« Use 434&nbsp;MHz or lose it. »**

From a regulatory point of view, long range communication —which, by definition, includes LoRa— is not allowed on ISM (Industrial, Scienitfic & Medical) bands. ISM&nbsp;bands are intended for local use only. The amateur radio service forms a sole exception to this, as its 70&nbsp;cm UHF band happens to [overlap](https://hamwaves.com/lpd433/en/index.html#lpd433-channels) the [ITU&nbsp;Region&nbsp;1](https://en.wikipedia.org/wiki/ITU_Region) 434&nbsp;MHz ISM&nbsp;band as a primary service.

As a general rule, secondary users should always check whether a frequency is in use by a primary user before transmitting on air.
However, LoRa has no carrier sensing capability. Therfore, secondary ISM band users lack the ability to check whether an amateur radio operator is using the 434&nbsp;MHz band as a primary user.


## Recommended n-N paradigm paths

|station|generic digipeating path|coding|
|:-----:|:----------------------:|:----:|
|metropolitan fixed|`WIDE2-1`|0|
|extremely remote fixed|`WIDE2-2`|1|
|metropolitan mobile|`WIDE1-1,WIDE2-1`|2|
|extremely remote mobile|`WIDE1-1,WIDE2-2`|3|
|balloons & aircraft|`WIDE2-1`|4|
|space satellites|`ARISS,WIDE2-1`|5|

Note:
- The first `n` digit in `n-N` paradigm paths indicates the coverage level of the digipeater, whereby `1` is for domestic fill‑in digipeaters and `2` is for county-level digipeaters.
- The second `N` digit indicates the number of repeats at the indicated coverage level.


## Reducing Power Consumption
1. OLED displays have a limited life span and consume quite a bit of power. An OLED screen and its driver [can be put to sleep](https://bengoncalves.wordpress.com/2015/10/01/oled-display-and-arduino-with-power-save-mode/) when the tracker is idle. The same holds true for the LoRa radio module and the ESP32. This needs to be investigated.
2. GPS modules are also power hogs. It may be conceivable to use the WLAN receiver aboard an ESP32 for localisation, whereby the three strongest WLAN SSIDs are transmitted to the i‑gate. The i‑gate would then guess the tracker location from a freely available "war‑driving" data service from the Internet. This is comparable to how Google Android smartphone localisation works.


## Messaging Pager
Up to now, APRS has been unduly considered to be predominantly a one-way localisation technology. This went to the point that many mistakenly think the letter "P" in the acronym APRS would stand for "position." Bob Bruninga WB4APR (SK), the spiritual father of APRS, deeply resented this situation.

> _"APRS is not a vehicle tracking system. It is a two-way tactical real-time digital communications system between all assets in a network sharing information about everything going on in the local area."_
 
In Bob's view of APRS as being foremost a real-time situational and tactical tool, messaging defintely merrits its place.
We set ourselfs the long-term goal of rendering APRS messaging more popular by offering messaging pager designs.


## Recommended Hardware

### Tracker Hardware:
- TTGO T-Beam 434&nbsp;MHz v0.7 or v1.1
- longer 434&nbsp;MHz antenna with [SMA male](https://en.wikipedia.org/wiki/SMA_connector) connector
- 16.9&nbsp;mm long tiger tail wire soldered to the female SMA socket
- 5&nbsp;V 3&nbsp;A microUSB charge adapter
- Panasonic NCR18650B Li-ion cell, or quality equivalent
- glue gun to stick the GPS antenna to the cell holder
- SH1106 1.3" I²C (4‑pin) OLED display (slightly larger than the usual 0.8" displays often sold with the TTGO T-Beam)
- enclosure

### I-Gate Hardware:

- Either:
  + [TTGO LORA32 434&nbsp;MHz v2](http://www.lilygo.cn/prod_view.aspx?TypeId=50060&Id=1319&FId=t3:50060:3) ([U.FL](https://en.wikipedia.org/wiki/Hirose_U.FL) or [SMA female](https://en.wikipedia.org/wiki/SMA_connector) RF socket), or
  + Heltec ESP32 LoRa 434&nbsp;MHz **v2** ([U.FL](https://en.wikipedia.org/wiki/Hirose_U.FL) female RF socket)
  + **DO NOT USE** Heltec ESP32 LoRa 434&nbsp;MHz **v1** as it is as deaf as a post!
- 70&nbsp;cm amateur radio colinear groundplane antenna with coaxial cable and connectors
- 16.9&nbsp;mm long tiger tail wire soldered to the RF socket
- 5&nbsp;V 1&nbsp;A microUSB power supply
- enclosure


## ESP32 Firmware Downloads

### Tracker Firmware
- See: <https://github.com/aprs434/lora.tracker>
- The [`tracker.json`](https://github.com/aprs434/lora.tracker/blob/master/data/tracker.json) configuration file has been much simplified.

### I-Gate Firmware
- See: <https://github.com/lora-aprs/LoRa_APRS_iGate>
- Currently, the APRS&nbsp;434 tracker is still compatible with the [i-gate developped by Peter Buchegger, OE5BPA](https://github.com/lora-aprs/LoRa_APRS_iGate). However, this will soon change. When this happens, APRS&nbsp;434 will migrate to the new 434.000&nbsp;MHz channel.


## Development Road Map

### Data Link Layer

|tracker<br/>firmware|completed|feature|compatible with [OE5BPA&nbsp;i‑gate](https://github.com/lora-aprs/LoRa_APRS_iGate)|frequency|
|:------------------:|:-------:|:-----:|:--------------------------------------------------------------------------------:|:-------:|
|v0.1|✓|byte-saving [`tracker.json`](https://github.com/aprs434/lora.tracker/blob/master/data/tracker.json)|✓|433.775&nbsp;MHz|
|v0.2|✓|fork of the [OE5BPA tracker](https://github.com/lora-aprs/LoRa_APRS_Tracker) with significantly less transmitted bytes|✓|433.775&nbsp;MHz|
|v0.3||[Base91](https://en.wikipedia.org/wiki/List_of_numeral_systems#Standard_positional_numeral_systems) compression of the location, course and speed data|✓|433.775&nbsp;MHz|
|v0.4||random time jitter between fixed interval packets to avoid repetitive collisions|✓|433.775&nbsp;MHz|
|||tracker and i-gate with frame address compression and [LoRa&nbsp;CRC](https://en.wikipedia.org/wiki/Cyclic_redundancy_check)|✗|**434.000&nbsp;MHz**|

### Tracker Hardware

|tracker<br/>firmware|completed|feature|
|:------------------:|:-------:|:-----:|
|v0.3||coordinates displayed on screen|
|||reduced power consumption through [SH1106 OLED sleep](https://bengoncalves.wordpress.com/2015/10/01/oled-display-and-arduino-with-power-save-mode/)|
|||button press to activate OLED screen|

### Messaging

|tracker<br/>firmware|completed|feature|
|:------------------:|:-------:|:-----:|
|||add a [library](https://web.archive.org/web/20190316204938/http://cliffle.com/project/chatpad/arduino/) for the [Xbox 360 Chatpad](https://nuxx.net/gallery/v/acquired_stuff/xbox_360_chatpad/) keyboard|
|||support for the [M5Stack CardKB Mini](https://shop.m5stack.com/products/cardkb-mini-keyboard) keyboard|

### WiFi Geolocation
TBD


## News & Social
Feel free to join our public [**Telegram Group**](https://t.me/aprs434) for the latest news and cordial discussions.
