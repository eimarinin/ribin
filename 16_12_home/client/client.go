package main

import (
	"context"
	"log"
	"time"

	"google.golang.org/grpc"
	pb "homework.com/generated"
)

func main() {
	// Устанавливаем соединение с сервером
	conn, err := grpc.Dial("localhost:50051", grpc.WithInsecure())
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()

	client := pb.NewLibraryServiceClient(conn)

	// Добавляем книгу
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	addResp, err := client.AddBook(ctx, &pb.AddBookRequest{Title: "Go Programming", Author: "Alan A. A. Donovan"})
	if err != nil {
		log.Fatalf("could not add book: %v", err)
	}
	log.Printf("Added Book ID: %d", addResp.Id)

	// Получаем список книг
	listResp, err := client.ListBooks(ctx, &pb.Empty{})
	if err != nil {
		log.Fatalf("could not list books: %v", err)
	}
	log.Println("Books in library:")
	for _, book := range listResp.Books {
		log.Printf("ID: %d, Title: %s, Author: %s", book.Id, book.Title, book.Author)
	}

	// Получаем информацию о книге по ID
	getResp, err := client.GetBook(ctx, &pb.GetBookRequest{Id: addResp.Id})
	if err != nil {
		log.Fatalf("could not get book: %v", err)
	}
	log.Printf("Book Details - ID: %d, Title: %s, Author: %s", getResp.Book.Id, getResp.Book.Title, getResp.Book.Author)
}
