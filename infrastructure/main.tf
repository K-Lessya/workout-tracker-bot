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