# Chapter 2 - Deciphering the Markets with Technical Analysis

Explored different technical analysis indicators.

# Problems Identified in Chapter 2

### 1) Code not following standard practice
####   - Inconsistencies in white-spacings and lack of comments throughout
####   - Repeated code can be written in a separate file
####   - Imports can be grouped at top of file
####   - Typos like referring to lowercase sigma as lowercase delta (page 63, BBANDS formulas)

### 2) Variance (sigma<sup>2</sup>) for calculating Bollinger Bands computed by 1/N * ∑(P<sub>*i*</sub> - mean)<sup>2</sup>
####   - Is it the right way? Since at time *i*, we do not yet know P<sub>i+k</sub> future values, so how can we calculate variance at time *i* with unknown future prices?