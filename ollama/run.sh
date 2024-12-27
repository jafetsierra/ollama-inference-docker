sudo docker run -p 8080:8080 -d --gpus=all --name ollama ollama:latest

# create model from gguf files
ollama create ollama-32-1b-ft-v1 -f Modelfile

ollama run ollama-32-1b-ft-v1