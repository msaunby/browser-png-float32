# Simple decoder for WCS JSON format
#
# No attempt made to verify data is complete or agrees with header values
#
#This is what the data looks like -
#
sample_data = """
{
  "coverageData": [
    {
      "values": [
        [
          99.999999999999972,
          98.799999999999983,
          98.774547306499471
        ],
        [
          99.999999999999972,
          98.799999999999983,
          62.15816124492018
        ],
        [
          99.999999999999972,
          98.799999999999983,
          94.303465607543217
        ]
      ],
      "coordinates": [
        [
          {
            "lat": 52.13165,
            "long": -4.9326600000000074
          },
          {
            "lat": 52.13165,
            "long": -3.5266600000000086
          },
          {
            "lat": 52.13165,
            "long": -2.1206600000000098
          }
        ],
        [
          {
            "lat": 50.725650000000002,
            "long": -4.9326600000000074
          },
          {
            "lat": 50.725650000000002,
            "long": -3.5266600000000086
          },
          {
            "lat": 50.725650000000002,
            "long": -2.1206600000000098
          }
        ],
        [
          {
            "lat": 49.319650000000003,
            "long": -4.9326600000000074
          },
          {
            "lat": 49.319650000000003,
            "long": -3.5266600000000086
          },
          {
            "lat": 49.319650000000003,
            "long": -2.1206600000000098
          }
        ]
      ],
      "parameterName": "Total_cloud_cover",
      "units": "C_PERC",
      "modelName": "UKMO Post Processed\/EA Best Data - Medium Range",
      "modelRun": "2015-01-11T15:00:00Z",
      "modelForecast": "PT0S",
      "validity": "2015-01-11T15:00:00Z",
      "level": "atmosphere",
      "dataset": "spec:search-recent"
    }
  ],
  "parameterName": "Total_cloud_cover",
  "modelName": "UKMO Post Processed\/EA Best Data - Medium Range",
  "modelRun": "2015-01-11T15:00:00Z",
  "modelForecast": "PT0S",
  "validity": "2015-01-11T15:00:00Z",
  "level": "atmosphere",
  "dataset": "spec:search-recent"
}
"""

import json

def binary_wxjson( text ):
    import array
    data = array.array('f')
    inp = json.loads( text )
    for row in inp['coverageData'][0]['values']:
        for x in row:
            if x == None:
                data.append( 0.0 )
            else:
                data.append( x )
    #print data
    return data.tostring()

def binH_wxjson( text ):
    import array
    data = array.array('H')
    inp = json.loads( text )
    for row in inp['coverageData'][0]['values']:
        for x in row:
            if x == None:
                data.append( 0 )
            else:
                try:
                    data.append( int(x) )
                except:
                    data.append( 0 )
    return data.tostring()

def pngB_wxjson( text ):
    import png
    import StringIO
    strFile = StringIO.StringIO()
    inp = json.loads( text )
    data = []
    for row in inp['coverageData'][0]['values']:
        dataRow = []
        for x in row:
            if x == None:
                dataRow.append(0)
            else:
                try:
                    dataRow.append( int(x) )
                except:
                    dataRow.append( 0 ) 
        data.append( dataRow )
    img = png.from_array(data, mode='L;8', info={'compression':-1})  # 0 for no compression
    img.save(strFile)
    return strFile.getvalue()

def pngRGBA_wxjson( text ):
    import png
    import StringIO
    strFile = StringIO.StringIO()
    inp = json.loads( text )
    data = []
    for row in inp['coverageData'][0]['values']:
        dataRow = []
        for x in row:
            if x == None:
                dataRow.append(0)
            else:
                try:
                    dataRow.append( int(x) )
                except:
                    dataRow.append( 0 ) 
        data.append( dataRow )
    img = png.from_array(data, mode='L;16', info={'compression':-1})  # 0 for no compression
    img.save(strFile)
    return strFile.getvalue()

def pngFloat_wxjson( text ):
    import png
    import StringIO
    import struct
    strFile = StringIO.StringIO()
    inp = json.loads( text )
    data = []
    for row in inp['coverageData'][0]['values']:
        dataRow = []
        # struct.pack('%sf' % len(row), *row)
        for x in row:
            if x == None:
                dataRow.append([0,0,0,0])
            else:
                #try:
                (r,g,b,a) = struct.unpack('4B', struct.pack('f',x))
                dataRow.append(r)
                dataRow.append(g)
                dataRow.append(b)
                dataRow.append(a)
                #except:
                #    dataRow.append( [0,0,0,0] ) 
        data.append( dataRow )
    print data
    img = png.from_array(data, mode='RGBA', info={'compression':-1, 'alpha':True})  # 0 for no compression
    img.save(strFile)
    return strFile.getvalue()


if __name__ == '__main__':
    d = binary_wxjson( sample_data )
    p = pngH_wxjson( sample_data )
    print d
