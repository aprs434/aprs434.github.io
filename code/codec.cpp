/*

C++ codec algorithms for APRS 434 LoRa:

    - Callsign Compression CCCC
    - SSID, pathCode & Data Type Compression D

    - Callsign Compression EEEE
    - SSID & MessageNo Compression F

    - Text Compression tttt


REVISION HISTORY

    2022-05-11 PA0FOT Initial version and tests


REQUIRES
    $ sudo apt install libboost-all-dev


CAVEAT ON ESP32

    Avoid deep recursive function calls.
    Individual recursive function calls do not always add a lot of stack usage each time they are called,
    but if each function includes large stack-based variables then the overhead can get quite high.

    https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/performance/ram-usage.html


CAVEAT LARGEST INTEGER

    The largest unsigned integer produced by this algorithm is:
    In [1]: 42**51
    Out[1]: 61053956130164410003966197248726664261467607807747252759217406888527859374733918208

*/

// #define DEBUG


#include <assert.h>
#include <iostream>
#include <cstdio>
#include <cstring>
#include <cctype>
#include <cmath>
#include "uintwide_t.h"

#define uchar uint8_t
#define uint uint32_t

static void strrev(char s[])
{
    int length = strlen(s) ;
    int c, i, j;

    for (i = 0, j = length - 1; i < j; i++, j--)
    {
        c = s[i];
        s[i] = s[j];
        s[j] = c;
    }
}

namespace mp = math::wide_integer;
using std::cout;
using std::endl;
using std::dec;
using std::hex;

const char* digits = " 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-./?@";

uchar bytes[100];

uint32_t encodeCallsign(const char *callsign) {
    const int b = 37;

    uint32_t result;
    uint32_t weight;
    int i, j, k, ch;

    assert(b <= strlen(digits));
    assert(b > 1);

    result = 0, weight = 1;
    for (i = j = strlen(callsign); i > 0; i--)         // iterate over input string
    {
        ch=toupper(callsign[i-1]);
        for (k = 0; k < strlen(digits); k++) {    //lookup char index
            if (digits[k] == ch) {
                break;
            }
        }
        if (k == strlen(digits))                  // ignore if ch not found in digits
            continue;
        result = result + ((k) * weight);
        weight = weight * b;
    }

    return result;                                // result can be pow(42,51)!
}

uchar* encodeBase(int n, mp::uint512_t num) {     // base n, unsigned num - 64 bytes max

    int i, nummodn;

    assert(n <= strlen(digits));
    assert (n > 1);

    i = 0;
    while (num > 0) {
        nummodn = (int)(num % n);
        bytes[i++] = digits[nummodn];
        num /= n;
    };
    bytes[i] = 0;
    strrev((char*)bytes);

    return bytes;                                 // return base n encoded '\0' terminated string
}

mp::uint512_t decodeBase(int b, char* str) {      // base b, str 64 bytes max '\0' terminated

    mp::uint512_t result;
    mp::uint512_t weight;
    int i, j, k, ch;

    assert(b <= strlen(digits));
    assert (b > 1);

    result = 0, weight = 1;
    for (i = j = strlen(str); i > 0; i--)         // iterate over input string
    {
        ch=toupper(str[i-1]);
        for (k = 0; k < strlen(digits); k++) {    //lookup char index
            if (digits[k] == ch) {
                break;
            }
        }
        if (k == strlen(digits))                  // ignore if ch not found in digits
            continue;
        result = result + ((k) * weight);
        weight = weight * b;
    }

    return result;                                // result can be pow(42,51)!
}

uint encodeCCCC(std::string s) {
    return (uint)decodeBase(37, (char*)s.c_str());
}

uchar* decodeCCCC(uint i) {
    return encodeBase(37, i);
}

mp::uint512_t encodetttt(std::string s) {
    return decodeBase(42, (char*)s.c_str());
}

uchar* decodetttt(mp::uint512_t i) {
    return encodeBase(42, i);
}

int main() {

    char uncompressed[] = "0 This is ON4AA-6. QSL? @ Yes/No";
    char challenge[100];

    int i;

    const char* callsigns[] =
    {
        "ON4AA", "PA0FOT", "cd2rxu", "W3A", "W3A   ", "ZZZZZZ", "HB9EGM", "0HN0"
    };

    for (const char* callsign : callsigns) {
        uint e1 = encodeCCCC(callsign);
        uint32_t e2 = encodeCallsign(callsign);

        printf("%08x\n", e1);
        printf("%s %s\n\n", decodeCCCC(e1), decodeCCCC(e2));

        if (e1 != e2) {
            printf("%08x\n", e2);
            printf("%s\n\n", decodeCCCC(encodeCallsign(callsign)));
        }
    }

    mp::uint512_t bignum = encodetttt((char*) uncompressed);
    cout << hex << bignum << " = " << dec << sizeof(bignum) << " bytes" << endl;
    cout << "Bytewise: ";
    for (int i = 0; i <= 512; i += 8) {
        auto v = static_cast<uint8_t>((bignum >> (512-i)) & 0xFF);
        if (v) {
            cout << hex << (int)v;
        }
    }
    cout << dec << endl;

    decodetttt(bignum);
    cout << bytes << " =  " << strlen((char*)bytes) << " bytes" << endl;


    while (1) {
        printf("\nEnter text for testing, or press enter to exit\n");
        printf("-> ");
        i = 0;
        while(i<sizeof(challenge)-1) {
            scanf("%c", &challenge[i]);
            if (challenge[i] == '\n')
                break;
            i++;
            }
        challenge[i]='\0';

        if (i == 0)
            break;

        cout << "challenge: '" << challenge << "' - " << strlen(challenge) << " bytes" << endl;
        cout << "encoded  : " << hex << (bignum = encodetttt(challenge)) << dec << endl;

        cout << "Bytewise: ";
        for (int i = 0; i <= 512; i += 8) {
            auto v = static_cast<uint8_t>((bignum >> (512-i)) & 0xFF);
            if (v) {
                cout << hex << (int)v;
            }
        }
        cout << dec << endl;

        decodetttt(bignum);
        cout << "decoded  : '" << bytes << "' - " << strlen((char*)bytes) << " bytes" << endl << endl;
    }

    return 0;
}
