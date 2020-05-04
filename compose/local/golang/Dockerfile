from golang:latest


WORKDIR /go/src/app



COPY ./orderbook_veinte/order_book_ws/ .

RUN pwd

RUN go get -d -v ./...
RUN go install -v ./...


#RUN go get -u -v -f all  


RUN go build  . 

#RUN ./order_book_ws

CMD [ "app" ]