if (__name__ == '__main__'):
    import ftplib
    session = ftplib.FTP('server.address.com','USERNAME','PASSWORD')
    file = open('kitten.jpg','rb')                  # file to send
    session.storbinary('STOR kitten.jpg', file)     # send the file
    file.close()                                    # close file and FTP
    session.quit()
    