provider "aws" {
  region = "us-west-2"  # Change to your desired region
}

# Create an S3 bucket to store Docker image if using Amazon ECR or for logs
resource "aws_s3_bucket" "bucket" {
  bucket = "hand-gesture-recognition-bucket"
}

# Create an ECS Cluster
resource "aws_ecs_cluster" "gesture_cluster" {
  name = "gesture-recognition-cluster"
}

# Create a Docker image repository in AWS ECR
resource "aws_ecr_repository" "gesture_repo" {
  name = "hand-gesture-recognition-repo"
}

# Push your Docker image to the repository
# Follow AWS documentation to push Docker image to the ECR

# Define ECS Task Definition
resource "aws_ecs_task_definition" "gesture_task" {
  family                   = "gesture-recognition-task"
  execution_role_arn       = "arn:aws:iam::aws_account_id:role/ecsTaskExecutionRole" # Replace with actual execution role ARN
  task_role_arn            = "arn:aws:iam::aws_account_id:role/ecsTaskExecutionRole"  # Replace with actual task role ARN
  network_mode             = "awsvpc"
  container_definitions    = <<DEFINITION
    [
      {
        "name": "gesture-container",
        "image": "${aws_ecr_repository.gesture_repo.repository_url}:latest",
        "memory": 512,
        "cpu": 256,
        "essential": true,
        "portMappings": [
          {
            "containerPort": 5000,
            "hostPort": 5000,
            "protocol": "tcp"
          }
        ]
      }
    ]
  DEFINITION
}

# Create a security group to allow access to your container
resource "aws_security_group" "gesture_sg" {
  name        = "gesture-security-group"
  description = "Allow inbound access to hand gesture container"
  
  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create an ECS Service to run the task
resource "aws_ecs_service" "gesture_service" {
  name            = "gesture-recognition-service"
  cluster         = aws_ecs_cluster.gesture_cluster.id
  task_definition = aws_ecs_task_definition.gesture_task.id
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    subnets          = ["subnet-xxxxxx"] # Replace with actual subnet
    security_groups  = [aws_security_group.gesture_sg.id]
    assign_public_ip = true
  }
}

# Optionally, create an Elastic Load Balancer if needed
resource "aws_lb" "gesture_lb" {
  name               = "gesture-recognition-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups   = [aws_security_group.gesture_sg.id]
  subnets           = ["subnet-xxxxxx"] # Replace with your subnet
}

# Configure listener for the Load Balancer
resource "aws_lb_listener" "gesture_lb_listener" {
  load_balancer_arn = aws_lb.gesture_lb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "fixed-response"
    fixed_response {
      status_code = 200
      message_body = "OK"
      content_type = "text/plain"
    }
  }
}
