cwlVersion: v1.0
class: CommandLineTool
hints:
  DockerRequirement:
    dockerPull: alpine:latest
baseCommand: echo
stdout: output.txt
inputs:
  message:
    type: string
    inputBinding:
      position: 1
outputs:
  output:
    type: string
    outputBinding:
      glob: output.txt
      loadContents: true
      outputEval: $(self[0].contents)
