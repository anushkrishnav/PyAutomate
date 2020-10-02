# github: rkgeekoftheweek

# install required packages
import PyPDF2
import pyttsx3


def read_book(bookName):
    pdfBook = open(bookName, "rb")
    pdfReader = PyPDF2.PdfFileReader(pdfBook)
    return pdfReader


def listen_book(reader, pageNumber):
    speaker = pyttsx3.init()
    page = reader.getPage(pageNumber)
    text = page.extractText()
    speaker.say(text)
    speaker.runAndWait()


if __name__ == "__main__":

    # change bookname and page number here
    bookName = "alchemist.pdf"
    pageNumber = 7

    reader = read_book(bookName)
    listen_book(reader, pageNumber)
