#!/usr/bin/python
import string

def main():
  # get the list of tags and their frequency from input file
  taglist = getTagListSortedByFrequency('tags.txt')
  # find max and min frequency
  ranges = getRanges(taglist)
  # write out results to output, tags are written out alphabetically
  # with size indicating the relative frequency of their occurence
  writeCloud(taglist, ranges, 'tags.html')

def tag_weight(x):
    if x==None or x==0:
         x = 1
    return weight * math.log(x, math.e)

def getTagListSortedByFrequency(inputfile):
  inputf = open(inputfile, 'r')
  taglist = []
  while (True):
    line = inputf.readline()[:-1]
    if (line == ''):
      break
    (tag, count) = line.split("|")
    taglist.append((tag, int(count)))
  inputf.close()
  # sort tagdict by count
  taglist.sort(lambda x, y: cmp(x[1], y[1]))
  return taglist

def getRanges(taglist):
  mincount = taglist[0][1]
  maxcount = taglist[len(taglist) - 1][1]
  distrib = (maxcount - mincount) / 4;
  index = mincount
  ranges = []
  while (index <= maxcount):
    range = (index, index + distrib)
    index = index + distrib
    ranges.append(range)
  return ranges

def writeCloud(taglist, ranges, outputfile):
  outputf = open(outputfile, 'w')
  outputf.write("<style type=\"text/css\">\n")
  outputf.write(".smallestTag {font-size: xx-small;}\n")
  outputf.write(".smallTag {font-size: small;}\n")
  outputf.write(".mediumTag {font-size: medium;}\n")
  outputf.write(".largeTag {font-size: large;}\n")
  outputf.write(".largestTag {font-size: xx-large;}\n")
  outputf.write("</style>\n")
  rangeStyle = ["smallestTag", "smallTag", "mediumTag", "largeTag", "largestTag"]
  # resort the tags alphabetically
  taglist.sort(lambda x, y: cmp(x[0], y[0]))
  for tag in taglist:
    rangeIndex = 0
    for range in ranges:
      url = "http://www.google.com/search?q=" + tag[0].replace(' ', '+') + "+site%3Asujitpal.blogspot.com"
      if (tag[1] >= range[0] and tag[1] <= range[1]):
        outputf.write("<span class=\"" + rangeStyle[rangeIndex] + "\"><a href=\"" + url + "\">" + tag[0] + "</a></span> ")
        break
      rangeIndex = rangeIndex + 1
  outputf.close()

if __name__ == "__main__":
  main()
