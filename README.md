# APRS 434
Welcome to the home of **APRS&nbsp;434**, the 434&nbsp;MHz LoRa APRS amateur radio project that **extends range by saving bytes.**

Unlike other ham radio LoRa APRS projects, this project aims at **deploying LoRa the way it was intended;** namely by being frugal about the number of bytes put on air. Doing so, reaps a number of benefits:

- Increased battery life,
- Higher chances of good packet reception,
- Hence, increased range,
- Lower probability of packet collisions,
- Therefore, more channel capacity.

## Index
- [An Open Standard for LoRa Frame Compression](#an-open-standard-for-lora-frame-compression)
- [Measurable Benefits](#measrable-benefits)
- [LoRa Link Parameters](#)
- [Callsign, SSID, Path and Data Type Compression](#)
- [Digipeating on LoRa Channels](#)
- [](#)
- [](#)
- [](#)
- [](#)
- [](#)
- [](#)
- [](#)


## An Open Standard for LoRa Frame Compression
As a physical layer, LoRa permits sending any of the [256 characters](https://en.wikipedia.org/wiki/Extended_ASCII) from `\00` to `\ff`. This is double the amount of the [7‑bit, 128 ASCII character set](https://en.wikipedia.org/wiki/ASCII#Character_set). Hence, there are ample opportunities for compressing [AX.25](https://en.wikipedia.org/wiki/AX.25) ([packet radio](https://en.wikipedia.org/wiki/Packet_radio)) unnumbered information (UI) frames at the [data link layer](https://en.wikipedia.org/wiki/Data_link_layer), namely:

|[AX.25](https://en.wikipedia.org/wiki/AX.25) UI frame&nbsp;field|required characters or digits with&nbsp;LoRa|
|:-:|:-:|
|_Flag_|**not required**; provided by LoRa|
|_Destination Address_|**not required**; software version provided by the i‑gate|
|_Source Address_|any 6 out of **37** characters: 26 capital letters + 10 digits + space|
|_SSID_|1 out of [**16** hexadecimal numerals](https://en.wikipedia.org/wiki/Hexadecimal)|
|_Digipeater Address_|any out of [**5** recommended `n-N` paradigm paths](#digipeating-on-lora-channels)|
|_Control Field_|**not required**|
|_Protocol ID_|**not required**|
|_Information Field_|up to 256 out of [**95** printable ASCII characters](https://en.wikipedia.org/wiki/ASCII#Printable_characters)<br/>first character = [_Data Type ID_](#data-type-codes)|
|_Frame Check Sequence_|**not required**; [FEC](https://en.wikipedia.org/wiki/Error_correction_code#Forward_error_correction)&nbsp;& [CRC](https://en.wikipedia.org/wiki/Cyclic_redundancy_check) are provided by LoRa|
|_Flag_|**not required**|

- _Source Address, SSID_ and _Data Type ID_ can be compressed into only 5 payload bytes, compared to 26 payload bytes with OE5BPA firmware.
- It is customary to compress latitude, longitude, symbol, course and speed using [Base91](https://en.wikipedia.org/wiki/List_of_numeral_systems#Standard_positional_numeral_systems), which results in another 13 payload bytes; _Data Type ID_ not included. **APRS&nbsp;434** will not differ in this respect.
- If APRS Mic-E compression were to be used instead, that would require another 16 payload bytes to compress latitude, longitude, symbol, course and speed; 7&nbsp;bytes in the superfluous _Destination&nbsp;Address_ and 9&nbsp;bytes in the _Information&nbsp;Field; Data Type ID_ included. Hence, this is not a good option.

## Measurable Benefits
**APRS&nbsp;434** geolocation beacons will encode a total of **only 18 payload bytes** at a time, tremendously **increasing the chances of a flawless reception** by an [**APRS&nbsp;434&nbsp;LoRa&nbsp;i-gate**](https://github.com/aprs434/lora.igate). Other firmware tends to consume about six times as many LoRa payload bytes.

LoRa may receive up to 20&nbsp;dB under the noise floor, but keep in mind that the packet error ratio (PER) as a function of the bit error rate (BER) [increases with the number of transmitted bits](https://en.wikipedia.org/wiki/Bit_error_rate#Packet_error_ratio).

$$PER = 1 - (1 - BER)^n$$

where: $n$ is the number of bits; not bytes.

Due to the LoRa symbol encoding scheme, airtime gains occur in steps of 5&nbsp;bytes when the spreading factor is SF12 and the bandwidth 125&nbsp;kHz. This is depicted as the stepped top trace on the figure below. (Adapted from [airtime-calculator](https://avbentem.github.io/airtime-calculator/ttn/eu868/4,14).)

![Figure 1: The top trace is for SF12BW125. The dot represents a total payload of 18 bytes as proposed for geolocation packets with compression.](lora.airtime-payload.18bytes.png)


## LoRa Link Parameters
Currently, the following LoRa link parameters are commonly in use among amateur radio operators:
- In order to achieve a maximum range, [Semtech](https://en.wikipedia.org/wiki/Semtech) —&nbsp;the company that developed LoRa&nbsp;— recommends selecting the maximum spreading factor $SF = 12$. This corresponds to 12&nbsp;raw bits per symbol. Therefore, each symbol (or frequency chirp) holds $2^{12} = 4096\,\text{chips}$.
- Likewise, the bandwidth is set to the smallest commonly available bandwidth among all LoRa ICs, namely $BW = 125\,\text{kHz}$. This is by definition also the chip rate $R_c = BW$.
- To avoid any further overhead in an already slow mode, the [forward error correction (FEC)](https://en.wikipedia.org/wiki/Error_correction_code#Forward_error_correction) coding rate is kept at $CR = 1$, which corresponds to $\frac{data}{data + FEC} = \frac{4}{5}$.

With these settings, the symbol rate is:

$$R_s = \frac{R_c}{2^{SF}} = \frac{BW}{2^{SF}} = \frac{125\,000}{2^{12}} \approx 30.5\,\text{symbols/s}$$

Whereas the effective data rate $DR$ or bit rate $R_b$ can be calculated as follows:

$$DR = R_b =  \frac{BW}{2^{SF}} \cdot SF \cdot \frac{4}{4 + CR} = \frac{125\,000}{2^{12}} \cdot 12 \cdot \frac{4}{5} \approx 293\,\text{bits/s} \approx 36.6\,\text{byte/s}$$

Above LoRa parameters are adequate for sending geolocation frames.

However, sending even length and character set limited text messages with SF12 would tremendously increase airtime and quickly congest the LoRa channel. The same holds true for local digipeating or meshing. Therefore, the ham radio community should seriously **consider switching from SF12 to SF11,** effectively doubling the data rate.

SF11 not only prevents channel congestion; It also saves 50% on airtime and batteries. Most importantly, SF11 would leave more room for text messaging. The range penalty from switching from SF12 to SF11 would in most circumstances not be too bad at all.

With a payload of only 18&nbsp;bytes, the compressed geolocation frame is perfectly geared towards taking advantage of the reduced airtime offered by SF11 (see [graph](#measurable-benefits)).

Finally, it was observed that amateur radio predominantly employs the LoRa sync word '0x12'; which is manufacturer recommended for private networks, different from LoRaWAN.

Summarised, the following LoRa link parameters are proposed for APRS:

|LoRa parameter|for uplink only|for 2‑way&nbsp;& digipeating|
|:------------:|:-------------:|:--------------------------:|
|SF|12|11|
|BW|125 000|125 000|
|CR|1 (5/4)|1 (5/4)|
|sync word|`0x12`|`0x12`|
|header|explicit|explicit|
|[CRC](https://en.wikipedia.org/wiki/Cyclic_redundancy_check)|on|on|

Unfortunately, most cheap i‑gates currently in use by ham operators are only capable of receiving one preset spreading factor. Therefore, a choice needs to be made between SF12 and SF11. In view of what the amateur radio community expects of APRS over LoRa, the faster data rate offered by SF11 ought to be preferred. 

> For an in depth tutorial slide series about LoRa (and LoRaWAN), please refer to [Mobilefish.com](https://www.mobilefish.com/developer/lorawan/lorawan_quickguide_tutorial.html), also available in video format on [YouTube](https://youtube.com/playlist?list=PLmL13yqb6OxdeOi97EvI8QeO8o-PqeQ0g). **[TODO: spec sheets]**


Upon succesful demonstration of its merits, below LoRa frame compression protocols **will be formally proposed as an extension to the APRS standard:**

## Callsign, SSID, Path and Data Type Compression

|_Callsign_|_SSID_,<br/>_Path Code_&nbsp;&<br/>_Data Type Code_|_Compressed Data_|
|:--------:|:-------------------------------------------------:|:---------------:|
|4 bytes|1 byte|≤&nbsp;d bytes|
|`CCCC`|`D`||

where:
- `CCCC`: the compressed 6 character _Callsign_
- `D`:
  + the compressed _SSID_ (between SSID 0 [none] and 15; included),
  + the _Path Code_ (between path 0 [none] and 3; included), and
  + the _Data Type Code_ (between type 0 and 3; included)
- `d`: a sensible maximum allowed number of compressed data bytes, taking into account the [stepped airtime function](#measurable-benefits)

### Encoding CCCC
1. Treat the given 6&nbsp;character callsign string as a Base36 encoding. Decode it first to an integer.
2. Then, encode this integer as a 4&nbsp;byte Base256 `CCCC` bytestring.

### Decoding CCCC
1. First, decode the given 4&nbsp;byte Base256 `CCCC` bytestring to an integer.
2. Then, encode this integer as a 6&nbsp;character Base36 string, corresponding to the callsign.

### Encoding D
0. **[REWRITE]**
1. First, multiply the _SSID_ integer by&nbsp;16.
2. Then, algebraically add to this the _Data Type Code_ integer as listed in below table.
3. Finally, convert the resulting integer to a single Base256 `D` byte.

### Decoding D
0. **[REWRITE]**
1. First, decode the given Base256 `D` byte to an integer.
2. The _SSID_ equals the **integer quotient** after [integer division](https://en.wikipedia.org/wiki/Division_(mathematics)#Of_integers) of the decoded integer by&nbsp;16.
3. Whereas the _Data Type Code_ equals the [**remainder**](https://en.wikipedia.org/wiki/Remainder) of the decoded integer by&nbsp;16 ([modulo operation](https://en.wikipedia.org/wiki/Modulo_operation)).

### CCCCD Codec Algorithms
- [Python3](compression.py) compression algorithms and tests
- [MIT License](https://github.com/aprs434/aprs434.github.io/blob/main/LICENSE)

### Data Type Codes
Of all the _Data Types_ defined in the [APRS Protocol Reference](https://hamwaves.com/prs/doc/2000.aprs.1.01.pdf), a subset was selected, based on popularity and foremost suitability for LoRa.

|_Data Type_|_ID_|_Data Type Code_|payload|
|:---------:|:--:|:--------------:|:-----:|
|compressed geolocation — no&nbsp;timestamp|`!`&nbsp;or&nbsp;`=`|0|18|
|complete weather report — with compressed geolocation, no&nbsp;timestamp|`!`&nbsp;or&nbsp;`=`|0|29|
|status report|`>`|1|≤&nbsp;20|
|item report — with compressed geolocation|`)`|2|20|
|message|`:`|3|≤&nbsp;d|

Note:
- Weather reports use the same _Data Type IDs_ as position reports but with a _Symbol Code_ `_` overlay.
- `d`: a sensible maximum allowed number of compressed data bytes, taking into account the [stepped airtime function](#measurable-benefits)


## Digipeating on LoRa Channels
> **⚠ <u>REFRAIN</u> from digipeating on LoRa channels!**
> Because of LoRa being a slow data rate mode, digipeating on LoRa channels quickly leads to unwanted channel congestion.

Also consider that:
- Most LoRa gateways are connected to the APRS‑IS Internet server network and many users are merely interested in reaching APRS‑IS.
- There are hardly any, if any, low power portable LoRa devices displaying situational awareness in relation to other LoRa devices.

Hence, below `n-N` paradigm paths could be interpreted foremost as crossover AX.25 packet digipeating paths for any (VHF) digipeater co‑located with the LoRa (i‑)gate.

However, suppose general digipeating were to be allowed on the LoRa channel; even by trackers. This would render it into a mesh network. It would also absolutely require switching from SF12 to the higher data rate SF11 [as explained above](#lora-link-parameters). In such a scenario, below table represents the LoRa device communicating its digipeating requirements to the mesh network.

|station|recommended `n-N` paradigm path|_Path Code_|
|:-----:|:-----------------------------:|:---------:|
|no digipeating||0|
|metropolitan fixed, mountain expeditions, balloons&nbsp;& aircraft|`WIDE2-1`|1|
|extremely remote fixed|`WIDE2-2`||
|metropolitan mobile|`WIDE1-1,WIDE2-1`|2|
|extremely remote mobile|`WIDE1-1,WIDE2-2`||
|space satellites|`ARISS,WIDE2-1`|3|

Note:
- The first `n` digit in `n-N` paradigm paths indicates the coverage level of the digipeater, whereby `1` is for domestic fill‑in digipeaters and `2` is for county-level digipeaters.
- The second `N` digit indicates the number of repeats at the indicated coverage level.


## Compressed Geolocation Frames

|_Callsign_|_SSID_,<br/>_Path Code_&nbsp;&<br/>_Data Type Code_|_Compressed Data_|
|:--------:|:-------------------------------------------------:|:---------------:|
|4 bytes|1 byte|13 bytes|
|`CCCC`|`D`|`/XXXXYYYY$csT`|

where:
- `CCCC`: the compressed 6 character _Callsign_
- `D`:
  + the compressed _SSID_ (between SSID 0 [none] and 15; included),
  + the _Path Code_ (between path 0 [none] and 3; included), and
  + the _Data Type Code_ (between type 0 and 3; included)
- `/`: the _Symbol Table Identifier_
- `XXXX`: the Base91 compressed longitude
- `YYYY`: the Base91 compressed latitude
- `$`: the _Symbol Code_
- `cs`: the compressed course (in degrees) and speed (in knots)
- `T`: the _Compression Type Byte_

> **⚠ <u>DO NOT</u> add any altitude data or comment!**
> Any transmitted bytes beyond the `T` _Compression Type Byte_ will result in the <u>entire</u> geolocation frame being <u>rejected</u> by the i‑gate <u>by design</u>.
> Terrestrial objects do not require sending altitude data.
> Flying objects may alternate the `csT` bytes between altitude and course & speed.
> Only if deemed absolutely necessary, transmit any other information with an occassional [_Status Report_](#compressed-status-report-frames).


## Compressed Weather Report Frames

|_Callsign_|_SSID_,<br/>_Path Code_&nbsp;&<br/>_Data Type Code_|_Compressed Data_|
|:--------:|:-------------------------------------------------:|:---------------:|
|4 bytes|1 byte|24 bytes|
|`CCCC`|`D`|`/XXXXYYYY_csTgtrrppPPhbb`|

where:
- `CCCC`: the compressed 6 character _Callsign_
- `D`:
  + the compressed _SSID_ (between SSID 0 [none] and 15; included),
  + the _Path Code_ (between path 0 [none] and 3; included), and
  + the _Data Type Code_ (between type 0 and 3; included)
- `/`: the _Symbol Table Identifier_
- `XXXX`: the Base91 compressed longitude
- `YYYY`: the Base91 compressed latitude
- `_`: the weather report _Symbol Code_
- `cs`: the compressed wind direction (in degrees) and sustained one-minute wind speed (in knots)
- `T`: the _Compression Type Byte_
- `g`: gust (half of peak wind speed in km/h in the last 5 minutes)
- `t`: temperature (in kelvin above 173.15 K)
- `rr`: rainfall (in mm) in the last hour
- `pp`: rainfall (in mm) in the last 24 hours
- `PP`: rainfall (in mm) since midnight
- `h`: humidity (in %)
- `bb`: barometric pressure (in Pa above 50000)

Here is a list of [weather records](https://en.wikipedia.org/wiki/List_of_weather_records).

**[TBD]** algorithms


## Compressed Text
In order to prevent channel congestion, it is crucial to limit the character set of messages. This allows for more frame compression.
In resemblance to Morse code, the character set would contain only 26 Latin lower‑case letters, the 10&nbsp;digits, space and a few punctuation marks and symbols. Limiting the set to 42 characters lets it fit 6 times in the 256 character set of LoRa.

|character set|amount|
|:-----------:|:----:|
|Latin lower‑case letters|26|
|digits|10|
|space|1|
|punctuation `.`&nbsp;`?`|2|
|symbols `-`&nbsp;`/`&nbsp;`_`|3|
|**TOTAL**|**42**|

### Encoding tttt…tttt
1. Perform character replacement and filtering on the given string; only allow for charcters of the [42&nbsp;character set](#compressed-text).
2. Treat the resulting text string as a Base42 encoding. Decode it first to an integer.
3. Then, encode this integer as a Base256 `tttt…tttt` bytestring.

### Decoding tttt…tttt
1. First, decode the given Base256 `tttt…tttt` bytestring to an integer.
2. Then, encode this integer as a Base42 string, corresponding to the text.

### Codec Algorithms for tttt…tttt
- [Python3](compression.py) compression algorithms and tests **[TODO]**
- [MIT License](https://github.com/aprs434/aprs434.github.io/blob/main/LICENSE)


## Comments
> **⚠ <u>REFRAIN</u> from adding any comments!**
> Adding more bytes to a LoRa frame only reduces the chances on successful reception.
> Rather, consider sending an occasional [status report](#compressed-status-report-frames).


## Compressed Status Report Frames
Obviously, above `tttt…tttt` compression can also be applied to other APRS text frame types.
For example for `>` APRS status reports. In practice, status reports are also often employed to send telemetry data.

|_Callsign_|_SSID_,<br/>_Path Code_&nbsp;&<br/>_Data Type Code_|_Compressed Data_|
|:--------:|:-------------------------------------------------:|:---------------:|
|4 bytes|1 byte|≤&nbsp;15&nbsp;bytes|
|`CCCC`|`D`|`tttt…tttt`|

where:
- `CCCC`: the compressed 6 character _Callsign_
- `D`:
  + the compressed _SSID_ (between SSID 0 [none] and 15; included),
  + the _Path Code_ (between path 0 [none] and 3; included), and
  + the _Data Type Code_ (between type 0 and 3; included)
- `tttt…tttt`: maximum 15 bytes of compressed text from a limited 42 character set, corresponding to 22 uncompressed characters


## Compressed Item Report Frames

|_Callsign_|_SSID_,<br/>_Path Code_&nbsp;&<br/>_Data Type Code_|_Compressed Data_|
|:--------:|:-------------------------------------------------:|:---------------:|
|4 bytes|1 byte|20 bytes|
|`CCCC`|`D`|`/XXXXYYYY$csTttttttt`|

where:
- `CCCC`: the compressed 6 character _Callsign_
- `D`:
  + the compressed _SSID_ (between SSID 0 [none] and 15; included),
  + the _Path Code_ (between path 0 [none] and 3; included), and
  + the _Data Type Code_ (between type 0 and 3; included)
- `/`: the _Symbol Table Identifier_
- `XXXX`: the Base91 compressed longitude
- `YYYY`: the Base91 compressed latitude
- `$`: the _Symbol Code_
- `cs`: the compressed course and speed
- `T`: the _Compression Type Byte_
- `ttttttt`: the 9 character item name in 7 bytes compressed text from a limited 42 character set


## Compressed Addressed Message Frames
Up to now, APRS has been unduly considered to be predominantly a one-way localisation technology. This went to the point that many mistakenly think the letter "P" in the acronym APRS would stand for "position." [Bob Bruninga WB4APR (SK)](http://www.aprs.org), the spiritual father of APRS, deeply resented this situation.

> _"APRS is not a vehicle tracking system. It is a two-way tactical real-time digital communications system between all assets in a network sharing information about everything going on in the local area."_
 
In Bob's view of APRS as being foremost a real-time situational and tactical tool, messaging definitely merits its place.
One of the long-term goals is rendering APRS messaging more popular by offering messaging pager designs.

Below proposal for the compression of addressed LoRa message frames is still somewhat tentative since on air experience is limited. Therefore, below specification **may be subject to change.**

Furthermore, 2‑way messaging requires [SF11](#lora-link-parameters) and GPS-disciplined, dynamic [time division multiple access (TDMA)](https://en.wikipedia.org/wiki/Time-division_multiple_access) multiplexing, which protocol is beyond the scope of this document. Therfore, below proposals for LoRa text frames should be foremost considered as an **uplink protocol only,** e.g. for SOTA or POTA self-spotting, emergencies, telemetry, status reports etc.

|_Callsign_|_SSID_,<br/>_Path Code_&nbsp;&<br/>_Data Type Code_|_Compressed Data_|
|:--------:|:-------------------------------------------------:|:---------------:|
|4 bytes|1 byte|≤&nbsp;d bytes|
|`CCCC`|`D`|`EEEEFtttt…tttt`|

where:
- `CCCC`: the compressed 6 character _Callsign_
- `D`:
  + the compressed _SSID_ (between SSID 0 [none] and 15; included),
  + the _Path Code_ (between path 0 [none] and 3; included), and
  + the _Data Type Code_ (between type 0 and 3; included)
- `EEEE`: the compressed _Addressee_ (6 character callsign)
- `F`:
  + the compressed _Addressee SSID_ (between SSID 0 [none] and 15; included), and
  + the _Message No_ (from 0 to 15; included)
- `tttt…tttt`: compressed text from a limited 42 character set.
- `d`: a sensible maximum allowed number of compressed data bytes, taking into account the [stepped airtime function](#measurable-benefits)

### Encoding and Decoding EEEE
The `EEEE` codec algorithms are identical to the [`CCCC` codec algorithms](#encoding-cccc).

### Encoding F
1. First, multiply the _SSID_ integer by&nbsp;16.
2. Then, algebraically add to this the _Message No_ integer.
3. Finally, convert the resulting integer to a single Base256 `F` byte.

### Decoding F
1. First, decode the given Base256 `F` byte to an integer.
2. The _SSID_ equals the integer quotient after [integer division](https://en.wikipedia.org/wiki/Division_(mathematics)#Of_integers) of the decoded integer by&nbsp;16.
3. Whereas the _Message No_ equals the [remainder](https://en.wikipedia.org/wiki/Remainder) of the decoded integer by&nbsp;16 ([modulo operation](https://en.wikipedia.org/wiki/Modulo_operation)).


## ITU Regulation
From a ITU regulatory point of view, long range communication —which, by definition, includes LoRa— is not allowed on ISM (Industrial, Scientific&nbsp;& Medical) bands. ISM&nbsp;bands are intended for local use only.

The amateur radio service forms a sole exception to this, as its 70&nbsp;cm UHF band happens to [overlap](https://hamwaves.com/lpd433/en/index.html#lpd433-channels) the [ITU&nbsp;Region&nbsp;1](https://en.wikipedia.org/wiki/ITU_Region) 434&nbsp;MHz ISM&nbsp;band as a primary service.
Moreover, ham radio is not restricted to a 20&nbsp;dBm (=&nbsp;100&nbsp;mW) power level, nor any 1% duty cycle limits on this band.

As a general rule, secondary users should always check whether a frequency is in use by a primary user before transmitting on air.
However, LoRa has no carrier sensing capability. Therefore, secondary ISM band users lack the ability to check whether an amateur radio operator is using the 434&nbsp;MHz band as a primary user.


## Reducing Power Consumption
1. OLED displays have a limited life span and consume quite a bit of power. An OLED screen and its driver [can be put to sleep](https://bengoncalves.wordpress.com/2015/10/01/oled-display-and-arduino-with-power-save-mode/) when the tracker is idle. The same holds true for the LoRa radio module and the ESP32. This needs to be investigated.
2. GPS modules are also power hogs. It may be conceivable to use the WLAN receiver aboard an ESP32 for localisation, whereby the three strongest WLAN SSIDs are transmitted to the i‑gate. The i‑gate would then guess the tracker location from a freely available [wardriving](https://en.wikipedia.org/wiki/Wardriving) data service from the Internet. This is comparable to how Google Android smartphone localisation works.


## Recommended Hardware

### Tracker Hardware:
- TTGO T-Beam 433&nbsp;MHz v0.7 or v1.1
- longer 433&nbsp;MHz antenna with [SMA male](https://en.wikipedia.org/wiki/SMA_connector) connector
- 16.9&nbsp;mm long tiger tail wire soldered to the female SMA socket
- 5&nbsp;V, 3&nbsp;A microUSB charge adapter
- Panasonic NCR18650B Li-ion cell, or quality equivalent
- glue gun to stick the GPS antenna to the cell holder
- SH1106 1.3" I²C (4‑pin) OLED display (slightly larger than the usual 0.8" displays often sold with the TTGO T-Beam)
- enclosure

### I-Gate Hardware:
- Either:
  + [TTGO LORA32 433&nbsp;MHz v2](http://www.lilygo.cn/prod_view.aspx?TypeId=50060&Id=1319&FId=t3:50060:3) ([U.FL](https://en.wikipedia.org/wiki/Hirose_U.FL) or [SMA female](https://en.wikipedia.org/wiki/SMA_connector) RF socket), or
  + maybe Heltec ESP32 LoRa 433&nbsp;MHz **v2** ([U.FL](https://en.wikipedia.org/wiki/Hirose_U.FL) female RF socket); subject to satisfactory receiver testing
  + **⚠ <u>DO NOT USE</u>** Heltec ESP32 LoRa 433&nbsp;MHz **v1** as it is as deaf as a post!
- 70&nbsp;cm amateur radio colinear groundplane antenna with coaxial cable and connectors
- 16.9&nbsp;mm long tiger tail wire soldered to the RF socket
- 5&nbsp;V, 1&nbsp;A microUSB power supply
- enclosure


## ESP32 Firmware Downloads

### Tracker Firmware
See: <https://github.com/aprs434/lora.tracker>

Please, note that the [`tracker.json`](https://github.com/aprs434/lora.tracker/blob/master/data/tracker.json) configuration file has been much simplified.

### I-Gate Firmware
See: <https://github.com/aprs434/lora.igate>

> Currently, the APRS&nbsp;434 tracker is still compatible with the i-gate developed by Peter Buchegger, OE5BPA. However, this will soon change as more LoRa frame compression is added.
>
> We feel confident that trackers with the proposed APRS&nbsp;434 compressed LoRa frame will eventually become dominant because of the longer range merit. To smooth out the transition, we are developing an **i‑gate capable of understanding both formats;** i.e. compressed APRS&nbsp;434&nbsp;and longer, legacy OE5BPA.
>
> It is strongly advised to install [**the accompanying APRS&nbsp;434 i-gate**](https://github.com/aprs434/lora.igate) as new releases will be automatically pulled over‑the‑air (OTA) via WiFi.


## Development Road Map

### Data Link Layer

|tracker<br/>firmware|completed|feature|LoRa payload|compatible with OE5BPA i‑gate|
|:------------------:|:-------:|:-----:|:----------:|:---------------------------:|
|v0.0.0|✓|original [OE5BPA tracker](https://github.com/lora-aprs/LoRa_APRS_Tracker)|113 bytes|✓|
|v0.1.0|✓|byte-saving [`tracker.json`](https://github.com/aprs434/lora.tracker/blob/master/data/tracker.json)|87 bytes|✓|
|v0.2.0|✓|fork of the [OE5BPA tracker](https://github.com/lora-aprs/LoRa_APRS_Tracker)<br/>with significantly less transmitted&nbsp;bytes|44 bytes|✓|
|v0.3.0|✓|[Base91](https://en.wikipedia.org/wiki/List_of_numeral_systems#Standard_positional_numeral_systems) compression of  location, course&nbsp;and speed&nbsp;data|31 bytes|✓|
|[v0.4.0](https://github.com/aprs434/lora.tracker)|✓|removal of the transmitted [newline](https://en.wikipedia.org/wiki/Newline) `\n`&nbsp;character at&nbsp;frame&nbsp;end|30 bytes|✓|
|||random time jitter between fixed interval packets to&nbsp;avoid repetitive&nbsp;[collisions](https://en.wikipedia.org/wiki/Collision_domain)|30 bytes|✓|
|||[tracker](https://github.com/aprs434/lora.tracker) and [i-gate](https://github.com/aprs434/lora.igate) with frame&nbsp;address&nbsp;compression,<br/>no custom&nbsp;header in&nbsp;payload|18 bytes|use the [APRS&nbsp;434 i‑gate](https://github.com/aprs434/lora.igate)|

> Currently, the APRS&nbsp;434 tracker is still compatible with the i-gate developed by Peter Buchegger, OE5BPA. However, this will soon change as more LoRa frame compression is added.
>
> We feel confident that trackers with the proposed APRS&nbsp;434 compressed LoRa frame will eventually become dominant because of the longer range merit. To smooth out the transition, we are developing an **i‑gate capable of understanding both formats;** i.e. compressed APRS&nbsp;434&nbsp;and longer, legacy OE5BPA.
>
> It is strongly advised to install [**the accompanying APRS&nbsp;434 i-gate**](https://github.com/aprs434/lora.igate) as new releases will be automatically pulled over‑the‑air (OTA) via WiFi.

### Tracker Hardware

|tracker<br/>firmware|completed|feature|
|:------------------:|:-------:|:-----:|
|v0.3.1|✓|coordinates displayed on screen|
|||reduced power consumption through [SH1106 OLED sleep](https://bengoncalves.wordpress.com/2015/10/01/oled-display-and-arduino-with-power-save-mode/)|
|||button press to activate OLED screen|
|||ESP32 power reduction|

### Messaging
At first, only uplink messaging to an i-gate will be considered. This is useful for status updates, [SOTA self‑spotting](https://www.sotaspots.co.uk/Aprs2Sota_Info.php), or even emergencies.

On the other hand, bidirectional messaging requires time division multiplexing between the up- and downlink, based on precise GPS timing. That is because channel isolation between different up- and downlink frequencies probably would require costly and bulky resonant cavities.

|tracker<br/>firmware|completed|feature|
|:------------------:|:-------:|:-----:|
|||add a [library](https://web.archive.org/web/20190316204938/http://cliffle.com/project/chatpad/arduino/) for the [Xbox 360 Chatpad](https://nuxx.net/gallery/v/acquired_stuff/xbox_360_chatpad/) keyboard|
|||[support](https://www.hackster.io/scottpowell69/lora-qwerty-messenger-c0eee6) for the [M5Stack CardKB Mini](https://shop.m5stack.com/products/cardkb-mini-keyboard) keyboard|

### WiFi Geolocation
TBD


## News, Social & Co-Development
Feel free to join our public [**Telegram Group**](https://t.me/aprs434) for the latest news and cordial discussions.

You are invited to contribute code improvements to [**this project on GitHub**](https://github.com/aprs434).
Here is a lightweight [video introduction to using GitHub](https://youtu.be/tCuPbW31vAw) by Andreas Spiess, HB9BLA.

<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$']]
  }
};
</script>
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
