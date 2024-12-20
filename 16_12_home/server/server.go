package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net"
	"net/http"
	"strconv"
	"sync"

	"google.golang.org/grpc"
	pb "homework.com/generated"
)

// Реализация сервиса
type LibraryServer struct {
	pb.UnimplementedLibraryServiceServer
	mu     sync.Mutex
	books  []*pb.Book
	nextID int32
}

func (s *LibraryServer) AddBook(ctx context.Context, req *pb.AddBookRequest) (*pb.AddBookResponse, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	// Создаем новую книгу
	book := &pb.Book{
		Id:     s.nextID,
		Title:  req.Title,
		Author: req.Author,
	}
	s.books = append(s.books, book)
	s.nextID++

	return &pb.AddBookResponse{Id: book.Id}, nil
}

func (s *LibraryServer) ListBooks(ctx context.Context, req *pb.Empty) (*pb.ListBooksResponse, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	return &pb.ListBooksResponse{Books: s.books}, nil
}

func (s *LibraryServer) GetBook(ctx context.Context, req *pb.GetBookRequest) (*pb.GetBookResponse, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	for _, book := range s.books {
		if book.Id == req.Id {
			return &pb.GetBookResponse{Book: book}, nil
		}
	}

	return nil, fmt.Errorf("book with ID %d not found", req.Id)
}

// HTTP Handlers

// Обработчик для добавления книги
func (s *LibraryServer) handleAddBook(w http.ResponseWriter, r *http.Request) {
	var req pb.AddBookRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// Call the gRPC service
	resp, err := s.AddBook(context.Background(), &req)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

// Обработчик для получения списка книг
func (s *LibraryServer) handleListBooks(w http.ResponseWriter, r *http.Request) {
	// Call the gRPC service
	resp, err := s.ListBooks(context.Background(), &pb.Empty{})
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

// Обработчик для получения книги по ID
func (s *LibraryServer) handleGetBook(w http.ResponseWriter, r *http.Request) {
	// Получаем ID книги из параметров URL
	id := r.URL.Query().Get("id")
	if id == "" {
		http.Error(w, "ID is required", http.StatusBadRequest)
		return
	}

	// Преобразуем строку id в int32
	bookID, err := strconv.Atoi(id)
	if err != nil {
		http.Error(w, fmt.Sprintf("Invalid ID format: %v", err), http.StatusBadRequest)
		return
	}

	// Вызываем gRPC сервис
	resp, err := s.GetBook(context.Background(), &pb.GetBookRequest{Id: int32(bookID)})
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Отправляем ответ в формате JSON
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

func main() {
	// Настроим gRPC сервер
	listener, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	grpcServer := grpc.NewServer()
	libraryServer := &LibraryServer{nextID: 1}
	pb.RegisterLibraryServiceServer(grpcServer, libraryServer)

	// Запуск HTTP сервера
	http.HandleFunc("/addBook", libraryServer.handleAddBook)
	http.HandleFunc("/listBooks", libraryServer.handleListBooks)
	http.HandleFunc("/getBook", libraryServer.handleGetBook)

	// Статические файлы для веб-интерфейса
	http.Handle("/", http.StripPrefix("/", http.FileServer(http.Dir("web"))))

	// Запуск HTTP сервера в горутине
	go func() {
		log.Println("Starting HTTP server on port :8080...")
		if err := http.ListenAndServe(":8080", nil); err != nil {
			log.Fatalf("failed to start HTTP server: %v", err)
		}
	}()

	// Запуск gRPC сервера
	log.Println("Starting gRPC server on port :50051...")
	if err := grpcServer.Serve(listener); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
