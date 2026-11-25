data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

data "aws_security_group" "app" {
  name   = var.app_security_group_name
  vpc_id = data.aws_vpc.default.id
}

data "aws_lb_target_group" "app" {
  name = var.target_group_name
}

data "aws_iam_role" "execution" {
  name = var.execution_role_name
}

data "aws_ecr_repository" "app" {
  name = var.app_name
}