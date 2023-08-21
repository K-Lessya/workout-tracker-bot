locals {
  tfenvfile = "${path.module}/config/tfenv.json"
  tfenv = jsondecode(file(local.tfenvfile))

}

resource "aws_iam_role" "task_role" {
  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Service": [
                    "ecs-tasks.amazonaws.com"
                ]
            },
            "Action": "sts:AssumeRole"
        }
    ]
  })
  name = "workout-bot-task-role"
}
resource "aws_iam_role_policy_attachment" "this" {
  policy_arn = aws_iam_policy.this.arn
  role       = aws_iam_role.task_role.name
}
resource "aws_iam_policy" "this" {
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "ssm:*"
        Effect = "Allow"
        Resource = "*"
      }
    ]
  })
}

resource "aws_ecs_task_definition" "this" {
  container_definitions = jsonencode(
        [
            {
                cpu               = 1400
                secrets  = [
                  {
                    name = "TESTER_ID"
                    valueFrom = aws_ssm_parameter.tester_id.arn
                  },
                  {
                    name = "TEST_USERS_ID"
                    valueFrom = aws_ssm_parameter.test_users_id.arn
                  }
                ]
                environment       = [
                  {
                    name = "MONGO_CONNECTION_STRING"
                    value = var.MONGO_CONNECTION_STRING
                  },
                  {
                    name = "PHOTO_BUCKET"
                    value = "rorychan-workout-bot"
                  },
                  {
                    name = "BOT_TOKEN",
                    value = var.BOT_TOKEN
                  },
                  {
                    name = "AWS_ACCESS_KEY_ID"
                    value = var.AWS_ACCESS_KEY_ID
                  },
                  {
                    name = "AWS_SECRET_ACCESS_KEY"
                    value = var.AWS_SECRET_ACCESS_KEY
                  },
                  {
                    name = "APP_VERSION"
                    value = var.IMAGE_TAG
                  }
                ]
                environmentFiles  = []
                essential         = true
                image             = "935625980877.dkr.ecr.us-east-1.amazonaws.com/workout_bot:${var.IMAGE_TAG}"
                logConfiguration  = {
                    logDriver     = "awslogs"
                    options       = {
                        awslogs-create-group  = "true"
                        awslogs-group         = "/ecs/"
                        awslogs-region        = "us-east-1"
                        awslogs-stream-prefix = "ecs"
                    }
                    secretOptions = []
                }
                memory            = 512
                memoryReservation = 512
                mountPoints       = []
                name              = "workout-bot"
                portMappings      = []
                ulimits           = []
                volumesFrom       = []
            },
        ]
    )
    cpu                      = "1400"
    execution_role_arn       = "arn:aws:iam::935625980877:role/ecsTaskExecutionRole"
    family                   = "workout-bot"
    memory                   = "600"
    network_mode             = "bridge"
    requires_compatibilities = [
        "EC2",
    ]
    tags                     = {}
    tags_all                 = {}
    task_role_arn = aws_iam_role.task_role.arn
    runtime_platform {
        cpu_architecture        = "X86_64"
        operating_system_family = "LINUX"
    }
}

resource "aws_ssm_parameter" "tester_id" {
  name  = "TESTER_ID"
  type  = "String"
  value = "363439865"
}

resource "aws_ssm_parameter" "test_users_id" {
  name = "TEST_USERS_ID"
  type = "String"
  value = "363439865 312380813"
}


resource "aws_ecs_service" "this" {
  name = "workout-bot"
  cluster = "arn:aws:ecs:us-east-1:935625980877:cluster/test"
  deployment_maximum_percent = 100
  deployment_minimum_healthy_percent = 0
  desired_count = 1
  enable_ecs_managed_tags = true
  health_check_grace_period_seconds = 0
  launch_type = "EC2"
  scheduling_strategy = "DAEMON"
  task_definition = aws_ecs_task_definition.this.arn
  wait_for_steady_state = false
  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }
  deployment_controller {
    type = "ECS"
  }
}