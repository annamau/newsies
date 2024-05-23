from gatherer.gatherer import gather
from transformator.summarizer_ollama import summarize
import time

def main():
    gather(1)
    summarize()
    
def __init__():
    start = time.time()
    main()
    end = time.time()
    print("Time elapsed during gathering and summarize: ", end - start)