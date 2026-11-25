variable "region" {
  type    = string
  default = "eu-west-2"
}

variable "app_name" {
  type    = string
  default = "hello-world"
}

variable "image_tag" {
  type    = string
  default = "bootstrap"
}

variable "container_port" {
  type    = number
  default = 8080
}

variable "desired_count" {
  type    = number
  default = 1
}

variable "execution_role_name" {
  type    = string
  default = "exam-ecs-task-execution-role"
}

variable "app_security_group_name" {
  type    = string
  default = "exam-app-sg"
}

variable "target_group_name" {
  type    = string
  default = "hello-world-tg"
}