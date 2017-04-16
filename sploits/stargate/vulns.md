# Stargate vulns

## Check some data but use others
Stargate authorization mechanism uses HMAC256 value calculated by raw bytes of transmission name. However internal index use Base64 string representation of this bytes for maintaining uniqueness of transmissions. The question is, are there any Base64 strings that represents the same bytes sequences of the name? The answer is, of course, it depends on implementation.
First of all .net implementation ignores [ \t\n\r] chars, but this way to exploit was closed by removing all whitespaces in header value.
The second way depends on string length and output padding. Look at this example:

<table class="wikitable">
<tbody><tr>
<th scope="row">Text</th>
<td colspan="8" align="center">M</td>
<td colspan="8" align="center">a</td>
<td colspan="8" align="center"></td>
</tr>
<tr>
<th scope="row">ASCII</th>
<td colspan="8" align="center">77 (0x4d)</td>
<td colspan="8" align="center">97 (0x61)</td>
<td colspan="8" align="center">0 (0x00)</td>
</tr>
<tr>
<th scope="row">Bits</th>
<td>0</td>
<td>1</td>
<td>0</td>
<td>0</td>
<td>1</td>
<td>1</td>
<td>0</td>
<td>1</td>
<td>0</td>
<td>1</td>
<td>1</td>
<td>0</td>
<td>0</td>
<td>0</td>
<td>0</td>
<td>1</td>
<td><b>0</b></td>
<td><b>0</b></td>
<td>0</td>
<td>0</td>
<td>0</td>
<td>0</td>
<td>0</td>
<td>0</td>
</tr>
<tr>
<th scope="row">Index</th>
<td colspan="6" align="center">19</td>
<td colspan="6" align="center">22</td>
<td colspan="6" align="center">4</td>
<td colspan="6" align="center">0</td>
</tr>
<tr>
<th scope="row">Base64</th>
<td colspan="6" align="center">T</td>
<td colspan="6" align="center">W</td>
<td colspan="6" align="center">E</td>
<td colspan="6" align="center">=</td>
</tr>
</tbody></table>

Bolded two bits are insignificant to decoded value. That's why:
```
> Convert.FromBase64String("TWE=")
byte[2] { 77, 97 }
> Convert.FromBase64String("TWG=")
byte[2] { 77, 97 }
> Convert.FromBase64String("TWH=")
byte[2] { 77, 97 }
```

https://en.wikipedia.org/wiki/Base64

## Buffer over-read
[DirectBitmap](https://github.com/HackerDom/ructf-2017/blob/master/services/stargate/src/utils/DirectBitmap.cs#L13) class uses unsafe int* pointer to raw pixels however image PixelFormat isn't checked to be 32bpp. This allows to over-read data on unmanaged heap. Data is used later for histogram aka "spectrum" calculation. With some good probability HMAC256 openssl implementation allocated immediately after image data. As a result ones can use histograms statistics in response on image upload requests to brute-force 128 bit of the HMAC key.
