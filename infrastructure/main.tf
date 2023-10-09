
data "aws_ami" "ecs_ami" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-ecs-hvm-*-x86_64-ebs"]
  }
}



resource "aws_s3_bucket" "this" {
  bucket = "rorychan-workout-bot"
  acl = "private"

}

resource "aws_iam_role" "this" {
  name = "workout_bot"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Action    = "sts:AssumeRole"
        Principal = {
          AWS = "arn:aws:iam::935625980877:root"
        }
      }
    ]
  })
}
data "aws_iam_policy_document" "s3_access" {
  statement {
    actions = [
      "s3:ListBucket",
      "s3:PutObject",
      "s3:GetObject",
      "s3:DeleteObject"
    ]
    effect = "Allow"
    resources = [
      "${aws_s3_bucket.this.arn}",
      "${aws_s3_bucket.this.arn}/*"
    ]
    sid = "s3access"
  }
}
resource "aws_iam_policy" "this" {
  policy = data.aws_iam_policy_document.s3_access.json
  name = "s3-bot-access"
}
resource "aws_iam_policy_attachment" "this" {
  name       = "attachment"
  policy_arn = aws_iam_policy.this.arn
  roles = [aws_iam_role.this.name]
}



resource "aws_vpc" "this" {
  cidr_block = "10.0.0.0/16"
  tags = {
    name = "Main"
  }
}
resource "aws_subnet" "this" {
  cidr_block = "10.0.1.0/24"
  vpc_id     = aws_vpc.this.id
  map_public_ip_on_launch = true
}
resource "aws_subnet" "second" {
  cidr_block = "10.0.2.0/24"
  availability_zone = "us-east-1a"
  vpc_id     = aws_vpc.this.id
  map_public_ip_on_launch = true
}

resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id
}



resource "aws_security_group" "this" {
  vpc_id = aws_vpc.this.id
  name = "Workout-bot_sg"
  ingress {
    from_port = 0
    protocol  = "tcp"
    to_port   = 0
    security_groups = [aws_security_group.lb.id]
  }
  ingress {
    from_port = 22
    protocol  = "tcp"
    to_port   = 22
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port = 0
    protocol  = "-1"
    to_port   = 0
    security_groups = [aws_security_group.lb.id]
  }
}

resource "aws_route_table" "this" {
  vpc_id = aws_vpc.this.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.this.id
  }
}
resource "aws_route_table_association" "this" {
  route_table_id = aws_route_table.this.id
  subnet_id = aws_subnet.this.id
}
resource "aws_route_table_association" "second" {
  route_table_id = aws_route_table.this.id
  subnet_id = aws_subnet.second.id
}


resource "aws_key_pair" "this" {
  key_name = "Workout_instance_key"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQD+TBRUz2VF7IpELG/19kFjOGruxvrMrO20g3Zr2rjKZI7sQax+2TJLjCqBXtb3/o+FprGrFWN0DI2TS23SOvAe2Io9Yl+uKh5qs4ounMBWCSCphfvTocvroFeP7tpVpjxIlpqJ9HHMsV7myZEI1UMOua/icjTjBe/+xgDa23jspNQCvdddZvNaqPwlLvMO7vBsRXZ3M2VZQHWOObqnjeE6micK9z2QyQmACLDOpjvgOGGgLLnz0q8D0cYIeKt4tv/d8yEWzTUC9RyKW0nSHsxv7Zplg6b4xNZxh5HviWlQuhNPuzSIFkceXQJnVQVjGp9iuHuCrrnMYeukxmowknUbpXoHDrpcawWKBZO1PubRRS2VviAzDI9hnSXRCcQWmcu6CqbrM7riYj4f8sTeyY2Jyh/ZWzwuVntmCaRUBd9AXKGebARACyKY5klGmw36moD81Bx4WXDUnx0fC1NS+9HwKGmW+M1kPbyN1btOi41TkeZpzoZx39T0uPaASCqqUvk= andrejryzikov@ip-10-146-104-247.ec2.internal"
}

resource "aws_ecr_repository" "this" {
  name = "workout_bot"
}
resource "aws_security_group" "lb" {
  vpc_id = aws_vpc.this.id
  name = "alb-sg"
  ingress {
    from_port = 80
    protocol  = "tcp"
    to_port   = 80
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port = 0
    protocol  = "-1"
    to_port   = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}
resource "aws_lb" "this" {
  name               = "test"
  load_balancer_type = "application"
  security_groups    = []
  subnets            = [aws_subnet.this.id, aws_subnet.second.id]
}