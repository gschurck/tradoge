FROM golang:1.23-alpine3.20 AS builder

WORKDIR /app

# Copy go mod files
COPY go.mod ./

# Download dependencies
RUN go mod download

# Copy source code
COPY . .

# Build the application
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# Use a minimal alpine image for the final stage
FROM alpine:3.20

WORKDIR /app

# Copy the binary from builder
COPY --from=builder /app/main .


# Set the binary as the entrypoint
ENTRYPOINT ["/app/main"]