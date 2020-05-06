from golang:latest


WORKDIR /go/src/app



COPY ./orderbook_veinte/order_book_ws/ .

RUN pwd

RUN go get -d -v ./...
RUN go install -v ./...


#RUN go get -u -v -f all  



#RUN ./order_book_ws
COPY ./compose/local/golang/start   /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start


CMD [ "app" , "/start" ]
ENTRYPOINT ["/start"]