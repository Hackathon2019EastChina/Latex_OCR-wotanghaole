from checkpoint import load_checkpoint

checkpoint_name = "./checkpoints/xavier-dropout-bottleneckonly-teacher0.5-0380.pth"

checkpoint = load_checkpoint(checkpoint_name, cuda=True)

encoder_checkpoint = checkpoint["model"].get("train_loss")
decoder_checkpoint = checkpoint["model"].get("train_accuracy")
encoder_checkpoint = checkpoint["model"].get("validation_loss")
decoder_checkpoint = checkpoint["model"].get("validation_accuracy")
print(encoder_checkpoint)