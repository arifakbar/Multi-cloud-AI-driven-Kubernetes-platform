output "vpc_id" {
  value = aws_vpc.this.id
}

output "public_subnet_id" {
  value = var.enable_public_subnet ? aws_subnet.public[0].id : null
}

output "private_subnet_ids" {
  value = { for k, v in aws_subnet.private : k => v.id }
}