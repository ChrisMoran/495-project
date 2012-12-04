
import urllib.request
import urllib.parse

def search(term):
  url = "http://ec2-23-20-206-252.compute-1.amazonaws.com/search/?query="+urllib.parse.quote_plus(term[:-1])
  print(url)
  request = urllib.request.Request(url) 
  response = urllib.request.urlopen(request)

def main():
  
  print("opened file")
  res={};
  fr_ids = open("SearchTerms.txt");
  print("opened file")
  for line in fr_ids:

      if line[0] != "#" and line[0] != "\n":
        search(line);
        
  return res;  

if __name__ == "__main__":
    main()
