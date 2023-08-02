resource "aws_ecs_task_definition" "this" {
  container_definitions = {

    name = "bot",
    image = "service-second",
    cpu=  0.2,
    memory= 128,
    essential= true,
  }

  }
  family                = "workout-bot"
}