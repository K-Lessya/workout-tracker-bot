locals {
  tfenvfile = "${path.module}/config/tfenv.json"
  tfenv = jsondecode(file(local.tfenvfile))

}



resource "aws_ecs_task_definition" "this" {
  container_definitions = jsonencode(
        [
            {
                cpu               = 512
                environment       = [
                  {
                    name = "MONGO_CONNECTION_STRING"
                    value = var.MONGO_CONNECTION_STRING
                  },
                  {
                    name = "PHOTO_BUCKET"
                    value = "workout-bot"
                  },
                  {
                    name = "AWS_ACCESS_KEY_ID"
                    value = var.AWS_ACCESS_KEY_ID
                  },
                  {
                    name = "AWS_SECRET_ACCESS_KEY"
                    value = var.AWS_SECRET_ACCESS_KEY
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
                memory            = 524
                memoryReservation = 262
                mountPoints       = []
                name              = "workout-bot"
                portMappings      = []
                ulimits           = []
                volumesFrom       = []
            },
        ]
    )
    cpu                      = "512"
    execution_role_arn       = "arn:aws:iam::935625980877:role/ecsTaskExecutionRole"
    family                   = "workout-bot"
    memory                   = "1024"
    network_mode             = "awsvpc"
    requires_compatibilities = [
        "EC2",
    ]
    tags                     = {}
    tags_all                 = {}

    runtime_platform {
        cpu_architecture        = "X86_64"
        operating_system_family = "LINUX"
    }
}
